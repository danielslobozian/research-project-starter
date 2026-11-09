"""Maintain the versioned GitHub Pages site in docs/.

The latest engine version lives at the site root; every older version is a frozen
copy in docs/v<version>/. docs/versions.json lists the versions, latest first.

  python tools/site_versions.py archive 1.6 --dirs samples accessible-text
      Move the root pages (and the listed content folders) into docs/v1.6/ and
      rewrite their links so they keep working from there. Run this before the
      root pages are rewritten for a new version.

  python tools/site_versions.py switcher
      Write the version menu into every page of every version, and the
      "older version" banner into every page that is not the latest.
      Idempotent: rerun it after adding or changing any page.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
CONFIG = DOCS / "versions.json"

SWITCH_START, SWITCH_END = "<!-- version-switch -->", "<!-- /version-switch -->"
BANNER_START, BANNER_END = "<!-- version-banner -->", "<!-- /version-banner -->"
MARKED = re.compile(r"<!-- (version-switch|version-banner) -->.*?<!-- /\1 -->", re.S)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def version_dir(version: dict) -> Path:
    return DOCS / version["dir"] if version["dir"] else DOCS


def pages_of(version: dict) -> list[Path]:
    return sorted(version_dir(version).glob("*.html"))


def archive(name: str, content_dirs: list[str]) -> None:
    config = load_config()
    if any(v["name"] == name for v in config["versions"][1:]):
        sys.exit(f"version {name} is already archived")
    target = DOCS / f"v{name}"
    if target.exists():
        sys.exit(f"{target} already exists")
    target.mkdir()
    site_url = config["site_url"].rstrip("/")
    repo_url = f"https://github.com/{config['repository']}"
    for page in sorted(DOCS.glob("*.html")):
        html = MARKED.sub("", page.read_text(encoding="utf-8"))
        # Shared assets stay at the root; the archived page reaches them one level up.
        html = re.sub(r'((?:href|src)=")assets/', r"\1../assets/", html)
        html = html.replace(f"{site_url}/{page.name}", f"{site_url}/v{name}/{page.name}")
        html = html.replace(f'content="{site_url}/"', f'content="{site_url}/v{name}/"')
        html = html.replace(f'href="{site_url}/"', f'href="{site_url}/v{name}/"')
        # Links to "the current release" or the moving main branch must stay on this version.
        html = html.replace(f"{repo_url}/releases/latest", f"{repo_url}/releases/tag/v{name}")
        html = re.sub(rf"{re.escape(repo_url)}/(tree|blob)/main/", rf"{repo_url}/\1/v{name}/", html)
        (target / page.name).write_text(html, encoding="utf-8")
        page.unlink()
    for folder in content_dirs:
        shutil.move(str(DOCS / folder), str(target / folder))
    config["versions"].insert(1, {"name": name, "dir": f"v{name}", "tag": f"v{name}"})
    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"archived {name} into {target}; now write the new root pages, then run 'switcher'")


def link(from_page: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, from_page.parent).replace(os.sep, "/")


def counterpart(page: Path, version: dict, fallbacks: dict) -> Path:
    """The same page in another version, else its named fallback, else that version's home."""
    folder = version_dir(version)
    for name in (page.name, fallbacks.get(page.name)):
        if name and (folder / name).exists():
            return folder / name
    return folder / "index.html"


def switch_markup(page: Path, current: dict, config: dict) -> str:
    latest = config["versions"][0]
    items = []
    for version in config["versions"]:
        label = version["name"] + (' <span class="version-tag">latest</span>' if version is latest else "")
        mark = ' aria-current="true"' if version is current else ""
        href = link(page, counterpart(page, version, config.get("fallbacks", {})))
        items.append(f'<li><a href="{href}"{mark}>{label}</a></li>')
    return (
        f'{SWITCH_START}<details class="version-switch"><summary aria-label="Engine version {current["name"]}, '
        f'choose another">v{current["name"]}</summary><ul>{"".join(items)}</ul></details>{SWITCH_END}'
    )


def banner_markup(page: Path, current: dict, config: dict) -> str:
    latest = config["versions"][0]
    href = link(page, counterpart(page, latest, config.get("fallbacks", {})))
    return (
        f'{BANNER_START}<div class="version-banner" role="note">You are reading version {current["name"]}. '
        f'<a href="{href}">Read the latest version ({latest["name"]}) →</a></div>{BANNER_END}'
    )


def switcher() -> None:
    config = load_config()
    latest = config["versions"][0]
    for version in config["versions"]:
        for page in pages_of(version):
            html = MARKED.sub("", page.read_text(encoding="utf-8"))
            if "version-switch.css" not in html:
                stylesheet = link(page, DOCS / "assets" / "version-switch.css")
                html = html.replace("</head>", f'<link href="{stylesheet}" rel="stylesheet"/></head>', 1)
            menu = switch_markup(page, version, config)
            github = re.search(r'<a [^>]*class="nav-gh"', html)
            if github:
                html = html[: github.start()] + menu + html[github.start():]
            else:  # a page without the site header: the menu sits in a bar at the top
                bar = SWITCH_START + '<div class="version-bar">' + menu.removeprefix(SWITCH_START).removesuffix(SWITCH_END) + "</div>" + SWITCH_END
                html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + bar, html, count=1)
            if version is not latest:
                banner = banner_markup(page, version, config)
                if "</header>" in html:
                    html = html.replace("</header>", "</header>" + banner, 1)
                else:
                    html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + banner, html, count=1)
            page.write_text(html, encoding="utf-8")
            print(f"{page.relative_to(DOCS)}: v{version['name']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    archive_cmd = commands.add_parser("archive", help="move the root pages into docs/v<version>/")
    archive_cmd.add_argument("version")
    archive_cmd.add_argument("--dirs", nargs="*", default=[], help="content folders that belong to this version")
    commands.add_parser("switcher", help="write the version menu and banner into every page")
    args = parser.parse_args()
    if args.command == "archive":
        archive(args.version, args.dirs)
    else:
        switcher()


if __name__ == "__main__":
    main()
