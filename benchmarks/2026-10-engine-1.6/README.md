# Benchmark edition 2026-10: engine 1.6

Does the research engine make an AI model's research reports better? This edition compares three ways of
asking the same model for a report, across 15 model configurations, with one judge reading every pair of
reports side by side.

- **Engine:** research-project-starter 1.6 (the four files at the repository root; SHA-256 below).
- **Grader:** `grader/report-assessment-v4.1.md`, run by Claude Opus 5.5.
- **Research runs:** 22–30 October 2026. **Grading:** 24–31 October 2026.

## Release statements

**Recommendation.** For engine 1.6, write the research brief (RB) first, then research from it (arm B), at the
highest reasoning effort the model allows. The full engine (arm C) is not recommended in this release: its effect
depends on the model.

1. Writing the RB first (B) beats the plain question (A) for 11 of the 12 models that ran both, often decisively
   (+0.77 to +1.00). The gain is smaller for Qwen3.5 4B (+0.48) and Mistral Medium 3.5 (+0.28), and not
   measurable for Gemma 4 12B (+0.20 [−0.16, +0.60]).
2. The full engine (C) beats the plain question (A) for 10 of 12 models; the difference is not measurable for
   Qwen3.5 9B and Gemma 4 12B.
3. C against B depends on the model:
   - better for GPT-6 Luna (+0.49), Claude Sonnet 5.5 (+0.88) and Mistral Medium 3.5 (+0.64);
   - no measurable difference for Claude Haiku 5.5, Claude Opus 5.5, Mistral Large 4, GLM-5.3 Flash, Qwen3.5 4B
     and 9B, Gemma 4 12B;
   - worse for GPT-6.1 Sol at low effort (−0.80) and at high effort (−0.92), and for GPT-6 Astra (−0.80).
4. Raising reasoning effort helps a lot within a model: Haiku xhigh over medium +0.84, Luna xhigh over medium
   +0.92, Sol high over low +0.84. It does not make a cheaper model reach a stronger one: Luna at xhigh loses to
   Sol at low effort (−0.84).
5. For Luna, B at xhigh is better than C at medium (+0.80), and cheaper ($0.094 against $0.11 per report) and
   faster (5.9 against 6.4 min).
6. On one scale across all 15 executions (arm B), the strongest reports come from Claude Opus 5.5 and GPT-6.1 Sol
   at high effort; Sol at high effort costs about a third as much per report ($1.44 against $4.18). Opus is also
   the judge's model, which may favour it.
7. The local models (Qwen3.5 4B and 9B, Gemma 4 12B on one consumer GPU) rank last in every arm, at a few cents
   per report. Gemma 4 12B could not reliably finish the tasks (11 of 80 jobs failed).

Scores from +1 (the first always wins) to −1 (it always loses), mean over topics, with a 95% topic-bootstrap
interval. Haiku, Luna and GLM Flash within-model results rest on 55 topics; everything else on the 5 shared
topics (Gemma's C results on 4).

## The question and the three arms

Each topic is a casual question, as a person would type it (`inputs/topics.md`). For each model and topic:

- **Stage 1, once per topic:** the model, loaded with the engine, turns the question into a brief; the brief is
  approved as proposed, and the model writes the Research Boundaries file (RB). Arms B and C share that RB.
- **A:** the casual question, plus "research this and write me a report as a Markdown file".
- **B:** the RB only, plus "carry out the research this file describes"; no engine files.
- **C:** the engine (instructions, protocol, template) plus the RB, then "execute".

Five runs per arm and topic. Every job runs headless in a fresh folder, with web search, file writing and code
execution, and must deliver its mandatory result (A and B: the report; C: the report and its companion JSON);
a job without it has failed (`inputs/failed-jobs.json`).

## Models: 15 executions

| Model | Effort | Client | Topics | Arms |
|---|---|---|---|---|
| Claude Opus 5.5 | medium | Claude Code | 5 | A B C |
| Claude Sonnet 5.5 | medium | Claude Code | 5 | A B C |
| Claude Haiku 5.5 | medium | Claude Code | 55 | A B C |
| Claude Haiku 5.5 | xhigh | Claude Code | 5 | B |
| GPT-6.1 Sol | low | Codex | 5 | A B C |
| GPT-6.1 Sol | high | Codex | 5 | B C (Sol's RBs) |
| GPT-6 Astra | medium | Codex | 5 | A B C |
| GPT-6 Luna | medium | Codex | 55 | A B C |
| GPT-6 Luna | xhigh | Codex | 5 | B |
| Mistral Large 4 | thinking high | Mistral Vibe | 5 | A B C |
| Mistral Medium 3.5 | Vibe default | Mistral Vibe | 5 | A B C |
| GLM-5.3 Flash | thinking high | Mistral Vibe | 55 | A B C |
| Qwen3.5 9B (Q4_K_M, local) | thinking on | OpenCode + llama.cpp | 5 | A B C |
| Qwen3.5 4B (Q4_K_M, local) | thinking on | OpenCode + llama.cpp | 5 | A B C |
| Gemma 4 12B (QAT Q4_0, local) | default | OpenCode + llama.cpp | 5 | A B C |

Shared topics: T3 (screen time), T9 (10,000 steps), T20 (sitting and smoking), S13 (pair programming), S23
(direct air capture). Effort without a flag is the client's default: Claude Code's effort setting (medium), the
Codex default per model (Sol: low; Luna, Astra: medium). Details in `inputs/models.json`.

## How reports were judged

One judge, Claude Opus 5.5, with grader v4.1: it reads blinded reports for the same question side by side and
gives a reasoned verdict for each pair (first better, second better, mixed, similar, inconclusive), after
checking a bounded sample of sources. Report order is randomised outside the grader.

- **Within a model** (`results/within-model/`): A, B and C of the same topic and run in one session.
- **Effort and cross-model comparisons** (`results/comparisons/`): two to four reports per session.
- **One scale for everything** (`results/ranking.json`, `results/ranking.md`): panel sessions of four reports from
  different models (stage 1: 150 sessions, six models; stage 2: 275 sessions, all 15), fitted together with every
  other v4.1 verdict on the shared topics into Bradley-Terry scores. 4,075 verdicts in total.

The grader was validated before this edition (consistency across repeated gradings, then detection of
deliberately degraded reports); its rules were fixed before the panel ran. 1,666 grading sessions cost $1,350
at list price.

## Prices

`results/prices.json`, in USD per report; B and C include the RB. Claude: the cost Claude Code reports. GPT-6:
the job's tokens at OpenAI's standard prices (`inputs/pricing.json`, checked against OpenAI's pricing page on
2026-10-31; requests above 272K input tokens cost more and were not checked). Mistral Vibe models: the Mistral
console's usage, one price per model, EUR converted at the ECB October 2026 mean (1.1202). Local models: the
GPU's measured energy at €0.20/kWh plus the Brave Search API calls at $5 per 1,000 (`inputs/costs.json`).
Retries and failed attempts are paid by the published reports.

## Deviations and incidents

- **Mistral Large 4's price was cut by half during the round** (29–30 October). Every Large 4 job is priced at the
  new rate; the actual bill was €62.06.
- **Local search:** free search engines blocked the lab's metasearch on 28 October; the local rounds then used the
  Brave Search API only, behind a cache. Earlier local rounds without working search are not published.
- **Diagrams:** the cloud rounds ran without a working Mermaid renderer (the sandbox blocked its browser); the
  grader reads only Markdown, so reports were judged without diagrams. Later rounds used the system browser.
- **Local runs** got one extra sentence naming the mandatory files; Gemma got an explicit stage-1 approval
  message, and its failure cap was raised from 5 to 10 for its last batches.
- **Reports delivered outside the delivery folder** were copied back by a script after each local round.
  On 30 October that script also copied 4 files from older job folders; they were caught before grading and
  removed.
- **Seven GLM Flash jobs** left only a checkpoint or notes file, which the grader at first took for a report.
  Found on 31 October, before release: they count as failed and their verdicts are left out.
- **Sol High** reused Sol's RBs (low effort); its B and C prices and times include them.
- **Two PDFs are not in the release archive:** the models printed their sandbox path in them, and PDF text
  cannot be rewritten (`REDACTED.md` in the archive names them). Their Markdown reports, the graded files, are in.

## What is not in this edition

- **Rounds that failed on the harness, not the model:** local rounds without search (27 October) or with degraded
  search, a Gemma round on an older server, jobs that silently fell back to another model, pilots and tests
  (Qwen3.5 2B, Qwen3 14B, Ministral 3 8B, configurations without thinking).
- **GLM-5.3 Flash at maximum effort:** stopped as unstable (garbled output, five failed B jobs); not graded.
- **Older grader versions** and their validation runs.

## Limits

One judge, from one of the tested model families; 5 shared topics for the cross-model results; reports judged
on their Markdown only. The ranking measures what this judge prefers for a research reader, with the
uncertainty of five topics; it is not an absolute quality score.

## Files

| Path | What |
|---|---|
| `inputs/` | topics, the topic draw, models, prices and cost inputs, failed jobs, the job environment |
| `results/ranking.md`, `ranking.json` | the three arm tables and the full ranking |
| `results/prices.json` | price per report, with sources |
| `results/within-model/<model>/` | each model's A/B/C analysis (`analysis.json`) and per-topic means (`topics.csv`) |
| `results/comparisons/<name>/` | effort and cross-model comparisons |
| `ledger.jsonl` | every published research run and grading session: model, time, tokens, cost |
| `MANIFEST.sha256` | checksums of every file of the edition and of the release archive |

Raw data (every run's delivery, every grading session, the published ledger and the price tool's inputs) is
in the release archive `benchmark-2026-10-engine-1.6.zip`, attached to the GitHub release of this edition.
Personal paths and machine names in it were replaced by placeholders (`<home>`, `<jobs>`, `<tmp>`,
`gpu-server`, `runner`).

## Reproduce

The tools are in `tools/`. Data lives outside the repository: unzip the release archive into
`$RPS_DATA/benchmarks/2026-10-engine-1.6/` and set `RPS_DATA`. Then:

```
python3 tools/panel_rank.py        # ranking from every v4.1 verdict
python3 tools/report_prices.py     # prices
python3 tools/export_results.py    # results/ in the repository
```

Engine 1.6 files, SHA-256:

```
56113e6ca27805496137fa9004372dddf8f4e03476c3f93da4b1dd9d37436bb2  research-project-instructions.txt
ef17c09e5a1b90dea1ba00d8d9ee5a0292698faec0c34554d020a1b0ab5a5490  research-protocol.md
d89d91eb61b1860641d047f30b3cbc7eb5d473a3640a811872c3d1a4ea7b9953  research-boundaries-template.md
```
