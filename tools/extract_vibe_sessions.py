"""Copy what the price tool needs from Mistral Vibe's local session logs into the edition's data.

Vibe keeps one folder per session under ~/.vibe/logs/session/unified/ (meta.json: model, working directory,
start and end; journal/*.jsonl: every model call's token usage). This writes one line per session to
$RPS_DATA/benchmarks/<edition>/vibe-sessions.jsonl, so the prices no longer depend on Vibe keeping its logs:
session id, billed model, working directory, start, end, and tokens (cached input, other input, output).

Usage:
  python3 extract_vibe_sessions.py [--logs ~/.vibe/logs/session/unified]
"""
import argparse
import glob
import json
import os

import paths


def usage(session_dir):
    """Token totals over the session's journal; a call's usage is counted once even if journaled twice."""
    cached = other = output = 0
    seen = set()

    def walk(x):
        nonlocal cached, other, output
        if isinstance(x, dict):
            u = x.get("usage")
            if isinstance(u, dict) and "input_tokens" in u:
                key = json.dumps(u, sort_keys=True) + str(x.get("id", ""))
                if key not in seen:
                    seen.add(key)
                    c = u.get("cached_input_tokens") or 0
                    cached += c
                    other += (u.get("input_tokens") or 0) - c
                    output += u.get("output_tokens") or 0
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for journal in sorted(glob.glob(os.path.join(session_dir, "journal", "*.jsonl"))):
        for line in open(journal):
            try:
                walk(json.loads(line))
            except ValueError:
                continue
    return cached, other, output


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", default=os.path.expanduser("~/.vibe/logs/session/unified"))
    a = ap.parse_args()
    out = os.path.join(paths.DATA, "vibe-sessions.jsonl")
    n = 0
    with open(out, "w") as f:
        for meta_path in sorted(glob.glob(os.path.join(a.logs, "*", "meta.json"))):
            meta = json.load(open(meta_path))
            cached, other, output = usage(os.path.dirname(meta_path))
            f.write(json.dumps({
                "session": meta["session_id"],
                # sessions before Vibe recorded the model ran its default, Mistral Medium (billed as below)
                "model": (meta.get("config") or {}).get("model_name") or "mistral-vibe-cli-latest",
                "workdir": (meta.get("environment") or {}).get("working_directory", ""),
                "start": meta.get("start_time"), "end": meta.get("end_time"),
                "tokens": {"cached_input": cached, "input": other, "output": output}}) + "\n")
            n += 1
    print(f"{n} sessions -> {out}")


if __name__ == "__main__":
    main()
