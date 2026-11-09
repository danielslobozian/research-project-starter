# Why ChatGPT Projects sometimes “forget”

Memory, long conversations and practical reliability — 3 November 2026

*Memory, long conversations and practical reliability | Focused evidence review | 3 November 2026*

> **Short answer.** A Project is an organized place where ChatGPT *can* draw on related chats, files and instructions; it is not a promise to reread or perfectly retain every past exchange. OpenAI explicitly says Memory does not retain every detail. A long chat can also become harder to use accurately, even before any visible size limit is reached. The most dependable response is to put critical facts in a short, maintained project source and explicitly ask ChatGPT to use it. [1–3]

### 1 | Three different ways information can be available

**The current conversation.** Your messages, replies and material supplied for the present task form the immediate working context. That context is finite: as a conversation grows, a model cannot necessarily use every earlier word at once. OpenAI describes a “context window full” notice and warns that a continuation summary can omit details or exact wording. [3]

**The Project’s chats and sources.** A Project groups past conversations, uploaded reference files and project-specific instructions. ChatGPT *can* use them in later project chats. An uploaded or saved source is a much clearer place to keep a confirmed decision than hoping it will be reconstructed from an old discussion. However, “can use” is not “will find and apply the right passage on every turn.” [1]

**Personal Memory.** With Memory enabled, ChatGPT may use broader summaries, relevant preferences and details from past chats or other permitted sources. Availability and controls vary by plan and setting. OpenAI says remembered information is selective and may change; a Memory summary is a high-level view, not a transcript or a complete inventory. [2]

### 2 | What Project-only memory actually changes

Projects offer **default** and **project-only** memory. Project-only keeps references to past conversations inside that Project and excludes personal memories and chats from outside it; shared Projects use it automatically. With default memory, chats can reference the same Project, while cross-project access depends on the plan and workspace settings. Account and workspace memory controls must also permit the feature. [1]

Since August 2026, eligible existing unshared Projects can switch memory mode in **Project settings → Memory**; OpenAI says changes may take a few hours. There is no browseable list of “project memories.” These settings define *where information may be referenced*, not a guarantee that all eligible information will surface. [1,11]

*Evidence labels used below: DOCUMENTED = OpenAI product guidance; TESTED = a published experiment under stated conditions; INFERENCE = plausible explanation, not confirmed ChatGPT internals.*


---

## Why recall can be inconsistent

### 3 | One symptom, several possible explanations

Imagine a Project containing an older chat about a preferred writing style and a recent chat that changes a delivery deadline. A later answer uses the old style correctly but states the old deadline. That pattern does *not* show that ChatGPT processes Project history oldest-first or that the newer chat was erased.

- **Selection and relevance (DOCUMENTED).** OpenAI says memory uses information it judges relevant, rather than all previous details; Project content is context that may be used. A durable preference might therefore appear more often than a one-off date. What gets selected for any particular question is not publicly auditable. [1,2]

- **Finding the right evidence (TESTED outside Projects).** LongMemEval separates memory into finding information, retrieving it, and using it to answer. Tested systems can fail at any stage. It is *reasonable to hypothesize* similar categories of error for Projects, but OpenAI has not disclosed a complete Project retrieval pipeline. [7]

- **Newer facts overriding older ones (TESTED outside Projects).** Memory benchmarks specifically test knowledge updates and dates. A system may retrieve the earlier and the later statement yet mishandle which one is current. This is one explanation for a stale answer, not proof of any particular incident. [7,10]

- **Missing active context (DOCUMENTED in principle).** A chat has limited working space; summaries of a previous chat may omit exact instructions. OpenAI does not publish a general rule specifying which turns of a Project conversation are dropped or retained for every model. [3]

- **Conflicting instructions or inferred assumptions (TESTED in dialogue research).** When a task unfolds over turns, an assistant can anchor on its first interpretation, reuse a previous mistake, or underweight corrections. This can resemble forgetting even when the information was presented. [9]

### 4 | The distinction that prevents false diagnoses

“It forgot” may mean at least three different things: **the fact was not available** in usable context; **the fact was available but not found**; or **the fact was found but misapplied**. A wrong answer alone cannot distinguish them. Also consider mundane causes: a conversation outside the Project, a memory-setting change, missing source material, or a question that did not signal which past detail mattered. [1–3]

There is no publicly verified evidence that all chats within a Project are always loaded together, that the most recent chat is always retrieved first, or that a particular “memory consolidation” algorithm explains the reported experiences. Avoid treating such suggestions as known product architecture.

### 5 | A fair test of a missed fact

Try the same question **(a)** without prompting, **(b)** with the earlier conversation named or linked, and **(c)** with the authoritative sentence pasted. If (c) works but (a) does not, access or selection is a candidate issue; if even (c) fails, interpretation or instruction conflict becomes more plausible. This is a simple diagnostic suggestion, **not** a validated method for isolating the backend cause.


---

## Do long conversations get less reliable?

### 6 | What controlled studies actually found

**Position matters: Liu et al., 2024 (TESTED).** On multi-document question answering and key-value retrieval, GPT-3.5-Turbo, Claude 1.3 and two open models often performed better when the relevant passage was near the start or end than in the middle. This is evidence of a long-input *position effect*; it does not prove that current ChatGPT loses every middle-of-chat fact. [5]

**Advertised capacity is not usable recall: RULER, 2024 (TESTED).** Seventeen long-context models were evaluated on 13 synthetic tasks involving retrieval, tracing and aggregation. Many degraded as context grew, even if simple “find the phrase” tests were easy. This was an older model set and synthetic evaluation, so its numeric thresholds should not be carried over to ChatGPT today. [6]

**Meaning can be harder than literal matching: NoLiMa, 2025 (TESTED).** Thirteen models were assessed on synthetic questions whose wording barely overlapped with the buried clue. At 32,000 input tokens, 11 fell below half their short-input baseline; GPT-4o fell from 99.3% to 69.7% accuracy. The experiment tests locating implicit associations in supplied text, not memory inside ChatGPT Projects. [8]

**Cross-session memory is difficult: LongMemEval, 2025 (TESTED).** Five hundred curated questions probe extracting facts, combining sessions, handling time and updates, and saying “I don’t know.” Evaluated assistants and long-context systems showed substantial declines (the authors report about a 30% accuracy drop in sustained-interaction conditions); changes to indexing and retrieval improved results. The benchmark used custom constructed histories and systems, *not* a direct audit of ChatGPT Projects. [7]

**Multi-turn reasoning can drift: Laban et al., ICLR 2026 (TESTED).** Across more than 200,000 simulated dialogues, 15 models (including GPT-4.1, o3, Claude 3.7 and Gemini 2.5) averaged a 39% relative performance reduction across six generation tasks when requirements arrived in successive turns instead of one complete prompt. The tasks were simulated and the tested model versions predate current ChatGPT. The result concerns *incremental specification and error propagation*, not simply how many tokens are in a chat. [9]

### 7 | Newer evidence, and evidence that complicates the story

RHELM, published in October 2026, tests evolving synthetic user histories linked to emails and files. Even full-context and dedicated memory systems struggle with multi-source, temporal and aggregation questions; stronger newer models improve some scores. Therefore, “all long chats inevitably deteriorate” is too strong. Outcomes depend on model, task, clue location, contradictions and how context is supplied. RHELM likewise does not test ChatGPT Project settings. [10]


---

## How to interpret “deterioration” in practice

### 8 | Three pathways that can look alike

**Length pressure.** Adding dozens of exchanges increases the amount of potentially relevant material and the chance that an important line is hard to find or outside the current working context. The key distinction is *capacity versus effective use*: accepting a large input is not the same as reasoning perfectly over it. The studies support risk, not a universal failure point at a particular message count. [3,5,6,8]

**Interaction pressure.** Long collaborations accumulate partially specified requirements, revisions, rejected options and earlier assistant guesses. A model may confuse a discarded plan with an approved one or continue a line of reasoning built on an error. The 2026 multi-turn study reports this even in conversations with only a few turns; sheer length is not required. [9]

**Memory pressure across chats.** When a new Project conversation asks about something said elsewhere, the task now requires choosing appropriate past information, checking updates and applying it to the new question. LongMemEval and RHELM show why this is nontrivial in other systems, but they do not identify exactly how ChatGPT performs that selection. [1,7,10]

### 9 | Reasons not to overgeneralize

- **Not every study predicts every task.** The strongest long-context findings mostly come from designed tests with hidden clues, artificial distractors or simulated users. Reading one nearby paragraph and synthesizing several months of evolving decisions are very different tasks. [5–10]

- **Models and products change.** These papers span models released in 2023–2026. A benchmark score from GPT-4o, GPT-4.1 or a separate memory framework cannot be used as the current accuracy of consumer ChatGPT Projects. [5,8–10]

- **Refreshes help in some tests, not perfectly.** In Laban et al.’s supplemental GPT-4o/GPT-4o-mini experiments, restating cumulative requirements or adding a recap improved multi-turn answers, but did not restore single-turn performance. Simply telling a system to ask for clarification yielded mixed results. [9]

### 10 | So should you start a new chat?

**Yes, when the discussion has become crowded or tangled**—particularly after major changes of direction, repeated contradictory drafts, confusion about which decision is final, sluggish operation, or an explicit “context window full” notice. OpenAI itself advises trying a new chat for long or unresponsive conversations. [3,4]

**No, not automatically for every small extension.** Starting fresh can remove useful active context. A new chat works best with a short handoff: current goal, confirmed decisions, constraints, relevant source links, open questions, and what must *not* be treated as settled. A generated summary is convenient, but review it because summaries can omit exact wording. [3]

> **Useful rule of thumb (INFERENCE):** Maintain continuity in a small, explicit project reference; reset the conversation when the discussion itself becomes messy. This is a workflow recommendation, not a scientifically established turn-count threshold.


---

## A practical reliability playbook

### 11 | Actions matched to the failure they address

- **1. Keep a dated “current truth” document.** Record decisions, constraints, deadlines and source links; mark replaced facts as obsolete. Add it as a Project source or save a useful response with **Add to project sources**. **Documented feature; reliability benefit not directly tested.** [1]

- **2. Put standing rules in Project instructions.** State format, constraints and what to do if sources conflict. Project instructions override global custom instructions in that Project. Reserve changing details for a source file. **Documented feature; outcome not guaranteed.** [1]

- **3. Point explicitly to the source for critical claims.** For a deadline, number or accepted decision, say: “Use the latest approved project brief; quote the relevant line before deciding.” Check whether the answer actually names the source. **Inference** from known selection failures; source-based workflows are enabled by Projects. [1,7]

- **4. Make updates unambiguous.** Write “Decision changed on 3 November: Friday replaces Thursday; Thursday is obsolete.” Preserve dates and version labels. This targets stale-fact conflicts seen in memory benchmarks. **Indirect research support.** [7,10]

- **5. Periodically recap requirements and verify.** Before a long task, consolidate the confirmed requirements in one message; ask for a brief checklist of assumptions and compare it with the source. Recaps improved outcomes in a controlled multi-turn study, though were not a complete fix. **Direct research support for a different setting.** [9]

- **6. Begin a clean thread after a reset point.** When iterations drift, create a fresh Project chat, paste the vetted handoff and refer to the canonical document. OpenAI recommends a fresh chat for lengthy or sluggish threads; the handoff recipe is an **untested practical heuristic**. [3,4]

- **7. Verify high-stakes details yourself.** Use Project chat search to retrieve the original decision and compare quotations or dates with its source. Do not treat fluent recall as proof. **Documented search capability; general quality-control advice.** [1]

### 12 | Minimum setup that usually matters most

Start with **(i)** one dated source of confirmed facts, **(ii)** stable Project instructions, and **(iii)** an explicit request to consult the source. Update it when decisions change; open a new chat if the old one becomes tangled.

### Limits of this review

Focused, not systematic, review of sources through 3 November 2026. No personal chats were accessed and no live Projects experiment was run. The exact internal retrieval and context-selection steps, and thus causes of individual failures, are not publicly verifiable.

> **Bottom line:** Treat Project memory as a helpful, selective aid—not an authoritative archive. Make the important information easy to find, current, and explicitly referenced, and review its use when accuracy matters.

---

## Sources and evidence notes

This review distinguishes documented product guidance from independent experiments, and does not audit live Project conversations.

[1] OpenAI. “Projects in ChatGPT.” Help Center (accessed 3 Nov 2026).  https://help.openai.com/en/articles/10169521-projects-in-chatgpt

[2] OpenAI. “Memory in ChatGPT.” Help Center (accessed 3 Nov 2026).  https://help.openai.com/en/articles/8590148-memory-in-chatgpt

[3] OpenAI. “ChatGPT Free Tier FAQ.” Sections on full chats and continuation (accessed 3 Nov 2026).  https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq

[4] OpenAI. “Troubleshooting ChatGPT Error Messages.” Help Center (accessed 3 Nov 2026).  https://help.openai.com/en/articles/7996703-troubleshooting-chatgpt-error-messages

[5] Liu, N. F., et al. (2024). “Lost in the Middle.” TACL, 12, 157–173.  https://aclanthology.org/2024.tacl-1.9/

[6] Hsieh, C.-P., et al. (2024). “RULER: What’s the Real Context Size of Your Long-Context Language Models?”  https://arxiv.org/abs/2404.06654

[7] Wu, D., et al. (2025). “LongMemEval.” ICLR 2025.  https://mlanthology.org/iclr/2025/wu2025iclr-longmemeval/

[8] Modarressi, A., et al. (2025). “NoLiMa.” ICML 2025, PMLR 267.  https://proceedings.mlr.press/v267/modarressi25a.html

[9] Laban, P., et al. (2026). “LLMs Get Lost In Multi-Turn Conversation.” ICLR 2026.  https://proceedings.iclr.cc/paper_files/paper/2026/hash/59f6421e64707225fdf5b28840679a07-Abstract-Conference.html

[10] Zhang, H., et al. (2026). “Beyond Static Dialogues: ... Evolving Long-Horizon Memory.” Findings of EMNLP 2026.  https://aclanthology.org/2026.findings-emnlp.1679/

[11] OpenAI. “ChatGPT release notes.” 14 Aug 2026, project memory setting update.  https://help.openai.com/en/articles/6825453-chatgpt-release-notes
