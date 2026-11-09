---
title: "Why the engine works as it does"
subtitle: "Research Project Starter 1.7b.10 — design guide"
lang: en
guide_version: "1.7b.10"
updated: "2026-11-09"
---

# Summary

> This guide was written with Claude Opus 5.5.

Research Project Starter 1.7b.10 is two sets of project instructions for a hosted assistant such as ChatGPT, Claude
or Mistral Vibe. The **generation project** agrees a research question with you and issues a **Research Boundaries
(RB)** file. The **execution project** takes that file and researches it, and delivers a report to read, its
Markdown source and the unchanged RB.

This guide explains the design choices behind that workflow: why the work is split into two projects, why the first
reply asks about the reader, how a reader's situation differs from the research scope, what approval means, how the
research keeps the evidence that carries the answer, and what the delivered files promise. It is explanatory only.
The two protocols are the contract the models follow; this guide cannot override them. How to install and use the
projects is on the [engine page](https://danielslobozian.github.io/research-project-starter/engine.html).

# 1. Two projects, one contract

Deciding *what* to investigate and investigating it are different jobs with different risks. While the question is
being agreed, the risk is that early findings shape the scope: a model that has already read three studies tends to
draft a brief around them. While the research runs, the risk is the opposite: that inconvenient findings quietly
narrow the question.

The engine separates the two jobs into two projects joined by one file:

- The generation project may run a handful of searches to learn a field's vocabulary or to check that an
  interpretation is coherent, but it does not appraise sources or report findings. It ends when you approve a brief
  and it issues the RB. It never researches.
- The execution project never interviews you, approves anything or edits the RB. It treats the RB as the scope:
  contrary findings are reported, not used to change the question. A change of questions, corpus, mandatory cases or
  exclusions needs a new RB from the generation project.

The RB is the only thing passed between them. That makes the agreement inspectable: anyone holding the RB can see
what the research was meant to answer, without the conversation that produced it. It also makes the research
portable: the RB can be run in another app or by another model.

Inside the execution project, one assistant does everything in one continuous conversation: research, writing,
rendering, checking and delivery. It does not hand work to other agents or models. This keeps one working record of
what was read and why, and avoids losing evidence at handoffs between stages.

# 2. Asking about the reader first

A report is written for someone and for a use. The same evidence on screen time serves a parent setting family rules
differently from a researcher checking a meta-analysis. Before 1.7b.10 the brief asked about the reader in passing,
next to the format, and the model usually fell back to a generic reader.

## 2.1 A dedicated first turn

On a new topic, the first reply is a short message of questions and nothing else: no brief, no scope, no findings.
It asks only about points that are still unknown **and** would change the report:

1. the reader's starting point: what they already know of the subject and its vocabulary;
2. the use: what the report should let them do (decide, understand, explain to others, check or cite a claim);
3. the readers: the person asking alone, or others, and who they are;
4. the situation, only where it changes which evidence applies (a country, an age group, a setting).

Models can recognise that a request is ambiguous and still answer it directly instead of asking; clarifying an
ambiguous information need is a known weak point of language models. [[1]](#ref-1) [[2]](#ref-2) A question that is
optional inside a longer reply is easy to skip, so the engine makes the questions the whole first turn and requires
the model to stop after them.

The turn is skipped when the request already answers every point that matters, when you waive it, when you continue
an earlier topic in the same conversation, or when you revise an existing brief or RB.

## 2.2 Few, open questions, each with a default

Every question costs the reader attention. In a randomised study of AI-assisted interviews, follow-up probing
produced more specific answers, but about doubled the length of the conversation and shifted the respondents'
experience slightly for the worse. [[3]](#ref-3) The engine therefore asks at most four questions, only those whose
answer would change the report, in plain words. The number four is a design choice: the evidence shows that questions
have a cost, not where the optimum lies.

Each question states the assumption the model will use if it stays unanswered, and one word, “skip”, accepts them
all. You can answer some, all or none. The assumptions reach the RB as assumptions, so a later reader can tell what you
said from what was assumed.

The questions are open. Offered answers shape answers: the range and the order of response options change what
people report. [[4]](#ref-4) [[5]](#ref-5) A list such as “decide / understand / cite” would steer the reader toward
the listed uses, so the protocol forbids presenting the uses, or any other list, as options to pick from.

## 2.3 Answers are not approval

A reply to the reader questions leads to a brief, never to an RB, even if it says “approved”: you have not seen a
brief yet. The brief then shows the reader lines in plain words, marks assumed values, and says that they will be
recorded in the RB.

# 3. Reader context is not scope

The situation answer needs care, because it can do two different things.

Most often it only changes which evidence is most applicable. A parent of a six-year-old in France asking about screen
time still benefits from evidence on other ages and countries; the report should say where evidence for that age is
thin and what French guidance says. The engine records this as **reader context** in RB section 8. The execution
project uses it to decide which evidence is discussed as most applicable and where limits matter; it does not narrow
the search or remove evidence.

Sometimes the situation should restrict the research: “only studies from France”, “only children under ten”. That is a
scope decision. The engine shows it as a proposed boundary in the brief, and it becomes scope only when you approve it.

The recorded cases show why the distinction is written down. In three runs, a situation answer drifted into the scope
(an age band of 5 to 7, the exclusion of under-25s) instead of staying reader context. The protocol says it should
not; the cases show that models still do it, so the brief is the place to catch it before approval.

Personal details are recorded only as far as they change the report, impersonally and without names (“a parent of a
child of about six”). The RB is a file you may share, and the report should be readable by anyone.

# 4. Truthful approval, preserved versions

## 4.1 Approval covers what you saw

Each proposed brief has an identifier (`BR-001`, then `BR-002` for a revision). Approval refers to one brief, and the
RB records which one was approved and on what basis. The RB may add headings, identifiers and faithful operational
detail; it may not add a research question, a mandatory comparison, an evidence restriction or a deliverable that you
did not see.

A reply that changes the scope is applied directly only when it is unambiguous and can be written into the RB word
for word. Anything that would need interpretation is shown again as a new brief, and needs one more confirmation.

If you waive approval (“skip the brief”), the RB is issued with the status `assumptions-not-explicitly-approved`. A
waiver allows the work to proceed; it never becomes a recorded approval.

## 4.2 Issued files do not change

An issued RB is kept byte for byte. A scope revision is a new RB file with its own version and a pointer to the one
it supersedes. A corrected report is a new report version (`topic.v1.1.md` with matching reading copies). Scope
versions and report versions are counted separately, because a corrected figure in a report does not change what the
research was meant to answer.

# 5. Research the questions, keep the evidence

## 5.1 Investigate the questions, not the document

The execution project works from the RB's questions. Each one closes with a supported answer, an investigated
inconclusive result, or a disclosed evidence gap, after consequential counter-evidence has been considered. A failed
retrieval is recorded as an access limit, never as proof that evidence does not exist. Normal closure also needs a
reason why further searching within the scope would not add materially useful evidence; research stopped by a limit
is labelled incomplete, with the unfinished questions named.

Evidence that drives a conclusion is appraised in context: what was tested, on whom or on what system, against what
comparison, with what outcome, magnitude and uncertainty, and how far it applies to the reader's setting. A citation
being present is not the same as the cited source supporting the claim; the two are checked separately. [[6]](#ref-6)

## 5.2 Adapt the explanation, not the evidence

Writing for a reader invites simplification, and simplification can quietly drop the estimate, the denominator or the
qualification that carries an answer. The execution protocol keeps one working record of decisive estimates,
assumptions, conflicts and inspected source locations, and writes the report from it. Adapting to the reader changes
how much is explained, in what order and with what vocabulary; it does not change which consequential evidence
survives. The **purpose** decides what the reader meets first (a decision, an explanation for others, a claim to check
and cite); the **reader context** decides which evidence is discussed as most applicable.

## 5.3 Reconcile once, then deliver

Before delivery, the claims that drive conclusions are rechecked against the inspected source locations, the
questions are checked for coverage, and the delivered files are checked against each other. The reporting borrows
items from scoping-review guidance (objectives, eligibility, sources, search, limitations) without claiming
compliance with it. [[7]](#ref-7)

# 6. What you receive

| File | What it is |
|---|---|
| `topic.html` or `topic.pdf` | The reading copy: self-contained HTML by default, PDF when the RB asks for one. Numbered citations link to an anchored bibliography with inspectable source locations. |
| `topic.md` | The same content in Markdown, labelled as source for tools, not as the reading copy. |
| `topic.rb.md` | The unmodified RB the research followed. |
| `topic-research-package.zip` | All public files with their figures, when the report has any. |

The body length is measured in a fixed A4 reference layout (11-point text, 25 mm margins). When that render is not
possible in the app, the delivery says “Substantive body page count: unverified” instead of claiming compliance.

Every delivery states two separate outcomes: whether the **research** is complete or constrained-incomplete, and
whether the **delivery** is complete or partial (a missing format, an exceeded limit, a substitute reading copy). It
also lists which checks were performed and which were not.

# 7. Apps differ

The same instructions meet different hosts. Before relying on web access, file creation, code, PDF production or
visual inspection, each project checks what the app actually provides and names a fallback for what it lacks: an HTML
reading copy when PDF fails, inline substitutes when files cannot be created, an explicit “not performed” for checks
the app cannot do. The execution project rechecks its own app; capabilities do not carry over from the generation
project.

The recorded cases add what the protocol cannot control:

- On lighter settings (ChatGPT Medium and Instant, Claude Haiku at Low) a simple-looking question was answered
  directly, without the engine.
- Claude Fable 5.1 at Max judged the project instructions a prompt injection, because the app delivered them inside a
  tool result.
- Mistral Vibe turns questions into multiple-choice popups, which works against open questions: type your own answer
  in the free field. Vibe cannot render PDFs, so ask for HTML reading copies.

# 8. Limitations

Project instructions are a request to the model; the app and the model decide whether to follow them. In the recorded
cases, five of fifteen runs answered directly instead.

The checks are done by the same assistant that did the research, and are reported as performed or not performed. They
are not independent verification of the findings.

The October 2026 benchmark measured engine 1.6. Version 1.7b.10 has not been benchmarked: its reader questions and
its execution project are shown by the recorded cases, not measured. The sources cited here are background for the
design choices, not experiments validating this engine.

# Glossary

| Term | Meaning in this guide |
|---|---|
| Brief | The proposal shown for approval before an RB exists, identified as `BR-001`, `BR-002`, and so on. |
| Evidence gap | Adequate support was not found in the stated search; not proof that support does not exist. |
| Purpose/use | What the reader will do with the report; it decides what the report leads with. |
| Reader context | The reader's situation where it makes some evidence more applicable; it shapes emphasis, not scope. |
| Reading copy | The HTML or PDF meant to be read; the Markdown is source for tools. |
| Reference layout | The fixed A4 rendering used to measure the body length. |
| Research Boundaries (RB) | The standalone file defining the agreed research and its deliverable. |
| Waiver | Your instruction to proceed without approving a brief; the RB then records assumptions, not approval. |

# Bibliography

### [1] CLAMBER {#ref-1}

Tong Zhang, Peixin Qin, Yang Deng, Chen Huang, Wenqiang Lei, Junhong Liu, Dingnan Jin, Hongru Liang, and Tat-Seng
Chua. 2024. *CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language
Models*. ACL 2024, pp. 10746–10766. Used for its general finding that clarifying ambiguous information needs is a weak
point of language models.

<https://aclanthology.org/2024.acl-long.578/> · DOI: <https://doi.org/10.18653/v1/2024.acl-long.578>

### [2] Knowing but Not Showing {#ref-2}

Jinyan Su and Claire Cardie. 2026. *Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying
Questions*. Preprint, arXiv:2605.25284v1, §§3–4. Used for the gap between recognising ambiguity and asking about it;
its answering condition instructed direct answers, so it does not show an intrinsic inability to ask.

<https://arxiv.org/abs/2605.25284v1>

### [3] AI-Assisted Conversational Interviewing {#ref-3}

S. Barari, J. Angbazo, N. Wang, L. M. Christian, E. Dean, Z. Slowinski, and B. Sepulvado. 2026. *AI-Assisted
Conversational Interviewing: Effects on Data Quality and Respondent Experience*. Survey Research Methods 20(2),
161–180. Used for the trade-off between more specific answers and longer, slightly less pleasant conversations; its
cap of one probe per question is a tested condition, not an optimum.

<https://doi.org/10.18148/srm/2026.v20i2.8624>

### [4] The Range of Response Alternatives {#ref-4}

Norbert Schwarz, Fritz Strack, Gesine Müller, and Brigitte Chassein. 1988. *The Range of Response Alternatives May
Determine the Meaning of the Question: Further Evidence on Informative Functions of Response Alternatives*. Social
Cognition 6(2), 107–117. Used for the finding that offered response ranges change what people consider.

<https://doi.org/10.1521/soco.1988.6.2.107>

### [5] Response-Order Effects {#ref-5}

Jon A. Krosnick and Duane F. Alwin. 1987. *An Evaluation of a Cognitive Theory of Response-Order Effects in Survey
Measurement*. Public Opinion Quarterly 51(2), 201–219. Used for primacy effects of offered answer lists.

<https://doi.org/10.1086/269029>

### [6] Enabling Large Language Models to Generate Text with Citations {#ref-6}

Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. *Enabling Large Language Models to Generate Text with
Citations*. EMNLP 2023, pp. 6465–6488. Used for the distinction between a correct answer and a citation that supports
it.

<https://aclanthology.org/2023.emnlp-main.398/> · DOI: <https://doi.org/10.18653/v1/2023.emnlp-main.398>

### [7] PRISMA-ScR checklist {#ref-7}

PRISMA. *Preferred Reporting Items for Systematic reviews and Meta-Analyses extension for Scoping Reviews: Checklist*.
2019. Used as reporting guidance, not as evidence that this workflow meets the full standard.

<https://www.prisma-statement.org/scoping>
