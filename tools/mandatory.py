"""Each task's mandatory result (rule since 2026-10-29). A task whose result is missing has failed, whatever the
model said it did.

- stage 1: the RB file, named `<report_basename>.rb.md` after the slug in its own front matter (the protocol:
  "The initial file is `<topic-slug>.rb.md`; the first report uses the same slug") — rb_name_problem();
- A and B: the Markdown report (the prompt asks for "a report as a Markdown file");
- C: the Markdown report and the companion `<slug>.analysis.json`, valid JSON (the protocol's mandatory public
  artifacts). The PDF and the research package are not mandatory: the protocol counts them as partial delivery.

A job stopped by the runner (search cap, loop, timeout) has also failed, even if it left files.
"""
import glob
import json
import os
import re

C_REQUIRES_COMPANION = True


def rb_name_problem(path):
    """None if the RB's file name is `<report_basename>.rb.md` (its front matter's slug), else what is wrong.
    2026-10-29: a 4B named its RB `sitting-vs-smoking-sedation.sitting_vs_smoking_sedation.rb.md`, and its C
    jobs then took the file for evidence, not for their RB."""
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'^report_basename:\s*["\']?([^"\'\n]+?)["\']?\s*$', text, re.M)
    if not m:
        return "no report_basename in its front matter"
    if os.path.basename(path) != m.group(1) + ".rb.md":
        return f"named {os.path.basename(path)!r}, not {m.group(1) + '.rb.md'!r}"
    return None


def report_file(folder):
    """The Markdown report: the largest .md that is not the reply, an RB, working notes or a checkpoint."""
    mds = [p for p in glob.glob(os.path.join(folder, "*.md"))
           if not p.endswith(("_reply.md", ".rb.md", ".working.md", ".checkpoint.md"))]
    return max(mds, key=os.path.getsize) if mds else None


def companion_ok(folder):
    """A valid JSON companion in the folder."""
    for p in glob.glob(os.path.join(folder, "*.analysis.json")):
        try:
            json.load(open(p, encoding="utf-8"))
            return True
        except (ValueError, UnicodeDecodeError):
            continue
    return False


def missing(arm, folder, cli_results=()):
    """What the task in `folder` lacks, as a list of short names (empty = the task succeeded)."""
    out = [f"stopped by the runner ({r['result'][:80]})" for r in cli_results
           if r.get("search_cap") or r.get("loop") or r.get("timeout")][:1]
    if not os.path.isdir(folder) or not report_file(folder):
        out.append("Markdown report")
    if arm == "C" and C_REQUIRES_COMPANION and not companion_ok(folder):
        out.append("companion .analysis.json")
    return out
