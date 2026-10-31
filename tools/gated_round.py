"""One model's benchmark round with an RB gate.

1. RB step only, for all topics (one retry for any topic without an RB).
2. Only if every topic has an RB: arms A, B, C for the runs.
3. Grade and analyse (cross_model_round.py, which first rescues misplaced reports).

Usage:
  python3 gated_round.py --client codex --model gpt-6.1-sol --name sol --topics T3,T9,T20,S13,S23
  python3 gated_round.py --model claude-opus-5-5 --name opus --topics T3,T9,T20,S13,S23 --pace-usd-per-hour 28
"""
import argparse
import glob
import os
import subprocess
import sys
import time
import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS


def log(name, msg):
    print(f"{time.strftime('%H:%M:%S')} {name}: {msg}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="claude")
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True, help="folder runs-<name>, ledger research-<name>")
    ap.add_argument("--topics", required=True)
    ap.add_argument("--runs", default="1-5")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--pace-usd-per-hour", type=float)
    a = ap.parse_args()
    root = os.path.join(BENCH, f"runs-{a.name}")
    topics = a.topics.split(",")

    def research(arms):
        cmd = [sys.executable, os.path.join(SCRIPTS, "run_headless.py"), "--client", a.client, "--model", a.model,
               "--root", root, "--topics", a.topics, "--runs", a.runs, "--arms", arms, "--parallel", str(a.parallel)]
        if a.pace_usd_per_hour:
            cmd += ["--pace-usd-per-hour", str(a.pace_usd_per_hour)]
        subprocess.run(cmd, check=False)

    for attempt in (1, 2):
        research("")
        missing = [t for t in topics if not glob.glob(os.path.join(root, t, "stage1", "*.rb.md"))]
        log(a.name, f"RB attempt {attempt}: {len(topics) - len(missing)}/{len(topics)} RBs; missing {missing}")
        if not missing:
            break
    if missing:
        log(a.name, "not all RBs exist; research not launched")
        return
    research("ABC")
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "cross_model_round.py"), "--models", a.name,
                    "--topics", a.topics], check=False)
    log(a.name, "round done")


if __name__ == "__main__":
    main()
