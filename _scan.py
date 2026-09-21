import pathlib, re, collections

root = pathlib.Path("content")
pat = re.compile(r'\\\\([A-Za-z]+)')
target = {"cref","ref","eqref","figref","tabref","secref","chapref",
          "cite","label","appref","eqnrefs","eqnrange","Cref","bookmark"}
hits = collections.Counter()
files = collections.defaultdict(list)
for p in root.rglob("*.tex"):
    t = p.read_text(encoding="utf-8")
    for m in pat.finditer(t):
        cmd = m.group(1)
        if cmd in target:
            hits[cmd] += 1
            line = t.count("\n", 0, m.start()) + 1
            files[cmd].append((str(p), line))
for c, n in sorted(hits.items()):
    print(c, n)
    for f, l in files[c]:
        print("    ", f, l)