"""Run benchmark research jobs as isolated headless agent processes.

Every job runs entirely in a fresh folder under $RPS_TMP/bench-jobs/ (default /tmp/rps)
(one per attempt, never reused): `work/` (its working folder), `delivery/`,
and copies of the engine and the attached RB. The job is given no path in the
benchmark folder. After its process has exited, the runner copies `delivery/`
into <root>/<topic>/<arm><n>/. Every prompt tells the model never to delete
anything, and guard() refuses to start a job whose folders lie outside
$RPS_TMP or whose prompt names a path under my-work.

With --client claude (the default), each job is one `claude -p` process in
restricted mode: it ignores user and project settings, starts in its job's
working folder, and its file tools reach only that folder plus the folders
added for it. It never sees any other conversation.

With --client codex, each job is one `codex exec` process that ignores the
user's config.toml, never asks for approval, and may write only to its scratch
and added folders (network and live web search on). With --client vibe, each
job is one `vibe -p` process with tools auto-approved and the added folders as
workspace roots. Vibe has no sandbox of its own (a Vibe job deleted
prompt/public on 2026-10-25), so it runs inside bubblewrap: the whole
filesystem read-only, an empty /tmp, and only its job folders and
~/.vibe/logs writable. Read limits rest on the prompt, as with the other two.

With --client opencode, each job is one `opencode run` process on a local model
(llama.cpp on the GPU server through a private network, one server slot, so one job at
a time), in the same bubblewrap sandbox, with only the job folder and OpenCode's
own state folders writable. Its cost is $0; the ledger keeps time, steps, tokens, tool calls,
searches and the largest context. With BENCH_SEARCH_HEALTH set, jobs wait while search is degraded
and a job that met degraded search is redone; a job repeating one tool call LOOP_REPEATS times is
killed as a loop. Neither reports a
cost: their ledger entries carry time, steps and (Codex only) tokens. A quota
or rate-limit failure from either ends the batch.

Per topic: stage 1 (brief, then "approved", which issues the RB), then arms
A, B and C for the requested run numbers. Finished jobs are skipped, so the
script can be rerun after a stop. Creating benchmark/STOP stops new jobs from
starting. Every job is appended to run-ledger.jsonl.

When a job hits the 5-hour session limit, no new jobs start until the reset
time the CLI reports; the interrupted jobs set their partial output aside and
run again after the reset. A weekly limit ends the batch.

Usage:
  python3 run_headless.py --topics S3 --runs 1-5 --parallel 10
  python3 run_headless.py --client codex --model gpt-6-luna --root ../runs-luna --topics S3 --runs 1
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
import paths

BENCH = paths.DATA
BASE = paths.REPO
TMP_ROOT = (os.environ.get("RPS_TMP") or "/tmp/rps").rstrip("/") + "/"   # work folders of the runs
JOBS = TMP_ROOT + "bench-jobs"
SCRATCH = TMP_ROOT + "bench-p2"   # scratch folders of the runs before 2026-10-26
ENGINE_FILES = ["research-project-instructions.txt", "research-protocol.md", "research-boundaries-template.md"]
TOOLS = "Read Write Edit Glob Grep Bash WebSearch WebFetch"
TOOLS_TEXT = ("web search, web page fetching, file reading/writing, and code execution "
              "(bash, python, pandoc, xelatex, pdftotext, mermaid-cli are installed)")
# What TOOLS_TEXT promises, as commands that must work where the jobs run (preflight(), before a batch).
# 2026-10-28: the runner machine had none of the document tools, and nothing noticed: a missing command is only a
# tool result the model reads, so the job still ends "ok".
PREFLIGHT = r"""set -e
cd "$1"
python3 -c 'print(1)' >/dev/null
python -c 'print(1)' >/dev/null
printf 'graph LR\n  A[start] --> B[end]\n' > d.mmd
mmdc -q -i d.mmd -o d.svg
printf '# Preflight\n\nAccents: é à ç.\n' > t.md
pandoc t.md -o t.pdf --pdf-engine=xelatex
pdftotext t.pdf - | grep -q Preflight
zip -q t.zip t.md
unzip -l t.zip | grep -q t.md
"""
# bash: "bash: line 3: xelatex: command not found"; dash: "/bin/sh: 1: mmdc: not found"
# Environment problems stop the batch at once and write one line to ALERTS (the watcher reads only that file).
# The benchmark environment (inputs/bench-environment.md): a job that cannot find one of these commands met an
# environment problem. Other missing commands are only recorded in the ledger.
ALERTS = os.path.join(BENCH, "ALERTS.log")
PROMISED_CMDS = {"bash", "python", "python3", "pandoc", "xelatex", "pdftotext", "mmdc", "zip", "unzip"}   # inputs/bench-environment.md
MISSING_CMD_RE = re.compile(r"([\w.+-]+): command not found|sh: \d+: ([\w.+-]+): not found")
NO_SUBAGENTS = "Do not spawn sub-agents; do all the work yourself."
NO_DELETE = ("Never delete anything, anywhere: do not run rm, rmdir, unlink, find -delete, shutil.rmtree, "
             "os.remove or any other command that deletes files or folders. Leave scratch files in place.")
ASK_BRIEF = "Please prepare a research brief for my question."
TIMEOUT_S = 3600
RESET_MARGIN_S = 180
LIMIT_RE = re.compile(r"hit your (session|weekly) limit[^\n]*?resets (\d{1,2})(?::(\d\d))?\s*(am|pm)", re.I)
QUOTA_RE = re.compile(r"\b(429|402)\b|rate.?limit|quota|usage limit|too many requests|insufficient|budget exhausted|billing", re.I)
DEFAULT_MODELS = {"claude": "claude-haiku-5-5", "codex": "gpt-6-luna", "vibe": "mistral-medium-3.5",
                  "opencode": "llamacpp/qwen3.5-9b-think"}
# llama-server in router mode, one per machine (see ~/lab/llm-presets/PRESETS.md): the request's model
# names the preset; GET /models (no /v1) lists the presets and which one is loaded.
# BENCH_LLAMACPP (JSON) overrides it on another host, e.g. the runner machine, where the tunnel is on 18080.
# The lab's search cache on the GPU server: /health answers 200 while every engine of the fixed
# set answers, 503 otherwise. Set for OpenCode rounds; jobs wait while search is degraded, and a job that
# met degraded search is set aside and redone. SEARXNG_CACHE_NS (read by searxng-mcp) names the cache namespace.
SEARCH_HEALTH = os.environ.get("BENCH_SEARCH_HEALTH")
SEARCH_DEGRADED_ATTEMPTS = 3   # a job set aside this many times for degraded search ends the batch
# Loop watchdog: a job that makes the same tool call (tool and arguments) this many times is killed
# (2026-10-28: a 4B model fetched the same two 404 URLs 1,163 times in 45 minutes).
LOOP_REPEATS = 10
SEARCH_CAP = 30          # searches per job (Brave is metered): the job is stopped there and has failed (--search-cap;
                         # 20 until 2026-10-29 07:35 UTC, raised after legitimate jobs reached it)
TIER_SEARCH_CAP = 600    # searches per runs folder, all attempts included: no job starts beyond it
MAX_FAILURES = 5         # more failed tasks than this in a runs folder stops the benchmark (--max-failures)
LLAMACPP = json.loads(os.environ.get("BENCH_LLAMACPP") or
                      '{"llamacpp": "http://localhost:8080", "llamacpp970": "http://localhost:8081"}')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_meta  # noqa: E402
import mandatory  # noqa: E402

ledger_lock = threading.Lock()
spent = {"usd": 0.0, "budget": None}
limit_lock = threading.Lock()
paused = {"until": 0.0, "weekly": False}
pace = {"usd_per_hour": None, "start": 0.0, "burst_usd": 8.0}
client = {"name": "claude", "effort": None, "approve": "approved", "mandatory_outputs": False}
# --mandatory-outputs (the local tiers, since 2026-10-29: a small push for local models is accepted):
# each arm's prompt names the files the task must deliver (mandatory.py). A deviation from the cloud rounds' prompts.
MANDATORY_OUTPUTS = {
    "A": "Mandatory output: the report as a Markdown file (.md) in {delivery}/. Without it the task has failed.",
    "B": "Mandatory output: the report as a Markdown file (.md) in {delivery}/. Without it the task has failed.",
    "C": ("Mandatory outputs, both in {delivery}/: the report <topic-slug>.md and its companion "
          "<topic-slug>.analysis.json (valid JSON), as the protocol requires. Without both the task has failed."),
}


def load_topics():
    topics = {}
    for line in open(os.path.join(paths.INPUTS, "topics.md")):
        m = re.match(r"\|\s*([TS]\d+)\s*\|[^|]*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            topics[m.group(1)] = m.group(2)
    return topics


def log(root, msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(os.path.join(root, "progress.log"), "a") as f:
        f.write(line + "\n")


def new_job(root, tid, label, rb=None):
    """A fresh job folder for one attempt: work/, delivery/, engine/ (a copy) and,
    with an RB, attached/<rb> (a copy). Returns (job, rb copy or None)."""
    base = os.path.join(JOBS, os.path.basename(root), f"{tid}-{label}")
    k = 1
    while os.path.exists(f"{base}-a{k}"):
        k += 1
    job = f"{base}-a{k}"
    for sub in ("work", "delivery", "engine"):
        os.makedirs(os.path.join(job, sub))
    for f in ENGINE_FILES:
        shutil.copyfile(os.path.join(BASE, f), os.path.join(job, "engine", f))
    if not rb:
        return job, None
    os.makedirs(os.path.join(job, "attached"))
    copy = os.path.join(job, "attached", os.path.basename(rb))
    shutil.copyfile(rb, copy)
    return job, copy


def guard(prompt, cwd, add_dirs, resume=None):
    """Refuse a job that could reach the work folders; return the prompt with the no-delete rule
    (first prompt only: appended to a short follow-up such as "approved", weak models answer the
    rule instead of the message)."""
    for d in [cwd, *add_dirs]:
        if not os.path.realpath(d).startswith(TMP_ROOT):
            raise RuntimeError(f"refusing to start a job with a folder outside {TMP_ROOT}: {d}")
    if "my-work" in prompt:
        raise RuntimeError("refusing to start a job whose prompt names a path under my-work")
    return prompt if resume else f"{prompt}\n\n{NO_DELETE}"


RB_NAMES = re.compile(r"([._-]rb\.md|[._-]br\.md|boundar[a-z]*[\w-]*\.md)$", re.I)


def misplaced_rb(job, delivery):
    """An RB the model issued outside the delivery folder or under a non-standard name (seen with
    local models): the oldest matching .md file in the job folder, the engine's template excluded."""
    found = []
    for p in glob.glob(os.path.join(job, "**", "*.md"), recursive=True):
        name = os.path.basename(p)
        if name == "research-boundaries-template.md" or not RB_NAMES.search(name):
            continue
        if os.path.dirname(p) == delivery and name.endswith(".rb.md"):
            continue   # the standard place and name: not misplaced
        found.append(p)
    return sorted(found, key=os.path.getmtime)[0] if found else None


def collect(job, dest):
    """Copy a finished job's delivery folder into the work folder; the job's process has exited."""
    shutil.copytree(os.path.join(job, "delivery"), dest, dirs_exist_ok=True)


def limit_hit(res, root):
    """If res is a usage-limit refusal, pause new jobs until the reset and return True."""
    text = str(res.get("result", "")) if res.get("is_error") else ""
    if res.get("client") in ("codex", "vibe", "opencode"):
        if not QUOTA_RE.search(text):
            return False
        with limit_lock:
            if not paused["weekly"]:
                log(root, f"{res['client']} quota or rate limit: {text[-160:]!r}; ending the batch")
            paused["weekly"] = True
        return True
    if "limit" not in text or "hit your" not in text:
        return False
    m = LIMIT_RE.search(text)
    with limit_lock:
        if "weekly" in text.lower():
            if not paused["weekly"]:
                log(root, f"weekly limit hit: {text[:120]!r}; ending the batch")
            paused["weekly"] = True
            return True
        now = datetime.datetime.now()
        if m:
            hour = int(m.group(2)) % 12 + (12 if m.group(4).lower() == "pm" else 0)
            reset = now.replace(hour=hour, minute=int(m.group(3) or 0), second=0, microsecond=0)
            if reset <= now:
                reset += datetime.timedelta(days=1)
        else:
            reset = now + datetime.timedelta(minutes=30)
        until = reset.timestamp() + RESET_MARGIN_S
        if until > paused["until"]:
            paused["until"] = until
            log(root, f"session limit hit; pausing until {time.strftime('%H:%M', time.localtime(until))}")
    return True


quota_cache = {"at": 0.0, "ok": False}
quota_lock = threading.Lock()


def quota_ok():
    """Pacing rules on the account's real usage (`claude-quota`, read at most
    every 2 minutes). In hour h of the 5-hour window, usage may be at most 20% x h,
    except during sleep hours (23:00-07:00 Europe/Paris), when the whole window may be
    used. Across the week, at most 55% until 4/7 of the cycle, 75% until 6/7, then 90%
    (each checkpoint's cap holds until the next). Only Claude jobs count. Since 2026-10-31
    the plan has no 5-hour window (claude-quota reports it null), so only the week counts.
    BENCH_WEEK_CAP overrides the weekly cap for one run (2026-10-31: the week's last 15% used
    before its reset).
    One reading at a time (parallel sessions once read a stale "ok" while the first
    reading was still running, 2026-10-27), and a failed or odd reading means wait."""
    if client["name"] != "claude":
        return True
    with quota_lock:
        if time.time() - quota_cache["at"] < 120:
            return quota_cache["ok"]
        ok = False
        try:
            q = json.loads(subprocess.run(["claude-quota"], capture_output=True, text=True, timeout=60).stdout)
            now = datetime.datetime.now(datetime.timezone.utc)
            five, week = q["five_hour"], q["seven_day"]
            if five and five.get("resets_at"):
                hour = int((now - (datetime.datetime.fromisoformat(five["resets_at"]) - datetime.timedelta(hours=5)))
                           .total_seconds() // 3600) + 1
            else:
                hour = 1   # no 5-hour window open yet
            local = now.astimezone(ZoneInfo("Europe/Paris")).hour
            window_cap = 100 if local >= 23 or local < 7 else 20 * min(max(hour, 1), 5)
            cycle = 1 - (datetime.datetime.fromisoformat(week["resets_at"]) - now).total_seconds() / (7 * 86400)
            week_cap = float(os.environ.get("BENCH_WEEK_CAP") or (55 if cycle < 4 / 7 else 75 if cycle < 6 / 7 else 90))
            five_used = five["utilization"] if five else 0
            ok = five_used < window_cap and week["utilization"] < week_cap
            if not ok:
                print(f"{time.strftime('%H:%M:%S')} quota pause: 5h {five_used}% (cap {window_cap}%), "
                      f"week {week['utilization']}% (cap {week_cap}%)", flush=True)
        except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as e:
            print(f"{time.strftime('%H:%M:%S')} quota reading failed ({e!r}); waiting", flush=True)
        quota_cache.update(at=time.time(), ok=ok)
        return ok


def wait_if_paused():
    """Block while the session limit is in force, the batch is ahead of its pace, or
    the account's real usage is over the pacing caps (quota_ok).
    Returns False if the batch must end."""
    while True:
        if paused["weekly"] or os.path.exists(os.path.join(BENCH, "STOP")):
            return False
        left = paused["until"] - time.time()
        if pace["usd_per_hour"]:
            allowed = pace["burst_usd"] + pace["usd_per_hour"] * (time.time() - pace["start"]) / 3600
            left = max(left, (spent["usd"] - allowed) / pace["usd_per_hour"] * 3600)
        if left <= 0 and quota_ok() and search_ok(wait=True):
            return True
        time.sleep(min(max(left, 60), 60))


search_state = {"degraded": None}


def search_ok(wait=False):
    """True if no search health URL is set, or it answers 200. With wait=True, a change of state is
    printed (SEARCH-DEGRADED / SEARCH-OK lines, for the watcher)."""
    if not SEARCH_HEALTH:
        return True
    out = subprocess.run(["curl", "-s", "-m", "60", "-w", "\n%{http_code}", SEARCH_HEALTH],
                         capture_output=True, text=True)
    body, _, code = out.stdout.rpartition("\n")
    degraded = None
    if code != "200":
        try:   # name the failing engines; the rest of the body (ages, counts) changes every probe
            degraded = json.dumps(json.loads(body)["degraded"], sort_keys=True)
        except (ValueError, KeyError, TypeError):
            degraded = body.strip()[:300] or f"no answer (curl exit {out.returncode})"
    if wait and degraded != search_state["degraded"]:
        print(f"{time.strftime('%H:%M:%S')} " + (f"SEARCH-DEGRADED {degraded}; waiting" if degraded else "SEARCH-OK"),
              flush=True)
        alert(f"SEARCH-DEGRADED {degraded}; jobs wait" if degraded else "SEARCH-OK again; jobs resume")
    if wait:
        search_state["degraded"] = degraded
    return degraded is None


def alert(msg):
    """One line in ALERTS.log (and stdout): something needs attention now."""
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print("ALERT " + line, flush=True)
    with open(ALERTS, "a") as f:
        f.write(line + "\n")


env_state = {"stopped": False}


def env_stop(root, msg):
    """An environment problem: alert, and start no further job (main exits with status 3)."""
    with limit_lock:
        first = not env_state["stopped"]
        env_state["stopped"] = paused["weekly"] = True
    if first:
        log(root, f"ENV-STOP {msg}")
        alert(f"ENV-STOP {os.path.basename(root)}: {msg}")


def env_missing(res):
    """The commands this job could not find that the prompt promises."""
    return sorted(set(res.get("missing_commands") or []) & PROMISED_CMDS)


def env_retry(root, job, dest, what, res, results, missing):
    """Set aside a job that met a missing command as <dest>.env-missing<k> (it is redone once the
    environment is fixed), and stop the batch."""
    k = 1
    while os.path.exists(f"{dest}.env-missing{k}"):
        k += 1
    collect(job, f"{dest}.env-missing{k}")
    tid, label = what.split("/")
    record(root, f"{prefix(root)}/{tid}/{label}.env-missing{k}", f"{dest}.env-missing{k}", res, results)
    env_stop(root, f"{what} could not find {', '.join(missing)} (set aside as {label}.env-missing{k})")


def failed_tasks(root):
    """The tasks in this runs folder whose latest recorded attempt lacks its mandatory result (mandatory.py), or
    whose RB was never issued after a failed stage 1. Set-aside attempts (labels with a dot) do not count."""
    out = []
    for meta in glob.glob(os.path.join(root, "_meta", f"{prefix(root)}_*.json")):
        tid, label = os.path.basename(meta)[:-5].rsplit("_", 2)[-2:]
        if "." in label:
            if label.startswith("stage1.failed") and not glob.glob(os.path.join(root, tid, "stage1", "*.rb.md")):
                out.append(f"{tid}/stage1")
            continue
        if label[0] in "ABC":
            gaps = mandatory.missing(label[0], os.path.join(root, tid, label), json.load(open(meta)))
            if gaps:
                out.append(f"{tid}/{label}")
    return sorted(set(out))


def tier_searches(root):
    """Searches made by every attempt recorded in this runs folder (the ledger, set-aside attempts included)."""
    n = 0
    with ledger_lock:
        for line in open(os.path.join(BENCH, "run-ledger.jsonl")) if os.path.exists(os.path.join(BENCH, "run-ledger.jsonl")) else []:
            e = json.loads(line)
            if e["label"].startswith(prefix(root) + "/"):
                n += e.get("searches") or 0
    return n


def check_limits(root):
    """Stop the batch when the runs folder has more failed tasks than MAX_FAILURES, or has spent its searches."""
    failed = failed_tasks(root)
    if len(failed) > MAX_FAILURES:
        env_stop(root, f"FAILURE-CAP {len(failed)} failed tasks (cap {MAX_FAILURES}): {', '.join(failed)}")
    if client["name"] == "opencode" and tier_searches(root) >= TIER_SEARCH_CAP:
        env_stop(root, f"SEARCH-CAP the runs folder has made {tier_searches(root)} searches (cap {TIER_SEARCH_CAP})")


def set_aside(job, dest):
    """Keep a limit-interrupted job's partial output as <dest>.limit-attempt<k>; the retry
    runs in a new job folder."""
    if os.listdir(os.path.join(job, "delivery")):
        k = 1
        while os.path.exists(f"{dest}.limit-attempt{k}"):
            k += 1
        collect(job, f"{dest}.limit-attempt{k}")
        return k
    return 0


def claude(prompt, cwd, add_dirs, model, resume=None, tools=TOOLS):
    prompt = guard(prompt, cwd, add_dirs, resume)
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--restricted", "--strict-mcp-config", "--tools", tools, "--allowedTools", tools]
    for d in add_dirs:
        cmd += ["--add-dir", d]
    if resume:
        cmd += ["--resume", resume]
    if client["effort"]:   # else the user's effortLevel setting (medium since the first rounds)
        cmd += ["--effort", client["effort"]]
    env = dict(os.environ, CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION="1000")
    start = time.time()
    try:
        out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT_S)
        res = json.loads(out.stdout) if out.stdout.strip().startswith("{") else {
            "is_error": True, "result": (out.stdout + out.stderr)[-2000:]}
    except subprocess.TimeoutExpired:
        res = {"is_error": True, "result": f"timeout after {TIMEOUT_S}s"}
    res["wall_s"] = round(time.time() - start)
    return res


def codex(prompt, cwd, add_dirs, model, resume=None):
    """One `codex exec` job; the prompt goes on stdin. Its --json output is a stream
    of events: the reply is the last agent_message, the usage is on turn.completed."""
    prompt = guard(prompt, cwd, add_dirs, resume)
    roots = json.dumps([cwd, *add_dirs])
    cmd = ["codex", "exec"] + (["resume"] if resume else []) + [
        "--json", "--skip-git-repo-check", "--ignore-user-config", "--model", model,
        "-c", 'approval_policy="never"', "-c", 'sandbox_mode="workspace-write"',
        "-c", "sandbox_workspace_write.network_access=true",
        "-c", f"sandbox_workspace_write.writable_roots={roots}", "-c", 'web_search="live"']
    if client["effort"]:   # else the model's default (gpt-6.1-sol: low; luna, astra: medium)
        cmd += ["-c", f'model_reasoning_effort="{client["effort"]}"']
    cmd += [resume, "-"] if resume else ["-"]
    start = time.time()
    res = {"client": "codex", "model": model, "is_error": True, "result": "", "steps": 0}
    try:
        out = subprocess.run(cmd, cwd=cwd, input=prompt, capture_output=True, text=True, timeout=TIMEOUT_S)
        errors = []
        for line in out.stdout.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            kind = event.get("type")
            if kind == "thread.started":
                res["session_id"] = event.get("thread_id")
            elif kind == "item.completed":
                res["steps"] += 1
                item = event.get("item") or {}
                if item.get("type") == "agent_message":
                    res["result"] = item.get("text", "")
            elif kind == "turn.completed":
                res["tokens"] = event.get("usage") or {}
                res["is_error"] = False
            elif kind in ("error", "turn.failed"):
                errors.append(json.dumps(event)[:500])
        if res["is_error"]:
            res["result"] = "\n".join(errors) or (out.stdout + out.stderr)[-2000:]
    except subprocess.TimeoutExpired:
        res["result"] = f"timeout after {TIMEOUT_S}s"
    res["wall_s"] = round(time.time() - start)
    return res


def sandbox(writable):
    """bubblewrap prefix: the whole filesystem read-only, an empty /tmp, only `writable` writable,
    and its own process space, so a timeout kill takes every process in the job with it."""
    cmd = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
           "--unshare-pid", "--die-with-parent"]
    for d in writable:
        cmd += ["--bind", d, d]
    return cmd


def preflight():
    """Check that python3, mmdc, pandoc with xelatex and pdftotext work where this batch's jobs run (in the
    bubblewrap sandbox for Vibe and OpenCode). Returns None, or what failed."""
    os.makedirs(JOBS, exist_ok=True)
    d = tempfile.mkdtemp(prefix="_preflight-", dir=JOBS)
    cmd = (sandbox([d]) if client["name"] in ("vibe", "opencode") else []) + ["bash", "-c", PREFLIGHT, "preflight", d]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return "timed out after 300 s"
    return None if out.returncode == 0 else (out.stdout + out.stderr)[-600:] or f"exit {out.returncode}"


def presets(provider):
    """The presets the provider's router offers, or None if it is unreachable."""
    try:
        out = subprocess.run(["curl", "-sf", "-m", "10", LLAMACPP[provider] + "/models"],
                             capture_output=True, text=True, check=True)
        return [m["id"] for m in json.loads(out.stdout)["data"]]
    except (subprocess.CalledProcessError, ValueError, KeyError):
        return None


def opencode(prompt, cwd, add_dirs, model, resume=None):
    """One `opencode run` job. Its --format json output is one event per line: text parts carry
    the reply, step_finish parts the tokens. --dir is the whole job folder, so the delivery,
    engine and RB folders are inside OpenCode's project and need no permission prompt."""
    prompt = guard(prompt, cwd, add_dirs, resume)
    provider, preset = model.split("/", 1)
    if preset not in (presets(provider) or []):
        # The router answers an unknown name with HTTP 400; stop before the job instead.
        paused["weekly"] = True
        return {"client": "opencode", "model": model, "is_error": True, "steps": 0, "wall_s": 0,
                "result": f"{provider} does not offer the preset {preset!r} (or is unreachable); batch stopped"}
    job = os.path.commonpath([cwd, *add_dirs])
    state = [os.path.expanduser(p) for p in ("~/.local/share/opencode", "~/.cache/opencode", "~/.local/state/opencode")]
    cmd = sandbox([job, *state]) + ["opencode", "run", "--dir", job, "--model", model, "--format", "json"]
    if resume:
        cmd += ["--session", resume]
    cmd.append(prompt)
    start = time.time()
    res = {"client": "opencode", "model": model, "is_error": True, "result": "", "steps": 0}
    # OpenCode misreads relative paths such as `cd work && mv x ../delivery/` as outside its
    # project and auto-rejects them; bubblewrap already keeps every write inside the job.
    env = dict(os.environ, OPENCODE_CONFIG_CONTENT='{"permission":{"external_directory":"allow"}}')
    # stdin closed: without a terminal, `opencode run` otherwise waits on stdin forever.
    # stderr joins stdout; its lines are not JSON and are kept only for the error text.
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    killed = {}
    timer = threading.Timer(TIMEOUT_S, lambda: (killed.setdefault("why", f"timeout after {TIMEOUT_S}s"), proc.kill()))
    timer.start()
    texts, tokens, errors, step_text, raw = [], {}, [], [], []
    tools, calls, search_log, missing = {}, {}, [], set()
    max_context = 0
    for line in proc.stdout:
        raw.append(line)
        del raw[:-200]
        try:
            event = json.loads(line)
        except ValueError:
            continue
        res["session_id"] = event.get("sessionID") or res.get("session_id")
        part = event.get("part") or {}
        if event.get("type") == "step_start":
            step_text = []
        elif event.get("type") == "text" and part.get("text", "").strip():
            step_text.append(part["text"])
        elif event.get("type") == "tool_use":
            # one event per finished tool call (completed or error)
            name, state = part.get("tool", "?"), part.get("state") or {}
            tools[name] = tools.get(name, 0) + 1
            if "search" in name and "url" not in name:
                search_log.append({"query": (state.get("input") or {}).get("query"), "status": state.get("status"),
                                   "error": str(state.get("error") or "")[:300] or None})
                if len(search_log) >= SEARCH_CAP and "why" not in killed:
                    killed["why"] = f"search cap: {len(search_log)} searches (cap {SEARCH_CAP})"
                    proc.kill()
            if name == "bash":
                text = str(state.get("output") or "") + str(state.get("error") or "")
                missing.update(a or b for a, b in MISSING_CMD_RE.findall(text))
            sig = name + " " + json.dumps(state.get("input"), sort_keys=True)
            calls[sig] = calls.get(sig, 0) + 1
            if calls[sig] >= LOOP_REPEATS and "why" not in killed:
                killed["why"] = f"loop: the same call made {calls[sig]} times: {sig[:300]}"
                proc.kill()
        elif event.get("type") == "step_finish":
            res["steps"] += 1
            if step_text:
                texts.append("".join(step_text))
            t = part.get("tokens") or {}
            for k, v in (("input", t.get("input")), ("output", t.get("output")),
                         ("reasoning", t.get("reasoning")), ("cache_read", (t.get("cache") or {}).get("read"))):
                tokens[k] = tokens.get(k, 0) + (v or 0)
            # the context this call was given: its fresh input plus what was read from the prompt cache
            max_context = max(max_context, (t.get("input") or 0) + ((t.get("cache") or {}).get("read") or 0))
        elif event.get("type") == "error":
            errors.append(json.dumps(event)[:500])
    proc.wait()
    timer.cancel()
    res.update(tokens=tokens, tool_calls=sum(tools.values()), tools=tools, max_context=max_context,
               searches=len(search_log), search_errors=sum(1 for q in search_log if q["status"] == "error"),
               search_log=search_log, missing_commands=sorted(missing))
    if killed:
        res["result"] = killed["why"]
        res[{"loop": "loop", "search": "search_cap"}.get(killed["why"].split(" ")[0].rstrip(":"), "timeout")] = True
    elif proc.returncode == 0 and texts and not errors:
        res.update(is_error=False, result=texts[-1])
    else:
        res["result"] = "\n".join(errors) or "".join(raw)[-2000:]
    # Search failures the model saw, or a degraded state right after the job: the job did not get
    # the fixed engine set, so it is redone (run_arm_once, stage1_once).
    degraded = [q["error"] for q in search_log if q["error"] and "degraded" in q["error"].lower()]
    if degraded or not search_ok():
        res["search_degraded"] = degraded[0] if degraded else "search health degraded right after the job"
    res["wall_s"] = round(time.time() - start)
    return res


def vibe(prompt, cwd, add_dirs, model, resume=None):
    """One `vibe -p` job. Its --output json is the history entries; the reply is the
    text of the last assistant message, whose content is a list of text parts."""
    prompt = guard(prompt, cwd, add_dirs, resume)
    cmd = sandbox([cwd, *add_dirs, os.path.expanduser("~/.vibe/logs")]) + ["vibe", "-p", prompt, "--output", "json", "--auto-approve", "--trust", "--workdir", cwd]
    for d in add_dirs:
        cmd += ["--add-dir", d]
    if resume:
        cmd += ["--resume", resume]
    # Vibe 3 loads its server model catalogue (GLM, ...) only with this flag, which the
    # interactive client sets and headless mode does not. Preview models (Mistral Large 4)
    # arrive through Vibe's feature flags, which load only with telemetry on, so telemetry
    # keeps the user's own setting. Without either, an unlisted model silently falls back
    # to a default model (vibe_model_used() records what really ran).
    env = dict(os.environ, VIBE_ACTIVE_MODEL=model, VIBE_EXPERIMENTAL_ENABLE_MODEL_CATALOG="true",
               VIBE_ENABLE_UPDATE_CHECKS="false", VIBE_ENABLE_NOTIFICATIONS="false")
    start = time.time()
    res = {"client": "vibe", "model": model, "is_error": True, "result": "", "steps": 0}
    try:
        out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT_S)
        try:
            history = json.loads(out.stdout)
        except ValueError:
            history = None
        history = history.get("history") if isinstance(history, dict) else history
        entries = [m for m in history or [] if isinstance(m, dict)]
        # Steps: what the model produced in this call's turn, reasoning aside (assistant
        # messages, tool calls); a resumed history also holds the earlier turns.
        turn = entries[-1].get("turnId") if entries else None
        res["steps"] = sum(1 for m in entries if m.get("turnId") == turn
                           and m.get("role") != "user" and m.get("type") != "reasoning")
        texts = []
        for m in entries:
            if m.get("role") == "assistant":
                parts = m.get("content")
                parts = [{"text": parts}] if isinstance(parts, str) else parts or []
                text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
                if text.strip():
                    texts.append(text)
        if out.returncode == 0 and texts:
            res.update(is_error=False, result=texts[-1], session_id=entries[-1].get("sessionId"))
            res["model"] = vibe_model_used(res["session_id"]) or model
            if res["model"] != model:
                # Vibe fell back to another model: the job is not a sample of the requested one
                res.update(is_error=True, result=f"Vibe ran {res['model']} instead of {model}")
                paused["weekly"] = True
        else:
            res["result"] = (out.stdout + out.stderr)[-2000:]
    except subprocess.TimeoutExpired:
        res["result"] = f"timeout after {TIMEOUT_S}s"
    res["wall_s"] = round(time.time() - start)
    return res


def vibe_model_used(session_id):
    """The model a Vibe session actually ran, from its session log. Vibe silently
    falls back to its default for an unknown VIBE_ACTIVE_MODEL, so the requested
    name alone is not evidence."""
    found = None
    folder = os.path.expanduser(f"~/.vibe/logs/session/unified/{session_id}")
    for path in sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True)):
        if os.path.isfile(path):
            with open(path, errors="ignore") as f:
                found = (re.findall(r'"active_model":\s*"([^"]+)"', f.read()) or [found])[-1]
    return found


def agent(prompt, cwd, add_dirs, model, resume=None):
    """A research job on the batch's client."""
    if not os.path.isdir(cwd):
        # The model moved or removed its own working folder (seen with a 2B local model).
        return {"client": client["name"], "model": model, "is_error": True, "steps": 0, "wall_s": 0,
                "result": f"working folder {cwd} no longer exists"}
    if client["name"] == "codex":
        return codex(prompt, cwd, add_dirs, model, resume)
    if client["name"] == "vibe":
        return vibe(prompt, cwd, add_dirs, model, resume)
    if client["name"] == "opencode":
        return opencode(prompt, cwd, add_dirs, model, resume)
    return claude(prompt, cwd, add_dirs, model, resume)


def record(root, label, delivery, res, cli_results, kind="research"):
    meta_dir = os.path.join(root, "_meta")
    os.makedirs(meta_dir, exist_ok=True)
    with open(os.path.join(meta_dir, label.replace("/", "_") + ".json"), "w") as f:
        json.dump(cli_results, f, indent=1)
    if cli_results and cli_results[0].get("client") in ("codex", "vibe", "opencode"):
        return record_other(root, label, delivery, res, cli_results, kind)
    pricing = json.load(open(os.path.join(paths.INPUTS, "pricing.json")))
    entry = {"label": label, "kind": kind, "output": os.path.relpath(delivery, BENCH)}
    logs = [p for r in cli_results if r.get("session_id")
            for p in glob.glob(os.path.expanduser(f"~/.claude/projects/*/{r['session_id']}.jsonl"))]
    if logs:
        parts = [run_meta.summarize(p, pricing) for p in sorted(set(logs))]
        entry.update(merge(parts))
    entry["cli_cost_usd"] = round(sum(r.get("total_cost_usd") or 0 for r in cli_results), 4)
    # The CLI figure is the cost of record: the session log omits Claude Code's
    # internal Haiku 4.5 web-tool calls and long-context pricing.
    entry["log_cost_usd"] = entry.get("cost_usd")
    entry["cost_usd"] = entry["cli_cost_usd"]
    entry["cost_note"] = ("Claude Code CLI total_cost_usd at list prices; includes Claude Code's internal "
                          "Haiku 4.5 calls for web search/fetch and long-context pricing")
    entry["ok"] = not res.get("is_error")
    with ledger_lock, open(os.path.join(BENCH, "run-ledger.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")
        spent["usd"] += entry["cost_usd"]
    return entry


def record_other(root, label, delivery, res, cli_results, kind):
    """Ledger entry for a Codex or Vibe job: time, steps and tokens, no cost."""
    first = cli_results[0]
    tokens = {}
    for r in cli_results:
        for k, v in (r.get("tokens") or {}).items():
            tokens[k] = tokens.get(k, 0) + v
    steps = sum(r.get("steps", 0) for r in cli_results)
    extra = {}
    if first["client"] == "opencode":
        tools = {}
        for r in cli_results:
            for k, v in (r.get("tools") or {}).items():
                tools[k] = tools.get(k, 0) + v
        extra = {"tool_calls": sum(tools.values()), "tools": tools,
                 "searches": sum(r.get("searches", 0) for r in cli_results),
                 "search_errors": sum(r.get("search_errors", 0) for r in cli_results),
                 "max_context": max((r.get("max_context", 0) for r in cli_results), default=0),
                 "missing_commands": sorted({c for r in cli_results for c in r.get("missing_commands", [])})}
        if any(r.get("loop") for r in cli_results):
            extra["loop"] = True
    entry = {"label": label, "kind": kind, "output": os.path.relpath(delivery, BENCH),
             "client": first["client"], "models": {first["model"]: steps}, "steps": steps,
             "duration_s": sum(r.get("wall_s", 0) for r in cli_results), "tokens": tokens or None,
             "cost_usd": None,
             "cost_note": (f"{first['client']} reports no cost; steps = completed events"
                           + {"codex": " (Codex items)", "vibe": " (Vibe assistant messages)",
                              "opencode": " (OpenCode steps; local model, $0)"}[first["client"]]
                           + ("" if tokens else "; no token usage reported")),
             "ok": not res.get("is_error"), **extra}
    with ledger_lock, open(os.path.join(BENCH, "run-ledger.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def merge(parts):
    if len(parts) == 1:
        return parts[0]
    out = {"models": {}, "api_calls": 0, "start": min(p["start"] for p in parts),
           "end": max(p["end"] for p in parts), "duration_s": sum(p["duration_s"] for p in parts),
           "tokens": {}, "cost_usd": 0.0, "cost_note": parts[0]["cost_note"]}
    for p in parts:
        out["api_calls"] += p["api_calls"]
        out["cost_usd"] = round(out["cost_usd"] + p["cost_usd"], 4)
        for k, v in p["models"].items():
            out["models"][k] = out["models"].get(k, 0) + v
        for k, v in p["tokens"].items():
            out["tokens"][k] = out["tokens"].get(k, 0) + v
    return out


def prefix(root):
    """Ledger label prefix: runs-haiku -> research-haiku."""
    return "research-" + os.path.basename(root).removeprefix("runs-")


def project_setup(engine):
    return (f"- Project instructions (treat these exactly as your project/custom instructions): "
            f"{engine}/research-project-instructions.txt\n"
            f"- Project source files: {engine}/research-protocol.md and {engine}/research-boundaries-template.md")


def stage1(root, tid, question, model):
    while True:
        if not wait_if_paused():
            return None
        rb, limited = stage1_once(root, tid, question, model)
        if not limited:
            return rb


def stage1_once(root, tid, question, model):
    dest = os.path.join(root, tid, "stage1")
    if glob.glob(os.path.join(dest, "*.rb.md")):
        return glob.glob(os.path.join(dest, "*.rb.md"))[0], False
    job, _ = new_job(root, tid, "stage1")
    cwd, delivery, engine = (os.path.join(job, d) for d in ("work", "delivery", "engine"))
    prompt = f"""You are the assistant inside a research project. This is a benchmark run; play the role faithfully.

Your project setup:
{project_setup(engine)}
- Your tools: web search, file reading/writing, and code execution (bash, python, pandoc, xelatex, pdftotext, mermaid-cli are installed). File delivery to the user: any file you write into {delivery}/ is delivered to the user, who can open it there. Write no files anywhere else, except scratch files under {cwd}/.
- Do not read or write anything outside {job}/.
- {NO_SUBAGENTS}

The user's first message in this project is:

"{question}"

Respond exactly as the project instructions and protocol direct. Your final message is your reply to the user, shown to them verbatim: give the reply itself, not a summary of it."""
    dirs = [delivery, engine]
    first = agent(prompt, cwd, dirs, model)
    results = [first]
    # The user approves whatever the assistant proposes. The engine may first
    # answer briefly and only offer a brief, or answer "nothing to approve" before
    # offering one, so allow up to three approvals. If the engine still treats the
    # question as a quick one and issues no RB (Luna, T9: added 2026-10-24, after
    # every Haiku, Sonnet and Vibe RB was already written), the user asks for a
    # brief and approves it.
    last = first
    for message in [client["approve"]] * 3 + [ASK_BRIEF] + [client["approve"]] * 2:
        if last.get("is_error") or glob.glob(os.path.join(delivery, "*.rb.md")) or misplaced_rb(job, delivery):
            break
        with open(os.path.join(delivery, "brief-BR-001.md"), "w") as f:
            f.write(last.get("result", ""))
        last = agent(message, cwd, dirs, model, resume=last.get("session_id"))
        results.append(last)
    rbs = glob.glob(os.path.join(delivery, "*.rb.md"))
    if not rbs and misplaced_rb(job, delivery):
        # Use it under the standard name, and say so in the progress log.
        src = misplaced_rb(job, delivery)
        name = re.sub(r"([._-]rb|[._-]br)?\.md$", "", os.path.basename(src)) + ".rb.md"
        shutil.copyfile(src, os.path.join(delivery, name))
        log(root, f"{tid} stage1: RB issued as {os.path.relpath(src, job)}; copied to the delivery folder as {name}")
        rbs = glob.glob(os.path.join(delivery, "*.rb.md"))
    if rbs and mandatory.rb_name_problem(rbs[0]):
        log(root, f"{tid} stage1: RB {mandatory.rb_name_problem(rbs[0])}; the task has failed")
        rbs = []
    res = {"is_error": not rbs}
    missing = sorted({c for r in results for c in env_missing(r)})
    if missing:
        env_retry(root, job, dest, f"{tid}/stage1", res, results, missing)
        return None, False
    if any(r.get("search_degraded") for r in results):
        return None, search_retry(root, job, dest, f"{tid}/stage1", res, results)
    if not rbs and limit_hit(last, root):
        k = set_aside(job, dest)
        record(root, f"{prefix(root)}/{tid}/stage1.limit-attempt{k}", f"{dest}.limit-attempt{k}", res, results)
        log(root, f"{tid} stage1 interrupted by usage limit; will retry")
        return None, True
    if not rbs:
        # A stage 1 without an RB is a failure: keep it as stage1.failed<k>, so the next call retries cleanly.
        k = 1
        while os.path.exists(f"{dest}.failed{k}"):
            k += 1
        collect(job, f"{dest}.failed{k}")
        record(root, f"{prefix(root)}/{tid}/stage1.failed{k}", f"{dest}.failed{k}", res, results)
        log(root, f"{tid} stage1 FAILED: no RB (attempt set aside as stage1.failed{k}; retried on the next pass)")
        check_limits(root)
        return None, False
    collect(job, dest)
    record(root, f"{prefix(root)}/{tid}/stage1", dest, res, results)
    log(root, f"{tid} stage1 RB {os.path.basename(rbs[0])}")
    check_limits(root)
    return (os.path.join(dest, os.path.basename(rbs[0])) if rbs else None), False


def search_retry(root, job, dest, what, res, results):
    """Set aside a job that met degraded search as <dest>.search-degraded<k>. Returns True (redo it,
    once search is healthy), or False after SEARCH_DEGRADED_ATTEMPTS, which also ends the batch."""
    k = 1
    while os.path.exists(f"{dest}.search-degraded{k}"):
        k += 1
    collect(job, f"{dest}.search-degraded{k}")
    tid, label = what.split("/")
    record(root, f"{prefix(root)}/{tid}/{label}.search-degraded{k}", f"{dest}.search-degraded{k}", res, results)
    reason = next(r["search_degraded"] for r in results if r.get("search_degraded"))
    if k >= SEARCH_DEGRADED_ATTEMPTS:
        env_stop(root, f"{what} met degraded search {k} times ({reason[:160]})")
        return False
    log(root, f"{what} set aside: search degraded ({reason[:160]}); will redo it")
    return True


def run_arm(root, tid, question, arm, n, rb, model):
    while wait_if_paused():
        if not run_arm_once(root, tid, question, arm, n, rb, model):
            return


def run_arm_once(root, tid, question, arm, n, rb, model):
    """Run one job. Returns True if it was interrupted by the usage limit."""
    label = f"{arm}{n}"
    dest = os.path.join(root, tid, label)
    if os.path.exists(os.path.join(root, "_meta", f"{prefix(root)}_{tid}_{label}.json")):
        return False
    if os.path.exists(os.path.join(BENCH, "STOP")):
        log(root, f"{tid} {label} skipped: STOP file present")
        return False
    if spent["budget"] is not None and spent["usd"] >= spent["budget"]:
        log(root, f"{tid} {label} skipped: batch budget ${spent['budget']} reached")
        return False
    check_limits(root)
    if paused["weekly"]:
        return False
    job, rb = new_job(root, tid, label, rb if arm != "A" else None)
    cwd, delivery, engine = (os.path.join(job, d) for d in ("work", "delivery", "engine"))
    head = (f"Files you write into {delivery}/ are delivered to the user. Write no files anywhere else, "
            f"except scratch files under {cwd}/."
            + (" " + MANDATORY_OUTPUTS[arm].format(delivery=delivery) if client["mandatory_outputs"] else ""))
    if arm == "A":
        dirs = [delivery]
        prompt = f"""Your tools: {TOOLS_TEXT}. {head} Do not read anything on this computer outside that delivery folder. {NO_SUBAGENTS}

The user writes:

"{question} Research this and write me a report as a Markdown file."

Do the work. Your final message is your reply to the user."""
    elif arm == "B":
        dirs = [delivery, os.path.dirname(rb)]
        prompt = f"""Your tools: {TOOLS_TEXT}. {head} Do not read anything on this computer except the attached file below and that delivery folder. {NO_SUBAGENTS}

The user attaches this file: {rb}

and writes:

"Carry out the research this file describes and write the report as a Markdown file."

Do the work. Your final message is your reply to the user."""
    else:
        dirs = [delivery, os.path.dirname(rb), engine]
        prompt = f"""You are the assistant inside a research project. This is a benchmark run; play the role faithfully.

Your project setup:
{project_setup(engine)}
- Your tools: {TOOLS_TEXT}. {head} Do not read anything on this computer except the files named here and that delivery folder.
- {NO_SUBAGENTS}

This is a new conversation in the project. The user attaches this file: {rb}

and writes:

"execute"

Respond exactly as the project instructions and protocol direct. Your final message is your reply to the user."""
    res = agent(prompt, cwd, dirs, model)
    if env_missing(res):
        env_retry(root, job, dest, f"{tid}/{label}", res, [res], env_missing(res))
        return False
    if res.get("search_degraded"):
        return search_retry(root, job, dest, f"{tid}/{label}", res, [res])
    if limit_hit(res, root):
        k = set_aside(job, dest)
        entry = record(root, f"{prefix(root)}/{tid}/{label}.limit-attempt{k}", f"{dest}.limit-attempt{k}", res, [res])
        log(root, f"{tid} {label} interrupted by usage limit after {res['wall_s']}s "
                  f"${entry.get('cost_usd', '?')}; will retry")
        return True
    with open(os.path.join(delivery, "_reply.md"), "w") as f:
        f.write(res.get("result", ""))
    collect(job, dest)
    entry = record(root, f"{prefix(root)}/{tid}/{label}", dest, res, [res])
    import rescue_misplaced   # here: it imports this module
    for note in rescue_misplaced.rescue_one(root, tid, label):
        log(root, f"rescued {note[2:]}")
    reports = [p for p in glob.glob(os.path.join(dest, "*.md")) if not p.endswith("_reply.md")]
    gaps = mandatory.missing(arm, dest, [res])
    log(root, f"{tid} {label} {'ok' if entry['ok'] else 'ERROR'} reports={len(reports)} "
              + (f"FAILED (missing: {'; '.join(gaps)}) " if gaps else "")
              + f"{res['wall_s']}s ${entry.get('cost_usd', '?')}"
              + (f" MISSING-COMMANDS {','.join(res['missing_commands'])}" if res.get("missing_commands") else ""))
    check_limits(root)
    return False


def parse_runs(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def main():
    global TIMEOUT_S
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", required=True, help="comma-separated topic IDs, or 'all'")
    ap.add_argument("--runs", default="1-5")
    ap.add_argument("--arms", default="ABC")
    ap.add_argument("--parallel", type=int, default=10)
    ap.add_argument("--client", choices=sorted(DEFAULT_MODELS), default="claude")
    ap.add_argument("--model", help="default per client: " + ", ".join(f"{c} {m}" for c, m in DEFAULT_MODELS.items()))
    ap.add_argument("--root", default=os.path.join(BENCH, "runs-haiku"))
    ap.add_argument("--pace-usd-per-hour", type=float,
                    help="start jobs no faster than this list-price spend rate (a 5-hour window is about $150 of Haiku)")
    ap.add_argument("--effort", help="reasoning effort for Codex and Claude (low, medium, high, xhigh, ...); default: the model's own")
    ap.add_argument("--approve-message", default="approved",
                    help="the user's stage-1 approval (a deviation from the standard 'approved'; log it in NOTES.md)")
    ap.add_argument("--timeout", type=int, default=TIMEOUT_S, help="seconds before a job is killed")
    ap.add_argument("--mandatory-outputs", action="store_true",
                    help="name each arm's mandatory output files in its prompt (a deviation; log it in NOTES.md)")
    ap.add_argument("--search-cap", type=int, default=SEARCH_CAP, help="searches per job before it is stopped (failed)")
    ap.add_argument("--max-failures", type=int, default=MAX_FAILURES,
                    help="stop when the runs folder has more failed tasks than this (mandatory.py)")
    ap.add_argument("--budget-usd", type=float, help="stop starting jobs once this batch has spent this much (list price)")
    a = ap.parse_args()
    client["name"] = a.client
    client["effort"] = a.effort
    client["approve"] = a.approve_message
    client["mandatory_outputs"] = a.mandatory_outputs
    if a.client == "opencode":
        a.parallel = 1   # each machine has one slot; parallel jobs would only queue and swap models
        provider, preset = a.model.split("/", 1)
        if provider not in LLAMACPP:
            sys.exit(f"unknown provider {provider!r}; known: {', '.join(LLAMACPP)}")
        offered = presets(provider)
        if offered is None:
            sys.exit(f"{provider} not reachable at {LLAMACPP[provider]}: is NordVPN Meshnet on, and the SSH tunnel open?")
        if preset not in offered:
            sys.exit(f"{provider} has no preset {preset!r}; it offers: {', '.join(offered)}")
    TIMEOUT_S = a.timeout
    globals()["MAX_FAILURES"] = a.max_failures
    globals()["SEARCH_CAP"] = a.search_cap
    failed = preflight()
    if failed:
        alert(f"ENV-STOP preflight failed on {a.root}: {failed.strip()[-200:]}")
        print(f"preflight failed: the jobs' prompt promises tools that do not work here:\n{failed}", flush=True)
        sys.exit(3)
    a.model = a.model or DEFAULT_MODELS[a.client]
    a.root = os.path.abspath(a.root)  # sessions run in scratch folders; a relative root would resolve there
    topics = load_topics()
    ids = [t for t in topics if t[0] in "TS"] if a.topics == "all" else a.topics.split(",")
    os.makedirs(a.root, exist_ok=True)
    spent["budget"] = a.budget_usd
    pace.update(usd_per_hour=a.pace_usd_per_hour, start=time.time())
    log(a.root, f"start topics={','.join(ids)} runs={a.runs} arms={a.arms} parallel={a.parallel} "
                f"client={a.client} model={a.model} effort={a.effort or 'default'} budget={a.budget_usd} pace={a.pace_usd_per_hour}/h"
                + (" mandatory-outputs=on" if a.mandatory_outputs else "") + f" search-cap={a.search_cap}")
    with ThreadPoolExecutor(max_workers=a.parallel) as pool:
        rbs = dict(zip(ids, pool.map(lambda t: stage1(a.root, t, topics[t], a.model), ids)))
        jobs = [pool.submit(run_arm, a.root, t, topics[t], arm, n, rbs[t], a.model)
                for t in ids for n in parse_runs(a.runs) for arm in a.arms
                if rbs[t] or arm == "A"]
        for j in jobs:
            j.result()
    log(a.root, f"done, batch spent ${spent['usd']:.2f}")
    if env_state["stopped"]:
        sys.exit(3)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:   # a crash is an environment problem too: say so before the traceback
        alert(f"ENV-STOP run_headless crashed: {e!r}"[:300])
        raise
