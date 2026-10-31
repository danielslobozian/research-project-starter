"""Set aside finished jobs that failed, so a rerun redoes them.

For every <root>/<topic>/<arm><n>/ with a _meta file whose task lacks its mandatory result (mandatory.py:
the report, for C also the companion, or a job the runner stopped), after rescue_misplaced.py has had its chance, moves the folder and its _meta file into
<root>/<label>/ and appends the list to <root>/NOTES.md. Prints the count. The caller then
reruns run_headless.py with the same arguments; finished jobs are skipped.

Usage:
  python3 rerun_reportless.py ../runs-glm-flash early-stop-2026-10-27
"""
import argparse
import datetime
import glob
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json  # noqa: E402
import mandatory  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("label")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    name = os.path.basename(root).removeprefix("runs-")
    moved = []
    for meta in sorted(glob.glob(os.path.join(root, "_meta", f"research-{name}_*_[ABC][0-9]*.json"))):
        tid, label = os.path.basename(meta)[:-5].split("_")[-2:]
        if "." in label:
            continue
        delivery = os.path.join(root, tid, label)
        if not mandatory.missing(label[0], delivery, json.load(open(meta))):
            continue
        dest = os.path.join(root, a.label, tid)
        os.makedirs(os.path.join(root, a.label, "_meta"), exist_ok=True)
        os.makedirs(dest, exist_ok=True)
        # a task set aside twice under the same label (two passes on one day) keeps both attempts
        k, suffix = 1, ""
        while os.path.exists(os.path.join(dest, label + suffix)) or os.path.exists(
                os.path.join(root, a.label, "_meta", os.path.basename(meta)[:-5] + suffix + ".json")):
            k += 1
            suffix = f".attempt{k}"
        if os.path.isdir(delivery):
            shutil.move(delivery, os.path.join(dest, label + suffix))
        shutil.move(meta, os.path.join(root, a.label, "_meta", os.path.basename(meta)[:-5] + suffix + ".json"))
        moved.append(f"{tid}/{label}")
    if moved:
        with open(os.path.join(root, "NOTES.md"), "a") as f:
            f.write(f"\n## Jobs without a report set aside for rerun ({datetime.date.today()}, rerun_reportless.py)\n\n"
                    f"{len(moved)} jobs moved to {a.label}/: {', '.join(moved)}\n")
    print(f"set aside {len(moved)}: {moved}")


if __name__ == "__main__":
    main()
