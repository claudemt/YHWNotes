#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification: bare eqref/ref, Chinese labels, dangling refs."""
import os, re

ROOT = r"E:\OneDrive\Desktop\YHWNotes"
BODY_DIR = os.path.join(ROOT, "content", "YHWNotes", "sections")

def iter_body_files():
    for dirpath, dirnames, filenames in os.walk(BODY_DIR):
        base = os.path.basename(dirpath)
        if base.endswith("_fig_code"):
            continue
        for fn in filenames:
            if fn.endswith(".tex"):
                yield os.path.join(dirpath, fn)

# 1) bare \eqref and \ref (not \cref/\Cref)
bare_eqref = re.compile(r"(?<!\\c)\\eqref\{")
bare_ref = re.compile(r"(?<![a-zA-Z\\])\\ref\{")

# 2) Chinese labels
label_re = re.compile(r"\\label\{([^}]*)\}")

# 3) all cref/ref targets
cref_re = re.compile(r"\\(?:cref|Cref|ref|eqref|autoref|pageref)\{([^}]*)\}")

labels = set()
n_bare_eqref = 0
n_bare_ref = 0
chinese_labels = []
all_refs = []  # (rel, target)

# Pass 1: collect all labels and stats
for f in iter_body_files():
    rel = os.path.relpath(f, ROOT)
    with open(f, "r", encoding="utf-8") as fh:
        txt = fh.read()
    n_bare_eqref += len(bare_eqref.findall(txt))
    n_bare_ref += len(bare_ref.findall(txt))
    for m in label_re.finditer(txt):
        name = m.group(1)
        labels.add(name)
        if re.search(r"[^\x00-\x7F]", name):
            chinese_labels.append((rel, name))
    for m in cref_re.finditer(txt):
        all_refs.append((rel, m.group(1)))

# Pass 2: dangling check (now labels is fully populated)
dangling = []
for rel, target in all_refs:
    if target not in labels:
        dangling.append((rel, target))

print(f"bare \\eqref remaining: {n_bare_eqref}")
print(f"bare \\ref remaining: {n_bare_ref}")
print(f"Chinese labels remaining: {len(chinese_labels)}")
for rel, name in chinese_labels:
    print(f"  [{rel}] {name!r}")
print(f"dangling references: {len(dangling)}")
for rel, t in dangling:
    print(f"  [{rel}] -> {t!r}")
print(f"total labels now: {len(labels)}")
