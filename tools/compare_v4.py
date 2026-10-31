"""Side-by-side grading with v4.0: one session per topic and presentation order.

Each session sees one topic's A/B/C reports (runs from draw.json), blinded,
under fresh random IDs, in an order fixed here: with --orders all, every one
of the 6 orders once (or a number of random orders). With --reference, the
topic's GPT 6 Pro report from $RPS_DATA/reference-reports/ joins as arm P. With --guest,
one arm of another model's runs (same run number) joins as arm X; with --panel,
any arms of any models' runs join under letters of your choice. The key
(session -> ID -> arm, run, position) is written to <root>/key.json and never
enters a session. Each session sees only its own
scratch folder. Every session is appended to run-ledger.jsonl.

Usage:
  python3 compare_v4.py --topics G1,G2 --reference inputs/gold-draw.json --runs-root runs-gold \
      --orders 1 --root scoring/v4.0-validation/gold
  python3 compare_v4.py --topics T22 --draw scoring/v4.0-validation/draw.json \
      --root scoring/v4.0-validation/step1
  python3 compare_v4.py --topics T3 --run 1 --guest ../runs-sonnet:A --orders 1 \
      --root scoring/v4.1-inter/sonnet-A/run1
  python3 compare_v4.py --topics T3 --run 1 --arms '' --orders 1 \
      --panel H=../runs-haiku:B,S=../runs-sonnet:B,O=../runs-opus:B,L=../runs-luna:B \
      --root scoring/v4.1-panel/B/run1
"""
import argparse
import itertools
import json
import os
import secrets
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_headless as rh  # noqa: E402
from grading_common import GRADER_TOOLS, SCRATCH, blind, report_file  # noqa: E402
import paths  # noqa: E402

RESULTS = os.path.join(paths.DATA_ROOT, "reference-reports")
KEY_LOCK = threading.Lock()   # sessions run in threads and share the key file
panel = {}   # letter -> {"root", "arm"}: an arm of some model's runs (--guest is panel X)


def session(root, topic, k, order, runs, runs_root, question, model, prompt_file, key):
    sid = f"{topic}-o{k}"
    out = os.path.join(root, f"{sid}.md")
    if os.path.exists(out):
        return
    if not rh.wait_if_paused():         # waits out a usage limit; False once a weekly limit ends the batch
        return
    folder = os.path.abspath(root)   # unique per model and run: .../<model>/run<k>
    cwd = os.path.join(SCRATCH, f"v4-{os.path.basename(os.path.dirname(folder))}-{os.path.basename(folder)}-{sid}")
    shutil.rmtree(cwd, ignore_errors=True)
    os.makedirs(cwd)
    shutil.copyfile(prompt_file, os.path.join(cwd, "instructions.md"))
    ids, paths = {}, []
    for pos, arm in enumerate(order, 1):
        rid = "R" + secrets.token_hex(3)
        if arm == "P":   # reference report (GPT 6 Pro, engine v1.4) from $RPS_DATA/reference-reports/
            src = os.path.join(RESULTS, runs["P"], runs["P"] + ".md")
        elif arm in panel:
            src = report_file(os.path.join(panel[arm]["root"], topic, f"{panel[arm]['arm']}{runs[arm]}"))
        else:
            src = report_file(os.path.join(runs_root, topic, f"{arm}{runs[arm]}"))
        p = os.path.join(cwd, f"{rid}.md")
        with open(p, "w") as f:
            f.write(blind(open(src).read()))
        ids[rid] = {"arm": arm, "run": runs.get(arm), "position": pos}
        paths.append(p)
    key[sid] = {"topic": topic, "order": "".join(order), "ids": ids}
    if any(arm in panel for arm in order):
        key[sid]["panel"] = {arm: panel[arm] for arm in order if arm in panel}
    with KEY_LOCK, open(os.path.join(root, "key.json"), "w") as f:
        json.dump(key, f, indent=1)
    prompt = f"""Follow the assessment instructions in {cwd}/instructions.md exactly.

Reports (in this presentation order): {", ".join(paths)}
Original research question: "{question}"
Reader profile: default (research reader).
Output path: {cwd}/assessment.md

{rh.NO_SUBAGENTS} Write no other files, except scratch files under {cwd}/."""
    res = rh.claude(prompt, cwd, [], model, tools=GRADER_TOOLS)
    if os.path.exists(os.path.join(cwd, "assessment.md")):
        shutil.copyfile(os.path.join(cwd, "assessment.md"), out)
    if rh.limit_hit(res, root):
        rh.log(root, f"{sid} interrupted by usage limit; will retry")
        return session(root, topic, k, order, runs, runs_root, question, model, prompt_file, key)
    entry = rh.record(root, f"compare-v4.0/{sid}", out, res, [res], kind="grading")
    rh.log(root, f"{sid} {''.join(order)} {'ok' if entry['ok'] and os.path.exists(out) else 'ERROR'} "
                 f"{res['wall_s']}s ${entry.get('cost_usd', '?')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", required=True)
    ap.add_argument("--draw", help="JSON with runs per topic and arm (else --run for every arm)")
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--arms", default="ABC")
    ap.add_argument("--reference", help="gold-draw.json: adds the reference report as arm P")
    ap.add_argument("--guest", help="<runs folder>:<arm>, e.g. ../runs-sonnet:A; adds that arm as X")
    ap.add_argument("--panel", help="<letter>=<runs folder>:<arm>,... e.g. H=../runs-haiku:B,S=../runs-sonnet:B")
    ap.add_argument("--orders", default="all", help="'all' for every order, or a number of random orders")
    ap.add_argument("--parallel", type=int, default=6)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--prompt", default=paths.GRADER)
    ap.add_argument("--runs-root", default=os.path.join(rh.BENCH, "runs-haiku"))
    ap.add_argument("--root", required=True)
    ap.add_argument("--pace-usd-per-hour", type=float)
    ap.add_argument("--budget-usd", type=float)
    a = ap.parse_args()
    os.makedirs(a.root, exist_ok=True)
    topics = rh.load_topics()
    names = a.topics.split(",")
    runs = json.load(open(a.draw))["runs"] if a.draw else {t: {arm: a.run for arm in a.arms} for t in names}
    arms = a.arms
    if a.reference:
        for t, folder, _ in json.load(open(a.reference))["topics"]:
            if t in runs:
                runs[t]["P"] = folder
        arms += "P"
    specs = ([f"X={a.guest}"] if a.guest else []) + (a.panel.split(",") if a.panel else [])
    for spec in specs:
        letter, _, source = spec.partition("=")
        root_, _, arm_ = source.rpartition(":")
        assert len(letter) == 1 and letter not in arms, spec
        panel[letter] = {"root": os.path.abspath(root_), "arm": arm_}
        for t in names:
            runs[t][letter] = a.run
        arms += letter
    perms = list(itertools.permutations(arms))
    key_path = os.path.join(a.root, "key.json")
    key = json.load(open(key_path)) if os.path.exists(key_path) else {}
    rh.spent["budget"] = a.budget_usd
    rh.pace.update(usd_per_hour=a.pace_usd_per_hour, start=__import__("time").time())
    rh.log(a.root, f"start prompt={os.path.basename(a.prompt)} topics={a.topics} orders={a.orders} model={a.model}")
    rnd = __import__("random").SystemRandom()
    jobs = [(t, k, o) for t in names
            for k, o in enumerate(perms if a.orders == "all" else rnd.sample(perms, int(a.orders)), 1)]
    with ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for j in [pool.submit(session, a.root, t, k, o, runs[t], a.runs_root, topics[t], a.model, a.prompt, key)
                  for t, k, o in jobs]:
            j.result()
    with open(key_path, "w") as f:
        json.dump(key, f, indent=1)
    rh.log(a.root, f"done, spent ${rh.spent['usd']:.2f}")


if __name__ == "__main__":
    main()
