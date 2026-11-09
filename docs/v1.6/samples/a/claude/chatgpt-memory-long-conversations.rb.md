---
title: "Research Boundaries: How ChatGPT Retains Information Across Conversations and Projects, and Whether Long Conversations Degrade Answer Quality"
protocol_version: "1.6"
research_id: "chatgpt-memory-long-conversations-2026-11"
rb_version: "1.0"
approval_status: "approved"
approval_basis: "Explicit approval of BR-002 (revising BR-001) with the presentation change made in the approving reply (strict 5-page body limit, 0% tolerance); scope reproduced in sections 1–9"
approved_brief_id: "BR-002"
approval_date: "2026-11-03"
report_basename: "chatgpt-memory-long-conversations"
supersedes: null
---

# 1. Research objective and motivation

Users of ChatGPT, including users who keep several conversations inside the same ChatGPT Project, report that recall of earlier information appears inconsistent: some details from weeks earlier are recalled, while important information from a recent conversation is not. Users also report an impression that answer quality declines as a conversation becomes very long. The investigation aims to explain, for a non-specialist reader, which mechanisms determine whether earlier information is kept and used, and whether a decline in quality over long conversations is a documented effect, under what conditions it occurs, or whether the impression may arise partly from other factors (for example harder later requests or changes to the model). Neither inconsistent memory nor quality decline is assumed to be demonstrated at the outset; both are treated as observations to explain.

# 2. Primary research question

**Q0.** What determines whether ChatGPT, including within ChatGPT Projects, keeps and uses information from earlier conversations, and does answer quality change as a conversation gets longer?

# 3. Secondary research questions

**Q1.** What kinds of "memory" does ChatGPT have (the current conversation, saved memories, past-chat lookup, Project files and Project-level memory), and how do they explain why something from weeks ago may be recalled while something from yesterday is not?

**Q2.** Does research show that answers really get worse in long conversations, or could the effect be partly an impression, and under what conditions does it happen?

**Q3.** What practical habits does the evidence or OpenAI's documentation support for getting more reliable recall and answers?

# 4. Included scope

- ChatGPT as the focus, in particular how ChatGPT Projects handle information across separate conversations, described from OpenAI's official documentation as available at the actual search date.
- The different memory mechanisms in ChatGPT (the context of the current conversation, saved memories, reference to past chats, Project files and Project-level memory), including how a user can check which memory settings are enabled, given that settings and features differ by plan and change over time.
- The general mechanisms of large language model chat assistants needed to explain these behaviours (for example the limited context a model processes at once).
- Research on model performance with long inputs and long multi-turn conversations, drawn from studies of large language models in general, because few studies test ChatGPT specifically; applicability to ChatGPT is stated explicitly.
- Coverage: foundational work plus relevant developments available at the actual search date; no fixed time range.

# 5. Exclusions

- The requester's personal conversations are not examined or analysed.
- Undocumented internal details of ChatGPT's implementation are not covered beyond what official documentation or published research supports.
- Other chat products are not covered, except where a study included in the review happens to use them.
- No product rankings or comparisons of which assistant is best.
- No heavy mathematics.

# 6. Research approach and evidence expectations

- Review type: structured narrative evidence review; not an exhaustive or systematic review.
- Evidence for ChatGPT's memory features: OpenAI's official documentation and help pages, recorded with the date they were consulted; vendor documentation is treated as a description of intended behaviour, not as independent evidence of performance.
- Evidence for quality changes in long conversations: original empirical studies (peer-reviewed papers and preprints, with publication status labelled), appraised for tested models, task types, context lengths, metrics, and applicability to ChatGPT conversations.
- Counterevidence and boundary conditions are searched for actively, including results that do not show degradation and alternative explanations for perceived decline.
- Documented facts, cross-source synthesis, and reasonable inference are kept clearly separated; practical habits are presented as conditional options tied to their evidence, not as instructions.
- Uncertainty, access limits (for example paywalled sources read only as abstracts), and the date-dependence of product documentation are disclosed.

# 7. Status of examples

The reported observations (a detail from weeks earlier recalled while information from the previous day was forgotten, including within the same Project; answers that seemed to worsen in very long conversations) are illustrative of the phenomenon. They are not mandatory cases to be tested, and they are not examined through the requester's own conversations.

# 8. Deliverable contract

- Audience/prior knowledge: an interested non-specialist with no software-engineering background, approximately 15–18-year-old reading level, without a childish tone
- Language: English
- Explanation depth: the intuitive idea first, then the technical detail needed to follow and judge the evidence; no heavy mathematics
- PDF: Yes, chatgpt-memory-long-conversations.pdf
- Reference layout: A4 reference layout (A4, 11 pt body text, 25 mm margins, 1.15 line spacing)
- Body limit: 5 pages of substantive body in the reference layout, with a tolerance of 0% (strict)
- Length limit the user gave in another unit: None
- Capability gaps at issue: None (file creation, web search, code execution, and PDF rendering were confirmed available at the capability check)

Process rules (public artifacts, page counting, consistency, presentation changes, revisions, later capability fallbacks) come from the protocol version used for execution; `protocol_version` above records the version used to create this RB.

# 9. Assumptions, uncertainties, and open boundaries

- Which ChatGPT memory settings are enabled for the requester is unknown; the report covers both the enabled and disabled cases and explains how a user can check them.
- ChatGPT's memory and Project features vary by subscription plan and change over time; descriptions apply to the documentation available at the actual search date and may not match every account.
- Few published studies test ChatGPT's consumer product directly; findings from studies of other models or of API access are applied to ChatGPT with explicitly stated limits of applicability.
- How Project-level memory interacts with account-level memory settings may be only partly documented; undocumented aspects are reported as unknown rather than inferred as fact.
- The strict 5-page body limit constrains depth; each question receives at least a short answer, and material shortened or omitted for length is to be disclosed in the report's limitations section.
