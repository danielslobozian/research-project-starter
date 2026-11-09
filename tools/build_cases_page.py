"""Build the live-examples page (docs/demos.html) of the latest engine version from its recorded cases.

Inputs, all in docs/cases/ (published with the site):
  cases.json             the case definitions: opening message, profile card, what each case tests
  runs.json              one entry per case and app: model, outcome, what happened, check notes, links
  case<N>/<app>/         the files a run delivered (Research Boundaries file, report, assets) and CHECK.json

  python tools/build_cases_page.py import CASES_JSON RUNS_DIR
      Copy the case definitions and each run's delivered files into docs/cases/. Only
      RUNS_DIR/case<N>/<app>/ folders are copied; anything else in RUNS_DIR (records,
      transcripts, shares) stays private. Then run the privacy check on docs/cases/.

  python tools/build_cases_page.py build
      Write docs/demos.html; then run tools/site_versions.py switcher.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

from site_shell import page

REPO = Path(__file__).resolve().parent.parent
CASES = REPO / "docs" / "cases"
OUTPUT = REPO / "docs" / "demos.html"
BENCHMARK_1_6 = "v1.6/benchmark.html"

# Mistral's file hosting appends this analytics script to HTML files it serves for download.
HOSTING_BEACON = re.compile(r"<script[^>]*static\.cloudflareinsights\.com/beacon[^>]*>\s*</script>\s*", re.I)

OUTCOME_TAG = {"full": "mint", "direct": "orange", "failed": "orange"}


def import_runs(cases_json: Path, runs_dir: Path) -> None:
    cases = json.loads(cases_json.read_text(encoding="utf-8"))
    cases["_about"] = (
        "Hand-run cases for engine 1.7b.10 (2026-11-09). One run per case per app. The opening message is sent "
        "verbatim; every later answer comes from the profile card."
    )
    CASES.mkdir(parents=True, exist_ok=True)
    (CASES / "cases.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    apps = json.loads((CASES / "runs.json").read_text(encoding="utf-8"))["apps"]
    for case in cases["cases"]:
        for app in apps:
            source = runs_dir / f"case{case['id']}" / app
            if not source.is_dir():
                continue
            target = CASES / f"case{case['id']}" / app
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
            for html_file in target.rglob("*.html"):
                text = html_file.read_text(encoding="utf-8")
                cleaned = HOSTING_BEACON.sub("", text)
                if cleaned != text:
                    html_file.write_text(cleaned, encoding="utf-8")
                    print(f"removed the hosting analytics script from {html_file.relative_to(REPO)}")
            print(f"copied {target.relative_to(REPO)}")
    check = subprocess.run([sys.executable, str(REPO / "tools" / "check_private.py"), str(CASES)])
    if check.returncode:
        sys.exit("privacy check failed: fix the files above before building")


def run_files(case_id: int, app: str) -> dict:
    folder = CASES / f"case{case_id}" / app
    if not folder.is_dir():
        return {}
    files = {p.name: p for p in folder.iterdir() if p.is_file()}
    rb = next((p for n, p in files.items() if n.endswith(".rb.md")), None)
    md = next((p for n, p in files.items() if n.endswith(".md") and not n.endswith(".rb.md")), None)
    html = next((p for n, p in files.items() if n.endswith(".html")), None)
    pdf = next((p for n, p in files.items() if n.endswith(".pdf")), None)
    checks = json.loads(files["CHECK.json"].read_text(encoding="utf-8"))["results"] if "CHECK.json" in files else []
    return {"rb": rb, "md": md, "html": html, "pdf": pdf, "checks": checks}


def href(path: Path) -> str:
    return escape(os.path.relpath(path, OUTPUT.parent).replace(os.sep, "/"))


def external(url: str, label: str, context: str) -> str:
    return (f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{escape(label)} for {escape(context)} (opens in a new tab)">{escape(label)} <span aria-hidden="true">↗</span></a>')


def checks_block(checks: list, notes: dict, context: str) -> str:
    if not checks:
        return ""
    passed = sum(c["result"] == "PASS" for c in checks)
    rows = []
    for c in checks:
        note = notes.get(c["check"], "")
        result = "Pass" if c["result"] == "PASS" else "Fail"
        rows.append(f'<tr><td>{escape(c["check"])}</td><td>{result}</td><td>{escape(note)}</td></tr>')
    failed_notes = "".join(
        f'<p class="micro"><strong>Failed:</strong> {escape(c["check"])}. {escape(notes.get(c["check"], ""))}</p>'
        for c in checks if c["result"] != "PASS")
    return (
        f'<details class="evidence-more"><summary>Automatic checks: {passed} of {len(checks)} passed'
        f'<span class="screen-reader"> for {escape(context)}</span></summary>{failed_notes}'
        '<div class="table-wrap" tabindex="0"><table><thead><tr><th>Check</th><th>Result</th><th>Note</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></details>'
    )


def run_card(case: dict, run: dict, apps: dict, outcomes: dict) -> str:
    app = apps[run["app"]]
    context = f"case {case['id']} {app['name']}"
    files = run_files(case["id"], run["app"])
    setting = case["settings"][run["app"]]
    # Claude settings name the model ("Opus 5.5 · High"); keep only the effort part after the model name.
    if " · " in setting and setting.split(" · ")[0] in run["model"]:
        setting = setting.split(" · ", 1)[1]
    label = run["model"] if setting in run["model"] else f'{run["model"]} · {setting}'
    parts = [
        '<article class="demo-model-card">',
        f'<div class="model-line"><span class="model-dot {app["dot"]}">{app["letter"]}</span><div><strong>{escape(app["name"])}</strong>'
        f'<span>{escape(label)}</span></div>'
        f'<span class="tag {OUTCOME_TAG[run["outcome"]]}">{escape(outcomes[run["outcome"]])}</span></div>',
        f'<div class="result-label">Reader questions and brief</div><p>{escape(run["generation"])}</p>',
    ]
    if run["execution"]:
        parts.append(f'<div class="result-label">Research run</div><p>{escape(run["execution"])}</p>')
    links = []
    if files.get("html"):
        links.append(f'<a href="{href(files["html"])}">Read the report (HTML) <span aria-hidden="true">→</span></a>')
    if files.get("pdf"):
        label = "Report (PDF, blank in most readers)" if run["outcome"] == "failed" else "Read the report (PDF)"
        links.append(f'<a href="{href(files["pdf"])}">{label} <span aria-hidden="true">→</span></a>')
    if files.get("md"):
        links.append(f'<a href="{href(files["md"])}">Report source (Markdown) <span aria-hidden="true">→</span></a>')
    if files.get("rb"):
        links.append(f'<a href="{href(files["rb"])}">Research Boundaries file <span aria-hidden="true">→</span></a>')
    if run["generation_link"]:
        links.append(external(run["generation_link"], "Brief conversation", context))
    if run["execution_link"]:
        links.append(external(run["execution_link"], "Research conversation", context))
    if links:
        parts.append(f'<div class="demo-links evidence-primary" aria-label="Files and conversations for {escape(context)}">{"".join(links)}</div>')
    if not run["generation_link"] and not run["execution_link"]:
        parts.append('<p class="micro">The conversations of this run are not published.</p>')
    parts.append(checks_block(files.get("checks", []), run["check_notes"], context))
    parts.append("</article>")
    return "".join(parts)


def case_section(case: dict, runs: list, data: dict, index: int) -> str:
    apps, outcomes = data["apps"], data["outcomes"]
    lang = ' lang="fr"' if case["expect"]["language"] == "fr" else ""
    card = "".join(f"<tr><th scope=\"row\">{escape(k)}</th><td>{escape(v)}</td></tr>" for k, v in case["card"])
    followed = sum(r["outcome"] != "direct" for r in runs)
    cards = "".join(run_card(case, r, apps, outcomes) for r in runs)
    shade = "white" if index % 2 == 0 else "warm"
    return (
        f'<section class="section {shade}" id="case-{case["id"]}"><div class="container">'
        f'<div class="case-head"><div><div class="eyebrow">Case {case["id"]} / {escape(case["title"])}</div>'
        f'<h2{lang}>“{escape(case["opening"])}”</h2>'
        f'<p class="lead">{escape(re.sub(r"\s*Same question as benchmark topic \w+\.", "", case["tests"]))}</p></div>'
        f'<span class="case-badge">{followed} of {len(runs)} followed</span></div>'
        '<div class="grid grid-2 case-profile"><div><div class="result-label">The simulated user’s profile card</div>'
        f'<div class="table-wrap" tabindex="0"><table><tbody>{card}</tbody></table></div>'
        f'<p class="micro">Same question as topic {escape(case["topic_ref"])} of the <a class="link-inline" href="{BENCHMARK_1_6}">1.6 benchmark</a>.</p></div>'
        f'<div class="demo-insight stacked"><span>COMPARISON</span><p>{escape(data["comparisons"][str(case["id"])])}</p></div></div>'
        f'<div class="grid grid-3 demo-result-grid">{cards}</div>'
        "</div></section>"
    )


def build() -> None:
    cases = json.loads((CASES / "cases.json").read_text(encoding="utf-8"))
    data = json.loads((CASES / "runs.json").read_text(encoding="utf-8"))
    app_order = list(data["apps"])
    by_case = {c["id"]: sorted((r for r in data["runs"] if r["case"] == c["id"]), key=lambda r: app_order.index(r["app"]))
               for c in cases["cases"]}
    ordered = sorted(cases["cases"], key=lambda c: c["id"])
    runs = data["runs"]
    counts = {k: sum(r["outcome"] == k for r in runs) for k in data["outcomes"]}

    overview_rows = "".join(
        f'<tr><th scope="row"><a class="link-inline" href="#case-{c["id"]}">{c["id"]} · {escape(c["title"])}</a></th>'
        + "".join(f'<td>{escape(data["outcomes"][r["outcome"]])}<br><span class="micro">{escape(c["settings"][r["app"]])}</span></td>'
                  for r in by_case[c["id"]])
        + "</tr>"
        for c in ordered)
    app_heads = "".join(f"<th>{escape(a['name'])}</th>" for a in data["apps"].values())
    rules = "".join(f"<li>{escape(r)}</li>" for r in cases["rules_for_the_user"])
    nav = "".join(f'<a class="btn light small" href="#case-{c["id"]}">{c["id"]} · {escape(c["title"])}</a>' for c in ordered)

    main = (
        '<section class="page-hero demo-hero"><div class="container">'
        f'<div class="eyebrow">Recorded cases · 9 November 2026 · engine {escape(cases["engine"])}</div>'
        '<div class="demo-hero-grid"><div><h1>Five questions, <span class="serif accent">three</span> apps.</h1>'
        '<p class="lead">Each case is one question asked in ChatGPT, Claude and Mistral Vibe with the two projects installed: '
        'first the brief and its Research Boundaries file, then the research run that file drives. '
        'Every run is shown as it ended, including the ones that skipped the engine.</p>'
        '<p class="demo-context">These are genuine runs with <strong>simulated users</strong>: the person typing answered '
        'only from a profile card written beforehand.</p>'
        f'<nav class="btn-row case-nav" aria-label="Choose a case">{nav}</nav>'
        '<p class="micro demo-method-link"><a class="link-inline" href="#how">How these runs were made <span aria-hidden="true">↓</span></a></p></div>'
        '<div class="demo-hero-sidebar">'
        f'<div class="demo-stat"><strong>{len(runs):02d}</strong><span>runs<br>5 cases × 3 apps</span></div>'
        f'<div class="demo-stat"><strong>{counts["full"]:02d}</strong><span>followed the engine<br>to a readable report</span></div>'
        f'<div class="demo-stat"><strong>{counts["direct"]:02d}</strong><span>answered directly<br>without the engine</span></div>'
        "</div></div></div></section>"
        '<section class="section white" id="overview"><div class="container"><div class="eyebrow">At a glance</div>'
        '<h2>What each app did.</h2>'
        f'<div class="table-wrap" tabindex="0"><table><thead><tr><th>Case</th>{app_heads}</tr></thead><tbody>{overview_rows}</tbody></table></div>'
        '<p class="micro">“Delivered an unreadable file”: the report PDF is blank in most readers; its Markdown copy is intact.</p>'
        "</div></section>"
        '<section class="section warm" id="lessons"><div class="container"><div class="eyebrow">What the runs show</div>'
        '<h2>Use the stronger settings, and know your app.</h2><div class="grid grid-2">'
        '<div class="demo-insight stacked"><span>SETTINGS</span><p>On ChatGPT at Medium and Instant, and on Claude Haiku at Low, '
        'the generation project was skipped: a simple-looking question got a direct answer, with no reader questions and no brief. '
        'The higher settings followed the engine.</p></div>'
        '<div class="demo-insight stacked"><span>MISTRAL VIBE</span><p>The “Thinking” setting runs <strong>GLM-5</strong> '
        '(<code>glm-5-latest-short</code>, a model Mistral hosts), not a Mistral model. Vibe turns every question into a '
        'multiple-choice popup: type your own answer in its free field. Vibe cannot render PDFs, so ask for HTML reading copies.</p></div>'
        '<div class="demo-insight stacked"><span>CLAUDE FABLE 5.1</span><p>At Max, Fable 5.1 treated the project instructions as a '
        'prompt injection, because the app delivered them inside a tool result, and answered directly.</p></div>'
        '<div class="demo-insight stacked"><span>READER QUESTIONS</span><p>Every app that followed the engine asked its reader questions '
        'first: at most four, open, each with a default, and never took the answers as approval of the brief.</p></div>'
        "</div></div></section>"
        + "".join(case_section(c, by_case[c["id"]], data, i) for i, c in enumerate(ordered))
        + '<section class="section white" id="how"><div class="container"><div class="eyebrow">Method</div>'
        '<h2>How these runs were made.</h2>'
        '<p>One run per case and app, on one day, with engine 1.7b.10 installed as two projects in each app. Nothing was re-run: '
        'a run that answered directly or delivered a broken file is reported as it ended. The settings differ from case to case '
        'on purpose, from the lightest (case 5) to the strongest (cases 3 and 4).</p>'
        f'<p>The person running the cases followed these rules:</p><ol>{rules}</ol>'
        '<p>Each delivered run was then checked automatically: the Research Boundaries file, the reader-context fields, the '
        'format, the language, page limits, self-contained HTML and the absence of personal details. The checks and their '
        'results are with each run. The definitions are in <a class="link-inline" href="cases/cases.json">cases.json</a> '
        'and the run summaries in <a class="link-inline" href="cases/runs.json">runs.json</a>.</p>'
        "</div></section>"
    )
    description = ("Five questions run in ChatGPT, Claude and Mistral Vibe with engine 1.7b.10: the briefs, the "
                   "Research Boundaries files, the reports and what each app did.")
    OUTPUT.write_text(page("demos.html", "Live examples", description, main), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO)}; now run: python tools/site_versions.py switcher")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    imp = commands.add_parser("import", help="copy case definitions and delivered files into docs/cases/")
    imp.add_argument("cases_json", type=Path)
    imp.add_argument("runs_dir", type=Path)
    commands.add_parser("build", help="write docs/demos.html")
    args = parser.parse_args()
    if args.command == "import":
        import_runs(args.cases_json, args.runs_dir)
    else:
        build()


if __name__ == "__main__":
    main()
