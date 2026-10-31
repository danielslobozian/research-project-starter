---
title: Benchmark 2026-10, engine 1.6
---

[← Research Project Starter](./)

Does the research engine make an AI model's research reports better? This edition compares three ways of asking
the same model for a report, across 15 model configurations; one judge (Claude Opus 5.5, grader v4.1) reads the
reports side by side and says which serves a research reader better. Research runs 22–30 October 2026, grading
24–31 October 2026.

- **A:** the casual question, plus "research this and write me a report as a Markdown file".
- **B:** the Research Boundaries file (RB) the engine wrote from that question, plus "carry out the research this
  file describes"; no engine files.
- **C:** the full engine with the RB.

## Release statements

**Recommendation.** For engine 1.6, write the research brief (RB) first, then research from it (arm B), at the
highest reasoning effort the model allows. The full engine (arm C) is not recommended in this release: its effect
depends on the model.

1. Writing the RB first (B) beats the plain question (A) for 11 of the 12 models that ran both, often decisively
   (+0.77 to +1.00). The gain is smaller for Qwen3.5 4B (+0.48) and Mistral Medium 3.5 (+0.28), and not
   measurable for Gemma 4 12B (+0.20 [−0.16, +0.60]).
2. The full engine (C) beats the plain question (A) for 10 of 12 models; the difference is not measurable for
   Qwen3.5 9B and Gemma 4 12B.
3. C against B depends on the model: better for GPT-6 Luna (+0.49), Claude Sonnet 5.5 (+0.88) and Mistral Medium
   3.5 (+0.64); no measurable difference for Claude Haiku 5.5, Claude Opus 5.5, Mistral Large 4, GLM-5.3 Flash,
   Qwen3.5 4B and 9B, Gemma 4 12B; worse for GPT-6.1 Sol at low effort (−0.80) and at high effort (−0.92), and for
   GPT-6 Astra (−0.80).
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

Statements 1–5: +1 means the first always wins, −1 that it always loses; mean over topics, 95% topic-bootstrap
interval.

## Ranking

{% assign edition = site.data["2026_10_engine_1_6"] %}
All items share one scale across the three arms: Bradley-Terry scores (log strength, centred on the mean item)
fitted on {{ edition.verdicts }} verdicts over the five shared topics, with a 95% topic-bootstrap interval. Price
per report in USD, the RB included for B and C; median minutes per report.

### Arm A: the casual question

{% include ranking-table.md data="2026_10_engine_1_6" arm="A" %}

### Arm B: the RB, then research from it

{% include ranking-table.md data="2026_10_engine_1_6" arm="B" %}

### Arm C: the full engine

{% include ranking-table.md data="2026_10_engine_1_6" arm="C" %}

## Limits

One judge, from one of the tested model families; five shared topics for the cross-model results (55 for the
within-model results of Haiku, Luna and GLM Flash); reports judged on their Markdown only. The ranking measures
what this judge prefers for a research reader, with the uncertainty of five topics; it is not an absolute
quality score.

## Everything else

The [edition card](https://github.com/danielslobozian/research-project-starter/tree/main/benchmarks/2026-10-engine-1.6)
has the design, the 15 executions, how prices were computed, every deviation and what was left out. Results,
ledger and tools are in the repository; every run's delivery and every grading session are in the release
archive.
