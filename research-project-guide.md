---
title: "From Research Boundaries to Faithful Research Artifacts"
subtitle: "Research Project Starter v1.6 — installation and operating guide"
lang: en
guide_version: "1.6"
updated: "2026-10-20"
document_type: "Explanatory installation and operating guide"
generated_with: "GPT-6 Astra and Claude Opus 5.5"
---

# Summary

> This file was generated with GPT-6 Astra and Claude Opus 5.5.

Research Project Starter is a set of instructions for running evidence-based research inside an online LLM project: any hosted assistant workspace that lets you create a project, configure project instructions, and upload source files. It needs no local software.

The workflow has two stages. First, the assistant turns an informal research idea into a neutral, identified research brief, and records the agreed scope as a standalone **Research Boundaries (RB)** file. Second, it researches within that scope and publishes the result.

Every investigation that delivers a report, including one stopped early by a limit, publishes **three public artifacts**: the exact active Research Boundaries file, the complete readable Markdown report, and one `<topic-slug>.analysis.json` companion. Necessary assets accompany them, and by default a PDF of the report. The report itself stays clean to read: its front matter holds only title, subtitle, language, and date, while the research bookkeeping (identity, versions, page verification) lives in the companion. A checkpoint is conditional and private by default. Cross-investigation catalogues, retrieval across reports, and downstream adoption decisions are outside this workflow.

The default limit is twenty substantive A4 pages, with a 25% tolerance (up to 25 pages), unless the limit is stated as strict. Glossary, bibliography, title, contents, and summary stay outside that limit; substantive analysis and figures stay inside it. These are chosen publication rules, not a measured quantity until the reference document is rendered.

**Role of this guide:** explanatory only. The Project instructions activate the protocol; `research-protocol.md` is the workflow contract and the active RB is the topic contract. This guide cannot override either.

# 1. Install the four-file package

Create a project in your assistant of choice. Paste the complete contents of [research-project-instructions.txt](research-project-instructions.txt) into the project's instructions field. Upload [research-protocol.md](research-protocol.md) and [research-boundaries-template.md](https://github.com/danielslobozian/research-project-starter/blob/main/research-boundaries-template.md) as project files. Keep this guide as optional documentation; it is not another required instruction source. Host documentation describes project files and instructions, but does not certify adherence to this workflow. [[1]](#ref-1)

When upgrading, remove superseded **configuration** copies from the active project to avoid competing protocols. Do not delete research RBs or reports already produced: their identity and immutability are part of the workflow. A new topic chat after installation is the simplest way to avoid mixing a configuration discussion with research.

Some hosts let you create a project but give the model no way to create files in a given chat (for example, when file creation is switched off, or code execution is unavailable for that model). The workflow still runs: the brief says so up front, the RB, report, and companion arrive as labelled blocks in the chat for you to save, and delivery is recorded as partial. The protocol's *Capabilities and fallbacks* table lists what happens for each missing capability.

| Package file | Role |
|---|---|
| `research-project-instructions.txt` | A short core: activation, precedence, and the few rules that must hold before the protocol is read (approval stop, a pointer to the protocol's reply table, issued RBs never edited, no pausing during execution, honest provenance, source trust). The protocol's wording wins on any difference. |
| `research-protocol.md` | Terms, full method, transitions, RB rules, evidence/coverage rules, checkpoints, report contract, the companion specification with one illustrative JSON example, and the pre-delivery checklist. |
| `research-boundaries-template.md` | Structural aid with truthful approval placeholders and nine required sections. |
| `research-project-guide.md` | Installation, examples, rationale, and limitations; not governing. |

No renderer, converter, model account, external service, font, or evaluation harness is bundled. Uploaded instructions do not install dependencies. Available tools must be checked in the actual execution environment; missing access must be disclosed rather than simulated. Instruction-only control is inherently non-deterministic: the package states a contract, it does not guarantee that a given model follows it. [[2]](#ref-2)

**RBs created under an earlier protocol version remain usable.** An RB with clear scope needs no migration or reapproval. Preserve its original bytes and protocol label; the new companion and the report's identification line record execution version `1.6`. Missing identity or question mappings go in the report scope section and working record, not a rewritten RB.

# 2. The interaction stays simple

An opening request can remain informal:

```text
Research idea: assistants sometimes seem less reliable during long conversations.
I do not know whether context length, changing instructions, or something else
explains it. My examples illustrate the concern; they are not required test cases.
20 substantive A4 pages (up to 25 accepted), for an interested non-specialist, with useful diagrams.
```

Before the first brief, the model checks what the host can do (create files, search the web, run code, render a PDF) and shows any gap, with its fallback, in the brief. The first output is an identified proposed brief (`BR-001`), including the primary question `Q0`, any secondary questions, scope, exclusions, and delivery defaults. The model distinguishes an observation from a proposed explanation and an example from a mandatory constraint. A more scientific formulation means a more precise question, not a predetermined answer or obscure vocabulary. Clarifying ambiguous information needs before answering is a known weak point of language models, which is why this step is explicit. [[3]](#ref-3)

The default is no more than three consequential unanswered questions. Once the material uncertainty is resolved, the model asks for approval only. It must not ask for a technical diagnosis that the investigation is supposed to discover.

| Message or situation | What should happen |
|---|---|
| `BR-001 approved.` or `Looks good.` | Create and link the RB, then stop. |
| `BR-001 approved. Create the RB and execute.` or `Looks good, go ahead.` | Create, read back, and link the RB first; proceed without another approval round. |
| `I explicitly waive scope approval. State assumptions and proceed.` | State the assumptions, create and read back the RB with unapproved-assumptions status, then execute; no fabricated approval. |
| `Execute the attached approved RB.` | Read it and the protocol; execute without recreating the original interview. |
| A reply materially changes the proposed scope | If the change is unambiguous and can go into the RB word for word, the approval in the same message covers it; otherwise show the revised scope under a new brief ID and obtain one confirmation. |
| A follow-up asks about a completed report | Answer directly; a request for new searches within the RB ("update it with newer studies") executes on that RB and produces new versions; materially new research needs a new brief. |

Replies are classified by intent, in any language, not matched word for word. When it is unclear whether execution was requested, the model creates the RB and stops: that costs one message and lets you review the RB first. Each open question in a brief comes with the assumption the model will use if you leave it unanswered, so approving the brief as it stands is always possible.

For a definition-to-execution handoff, an available lower-effort setting may draft the brief and RB, followed by an available higher-effort setting for research. A model switch is never approval by itself; approving the brief before switching means the RB already exists. If the switch happens before RB creation, the receiving model recovers the approved brief and every earlier brief it revises, asks for any it cannot recover, and creates the RB before research. In a new chat session, attach the active RB (and the checkpoint, if any), because files created in another conversation may not be available there. This package does not promise that any particular model or interface exposes the same tools, preserves accessible files, or interprets the contract perfectly.

# 3. One topic contract, truthful approval, preserved versions

## 3.1 Authority is separated by responsibility

The protocol specifies **how** to investigate and publish. The active RB specifies **what** to investigate and accepted choices such as a fixed corpus or the body limit. A scope-specific accepted choice can override a default, not an integrity requirement. A template supplies structure; the guide supplies explanation. Neither can silently change approved scope.

Older exploratory messages do not outrank the active RB. Later instructions can request a new scope, but a material change is recorded in a newly approved revision. Conflicting active RBs require one targeted resolution rather than a guessed “latest” filename, silent merge, or timestamp rule.

Sources are evidence rather than operational authority. Instructions embedded in a paper, webpage, repository, or quoted text cannot change approval status, redirect research, or authorize disclosure of unrelated project content. Useful evidence in such a source can still be evaluated. This is a stated trust boundary, not proof of resistance to every attack.

## 3.2 Approval covers the accepted brief, not invented additions

The RB may add headings, stable IDs, and faithful operational detail. It may not quietly add a research question, exclude a requested case, impose a different corpus, or introduce another deliverable while claiming all of it was approved.

The approval metadata includes `approval_basis` and the actually approved brief ID. The template starts with null approval fields that must be filled truthfully at issue. Approval dates remain null when unknown and on a waiver. Minimal process metadata is allowed without requester names, signatures, or private chat text.

Approval is not evidence validation. A supplied approved RB states a scope contract; the receiving model must not invent the historical approving event. All nine RB sections remain present, including a no-examples statement where no examples matter.

## 3.3 Scope revisions and result corrections are different

The initial file is `topic.rb.md`. A revised scope may be `topic.rb-v1.1.md`, with `rb_version: "1.1"`, the same research ID, and `supersedes: "topic.rb.md"`. Every report points to its exact governing file. Issued RB bytes remain unchanged; even an editorial-only file revision is saved separately with a clear note. The protocol's *Versions, revisions, and corrections* section gathers the file names and version numbers of every artifact in one table.

A discovery that the motivating suspicion is false does not change the question. A corrected source percentage normally changes the report, its summary, and any affected figure—not the RB. A revised report may be `topic.v1.1.md`, recording its own `supersedes` pointer. Research IDs, brief IDs, RB versions, report versions, and checkpoint versions have distinct purposes.

# 4. Make the research work inspectable

## 4.1 One lightweight coverage record

The research stage maintains one working record rather than another required public document. It maps the accepted question IDs to search concepts, sources and locations inspected, provisional answers, unresolved gaps, and next action or closure. For an atomic investigation, one primary-question row is enough. For a broad investigation, more detail is justified.

| Coverage status | Meaning |
|---|---|
| `pending` | The question has not yet been adequately investigated. |
| `partial` | Some required parts have a qualified answer and others do not; both are named. |
| `answered` | Every required part has a qualified supported, mixed, or inconclusive answer. |
| `evidence-gap` | A relevant permitted search did not produce adequate accessible support; this does not prove nonexistence. |
| `blocked` | Access, tools, or another actual constraint prevented the necessary investigation. |

Queries that are merely planned stay labeled planned. The model should try relevant disciplinary vocabulary and alternative source locations when literal wording fails, without changing the accepted topic or leaving a fixed corpus. No minimum number of papers substitutes for coverage.

Important unresolved questions must appear in the public report's method, limitations, or conclusion. They cannot disappear into private notes. A small public coverage table is optional, not a new mandatory section. The reporting items borrow selectively from scoping-review guidance without claiming compliance with it. [[4]](#ref-4)

## 4.2 Appraise evidence that drives the conclusions

For central empirical results and recommendation-driving claims, inspect the relevant design/type, comparison baseline, sample or corpus, conditions and system version, uncertainty and confounding, independence, correction/version status, and applicability. Fields that genuinely do not apply should not become invented data or busywork.

A software manual can establish documented behavior without proving a measured performance benefit. An observational comparison may support an association without isolating its cause. A proposed remedy is not a validated remedy merely because a source describes it. Different metrics, study settings, or versions need not be directly contradictory. A citation being present is not the same as the cited source supporting the claim; the workflow checks both. [[5]](#ref-5)

This is a domain-adapted procedure, not a compulsory named evidence-grading framework or a claim of systematic-review completeness.

## 4.3 Say why research stopped

Normal closure means material questions have supported answers or explicit limitations, consequential contrary evidence has been considered, and reasonable further searching within the accepted scope is no longer adding materially useful independent evidence. The report states the actual search and stopping reason without claiming exhaustive saturation.

Constrained closure is different: a hard host limit, a budget the user stated, the loss of needed sources or tools, or the user's explicit instruction to stop ends execution before completion. The report remains useful but is labeled limited or incomplete, with pending and blocked questions visible. Stopping early cannot be relabeled “no evidence exists.”

Appraisal, search methods, coverage explanations, and limitations are substantive research content and count toward the body-page limit.

# 5. Recover execution without rewriting scope

## 5.1 When a checkpoint is useful

The RB preserves intended research. A checkpoint preserves work already performed: which sources were inspected, what remains unresolved, what files exist, and what action should come next.

During execution, the model saves a checkpoint each time a question's coverage status changes, before a handoff to another model or session, after about every ten research-tool calls when no status changes, and at a constrained closure or a pause you asked for. Checkpoints are private (kept out of the public package) but saved where you can download them, so that, where the host allows it, they survive a hard stop. None is saved before research starts: the RB is enough. The model never pauses on its own (the only pauses are ones you ask for, such as "show me the sources before writing"): once execution starts, it finishes without asking questions, because on an expensive plan every extra turn costs a scarce message. The questions it may need (such as which RB, a missing RB, or a version mismatch; the full list is in the protocol's *Finish once launched*) are asked before execution starts, or when an execution is resumed in a new session. Decisions it would otherwise ask about are made and recorded in the report's limitations; a needed scope change is proposed after delivery, not made mid-run. Where it can see how much of a host limit remains, it stops searching in time to write and deliver.

The file is `<topic-slug>.checkpoint.md`. Unlike the immutable RB, it is a mutable working snapshot with an incrementing checkpoint version. Save and read back the file before claiming persistence. A sudden interruption can occur before a save; the protocol cannot guarantee recovery from all host failures and does not schedule background work.

## 5.2 Compact checkpoint structure

This is an embedded template, not an additional package dependency or a real execution record. Fill only facts actually known; remove placeholders. Keep concise work/evidence notes, not hidden reasoning transcripts.

```markdown
---
protocol_version: "1.6"
research_id: "<actual-investigation-id>"
research_boundaries_file: "<exact-active-rb-filename>"
rb_version: "<actual-active-rb-version>"
checkpoint_version: 1
saved_at: null # Replace with the actual known save date/time; never invent it.
record_basis: "<current-run record, observable tool events, inherited log, or mixed>"
visibility: "private-working-record"
---

# Research execution checkpoint

## Question coverage
Question IDs, current statuses, qualified provisional answers,
evidence locators, gaps, and next search/check or stop reason.

## Sources and evidence checked
Source IDs, recoverable URLs/file identities, inspected sections/pages,
access scope, conditions, central appraisal notes, and source activity.
For each activity, record its basis and purpose-specific disposition/reason.

## Unresolved issues
Conflicting claims, pending correction checks, unavailable sources,
and any material limitations on resumption.

## Runtime controls
Each user budget, with its unit, usage, and remaining allowance (or unknown),
and any user-requested pause or stop point not reached yet.

## Existing artifacts
Actual filenames, versions, and completion/validation status.
Do not list an artifact as created when it is only planned.

## Next action
The next concrete research or verification step within the active RB.
```

If the needed file cannot be saved, the model says so and posts the checkpoint content in the chat instead, rather than claiming a recoverable artifact. On resumption, verify actual RB/artifact access and revisit central source support before presenting claims as verified. An inherited checkpoint is a pointer to evidence, not independent evidence.

## 5.3 Source activity is not a truth label

Record the material actually accessed and the purpose for which it was assessed:

| State | What it does and does not establish |
|---|---|
| `discovered-unopened` | Discovery/non-opening is recorded; full text was not inspected. |
| `opened-not-assessed` | Specified text was accessed, but appraisal is incomplete. |
| `assessed-used` | Inspected material contributed to an identified claim, question, or context. |
| `assessed-not-retained` | The material was declined for a specified purpose, with a reason; it may still serve a different purpose. |
| `inaccessible` | Needed material could not be accessed; an abstract/index may still have been seen. Its conclusion is not thereby false. |
| `unknown` | The record does not establish what happened. It does not mean never examined. |

Keep the basis of an activity explicit: observable tool events, a current-run researcher record, or an inherited assertion. A self-reported log is not independently verified merely because it is neatly structured. A source may be declined as independent corroboration because it mirrors a study while still being used for historical context.

## 5.4 Keep public and working artifacts separate

A normal public package contains:

```text
topic.rb.md              # Exact active scope file; may have a revision suffix
topic.md                 # Standalone report; may have a report-version suffix
topic.analysis.json      # Faithful companion and research bookkeeping; own revision suffix
topic.pdf                # Report rendered in the A4 reference layout, when the RB includes it
assets/                  # Only when required by the report
```

The conditional `topic.checkpoint.md` stays outside that public bundle. “Private” describes its intended distribution, not a guarantee of access control. The model saves it where you can download it and points you to it at a handoff, a pause, or a constrained closure; minimize sensitive data, copied source text, and temporary local paths. A request to publish working records requires a separate disclosure check. Public method and limitation reporting remains mandatory even when the detailed checkpoint stays private.

# 6. Publication requirements

The editable source is an actual UTF-8 Pandoc Markdown file. [[6]](#ref-6) The report has a meaningful title, summary, question/scope, concepts, review method, findings, implications/trade-offs, limitations, conclusion, glossary, and bibliography. It is independent of the original chat and contains no requester references.

By default, use portable numbered citations with Pandoc heading targets, for example `[[1]](#ref-1)` and `{#ref-1}`; another verifiable citation style can be requested, since only the honesty requirements (real sources, supported claims, locators) are fixed. Add precise locators for important claims and real source links. Source existence and claim support are separate checks. Findings, synthesis/inference, recommendations, and unknowns remain distinguishable.

Visuals are purpose-driven: explain mechanisms, timelines, relationships, or verified data when a figure communicates better than prose. Provide a caption, readable labels, evidence status, attribution, and a textual explanation/alternative. [[8]](#ref-8) Measured charts preserve values, metrics, units, and conditions. A conceptual drawing is not an experiment, and unrendered diagram source (for example Mermaid [[7]](#ref-7)) is not an inspected figure.

**A4 is the length reference:** 210 × 297 mm, 11 pt body, 25 mm margins, 1.15 line spacing. Default limit: twenty substantive pages, not a target, with a 25% tolerance (up to 25 pages is accepted); a limit stated as strict has no tolerance. Beyond that, the model shortens on its own: every accepted question keeps at least a short answer, and the limitations section lists what was cut. Count the entire research body, tables, figures, captions, methods, limitations, conclusion, and substantive appendices. Exclude only title material, contents, summary, glossary, and bibliography. Do not relocate essential analysis to excluded sections or shrink typography to evade the limit.

The PDF is a presentation choice recorded in RB section 8. The brief shows it as a default (yes, A4 reference layout, or no when the host cannot render PDFs) that the user can change when approving, rather than spending one of the three clarifying questions on it. The model renders it from the final Markdown with the host's own tools, so a user without a converter still gets a readable file; if the host cannot render, the model says so and delivers the other files. The layout is set explicitly in the renderer, because a conversion with the renderer's own defaults is not the A4 reference layout. Rendering in the A4 reference layout also verifies the body limit in the same step. A PDF in another layout, such as a screen-reading one, does not count for the body limit. The markers `<!-- RESEARCH_BODY_START -->` and `<!-- RESEARCH_BODY_END -->` identify the counted span but are not automatic page breaks. A verified count requires an actual fixed-layout A4 render, physical page-span accounting, and inspection. Otherwise report **“Substantive body page count: unverified.”**

The exact rendering engine, font, document class, and layout configuration used for verification should be recorded when a body limit is asserted; ordinary typography alone does not make pagination identical across all engines. The PDF is derived from the Markdown, never a substitute for it or a separate rewrite.

## 6.1 Methods and presentation have different responsibilities

The same neutral brief and nine-section RB capture research obligations (questions, corpus, evidence approach, exclusions, and uncertainty) separately from audience, language, explanation depth, and publication preferences. There is no menu of modes: the method adapts to the question. A named report format cannot establish that a systematic method was performed.

An explicit later request for novice wording, another language, a different body limit or reference layout, or adding or dropping the PDF can authorize a presentation-only variation. Record the actual basis/changes in the companion's `report.presentation_variation`, leave issued RB bytes unchanged, and retain the same evidence and qualified conclusions. This is not permission to drop accepted questions or substantive qualifications. A material method/scope change still needs an approved RB revision, not another routine approval ceremony.

## 6.2 How the companion is produced and read

The protocol's **Structured research-analysis companion (schema 1.1)** is the only field/type/status definition. A small table there states which coverage and answer statuses may be combined. The four-file package intentionally has no fifth schema file or runtime; the protocol includes one illustrative JSON example so that field names come from one place. Its one JSON object groups identity, scope/method, questions, findings, sources, optional relations, corrections, and actual check status. Empty relation/correction arrays suffice when nothing is needed. Its `report` entry also carries the report's bookkeeping, so the report needs none beyond its final identification line. It does not list every claim.

The format is chosen for explicit keys, types, IDs, and straightforward syntax checks, while keeping public justifications as editable prose. JSON punctuation is less forgiving than Markdown and semantic drift remains possible; syntax validity does not establish truth or downstream benefit. The general serialization rules are described by RFC 8259. [[9]](#ref-9) An available host parser can check syntax; no custom installed application is required, and an unexecuted check must stay labeled unexecuted.

Derive the report and companion from the same inspected evidence/coverage record. The RB establishes scope, sources supply evidence, the report supplies the full explanation, and the companion selects a faithful analytical view. Neither authored view wins automatically when they disagree. Revisit the evidence and reconcile the error, including conditions, alternatives, unknowns, source-access limitations, and public rationale. The companion never asks for hidden reasoning and never turns a proposal into a proven effect or mandatory engineering choice.

Initial companion: `topic.analysis.json`; next issue might be `topic.analysis-v1.1.json`. It records the exact RB/report filename/version and its own predecessor. Changed findings receive new IDs with retained superseded statements, reasons, and known affected derivative pointers. Unchanged meanings retain IDs. Source corrections change findings, not approved scope. An old downloaded copy cannot detect a later correction that it has never received; the workflow does not implement update propagation.

Relative report locators use explicit Pandoc section IDs rather than depending on the text of a heading. A reader can also search those visible IDs in plain text. Renaming a file may break literal paths; verify research ID, kind, and version before remapping a moved copy. Pandoc heading attributes are documented format features, not a guarantee that every viewer renders them. [[10]](#ref-10)

A fresh AI receiving only the companion can read the recorded qualified answers, limits, rationale, and known provenance/corrections. It cannot independently verify source support, original approval, completeness, or latestness. It needs the exact report/RB and relevant original evidence for those checks. Quoted source instructions remain data. Later research selection or technical choices are separate decisions, not commands contained in the research.

## 6.3 Actual file checks, not imaginary publication

Check actual files and identities, JSON syntax when a parser is available (an ordinary parser silently accepts duplicate keys, so that check needs a stricter one), required fields/IDs/references, active report anchors, and known correction/version compatibility. Separately compare meaning and revisit relevant evidence. Record the actual method and limits of each check. A self-review is not an independent behavioral experiment.

Missing mandatory files or known unresolved contradictions mean partial/blocked delivery, with the exact failure disclosed and only real files linked. An unavailable parser means syntax validation is unperformed or partial, not that successful parsing happened. An unavailable renderer means A4 page count remains unverified; a PDF cannot replace the Markdown. Detailed checkpoints and working records stay private by default.

# 7. Converters

No converter is bundled or certified; the model uses whatever the host provides. Before relying on your own Markdown-to-PDF converter instead, check its actual A4 capability, substantive-body page counting, document-class selection, asset paths, citation-target handling, and diagram dependencies. A screen-reading layout must not be substituted for the A4 reference. Uploading a script to a project does not install its tools or fonts.

# 8. Limitations

Archive, parser, identity, and locator checks can test file mechanics; cross-file review can find obvious specification contradictions. Neither establishes scientific truth, model reliability, recovery robustness, or resistance to malicious source instructions. The design draws on published work about ambiguity, citation support, and reporting standards, but those references are background, not experiments validating this package. Whether the workflow improves research outcomes against an unstructured prompt has not been measured.

# Glossary

The protocol's Terms section defines the words the model uses (brief, issued RB, waiver, material change, and so on). This glossary explains the words used in this guide.

| Term | Meaning in this guide |
|---|---|
| Active RB | The exact scope file selected for the investigation, including its revision identity. |
| Approval basis | A truthful reference to what scope was approved, or a record of the waiver. |
| Brief | The identified proposal shown for scope agreement before the RB is created. |
| Central-evidence appraisal | Assessing the design, limits, independence, and applicability of evidence that drives a conclusion. |
| Companion | A faithful structured analytical view of the same research, not an authority or independent evidence source. |
| Checkpoint | A saved working record for resuming execution; it is not the scope contract or report. |
| Coverage map | A proportionate record of progress and evidence gaps for accepted research questions. |
| Disposition | Whether material was retained for a specific purpose, or declined with a reason. |
| Evidence gap | Adequate support was not found in the stated search; not proof that support does not exist. |
| Immutable | Preserved without changing its bytes; revisions are saved as distinct artifacts. |
| Online LLM project | A hosted assistant workspace with configurable project instructions and uploaded files. |
| Pandoc Markdown | The Markdown dialect selected for the editable research files. |
| Provenance | Information about where a record, claim, or artifact came from and how it was produced. |
| Reference layout | The fixed A4 rendering configuration used to measure the substantive-page cap. |
| Research Boundaries (RB) | The standalone contract defining intended research and accepted constraints. |
| Source activity unknown | Insufficient recorded information to establish how a source was handled. |
| Stopping reason | Why investigation closed normally or ended under an actual constraint. |
| Supersedes | A pointer from a newer revision to the exact earlier artifact it replaces for active use. |

# Bibliography

### [1] Projects in ChatGPT {#ref-1}

OpenAI. *Projects in ChatGPT*. Official product documentation, inspected 17 October 2026, sections “Add files” and “Add project instructions.” One example of a host offering project instructions and uploaded files; supports the configuration concept, not automatic full-file reading or identical tools across hosts.

Original source: <https://help.openai.com/en/articles/10169521-projects-in-chatgpt>

### [2] Prompt engineering {#ref-2}

OpenAI. *Prompt engineering*. Official developer documentation, accessed 14 October 2026. Relevant section: non-deterministic generation and prompt design.

Original source: <https://developers.openai.com/api/docs/guides/prompt-engineering>

### [3] CLAMBER {#ref-3}

Tong Zhang, Peixin Qin, Yang Deng, Chen Huang, Wenqiang Lei, Junhong Liu, Dingnan Jin, Hongru Liang, and Tat-Seng Chua. 2024. *CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models*. ACL 2024, pp. 10746–10766. Peer-reviewed conference paper. Used for its general finding from the publication record and abstract; detailed experimental scores are not reproduced.

Original source: <https://aclanthology.org/2024.acl-long.578/>

DOI: <https://doi.org/10.18653/v1/2024.acl-long.578>

### [4] PRISMA-ScR checklist {#ref-4}

PRISMA. *Preferred Reporting Items for Systematic reviews and Meta-Analyses extension for Scoping Reviews: Checklist*. Reporting guidance; fillable checklist version dated September 2019. Relevant items: objectives, eligibility criteria, information sources, search, and limitations. Used as reporting guidance, not as evidence that this workflow meets the full standard.

Official overview: <https://www.prisma-statement.org/scoping>

Checklist: <https://www.prisma-statement.org/s/PRISMA-ScR-Fillable-Checklist_11Sept2019.pdf>

### [5] Enabling Large Language Models to Generate Text with Citations {#ref-5}

Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. *Enabling Large Language Models to Generate Text with Citations*. EMNLP 2023, pp. 6465–6488. Peer-reviewed conference paper introducing ALCE. Used for the distinction between answer correctness and citation support, without extrapolating a numerical failure rate to current models.

Original source: <https://aclanthology.org/2023.emnlp-main.398/>

DOI: <https://doi.org/10.18653/v1/2023.emnlp-main.398>

### [6] Pandoc User's Guide {#ref-6}

Pandoc project. *Pandoc User's Guide*. Official technical documentation, accessed 14 October 2026. Relevant sections: output formats, heading identifiers, raw HTML, resource paths, and citation rendering.

Original source: <https://pandoc.org/MANUAL.html>

### [7] Mermaid CLI {#ref-7}

Mermaid project. *mermaid-cli*. Official project README, accessed 14 October 2026. Relevant sections: diagram output formats and transforming Markdown with Mermaid diagrams.

Original source: <https://github.com/mermaid-js/mermaid-cli>

### [8] Complex Images {#ref-8}

World Wide Web Consortium, Web Accessibility Initiative. *Complex Images*. Official accessibility guidance, accessed 14 October 2026. Relevant sections: two-part text alternatives and accompanying explanations.

Original source: <https://www.w3.org/WAI/tutorials/images/complex/>

### [9] JSON serialization {#ref-9}

IETF. RFC 8259, December 2017. *The JavaScript Object Notation (JSON) Data Interchange Format*. Inspected 17 October 2026, sections 4, 6–9: unique member-name guidance, permitted values, UTF-8, strings, and parsing. Supports syntax/interoperability choices, not the semantic contract or AI benefit.

Original source: <https://www.rfc-editor.org/rfc/rfc8259.html>

### [10] Explicit heading identifiers {#ref-10}

Pandoc project. *Pandoc User's Guide*, “Extension: header_attributes.” Inspected 17 October 2026. Describes explicit heading identifiers; does not certify all renderers or relocation of renamed files.

Original source: <https://pandoc.org/MANUAL.html#extension-header_attributes>
