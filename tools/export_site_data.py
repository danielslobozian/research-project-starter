"""Write the website's data for an edition from its results: docs/_data/<edition>.json.

The site (docs/, GitHub Pages) shows the ranking tables from this file; the numbers are formatted here, so
the page templates only lay them out. Run export_results.py first.

Usage:
  python3 export_site_data.py
"""
import json
import os

import paths

RESULTS = os.path.join(paths.REPO, "benchmarks", paths.EDITION, "results")


def price_text(usd):
    if usd is None:
        return "–"
    return f"${usd:.3f}" if usd < 0.1 else f"${usd:.2f}"


def main():
    ranking = json.load(open(os.path.join(RESULTS, "ranking.json")))
    rows = []
    for arm in "ABC":
        for rank, r in enumerate((r for r in ranking["ranking"] if r["arm"] == arm), 1):
            rows.append({"arm": arm, "rank": rank,
                         "model": r["name"] + (" (local)" if r["where"] != "cloud" else ""),
                         "effort": r["effort"],
                         "score": f"{r['score']:+.2f}".replace("-", "−"),
                         "ci95": f"[{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}]".replace("-", "−"),
                         "price": price_text(r["price_usd"]),
                         "minutes": r.get("median_minutes")})
    data = {"edition": paths.EDITION, "verdicts": ranking["verdicts"], "topics": ranking["topics"], "rows": rows}
    out = os.path.join(paths.REPO, "docs", "_data", paths.EDITION.replace("-", "_").replace(".", "_") + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"{len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()
