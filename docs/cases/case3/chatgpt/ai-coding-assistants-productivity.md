<!-- Source for tools (not the reading copy). The reading copy is ai-coding-assistants-productivity.html. -->

# AI coding assistants: measured and perceived productivity in experienced developers

English · Finalized 9 November 2026

<a id="summary"></a>
## Manager-facing summary

**“AI makes developers 55% faster” is not an established result for experienced developers maintaining large existing codebases.** A plausible origin is GitHub’s 2022 experiment: professional programmers completed a small HTTP-server assignment in substantially less time with Copilot. The underlying estimate is a **55.8% reduction in completion time among successful finishers**, not a 55.8% increase in work rate or an estimate of production-maintenance throughput. The original source of the quoted claim remains unknown. [[1]](#ref-1) [[2]](#ref-2)

The closest-fit randomized study found the opposite direction: experienced contributors working in familiar, mature repositories took longer with early-2025 AI tools, despite believing that AI saved time. This is evidence for that setting—not a timeless verdict on assistants. [[4]](#ref-4) Positive enterprise experiments also exist, but measure different tasks or output counts. [[5]](#ref-5) [[6]](#ref-6)

Later evidence does not justify simply carrying the slowdown forward to November 2026. METR’s follow-up has estimates favoring speedup, but selection, noncompletion and time-accounting problems prevent a reliable current-effect estimate. [[7]](#ref-7)

**The defensible management conclusion is conditional:** useful gains are possible, perceived gains are not sufficient evidence, and code-production gains should not be equated with quality-adjusted delivery. Neither a universal speed advantage nor a universal productivity illusion is supported. Evaluate comparable completed work, total human effort and downstream quality together.

<nav aria-label="Report contents">
<p><strong>In this report:</strong> <a href="#scope">Scope and method</a> · <a href="#q1">Q1: the 55% claim</a> · <a href="#q0">Q0: overall evidence</a> · <a href="#q2">Q2: costs, quality and perception</a> · <a href="#q3">Q3: differences and explanations</a> · <a href="#implications">Management wording</a> · <a href="#limitations">Limits</a> · <a href="#references">References</a></p>
</nav>

<!-- RESEARCH_BODY_START -->

<a id="scope"></a>
## Scope and review method

The target is experienced professional developers maintaining, debugging, testing and extending **large existing codebases**. Backend development supplies the relevance lens, not a language restriction. General development experience, familiarity with a repository and familiarity with an assistant are separate characteristics. No numerical threshold for “experienced” or “large” is imposed; the study settings below make the distinctions visible. Small-project evidence is included only to trace the headline claim or test its transferability. Product rankings, purchasing recommendations and employment forecasts are outside scope.

This is a **structured narrative evidence review**, searched on **9 November 2026**, not an exhaustive systematic review. Searches covered the quoted claim and its author/vendor origins, randomized developer-productivity experiments, workplace evaluations, perceived versus measured gains, review and maintenance burden, and 2026 updates. Author sites, original publications, public manuscripts and citation trails were followed. Recent-date searches and targeted correction searches supplemented foundational studies. Later repetitions of the same experiment were not counted as replications.

Assessment emphasized assignment and selection, missing outcomes, the actual comparison, outcome units, uncertainty, tool/workflow dates, quality coverage, sponsorship and relevance. Quantitative findings were checked in the available original text and tables; selected PDF tables and figures were also viewed. No raw-data reanalysis, formal certainty grading or independent validation was performed. Evidence confidence below is a reasoned assessment of these designs, not a numerical probability.

The review stopped after the mandatory claim, the closest-fit trial, positive professional-work counterevidence, later updates and quality/perception evidence had been examined. Further searches returned known studies or less-direct material rather than a new comparable randomized estimate resolving the remaining gaps. This supports narrative-review closure, not a claim that every relevant study was found. Access and version limitations are specified in the references and limitations section.

<a id="q1"></a>
## Q1 — What does “55% faster” actually mean?

**Question.** What does the evidence underlying “55% faster” actually measure, including the distinction between reduced completion time and increased work rate, and what generalisation does its design support?

<a id="f1"></a>
### F1. A genuine task-level result became an overbroad shorthand

**Answer: the statistic describes a particular task-completion comparison, not a general experienced-developer productivity gain.** Confidence is high in the provenance and arithmetic; transfer to mature-codebase maintenance is unsupported by that experiment alone.

Two plausible direct origins are identifiable. GitHub’s 7 September 2022 research post used the rounded wording “55% faster.” Peng and colleagues’ February 2023 paper used “55.8% faster” in its abstract and specified a reduction in completion time in its results. They report **the same experiment**, not two corroborating trials. Neither establishes which source originally conveyed the claim being checked. [[1]](#ref-1) [[2]](#ref-2)

The experiment randomized 95 recruited professional programmers: 45 to Copilot access and 50 to control. Thirty-five in each group completed the task and exit survey. The assignment was a JavaScript HTTP server, starting from a skeleton, with 12 visible tests. Timing ran from repository creation to the first pushed commit passing all tests. The described participants averaged six years of coding experience. This is therefore not accurately dismissed as a “novice study”; the major transfer problem is the small, standardized new-project task. [[2]](#ref-2 "Experimental design and Results, pp. 3–7")

Among finishers, means were **71.17 minutes with Copilot and 160.89 without it**. The reported reduction was 55.8%, with a 95% confidence interval of 21%–89% and p = 0.0017. Completion itself was not significantly improved. [[2]](#ref-2 "Results, pp. 5–6") GitHub’s corresponding account reports approximately 78% versus 70% completion and 71 versus 161 minutes. [[1]](#ref-1 "Controlled experiment results")

### Time reduction is not work-rate increase

The following are original arithmetic using the published mean times—not additional empirical outcomes:

**Time reduction** = (160.89 − 71.17) / 160.89 = **55.76%**.

**Inverse-time rate increase** = (160.89 / 71.17) − 1 = **126.06%**.

Thus, repeating identical successful tasks under unchanged conditions would imply about **2.26 times the rate**, not 1.558 times. That hypothetical conversion is not a measurement of sustained output, business value or throughput across heterogeneous tasks. Conversely, a literal **55% increase in rate** implies 1 − 1/1.55 = **35.48% less time**. The denominator changes the meaning.

For discussion, “55.8% less completion time on the experimental task” is less ambiguous than “55.8% faster.” Keeping the published confidence interval beside the estimate also prevents the point estimate being mistaken for a precisely known constant.

### What the design does—and does not—identify

Random assignment strengthens causal interpretation of access **within the experiment**. However, conditioning the timing comparison on successful completion is consequential: success occurs after assignment. If access changes who finishes, the successful participants in the two groups need not remain comparable, even when the original groups were randomized. The nonsignificant completion difference does not prove identical selection. This is a methodological limitation, not evidence that the large timing difference must be spurious.

Passing supplied tests is also narrower than production readiness. The study did not establish a reduction of the same magnitude for understanding historical design decisions, coordinating changes across services, reviewer labor, deployment, incident repair or future maintenance. Those are missing endpoints, not costs that can legitimately be assumed to be zero. The target population overlaps in professional experience; the target workflow does not. [[1]](#ref-1) [[2]](#ref-2)

<a id="q0"></a>
## Q0 — What is supported for experienced developers on existing codebases?

**Question.** For experienced developers working on large existing codebases, how do AI coding assistants affect end-to-end task completion time and software quality, compared with working without them, and how do measured effects compare with perceived gains?

**Answer: there is no defensible single percentage for this population and setting.** The closest-fit randomized evidence demonstrates a slowdown in one early-2025 workflow; other professional experiments demonstrate or suggest gains on different endpoints. Evidence remains insufficient for a general current estimate of fully loaded completion time with equivalent long-term quality. This is an investigated limitation, not a finding of zero effect. [[3]](#ref-3) [[5]](#ref-5) [[6]](#ref-6) [[7]](#ref-7)

<a id="f2"></a>
### F2. The apparent disagreement is partly about what was measured

Table 1 separates time, output and downstream maintenance. **Negative time changes mean less time; positive output changes mean more output.** These are not interchangeable percentages, and the rows should not be averaged or ranked. CI denotes a frequentist confidence interval; CrI denotes a Bayesian credible interval. Neither resolves bias outside its model.

<p class="table-caption" id="table-1"><strong>Table 1.</strong> Study comparison: design, measured result and relevance to experienced developers maintaining large codebases.</p>

| Study and setting | Measured result and uncertainty | Applicability and key boundary |
|---|---|---|
| **Peng et al.; 2022 experiment.** Randomized access; professional programmers; small new HTTP server. [[1]](#ref-1) [[2]](#ref-2) | Successful finishers took 55.8% less time; 95% CI 21%–89% less. | Claim provenance, not a maintenance-workflow estimate. Completion and time require separate denominators. |
| **METR; February–June 2025.** 16 established contributors, 246 real issues in familiar repositories; issue-level randomization. Primarily Cursor Pro with Claude 3.5/3.7 Sonnet. [[3]](#ref-3) [[4]](#ref-4) | Active author implementation time **+19%**; 95% CI **+2% to +39%**. | Closest fit: repositories averaged about 1.1 million lines; contributors averaged five years in them. Small, selected developer sample; not lifecycle labor. |
| **Google; summer 2024.** 96 employees randomized; internal AI completion, smart paste and code generation; standardized, unfamiliar logging task. [[5]](#ref-5) | Best adjusted estimate **−21.3% time**, transformed 95% CI **−40.0% to +3.0%**; p = 0.086. | Enterprise infrastructure, but a 10-file, 474-line starting change—not years of familiarity with the task code. |
| **Cui et al.; 2022–2023 experiments.** Three companies; 4,867 analyzed developers; randomized access/rollout of autocomplete Copilot. [[6]](#ref-6) | Weekly completed pull requests **+26.08%**, SE 10.3 percentage points. Approximate 95% interval **+5.9% to +46.3%**. | Ordinary professional work, but an adoption/complier estimate of output, not per-task elapsed time or a senior-maintainer-only result. |
| **METR follow-up, begun August 2025; reported February 2026.** Ten returning and 47 new developers. [[7]](#ref-7) | Returning: time **−18%**, CI **−38% to +9%**. New: **−4%**, CI **−15% to +9%**. | Estimates include no change; author-identified selection, noncompletion and time-accounting problems limit interpretation. |
| **Borg et al.; 2024–2025 experiment, published 2026.** 151 completions across two phases; approximately 2,500-line Java application. [[8]](#ref-8) | Maintaining code previously co-written with AI by a **habitual AI user**: posterior mean **−12.59% time**, 95% CrI **−45.77% to +32.68%**. | Randomized downstream artifact assignment, not randomized AI use in phase 1. Small-project transferability evidence; no equivalence established. |
| **Demirer et al.; May 2026 working paper.** Matched observational adoption studies across coding-tool generations. [[10]](#ref-10) | For synchronous agents at weeks 21–30: approximately **+109% commits versus +20% releases**. | Modern-agent evidence, but output counts, not fixed-task hours; adoption was not randomized and target experience was not isolated. |

*Calculations in Table 1:* Google’s published log-time coefficient −0.24 and CI [−0.51, +0.03] are transformed as 100 × (exp(coefficient) − 1). The Cui interval is 26.08 ± 1.96 × 10.3, an approximate normal interval calculated here, not a published interval. Demirer’s Table 5 gives 109.1% (SE 2.7) and 20.3% (SE 2.6); the narrative rounds the latter differently, so the comparison is deliberately approximate. [[5]](#ref-5 "Table III and section V.C, p. 8") [[6]](#ref-6 "June 2025 manuscript, Table 3") [[10]](#ref-10 "Table 5, printed p. 33")

### Why the closest-fit trial matters without settling the whole question

METR adjusts log implementation time for pre-assignment forecasts and checks alternative uncertainty calculations. [[3]](#ref-3 "Sections 2–3; Appendix D") Repeated tasks from a small set of contributors are not independent developer samples. The advantage of its design is the close match to familiar-repository work, not representativeness of all developers.

**Interpretation:** randomization can establish a result in a narrow population while leaving generalization uncertain. Conversely, a large workplace sample can improve precision without estimating the exact outcome needed here. Neither “only 16 developers” nor “thousands of developers” is sufficient to decide which result answers a particular management question.

Google supplies positive time-based counterevidence, but its adjusted interval includes a small slowdown. The unadjusted comparison was significant (p = 0.038), whereas the preferred adjusted treatment coefficient was not at the 5% level. That is a distinction between analyses, not a license to report only whichever significance result supports a preferred narrative. Ninety-three participants completed the task; the reported regression table lists N = 96. [[5]](#ref-5 "Section V and Table III")

The workplace estimate concerns **induced adopters**, not everyone offered access. Analytic exclusions include missing records, leavers, nondevelopers and prior adopters. An additional, layoff-disrupted trial lacked adoption data; including it with imputation gives +21.34% output (SE 9.92). [[6]](#ref-6 "Sections 4.1–4.4; Appendices A and E")

**Interpretation:** output per week can increase because tasks become faster, more tasks are attempted, work is reorganized or units become smaller. It cannot be converted into completion-time savings without additional assumptions about task mix, hours and quality. The instrumental-variable interpretation additionally depends on assignment affecting outcomes through adoption and on the relevant compliance assumptions; randomization does not make those assumptions automatic.

<a id="f3"></a>
### F3. Later tools require later evidence, not retrospective extrapolation

METR’s later experiment is important but not a clean demonstration that the early slowdown reversed. Developers increasingly declined no-AI work or withheld tasks they expected AI to help most. Pay also fell from $150 to $50 per hour. Concurrent agent work complicated timing, and completion and scope could differ between conditions. [[7]](#ref-7 "Wider adoption of AI has made it more difficult to measure task-level productivity")

The authors interpret selection as likely understating benefits. **Review inference:** that direction is plausible, but optimism about a task is not the same as an observed treatment effect. Neither the size nor a guaranteed lower bound follows from those expectations alone. The follow-up narrows what can be said about current tools; it does not erase the original randomized observation.

The modern-agent observational paper strengthens the case that code activity and shipped output can diverge. Its matched historical controls, pre-trend checks and placebo comparisons address some confounding, but do not randomize adoption. More releases are also not necessarily more value or fewer defects. Treat it as relevant contemporary output evidence, not a causal replacement for a fully loaded timing trial. [[10]](#ref-10 "Sections 5–7 and Appendix D")

<a id="q2"></a>
## Q2 — What remains after checking, review and rework?

**Question.** What effects remain when prompting, checking, testing, review, and rework are counted, with quality and task completion assessed alongside speed? How closely do developers’ expectations and retrospective impressions match those measurements?

<a id="f4"></a>
### F4. The timing boundary changes the answer

**Answer: gains can survive in some measured workflows, but there is no assessed estimate that fully charges all participants’ labor and long-term quality costs in the target setting.** METR includes more author-side work than a code-generation benchmark and still finds a slowdown. Workplace output gains coexist with incomplete cost allocation and mixed quality proxies. [[3]](#ref-3) [[6]](#ref-6)

METR counts author implementation—including prompting, checking, tests and post-review changes—not other reviewers’ labor, waiting or future maintenance. Post-review time was imputed for 27 issues; sensitivity analyses retained slowdown. [[3]](#ref-3 "Section 2.3; Appendix C.3.4; Appendix G.2") Qualitative PR assessments did not identify a material quality difference. That is not a formal non-inferiority test for defects or security. [[4]](#ref-4 "Factor Analysis")

A useful accounting distinction is between **author effort**, **total human effort**, and **elapsed delivery time**. These are definitions for interpreting the evidence, not interchangeable measured variables:

- Author effort includes the developer’s own planning, prompting, coding, checking, tests and rework.
- Total human effort adds other people’s review, coordination and attributable repair work.
- Elapsed delivery time includes waiting, parallel work and deployment dependencies, without double-counting overlapping hours as labor.

A task may improve on one and worsen on another. An agent running while its user works on something else makes this especially important: wall-clock agent duration is not automatically human effort saved or spent. A measurement design must state which clock it uses and how overlapping work is allocated.

### Quality evidence neither establishes universal harm nor certifies safety

In the workplace trials, Microsoft’s PR approval rate improved by 9.88% relative to baseline (SE 3.28), while Accenture’s build-success rate fell by 17.40% relative (SE 7.12). These are process indicators, not long-term defect or security rates. [[6]](#ref-6 "Tables 3–4") They show why a claim of unqualified quality improvement would be too strong; they also do not establish that all additional output is low quality.

In Borg’s study, downstream maintainers worked without AI; 151 of 449 sign-ups completed across both phases, with 72 downstream timing observations. Overall frequentist tests found no CodeHealth or test-coverage difference. However, the habitual-original-user model suggests a small CodeHealth gain: **+0.10 points**, 95% CrI **+0.02 to +0.19**. The timing estimate in Table 1 is prior-sensitive. [[8]](#ref-8 "Sections 3, 4.2.1 and 4.3.1; Figure 14") Neither nonsignificance nor this small model-based quality gain establishes equivalent maintainability or a net time benefit.

Xu and colleagues report a shift from original contributions toward review among core contributors after Copilot’s introduction. However, actual individual use is unobserved: treatment is proxied through initially endorsed programming languages in Microsoft-owned repositories. “Core” is based on contribution activity, not a verified professional-experience category. Review counts are not review minutes, and rework is not a direct measure of latent defects. This is suggestive evidence of redistributed burden, not decisive identification of its cause or cost. [[9]](#ref-9 "Sections 3 and 6")

**Evidence gap:** the assessed studies do not jointly provide a mature-codebase randomized estimate of completion, all contributor/reviewer effort, deployment outcomes and months of attributable defects. Consequently, a quality-adjusted net benefit cannot be calculated from them without inventing missing inputs.

<a id="f5"></a>
### F5. Perceived benefit can have the wrong sign—but does not always

In METR’s early trial, developers forecast **24% less time** before work and retrospectively estimated **20% less**, despite the measured increase. Expectations were elicited before assignment; retrospective judgments came after experience with the workflow. [[4]](#ref-4 "Core Result") This is direct evidence of miscalibration for this sample, not merely disagreement between an unrelated survey and a trial.

Peng’s exit survey points in the other direction: participants estimated about **35% productivity improvement**, below the paper’s reported task gain. The survey and paper use productivity/speed wording rather than a rigorously harmonized rate-versus-time scale, so the exact difference should not be treated as a clean calibration statistic. [[2]](#ref-2 "Exit survey and Figure 7, pp. 6–7")

A 2026 METR survey of 349 technical workers, including 87 software engineers, reports median perceived value gains of 1.4–2 times and perceived speed of 3 times. These are self-reported counterfactuals in a mixed population, not measured causal effects for experienced backend maintainers. The authors explicitly caution against interpreting them as reality-grounded estimates. [[12]](#ref-12 "Summary and discussion of self-report limitations")

**Interpretation:** satisfaction, reduced tedium, faster visible code production and faster completion are different claims. A person can accurately report a better experience while misestimating time saved. Conversely, miscalibration in one experiment does not invalidate every report of benefit. The missing counterfactual—how the same task would have gone without assistance—is precisely what randomization tries to estimate.

<a id="q3"></a>
## Q3 — Which differences and explanations are supported?

**Question.** Which differences by task, developer experience, repository familiarity, assistant familiarity, and tool version are supported by evidence? What explains conflicting results or perception–performance gaps, and what remains speculative?

**Answer: differences in tasks, measurement and workflows are established; universal moderator rules are not.** Confidence is stronger in explaining why studies are not equivalent than in identifying a single mechanism causing their effects.

<a id="f6"></a>
### F6. “Experience” has several meanings, with no universal direction of benefit

The original trial’s programming-experience interaction had p = 0.0629, so its often-repeated claim of larger benefits for less-experienced programmers was not established at the conventional 5% threshold. [[2]](#ref-2 "Table 1, p. 6") Workplace analyses suggest greater gains for junior or shorter-tenure employees, but those categories combine different tasks and organizational roles. [[6]](#ref-6 "Section 5 and heterogeneity analyses")

An important counterexample is Daniotti and colleagues’ 2026 observational study. It infers AI-generated Python code with a classifier and uses within-developer models; gains are concentrated among longer-tenure GitHub users. Platform tenure is not company seniority, and the design does not randomize AI use. Data end in 2024 despite the 2026 publication date. It does not overturn randomized findings, but undermines a simplistic “AI helps juniors, not seniors” generalization. [[11]](#ref-11 "Results and discussion, pp. 832–834")

**Review inference:** compare like definitions before treating these as contradictory treatment interactions. Professional expertise, historical repository knowledge and ability to direct/check an assistant could plausibly have different effects. Existing evidence does not identify a single numerical adjustment for each.

### Repository familiarity, task fit and assistant familiarity

METR’s exploratory mechanisms include familiarity, implicit requirements and unreliable suggestions; participants had varying assistant experience. Its analyses do not establish a learning-based explanation or isolate causal mediation. [[3]](#ref-3 "Table 1 and exploratory factor analysis")

**Mechanistic interpretation, not an additional empirical finding:** a developer who already knows a precise fix has little search or typing time to save, while explaining context and checking alternatives can still cost time. An unfamiliar but well-specified task may offer more opportunity for assistance. The studies are consistent with this account, but do not isolate familiarity from task complexity, standards or tool choice.

Similarly, acceptance of many suggestions is not itself proof of value, and rejection is not proof that every suggestion was harmful. A low acceptance rate may indicate poor fit, stringent standards or useful exploration. To identify the mechanism, one would need comparable tasks and interventions that vary context provision, checking burden or training while preserving the rest of the workflow.

### Versions and workflows cannot be pooled as one intervention

The evidence spans autocomplete, integrated code-editing features, chat/agent use and later concurrent agents. The oldest experiments cannot quantify the effect of the latest systems, and later nonrandom adoption cannot by itself identify the effect of model improvement. [[5]](#ref-5) [[6]](#ref-6) [[7]](#ref-7) [[10]](#ref-10)

Selection, training, task choice and model capability can change together. Therefore, “newer tools explain the difference” is a hypothesis with supporting context, not an isolated causal estimate. So is “developers simply need more practice.” Neither should be used to discard a contrary result without measuring the proposed explanation.

Perception gaps admit several hypotheses: salient moments of rapid generation, unremembered checking time, reduced effort being mistaken for reduced duration, or counterfactual judgments made against a different task scope. These are candidate explanations, not demonstrated universal biases. The supported result is the calibration failure where it was measured; its full psychological cause remains unresolved.

<a id="implications"></a>
## Implications and wording for a technical manager

### A source-backed formulation

> A widely quoted Copilot experiment found about 56% less completion time among developers who finished one small programming assignment. It did not establish a 55% general productivity gain for experienced maintainers. Evidence from realistic professional settings includes both gains and slowdowns, depending on the task, workflow and outcome. The closest-fit early-2025 trial found longer author work time despite perceived savings; later data do not yet supply a reliable general replacement estimate. [[1]](#ref-1) [[3]](#ref-3) [[6]](#ref-6) [[7]](#ref-7)

This is a synthesis for reuse, not a quotation from any source. Avoid replacing it with the opposite slogan, “AI only makes developers feel faster”: the professional-work counterevidence does not support that claim.

### A decision rule rather than an assumed percentage

The following is an original implication of the measurement gaps: define “done” and the quality boundary before interpreting a productivity number. For a local evaluation, the relevant comparison would preserve task eligibility and acceptance criteria, record the exact assistant/workflow, retain failed or abandoned tasks, and charge author and reviewer time separately. Report elapsed delivery time alongside labor rather than merging the two. Compare expectations recorded before assignment with outcomes afterward. These are conditions for interpreting evidence, not a recommendation to buy or reject a product.

A simple hypothetical break-even calculation illustrates the point. Suppose an assistant saves 30 author minutes but adds 15 author-checking minutes and 20 reviewer minutes. Total human effort increases by **5 minutes**, even though the author finishes **15 minutes sooner**. If the added review were only 5 minutes, total human effort would instead fall by **10 minutes**. No reviewed study supplies those particular inputs; the example demonstrates why the allocation of cost changes the conclusion.

The important unit is not generated code. It is accepted, sufficiently reliable work delivered with a stated expenditure of human effort. Extra tests, documentation or broader functionality may be valuable, but should be recorded as changed output rather than silently counted as equal work completed at a different speed.

<a id="limitations"></a>
## Limits of the evidence and this review

**Selection and generalization.** Volunteers, selected employers, publicly visible repositories and task experiments do not form a representative sample of all experienced backend developers. Randomization addresses assignment within a study, not recruitment into it. Small-project studies remain transferability evidence; observational platform studies do not verify the full target population. [[2]](#ref-2) [[3]](#ref-3) [[5]](#ref-5) [[6]](#ref-6) [[8]](#ref-8) [[11]](#ref-11)

**Access and versioning.** Cui’s published abstract was accessible, but detailed appraisal used the publicly hosted June 2025 manuscript rather than the final publisher full text. Daniotti’s publisher page was blocked; an institutional full-article copy was read, not its supplementary analyses. Some PDF screenshots failed, including the author-hosted workplace and writing-versus-shipping papers; their parsed tables and surrounding text were inspected instead. No numerical claim is based solely on a search-result snippet. Source entries identify the exact assessed versions. These boundaries limit claims about final-version details and visual verification, not the existence of the studies.

**Interests and independence.** GitHub/Microsoft affiliations are present in the original claim study and workplace research, and Google evaluated its own internal tools. Borg’s declared interests include employment by the provider of its CodeHealth measure and consultants offering AI-assisted delivery services. METR is a model-evaluation organization with an AI-risk research motivation, not an assistant vendor. These relationships warrant transparent appraisal; they do not determine whether a result is correct. [[1]](#ref-1) [[2]](#ref-2) [[4]](#ref-4) [[5]](#ref-5) [[6]](#ref-6) [[8]](#ref-8)

**Unresolved quantities.** A common quality-adjusted endpoint, complete reviewer costs, long-run maintenance effects and reliable current-agent effects remain missing for the target setting. Correction/version checks did not locate an authoritative withdrawal of the central results; this is not a guarantee that all later changes were discoverable. The February 2026 METR update changes present-day inference, not the historical experimental result. [[7]](#ref-7)

<a id="conclusion"></a>
## Conclusion

The “55% faster” claim has an identifiable empirical basis but an unjustified general form. **Q1** is resolved by separating a conditional task-time reduction from work-rate or production-productivity claims. **Q0** has a conditional answer: professional developers can benefit, while the closest-fit early-2025 trial found a slowdown; no single current effect is established. **Q2** shows that author-side checks can offset generation gains and that quality and other people’s effort remain incompletely measured. **Q3** identifies material differences among studies without pretending that experience, familiarity or newer models have one proven universal effect.

For mature backend codebases, the evidence supports neither guaranteed acceleration nor guaranteed illusion. The defensible claim is narrower: **measure the completed work and the whole relevant cost before assigning a productivity percentage.**

<!-- RESEARCH_BODY_END -->

<a id="references"></a>
## References and inspected locations

<a id="ref-1"></a>
### [1] GitHub’s original report of the 55% experiment

Eirini Kalliamvakou (7 September 2022; updated 21 May 2024). *Research: quantifying GitHub Copilot’s impact on developer productivity and happiness*. GitHub Blog. Primary vendor research communication; not an independent replication of [2]. [Original article](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/). **Inspected:** controlled-experiment description/results, completion rates, means and uncertainty; survey findings distinguished from the experiment.

<a id="ref-2"></a>
### [2] The underlying randomized task study

Sida Peng, Eirini Kalliamvakou, Peter Cihon and Mert Demirer (2023). *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot*. arXiv:2302.06590, version 1. Research preprint. [Versioned paper](https://arxiv.org/abs/2302.06590v1). **Inspected:** experimental design and results, pp. 3–7; Table 1, p. 6; Figures 6–7 and exit-survey discussion. Full text and selected PDF pages inspected.

<a id="ref-3"></a>
### [3] Randomized work in familiar, mature repositories

Joel Becker, Nate Rush, Beth Barnes and David Rein (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. arXiv:2507.09089, version 2, 25 July 2025. METR research preprint. [Versioned paper](https://arxiv.org/abs/2507.09089v2). **Inspected:** Sections 2–3; Figure 1, p. 2; Table 1, p. 11; Appendix C.3.4 on missing review time; Appendices D–G on estimation, dropout, perceptions and instructions. Version 2 governs this review; the earlier abstract/blog describes a slightly different count of explored factors.

<a id="ref-4"></a>
### [4] METR’s explanation and limits of the early-2025 trial

Joel Becker, Nate Rush, Beth Barnes and David Rein (10 July 2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. METR. Primary author communication about [3], not a separate study. [Original post](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). **Inspected:** Methodology, Core Result, Factor Analysis, limits on generalization and Discussion.

<a id="ref-5"></a>
### [5] Google’s enterprise-task experiment

Elise Paradis, Kate Grey, Quinn Madison, Daye Nam, Andrew Macvean, Vahid Meimand, Nan Zhang, Ben Ferrari-Church and Satish Chandra (2024/2025). *How Much Does AI Impact Development Speed? An Enterprise-Based Randomized Controlled Trial*. ICSE-SEIP 2025, DOI [10.1109/ICSE-SEIP66354.2025.00060](https://doi.org/10.1109/ICSE-SEIP66354.2025.00060). [Public manuscript, arXiv:2410.12944v3](https://arxiv.org/html/2410.12944v3). **Inspected:** methods, Sections IV–V, Table III and treatment-coefficient CI on p. 8; table viewed in PDF. The task/tooling is proprietary; the adjusted estimate is distinguished from the significant unadjusted test.

<a id="ref-6"></a>
### [6] Three workplace experiments

Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng and Tobias Salz (2026). *The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers*. *Management Science*, published online 27 February 2026. DOI [10.1287/mnsc.2025.00535](https://doi.org/10.1287/mnsc.2025.00535). **Access:** published abstract inspected; detailed appraisal used the [public June 2025 manuscript](https://www.mertdemirer.com/Papers/Demirer_AI_productivity.pdf), not inaccessible final full text. **Inspected:** Sections 2–5; Tables 1, 3 and 4; Appendices A, B and E. Manuscript PDF pp. 12–14 contain main output and quality tables. Parsed tables/text inspected; screenshot retrieval failed. Postregistered trial; Microsoft-affiliated authors and MIT GenAI funding disclosed.

<a id="ref-7"></a>
### [7] Later METR experiment and its selection problems

Joel Becker, Nate Rush, Tom Cunningham, David Rein and Khalid Mahamud (24 February 2026). *We are Changing our Developer Productivity Experiment Design*. METR research update. [Original post](https://metr.org/blog/2026-02-24-uplift-update/). **Inspected:** raw estimates and confidence intervals; “Wider adoption of AI has made it more difficult to measure task-level productivity”; selection, pay, scope, noncompletion and concurrent-work timing. Experiment began August 2025; not a retraction of [3].

<a id="ref-8"></a>
### [8] Downstream maintainability experiment

Markus Borg, Dave Hewett, Nadim Hagatulah, Noric Couderc, Emma Söderberg, Donald Graham, Uttam Kini and Dave Farley (9 June 2026). *Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability*. *Empirical Software Engineering* 31, article 161. DOI [10.1007/s10664-026-10889-1](https://doi.org/10.1007/s10664-026-10889-1). [Full article](https://link.springer.com/article/10.1007/s10664-026-10889-1). **Inspected:** Sections 3, 4.2.1 and 4.3.1; Figure 14’s habitual-original-user estimate, prior sensitivity and CodeHealth; Appendix A; Conflict of Interest. HTML full text inspected; PDF screenshot retrieval failed.

<a id="ref-9"></a>
### [9] Observational maintenance-burden evidence

Feiyang Xu, Poonacha K. Medappa, Murat M. Tunc, Martijn Vroegindeweij and Jan C. Fransoo (2025). *AI-assisted Programming May Decrease the Productivity of Experienced Developers by Increasing Maintenance Burden*. arXiv:2510.10165. Research preprint. [Full text](https://arxiv.org/html/2510.10165). **Inspected:** Sections 3 and 6, exposure proxy, contributor definitions and activity outcomes. Individual Copilot usage is unobserved; causal interpretation is correspondingly limited.

<a id="ref-10"></a>
### [10] Writing code versus shipping software

Mert Demirer, Leon Musolff and Liyuan Yang (27 May 2026). *Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI Coding Tools*. Working paper. [Assessed author-hosted manuscript](https://www.mertdemirer.com/Papers/Demirer_Writing_vs_shipping_code.pdf). **Inspected:** Sections 5–7, Table 5 (printed p. 33; PDF p. 34), robustness discussion and Appendix D. Parsed text/tables inspected; screenshots unavailable. Table 5 reports 20.3% for the synchronous-agent release estimate, while surrounding prose reports 20.2%; the body uses approximately 20%. Not a randomized comparison or a product ranking.

<a id="ref-11"></a>
### [11] Observational evidence on experience differences

Simone Daniotti, Johannes Wachs, Xiangnan Feng and Frank Neffke (2026). *Who is using AI to code? Global diffusion and impact of generative AI*. *Science* 391, 831–835; published online 22 January 2026. DOI [10.1126/science.adz9311](https://doi.org/10.1126/science.adz9311). [Inspected institutional full-article copy](https://real.mtak.hu/234712/1/science.adz9311.pdf). **Inspected:** main-article methods, Results and discussion, especially pp. 832–834. Publisher access blocked; supplementary analyses not inspected; PDF screenshots unavailable. Data through 2024; experience proxied by GitHub tenure.

<a id="ref-12"></a>
### [12] Perceived productivity in early 2026

Joel Becker (11 May 2026). *Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity*. METR research report. [Original post](https://metr.org/blog/2026-05-11-ai-usage-survey/). **Inspected:** sample description, summary statistics and limitations of counterfactual self-reports. Survey fieldwork February–April 2026; mixed technical-worker population, not a causal developer-timing experiment.

Research ID: ai-coding-assistants-productivity-2026-11 · Report 1.0 · Scope: ai-coding-assistants-productivity.rb.md · Protocol 1.7b.10
