"""The three local tiers, one after another on the GPU server: full rounds with search working.

For each tier: stage 1 (the RBs) as its own step, then A, B, C x runs 1-5 on the 5 shared
topics, then the rescue of misplaced reports, then one rerun of the jobs that still have no
report (model failures), then a last rescue. Prints a "<preset> TIER-DONE" line after each
tier and "ALL-TIERS-DONE" at the end, for the watcher. Meant to run on the runner machine (see
HANDOFF-2026-10-28.md section 4), where BENCH_LLAMACPP points the provider at port 18080.

Search goes through the lab's cache on the GPU server: every job waits while its
/health is degraded, and searxng-mcp stores results under the namespace SEARCH_NS.

Usage:
  python3 local_tiers.py                                    # all three tiers, full rounds
  python3 local_tiers.py --tiers 4b --topics T3 --runs 1    # a pilot: one RB, then A1, B1, C1
"""
import argparse
import datetime
import os
import subprocess
import sys
import time
import paths

BENCH = paths.DATA
SCRIPTS = paths.TOOLS
TOPICS = "T3,T9,T20,S13,S23"
GEMMA_APPROVE = "approved. Please issue the RB file now, as the protocol directs; do not start the research yet."

SEARCH_NS = "bench-2026-10-local-brave"
TIERS = [   # (preset, tier, approval message or None for the standard "approved")
    ("llamacpp/qwen3.5-4b-think-262k", "low", None),
    ("llamacpp/qwen3.5-9b-think", "mid", None),
    ("llamacpp/gemma-4-12b-guarded", "high", GEMMA_APPROVE),
]


def run(*args):
    """Run one step. A runner batch that ends on an environment problem (exit status 3, already written to
    ALERTS.log) or crashes stops this script: the next step never starts on a broken environment."""
    rc = subprocess.run([sys.executable, "-I", *args], check=False).returncode
    if rc != 0:
        print(f"TIER-STOP {os.path.basename(args[0])} exited with status {rc}", flush=True)
        with open(os.path.join(BENCH, "ALERTS.log"), "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} TIER-STOP {os.path.basename(args[0])} exited with status {rc}\n")
        sys.exit(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", default="4b,9b,gemma", help="comma-separated: 4b, 9b, gemma")
    ap.add_argument("--topics", default=TOPICS)
    ap.add_argument("--runs", default="1-5")
    a = ap.parse_args()
    os.environ.setdefault("BENCH_SEARCH_HEALTH", "http://localhost:8888/health")
    os.environ.setdefault("SEARXNG_CACHE_NS", SEARCH_NS)
    wanted = a.tiers.split(",")
    for preset, tier, approve in TIERS:
        if not any(w in preset for w in wanted):
            continue
        root = os.path.join(BENCH, "runs-" + preset.split("/", 1)[1])
        os.makedirs(root, exist_ok=True)
        notes = os.path.join(root, "NOTES.md")
        if not os.path.exists(notes):
            with open(notes, "w") as f:
                f.write(f"# {preset}: {tier} tier (local)\n\nRun from the runner machine against the GPU server's router "
                        f"(PRESETS.md), {datetime.date.today()}. OpenCode 1.19.0 in bubblewrap, stdin closed, "
                        f"timeout 3 h per job. Search: the Brave Search API only, behind the lab's cache (namespace "
                        f"{SEARCH_NS}); jobs wait while /health is degraded, and a job that met degraded search "
                        f"is set aside (*.search-degraded<k>) and redone. A job repeating one tool call "
                        f"10 times is killed as a loop (a model failure). The document tools the prompt names (pandoc, "
                        f"xelatex, pdftotext, mmdc) are installed on the runner machine since 2026-10-28 21:00 UTC; the runner's "
                        f"preflight checks them in the sandbox before each batch, and each job's ledger entry lists "
                        f"any command not found.\n"
                        f"Stage 1 for {TOPICS} as its own step, then A, B, C x runs 1-5; one rerun of the jobs "
                        f"without a report.\n"
                        + ("DEVIATION: explicit stage-1 approval message (Gemma skipped the RB with the bare "
                           "'approved').\n" if approve else ""))
        base = [os.path.join(SCRIPTS, "run_headless.py"), "--client", "opencode", "--model", preset,
                "--root", root, "--topics", a.topics, "--timeout", "10800", "--mandatory-outputs"]
        if approve:
            base += ["--approve-message", approve]
        run(*base, "--arms", "")
        run(*base, "--runs", a.runs, "--arms", "ABC")
        run(os.path.join(SCRIPTS, "rescue_misplaced.py"), root)
        run(os.path.join(SCRIPTS, "rerun_reportless.py"), root, f"no-report-{datetime.date.today()}")
        run(*base, "--runs", a.runs, "--arms", "ABC")
        run(os.path.join(SCRIPTS, "rescue_misplaced.py"), root)
        print(f"{preset} TIER-DONE", flush=True)
    print("ALL-TIERS-DONE", flush=True)


if __name__ == "__main__":
    main()
