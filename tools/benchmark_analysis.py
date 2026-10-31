"""Analyse benchmark round 1 (grader v4.1): does B beat A, and C beat B?

Plan: scoring/v4.0-validation/PLAN.md step 4. Per topic and contrast (B:A, C:B,
C:A) each session scores +1 if the first arm wins, -1 if it loses, 0 for MIXED,
SIMILAR or INCONCLUSIVE; a missing verdict is left out. A topic's score is the
mean over its runs, and the topic means are the units.

- 95% topic-cluster bootstrap interval of the mean (10 000 resamples, fixed seed).
- Primary: B:A and C:B, one-sided bootstrap p (share of resampled means <= 0),
  Holm-adjusted over the two.
- Secondary: exact two-sided sign test over topics (zero means dropped).
- Sensitivity: the same without the topics used to validate grader v4.x
  (draw.json: pilot, consistency, v41_check).

Usage:
  python3 benchmark_analysis.py scoring/v4.1-benchmark
Writes analysis.json and topics.csv into that folder.
"""
import argparse
import csv
import glob
import json
import math
import os
import random
import re

from grading_common import default_model, relations, without_failed
import paths

BENCH = paths.DATA
CONTRASTS = [("B", "A"), ("C", "B"), ("C", "A")]
PRIMARY = [("B", "A"), ("C", "B")]
RESAMPLES = 10_000
SEED = 20261024


def score(rel, x, y):
    """+1 if x won the pair, -1 if y won, 0 otherwise, None if missing."""
    if rel is None or rel in ("missing", "failed job"):
        return None
    if rel == f"{x}>{y}":
        return 1
    if rel == f"{y}>{x}":
        return -1
    return 0


def collect(root):
    """{topic: {contrast: [session scores]}}, plus verdict counts."""
    per_topic, counts = {}, {}
    model = default_model(root)
    for run_dir in sorted(glob.glob(os.path.join(root, "run*"))):
        key = json.load(open(os.path.join(run_dir, "key.json")))
        for sid, entry in key.items():
            path = os.path.join(run_dir, f"{sid}.md")
            graded = relations(path, entry["ids"]) if os.path.exists(path) else {}
            rels = without_failed(graded, entry, model)
            for x, y in CONTRASTS:
                pair = tuple(sorted((x, y)))
                rel = rels.get(pair, "failed job" if pair in graded else "missing")
                c = counts.setdefault(f"{x}:{y}", {})
                label = rel if rel in ("MIXED", "SIMILAR", "INCONCLUSIVE", "missing", "failed job") else (
                    "win" if rel == f"{x}>{y}" else "loss")
                c[label] = c.get(label, 0) + 1
                s = score(rel, x, y)
                if s is not None:
                    per_topic.setdefault(entry["topic"], {}).setdefault(f"{x}:{y}", []).append(s)
    return per_topic, counts


def bootstrap(means, rnd):
    n = len(means)
    stats = sorted(sum(rnd.choice(means) for _ in range(n)) / n for _ in range(RESAMPLES))
    low, high = stats[int(0.025 * RESAMPLES)], stats[int(0.975 * RESAMPLES) - 1]
    p_one_sided = sum(1 for s in stats if s <= 0) / RESAMPLES
    return low, high, p_one_sided


def sign_test(means):
    pos, neg = sum(m > 0 for m in means), sum(m < 0 for m in means)
    n, k = pos + neg, min(pos, neg)
    if n == 0:
        return pos, neg, 1.0
    p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return pos, neg, min(1.0, p)


def holm(pvalues):
    order = sorted(pvalues, key=pvalues.get)
    adjusted, running = {}, 0.0
    for i, name in enumerate(order):
        running = max(running, min(1.0, (len(order) - i) * pvalues[name]))
        adjusted[name] = running
    return adjusted


def analyse(per_topic, topics):
    rnd = random.Random(SEED)
    result = {}
    for x, y in CONTRASTS:
        name = f"{x}:{y}"
        means = [sum(v) / len(v) for t in topics if (v := per_topic.get(t, {}).get(name))]
        low, high, p_boot = bootstrap(means, rnd)
        pos, neg, p_sign = sign_test(means)
        result[name] = {"topics": len(means), "mean": sum(means) / len(means), "ci95": [low, high],
                        "p_bootstrap_one_sided": p_boot,
                        "sign_test": {"topics_above_0": pos, "topics_below_0": neg, "p_two_sided": p_sign}}
    adjusted = holm({f"{x}:{y}": result[f"{x}:{y}"]["p_bootstrap_one_sided"] for x, y in PRIMARY})
    for name, p in adjusted.items():
        result[name]["p_holm"] = p
    return result


def topic_sort_key(t):
    return (t[0], int(re.sub(r"\D", "", t)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="folder holding run1..run5")
    a = ap.parse_args()
    per_topic, counts = collect(a.root)
    draw = json.load(open(os.path.join(paths.INPUTS, "draw.json")))
    validation = {draw["pilot"], *draw["consistency"], *draw["v41_check"]["topics"]}
    all_topics = sorted(per_topic, key=topic_sort_key)
    report = {
        "verdicts": counts,
        "validation_topics": sorted(validation, key=topic_sort_key),
        "all_topics": analyse(per_topic, all_topics),
        "without_validation_topics": analyse(per_topic, [t for t in all_topics if t not in validation]),
    }
    with open(os.path.join(a.root, "analysis.json"), "w") as f:
        json.dump(report, f, indent=1)
    with open(os.path.join(a.root, "topics.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["topic", "validation"] + [f"{x}:{y} mean" for x, y in CONTRASTS]
                   + [f"{x}:{y} sessions" for x, y in CONTRASTS])
        for t in all_topics:
            v = per_topic[t]
            w.writerow([t, t in validation]
                       + [round(sum(v[c]) / len(v[c]), 3) if v.get(c) else "" for c in (f"{x}:{y}" for x, y in CONTRASTS)]
                       + [len(v.get(f"{x}:{y}", [])) for x, y in CONTRASTS])

    for name, c in counts.items():
        print(f"{name} verdicts: " + ", ".join(f"{k} {n}" for k, n in sorted(c.items())))
    for scope in ("all_topics", "without_validation_topics"):
        print(f"\n{scope}")
        for name, r in report[scope].items():
            s = r["sign_test"]
            holm_p = f"  p_holm {r['p_holm']:.4f}" if "p_holm" in r else ""
            print(f"  {name}  n={r['topics']}  mean {r['mean']:+.3f}  95% CI [{r['ci95'][0]:+.3f}, {r['ci95'][1]:+.3f}]"
                  f"  p_boot {r['p_bootstrap_one_sided']:.4f}{holm_p}"
                  f"  sign {s['topics_above_0']}/{s['topics_below_0']} p {s['p_two_sided']:.4f}")


if __name__ == "__main__":
    main()
