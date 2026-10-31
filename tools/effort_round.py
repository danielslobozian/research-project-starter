"""Higher-effort B rounds (2026-10-30): RB and B at a raised reasoning level, 5 shared topics.

  python3 effort_round.py haiku --topics T3 --runs 1      # pilot
  python3 effort_round.py haiku                           # full round

Models: haiku (Claude, --effort xhigh), luna (Codex, --effort xhigh), glm-flash (Vibe; the level is
thinking = "max" in ~/.vibe/config.toml, set for this round). Stage 1 first, then arm B only.
Prints EFFORT-DONE <model> or EFFORT-STOP <model> at the end.
"""
import argparse
import os
import subprocess
import sys
import paths

BENCH = paths.DATA
RUNNER = os.path.join(paths.TOOLS, "run_headless.py")
MODELS = {   # name: (runs folder, runner arguments)
    "haiku": ("runs-haiku-xhigh", ["--client", "claude", "--model", "claude-haiku-5-5", "--effort", "xhigh"]),
    "luna": ("runs-luna-xhigh", ["--client", "codex", "--model", "gpt-6-luna", "--effort", "xhigh"]),
    "glm-flash": ("runs-glm-flash-max", ["--client", "vibe", "--model", "zai-glm-5-3-flash"]),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", choices=sorted(MODELS))
    ap.add_argument("--topics", default="T3,T9,T20,S13,S23")
    ap.add_argument("--runs", default="1-5")
    a = ap.parse_args()
    folder, args = MODELS[a.model]
    # mmdc's own puppeteer Chrome has no AppArmor profile on this laptop and cannot start; the installed
    # Google Chrome has one (/etc/apparmor.d/chrome) and runs with its sandbox on.
    os.environ["PUPPETEER_EXECUTABLE_PATH"] = "/opt/google/chrome/chrome"
    base = [sys.executable, "-u", RUNNER, *args, "--root", os.path.join(BENCH, folder), "--topics", a.topics,
            "--parallel", "4"]
    for step in (["--arms", ""], ["--runs", a.runs, "--arms", "B"]):
        rc = subprocess.run(base + step, cwd=BENCH, check=False).returncode
        if rc != 0:
            print(f"EFFORT-STOP {a.model} runner exited with status {rc}", flush=True)
            sys.exit(3)
    print(f"EFFORT-DONE {a.model}", flush=True)


if __name__ == "__main__":
    main()
