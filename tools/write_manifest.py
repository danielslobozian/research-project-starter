"""Write an edition's MANIFEST.sha256: the SHA-256 of every file of benchmarks/<edition>/ and of the release
archive, in the format `sha256sum -c` reads (run it from the edition folder, with the archive beside it).

Usage:
  python3 write_manifest.py
"""
import hashlib
import os

import paths

EDITION = os.path.join(paths.REPO, "benchmarks", paths.EDITION)
ARCHIVE = os.path.join(paths.DATA_ROOT, "release", paths.EDITION, f"benchmark-{paths.EDITION}.zip")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    lines = []
    for d, _, files in sorted(os.walk(EDITION)):
        for f in sorted(files):
            path = os.path.join(d, f)
            if f != "MANIFEST.sha256":
                lines.append(f"{sha256(path)}  {os.path.relpath(path, EDITION)}")
    lines.append(f"{sha256(ARCHIVE)}  {os.path.basename(ARCHIVE)}")
    with open(os.path.join(EDITION, "MANIFEST.sha256"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines)} files -> {os.path.join(EDITION, 'MANIFEST.sha256')}")


if __name__ == "__main__":
    main()
