"""Build an edition's release archive from its data: every run's delivery and every grading session of the
published rounds, plus the inputs of the price tool, with private paths and names replaced.

Selection (from $RPS_DATA/benchmarks/<edition>/):
- runs-<model>/ for every model of inputs/models.json and the published failed round (FAILED_ROUNDS), with
  the model's own failures (set-aside folders, failed attempts); folders of runs that failed on the harness,
  not the model (HARNESS_FAILURES), are left out;
- scoring/: the v4.1 grading folders the results come from;
- the published run ledger (run-ledger.jsonl, as the tools expect it);
- the price tool's inputs: vibe-sessions.jsonl and lab/ (GPU power, model requests, search calls), reduced to
  the fields report_prices.py reads.

Every text file is rewritten with the replacements of $RPS_DATA/private-replacements.json (names, paths,
host names; kept out of the repository) and the generic ones below; text files inside zip archives too. Run
check_private.py on the archive afterwards.

Usage:
  python3 build_release.py
Writes $RPS_DATA/release/<edition>/benchmark-<edition>.zip (and its staging folder next to it).
"""
import collections
import io
import json
import os
import re
import shutil
import zipfile

from grading_common import SUPERSEDED
import paths

MODELS = json.load(open(os.path.join(paths.INPUTS, "models.json")))["models"]
FAILED_ROUNDS = ("glm-flash-max",)   # published as a failure: stopped as unstable
HARNESS_FAILURES = re.compile(r"(nosearch|degraded-search|no-doctools|env-missing|invalid-model-fallback|"
                              r"failed-before-2026-10-29|interrupted|contaminated)")
GRADING = ["v4.1-benchmark", "v4.1-cross", "v4.1-inter", "v4.1-panel", "v4.1-panel2"]
# PDFs a model rendered with its sandbox path printed in them: their text cannot be rewritten, so they are left
# out (their Markdown report, the graded file, stays) and REDACTED.md lists them.
REDACTED = {"runs-gemma-4-12b-guarded/T20/C2/sitting-vs-smoking.pdf",
            "runs-glm-flash/S26/B5/ego-depletion-willpower-resource.pdf"}
GENERIC = [(re.compile(r"/tmp/claude-\d+/bench-(?:jobs|p2)"), "<jobs>"),
           (re.compile(r"/tmp/claude-\d+(?:/[^\s\"'`)\]\\]*)?"), "<tmp>"),   # stops at a backslash: JSON escapes
           (re.compile(r"/tmp/(?:gmlc)-[A-Za-z0-9_]+"), "<tmp>"),
           (re.compile(r"/home/[a-z_][a-z0-9_-]*"), "<home>")]
TEXT_EXT = {".md", ".json", ".jsonl", ".txt", ".log", ".csv", ".yml", ".yaml", ".py", ".sh", ".html", ".svg",
            ".tex", ".bib", ".mmd", ".js", ".css", ".xml", ""}

counts = collections.Counter()


def scrub(text, private):
    for old, new in private:
        if old in text:
            counts[f"literal #{private.index((old, new)) + 1}"] += text.count(old)
            text = text.replace(old, new)
    for rx, new in GENERIC:
        text, n = rx.subn(new, text)
        if n:
            counts[f"generic {new}"] += n
    return text


def as_text(data):
    if b"\0" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def copy_file(src, dst, private):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    ext = os.path.splitext(src)[1].lower()
    data = open(src, "rb").read()
    if ext == ".zip":
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                member = zin.read(item.filename)
                text = as_text(member) if os.path.splitext(item.filename)[1].lower() in TEXT_EXT else None
                zout.writestr(item, scrub(text, private).encode() if text is not None else member)
        data = out.getvalue()
    elif ext in TEXT_EXT:
        text = as_text(data)
        if text is not None:
            data = scrub(text, private).encode()
    with open(dst, "wb") as f:
        f.write(data)


def copy_tree(src, dst, private, skip=None):
    for d, dirs, files in os.walk(src):
        dirs[:] = sorted(x for x in dirs if not (skip and skip.search(x)) and x != "__pycache__")
        for f in sorted(files):
            if os.path.relpath(os.path.join(d, f), paths.DATA) in REDACTED:
                continue
            copy_file(os.path.join(d, f), os.path.join(dst, os.path.relpath(os.path.join(d, f), src)), private)


def price_inputs(stage, private):
    """vibe-sessions.jsonl and lab/, reduced to what report_prices.py reads."""
    with open(os.path.join(stage, "vibe-sessions.jsonl"), "w") as out:
        for line in open(os.path.join(paths.DATA, "vibe-sessions.jsonl")):
            s = json.loads(line)
            s["workdir"] = scrub(s["workdir"], private)
            out.write(json.dumps(s) + "\n")
    lab = os.path.join(paths.DATA, "lab")
    for sub, keep in (("health", None), ("llm", ("preset", "model", "start", "end", "pp_tok", "gen_tok", "ctx")),
                      ("search", ("t", "ns", "q", "params", "status", "seconds", "results_per_engine", "failed"))):
        os.makedirs(os.path.join(stage, "lab", sub), exist_ok=True)
        for name in sorted(os.listdir(os.path.join(lab, sub))):
            with open(os.path.join(stage, "lab", sub, name), "w") as out:
                for line in open(os.path.join(lab, sub, name)):
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    if sub == "health":   # the GPU only: time, name, power, use, temperatures
                        r = {"ts": r["ts"], "gpus": [{k: g.get(k) for k in ("name", "power_w", "usage", "temp",
                                                                              "vram_temp")} for g in r.get("gpus") or []]}
                    else:
                        r = {k: r[k] for k in keep if k in r}
                    out.write(scrub(json.dumps(r), private) + "\n")


def main():
    private = [tuple(p) for p in json.load(open(os.path.join(paths.DATA_ROOT, "private-replacements.json")))["replace"]]
    out_dir = os.path.join(paths.DATA_ROOT, "release", paths.EDITION)
    stage = os.path.join(out_dir, "staging", f"benchmark-{paths.EDITION}")
    shutil.rmtree(os.path.dirname(stage), ignore_errors=True)
    for model in list(MODELS) + list(FAILED_ROUNDS):
        copy_tree(os.path.join(paths.DATA, f"runs-{model}"), os.path.join(stage, f"runs-{model}"), private,
                  skip=HARNESS_FAILURES)
    for name in GRADING:
        src = os.path.join(paths.DATA, "scoring", name)
        for sub in sorted(os.listdir(src)):
            if f"{name}/{sub}" in SUPERSEDED:
                continue
            path = os.path.join(src, sub)
            dst = os.path.join(stage, "scoring", name, sub)
            if os.path.isdir(path):
                copy_tree(path, dst, private)
            else:
                copy_file(path, dst, private)
    price_inputs(stage, private)
    shutil.copyfile(os.path.join(paths.REPO, "benchmarks", paths.EDITION, "ledger.jsonl"),
                    os.path.join(stage, "run-ledger.jsonl"))   # the published ledger, for the tools
    with open(os.path.join(stage, "REDACTED.md"), "w") as f:
        f.write("# Files left out\n\nThese PDFs, rendered by the model, print the job's sandbox path; PDF text "
                "cannot be rewritten, so they are not in this archive. The Markdown report next to each, the file "
                "that was graded, is.\n\n" + "".join(f"- `{p}`\n" for p in sorted(REDACTED)))
    archive = os.path.join(out_dir, f"benchmark-{paths.EDITION}.zip")
    if os.path.exists(archive):
        os.remove(archive)
    shutil.make_archive(archive[:-4], "zip", os.path.dirname(stage), os.path.basename(stage))
    files = sum(len(f) for _, _, f in os.walk(stage))
    print(f"{files} files -> {archive} ({os.path.getsize(archive) / 1e6:.0f} MB)")
    for rule, n in sorted(counts.items()):
        print(f"  replaced {n:6} x {rule}")


if __name__ == "__main__":
    main()
