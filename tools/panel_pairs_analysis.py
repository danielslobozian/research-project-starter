"""Analyse panel grading: every pair of reports shown together in compare_v4.py --panel sessions.

Folder layout (compare_v4.py --panel): <root>/run<k>/. A session shows the main model's arms
(e.g. B and C of runs-sol-high) next to panel arms of other runs folders (letters, e.g.
L=runs-sol:B, K=runs-sol:C). Items are named "<model>:<arm>": --main names the main model,
and each panel letter takes its runs folder's name. For every pair of items, each session
scores +1 if the first item won, -1 if it lost, 0 for MIXED, SIMILAR or INCONCLUSIVE; topic
means over runs, 95% topic-cluster bootstrap and an exact sign test, as in benchmark_analysis.py.
All pairs are reported alike (no primary contrast, no multiplicity adjustment).

Consistency check (--same-as, --map): the pair of panel arms named in --map is also compared
with the verdict an earlier round gave the same two reports (same topic and run): same
relation, softer (one side MIXED, SIMILAR or INCONCLUSIVE), or reversed.

Usage:
  python3 panel_pairs_analysis.py ../scoring/v4.1-inter/sol-high-vs-low --main sol-high \\
      --same-as ../scoring/v4.1-cross/sol --map K=C,L=B
Writes <root>/analysis.json and prints the table.
"""
import argparse
import glob
import itertools
import json
import os
import random

from benchmark_analysis import SEED, bootstrap, score, sign_test
from inter_analysis import kind
from grading_common import default_model, relations, without_failed
import paths


def sessions(folder, model):
    """(topic, run, entry, relations) for every graded session under folder/run*/, less the verdicts on
    failed jobs; model is the main model of the folder's unlettered arms."""
    for run_dir in sorted(glob.glob(os.path.join(folder, "run*"))):
        key = json.load(open(os.path.join(run_dir, "key.json")))
        for sid, entry in key.items():
            path = os.path.join(run_dir, f"{sid}.md")
            if os.path.exists(path):
                run = next(iter(entry["ids"].values()))["run"]
                yield entry["topic"], run, entry, without_failed(relations(path, entry["ids"]), entry, model)


def item_names(entry, main):
    """{arm letter: "<model>:<arm>"} for one session."""
    panel = entry.get("panel", {})
    names = {}
    for v in entry["ids"].values():
        arm = v["arm"]
        if arm in panel:
            names[arm] = f"{os.path.basename(panel[arm]['root']).removeprefix('runs-')}:{panel[arm]['arm']}"
        else:
            names[arm] = f"{main}:{arm}"
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="folder holding run1..run5")
    ap.add_argument("--main", required=True, help="name of the main model (its runs folder without runs-)")
    ap.add_argument("--same-as", help="earlier grading folder that judged the --map pair on its own")
    ap.add_argument("--map", help="panel letters to that folder's arms, e.g. K=C,L=B")
    a = ap.parse_args()
    rnd = random.Random(SEED)
    earlier = {(t, r): rels for t, r, _, rels in sessions(a.same_as, default_model(a.same_as))} if a.same_as else {}
    mapping = dict(p.split("=") for p in a.map.split(",")) if a.map else {}
    per_pair, order = {}, []
    consistency = {"same": 0, "softer": 0, "reversed": 0, "missing": 0}
    for topic, run, entry, rels in sessions(a.root, a.main):
        names = item_names(entry, a.main)
        arms = sorted(names, key=lambda x: (x in entry.get("panel", {}), x))   # main arms first
        for arm in arms:
            if names[arm] not in order:
                order.append(names[arm])
        for x, y in itertools.combinations(arms, 2):
            s = score(rels.get(tuple(sorted((x, y))), "missing"), x, y)
            if s is not None:
                per_pair.setdefault(f"{names[x]} : {names[y]}", {}).setdefault(topic, []).append(s)
        if mapping:
            (p1, e1), (p2, e2) = mapping.items()
            now = rels.get(tuple(sorted((p1, p2))), "missing")
            if ">" in now:   # "K>L" -> "C>B"; MIXED, SIMILAR, ... stay as they are
                now = ">".join({p1: e1, p2: e2}[arm] for arm in now.split(">"))
            then = earlier.get((topic, run), {}).get(tuple(sorted((e1, e2))), "missing")
            if "missing" in (now, then):
                consistency["missing"] += 1
            elif now == then:
                consistency["same"] += 1
            elif kind(now) == "win" and kind(then) == "win":
                consistency["reversed"] += 1
            else:
                consistency["softer"] += 1
    report = {"items": order, "contrasts": {}}
    if mapping:
        against = os.path.relpath(os.path.abspath(a.same_as), os.path.join(paths.DATA, "scoring"))
        report["consistency"] = {"pair": a.map, "against": against, **consistency}
    for name, topics in per_pair.items():
        means = [sum(v) / len(v) for v in topics.values()]
        low, high, _ = bootstrap(means, rnd)
        pos, neg, p = sign_test(means)
        all_sessions = [s for v in topics.values() for s in v]
        report["contrasts"][name] = {
            "topics": len(means), "sessions": len(all_sessions), "mean": sum(means) / len(means),
            "ci95": [low, high], "wins": all_sessions.count(1), "ties": all_sessions.count(0),
            "losses": all_sessions.count(-1),
            "sign_test": {"topics_above_0": pos, "topics_below_0": neg, "p_two_sided": p},
            "topic_means": {t: round(sum(v) / len(v), 3) for t, v in sorted(topics.items())}}
    with open(os.path.join(a.root, "analysis.json"), "w") as f:
        json.dump(report, f, indent=1)
    for name, r in report["contrasts"].items():
        print(f"{name:28} mean {r['mean']:+.2f}  CI [{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}]  "
              f"W/T/L {r['wins']}/{r['ties']}/{r['losses']}  topics +{r['sign_test']['topics_above_0']}"
              f"/-{r['sign_test']['topics_below_0']}  p {r['sign_test']['p_two_sided']:.3f}")
    if mapping:
        print(f"{a.map} against {a.same_as}:", consistency)


if __name__ == "__main__":
    main()
