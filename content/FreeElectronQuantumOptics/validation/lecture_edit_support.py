"""Atomic, uniquely anchored editing of reviewed lecture passages."""
from pathlib import Path
import json
BASE = Path(__file__).resolve().parents[1]
texts, changes = {}, []
def get(name):
    p = BASE / name
    return texts.setdefault(p, p.read_text(encoding='utf-8'))
def edit(name, old, new):
    s = get(name)
    if s.count(old) != 1:
        raise ValueError(f'{name}: passage count {s.count(old)}: {old[:100]!r}')
    texts[BASE / name] = s.replace(old, new)
    changes.append(dict(file=name,before=old,after=new))
def region(name, start, end, new):
    s=get(name); a=s.index(start); b=s.index(end,a)
    edit(name,s[a:b],new)
def lead(name, heading, new):
    s=get(name); a=s.index(heading)+len(heading)
    # All headings passed include any label on the same line.
    while s[a].isspace(): a+=1
    ends=[s.find(marker,a) for marker in ['\n\n',r'\begin{',r'\[']]
    b=min(x for x in ends if x>=0)
    edit(name,s[a:b],new.rstrip()+'\n' if s[b:b+1]=='\\' else new.rstrip())
def finish(stage):
    for p,s in texts.items(): p.write_text(s,encoding='utf-8',newline='\n')
    (BASE/'validation'/f'lecture-narrative-{stage}.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(changes)} reviewed passages in {len(texts)} files')
