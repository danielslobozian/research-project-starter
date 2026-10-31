"""Panel grading, stage 2: every model that executed on one scale, arm by arm.

Stage 1 (panel_round.py) put the six panel models in front of the judge. Stage 2 adds
Opus, Astra, Mistral Large 4, Sol High, the local tiers and the higher-effort rounds.
For each arm type (B first, then C, then A), run k and topic, that arm's items are
split into sessions of 4 reports; when the items do not fill the last session, items
drawn at random fill it (never twice in one session). The split is chosen per slot as in
panel_round.design(): of 2000 seeded random splits, the one that leaves the pair counts
most even so far. A report that does not exist or whose job failed (inputs/failed-jobs.json) leaves its session one
report short.

Each session is one compare_v4.py call with its own folder
(scoring/v4.1-panel2/<arm>/run<k>-<topic>-g<i>), so calls can run side by side;
--parallel sets how many. Finished sessions are skipped, so the script can be rerun
after a stop; benchmark/STOP stops new sessions; a weekly-limit reading at or above
BENCH_STOP_AT (default 99%) stops them too. Fits the ranking (panel_rank.py) at the end.

Usage:
  python3 panel_stage2.py --dry-run               # show the design and missing reports
  python3 panel_stage2.py --pilot                 # one B session
  python3 panel_stage2.py --parallel 10
"""
import argparse
import itertools
import json
import os
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from grading_common import FAILED, report_file
import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
ROOT = os.path.join(BENCH, "scoring", "v4.1-panel2")
PROMPT = paths.GRADER
TOPICS = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
MODELS = {"H": "haiku", "S": "sonnet", "L": "luna", "G": "sol", "M": "vibe", "F": "glm-flash",
          "O": "opus", "X": "astra", "R": "large4", "J": "sol-high", "K": "haiku-xhigh", "U": "luna-xhigh",
          "N": "qwen3.5-9b-think", "Q": "qwen3.5-4b-think-262k", "E": "gemma-4-12b-guarded"}
ARMS = {arm: [l for l in MODELS if os.path.isdir(os.path.join(BENCH, f"runs-{MODELS[l]}", TOPICS[0], f"{arm}1"))]
        for arm in "BCA"}
SIZE = 4


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def design():
    """[(arm, run, topic, group index, letters)] with near-even pair meetings per arm."""
    rnd = random.Random("panel-stage2")
    out = []
    for arm, letters in ARMS.items():
        counts = {pair: 0 for pair in itertools.combinations(sorted(letters), 2)}
        n_groups = -(-len(letters) // SIZE)
        for run in range(1, 6):
            for topic in TOPICS:
                best = None
                for _ in range(2000):
                    p = rnd.sample(letters, len(letters))
                    p += rnd.sample(letters, n_groups * SIZE - len(letters))
                    groups = [p[i:i + SIZE] for i in range(0, len(p), SIZE)]
                    if any(len(set(g)) < len(g) for g in groups):
                        continue
                    trial = dict(counts)
                    for g in groups:
                        for pair in itertools.combinations(sorted(g), 2):
                            trial[pair] += 1
                    spread = (max(trial.values()) - min(trial.values()), sum(v * v for v in trial.values()))
                    if best is None or spread < best[0]:
                        best = (spread, groups, trial)
                counts = best[2]
                out += [(arm, run, topic, i, g) for i, g in enumerate(best[1], 1)]
    return out


def present(letter, arm, run, topic):
    if (MODELS[letter], topic, f"{arm}{run}") in FAILED:
        return False
    return report_file(os.path.join(BENCH, f"runs-{MODELS[letter]}", topic, f"{arm}{run}")) is not None


def weekly_used():
    try:
        r = subprocess.run(["claude-quota"], capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout)["seven_day"]["utilization"]
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        return None


def session(arm, run, topic, i, letters):
    root = os.path.join(ROOT, arm, f"run{run}-{topic}-g{i}")
    if os.path.exists(os.path.join(root, f"{topic}-o1.md")):
        return
    if os.path.exists(os.path.join(BENCH, "STOP")):
        return
    used = weekly_used()
    if used is not None and used >= float(os.environ.get("BENCH_STOP_AT") or 99):
        log(f"weekly usage {used}%: not starting {root}")
        return
    panel = ",".join(f"{l}={BENCH}/runs-{MODELS[l]}:{arm}" for l in letters)
    log(f"start {arm} run{run} {topic} g{i}: {', '.join(MODELS[l] for l in letters)}")
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "compare.log"), "a") as out:
        subprocess.run([sys.executable, os.path.join(SCRIPTS, "compare_v4.py"), "--topics", topic, "--run", str(run),
                        "--arms", "", "--orders", "1", "--prompt", PROMPT, "--panel", panel, "--root", root,
                        "--parallel", "1"], check=False, stdout=out, stderr=subprocess.STDOUT)
    log(f"{'done' if os.path.exists(os.path.join(root, f'{topic}-o1.md')) else 'NO ASSESSMENT'} {root}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parallel", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    jobs = []
    for arm, run, topic, i, g in design():
        letters = [l for l in g if present(l, arm, run, topic)]
        if len(letters) < len(g):
            log(f"missing report: {arm} run{run} {topic} "
                f"{', '.join(MODELS[l] for l in g if l not in letters)}")
        if len(letters) >= 2:
            jobs.append((arm, run, topic, i, letters))
    for arm, letters in ARMS.items():
        log(f"arm {arm}: {len(letters)} items, {sum(1 for j in jobs if j[0] == arm)} sessions")
    if a.dry_run:
        return
    if a.pilot:
        jobs = jobs[:1]
    with ThreadPoolExecutor(max_workers=a.parallel) as pool:
        list(pool.map(lambda j: session(*j), jobs))
    if not a.pilot:
        subprocess.run([sys.executable, os.path.join(SCRIPTS, "panel_rank.py")], check=False)
    log("stage 2 done")


if __name__ == "__main__":
    main()
