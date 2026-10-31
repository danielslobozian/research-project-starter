"""Luna on the remaining 50 topics, same design as Haiku (3 arms x 5 runs).

1. RB step only, for all 50 topics (one retry for any topic without an RB).
2. Only if all 50 RBs exist: arms A, B, C, runs 1-5.
3. Rescue reports delivered outside the delivery folder (rescue_misplaced.py).
4. Grade and analyse all 55 Luna topics (cross_model_round.py --topics all).

Usage:
  python3 luna_full_round.py
"""
import glob
import json
import os
import subprocess
import sys
import time
import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
ROOT = os.path.join(BENCH, "runs-luna")
DONE = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
TOPICS = [t for t in [f"T{i}" for i in range(1, 28)] + [f"S{i}" for i in range(1, 29)] if t not in DONE]


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def research(arms):
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "run_headless.py"), "--client", "codex",
                    "--root", ROOT, "--topics", ",".join(TOPICS), "--runs", "1-5", "--arms", arms,
                    "--parallel", "6"], check=False)


def without_rb():
    return [t for t in TOPICS if not glob.glob(os.path.join(ROOT, t, "stage1", "*.rb.md"))]


def main():
    log(f"{len(TOPICS)} topics: {','.join(TOPICS)}")
    for attempt in (1, 2):
        research("")
        missing = without_rb()
        log(f"RB attempt {attempt}: {len(TOPICS) - len(missing)}/{len(TOPICS)} RBs; missing {missing}")
        if not missing:
            break
    if missing:
        log("not all RBs exist; research not launched")
        return
    research("ABC")
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "rescue_misplaced.py"), ROOT], check=False)
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "cross_model_round.py"), "--models", "luna",
                    "--topics", "all"], check=False)
    log("luna full round done")


if __name__ == "__main__":
    main()
