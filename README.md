# Research Project Starter

> This file was written with Claude Opus 5.5.

A structured, evidence-centred research workflow for online LLM projects: ChatGPT, Claude, Mistral Vibe, or any
hosted assistant that lets you create a project, set project instructions, upload files, search the web and create
files.

It is not software. It is two sets of instructions that make the assistant work like a careful researcher: find out
who the report is for, agree the question before researching, keep to the agreed scope, check that sources actually
support the claims, and say honestly what was not found or not verified.

Website: <https://danielslobozian.github.io/research-project-starter/>

## How it works

Engine 1.7b.10 is two projects joined by one file.

1. **Generation project: agree the research.** Describe what you want to know in your own words. The assistant
   first asks up to four short, open questions about who will read the report and what it is for (“skip” keeps
   its stated defaults). It then proposes a brief: a neutral main question, supporting questions, scope,
   exclusions, and the deliverable. When you reply “approved”, it issues a **Research Boundaries** file
   (`<topic>.rb.md`) and stops. It does not research.
2. **Execution project: carry it out.** Open a new chat in the second project, attach the RB file, and send it with
   no text. The assistant researches within the RB's scope and delivers:
   - `<topic>.html` (or `<topic>.pdf` if you asked for one): the report to read;
   - `<topic>.md`: the same content as source for tools;
   - `<topic>.rb.md`: the unmodified RB the research followed;
   - `<topic>-research-package.zip`: everything together, when the report has figures.

## Install

Download the [v1.7b.10 release](https://github.com/danielslobozian/research-project-starter/releases/tag/v1.7b.10),
or take the files from the two folders of this repository. Create **two separate projects**.

| Project | Project instructions (paste the whole file) | Project files (upload, keeping the names) |
|---|---|---|
| Generation | [`research-boundary-generation.instructions.md`](research-boundary-generation/research-boundary-generation.instructions.md) | [`research-boundary-generation.protocol.md`](research-boundary-generation/research-boundary-generation.protocol.md), [`research-boundary-generation.template.md`](research-boundary-generation/research-boundary-generation.template.md) |
| Execution | [`research-boundary-execution.instructions.md`](research-boundary-execution/research-boundary-execution.instructions.md) | [`research-boundary-execution.protocol.md`](research-boundary-execution/research-boundary-execution.protocol.md), [`research-boundary-execution.template.md`](research-boundary-execution/research-boundary-execution.template.md) |

In the execution project, enable web search, file reading and file creation. Code execution helps with PDF checks;
an HTML report needs no converter. Never put both sets of instructions in one project.

**Claude (new Projects):** gear icon → **Project settings → Memory → Project instructions** for the instructions;
**Overview → Library → Add** for the two files.

**Claude (classic Projects):** **Set project instructions** for the instructions; the **+** button in the project
knowledge panel for the two files.

**ChatGPT:** create a project, open its settings to add the instructions, and add the two files to the project's
files.

**Other hosts:** any assistant with project instructions and uploaded files should work. Each project checks what
the app can do and says when it falls back.

### Settings that matter

From the [recorded cases](https://danielslobozian.github.io/research-project-starter/demos.html):

- Use a strong setting. On ChatGPT Medium and Instant, and on Claude Haiku at Low, a simple-looking question was
  answered directly, without the engine.
- Claude Fable 5.1 at Max treated the project instructions as a prompt injection and answered directly.
- Mistral Vibe's “Thinking” setting runs GLM-5 (`glm-5-latest-short`). Vibe turns questions into multiple-choice
  popups: type your own answer in the free field. It cannot render PDFs, so ask for HTML.

## Read more

- [Website](https://danielslobozian.github.io/research-project-starter/): the engine, the recorded cases, the
  benchmark. Earlier versions are in its version menu.
- [Guide](research-project-guide.md): why the engine works as it does, with sources.
- [Benchmarks](benchmarks/): what the engine changes, measured. The October 2026 edition measured engine 1.6;
  1.7b.10 has not been benchmarked yet.
- Engine 1.6 (one project, with the benchmark's recommended RB-only route): the
  [v1.6 release](https://github.com/danielslobozian/research-project-starter/releases/tag/v1.6).

## Limitations

The instructions state a contract; they cannot force a model to follow it. In the recorded cases, five of fifteen
runs answered directly instead. The checks are done by the same assistant that did the research, and are reported
as performed or not performed; they are not independent verification.

## Licence

[Apache License 2.0](LICENSE).
