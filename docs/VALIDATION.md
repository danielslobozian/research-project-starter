# Validation record

3 November 2026 · `research-project-starter-editorial-refined.zip`

This record describes checks performed for this implementation. The two supplied audits and the input package's earlier validation were evidence to investigate, not inherited passes. No new usability score, participant study, scientific replication, benchmark execution or deployment is claimed.

**Result:** the revised package passes the source, preservation, numerical, local-reference and bounded browser checks reported below. A completed browser-to-disk download and actual 200% browser zoom remain unverified. This is an implementation verification record, not a WCAG conformance certificate or an unconditional publication-readiness claim.

## Content and source checks

### Reading and attribution

The implementation prompt, both audits, all five primary pages including hidden/disclosed content, shared CSS/JavaScript and package documentation were inspected. The method's source of truth was the complete v1.6 instructions, protocol, RB template and guide at commit **`f74aa2d31c910cd960a190d202b4888b158baf48`**. Stage 2, companion, coverage, approval, publication and correction rules were read in full context. These files were specifications for this edit; no research workflow was activated by reading them.

The two complete original ChatGPT reports and their RBs were read before selecting the A/B findings. Precise file/section provenance, attribution and limitations are recorded in [CHANGES.md](CHANGES.md). Each visible finding is attributed to its particular GPT-6 High report. Neither the wording nor the screenshots imply agreement by Claude or independent validation of those reports' scientific conclusions.

Fresh retrieval covered the pinned engine documents and historical edition records: edition README, ranking, all 12 within-model analyses plus the Sol-high effort comparison, prices and crosscheck, environment/model/pricing/cost/failure inputs, ledger, grading rules and relevant orchestration/statistics code. The GitHub web-opening tool returned an access error for some requests; ordinary HTTPS/raw/API retrieval succeeded. Those tool errors are not classified as broken source links.

The installation link was checked against the actual pinned README `#install` section. The v1.6 tag resolves to the exact commit above. The separately labeled latest-release route resolved to v1.6 on this date; its future destination may change. The optional guide's 20 October evaluation discussion is explicitly identified as predating the completed benchmark.

Primary verification sources:

- [v1.6 instructions](https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-project-instructions.txt), [protocol](https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-protocol.md), [template](https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/research-boundaries-template.md), and [installation section](https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/README.md#install).
- [Immutable October edition](https://github.com/danielslobozian/research-project-starter/tree/f74aa2d31c910cd960a190d202b4888b158baf48/benchmarks/2026-10-engine-1.6) and [grading rules v4.1](https://github.com/danielslobozian/research-project-starter/blob/f74aa2d31c910cd960a190d202b4888b158baf48/grader/report-assessment-v4.1.md).

### Repaired narrative transitions

| Before | Implemented and reviewed |
|---|---|
| The scope example moved to reuse before explaining the investigation. | The execution handoff leads directly to the research routes, qualified answer and outputs. Later scope comparison follows that explanation. |
| Artifact badges depended on modes explained elsewhere. | Routes are introduced first. The RB, report and full-engine companion have distinct roles and conditions. Repeated benefit groups were consolidated. |
| The companion sounded mainly like bookkeeping. | Evidence relationships, qualified answers, access limits and corrections are explained alongside its dependence on the report and original evidence. Coverage and answer states remain separate. |
| A/B examples required opening a report to find a result. | Each case has an attributed finding, material limitation and original-report route. All four unchanged previews sit with their corresponding runs. |
| Setup named counts before roles and linked to a general guide. | Pasted instructions and two uploaded files appear before version-matched links. The actual installation destination and first-question-to-execution handoff are present. |
| The Overview's benchmark rationale stopped at B/A. | The nearby C/B implication explains the v1.6 default, with date, judge and scope limitations close to the claim. |

These are source and rendered expert-review findings. No first-time visitor or recruiter comprehension study was conducted.

### Numerical invariance

All **15 ranking rows** and **13 C/B effect rows** were compared against the pinned records and input HTML. The complete original/final table cell matrices are identical, including model labels, efforts, ranks, intervals, prices and times. Engineering numerical tokens were also compared. No values were re-estimated.

Checked counts remain **11/12** B/A models improved, **10/12** C/A models improved, and **3 improved / 7 without a measurable difference / 3 worse** for C/B across 13 configurations. The Sol-high source reports B−C +0.92 [0.84, 1.00]; displayed C−B −0.92 [−1.00, −0.84] is its corresponding reversal. The ledger contains **3,799 research-job entries** and **1,666 grading entries**. Displayed grading cost **$1,350** matches rounding of $1,349.9855. Ledger entries are not relabeled as unique completed reports.

## Preservation

The input ZIP was inventoried and hashed before editing. Its SHA-256 is:

`2a60547ce9b2a152b4f901be91d456f765fbbdc12e843a00ef998bf89329dea6`

| Check | New result |
|---|---:|
| Original package paths retained | 34/34 |
| Protected files identical by SHA-256 | 24/24 |
| Original fragment IDs retained | 52/52 |
| Public conversation URLs retained | 10/10 |
| Distinct research-download/reading paths retained | 14/14 |
| Local reference instances resolving from primary pages at root | 133 |
| Local reference instances resolving including archive under the deployment prefix | 136 |
| Primary pages passing navigation/current-page/skip/main/metadata checks | 5/5 |

The 24 protected files comprise all 12 sample artifacts, four report previews, two text-reading alternatives, two social images, favicon, `.nojekyll`, historical HTML and its stylesheet. No protected bytes changed. Original fragments remain on their original pages; `#published-artifacts` now lands at the Case A result/report handoff and links onward to Case B. New Engineering IDs supplement existing ones.

Critical frozen hashes:

| File | Bytes | SHA-256 |
|---|---:|---|
| `benchmark-2026-10.html` | 15,101 | `a5f17674f31f9a065440421dbe9f2947ac21ee1091a85ca7cf358f6d4c624178` |
| `assets/css/style.css` | 9,569 | `5ed32f243f8539d477621a0a35081146e1bc9bfc4215fd56931297d6ab1a654c` |

Automated checks found no duplicate IDs, unresolved local fragments, unresolved ARIA references or missing required files. Social-image and favicon bytes remain unchanged; sharing text follows the edited meaning. Historical repository references on primary pages are pinned where appropriate. Latest-release and repository-home routes retain their separate roles. `node --check assets/site.js` passes.

## Browser checks

### Environment and coverage

Tests ran in **Chrome 155.0.0.0 on Linux**, using the site's system-UI and Georgia/Times CSS font stacks. A temporary local verification page embedded the static pages in same-origin browsing contexts with explicit CSS dimensions, checked against each frame's `innerWidth`/`innerHeight`. These are real browser layout tests, not physical-device emulation or a claim that the outer window was resized. The harness, failure injection and temporary dependencies are excluded from the deliverable.

All five pages were rendered and measured at every size below. A classic 15px vertical scrollbar reduced the usable width. The overflow test compared document `scrollWidth` with `clientWidth`, rather than confusing the scrollbar with page overflow.

| CSS viewport | Document client width | Overview | Engine | Demos | Benchmark | Engineering |
|---|---:|---|---|---|---|---|
| 1440 × 900 | 1425 | Pass | Pass | Pass | Pass | Pass |
| 820 × 1180 | 805 | Pass | Pass | Pass | Pass | Pass |
| 390 × 844 | 375 | Pass | Pass | Pass | Pass | Pass |
| 360 × 740 | 345 | Pass | Pass | Pass | Pass | Pass |
| 320 × 844 | 305 | Pass | Pass | Pass | Pass | Pass |

“Pass” means **no page-level horizontal overflow in the measured layout**. It does not certify every interaction or a full visual review at each size. Full desktop flows for all five pages were captured and independently inspected. Additional inspected views cover mobile Overview, A/B results, mobile ranking, Engineering opening, tablet setup, both narrow headings and the changed Overview handoffs. No visible collision, clipped ordinary heading, broken preview or disruptive alignment defect was found in those captures.

### The reported 320px failures

The original Demos and Engineering pages were first rendered at 320×844. In this browser/font environment their widths were 305/305 client/scroll pixels, so the audit's original 338px/325px failures were **not reproduced here**. That difference does not invalidate its recorded environment or justify ignoring 320px.

Final CSS includes safe heading wrapping and a lower narrow-width scale without hiding body overflow. Fresh captures show the full Demos “Read these as demonstrations…” and Engineering “Measure the assumption…” headings. Both final heading boxes run from x=16 to x=289 within the 305px document, with equal client and scroll widths. The 320×650 crops came from 320×844 contexts. Both long words are visibly readable.

### Interaction and resilience results

| Exercise | Observed result |
|---|---|
| Ordinary root serving/navigation | Clicked through all five destinations at `/`; each rendered with correct current-page state and no measured page overflow. |
| Deployment prefix | The 25-layout matrix used `/research-project-starter/`. The frozen historical page rendered there with its original `/research-project-starter/assets/css/style.css?v=…` reference. |
| Representative anchors | Setup clears the tablet sticky header: header bottom 108.67px, section top 128.69px. Case/report and Overview handoff targets were exercised. Direct `index.html#step-outcome` exposes the correct panel. Mobile navigation scrolls away. Static checks cover all retained fragments. |
| Skip and focus | Keyboard skip activation focuses `main`. Tab moves from the selected tab to its panel. Focus/selection was inspected; no screen-reader announcement was listened to. |
| Overview tabs | ArrowLeft/Right, wrapping, Home and End select the expected panel with one tab stop. Only the selected panel is visible after successful enhancement. |
| JavaScript blocked | Without script permission, all three Overview stages remain readable and the tab bar is hidden. All 15 ranking rows remain readable with filters hidden. Native disclosures still open using Enter, including the Engine RB record. |
| Interrupted initialization | A temporary fixture threw on the second relevant listener registration. Tabs recovered to all stages visible with controls hidden; ranking recovered to all 15 rows with controls hidden. The hook is not shipped. |
| Ranking filters | All/Hosted/Local show 15/12/3 rows; `aria-pressed` and status text update. Original ranks remain. Local was also activated with Space. |
| Both table regions | Each has a label, keyboard focus, contained scrolling and a semantic caption inside the table. ArrowRight changed each scroll position. Thirteen effect rows remain available. |
| Overflow cues | At desktop, both regions fit at 1040px and cues are hidden. At 390px, the regions are 271px wide against 515px/448px content; cues are visible and referenced by `aria-describedby`. |
| Report images | All four original lazy-loaded previews completed with nonzero natural width when brought into the capture flow. The Demos full capture confirms all four. |
| Computed contrast | Initial testing found faint decorative arrows. They now use the muted token; the Overview arrow is also hidden from assistive technology. Final checks across all five pages, three tab states and opened disclosures found no failures in tested solid-background text pairs, using 4.5:1 normal/3:1 large-text thresholds. Twenty gradient-backed Demos nodes were excluded from the calculation and visually inspected. This is not a complete contrast audit. |
| Actual download attempt | The Case A ChatGPT RB link was activated in a frame and top-level page. Download-event waits and the documented file-link download route timed out. No completed browser save or downloaded-file hash is claimed. The original path, `download` attribute and SHA-256-preserved payload remain verified. |

Console observations exposed extension metadata errors, not a demonstrated primary-site application error. Script blocking and injected failures were controlled conditions. A command-line request to `localhost:4173` could not reach the managed preview endpoint; root and prefix serving were confirmed through the browser's actual preview address. These environment limits are not reported as broken public URLs.

## Package and visual deliverables

The replacement ZIP has **34 file entries at its root and relative subdirectories**, without an extra enclosing archive level, obsolete site, harness, transcript, private RB, temporary dependency or review screenshot. ZIP CRC integrity, complete inventory, packaged-byte equality against the final site, protected hashes and equality of the separately supplied CHANGES/VALIDATION files were checked before handoff.

The separate preview ZIP contains 16 real JPEG captures and a dimension guide: desktop/mobile Overview, desktop Case A and mobile Case B results, desktop/mobile Benchmark and Engineering, both 320px headings, all five desktop flows, two Overview handoffs and tablet setup. Long captures expand context height at the stated width; normal viewport measurements above retain original heights. Captures show rendered states, not mockups or study results.

## Limits

- **A completed browser download is unverified** because save/download operations timed out. Confirm a saved artifact and hash in the final hosting environment. No live deployment was performed.
- **Actual 200% browser zoom was not performed.** The exposed controls did not provide a documented zoom-setting operation. Narrow CSS viewport tests are not substituted for zoom.
- Testing covered one Linux Chrome environment, not Safari, Firefox, physical phones, every font, assistive technology or every interaction combination. Reduced-motion behavior is present in source but was not independently exercised as an OS preference. Contrast calculations excluded gradient-backed nodes and did not certify every hover/focus or non-text state.
- The frozen archive retains historical accessibility limitations and its expected base path. It was preserved, not remediated. Existing PDF reading alternatives remain aids rather than full PDF accessibility remediation.
- Ten public conversation URLs are preserved; this implementation did not revalidate every live shared-chat destination or private reference. Untested external destinations are not labeled broken. The pinned specification, numerical records and setup/release destinations received the fresh checks described above.
- No benchmark, statistical analysis, research execution, scientific replication or full-engine companion validation was run. No private evidence, automatic memory system, catalogue or update propagation was added. The repository was not modified or committed to, and this package has not been published.
