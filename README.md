# Research Project Starter

> This file was generated with GPT-6 Astra and Claude Opus 5.5.

A structured, evidence-centred research workflow for online LLM projects: Claude, ChatGPT, or any hosted assistant that lets you create a project, set project instructions, and upload files.

It is not software. It is a set of instructions and a protocol that make the assistant work like a careful researcher: agree the question before researching, keep to the agreed scope, check that sources actually support the claims, and say honestly what was not found or not verified.

## How it works

1. **Agree the boundaries.** Describe your research idea informally. The assistant proposes a neutral research brief: a precise primary question, secondary questions, scope, exclusions, and delivery limits. It asks at most three questions that would change the investigation, then waits for your approval. Once research starts, it finishes without further questions.
2. **Record them.** On approval, it writes a standalone **Research Boundaries** file (`<topic>.rb.md`), the contract for the investigation.
3. **Research and publish.** It researches within that contract and delivers:
   - `<topic>.rb.md`: the exact scope that was approved;
   - `<topic>.md`: a standalone, readable report with glossary and linked bibliography (about 20 substantive A4 pages by default, 25% tolerance), free of bookkeeping metadata apart from a one-line identification at the end;
   - `<topic>.analysis.json`: a structured companion with the questions, qualified answers, findings, source provenance, and the research bookkeeping;
   - `<topic>.pdf`: the report rendered by the assistant, included by default (you can decline it when approving the brief).

## Recommended use (engine 1.6)

The [October 2026 benchmark](benchmarks/2026-10-engine-1.6/) tested 15 model configurations. Writing the Research
Boundaries file first and then researching from it produced better reports than the plain question for nearly
every model, while running the full engine helped some models and hurt others. So, for this version:

1. In the project, describe your research idea and agree the brief. Reply **"approved"** (not "approved,
   execute"): the assistant writes the Research Boundaries file (`<topic>.rb.md`) and stops.
2. Start a new chat **outside the project**, with the model's highest reasoning effort, attach the `.rb.md` file
   and write: *"Carry out the research this file describes and write the report as a Markdown file."*

Replying "approved, execute" runs the full engine (step 3 above) instead; it helped GPT-6 Luna, Claude Sonnet 5.5 and Mistral
Medium 3.5 in the benchmark, and hurt GPT-6.1 Sol and GPT-6 Astra.

## Install

You need four files. Download them all from the [latest release](https://github.com/danielslobozian/research-project-starter/releases/latest), or individually:

| File | Where it goes |
|---|---|
| [research-project-instructions.txt](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-project-instructions.txt) | Paste its content into the project's **instructions**. |
| [research-protocol.md](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-protocol.md) | Upload as a project **file**. |
| [research-boundaries-template.md](https://raw.githubusercontent.com/danielslobozian/research-project-starter/main/research-boundaries-template.md) | Upload as a project **file**. |
| [research-project-guide.md](research-project-guide.md) | Optional: read it, no need to upload it. |

**Claude (new Projects):** create the project, then gear icon → **Project settings → Memory → Project instructions** for the instructions; **Overview → Library → Add** for the two files.

**Claude (classic Projects):** **Set project instructions** for the instructions; the **+** button in the project knowledge panel for the two files.

**ChatGPT:** create a project, open its settings to add the instructions, and add the two files to the project's files.

**Other hosts:** any assistant that supports project-level instructions and uploaded files should work. Tool availability (web search, file creation) differs between hosts and plans; the protocol tells the model to disclose missing capabilities rather than pretend.

Then start a new chat in the project and describe what you want to research.

## Read more

- [Guide](research-project-guide.md): installation, worked interaction, and the reasoning behind each rule.
- [Protocol](research-protocol.md): the full workflow contract the assistant follows.
- [Benchmarks](benchmarks/): what the engine changes, measured, with every result and the tools to reproduce it.

## Limitations

The package states a contract; it cannot force a model to follow it. The benchmark measured its effect with one judge (Claude Opus 5.5) on five shared topics; the [edition card](benchmarks/2026-10-engine-1.6/) lists its limits.

## Licence

[Apache License 2.0](LICENSE).
