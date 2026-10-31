"""Copy an edition's results from its data into the repository, and write the ranking tables.

From $RPS_DATA/benchmarks/<edition>/scoring/ to benchmarks/<edition>/results/:
- within-model/<model>/: analysis.json and topics.csv of the model's own A/B/C grading (v4.1-cross/<model>,
  Haiku's round 1 from v4.1-benchmark);
- comparisons/<name>/analysis.json: the effort and cross-model comparisons (v4.1-inter);
- ranking.json: the panel ranking (panel_rank.py) with each item's display name, effort and price
  (inputs/models.json, results/prices.json from report_prices.py);
- ranking.md: one table per arm, best first.

Run panel_rank.py and report_prices.py first.

Usage:
  python3 export_results.py
"""
import json
import os
import shutil

import paths

SCORING = os.path.join(paths.DATA, "scoring")
RESULTS = os.path.join(paths.REPO, "benchmarks", paths.EDITION, "results")
MODELS = json.load(open(os.path.join(paths.INPUTS, "models.json")))["models"]
COMPARISONS = {"haiku-xhigh-vs-haiku": "haiku-xhigh-vs-haiku/analysis.json",
               "luna-xhigh-vs-luna": "luna-xhigh-vs-luna/analysis.json",
               "luna-xhigh-B-vs-luna-C": "luna-xhigh-vs-luna-C/analysis.json",
               "luna-xhigh-vs-sol": "luna-xhigh-vs-sol/analysis.json",
               "sol-high-vs-sol": "sol-high-vs-low/analysis.json",
               "sonnet-vs-haiku": "sonnet-analysis.json"}
ARMS = {"A": "the casual question", "B": "the research brief (RB), then research from it",
        "C": "the full engine with the RB"}


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def main():
    for model in MODELS:
        src = os.path.join(SCORING, "v4.1-benchmark" if model == "haiku" else os.path.join("v4.1-cross", model))
        if os.path.exists(os.path.join(src, "analysis.json")):
            for name in ("analysis.json", "topics.csv"):
                copy(os.path.join(src, name), os.path.join(RESULTS, "within-model", model, name))
    for name, src in COMPARISONS.items():
        copy(os.path.join(SCORING, "v4.1-inter", src), os.path.join(RESULTS, "comparisons", name, "analysis.json"))

    ranking = json.load(open(os.path.join(SCORING, "v4.1-panel", "ranking.json")))
    prices = json.load(open(os.path.join(RESULTS, "prices.json")))["prices"]
    for row in ranking["ranking"]:
        model, arm = row["item"].split(":")
        row.update(model=model, arm=arm, name=MODELS[model]["name"], effort=MODELS[model]["effort"],
                   where=MODELS[model]["where"], price_usd=prices.get(row["item"], {}).get("usd"))
    ranking["_about"] = ("Bradley-Terry scores on one scale for every model x arm (tools/panel_rank.py); "
                         "price per report in USD (tools/report_prices.py), B and C including the RB")
    with open(os.path.join(RESULTS, "ranking.json"), "w") as f:
        json.dump(ranking, f, indent=1)

    lines = ["# Ranking by arm", "",
             f"Scores share one scale across arms: log strength, centred on the mean item; 95% interval from a "
             f"topic bootstrap. {ranking['verdicts']} verdicts on {len(ranking['topics'])} topics "
             f"({', '.join(ranking['topics'])}). Price per report in USD; B and C include the RB."]
    for arm, what in ARMS.items():
        rows = [r for r in ranking["ranking"] if r["arm"] == arm]
        lines += ["", f"## Arm {arm}: {what}", "",
                  "| # | Model | Effort | Score [95% CI] | Price / report | Median min |",
                  "|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            local = " (local)" if r["where"] != "cloud" else ""
            price = f"${r['price_usd']:.3f}" if r["price_usd"] is not None and r["price_usd"] < 0.1 else (
                f"${r['price_usd']:.2f}" if r["price_usd"] is not None else "–")
            lines.append(f"| {i} | {r['name']}{local} | {r['effort']} | {r['score']:+.2f} "
                         f"[{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}] | {price} | {r.get('median_minutes', '–')} |")
        absent = [f"{m['name']} ({m['effort']})" for k, m in MODELS.items()
                  if not any(r["model"] == k for r in rows)]
        if absent:
            lines += ["", f"Not run in arm {arm}: {', '.join(absent)}."]
    with open(os.path.join(RESULTS, "ranking.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"results -> {RESULTS}")


if __name__ == "__main__":
    main()
