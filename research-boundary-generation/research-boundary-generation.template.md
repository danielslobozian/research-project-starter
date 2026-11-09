---
title: "Research Boundaries: <descriptive topic title>"
protocol_version: "1.7b.10"
research_id: "<stable-investigation-id>"
rb_version: "1.0" # "1.0" for the initial issue; each revision increments the second number (1.1, 1.2, ...).
approval_status: null # Required at issue: approved or assumptions-not-explicitly-approved.
approval_basis: null # Required at issue: the actual approval or waiver basis, factual and impersonal, e.g. "Explicit approval of <brief ID>; scope reproduced in sections 1–9", "Explicit approval of <brief ID> with the boundary added in the approving reply (<change>); scope reproduced in sections 1–9", or "Scope approval explicitly waived; assumptions recorded in section 9".
approved_brief_id: null # The approved brief ID when known; otherwise null.
approval_date: null # The actual approval date when known, as a quoted "YYYY-MM-DD" string; always null for a waiver.
report_basename: "<topic-slug>"
supersedes: null # Exact prior RB filename for a revision; null for the initial issue.
revision_note: null # Revisions only: one line describing what changed. Delete this line for the initial issue.
---

<!-- Template, protocol 1.7b.10. Words such as accepted, issued, waiver, and material change have the meanings in the protocol's Terms section. Replace each <a | b> placeholder with exactly one option, without the angle brackets, and turn the option's descriptive parts (such as "the PDF filename", "the reason", "the accepted percentage") into the actual values. Quote YAML values that contain a colon, a #, or quotation marks: in double quotes, escaping any double quote or backslash inside, as the template's own values are, so the front matter stays valid YAML.
For an initial RB, fill every section from the accepted brief together with every earlier brief it revises, or under a waiver from the stated assumptions; a revised brief that shows only changes is not the whole scope. For a revision, start from the prior issued RB and apply only the accepted changes. Keep all nine numbered sections and add no material scope.
Before issue, remove this whole comment block (including the provenance line below), every YAML # comment, and every <...> placeholder of this template (angle brackets and # characters that belong to accepted content stay); check that no placeholder or null approval_status or approval_basis remains.
Adapted for engine 1.7b.10 from the supplied RB template; historical provenance is retained in the changelog.
-->

# 1. Research objective and motivation

<Describe the accepted phenomenon or problem without assuming the suspected explanation is true.>

# 2. Primary research question

**Q0.** <The exact accepted neutral primary question.>

# 3. Secondary research questions

<List each accepted secondary question on its own line with its accepted ID, in the form **Q1.** followed by the question; keep existing IDs and gaps in a revision. If there are none, write "No separate secondary questions.">

# 4. Included scope

<Accepted domains, systems, populations, cases, comparison/baseline, and time range, and, if the brief named one, the fixed corpus. Only accepted restrictions and mandatory cases.>

# 5. Exclusions

<Accepted non-goals and limits on generalization. If none were specified, write "No exclusions specified.">

# 6. Research approach and evidence expectations

<The accepted review type, claim-appropriate evidence, comparison and appraisal approach, handling of uncertainty, and access limits, written as planned actions rather than completed searches. If a fixed corpus was accepted, name it and state that no searching goes beyond it.>

# 7. Status of examples

<If examples were supplied, label each as illustrative or a mandatory case according to the accepted brief. Only if no examples were supplied, write "No scope-defining examples supplied." Keep this section.>

# 8. Deliverable contract

- Audience/prior knowledge: <accepted background, expertise and age or level when relevant>
- Language: <accepted language>
- Explanation depth: <accepted depth, including needed terminology, method and statistics explanations>
- Purpose/use: <what the reader will do with the report (decide, understand, explain to others, check, cite, ...), within the accepted research scope>
- Reader context: <the reader's situation where it makes some evidence more applicable (place, population, age group, setting, constraint), in impersonal words without names | None>
- Reader artifact: <accepted format and exact filename; HTML or PDF, another format only with confirmed host support>
- Markdown source for tools: <exact .md filename; not the reading copy>
- Additional reader artifact: <accepted extra format and exact filename, or None>
- Citation style: <accepted portable citation form and locator expectations>
- Visuals: <accepted explanatory needs or preferences; no decorative quota>
- Reference layout: <A4 reference layout, or the accepted alternative with page size, font size, margins, and line spacing>
- Body limit: <accepted limit> pages of substantive body in the reference layout, with a tolerance of <25% (default) | the accepted percentage | 0% (strict)>
- Length limit the user gave in another unit: <the user's figure and unit, from which the page limit was estimated | None>
- Capability gaps at issue: <each capability that was unavailable or untested at the capability check, with its fallback, or "None">

Process rules (public artifacts, page counting, consistency, presentation changes, revisions, later capability fallbacks) come from the protocol version used for execution; `protocol_version` above records the version used to create this RB.

# 9. Assumptions, uncertainties, and open boundaries

<Unresolved scope or access details, the assumptions behind the scope (including those adopted for unanswered brief questions), and their limits. Under a waiver, state the assumptions without claiming their approval. No findings and no retrospective justification of the scope.>
