"""Pieces shared by the grading and analysis scripts: grader session settings, finding and
blinding a delivered report, reading the judge's pair verdicts from a v4 session, and leaving out
the verdicts on failed jobs (inputs/failed-jobs.json).
"""
import glob
import json
import os
import re

import paths

SCRATCH = (os.environ.get("RPS_TMP") or "/tmp/rps").rstrip("/") + "/bench-grade"
GRADER_TOOLS = "Read Write WebSearch WebFetch"
FOOTER_RE = re.compile(r"^\*Research ID:.*\*\s*$", re.M)
# Working files a job can leave instead of a report (2026-10-31: seven GLM Flash jobs were graded on one).
NOT_REPORT_RE = re.compile(r"(_reply|\.rb|\.working|\.checkpoint[^/]*|working[-.]record|/notes[^/]*|/test)\.md$")
MODELS = json.load(open(os.path.join(paths.INPUTS, "models.json")))["models"]
FAILED = {(j["model"], j["topic"], j["job"])
          for j in json.load(open(os.path.join(paths.INPUTS, "failed-jobs.json")))["jobs"]}
# Grading folders of the superseded no-search 9B round: not published, and left out of every analysis.
SUPERSEDED = ("v4.1-cross/qwen9b", "v4.1-inter/qwen9b-vs-luna")
# The model whose arms an inter folder's unlettered sessions show (compare_v4.py --runs-root); qwen9b-vs-luna
# is the superseded no-search 9B round.
INTER_MAIN = {"sonnet-A": "haiku", "sonnet-B": "haiku", "sonnet-C": "haiku", "haiku-xhigh-vs-haiku": "haiku-xhigh",
              "luna-xhigh-vs-luna": "luna-xhigh", "luna-xhigh-vs-luna-C": "luna-xhigh",
              "luna-xhigh-vs-sol": "luna-xhigh", "sol-high-vs-low": "sol-high", "qwen9b-vs-luna": "qwen9b"}


def report_file(folder):
    """The delivered report: the largest Markdown file that is not the reply, RB, or a working file."""
    mds = [p for p in glob.glob(os.path.join(folder, "*.md")) if not NOT_REPORT_RE.search(p)]
    return max(mds, key=os.path.getsize) if mds else None


def blind(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return FOOTER_RE.sub("", text).strip() + "\n"


def relations(path, ids):
    text = open(path).read()
    block = text[text.rfind('"schema"') - 20:] if '"schema"' in text else text
    start = block.find("{")
    data = None
    for end in range(len(block), start, -1):
        try:
            data = json.loads(block[start:end])
            break
        except ValueError:
            continue
    out = {}
    if not data:
        return out
    for p in data.get("pairs", []):
        a1, a2 = ids.get(p["first"], {}).get("arm"), ids.get(p["second"], {}).get("arm")
        if not a1 or not a2:
            continue
        rel = p["relation"]
        if rel == "FIRST_BETTER":
            rel = f"{a1}>{a2}"
        elif rel == "SECOND_BETTER":
            rel = f"{a2}>{a1}"
        out[tuple(sorted((a1, a2)))] = rel
    return out


def default_model(folder):
    """The model whose arms a grading folder's unlettered sessions show; None for panel folders."""
    folder = os.path.normpath(folder)
    name, parent = os.path.basename(folder), os.path.basename(os.path.dirname(folder))
    if name == "v4.1-benchmark":
        return "haiku"
    if parent == "v4.1-cross":
        return name
    if parent == "v4.1-inter":
        return INTER_MAIN[name]
    return None


def job_of(letter, entry, model):
    """(model, topic, job) of the report a session shows under letter: a panel or guest arm, or an arm of
    the folder's own model."""
    source = entry.get("panel", {}).get(letter) or (entry.get("guest") if letter == "X" else None)
    run = next(v["run"] for v in entry["ids"].values() if v["arm"] == letter)
    if source:
        return os.path.basename(source["root"]).removeprefix("runs-"), entry["topic"], f"{source['arm']}{run}"
    return model, entry["topic"], f"{letter}{run}"


def without_failed(rels, entry, model):
    """The session's pair verdicts, less those involving a failed job's report."""
    return {pair: rel for pair, rel in rels.items()
            if not any(job_of(letter, entry, model) in FAILED for letter in pair)}


def published_run(entry):
    """True for a ledger entry of a published research run: a model of inputs/models.json, and for the local
    models only runs with search tracking (from 2026-10-28), since the earlier no-search rounds used the same
    labels."""
    if entry.get("kind") != "research":
        return False
    model = entry.get("label", "").split("/")[0].removeprefix("research-")
    if model not in MODELS:
        return False
    return MODELS[model]["where"] == "cloud" or "searches" in entry
