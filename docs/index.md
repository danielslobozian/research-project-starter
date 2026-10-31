---
title: Research Project Starter
---

A structured, evidence-centred research workflow for online AI projects: Claude, ChatGPT, or any hosted
assistant that lets you create a project, set project instructions and upload files.

It is not software. It is a set of instructions and a protocol that make the assistant work like a careful
researcher: agree the question before researching, keep to the agreed scope, check that sources actually support
the claims, and say honestly what was not found or not verified.

## Recommended use (engine 1.6)

The [October 2026 benchmark](benchmark-2026-10.html) tested 15 model configurations. Writing the Research
Boundaries file first and then researching from it produced better reports than the plain question for nearly
every model, while running the full engine helped some models and hurt others. So, for this version:

1. In the project, describe your research idea and agree the brief. Reply **"approved"** (not "approved,
   execute"): the assistant writes the Research Boundaries file (`<topic>.rb.md`) and stops.
2. Start a new chat **outside the project**, with the model's highest reasoning effort, attach the `.rb.md` file
   and write: *"Carry out the research this file describes and write the report as a Markdown file."*

Replying "approved, execute" runs the full engine instead; it helped GPT-6 Luna, Claude Sonnet 5.5 and Mistral
Medium 3.5 in the benchmark, and hurt GPT-6.1 Sol and GPT-6 Astra.

## Install

You need three files, from the [latest release](https://github.com/danielslobozian/research-project-starter/releases/latest)
or individually:

| File | Where it goes |
|---|---|
| [research-project-instructions.txt](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-project-instructions.txt) | Paste its content into the project's **instructions**. |
| [research-protocol.md](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-protocol.md) | Upload as a project **file**. |
| [research-boundaries-template.md](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-boundaries-template.md) | Upload as a project **file**. |

The [guide](https://github.com/danielslobozian/research-project-starter/blob/main/research-project-guide.md)
explains installation on each host, a worked interaction, and the reasoning behind each rule.

## What the benchmark found

- Writing the research brief first (B) beats the plain question (A) for 11 of 12 models.
- The full engine (C) against B depends on the model: better for three, no measurable difference for seven,
  worse for GPT-6.1 Sol and GPT-6 Astra.
- Raising reasoning effort helps a lot within a model, but a cheaper model at its highest effort does not reach
  a stronger one.

[All results, prices and limits](benchmark-2026-10.html) ·
[Edition card and raw data](https://github.com/danielslobozian/research-project-starter/tree/main/benchmarks/2026-10-engine-1.6)

## Licence

[Apache License 2.0](https://github.com/danielslobozian/research-project-starter/blob/main/LICENSE).
