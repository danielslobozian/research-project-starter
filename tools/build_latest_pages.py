"""Write the hand-written pages of the latest engine version: docs/index.html (and, as they are added,
the other root pages). The live-examples page has its own builder, tools/build_cases_page.py.

  python tools/build_latest_pages.py
  python tools/site_versions.py switcher
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from site_shell import REPO_URL, page

DOCS = Path(__file__).resolve().parent.parent / "docs"
ENGINE = "1.7b.10"
RELEASE_URL = f"{REPO_URL}/releases/tag/v{ENGINE}"
BENCHMARK_1_6 = "v1.6/benchmark.html"

INDEX = f"""
<section class="hero"><div class="container hero-grid"><div>
<div class="eyebrow">Open-source research methodology · v{ENGINE}</div>
<h1>Research that <span class="serif accent">remembers</span> its boundaries.</h1>
<p class="lead">Two projects for ChatGPT, Claude or Mistral Vibe. The first asks who the report is for, agrees the
research with you and issues a Research Boundaries (RB) file. The second takes that file and researches it, and
returns a report with its evidence and limits.</p>
<div class="btn-row"><a class="btn" href="#two-projects">See how it works <span class="arrow">↓</span></a>
<a class="btn light" href="engine.html#install">Install the projects →</a></div>
<div class="hero-meta"><span class="tag">No app to install</span><span class="tag">ChatGPT, Claude &amp; Mistral Vibe projects</span><span class="tag">Apache 2.0</span></div>
</div>
<div class="hero-right"><div class="stage-card"><div class="window-head"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="window-title">case 3 / generation project</span></div>
<div class="stage-content">
<div class="stage-label"><span class="num">01</span> The question</div>
<p class="stage-question">“Do AI coding assistants actually make experienced developers faster, or does it just feel that way?”</p>
<div class="stage-arrow" aria-hidden="true">↓</div>
<div class="stage-label"><span class="num">02</span> Reader questions</div>
<p class="micro">Who will read it, what will they do with it, and in what situation? Answer, or type “skip”.</p>
<div class="stage-arrow" aria-hidden="true">↓</div>
<div class="stage-label"><span class="num">03</span> Approved Research Boundaries</div>
<div class="rb-block">
<div class="rb-line"><span class="rb-key">Q0</span><span class="rb-val">For experienced developers on large existing codebases, how do AI assistants affect completion time and quality, and how do measured effects compare with perceived gains?</span></div>
<div class="rb-line"><span class="rb-key">PURPOSE</span><span class="rb-val">Check the “55% faster” claim and give source-backed wording for a manager.</span></div>
<div class="rb-line"><span class="rb-key">READER</span><span class="rb-val">Professional backend development on large existing codebases.</span></div>
</div>
<div class="stage-out"><span class="file-chip">ai-coding-assistants-productivity.rb.md ✓</span></div>
</div></div>
<div class="stage-float">Excerpt from a <a class="link-inline" href="demos.html#case-3">recorded case</a>.</div></div>
</div></section>

<section class="section white" id="two-projects"><div class="container">
<div class="section-head"><div class="eyebrow">01 / Two projects, two decisions</div>
<h2>Agree the research first.<br/><span class="serif">Then run it.</span></h2>
<p class="lead">Deciding what to investigate and investigating it happen in two separate projects. The RB file
is the only thing that passes from one to the other, so the research works from what you approved and nothing else.</p></div>
<div class="mode-cols">
<div class="mode recommended"><span class="tag blue">Generation project</span><h3>From your question to an approved RB</h3>
<p>Describe what you want to know in your own words. The project asks a few reader questions, then proposes a
brief: the main question, the supporting questions, what is in and out of scope, and the evidence expected.
Correct it as often as you like; when you write “approved”, it issues the RB as a file. It does not research.</p></div>
<div class="mode"><span class="tag mint">Execution project</span><h3>From the RB to a report</h3>
<p>Open a new chat, attach the RB and send it with no text. The project searches, reads and appraises the
sources, answers each question or states the evidence gap, and checks its claims against the sources before
delivering. You receive the report as HTML (or PDF if you asked for one), its Markdown source and the RB.</p></div>
</div>
<p><a class="link-inline" href="engine.html">What each project does, step by step →</a></p>
</div></section>

<section class="section warm" id="reader-questions"><div class="container">
<div class="section-head"><div class="eyebrow">02 / New in {ENGINE}</div>
<h2>It asks who the report is for<br/><span class="serif">before it proposes anything.</span></h2>
<p class="lead">The first reply is a short set of questions, at most four, each open and each with a stated
default. Answer what you like; “skip” keeps the defaults, and the RB records them as assumptions.</p></div>
<div class="grid grid-2">
<div class="artifact"><strong>What you already know</strong><p>Sets the depth: a newcomer gets terms explained, an expert gets the statistics.</p></div>
<div class="artifact"><strong>What the report is for</strong><p>Decides what leads: a decision, an explanation for others, or a claim to check and cite.</p></div>
<div class="artifact"><strong>Who will read it</strong><p>The requester, or the colleagues, manager or committee it will be passed to.</p></div>
<div class="artifact"><strong>Your situation</strong><p>Asked only when it changes which evidence applies. It shapes emphasis, not scope, unless you choose to narrow the research.</p></div>
</div>
<p class="micro">Questions are skipped when everything is already known, when you waive them, or when you continue or revise an earlier topic. Personal details are written impersonally in the RB and the report.</p>
</div></section>

<section class="section white" id="artifacts"><div class="container">
<div class="section-head"><div class="eyebrow">03 / What you keep</div>
<h2>The answer stays tied<br/><span class="serif">to what was agreed.</span></h2></div>
<div class="grid grid-3">
<div class="artifact"><em>topic.rb.md</em><strong>What was agreed</strong><p>The questions, scope, exclusions, evidence expectations, reader context and the approval. Keep it: a later reader can see what the research was meant to answer.</p><span class="tag mint">Generation project</span></div>
<div class="artifact"><em>topic.html</em><strong>The report to read</strong><p>A self-contained HTML reading copy, or a PDF when the RB asks for one, with numbered references to inspectable sources.</p><span class="tag blue">Execution project</span></div>
<div class="artifact"><em>topic.md</em><strong>The source for tools</strong><p>The same content in Markdown, for search, comparison or feeding to another assistant.</p><span class="tag">Execution project</span></div>
</div></div></section>

<section class="section live-teaser" id="real-examples"><div class="container">
<div class="section-head"><div class="eyebrow">04 / Recorded cases</div>
<h2>Five questions.<br/><span class="serif">Three apps.</span></h2>
<p class="lead">Each case was run once in ChatGPT, Claude and Mistral Vibe, with a simulated user answering from a
profile card. Nine runs followed the engine to a readable report; five answered directly, mostly on lighter settings.</p></div>
<div class="grid grid-3">
<a class="demo-mini" href="demos.html#case-1"><span class="tag blue">CASE 1 · A PARENT</span><h3>Screen time and a six-year-old</h3><p>The child's age stays reader context: the reports lead with what the evidence means for family rules.</p><span class="demo-next">Explore case 1 →</span></a>
<a class="demo-mini" href="demos.html#case-3"><span class="tag mint">CASE 3 · AN EXPERT</span><h3>Checking “55% faster”</h3><p>Two reports trace the figure to its study and explain why it does not carry over to large existing codebases.</p><span class="demo-next">Explore case 3 →</span></a>
<a class="demo-mini" href="demos.html#case-5"><span class="tag orange">CASE 5 · IN FRENCH</span><h3>Every question skipped</h3><p>The skipped answers become recorded assumptions, and the report is written in French.</p><span class="demo-next">Explore case 5 →</span></a>
</div>
<p class="micro" style="margin-top:22px"><a class="link-inline" href="demos.html">All five cases, with what each app did →</a></p>
</div></section>

<section class="section dark" id="evidence"><div class="container">
<div class="section-head"><div class="eyebrow" style="color:#a7c4da">05 / Evidence</div>
<h2>Benchmarked at 1.6.<br/><span class="serif" style="color:#d1f6e8">Not yet at {ENGINE}.</span></h2>
<p class="lead">The October 2026 benchmark measured engine 1.6. It found that writing the research from an RB gave
better-judged reports than writing it from the initial question, for 11 of 12 models. Version {ENGINE} has not
been benchmarked: its reader questions and execution project are shown by the recorded cases, not measured.</p></div>
<div class="proof-panel"><div><div class="proof-large">11<span style="font-size:.45em;color:#a1b4c4">/12</span></div>
<p class="proof-sub">Models produced better-judged reports from Research Boundaries than from the initial question alone (engine 1.6).</p>
<p class="micro" style="color:#aac1ce">October 2026 conditions; one LLM judge; five shared topics across models. The result does not carry over automatically to later versions.</p></div>
<div class="proof-side"><h3>Inspect the experiment</h3><p>15 model configurations, 1,666 grading sessions and 4,075 pairwise verdicts, with the raw records.</p>
<a class="proof-link" href="{BENCHMARK_1_6}">Explore the 1.6 benchmark →</a></div></div>
</div></section>

<section class="section" id="start"><div class="container"><div class="section-head"><div class="eyebrow">06 / Start</div>
<h2>Set up two projects.<br/><span class="serif">Bring your question.</span></h2>
<p class="lead">Each project takes one block of instructions and two files. Use a strong setting: on the lighter
ones, a simple-looking question was answered directly instead of going through the engine.</p>
<div class="btn-row"><a class="btn" href="engine.html#install">Installation steps →</a><a class="btn light" href="{RELEASE_URL}">Download v{ENGINE} ↗</a></div></div>
</div></section>
"""


FILES_URL = f"{REPO_URL}/blob/v{ENGINE}"


def engine_file(path: str) -> str:
    name = path.rsplit("/", 1)[1]
    return f'<a class="link-inline" href="{FILES_URL}/{path}"><code>{name}</code></a>'


GEN = "research-boundary-generation/research-boundary-generation"
EXE = "research-boundary-execution/research-boundary-execution"

ENGINE_PAGE = f"""
<section class="page-hero"><div class="container"><div class="eyebrow">Research engine · v{ENGINE}</div>
<h1>Two projects. <span class="serif accent">One file</span> between them.</h1>
<p class="lead">The generation project turns your question into an approved Research Boundaries (RB) file. The
execution project researches that file and delivers the report. Each project is a block of instructions and two
files, in any assistant that has projects, web search and file creation.</p>
<div class="btn-row"><a class="btn" href="#install">Install <span class="arrow">↓</span></a>
<a class="btn light" href="{RELEASE_URL}">Download v{ENGINE} ↗</a></div></div></section>

<section class="section white" id="workflow"><div class="container">
<div class="section-head"><div class="eyebrow">01 / Generation project</div>
<h2>From your question<br/><span class="serif">to an approved RB.</span></h2>
<p class="lead">It does not research. Before approval it may run a handful of searches to learn the vocabulary,
but it does not read or report findings: the scope is not anchored on early results.</p></div>
<div class="grid grid-2">
<div class="artifact"><em>Step 1</em><strong>You ask, in your own words</strong><p>A question, a worry, a claim to check. Examples you give are treated as illustrations unless you make them mandatory.</p></div>
<div class="artifact"><em>Step 2</em><strong>Capability check and reader questions</strong><p>It checks what this app can do (web, files, PDF, code) and names any fallback. Then it asks up to four open questions about the reader, each with the default it will use, and stops.</p></div>
<div class="artifact"><em>Step 3</em><strong>A brief of about 350 words</strong><p>A neutral main question (Q0), supporting questions, boundaries and exclusions, the evidence expected, and one deliverable line: audience, depth, purpose, reader context, format, length. At most three open points, each with its assumption.</p></div>
<div class="artifact"><em>Step 4</em><strong>Approval issues the RB</strong><p>Correct the brief as often as you like; each revision gets a new brief ID. “approved” issues the RB file with nine sections, from the objective to the deliverable contract and the assumptions. A new question or boundary is shown again before it is approved.</p></div>
</div></div></section>

<section class="section warm" id="execution"><div class="container">
<div class="section-head"><div class="eyebrow">02 / Execution project</div>
<h2>From the RB<br/><span class="serif">to a report.</span></h2>
<p class="lead">Open a new chat in the execution project, attach the RB and send it with no text. One assistant
does everything in that one conversation; it does not change the RB's scope.</p></div>
<div class="grid grid-2">
<div class="artifact"><em>Step 5</em><strong>Investigate the questions</strong><p>Search and read within the RB's scope and method, appraise the evidence that drives conclusions, and weigh counter-evidence. Each question ends with an answer, an investigated inconclusive result, or a disclosed evidence gap.</p></div>
<div class="artifact"><em>Step 6</em><strong>Write for the reader</strong><p>The RB's purpose decides what leads (a decision, an explanation for others, a claim to check and cite); the reader context decides which evidence is emphasised. Numbered citations point to inspectable source locations.</p></div>
<div class="artifact"><em>Step 7</em><strong>Render and measure</strong><p>The reading copy (self-contained HTML, or PDF) is rendered from the Markdown source. The body length is measured in the reference layout, or reported as “unverified”.</p></div>
<div class="artifact"><em>Step 8</em><strong>Reconcile, then deliver</strong><p>The claims that drive conclusions are rechecked against their sources. You receive the reading copy, the Markdown source, the unmodified RB (and a ZIP when there are figures), with two stated outcomes: research complete or not, delivery complete or partial.</p></div>
</div></div></section>

<section class="section white" id="install"><div class="container">
<div class="section-head"><div class="eyebrow">03 / Install</div>
<h2>Two projects,<br/><span class="serif">three files each.</span></h2>
<p class="lead">Download the release, or open each file below. In every app, create two separate projects.</p></div>
<div class="mode-cols">
<div class="mode recommended"><span class="tag blue">Generation project</span><h3>Instructions and two files</h3>
<p><strong>Project instructions:</strong> paste the whole of {engine_file(GEN + ".instructions.md")}.</p>
<p><strong>Project files:</strong> upload {engine_file(GEN + ".protocol.md")} and {engine_file(GEN + ".template.md")}, keeping their names.</p></div>
<div class="mode"><span class="tag mint">Execution project</span><h3>Instructions, two files, tools on</h3>
<p><strong>Project instructions:</strong> paste the whole of {engine_file(EXE + ".instructions.md")}.</p>
<p><strong>Project files:</strong> upload {engine_file(EXE + ".protocol.md")} and {engine_file(EXE + ".template.md")}, keeping their names.</p>
<p><strong>Tools:</strong> enable web search, file reading and file creation. Code execution helps with PDF checks; an HTML report needs no converter.</p></div>
</div>
<div class="note" style="margin-top:25px"><strong>Keep the projects apart.</strong> Never put both sets of instructions in one project, and do not upload the README or the change log: they are documentation.</div>
<h3 style="margin-top:40px">Per app, from the recorded cases</h3>
<div class="grid grid-3">
<div class="artifact"><strong>ChatGPT</strong><p>Use a Thinking setting at High or above. At Medium and Instant, a simple-looking question was answered directly, without the engine.</p></div>
<div class="artifact"><strong>Claude</strong><p>Opus and Sonnet followed the engine. Haiku at Low answered directly; Fable 5.1 at Max treated the project instructions as a prompt injection.</p></div>
<div class="artifact"><strong>Mistral Vibe</strong><p>“Thinking” runs GLM-5 (<code>glm-5-latest-short</code>). Its questions come as multiple-choice popups: type your own answer in the free field. Ask for HTML: Vibe cannot render PDFs. Prefer the ZIP package: in case 1, an HTML file downloaded from Vibe on its own came with an analytics script added by its file hosting.</p></div>
</div>
<p class="micro"><a class="link-inline" href="demos.html">See what each app did in the five cases →</a></p>
</div></section>

<section class="section warm" id="use"><div class="container">
<div class="section-head"><div class="eyebrow">04 / Use</div><h2>Five steps,<br/><span class="serif">two chats.</span></h2></div>
<ol class="readable">
<li>In the generation project, describe what you want to know, in your own words.</li>
<li>Answer the reader questions as far as you like; “skip” uses the stated assumptions.</li>
<li>Read the brief; correct it, or approve it with “approved”. The RB is issued as a file.</li>
<li>In the execution project, open a new chat, attach the RB, and send it with no text.</li>
<li>You receive the report as HTML (or PDF if you asked for it), its Markdown source for tools, and the RB.</li>
</ol>
<p class="readable">To revise the research later, go back to the generation project: a material change is a new brief and a new RB.
Explanatory follow-up questions about a delivered report can be answered within its scope.</p>
</div></section>

<section class="section white" id="operating-limits"><div class="container">
<div class="section-head"><div class="eyebrow">05 / Limits</div><h2>A research method,<br/><span class="serif">not a guarantee.</span></h2></div>
<div class="grid grid-2">
<div class="artifact"><strong>The app decides whether to follow it</strong><p>Project instructions are a request to the model. In the cases, five of fifteen runs answered directly instead.</p></div>
<div class="artifact"><strong>The model checks its own work</strong><p>Source rechecks, page measurement and rendering checks are done by the same assistant, and reported as performed or not performed. They are not independent verification.</p></div>
<div class="artifact"><strong>Access limits evidence</strong><p>Paywalled or blocked sources are disclosed, not cited from memory. A failed retrieval is not evidence that a study does not exist.</p></div>
<div class="artifact"><strong>Not yet benchmarked</strong><p>The October 2026 benchmark measured engine 1.6. Version {ENGINE} is shown by the recorded cases, not measured. <a class="link-inline" href="{BENCHMARK_1_6}">The 1.6 benchmark →</a></p></div>
</div></div></section>

<section class="section warm" id="changes"><div class="container">
<div class="section-head"><div class="eyebrow">06 / Since 1.6</div><h2>What changed.</h2></div>
<ul class="readable">
<li><strong>Two projects instead of one.</strong> Agreeing the research and carrying it out are separate projects, joined only by the RB file.</li>
<li><strong>Reader questions.</strong> Before the first brief, up to four open questions about the reader and the use; the answers are recorded in the RB.</li>
<li><strong>Reader context.</strong> A new RB field for the reader's situation where it makes some evidence more applicable; it shapes emphasis, not scope.</li>
<li><strong>A reading copy by default.</strong> Every report comes as a self-contained HTML (or PDF) to read, with the Markdown as source for tools.</li>
</ul>
<p class="readable">The 1.6 engine, its guide and its live examples remain available: choose <strong>v1.6</strong> in the version menu, or download the <a class="link-inline" href="{REPO_URL}/releases/tag/v1.6">v1.6 release</a>.</p>
</div></section>
"""


BENCHMARK_PAGE = f"""
<section class="page-hero"><div class="container"><div class="eyebrow">Benchmark · engine v{ENGINE}</div>
<h1>Not yet <span class="serif accent">measured.</span></h1>
<p class="lead">No benchmark edition has measured engine {ENGINE} yet. Until one does, its behaviour is shown by the
<a class="link-inline" href="demos.html">recorded cases</a>: one run per case and app, described, not scored.</p></div></section>

<section class="section white" id="editions"><div class="container">
<div class="section-head"><div class="eyebrow">Editions</div><h2>Every edition<br/><span class="serif">stays published.</span></h2>
<p class="lead">An edition is immutable and names the engine version it measured. A new edition is added beside
the earlier ones; it does not replace them.</p></div>
<div class="table-wrap" tabindex="0"><table><thead><tr><th>Edition</th><th>Engine</th><th>What it compared</th><th>Results</th></tr></thead><tbody>
<tr><td>October 2026</td><td>1.6</td><td>An informal question, research from the RB alone, and research with the full protocol, across 15 model configurations, judged pairwise by one LLM judge.</td>
<td><a class="link-inline" href="{BENCHMARK_1_6}">Read the edition →</a><br/><a class="link-inline" href="{REPO_URL}/tree/main/benchmarks/2026-10-engine-1.6">Raw data ↗</a></td></tr>
</tbody></table></div>
<p class="micro">Results of one edition do not carry over to a later engine version: 1.7b.10 changed how the research is agreed and carried out.</p>
</div></section>
"""


GUIDE_SOURCE = DOCS.parent / "research-project-guide.md"


def guide_page() -> str:
    """The guide's Markdown (the repository copy) rendered into the site frame."""
    body = subprocess.run(
        ["pandoc", "--from", "markdown", "--to", "html", "--shift-heading-level-by=1", str(GUIDE_SOURCE)],
        check=True, capture_output=True, text=True).stdout
    body = re.sub(r'href="https://danielslobozian\.github\.io/research-project-starter/([a-z]+\.html)"', r'href="\1"', body)
    return (
        f'<section class="page-hero"><div class="container"><div class="eyebrow">Design guide · v{ENGINE}</div>'
        '<h1>Why the engine <span class="serif accent">works</span> as it does.</h1>'
        '<p class="lead">The design choices behind the two projects, the reader questions, approval, evidence and '
        f'delivery. Also available as <a class="link-inline" href="{FILES_URL}/research-project-guide.md">Markdown</a>.</p>'
        '</div></section>'
        f'<section class="section white"><div class="container readable guide-body">{body}</div></section>'
    )


def main() -> None:
    benchmark_description = (f"Benchmark editions of the Research Project Starter; engine {ENGINE} has not been "
                             "measured yet. The October 2026 edition measured engine 1.6.")
    (DOCS / "benchmark.html").write_text(page("benchmark.html", "Benchmark", benchmark_description, BENCHMARK_PAGE),
                                         encoding="utf-8")
    description = ("Two projects for ChatGPT, Claude or Mistral Vibe: agree the research and issue a Research "
                   "Boundaries file, then research from it and keep the answer with its evidence and limits.")
    guide_description = (f"The design rationale of engine {ENGINE}: two projects, reader questions, reader context, "
                         "approval, evidence and delivery, with sources.")
    (DOCS / "guide.html").write_text(page("guide.html", "Design guide", guide_description, guide_page()),
                                     encoding="utf-8")
    (DOCS / "index.html").write_text(page("index.html", "Research that remembers its boundaries", description, INDEX),
                                     encoding="utf-8")
    engine_description = (f"How the two projects of engine {ENGINE} work, how to install them in ChatGPT, Claude or "
                          "Mistral Vibe, and their limits.")
    (DOCS / "engine.html").write_text(page("engine.html", "Research engine", engine_description, ENGINE_PAGE),
                                      encoding="utf-8")
    print("wrote docs/index.html, engine.html, guide.html and benchmark.html; now run: python tools/site_versions.py switcher")


if __name__ == "__main__":
    main()
