"""Grade a higher-effort B round against the model's default-effort B (2-report sessions), runs 1-5.

  python3 grade_effort.py luna-xhigh luna       # runs-luna-xhigh B vs runs-luna B
  python3 grade_effort.py luna-xhigh luna C     # runs-luna-xhigh B vs runs-luna C
Writes scoring/v4.1-inter/<new>-vs-<old>[-<arm>]/run<k> and runs panel_pairs_analysis.py at the end.
"""
import os
import subprocess
import sys
import paths

BENCH = paths.DATA
PROMPT = paths.GRADER
new, old = sys.argv[1], sys.argv[2]
old_arm = sys.argv[3] if len(sys.argv) > 3 else "B"
root = os.path.join(BENCH, "scoring", "v4.1-inter", f"{new}-vs-{old}" + ("" if old_arm == "B" else f"-{old_arm}"))
for k in range(1, 6):
    subprocess.run([sys.executable, os.path.join(paths.TOOLS, "compare_v4.py"), "--topics", "T3,T9,T20,S13,S23",
                    "--run", str(k), "--arms", "B", "--runs-root", os.path.join(BENCH, f"runs-{new}"),
                    "--panel", f"L={os.path.join(BENCH, f'runs-{old}')}:{old_arm}", "--root", os.path.join(root, f"run{k}"),
                    "--orders", "1", "--prompt", PROMPT, "--parallel", "6", "--pace-usd-per-hour", "28"],
                   cwd=BENCH, check=False)
subprocess.run([sys.executable, os.path.join(paths.TOOLS, "panel_pairs_analysis.py"), root, "--main", new],
               cwd=paths.TOOLS, check=False)
print("GRADE-DONE", new, flush=True)
