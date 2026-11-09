# Benchmarks

Each edition measures one engine version and stays frozen once published: its inputs, results, ledger and
checksums never change, and a correction becomes a new edition. Raw data (every run's delivery and every
grading session) is in a release archive, not in git.

| Edition | Engine | Grader | Models | Topics | Result |
|---|---|---|---|---|---|
| [2026-10-engine-1.6](2026-10-engine-1.6/) | 1.6 | v4.1, Claude Opus 5.5 | 15 executions, 12 models | 5 shared, 55 for three models | Write the research brief first, then research from it (arm B), at the model's highest effort; the full engine (C) helps some models and hurts others |

## Engine files of an edition

The repository root holds the current engine. The engine an edition measured is at its release tag: engine 1.6 at
[`v1.6`](https://github.com/danielslobozian/research-project-starter/tree/v1.6). The ranking, price and export
tools of an edition work from its data alone; new research runs with `tools/run_headless.py` read the engine files
from the repository root, so run them from that tag.

## Comparing editions

Scores are comparable only within an edition: the ranking is a fit over that edition's own verdicts, and its
scale is centred on that edition's items. Across editions, compare conclusions (which arm wins, for which
models), and only when the grader version and the topics are the same; each edition card says which ones it used.
