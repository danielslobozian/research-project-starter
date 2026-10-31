"""Fail if anything about to be published holds a personal path, a machine name, an email, a key or another
private string.

Two sets of patterns:
- generic ones, in this file: home and temporary folders, email addresses, private IP addresses, common key
  formats;
- literal strings that must never appear (names, the lab's host names), one per line in
  $RPS_DATA/private-strings.txt, outside the repository; secret tokens (API keys) are listed there only as
  "sha256:<hash>", and every token of 16 characters or more in a scanned file is hashed and compared.

Every file under the given paths is read (zip archives included, member by member; PDFs through pdftotext);
any other file that is not text is skipped and counted. Each hit prints file, line and the matching rule (never the secret itself); any hit
exits with status 1.

Usage:
  python3 check_private.py [PATH ...]          # default: the repository
  python3 check_private.py --allow-emails-in PATTERN ...
  python3 check_private.py --allow FILE ARCHIVE    # FILE: reviewed exceptions, "<file glob><TAB><rule>" per line
"""
import argparse
import fnmatch
import hashlib
import os
import re
import subprocess
import sys
import zipfile

import paths

GENERIC = {
    "home folder": re.compile(r"(?<![\w.%-])(?:/home/[a-z_][a-z0-9_-]*|/Users/[A-Za-z])|C:\\Users\\", re.I),
    "temporary folder": re.compile(r"/tmp/(?:claude-\d+|gmlc-)"),
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "private IP address": re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|\b192\.168\.\d{1,3}\.\d{1,3}\b"),
    "API key": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|sk-ant-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}"
                          r"|AKIA[0-9A-Z]{16}|xox[bp]-[A-Za-z0-9-]{10,})"),
    "bearer token": re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
}
SKIP_DIRS = {".git", "__pycache__"}


def literals():
    path = os.path.join(paths.DATA_ROOT, "private-strings.txt")
    if not os.path.exists(path):
        sys.exit(f"missing {path}: one private string per line (names, host names, key values)")
    out = [s.strip() for s in open(path) if s.strip() and not s.startswith("#")]
    plain = [s for s in out if not s.startswith("sha256:")]
    hashes = {s.removeprefix("sha256:") for s in out if s.startswith("sha256:")}
    return [(f"private string #{i}", re.compile(re.escape(s), re.I)) for i, s in enumerate(plain, 1)], hashes


TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]{16,}")


def texts(root):
    """(name, text) for every file under root, zip members included; None as text for binary content."""
    files = [root] if os.path.isfile(root) else [
        os.path.join(d, f) for d, dirs, fs in os.walk(root) for f in fs
        if not dirs.__setitem__(slice(None), [x for x in dirs if x not in SKIP_DIRS])]
    for path in sorted(files):
        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                for member in z.namelist():
                    yield f"{path}!{member}", decode(z.read(member), member)
        else:
            with open(path, "rb") as f:
                yield path, decode(f.read(), path)


def decode(data, name):
    if name.lower().endswith(".pdf"):
        try:
            return subprocess.run(["pdftotext", "-q", "-", "-"], input=data, capture_output=True,
                                  timeout=120).stdout.decode("utf-8", "replace")
        except (OSError, subprocess.TimeoutExpired):
            return None
    if b"\0" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=[paths.REPO])
    ap.add_argument("--allow-emails-in", nargs="*", default=[],
                    help="glob patterns of files where third-party email addresses are expected (e.g. cited sources)")
    ap.add_argument("--allow", help="file of reviewed exceptions: a file glob and a rule name per line, tab-separated")
    a = ap.parse_args()
    allowed = [tuple(line.rstrip("\n").split("\t", 1)) for line in open(a.allow)
               if line.strip() and not line.startswith("#")] if a.allow else []
    private, hashes = literals()
    rules = list(GENERIC.items()) + private
    hits, scanned, binary = 0, 0, 0
    for root in a.paths:
        for name, text in texts(root):
            if text is None:
                binary += 1
                continue
            scanned += 1
            for n, line in enumerate(text.splitlines(), 1):
                for rule, rx in rules:
                    if rule == "email address" and any(fnmatch.fnmatch(name, p) for p in a.allow_emails_in):
                        continue
                    if rx.search(line):
                        if any(fnmatch.fnmatch(name, g) and rule == r for g, r in allowed):
                            continue
                        hits += 1
                        print(f"{name}:{n}: {rule}")
                if hashes and any(hashlib.sha256(t.encode()).hexdigest() in hashes for t in TOKEN_RE.findall(line)):
                    hits += 1
                    print(f"{name}:{n}: secret token (hash match)")
    print(f"{scanned} text files scanned, {binary} binary skipped, {hits} hits")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
