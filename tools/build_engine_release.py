"""Build the engine release archive: the two project folders at the repository root, the licence files and an
install README, in one zip to attach to the GitHub release.

Usage:
  python3 build_engine_release.py VERSION        # e.g. 1.7b.10
Writes $RPS_DATA/release/engine-<VERSION>/research-project-starter-v<VERSION>.zip and runs check_private.py on it.
Every runtime file must carry the version label, or the build stops.
"""
import os
import subprocess
import sys
import zipfile

import paths

FOLDERS = ("research-boundary-generation", "research-boundary-execution")
EXTRA = ("LICENSE", "NOTICE")

README = """# Research Project Starter v{version}

Two projects for ChatGPT, Claude, Mistral Vibe or another assistant with projects, web search and file creation.

1. **Generation project**: agrees the research with you and issues a Research Boundaries file (RB). It first asks a
   few short questions about who will read the report and what it is for, then proposes a brief; your approval
   issues the RB. It does not research.
2. **Execution project**: researches and writes the report from an RB. Start a new chat there, attach the RB and
   send it without writing anything.

## Install the generation project

- Project instructions: paste the complete contents of
  `research-boundary-generation/research-boundary-generation.instructions.md`.
- Project files: upload `research-boundary-generation.protocol.md` and `research-boundary-generation.template.md`,
  keeping their names.

## Install the execution project

- Project instructions: paste the complete contents of
  `research-boundary-execution/research-boundary-execution.instructions.md`.
- Project files: upload `research-boundary-execution.protocol.md` and `research-boundary-execution.template.md`,
  keeping their names.
- Enable web search, file reading and file creation. Code execution helps with PDF checks; an HTML report needs no
  converter.

Never put both projects' instructions in one project. Do not upload this README.

## Use

1. In the generation project, describe what you want to know, in your own words.
2. Answer the reader questions as far as you like ("skip" uses the stated assumptions).
3. Read the brief; correct it, or approve it ("approved"). The RB is issued as a file.
4. In the execution project, open a new chat, attach the RB, send it with no text.
5. You receive the report as HTML (or PDF if you asked for it), its Markdown source for tools, and the RB.

Use a strong setting: on lighter ones, a simple-looking question may be answered directly, without the engine.
More, including what each app did in the recorded cases: https://danielslobozian.github.io/research-project-starter/
"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    version = sys.argv[1]
    files = [os.path.join(folder, name) for folder in FOLDERS
             for name in sorted(os.listdir(os.path.join(paths.REPO, folder)))]
    unlabelled = [f for f in files if version not in open(os.path.join(paths.REPO, f), encoding="utf-8").read()]
    if unlabelled:
        sys.exit(f"files without the {version} label: {unlabelled}")
    out_dir = os.path.join(paths.DATA_ROOT, "release", f"engine-{version}")
    os.makedirs(out_dir, exist_ok=True)
    archive = os.path.join(out_dir, f"research-project-starter-v{version}.zip")
    root = f"research-project-starter-v{version}"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{root}/README.md", README.format(version=version))
        for f in list(EXTRA) + files:
            z.write(os.path.join(paths.REPO, f), f"{root}/{f}")
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            print(name)
    check = subprocess.run([sys.executable, os.path.join(paths.TOOLS, "check_private.py"), archive])
    if check.returncode:
        sys.exit("privacy check failed: do not publish this archive")
    print(f"wrote {archive}")


if __name__ == "__main__":
    main()
