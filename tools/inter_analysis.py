"""Analyse inter-model grading: one guest-model arm (X) against Haiku's A, B, C.

Folder layout (compare_v4.py --guest): <root>/<guest>-<arm>/run<k>/. Per guest arm
and Haiku arm, each session scores +1 if X won, -1 if it lost, 0 for MIXED,
SIMILAR or INCONCLUSIVE; topic means over runs, 95% topic-cluster bootstrap and an
exact sign test, as in benchmark_analysis.py.

Consistency check: the same sessions also judge Haiku's A, B and C against each
other. Each such verdict is compared with round 1's verdict for the same topic and
run (scoring/v4.1-benchmark): same relation, softer (one side MIXED or SIMILAR),
or reversed.

Usage:
  python3 inter_analysis.py ../scoring/v4.1-inter sonnet
Writes <root>/<guest>-analysis.json and prints the tables.
"""
import argparse
import glob
import json
import os
import random

from benchmark_analysis import SEED, bootstrap, score, sign_test
from grading_common import relations, without_failed
import paths

BENCH = paths.DATA
ROUND1 = os.path.join(BENCH, "scoring", "v4.1-benchmark")
HAIKU_PAIRS = [("B", "A"), ("C", "B"), ("C", "A")]


def sessions(folder):
    """(topic, run, relations) for every graded session under folder/run*/."""
    for run_dir in sorted(glob.glob(os.path.join(folder, "run*"))):
        key = json.load(open(os.path.join(run_dir, "key.json")))
        for sid, entry in key.items():
            path = os.path.join(run_dir, f"{sid}.md")
            if os.path.exists(path):
                run = next(v["run"] for v in entry["ids"].values() if v["arm"] == "A")
                yield entry["topic"], run, without_failed(relations(path, entry["ids"]), entry, "haiku")


def round1():
    out = {}
    for topic, run, rels in sessions(ROUND1):
        out[(topic, run)] = rels
    return out


def kind(rel):
    return "win" if ">" in rel else "tie" if rel in ("MIXED", "SIMILAR", "INCONCLUSIVE") else "missing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("guest")
    a = ap.parse_args()
    rnd = random.Random(SEED)
    first = round1()
    report = {"contrasts": {}, "consistency": {"same": 0, "softer": 0, "reversed": 0, "missing": 0}}
    for guest_arm in "ABC":
        folder = os.path.join(a.root, f"{a.guest}-{guest_arm}")
        per_topic = {}
        for topic, run, rels in sessions(folder):
            for h in "ABC":
                s = score(rels.get(tuple(sorted(("X", h))), "missing"), "X", h)
                if s is not None:
                    per_topic.setdefault(f"{a.guest} {guest_arm} : haiku {h}", {}).setdefault(topic, []).append(s)
            for x, y in HAIKU_PAIRS:
                now = rels.get(tuple(sorted((x, y))), "missing")
                then = first.get((topic, run), {}).get(tuple(sorted((x, y))), "missing")
                c = report["consistency"]
                if "missing" in (now, then):
                    c["missing"] += 1
                elif now == then:
                    c["same"] += 1
                elif kind(now) == "win" and kind(then) == "win":
                    c["reversed"] += 1
                else:
                    c["softer"] += 1
        for name, topics in per_topic.items():
            means = [sum(v) / len(v) for v in topics.values()]
            low, high, _ = bootstrap(means, rnd)
            pos, neg, p = sign_test(means)
            sessions_all = [s for v in topics.values() for s in v]
            report["contrasts"][name] = {
                "topics": len(means), "sessions": len(sessions_all), "mean": sum(means) / len(means),
                "ci95": [low, high], "wins": sessions_all.count(1), "ties": sessions_all.count(0),
                "losses": sessions_all.count(-1),
                "sign_test": {"topics_above_0": pos, "topics_below_0": neg, "p_two_sided": p},
                "topic_means": {t: round(sum(v) / len(v), 3) for t, v in sorted(topics.items())}}
    with open(os.path.join(a.root, f"{a.guest}-analysis.json"), "w") as f:
        json.dump(report, f, indent=1)
    for name, r in report["contrasts"].items():
        print(f"{name:22} mean {r['mean']:+.2f}  CI [{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}]  "
              f"W/T/L {r['wins']}/{r['ties']}/{r['losses']}  topics +{r['sign_test']['topics_above_0']}"
              f"/-{r['sign_test']['topics_below_0']}")
    print("haiku-vs-haiku against round 1:", report["consistency"])


if __name__ == "__main__":
    main()
