---
title: "Research Boundaries: AI coding assistants: measured versus perceived productivity in experienced developers"
protocol_version: "1.7b.10"
research_id: "ai-coding-assistants-productivity-2026-11"
rb_version: "1.0"
approval_status: "approved"
approval_basis: "Explicit approval of BR-001; scope reproduced in sections 1–9."
approved_brief_id: "BR-001"
approval_date: "2026-11-09"
report_basename: "ai-coding-assistants-productivity"
supersedes: null
---

# 1. Research objective and motivation

Investigate whether, and under what conditions, AI coding assistants change experienced developers' measured productivity and software quality when working on large existing codebases, and whether perceived productivity gains correspond to measured outcomes. Neither a general speed advantage nor an illusion of increased productivity is assumed.

The claim that AI assistants make developers “55% faster” requires a mandatory fact-check of its provenance, exact wording, measurement, uncertainty, and applicability to this development setting. The investigation is intended to establish what the evidence supports, rather than treating that figure as an established general result.

# 2. Primary research question

**Q0.** For experienced developers working on large existing codebases, how do AI coding assistants affect end-to-end task completion time and software quality, compared with working without them, and how do measured effects compare with perceived gains?

# 3. Secondary research questions

**Q1.** What does the evidence underlying “55% faster” actually measure, including the distinction between reduced completion time and increased work rate, and what generalisation does its design support?

**Q2.** What effects remain when prompting, checking, testing, review, and rework are counted, with quality and task completion assessed alongside speed? How closely do developers’ expectations and retrospective impressions match those measurements?

**Q3.** Which differences by task, developer experience, repository familiarity, assistant familiarity, and tool version are supported by evidence? What explains conflicting results or perception–performance gaps, and what remains speculative?

# 4. Included scope

- **Target population and setting:** Experienced professional developers maintaining, debugging, testing, and extending large existing codebases. Distinguish general development experience, familiarity with the repository, and experience using the assistant. Backend development is the relevance lens, not a restriction to particular programming languages.
- **Intervention and comparison:** AI coding assistants used in development workflows, compared with working without them. Distinguish assistant versions and workflows when assessing the evidence.
- **Outcomes:** End-to-end task completion time, task completion, and software quality, including time spent prompting, checking, testing, reviewing, and reworking. Compare measured effects with both expectations and retrospective impressions where these are evaluated.
- **Mandatory claim investigation:** Trace plausible origins of the “55% faster” claim, establish what the underlying evidence measures and supports, and assess its applicability to experienced developers working on large existing codebases. Do not assume which source originally conveyed the claim.
- **Transferability evidence:** Include studies involving novices or small new projects only to trace the claim or assess transferability to the target population and setting.
- **Coverage:** Foundational studies and relevant developments available at the actual search date. No fixed source corpus is prescribed.

# 5. Exclusions

Product rankings, purchasing recommendations, and employment forecasts are excluded.

Novice developers and small new projects are not independent target populations or settings. Evidence from them must not be treated as directly representative of experienced developers working on large existing codebases; its inclusion is limited to claim tracing and transferability assessment.

# 6. Research approach and evidence expectations

Use a structured narrative evidence review, not an exhaustive systematic review.

Prioritise publicly inspectable primary studies, particularly randomised evaluations and realistic workplace evaluations. Separate causal evidence from observational associations, surveys, vendor claims, and anecdotes. Evaluate the evidence underlying a claim rather than treating its repetition as confirmation.

For relevant studies, examine sample selection, randomisation, controls, outcome definitions, effect sizes, confidence intervals, missing outcomes, sponsorship, and applicability to the target setting. Identify whether time estimates include prompting, checking, testing, review, and rework, and whether quality and task completion are assessed alongside speed. Examine how expectations and retrospective perceptions are measured and compared with observed performance.

For the “55% faster” claim, investigate provenance and exact wording, identify the measured quantity and its uncertainty, and distinguish percentage reductions in completion time from percentage increases in work rate. Assess what the underlying design supports and what it does not establish for the target setting. Because the quoted source is unspecified, trace plausible origins without asserting that any one is the source originally encountered.

Compare studies with attention to task, developer experience, repository familiarity, assistant familiarity, tool version, and workflow. Do not pool unlike interventions as though they were equivalent. Distinguish evidence-supported explanations for conflicting results or perception–performance gaps from speculative mechanisms and unresolved confounding.

Give each research question a supported answer or an explicit evidence-gap statement. Disclose inaccessible sources, unresolved attribution, relevant uncertainty, and limits on generalisation.

# 7. Status of examples

The statement that AI assistants make developers “55% faster” is a **mandatory fact-check**, not merely an illustrative example and not an assumed finding. Its original source has not been supplied.

No particular assistant, programming language, workplace, or repository has been designated as a mandatory case. Backend work supplies a relevance lens within the accepted target setting.

# 8. Deliverable contract

- **Audience/prior knowledge:** A statistically literate senior backend developer familiar with effect sizes, confidence intervals, and randomised trials, and a technical manager who is not a researcher.
- **Language:** English.
- **Explanation depth:** A manager-facing summary followed by sufficient technical and methodological detail to judge the conclusions. Explain study methods and terminology where needed, while retaining the statistical detail appropriate to the audience.
- **Purpose/use:** Check the “55% faster” claim, judge how far its supporting evidence applies to the target setting, and provide source-backed wording and citations suitable for discussing the claim with a technical manager.
- **Reader context:** Professional backend development on large existing codebases; no particular workplace, language, repository, or assistant is specified.
- **Reader artifact:** A self-contained HTML reading copy named `ai-coding-assistants-productivity.html`.
- **Markdown source for tools:** `ai-coding-assistants-productivity.md`, containing the same substantive content as the reading copy and explicitly labelled as source for tools, not the reading copy.
- **Additional reader artifact:** None.
- **Citation style:** Numbered Markdown links to an anchored bibliography, with linked references and precise source locations sufficient to inspect the support for claims.
- **Visuals:** A study-comparison table; explanatory diagrams or data graphics only where useful.
- **Reference layout:** A4 (210 × 297 mm), 11-point body text, 25 mm margins, and 1.15 line spacing.
- **Body limit:** 20 A4 pages of substantive body in the reference layout, with a 25% tolerance, allowing up to 25 pages. This is a ceiling, not a target.
- **Length limit the user gave in another unit:** None.
- **Capability gaps at issue:** Reference-layout print pagination was untested at scoping. The execution session will recheck relevant host capabilities and verify the substantive-body page count if possible; otherwise it will explicitly state “Substantive body page count: unverified.” File creation and HTML preview checks were reported as passed during scoping; those results do not establish execution-host capabilities.

Process rules (public artifacts, page counting, consistency, presentation changes, revisions, later capability fallbacks) come from the protocol version used for execution; `protocol_version` above records the version used to create this RB.

# 9. Assumptions, uncertainties, and open boundaries

The original source of the quoted “55% faster” claim is unknown. Approval adopts the approach of tracing plausible origins without assuming which source was encountered; unresolved attribution must remain explicit.

No numerical threshold for “experienced” or “large existing codebase” has been prescribed. Preserve the target population and setting while reporting relevant study definitions and differences in general development experience, repository familiarity, and assistant familiarity. Do not silently substitute evidence from novices or small new projects for direct evidence about the target setting.

No specific workplace, language, codebase, or coding assistant requires special emphasis. Backend work informs relevance without imposing a language restriction.

The evidence cutoff is the actual search date, not the RB approval date. Public inspectability is prioritised; any access limitations encountered and their consequences for the questions must be disclosed. Whether the available evidence establishes specific causes of conflicting results or perception–performance gaps remains an open research question.
