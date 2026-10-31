"""Where the benchmark tools find things.

The repository holds what is published: the engine (at its root), the grader, each edition's inputs and these
tools. An edition's data (research runs, grading sessions, run ledger, logs) is too large for git and lives
outside it, under RPS_DATA:

    $RPS_DATA/benchmarks/<edition>/runs-<model>/...   research runs
    $RPS_DATA/benchmarks/<edition>/scoring/...        grading sessions and analyses
    $RPS_DATA/benchmarks/<edition>/run-ledger.jsonl   every run: model, time, tokens, cost

RPS_EDITION picks the edition (default: the current one).
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
GRADER = os.path.join(REPO, "grader", "report-assessment-v4.1.md")
EDITION = os.environ.get("RPS_EDITION") or "2026-10-engine-1.6"
INPUTS = os.path.join(REPO, "benchmarks", EDITION, "inputs")

if not os.environ.get("RPS_DATA"):
    raise SystemExit("RPS_DATA is not set: point it at the project's data folder, "
                     "e.g. export RPS_DATA=~/my-work/data/research-project-starter")
DATA_ROOT = os.path.expanduser(os.environ["RPS_DATA"])
DATA = os.path.join(DATA_ROOT, "benchmarks", EDITION)
