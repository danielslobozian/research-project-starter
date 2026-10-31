"""Panel grading: all models on one scale per arm type.

Stage 1 (Opus left out: it is the judge's own model and the only frontier model;
stage 2 will compare the frontier models with the stage-1 winners). For each arm
type (A, B, C) and run k, the 6 models are ordered and split into two sets of 4
that share two models: p[0:4] and p[2:6]. The orders come from design(): a
seeded greedy choice that keeps the pair counts as even as possible. Each set
is one compare_v4.py call over the 5 topics, each session showing that arm's
reports from its 4 models side by side (6 pairwise verdicts). So every topic, run
and arm type puts all 6 models in front of the judge. Waits first for the given gated rounds to finish, then fits the
ranking (panel_rank.py).

Usage:
  python3 panel_round.py [--wait glm-flash]
"""
import argparse
import itertools
import json
import os
import random
import subprocess
import sys
import time
import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
PROMPT = paths.GRADER
TOPICS = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
MODELS = {"H": "haiku", "S": "sonnet", "L": "luna", "G": "sol",                # G: GPT Sol
          "M": "vibe", "F": "glm-flash"}                                     # M: Mistral Medium 3.5 (Vibe)

GROUPS = lambda p: (p[0:4], p[2:6])   # two sessions of 4 covering all 6 models


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def design():
    """{(arm, run): model order} with near-even pair meetings: for each slot, of 500
    seeded random orders, the one that leaves the pair counts most even so far."""
    rnd = random.Random("panel-design")
    counts = {pair: 0 for pair in itertools.combinations(sorted(MODELS), 2)}
    out = {}
    for arm in "ABC":
        for run in range(1, 6):
            best = None
            for _ in range(500):
                p = rnd.sample(list(MODELS), len(MODELS))
                trial = dict(counts)
                for group in GROUPS(p):
                    for pair in itertools.combinations(sorted(group), 2):
                        trial[pair] += 1
                spread = (max(trial.values()) - min(trial.values()), sum(v * v for v in trial.values()))
                if best is None or spread < best[0]:
                    best = (spread, p, trial)
            out[(arm, run)], counts = best[1], best[2]
    return out


def gated_running(names):
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            args = open(f"/proc/{pid}/cmdline").read().split("\0")
        except OSError:
            continue
        if any(a.endswith("gated_round.py") for a in args) and "--name" in args \
                and args[args.index("--name") + 1] in names:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", default="glm-flash")
    names = ap.parse_args().wait.split(",")
    while gated_running(names):
        time.sleep(120)
    log("gated rounds finished; panel grading")
    orders = design()
    for arm in "ABC":
        for run in range(1, 6):
            p = orders[(arm, run)]
            for half, group in zip(("s1", "s2"), GROUPS(p)):
                panel = ",".join(f"{l}={BENCH}/runs-{MODELS[l]}:{arm}" for l in group)
                log(f"arm {arm} run{run} {half}: {', '.join(MODELS[l] for l in group)}")
                subprocess.run([sys.executable, os.path.join(SCRIPTS, "compare_v4.py"), "--topics", ",".join(TOPICS),
                                "--run", str(run), "--arms", "", "--orders", "1", "--prompt", PROMPT, "--panel", panel,
                                "--root", os.path.join(BENCH, "scoring", "v4.1-panel", arm, f"run{run}-{half}"),
                                "--parallel", "5", "--pace-usd-per-hour", "28"], check=False)
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "panel_rank.py")], check=False)
    log("panel round done")


if __name__ == "__main__":
    main()
