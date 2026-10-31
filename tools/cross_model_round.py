"""Grade and analyse the cross-model round once each model's research is finished.

For each model, waits until no run_headless.py process is writing its runs folder,
rescues misplaced reports (rescue_misplaced.py), then grades with v4.1 every topic and run whose A, B and C reports all exist
(compare_v4.py, one random order, $28/h pace), then runs benchmark_analysis.py on
that model's grading folder. Last, model_usage.py over all models plus Haiku on the
same topics. Rerunnable: finished grading sessions are skipped.

Usage:
  python3 cross_model_round.py [--models luna,sonnet,vibe] [--topics T1,...|all]
"""
import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grading_common import report_file  # noqa: E402
import paths  # noqa: E402

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
PROMPT = paths.GRADER
MODELS = ["luna", "sonnet", "vibe", "sol", "opus"]
TOPICS = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
ALL_TOPICS = [f"T{i}" for i in range(1, 28)] + [f"S{i}" for i in range(1, 29)]
RUNS = range(1, 6)


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def research_running(model):
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            args = open(f"/proc/{pid}/cmdline").read().split("\0")
        except OSError:
            continue
        if any(a.endswith("run_headless.py") for a in args) and "--root" in args:
            if os.path.basename(os.path.normpath(args[args.index("--root") + 1])) == f"runs-{model}":
                return True
    return False


def complete(model, run, topics):
    runs_root = os.path.join(BENCH, f"runs-{model}")
    return [t for t in topics
            if all(os.path.isdir(os.path.join(runs_root, t, f"{arm}{run}"))
                   and report_file(os.path.join(runs_root, t, f"{arm}{run}")) for arm in "ABC")]


def grade(model, topics):
    root = os.path.join(BENCH, "scoring", "v4.1-cross", model)
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "rescue_misplaced.py"),
                    os.path.join(BENCH, f"runs-{model}")], check=False)
    for run in RUNS:
        ready = complete(model, run, topics)
        log(f"{model} run{run}: {len(ready)} complete topics {ready}")
        if not ready:
            continue
        subprocess.run([sys.executable, os.path.join(SCRIPTS, "compare_v4.py"), "--topics", ",".join(ready),
                        "--run", str(run), "--orders", "1", "--prompt", PROMPT,
                        "--runs-root", os.path.join(BENCH, f"runs-{model}"),
                        "--root", os.path.join(root, f"run{run}"),
                        "--parallel", "6", "--pace-usd-per-hour", "28"], check=False)
    if os.path.isdir(root):
        subprocess.run([sys.executable, os.path.join(SCRIPTS, "benchmark_analysis.py"), root], check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--topics", default=",".join(TOPICS), help="'all' = T1-T27 and S1-S28")
    a = ap.parse_args()
    pending = a.models.split(",")
    topics = ALL_TOPICS if a.topics == "all" else a.topics.split(",")
    while pending:
        for model in list(pending):
            if not research_running(model):
                log(f"{model}: research finished; grading")
                grade(model, topics)
                pending.remove(model)
        if pending:
            time.sleep(120)
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "model_usage.py"), "--topics", ",".join(topics),
                    "haiku", *dict.fromkeys(MODELS + a.models.split(","))], check=False)
    log("cross-model round done")


if __name__ == "__main__":
    main()
