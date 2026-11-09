---
title: "Research Analysis Companion: Search, Evidence Appraisal, and Causal Attribution"
subtitle: "Companion to Effective Context Utilization, Conversation Length, and Factual Reliability in LLM Assistants"
author: "Research ID: llm-context-memory-reliability-2026-11 | Approved brief BR-001"
date: "3 November 2026"
lang: en
---

# 1. Function, protocol, and scope

This document is the **evidence and methods companion** to `llm-context-memory-reliability.md` and its PDF rendering. It records how the structured narrative review was assembled, what was actually inspected, which comparisons warrant causal interpretations, and which numerical claims require qualifications. The research protocol is the user-approved brief, `llm-context-memory-reliability.rb.md`, approved 3 November 2026, research ID `llm-context-memory-reliability-2026-11`, version 1.6. All findings were selected to address Q0–Q5 of that brief; no named product, case study, publication, or model was a mandated comparison. **Cutoff: material publicly available by 3 November 2026**. The intended audience understands model evaluations, estimands, and experimental controls.

This was a **structured narrative evidence review**, not a PRISMA systematic review, census, preregistered evidence synthesis, fresh benchmark, or meta-analysis. It generated no new LLM model responses, performed no user-level memory-store audit, and did not independently reproduce experimental model scores. Percentages are attributed to original researchers and vendor documentation, and study authors' causal interpretations are treated as hypotheses unless their controls isolate a corresponding manipulation.

# 2. Discovery and document inspection audit

## 2.1 Search approach actually followed

Searches were conducted in the publicly indexed web, with targeted queries combining known benchmark names and open-ended concept terms. Representative **actual search strings** included:

- `Lost in the Middle How Language Models Use Long Contexts Liu 2024 experiments answer accuracy position primary paper`
- `RULER What's the Real Context Size of Your Long-Context Language Models 2024 paper results`
- `NoLiMa Long-Context Evaluation Beyond Literal Matching 2025 findings primary paper`
- `LLMs Get Lost in Multi-Turn Conversation 2025 study original controlled turns tokens`
- `LongMemEval Benchmarking Chat Assistants`, `LoCoMo conversational memory benchmark`
- `2026 "multi-turn" language model reliability controlled evaluation context chat turns`
- `2026 "long-term memory" LLM assistants benchmark stage retrieval write read controlled`
- `context length alone hurts language model performance even when retrieving relevant information 2025 2026 study`
- `2026 multi-turn conversational factual temporal scope accuracy oracle context`
- `2026 language models long context distractor conflicting study`
- `2026 benchmarking evidence use long-term memory QA user satisfaction`
- `ChatGPT memory saved memories reference chat history help center updated 2026 memory context retrieval`

The workflow progressed from citation discovery to original publication pages, arXiv HTML/preprints, proceedings abstracts, official model/system descriptions, and publicly available PDF full text. It included affirmative and countervailing evidence: maintained performance on RULER, nonmonotonic temporal gains with gold contexts, context-degradation despite successful retrieval probes, and deployment null findings for satisfaction. Citations were cross-checked at primary publication pages where accessible. A secondary or commentary article was not used to establish the principal quantitative results.

**Audit limitation:** the web search service does not expose a standardized complete query-by-query screening export in this execution. Accordingly, this analysis does **not** invent total search hits, screened-abstract counts, excluded-study counts, or exact retrieval recall. Source discovery is selective and English-language; published and accessible work is overrepresented. Searches and inspection took place during this execution on 3 November 2026. The cited article publication dates and conference proceedings are not independently verified by archival snapshots for each link.

## 2.2 Inclusion/exclusion logic

**Include**: (a) controlled text-context QA/readout studies where position, length, distractors, information order, or context complexity varies; (b) controlled multi-turn studies with informative same-content, oracle-history, or self-conditioned comparisons; (c) persistent-memory studies explicitly distinguishing stages or testing updating, time scope, governed use, and natural integration; (d) original methodological benchmarks relevant to score interpretation; (e) vendor documents for documented claims, version names, and system features. **Exclude** from conclusions: unsupported anecdotal mechanisms, broad overall intelligence rankings, mostly multimodal research with no text-equivalent experiment, derivative unverified numerical claims, and model-versus-product comparisons that conflate architectures.

Evidentiary hierarchy for behavioral claims: within-item controlled interventions and inspected primary papers > published primary paper with limited inspected detail > vendor-run measures (valid as claims under stated tests, not independent measurement) > external uncontrolled anecdotes. For mechanistic claims the hierarchy depends more on actual stage instrumentation/intervention than on venue, scale, or year. Benchmark samples reusing the same narrative, conversations, or user must be clustered in uncertainty analyses.

## 2.3 Access and inspection levels

The following labels state what was reviewed; **PDF inspected** denotes text plus at least one rendered page/screenshot where available, not full replication or independent data audit. **Full HTML inspected** means the public original full text was consulted; **proceedings inspected** means at least the official metadata/abstract and relevant linked information were consulted. The paper-specific limitations below are *appraisal judgments*, distinct from the authors' own language.

| Ref. | Source, design and comparison | Actual inspection depth | Role and principal appraisal limit |
|:--|:--|:--|:--|
| R1 | Liu et al. 2024; move answer passage across fixed retrieved-doc positions | Original arXiv PDF text + rendered page; TACL publication metadata | High value for position effect; 2023-era models and QA construction limit portability. Direct TACL PDF fetch was unavailable; inspected arXiv PDF. |
| R2 | Shi et al. 2023; irrelevant-context interventions | Original PMLR proceedings page/abstract | Supports distractor plausibility; not used for detailed effect-size inference. |
| R3 | RULER 2024; 13 task types, model × context length, fixed operational threshold | Original arXiv full HTML and tables | Strong task heterogeneity evidence; synthetic tasks and non-position-balanced aggregate. |
| R4 | LongBench 2024; multi-task/bilingual benchmark | Original ACL publication page/abstract | Coverage reference, not a length-only causal estimate. |
| R5 | BABILong 2024; fact chains buried in long texts | Original NeurIPS proceedings page/abstract | Task comparison and stress-test framing, not standardized factuality. |
| R6 | NoLiMa 2025; remove lexical overlap between needle and question | Original ICML/PMLR full HTML and quantitative findings | Strong semantic-vs-literal contrast, limited template/task transfer. |
| R7 | LongBench v2 2025; difficult multi-doc multiple choice, 503 questions | Original ACL proceedings/publication page | Counts and unit (words) checked; not a clean intervention in length. |
| R8 | Du et al. 2025; length change + exact retrieval probes and masking controls | Original EMNLP PDF text + rendered page | Residual answer impairment with retrieval success under tested probes; retrieval probe need not share answer-trial hidden state. |
| R9 | Kurfalı & Östling 2025; conflicting needles | Original EMNLP PDF text + rendered page | Supports conflict as relevant dimension; not an independent effect-size meta-estimate. |
| R10 | MGAL 2026; multilingual granularity and contexts | Original ICML/PMLR article/publication | Illustrates domain/language boundary, not pivotal numeric claim. |
| R11 | Laban et al. 2026; FULL / CONCAT / SHARDED across 15 models and six tasks | Original ICLR/OpenReview PDF text + rendered page | Most decisive interaction-protocol control here; sharding also delays disclosure and changes role structure. |
| R12 | MultiChallenge 2025; hard multi-turn behavior benchmark | Original ACL Findings publication/page | Difficulty under conversational conditions, not token-matched turn-causal contrast. |
| R13 | Han et al. 2025; entangled instruction histories | Original EMNLP Findings publication/page | Ecological support; no isolated pure-turn estimand in this review. |
| R14 | Atri et al. 2026; Gold, Self-Conditioned, Questions-Only answer-history regimes | Original ACL PDF text + rendered page | Direct test of error propagation and gold benefits; graph-structured temporal QAs, variable history length. |
| R15 | Maharana et al. 2024; LoCoMo long dialogue benchmark | Original ACL PDF text + rendered page | Only 10 base conversations; simulation and multimodal components restrict extrapolation. |
| R16 | Wu et al. 2025; LongMemEval memory indexing/retrieval/reading ablations | Original arXiv v2 full HTML/tables; ICLR proceedings page | Stage-specific evidence, offline constructed histories; web-interface product pilot is dated and small. Proceedings PDF direct fetch not used. |
| R17 | Hu et al. 2026; MemoryAgentBench | Original arXiv abstract/publication information | Relevant framework; no detailed numeric scores extracted. |
| R18 | Uddin et al. 2026; Memora revision/forgetting cases | Original ACL Findings publication and available article information | Currency/governance dimension; metric details less extensively inspected than R16/R19. |
| R19 | Zhou et al. 2026; TimlMemBench canonical pool vs raw session pipeline | Original EMNLP PDF text + rendered page | Clear stage/view separation but variant task denominators and manually designed policies block causal subtraction. |
| R20 | Qing et al. 2026; UTILMEM evidence integration stress tests | Original EMNLP publication/full article | Shows retrieval/use gap; benchmarked synthetic/controlled tasks, not production telemetry. |
| R21 | Sumida et al. 2026; four-month random deployment + controlled reconstruction | Original EMNLP PDF text + rendered page | High ecological relevance; only 40 users, 72 cued moments, statistical power/context dependence. |
| R22 | Min et al. 2023; FActScore atomic claims | Original EMNLP paper/publication | A measurement method; not direct evidence on longer conversations. |
| R23 | OpenAI 2025; GPT-4.1 release: one-needle, MRCR, Graphwalks | Official release and numerical benchmark descriptions | Vendor-run, test-variant differences, not independent deployed assistant measurement. |
| R24 | OpenAI 2026; ChatGPT background memory synthesis (“dreaming”) | Official dated feature/system article | Documented claimed architecture, not per-user internal write/read observability. |
| R25 | OpenAI Help Center memory article | Official dynamically changing help article | Feature definitions may not be frozen to one product build. |
| R26 | Google 2024; Gemini 1.5 single-needle long-context claims | Official release publication | Vendor-run NIAH, weak general reading-reliability proxy. |

Direct PDF access sometimes failed or timed out; accessible original arXiv HTML or preprint PDF was used when available, with such substitution marked above. No inaccessible full text was silently represented as fully inspected. Rendered-page inspection supports quotations/figures read in accessible versions, **not** a comprehensive figure-by-figure audit of every paper.

# 3. Quantitative claim and comparison ledger

The figures below are **reported** measurements, not meta-analytic estimates. A comparison is identified by task, unit, and control; values should not be reinterpreted as a cross-paper leaderboard.

| Ref. | Reported values retained in report | Controlled contrast / denominator | Interpretation constraint |
|:--|:--|:--|:--|
| R1 | 75.8%, 57.2%, 53.8%, 55.4%, 63.2% for GPT-3.5-Turbo gold positions 1/5/10/15/20; 56.1% closed-book | 20-doc QA, same information at different locations | Best-minus-worst **22.0 percentage points**, not 22% relative. Earlier model/API and source design. |
| R3 | 96.7→94.4% Gemini-1.5-Pro; 96.5→66.6% Llama-3.1-70B from 4K to 128K; threshold 85.6% | Aggregate of 13 synthetic tasks/length, model-specific | Heterogeneity; no general law of decay, no exact position isolation. |
| R6 | 11/13 models below half short-context baseline by 32K; GPT-4o 99.3→69.7% | Semantic needle vs literal overlap task | Task-dependent lexical retrieval confound minimized, but template dependence remains. |
| R8 | Reported performance declines ranging 13.9–85% | Models/tasks plus retrieval/length/masked-context controls | Author's heterogeneous decline metric; do not pool or equate with percentage points. |
| R11 | Mean 39% *relative* drop FULL→SHARDED; CONCAT 95.1% of FULL; mean 16% aptitude reduction; unreliability increased 112% | 15 models, six tasks, >200K simulated interactions, seeded prompt protocols | Relative performance and spread are different scales. Sharding changes disclosure as well as turns. |
| R12 | Top tested model 41.4% average; all frontier models below 50% | MultiChallenge's four hard categories | Selection of deliberately difficult cases; not average everyday accuracy. |
| R14 | 1,469,628 temporal chains across 2–11 turns; gold can improve through turns 4–5 | Gold vs Self-Conditioned vs Questions Only | Number is evaluated chains, not unique human conversations; accuracy conditional on query generation. |
| R15 | 10 base dialogues, mean 588 turns / 27.2 sessions / 16,618 tokens | LoCoMo created dialogues and tasks | Nested evaluation observations are not 10+ independent natural users. |
| R16 | 500 questions; S ~115K tokens, M ~1.5M; GPT-4o oracle .870 vs full-S .606; R@5 .582→.644; downstream top-5 .615→.657 | Retrieval stage and answer-reading ablations | Oracle→full-S difference .264 points or **30.3% relative** to oracle. R@5 change ≠ answer-accuracy change. |
| R16 product pilot | ChatGPT .5773, offline GPT-4o .9184, Coze GPT-4o .3299; 97 questions | 3–6 session web histories, August 2024 interfaces | Distinct systems/prompts/product architectures, small dated sample. |
| R19 | 208 samples, 1,566 sessions, 1,715 QA, 1,821 governance; canonical pool 79.6–95.7%; raw-native revoke 20.7–71.5%, supersede 18–80.6%, boundary 28–74.1%, provenance 6.2–73.4% | Different evaluation views/task subsets | Cannot take canonical-pool minus raw-native as a storage-loss percentage. |
| R20 | 1,717 diagnostic instances | Evidence use and resistance to distractors | Different success rubric from R16 and R19. |
| R21 | 40 users, 1,872 sessions, seven randomized memory conditions, four months; QA 19.7–70.1% | Deployment conditions and satisfaction comparison | No comparable satisfaction difference found, but study low power for small effects. |
| R21 cue test | 72 natural memory-cue situations; direct QA 78.8% vs spontaneous mention 7.9% | Reconstructed same model/context, different requested response | Approx **70.9 percentage-point** gap is *task-conditioned mention frequency* vs QA correctness, not ordinary factual error rate. |
| R23 | GPT-4.1 2-needle MRCR 57.2% at 128K and 46.3% at 1M; Graphwalks BFS 61.7% <128K vs 19.0% >128K | Vendor-run MRCR and reasoning tasks | Length bands and test difficulty not randomized isolations. |
| R26 | ~99% one-needle extraction up to 1M | Vendor-run simple retrieval under release tests | Does not validate multi-fact integration or assistant memory. |

**Arithmetic discipline.** R1 difference 75.8 − 53.8 = **22.0 percentage points**. R16 full-S vs oracle relative drop = (0.870 − 0.606) / 0.870 ≈ **30.3%**. R21 cue difference = 78.8 − 7.9 = **70.9 percentage points**. A statement such as “39% relative sharding loss” must not be written as “39 points”; the denominators and task aggregates differ across references. The above sourced quantities are summarized rather than independently recomputed from released raw per-item data.

# 4. Stage diagnostics and causal-attribution matrix

## 4.1 What each experiment identifies

| Condition/contrast | Observable causal effect in tested setting | What remains underidentified |
|:--|:--|:--|
| Randomize position of fixed gold passage | Effect of source ordering/slot on answer | Whether internal attention, relevance selection, or answer decoding caused it. |
| Add distractors while fixing evidence and question | Effect of that distractor construction | Total tokens, retrieval salience, and instruction competition may covary. |
| Demonstrate correct answer-bearing retrieval on separate probe | Ability to retrieve in the probe | Recognition during actual answer pass; use of retrieved fact. |
| FULL vs CONCAT vs SHARDED | Effect of task disclosure and turn structure in protocol | “Turn count alone” because role tags, interim responses, and revealed information vary. |
| Gold vs Self-Conditioned history | Effect of earlier model-generated answer content/history | Remaining context-length differences, cumulative decision error, task dependence. |
| Inject gold entry into memory store | Effect of corrected store content, with same downstream path | Retrieval-ranking may interact with the altered store. |
| Force retrieve/expose same gold entry | Effect of a specific source exposure | Retrieval vs selection distinctions unless both logs instrumented. |
| Read exact gold evidence in clean prompt | Model's clean-evidence capability | Whether interference or lack of information caused full-system miss. |
| Test update and revoke after a fact changes | Temporal/governed use of eligible evidence | Did the write, selection, or response policy fail absent stage traces? |
| Randomize memory policy in deployed users | Effect of offered memory condition on observed product/workflow outcomes | Causal mediation by retrieval and utilization; power for nuanced behavioral effects. |

A **factorial identification target** might be written **E[Y | do(T = t), L = ℓ, P = p, D = d, A = a]** with turn count *T*, token length *L*, evidence position *P*, distractor type *D*, and assistant-history mode *A*. The notation is conceptual: an actual intervention that keeps length and *semantic content* fixed while changing turn boundaries is difficult. One also must ensure prompt/system-role effects are reported as part of the treatment, not misleadingly described as a pure discrete turn count effect.

## 4.2 Four-stage failure taxonomy and required logs

For cross-session memory, use at least **storage correctness** (was current fact captured, superseded, or revoked?), **retrieval success** (did candidates include the right time- and scope-valid record?), **selection/exposure success** (was it passed to the model intact alongside conflicting information?), and **interpretation/governed use** (was it applied only when relevant and permitted?). If correct evidence was visible in a later prompt, classification moves toward in-context use or competing instructions rather than a failure to persist. If the record never existed, in-prompt inference is not the primary storage culprit. A visible contradiction without any such tracing identifies only end-to-end failure.

Instrument exact prior dialog, store snapshots and timestamps, update actions, retrieval candidates and scores, selection policy, final exposed messages (including system/tool/summaries), model identity and route, sampling configuration, generated answer, grading references, and user-permission/privacy constraints. Where commercial interfaces conceal these, report **“stage cannot be determined”** rather than reverse-engineering an unobserved explanation from a single reply.

# 5. Validity threats, negative results, and synthesis limits

**External validity.** Many context benchmarks insert fact needles or use templated questions; policy-bound memory tests use designed schema and scopes; temporal knowledge chains use structured knowledge graph facts. These can reveal reproducible failures, but natural human requests, local language, retrieval infrastructure, and 2026 production product routes differ. The field is changing rapidly; a model tested in 2024 and a late-2026 model with the same brand cannot be assumed equivalent.

**Internal validity.** Context length changes may also alter document order, distractor difficulty, prompt form, number of relevant snippets, answer position, total compute, and truncation. Turn sharding can inject assistant-generated mistakes, delay important information, require preserving more intermediate state, or elicit an early commitment. Oracle history removes errors that a real chat would have produced. “Oracle context” also changes relative evidence prominence. Memory-stage interventions may alter both retrieval and prompt layout, so even improvements need careful identification.

**Scoring and uncertainty.** Exact string match rewards format compliance; LLM judges may share model errors or favor plausible phrasing; timestamped validity is different from generic truth; recall, precision, accuracy, refusal, satisfaction, and user-perceived usefulness are different outcomes. Raw item counts overcount independent replications when many QAs stem from the same base story or user. Most papers' headline values should not be treated as confidence intervals. The narrative review did not calculate a pooled uncertainty interval or effect-size meta-analysis because the interventions and endpoints are not exchangeable.

**Counterevidence and bounded nulls.** Gemini-1.5-Pro's high RULER aggregate through 128K shows **not all** tested models show sharp degradation on **all** length stressors. ChronoScope's Gold Context can improve accuracy for the first several turns, so length/turn count are not universal monotonic penalties. MemUse's deployment found major direct-memory-QA differences **without a correspondingly clear satisfaction separation**, so recall metrics need not transfer to deployment utility. None of these negative or mixed findings establishes that long contexts or memory systems never fail.

**Commercial evidence.** Vendor documents can establish claimed feature flows and test settings, but lack independent replication and often omit prompt/system details. The August 2024 product pilot establishes a result for then-current configured products, not a November 2026 reliability ranking. Anecdotal contradictions by themselves cannot distinguish source omission from retrieval failure from mistaken generation, and a current product's internal prompt may be hidden.

**Investigated evidence gaps.** (1) Few studies isolate a semantically invariant *pure turn-boundary effect* with exact matched tokens, positions, history quality, and instructions across many authentic tasks. (2) Public commercial cross-session failure rates rarely come with simultaneous source-store, retrieval, selection, and exact prompt traces, so population-level causal shares by stage are not available in the inspected evidence. (3) Ecologically valid, large randomized comparisons of *correct unsolicited memory integration*, *restraint/scope*, and fact quality with power to detect deployment benefits are sparse. (4) Independent, current-product replications of original long-context comparisons with unchanged tasks are incomplete in this selected corpus. These are **limitations of the inspected evidence**, not universal declarations that such studies do not exist.

# 6. Conclusions and reuse instructions

Each of Q0–Q5 is answered in the report. The strongest causal claims are confined to **tested controlled interventions**: gold-evidence placement, context/distractor manipulation, sharding protocol, oracle-history substitution, or memory-read/write intervention when independently tested. The evidence does **not** justify the claims that every added turn worsens factuality, that context-window size alone predicts effective understanding, or that a later-session mistake proves an internal memory persistence failure. A more defensible diagnosis consists of a defined task and benchmark, a temporally correct reference, matched comparators, separately reported metrics, and logs that establish which evidence was present **at generation time**.

For future replication, freeze exact model version and software configuration; preregister matched items and primary endpoints; retain item- and seed-level results; report clustered intervals; and make implementation artifacts available if permitted. Interpret contradictory results through differences in model, source construction, tokenization, question difficulty, position, role structure, retrieval settings, and grading, not through a single unqualified “conversation length” hypothesis.

**Citation mapping.** [R1]–[R26] identify the full bibliographic entries and original source links in the main report's References. This companion relies on the same primary-source corpus and cutoff; it does not introduce additional uncited literature. The user-approved brief is an authorization and scope document, not an empirical source for any of the reported measurements.
