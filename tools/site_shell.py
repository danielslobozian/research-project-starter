"""The page frame (head, header, footer) shared by the latest version's pages in docs/.

Page builders call page(...) with their <main> content; tools/site_versions.py
adds the version menu afterwards.
"""

from __future__ import annotations

from html import escape

SITE_URL = "https://danielslobozian.github.io/research-project-starter/"
REPO_URL = "https://github.com/danielslobozian/research-project-starter"

NAV = [
    ("index.html", "Overview"),
    ("engine.html", "Research engine"),
    ("guide.html", "Guide"),
    ("demos.html", "Live examples"),
    ("benchmark.html", "Benchmark"),
]


def page(file_name: str, title: str, description: str, main: str) -> str:
    full_title = f"{title} — Research Project Starter"
    url = SITE_URL + ("" if file_name == "index.html" else file_name)
    image = SITE_URL + "assets/social/overview.png"
    t, d = escape(full_title), escape(description)
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == file_name else ""}>{label}</a>' for href, label in NAV
    )
    footer_links = "".join(f'<a href="{href}">{label}</a>' for href, label in NAV[1:])
    return (
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="color-scheme" content="light"><meta name="theme-color" content="#f7f8f6">'
        f'<meta name="description" content="{d}"><title>{t}</title>'
        '<link rel="stylesheet" href="assets/site.css"><script defer src="assets/site.js"></script>'
        '<meta property="og:type" content="website"><meta property="og:site_name" content="Research Project Starter">'
        f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{image}">'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Research Project Starter — clear questions, reusable research">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
        f'<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{image}">'
        f'<meta name="author" content="Daniel Slobozian"><link rel="canonical" href="{url}">'
        '<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"></head><body id="top">\n'
        '<a class="skip-link" href="#main">Skip to main content</a><header class="nav"><nav class="nav-inner" aria-label="Main navigation">'
        '<a class="brand" href="index.html"><span class="brand-icon" aria-hidden="true"><span>R/</span></span>'
        '<span>Research Project Starter<span class="brand-sub">A method for AI-assisted research</span></span></a>'
        f'<div class="nav-items">{nav}<a class="nav-gh" href="{REPO_URL}" target="_blank" rel="noopener noreferrer" '
        'aria-label="GitHub (opens in a new tab)">GitHub ↗</a></div></nav></header>\n'
        f'<main id="main" tabindex="-1">\n{main}\n</main>'
        '<footer class="footer"><div class="container footer-inner"><div><a class="brand" href="index.html">'
        '<span class="brand-icon"><span>R/</span></span><span>Research Project Starter</span></a>'
        '<p>Open research methodology. Built and maintained by Daniel Slobozian. Apache 2.0.</p>'
        '<p class="micro">Benchmark editions are immutable; each names the engine version it measured.</p></div>'
        f'<div class="footer-links">{footer_links}<a href="{REPO_URL}" target="_blank" rel="noopener noreferrer" '
        'aria-label="Source (opens in a new tab)">Source ↗</a><a class="back-top" href="#top">Back ↑</a></div></div></footer></body></html>\n'
    )
