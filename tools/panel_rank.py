"""One quality scale for every model x arm (Bradley-Terry), with the median time per report.

Items are "<model>:<arm>" (e.g. sonnet:B). Every v4.1 pairwise verdict on the
cross-model topics feeds one fit: the panel sessions (scoring/v4.1-panel), the
per-model A/B/C rounds (scoring/v4.1-cross/<model>, and Haiku's round 1 restricted
to these topics), and the Sonnet-vs-Haiku sessions (scoring/v4.1-inter).

Rules, fixed before any panel session ran (2026-10-25):
- a win counts 1 for the winner; MIXED, SIMILAR or INCONCLUSIVE count 0.5 each;
  a missing verdict is left out;
- items: the six stage-1 panel models (Haiku, Sonnet, Luna, Sol, Mistral Medium via Vibe,
  GLM-5.3 Flash via Vibe) x A/B/C; Opus joins in stage 2 with Astra and Mistral Large 4;
  2026-10-31: stage 2 (panel_stage2.py, scoring/v4.1-panel2) also adds Sol High, Haiku and Luna
  at xhigh, and the local tiers; the inter folders' own items are now named after their model
  (they had all been read as Haiku's);
- Bradley-Terry strengths by the MM algorithm, each item also holding one virtual
  tie against a fixed reference of strength 1, so an item that wins every
  comparison keeps a finite score;
- score = log strength, centred on the mean item; 95% interval from 1000 topic
  resamples (topic-cluster bootstrap, seed 20261025);
- median time per report from the published runs of run-ledger.jsonl on the same topics, with the RB's median
  time added to every B and C report (Sol High reused Sol's RBs). Prices: report_prices.py.

Usage:
  python3 panel_rank.py
Writes scoring/v4.1-panel/ranking.json and prints the table.
"""
import glob
import json
import math
import os
import random
import statistics

from grading_common import SUPERSEDED, default_model, published_run, relations, without_failed
import paths

BENCH = paths.DATA
SCORING = os.path.join(BENCH, "scoring")
TOPICS = json.load(open(os.path.join(paths.INPUTS, "draw.json")))["cross_model"]["topics"]
SEED = 20261025
MODELS = ("haiku", "sonnet", "luna", "sol", "vibe", "glm-flash",     # stage 1; others would sit off the shared scale
          "opus", "astra", "large4", "sol-high", "haiku-xhigh", "luna-xhigh",                       # stage 2
          "qwen3.5-9b-think", "qwen3.5-4b-think-262k", "gemma-4-12b-guarded")
RB_FROM = {"sol-high": "sol"}   # rounds that reused another model's RBs
TIE = ("MIXED", "SIMILAR", "INCONCLUSIVE")


def item_of(letter, entry, default_model):
    """The model:arm behind a session letter: a panel arm, the older guest arm X, or
    an arm of the round's own model."""
    source = entry.get("panel", {}).get(letter) or (entry.get("guest") if letter == "X" else None)
    if source:
        return f"{os.path.basename(source['root']).removeprefix('runs-')}:{source['arm']}"
    return f"{default_model}:{letter}"


def comparisons():
    """(topic, item1, item2, score of item1) for every verdict on the cross-model topics."""
    sources = [(os.path.join(SCORING, "v4.1-benchmark"), "haiku")]
    sources += [(d, os.path.basename(d)) for d in sorted(glob.glob(os.path.join(SCORING, "v4.1-cross", "*")))
                if os.path.isdir(d)]
    sources += [(d, default_model(d))
                for d in sorted(glob.glob(os.path.join(SCORING, "v4.1-inter", "*"))) if os.path.isdir(d)]
    sources += [(d, None) for d in sorted(glob.glob(os.path.join(SCORING, "v4.1-panel", "*"))) if os.path.isdir(d)]
    sources += [(d, None) for d in sorted(glob.glob(os.path.join(SCORING, "v4.1-panel2", "*"))) if os.path.isdir(d)]
    out = []
    for folder, model in sources:
        if os.path.relpath(folder, SCORING) in SUPERSEDED:
            continue
        for key_path in glob.glob(os.path.join(folder, "run*", "key.json")):
            key = json.load(open(key_path))
            for sid, entry in key.items():
                path = os.path.join(os.path.dirname(key_path), f"{sid}.md")
                if entry["topic"] not in TOPICS or not os.path.exists(path):
                    continue
                for (l1, l2), rel in without_failed(relations(path, entry["ids"]), entry, model).items():
                    i1, i2 = item_of(l1, entry, model), item_of(l2, entry, model)
                    if i1.split(":")[0] not in MODELS or i2.split(":")[0] not in MODELS:
                        continue
                    if rel in TIE:
                        out.append((entry["topic"], i1, i2, 0.5))
                    elif rel == f"{l1}>{l2}":
                        out.append((entry["topic"], i1, i2, 1.0))
                    elif rel == f"{l2}>{l1}":
                        out.append((entry["topic"], i1, i2, 0.0))
    return out


def fit(comps, items):
    strength = {i: 1.0 for i in items}
    wins = {i: 0.5 for i in items}            # the virtual tie against the reference
    games = {}
    for _, a, b, s in comps:
        wins[a] += s
        wins[b] += 1 - s
        games[(a, b)] = games.get((a, b), 0) + 1
    opponents = {i: [] for i in items}
    for (a, b), n in games.items():
        opponents[a].append((b, n))
        opponents[b].append((a, n))
    for _ in range(2000):
        new = {i: wins[i] / (1 / (strength[i] + 1.0) + sum(n / (strength[i] + strength[j]) for j, n in opponents[i]))
               for i in items}
        done = max(abs(math.log(new[i] / strength[i])) for i in items) < 1e-9
        strength = new
        if done:
            break
    logs = {i: math.log(v) for i, v in strength.items()}
    mean = statistics.mean(logs.values())
    return {i: v - mean for i, v in logs.items()}


def times():
    """{item: {"median_minutes"}}, the RB's median time added to B and C."""
    jobs = {}
    for line in open(os.path.join(BENCH, "run-ledger.jsonl")):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        parts = e.get("label", "").split("/")
        if len(parts) != 3 or not published_run(e) or parts[1] not in TOPICS \
                or "attempt" in parts[2] or not e.get("ok"):
            continue
        model = parts[0].removeprefix("research-")
        arm = "RB" if parts[2] == "stage1" else parts[2][0]
        jobs.setdefault((model, arm), []).append((e.get("duration_s") or 0) / 60)
    out = {}
    for (model, arm), minutes in jobs.items():
        if arm == "RB":
            continue
        median = statistics.median(minutes)
        rb = jobs.get((RB_FROM.get(model, model), "RB"))
        if arm in "BC" and rb:
            median += statistics.median(rb)
        out[f"{model}:{arm}"] = {"median_minutes": round(median, 1)}
    return out


def main():
    comps = comparisons()
    items = sorted({c[1] for c in comps} | {c[2] for c in comps})
    scores = fit(comps, items)
    rnd = random.Random(SEED)
    by_topic = {t: [c for c in comps if c[0] == t] for t in TOPICS}
    boots = {i: [] for i in items}
    for _ in range(1000):
        sample = [c for t in (rnd.choice(TOPICS) for _ in TOPICS) for c in by_topic[t]]
        s = fit(sample, items)
        for i in items:
            boots[i].append(s[i])
    extra = times()
    table = []
    for i in sorted(items, key=lambda i: -scores[i]):
        b = sorted(boots[i])
        table.append({"item": i, "score": round(scores[i], 2), "ci95": [round(b[25], 2), round(b[974], 2)],
                      "comparisons": sum(1 for c in comps if i in (c[1], c[2])), **extra.get(i, {})})
    with open(os.path.join(SCORING, "v4.1-panel", "ranking.json"), "w") as f:
        json.dump({"topics": TOPICS, "verdicts": len(comps), "ranking": table}, f, indent=1)
    print(f"{len(comps)} verdicts on {', '.join(TOPICS)}")
    print(f"{'item':28} {'score':>6} {'95% CI':>15} {'n':>5} {'min':>5}")
    for r in table:
        print(f"{r['item']:28} {r['score']:+6.2f} [{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}] {r['comparisons']:5} "
              f"{r.get('median_minutes', '-'):>5}")


if __name__ == "__main__":
    main()
