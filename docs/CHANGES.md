# Implementation changes

3 November 2026 · Research Project Starter, editorial-refined replacement

This implementation repairs the five-page site's explanation of a complete investigation while retaining its visual identity, static delivery, public paths and original evidence. It reconciles both supplied audits against the actual implementation and the pinned v1.6 specification. The repository was not modified, committed to or deployed.

## Editorial decisions: before and after

**Overview.** Previously, the worked scope example led into reuse before explaining the investigation; artifact badges depended on modes introduced later. The sequence now runs from concern and proposed brief to issued RB, execution choice, qualified answer, analytical record, and then comparison of saved scopes. Repeated benefit trios were consolidated to make room. Manual or supplied-file comparison is explicit before the preserved overlap diagram, and Case C appears after that concept. Existing fragments remain meaningful destinations.

**Engine.** The page now explains what each execution route receives before describing its outputs. Approval alone issues the RB and stops before substantive research; an accompanying execution request authorizes the full protocol after issuance. The full protocol prescribes evidence appraisal, question coverage, qualified reporting, a companion and checks; these are requirements, not guaranteed behavior. Coverage concerns work performed, while an answer describes what that evidence supports. Inconclusive investigated evidence is different from unfinished or blocked work. Scope revisions and corrections to findings have different records. The companion retains evidence relationships and known corrections, but cannot independently establish correctness or latestness or update old copies. The original report, scope and sources remain necessary.

**Demonstrations.** Cases A and B now connect a practical need and consequential scope decision to an attributed finding, material limitation and original report. Each unchanged preview sits beside its corresponding run; the detached gallery was consolidated while retaining `#published-artifacts`. Case A keeps the user's pushback and revised brief. Case B preserves its contrasting technical purpose. Case C identifies a guided comparison of selected RBs introduced in two stages, with no new RB. Scope conversations are distinguished from its research subject, AI interviewers.

**Evidence and starting work.** The Overview completes the historical rationale: RB-first research improved judged reports, whereas adding the protocol did not consistently improve them further. Date, judge, topic scope and the unvalidated companion remain close to this claim. Setup identifies pasted instructions and two uploaded files, links to the actual installation section, then leads from the first question to execution options. Benchmark and Engineering retain their existing arguments, methodological qualifications and portfolio depth.

## Audit disposition

All 21 Claude findings and eight GPT findings are covered below. Verification references identify the corresponding sections of [VALIDATION.md](VALIDATION.md): **C** = Content and source checks; **P** = Preservation; **B** = Browser checks; **L** = Limits. Browser outcomes belong to that record; a source correction below is not itself a claim of a rendered test pass.

| Finding(s) | Observed status | Correction, rejection or deferral | Verification |
|---|---|---|---|
| Claude F-01, F-02, F-08; GPT F01 | Confirmed prerequisite and repetition problems | Explain one investigation and both routes before artifact labels and later reuse; consolidate repeated benefits. Reject deleting useful manual reuse. | C: Overview sequence; `index.html#execution`, `#connected` |
| Claude F-04; GPT F02 | Confirmed underexplained Stage 2; supplied A/B executions lack a full-engine JSON example | Explain qualified answers, evidence roles, limits and corrections. Explicitly reject companion-without-report claims and conflation of coverage with answer states. State demonstration coverage without inventing an execution. | C: protocol and Engine; L |
| Claude F-07, F-11; GPT F03 | Confirmed ambiguous agency and missing on-page research payoff | Attribute two report findings and limits; integrate four original previews; retain evidence access and gallery fragment. Describe supplied-file Case C and use “scope conversation.” | C: report provenance below; P; B: demonstrations |
| Claude F-05; GPT F04 | Confirmed incomplete benchmark implication | Add qualitative C/B conclusion beside the existing 11/12 B/A finding and connect it to the v1.6 default; retain nearby limitations. | C: published comparisons; `index.html#evidence` |
| Claude F-03, F-06, F-13; GPT F05 | Confirmed wrong setup destination, incomplete approval explanation and version ambiguity | Use pinned README installation anchor and files; separate latest release and older guide. Explain intent-based approval/execution examples. Reject “before anything is searched”: limited capability/terminology checks may precede approval. | C: pinned specification, installation and release checks |
| Claude F-12 | Confirmed names and roles needed before counts | Explain three active file roles, first/second brief IDs and “grading rules v4.1.” Clarify Case A's main question plus three secondary questions. | C: setup, original RBs, grading rules |
| Claude F-09, F-18; GPT F07 | Confirmed large heading scales, spacing and shifting Engineering left edges | Reduce heading growth and section gaps; align outer containers while retaining readable prose width. Reject blanket background alternation and arbitrary link quotas. | B: hierarchy and alignment; shared CSS |
| GPT F06 | Reported 320px failures require their own checks; a 360px pass cannot rebut them | Add safe heading wrapping and narrow sizing without body-level clipping; retain long headings for final rendering checks. | B: 320px Demos and Engineering captures |
| Claude F-19 | Confirmed captions/guidance inside scrolling region and viewport-based hint assumptions | Keep short semantic captions inside tables; place extended guidance outside. Reject moving captions outside tables and breakpoint-only cues; detect actual overflow. | B: both table regions; markup/JS |
| Claude F-21; GPT F08 | Confirmed unreadable unenhanced stages and inert controls | Start with every stage and ranking row readable; hide controls until handlers initialize. Add keyboard tab behavior, fragment selection, announcements and initialization recovery. | P: initial HTML; B: enabled/blocked scripts and interactions |
| Claude F-10 | Optional numerical expansion, not a missing core explanation | Defer additional B/A effect-size figures. Preserve existing raw evidence access, all displayed values and the coherent Benchmark argument. | C: numerical comparison; P |
| Claude F-14 | Confirmed mixed pinning, absolute archive link and CSS override accumulation | Pin historical repository links; use packaged relative archive route; consolidate shared CSS rules. | P: local references; C: historical-link review |
| Claude F-15 | Historical accessibility limitations acknowledged | Reject changing frozen archive bytes. Disclose limitations and retain current accessible presentations of C/B and arm-B results. | P: archive hashes; B/L: archive limits |
| Claude F-16, F-17 | Confirmed missing portfolio anchors and ambiguous ledger metric | Add six Engineering section IDs. Label 3,799 as research-job ledger entries including preparation, retries and failures; preserve authorship and third-party attribution. | P: IDs; C: ledger and portfolio wording |
| Claude F-20 | Illustration could be mistaken for literal schema | Label it conceptual rather than expanding it into a schema lesson. Ground the separate Engine identity excerpt in the [original Case A RB](samples/a/chatgpt/chatgpt-project-memory-reliability.rb.md). | C: illustration and original RB comparison |

## Provenance of the new report findings

Both complete ChatGPT reports and their approved RBs were read before selecting faithful paraphrases. These are findings of specific GPT-6 High demonstration runs, not newly established science or evidence of agreement with Claude.

| Placement | Exact original provenance | Finding and qualification retained |
|---|---|---|
| Case A result; Overview teaser | [Case A ChatGPT report](samples/a/chatgpt/chatgpt-project-memory-reliability.md), §4 “The distinction that prevents false diagnoses,” read with §3, §5 and “Limits of this review”; original RB §§1 and 5 | A wrong answer alone cannot distinguish unavailable information, information available but not retrieved, and information retrieved but misapplied. Focused public-source review; no personal-chat inspection or live Projects experiment. |
| Case B result; Overview teaser | [Case B ChatGPT report](samples/b/chatgpt/llm-context-memory-reliability.md), §7 Q2 and §8 “Limits of this review,” read with §§3.1–3.3; original RB §3 Q2 | Evidence about distributing requirements and reusing earlier answers differs from an isolated effect of turn count with tokens and meaning fixed. Targeted review with mixed source-access depth; no new experiment or independent replication. |

The separate Case B narrative appendix retains its original Markdown/PDF identity. Its RB §§6 and 8 mention an analysis companion but do not establish that the exact returned format was mandatory. It is not presented as `.analysis.json`.

## Version and preservation basis

Historical claims use commit **`f74aa2d31c910cd960a190d202b4888b158baf48`** of `danielslobozian/research-project-starter`. Fresh complete reads covered the [instructions][instructions], [protocol][protocol] (including all Stage 2, companion and correction rules), [RB template][template] and [guide][guide]. These were specifications for this edit, not an activated workflow. The guide's 20 October pre-benchmark evaluation statement is dated accordingly. The [README installation anchor][install] was verified; v1.6's tag maps to this commit. The separately labeled latest-release route resolved to v1.6 when checked on 3 November 2026.

Pinned [edition records][edition] verified 11/12 B/A models and the 3/7/3 C/B distribution across 13 configurations. All 15 ranking rows and 13 effect rows match the original and published records, including the reversed Sol-high contrast, intervals, denominators, prices and times. No benchmark was rerun.

All 34 original package paths remain. Hash comparisons preserve 24 protected files, including every sample, preview, reading alternative, frozen archive and dedicated stylesheet. All 52 original IDs, ten public conversation URLs and 14 distinct research-download/reading paths remain. Detailed source checks, actual browser results and remaining limits are in VALIDATION. No participant study, scientific replication or full-engine companion validation is claimed.

[instructions]: https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-project-instructions.txt
[protocol]: https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-protocol.md
[template]: https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-boundaries-template.md
[guide]: https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-project-guide.md
[install]: https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/README.md#install
[edition]: https://github.com/danielslobozian/research-project-starter/tree/f74aa2d31c910cd960a190d202b4888b158baf48/benchmarks/2026-10-engine-1.6
