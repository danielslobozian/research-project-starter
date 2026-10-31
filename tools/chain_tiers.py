"""Chain the local tiers unattended (rule since 2026-10-28): the next step starts only once the previous one
has fully run and left all its files; any doubt stops the chain.

Steps: wait for the running 4B tier to end, check it; then for the 9B and for Gemma: a one-topic pilot (T3: the
RB, then A1, B1, C1), check that all four have their file, then the full round, check it. A full round passes when
local_tiers.py printed "<preset> TIER-DONE", all 5 RBs exist, all 75 A/B/C jobs were recorded, no job hit a missing
command the prompt promises, and the log shows no harness failure. A job without a report after its rerun is a model failure and does
not stop the chain. Each step logs to ~/bench/local-tiers-<tier>-<pilot|full>.log; this script prints CHAIN-OK / CHAIN-STOP
lines (for the watcher) to its own log.

Usage (on the runner machine, from the benchmark folder, with PATH and BENCH_LLAMACPP set as for local_tiers.py):
  python3 -I scripts/chain_tiers.py --wait-pid <pid of the running 4B local_tiers.py>
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time

import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
LOGS = os.path.expanduser("~/bench")
TOPICS = ["T3", "T9", "T20", "S13", "S23"]
NEXT = [("9b", "qwen3.5-9b-think"), ("gemma", "gemma-4-12b-guarded")]
sys.path.insert(0, SCRIPTS)
import mandatory  # noqa: E402
from run_headless import PROMISED_CMDS as PROMISED  # noqa: E402   (inputs/bench-environment.md)
HARNESS_FAILURES = ("preflight failed", "ending the batch", "Traceback", "does not offer the preset")


def say(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def stop(msg):
    say(f"CHAIN-STOP {msg}")
    with open(os.path.join(BENCH, "ALERTS.log"), "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} CHAIN-STOP {msg[:400]}\n")
    sys.exit(1)


def problems(preset, log, topics, runs, need_reports=False):
    """What is missing or wrong in a finished step, as a list of strings (empty = passed)."""
    root = os.path.join(BENCH, "runs-" + preset)
    prefix = "research-" + preset
    text = open(log).read() if os.path.exists(log) else ""
    found = [f"log: {s!r}" for s in HARNESS_FAILURES if s in text]
    if f"{preset} TIER-DONE" not in text:
        found.append("no TIER-DONE line")
    for t in topics:
        if not glob.glob(os.path.join(root, t, "stage1", "*.rb.md")):
            found.append(f"{t}: no RB")
        for arm in "ABC":
            for n in runs:
                if not os.path.exists(os.path.join(root, "_meta", f"{prefix}_{t}_{arm}{n}.json")):
                    found.append(f"{t} {arm}{n}: not recorded")
                elif need_reports and mandatory.missing(arm, os.path.join(root, t, f"{arm}{n}"),
                                                        json.load(open(os.path.join(root, "_meta", f"{prefix}_{t}_{arm}{n}.json")))):
                    found.append(f"{t} {arm}{n}: failed ({'; '.join(mandatory.missing(arm, os.path.join(root, t, f'{arm}{n}')))})")
    ledger = os.path.join(BENCH, "run-ledger.jsonl")
    latest = {}   # the last entry per job: a redone job replaces its earlier attempt
    for line in open(ledger) if os.path.exists(ledger) else []:
        e = json.loads(line)
        if e["label"].startswith(prefix + "/") and "." not in e["label"].rsplit("/", 1)[1]:   # skip set-aside attempts
            latest[e["label"]] = e
    for e in latest.values():
        missing = PROMISED & set(e.get("missing_commands") or [])
        if missing:
            found.append(f"{e['label']}: missing promised commands {sorted(missing)}")
    return found


def step(tier, preset, log, topics, runs):
    """Run local_tiers.py for one tier (all topics and runs 1-5, or the T3 run-1 pilot) and check it."""
    pilot = runs == [1]
    args = ["--tiers", tier] + (["--topics", "T3", "--runs", "1"] if pilot else [])
    say(f"{tier}: {'pilot' if pilot else 'full round'} starting, log {log}")
    with open(log, "a") as f:
        rc = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "local_tiers.py"), *args],
                            stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, check=False).returncode
    if rc != 0:
        stop(f"{tier} {'pilot' if pilot else 'full round'}: local_tiers.py exited with status {rc} (see {log})")
    found = problems(preset, log, topics, runs, need_reports=pilot)
    if found:
        stop(f"{tier} {'pilot' if pilot else 'full round'}: " + "; ".join(found[:12]))
    say(f"CHAIN-OK {tier} {'pilot' if pilot else 'full round'} passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait-pid", type=int, default=0, help="the running 4B local_tiers.py (0: already finished)")
    ap.add_argument("--log-4b", default=os.path.join(LOGS, "local-tiers-4b-doctools.log"), help="the 4B tier's last log")
    a = ap.parse_args()
    say(f"waiting for the 4B tier (pid {a.wait_pid}) to end")
    while os.path.exists(f"/proc/{a.wait_pid}"):
        time.sleep(30)
    found = problems("qwen3.5-4b-think-262k", a.log_4b, TOPICS, [1, 2, 3, 4, 5])
    if found:
        stop("4b full round: " + "; ".join(found[:12]))
    say("CHAIN-OK 4b full round passed")
    for tier, preset in NEXT:
        step(tier, preset, os.path.join(LOGS, f"local-tiers-{tier}-pilot.log"), ["T3"], [1])
        step(tier, preset, os.path.join(LOGS, f"local-tiers-{tier}-full.log"), TOPICS, [1, 2, 3, 4, 5])
    say("CHAIN-DONE all tiers passed")


if __name__ == "__main__":
    main()
