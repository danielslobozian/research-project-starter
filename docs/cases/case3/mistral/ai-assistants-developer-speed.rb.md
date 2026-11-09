---
title: "Research Boundaries: Do AI coding assistants measurably speed up experienced developers?"
protocol_version: "1.7b.10"
research_id: "ai-assistants-developer-speed-2026-11"
rb_version: "1.0"
approval_status: "approved"
approval_basis: "Explicit approval of BR-001; scope reproduced in sections 1-9"
approved_brief_id: "BR-001"
approval_date: "2026-11-09"
report_basename: "ai-assistants-developer-speed"
supersedes: null
---

# 1. Research objective and motivation

AI coding assistants (tools such as GitHub Copilot and Cursor that suggest or generate code inline or through chat) are widely reported to make developers dramatically faster. The most widely quoted figure is that they make developers "55% faster", cited in the requesting conversation as a claim made by a manager. This investigation examines whether AI coding assistants measurably increase the productivity of experienced developers, how reliable the evidence behind the "55% faster" figure is, and whether perceived speed corresponds to measured net productivity. That measured gains transfer to experienced developers on large existing codebases, and that perceived speed equals real productivity, are premises to test, not established facts.

# 2. Primary research question

**Q0.** Do AI coding assistants measurably increase the productivity of experienced developers, and does the evidence support the widely quoted "55% faster" claim?

# 3. Secondary research questions

**Q1.** What is the provenance of the "55% faster" figure — which study produced it, on what population, on what tasks, and by what measurement?

**Q2.** How do measured effects of AI coding assistants vary by developer experience and by codebase size and maturity?

**Q3.** What explains gaps between perceived and measured productivity (self-reported versus instrumented outcomes, code review and rework costs, defect rates)?

# 4. Included scope

- Populations: experienced professional software developers; results for novices and students are included only as contrast.
- Interventions: AI coding assistants of the modern large-language-model era (roughly 2022 to the search date), such as GitHub Copilot, Cursor, and comparable tools.
- Evidence: controlled studies with measured outcomes (randomised trials, field experiments) and credible large-sample studies using instrumented telemetry; primary sources (peer-reviewed or preprint) over press coverage.
- Settings: large or existing codebases as the priority setting; new, small, or greenfield projects included as contrast.
- Outcomes: measured developer productivity, including speed and quality-adjusted net outcomes (defects, rework, maintenance).

# 5. Exclusions

- Not a tool-versus-tool buying guide or product recommendation.
- Populations of novices and students are covered only as contrast, not as a primary basis for the answer.
- Job-market and economic effects of AI coding assistants are excluded.
- General AI writing assistance beyond coding is excluded.

# 6. Research approach and evidence expectations

Structured narrative evidence review: identify, appraise, and synthesize the available evidence without claiming exhaustive or systematic-review coverage. For each key study, extract its design, population, task type, effect sizes, and confidence intervals, and appraise its internal validity and measurement approach. Null and negative results receive the same weight as positive ones. Evidence about experienced developers on large existing codebases is weighed as most applicable. Uncertainty is handled by reporting effect ranges and confidence intervals rather than single-point claims, and by stating clearly where evidence is thin or conflicting. Access limits: paywalled sources are appraised from accessible material (for example an abstract or preprint version) and recorded as a limitation; remembered knowledge is not an inspected source. Closure expectation: each question receives an answer or an explicit pending or blocked status.

# 7. Status of examples

No scope-defining examples supplied. The "55% faster" claim is a premise to be traced and appraised, not a mandatory case. The named tools (GitHub Copilot, Cursor) are illustrations of the tool class, not mandatory comparisons.

# 8. Deliverable contract

- Audience/prior knowledge: A senior backend developer with about 15 years of experience, comfortable with statistics (effect sizes, confidence intervals, randomised trials), and a technical manager who is not a researcher; both readers work in or around experienced software development.
- Language: English.
- Explanation depth: The intuitive idea first, then the technical and statistical detail (effect sizes, confidence intervals, trial design) wherever findings depend on it; specialist terminology explained in ordinary language for the non-researcher reader.
- Purpose/use: Check the widely quoted "55% faster" claim and cite the sources back to the manager.
- Reader context: Experienced developers working on large existing codebases, not new small projects.
- Reader artifact: Self-contained HTML; exact filename ai-assistants-developer-speed.html.
- Markdown source for tools: ai-assistants-developer-speed.md.
- Additional reader artifact: None. PDF production was untested at the capability check and is offered only after confirmation.
- Citation style: Numbered Markdown links to an anchored bibliography, each cited claim with a locator (section, page, or position) in the inspected source.
- Visuals: Explanatory diagrams or data graphics where they help the reader judge the evidence, for example a study-by-study effect comparison; no decorative quota.
- Reference layout: A4 reference layout (210 x 297 mm, 11 pt body text, 25 mm margins, 1.15 line spacing).
- Body limit: 12 pages of substantive body, with a tolerance of 25% (up to 15 pages); a ceiling, not a target.
- Length limit the user gave in another unit: None.
- Capability gaps at issue: Browser/visual inspection untested; fallback: deliver the HTML after source and link inspection and disclose that browser, mobile, and print inspection was not performed. PDF production untested; fallback: if an accepted PDF cannot be produced, deliver the same reader-adapted content as self-contained HTML labelled as a substitute reading copy, and name the missing format.

Process rules (public artifacts, page counting, consistency, presentation changes, revisions, later capability fallbacks) come from the protocol version used for execution; `protocol_version` above records the version used to create this RB.

# 9. Assumptions, uncertainties, and open boundaries

- The exact provenance of the manager's "55% faster" figure is unknown. Assumption (adopted with approval of BR-001): treat GitHub's 2023 Copilot completion-time experiment as the apparent leading candidate, and appraise the figure wherever it originates; if the traced provenance differs, the appraisal covers the actual source.
- The manager's exact wording is unknown. Assumption: the claim is treated as "AI assistants make developers 55% faster".
- Scope of "faster": Assumption (adopted with approval of BR-001): "faster" includes quality-adjusted outcomes — defects, rework, maintenance — as part of net productivity, since raw speed claims ignore them.
- The review covers evidence available at the actual search date; later studies may change the answer.
