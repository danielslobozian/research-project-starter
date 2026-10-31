"""Price per report for every model x arm on the cross-model topics, in USD, with where it comes from.

- Claude: the cost Claude Code reports for the job (run ledger).
- GPT-6 (Codex): the job's tokens (run ledger) at OpenAI's standard prices (inputs/pricing.json).
- Mistral Vibe (Mistral Medium, Large 4, GLM Flash): each Vibe session's tokens (vibe-sessions.jsonl, from
  extract_vibe_sessions.py), scaled per billed model and token kind to the usage on the Mistral console, at
  one published price per model (inputs/costs.json), converted from EUR.
- Local models: the GPU's measured energy over the round, shared across its jobs by duration, at the
  electricity price, plus the Brave Search API calls the job's queries caused (inputs/costs.json).

A job counts once (its last ledger entry); failed jobs (inputs/failed-jobs.json) are left out, but the
Mistral sessions and the local energy of their attempts are paid by the reports. B and C also carry the mean
price of the model's RB (stage 1); Sol High reused Sol's RBs.

Usage:
  python3 report_prices.py
Writes benchmarks/<edition>/results/prices.json in the repository and prints the table.
"""
import collections
import datetime
import glob
import json
import os
import re
import statistics

from grading_common import FAILED, report_file
import paths

TOPICS = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
PRICING = json.load(open(os.path.join(paths.INPUTS, "pricing.json")))
COSTS = json.load(open(os.path.join(paths.INPUTS, "costs.json")))
USD = COSTS["eur_usd"]["rate"]
CLAUDE = ("haiku", "sonnet", "opus", "haiku-xhigh")
CODEX = ("sol", "sol-high", "astra", "luna", "luna-xhigh")
VIBE = tuple(COSTS["mistral_console"]["published_price"])[1:]   # skip "_about"
LOCAL = ("qwen3.5-9b-think", "qwen3.5-4b-think-262k", "gemma-4-12b-guarded")
RB_FROM = {"sol-high": "sol"}
KINDS = ("cached_input", "input", "output")
JOB_RE = re.compile(r"runs-([a-z0-9.-]+?)[/-]((?:T|S)\d+)-(stage1|[ABC]\d)(?:-a\d+)?(?:/|$)")


def when(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def jobs():
    """{(model, topic, job): its last ledger entry ({} if none)} for the published jobs: a folder of the
    model's round on a cross-model topic holding its RB (stage 1) or a report, and not a failed job."""
    ledger = {}
    for line in open(os.path.join(paths.DATA, "run-ledger.jsonl")):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        parts = e.get("label", "").split("/")
        if len(parts) == 3 and parts[0].startswith("research-"):
            ledger[(parts[0].removeprefix("research-"), parts[1], parts[2])] = e
    out = {}
    for model in CLAUDE + CODEX + VIBE + LOCAL:
        for topic in TOPICS:
            for job in ["stage1"] + [f"{arm}{run}" for arm in "ABC" for run in range(1, 6)]:
                folder = os.path.join(paths.DATA, f"runs-{model}", topic, job)
                delivered = glob.glob(os.path.join(folder, "*.rb.md")) if job == "stage1" else report_file(folder)
                if job == "stage1" and model in RB_FROM:   # reused another model's RBs
                    continue
                if os.path.isdir(folder) and delivered and (model, topic, job) not in FAILED:
                    out[(model, topic, job)] = ledger.get((model, topic, job), {})
    return out


def codex_usd(e):
    model = next(iter(e.get("models") or {}), "")
    p, t = PRICING[model], e["tokens"]
    cached = t.get("cached_input_tokens", 0)
    return ((t["input_tokens"] - cached) * p["input"] + cached * p["cache_read"]
            + t["output_tokens"] * p["output"]) / 1e6


def vibe_usd():
    """{(model, topic, job): USD} over every Vibe session of the job, attempts included."""
    console = COSTS["mistral_console"]
    sessions = [json.loads(line) for line in open(os.path.join(paths.DATA, "vibe-sessions.jsonl"))]
    journal = collections.defaultdict(lambda: [0, 0, 0])
    for s in sessions:
        for i, k in enumerate(KINDS):
            journal[s["model"]][i] += s["tokens"][k]
    scale = {m: [b["usage_m"][i] * 1e6 / journal[m][i] if journal[m][i] else 0 for i in range(3)]
             for m, b in console["billed"].items()}
    out = collections.defaultdict(float)
    for s in sessions:
        m = JOB_RE.search(s["workdir"])
        if not m or m.group(1) not in VIBE or m.group(2) not in TOPICS:
            continue
        price = console["billed"][console["published_price"][m.group(1)]]["eur_per_m"]
        eur = sum(s["tokens"][k] * scale[s["model"]][i] * price[i] for i, k in enumerate(KINDS)) / 1e6
        out[(m.group(1), m.group(2), m.group(3))] += eur * USD
    return out


def local_usd(done):
    """{(model, topic, job): [energy USD, search USD]}: the GPU energy and the Brave calls of the periods
    the model's preset was serving, shared across its jobs by duration and by searches; plus the number of
    Brave calls, and of those made while no local model was serving (pilots and tests)."""
    lab, cfg = os.path.join(paths.DATA, "lab"), COSTS["local"]
    upstream = [json.loads(line) for line in open(os.path.join(lab, "search", "upstream.jsonl"))]
    brave = [u for u in upstream if u["ns"] == cfg["search_namespace"] and "braveapi" in u["results_per_engine"]]
    brave_on = min(when(u["t"]) for u in brave)
    samples = []
    for f in sorted(glob.glob(os.path.join(lab, "health", "*.jsonl"))):
        for line in open(f):
            try:
                h = json.loads(line)
            except ValueError:
                continue
            gpu = next((g for g in h.get("gpus") or [] if g.get("name") == cfg["gpu_name"]), None)
            if gpu and gpu.get("power_w") is not None:
                samples.append((when(h["ts"]), gpu["power_w"]))
    samples.sort()
    requests = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(lab, "llm", "*.jsonl"))):
        for line in open(f):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("preset") in LOCAL and r.get("start") and r.get("end") and when(r["start"]) >= brave_on:
                requests[r["preset"]].append((when(r["start"]), when(r["end"])))
    out, explained = {}, 0
    for model in LOCAL:
        periods = []
        for s, e in sorted(requests[model]):   # requests less than 15 minutes apart: one working period
            if periods and (s - periods[-1][1]).total_seconds() < 900:
                periods[-1][1] = max(periods[-1][1], e)
            else:
                periods.append([s, e])
        joules = 0.0
        for (t0, w), (t1, _) in zip(samples, samples[1:]):
            if any(s <= t0 < e for s, e in periods):
                joules += w * min((t1 - t0).total_seconds(), 60)
        energy_usd = joules / 3.6e6 * cfg["eur_per_kwh"] * USD
        calls = sum(1 for u in brave if any(s <= when(u["t"]) < e for s, e in periods))
        explained += calls
        mine = {k: e for k, e in done.items() if k[0] == model}
        total_s = sum(e.get("duration_s") or 0 for e in mine.values())
        total_q = sum(e.get("searches") or 0 for e in mine.values())
        for k, e in mine.items():
            out[k] = [energy_usd * (e.get("duration_s") or 0) / total_s,
                      calls * cfg["brave_usd_per_call"] * (e.get("searches") or 0) / total_q]
    return out, len(brave), len(brave) - explained


def main():
    done = jobs()
    vibe = vibe_usd()
    local, brave_calls, unexplained = local_usd(done)
    per_job = {}
    for k, e in done.items():
        model = k[0]
        if model in CLAUDE:
            per_job[k] = e.get("cost_usd")
        elif model in CODEX:
            per_job[k] = codex_usd(e) if e.get("tokens") else None
        elif model in VIBE:
            per_job[k] = vibe.get(k)
        elif model in LOCAL:
            per_job[k] = sum(local[k])
    source = {**{m: "Claude Code's reported cost" for m in CLAUDE},
              **{m: "tokens at OpenAI standard prices (pricing.json)" for m in CODEX},
              **{m: "Mistral console usage, one price per model, EUR at the ECB October 2026 mean" for m in VIBE},
              **{m: "measured GPU energy at EUR 0.20/kWh + Brave API calls at $5/1000" for m in LOCAL}}
    prices = {}
    for model in CLAUDE + CODEX + VIBE + LOCAL:
        rb = [v for (m, _, j), v in per_job.items() if m == RB_FROM.get(model, model) and j == "stage1" and v is not None]
        for arm in "ABC":
            v = [p for (m, _, j), p in per_job.items() if m == model and j[0] == arm and p is not None]
            if not v:
                continue
            item = {"usd": statistics.mean(v) + (statistics.mean(rb) if arm in "BC" and rb else 0), "jobs": len(v),
                    "source": source[model]}
            if arm in "BC":
                item["rb_usd"] = statistics.mean(rb) if rb else None
            if model in LOCAL:
                parts = [local[k] for k in done if k[0] == model and k[2][0] == arm]
                item["energy_usd"] = statistics.mean(p[0] for p in parts)
                item["search_usd"] = statistics.mean(p[1] for p in parts)
            prices[f"{model}:{arm}"] = item
    out = os.path.join(paths.REPO, "benchmarks", paths.EDITION, "results", "prices.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"_about": __doc__.split("\n\n")[0], "eur_usd": USD, "topics": TOPICS,
                   "brave_calls": brave_calls, "brave_calls_outside_rounds": unexplained, "prices": prices}, f, indent=1)
    print(f"Brave: {brave_calls} calls, {unexplained} made while no local model was serving")
    missing = [k for k, v in per_job.items() if v is None]
    if missing:
        print(f"{len(missing)} published jobs without a price: {missing}")
    for item, p in prices.items():
        print(f"{item:28} ${p['usd']:.3f}  ({p['jobs']} jobs)")


if __name__ == "__main__":
    main()
