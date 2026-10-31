"""Research effort per model and arm, from run-ledger.jsonl: time, steps, tokens, cost.

Counts only finished research jobs (ok, not a limit attempt) on the given topics.
Steps are model calls for Claude, completed items for Codex, assistant messages and
tool calls for Vibe: comparable in scale, not identical. Tokens: Claude input
includes cache writes and reads; Codex input includes its cached input. Vibe
reports no tokens and neither Codex nor Vibe reports a cost.

Usage:
  python3 model_usage.py --topics T3,T9,T20,S13,S23 haiku sonnet luna vibe
Writes scoring/v4.1-cross/usage.json and prints a table.
"""
import argparse
import collections
import json
import os
import statistics
import paths

BENCH = paths.DATA
ARMS = ["RB", "A", "B", "C"]


def tokens(entry):
    t = entry.get("tokens") or {}
    if "input_tokens" in t:   # Codex
        return t["input_tokens"], t.get("output_tokens", 0)   # reasoning is already inside output_tokens
    if t:                     # Claude
        return (t.get("input", 0) + t.get("cache_write_5m", 0) + t.get("cache_write_1h", 0)
                + t.get("cache_read", 0)), t.get("output", 0)
    return None, None


def collect(model, topics):
    jobs = collections.defaultdict(list)
    for line in open(os.path.join(BENCH, "run-ledger.jsonl")):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        parts = e.get("label", "").split("/")
        if (len(parts) != 3 or parts[0] != f"research-{model}" or parts[1] not in topics
                or "limit-attempt" in parts[2] or not e.get("ok")):
            continue
        jobs["RB" if parts[2] == "stage1" else parts[2][0]].append(e)
    return jobs


def summarise(entries):
    tin, tout = zip(*(tokens(e) for e in entries))
    known = [i for i in tin if i is not None]
    costs = [e["cost_usd"] for e in entries if e.get("cost_usd") is not None]
    return {
        "jobs": len(entries),
        "median_minutes": round(statistics.median(e.get("duration_s") or 0 for e in entries) / 60, 1),
        "median_steps": statistics.median(e.get("steps") or e.get("api_calls") or 0 for e in entries),
        "median_input_tokens": round(statistics.median(known)) if known else None,
        "median_output_tokens": round(statistics.median(o for o in tout if o is not None)) if known else None,
        "cost_usd_total": round(sum(costs), 2) if costs else None,
        "cost_usd_median": round(statistics.median(costs), 3) if costs else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", required=True)
    ap.add_argument("models", nargs="+", help="ledger names: research-<model>/...")
    a = ap.parse_args()
    topics = set(a.topics.split(","))
    report = {}
    for model in a.models:
        jobs = collect(model, topics)
        report[model] = {arm: summarise(jobs[arm]) for arm in ARMS if jobs[arm]}
    out = os.path.join(BENCH, "scoring", "v4.1-cross", "usage.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"topics": sorted(topics), "models": report}, f, indent=1)
    print(f"{'model':8} {'arm':3} {'jobs':>4} {'min':>5} {'steps':>6} {'in tok':>10} {'out tok':>8} {'$ total':>8}")
    for model, arms in report.items():
        for arm, s in arms.items():
            fmt = lambda v, w: f"{v:>{w}}" if v is not None else f"{'-':>{w}}"
            print(f"{model:8} {arm:3} {s['jobs']:>4} {s['median_minutes']:>5} {s['median_steps']:>6} "
                  f"{fmt(s['median_input_tokens'], 10)} {fmt(s['median_output_tokens'], 8)} {fmt(s['cost_usd_total'], 8)}")


if __name__ == "__main__":
    main()
