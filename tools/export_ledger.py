"""Write the published run ledger of an edition: the published rounds' research runs and v4.1 gradings,
with a fixed set of fields.

Kept: every research run of the edition's models (inputs/models.json), attempts and failures included; for the
local models only runs with search tracking (from 2026-10-28), since the earlier no-search rounds used the same
labels; and every grading session written under the published grading folders.

Usage:
  python3 export_ledger.py
Writes benchmarks/<edition>/ledger.jsonl in the repository.
"""
import json
import os

from grading_common import SUPERSEDED, published_run
import paths

FIELDS = ("label", "kind", "client", "models", "output", "start", "end", "duration_s", "api_calls", "steps",
          "tokens", "cost_usd", "cost_eur", "cost_note", "ok", "tool_calls", "tools", "searches", "search_errors",
          "max_context")
GRADING = ("scoring/v4.1-benchmark/", "scoring/v4.1-cross/", "scoring/v4.1-inter/", "scoring/v4.1-panel/",
           "scoring/v4.1-panel2/")


def published(e):
    if e.get("kind") == "research":
        return published_run(e)
    output = e.get("output") or ""
    return e.get("kind") == "grading" and output.startswith(GRADING) and not output.startswith(tuple(f"scoring/{s}/" for s in SUPERSEDED))


def main():
    out = os.path.join(paths.REPO, "benchmarks", paths.EDITION, "ledger.jsonl")
    n = 0
    with open(out, "w") as f:
        for line in open(os.path.join(paths.DATA, "run-ledger.jsonl")):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if published(e):
                f.write(json.dumps({k: e[k] for k in FIELDS if k in e}) + "\n")
                n += 1
    print(f"{n} entries -> {out}")


if __name__ == "__main__":
    main()
