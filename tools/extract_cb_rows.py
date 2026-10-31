"""Extract the judge's C-vs-B pair rows (relation + decisive differences) from v4.1 grading sessions.

Writes one JSONL line per session: model, topic, run, verdict from C's side (win/loss/tie), and the row text.
"""
import glob
import json
import os
import re
import sys
import paths

SCORING = os.path.join(paths.DATA, "scoring")
SOURCES = {   # model: (folder, arm letter for "B", arm letter for "C")
    "sol": ("v4.1-cross/sol", "B", "C"), "astra": ("v4.1-cross/astra", "B", "C"),
    "sol-high": ("v4.1-inter/sol-high-vs-low", "B", "C"),
    "opus": ("v4.1-cross/opus", "B", "C"), "large4": ("v4.1-cross/large4", "B", "C"),
    "sonnet": ("v4.1-cross/sonnet", "B", "C"), "vibe": ("v4.1-cross/vibe", "B", "C"),
}



def verdict_json(text):
    block = text[text.rfind('"schema"') - 20:] if '"schema"' in text else text
    start = block.find("{")
    for end in range(len(block), start, -1):
        try:
            return json.loads(block[start:end])
        except ValueError:
            continue
    return None


def relabel(text, label):
    """Replace report ids, and unambiguous id prefixes such as "Rc", by B, C or other."""
    def sub(m):
        hits = {lab for rid, lab in label.items() if rid.startswith(m[0])}
        return hits.pop() if len(hits) == 1 else m[0]
    return re.sub(r"\bR[0-9a-f]{1,6}\b", sub, text)


out = open(sys.argv[1], "w")
for model, (folder, b, c) in SOURCES.items():
    for key_path in sorted(glob.glob(os.path.join(SCORING, folder, "run*", "key.json"))):
        key = json.load(open(key_path))
        for sid, entry in key.items():
            path = os.path.join(os.path.dirname(key_path), f"{sid}.md")
            if not os.path.exists(path):
                continue
            arm = {r: v["arm"] for r, v in entry["ids"].items()}
            run = next(iter(entry["ids"].values()))["run"]
            data = verdict_json(open(path).read())
            label = {r: {b: "B", c: "C"}.get(a, "other") for r, a in arm.items()}
            for p in (data or {}).get("pairs", []):
                if {arm.get(p["first"]), arm.get(p["second"])} != {b, c}:
                    continue
                first_is_c = arm[p["first"]] == c
                rel = p["relation"]
                verdict = ("win" if (rel == "FIRST_BETTER") == first_is_c else "loss") \
                    if rel in ("FIRST_BETTER", "SECOND_BETTER") else "tie"
                reasons = [relabel(t, label) for t in p.get("decisive_reasons", [])]
                out.write(json.dumps({"model": model, "topic": entry["topic"], "run": run,
                                      "c_verdict": verdict, "relation": rel, "reasons": reasons}) + "\n")
