# Benchmark job environment

What every machine that runs benchmark jobs provides, by function. The jobs' prompt promises the first three rows
("bash, python, pandoc, xelatex, pdftotext, mermaid-cli are installed"); the prompt itself is not changed, so the
cloud rounds stay comparable. `run_headless.py` `preflight()` runs each tool inside the job sandbox before every
batch and refuses to start if one fails. A job that cannot find one of these commands stops the batch; any other
missing command is recorded in the ledger (`missing_commands`) and does not stop it.

| Function | Commands | Checked by the preflight |
|---|---|---|
| Shell and code | `bash`, `python`, `python3` | `python -c`, `python3 -c` |
| Documents | `pandoc`, `xelatex`, `pdftotext` | Markdown with accents to PDF through xelatex, read back with pdftotext |
| Diagrams | `mmdc` (mermaid-cli) | a one-edge graph to SVG |
| Archives | `zip`, `unzip` | zip a file and list it |

Archives are not named in the prompt, but the protocol's research package is a ZIP
(`<topic-slug>-research-package.zip`), so a C job needs them.

Machines: the runner machine (local rounds, OpenCode in bubblewrap). The cloud rounds ran on the laptop, where `mmdc` could not
start its browser (2026-10-28): a known difference, recorded for the analysis.
