"""Record model, duration, token usage and cost of one benchmark run.

Reads a Claude Code agent transcript (JSONL), counts each API message once
(by message id), prices it with benchmark/pricing.json, and appends one JSON
line to benchmark/run-ledger.jsonl.

Usage: python3 run_meta.py --label scoring/v3.1/S3 --kind scoring --log agent.jsonl [--output path]
"""
import argparse
import json
import os
from datetime import datetime
import paths

BENCH = paths.DATA


def summarize(log_path, pricing):
    seen, stamps = {}, []
    with open(log_path) as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("timestamp"):
                stamps.append(rec["timestamp"])
            msg = rec.get("message") or {}
            if msg.get("usage") and msg.get("id"):
                seen[msg["id"]] = (msg.get("model"), msg["usage"])
    tokens = {"input": 0, "output": 0, "cache_write_5m": 0, "cache_write_1h": 0, "cache_read": 0}
    cost, models = 0.0, {}
    for model, u in seen.values():
        cw = u.get("cache_creation") or {}
        t = {
            "input": u.get("input_tokens", 0),
            "output": u.get("output_tokens", 0),
            "cache_write_5m": cw.get("ephemeral_5m_input_tokens", u.get("cache_creation_input_tokens", 0) if not cw else 0),
            "cache_write_1h": cw.get("ephemeral_1h_input_tokens", 0),
            "cache_read": u.get("cache_read_input_tokens", 0),
        }
        models[model] = models.get(model, 0) + 1
        price = pricing.get(model)
        for k, v in t.items():
            tokens[k] += v
            if price:
                cost += v * price[k] / 1e6
    start, end = min(stamps), max(stamps)
    dur = (datetime.fromisoformat(end.replace("Z", "+00:00")) - datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds()
    unpriced = [m for m in models if m not in pricing]
    return {
        "models": models,
        "api_calls": len(seen),
        "start": start,
        "end": end,
        "duration_s": round(dur),
        "tokens": tokens,
        "cost_usd": round(cost, 4),
        "cost_note": "list-price estimate from pricing.json" + (f"; unpriced models: {unpriced}" if unpriced else ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--kind", required=True, choices=["research", "scoring", "synthesis"])
    ap.add_argument("--log", required=True)
    ap.add_argument("--output")
    ap.add_argument("--ledger", default=os.path.join(BENCH, "run-ledger.jsonl"))
    a = ap.parse_args()
    pricing = json.load(open(os.path.join(paths.INPUTS, "pricing.json")))
    out = os.path.relpath(a.output, BENCH) if a.output else None
    entry = {"label": a.label, "kind": a.kind, "output": out, **summarize(a.log, pricing)}
    with open(a.ledger, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(entry))


if __name__ == "__main__":
    main()
