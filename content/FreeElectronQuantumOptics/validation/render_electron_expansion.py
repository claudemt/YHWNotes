"""Render changed teaching sections and check text boxes across the final PDF."""
from pathlib import Path
import json
import re
import fitz
from PIL import Image, ImageOps, ImageDraw

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
OUT = BOOK / 'validation/render'
OUT.mkdir(parents=True, exist_ok=True)
doc = fitz.open(ROOT / 'example/FreeElectronQuantumOptics.pdf')
toc = doc.get_toc()
titles = [
    '从连续波包到通道相干', '有限作用窗：从振幅积累',
    '把场强、相位匹配和边带概率', '相干光照下，电子何时',
    '从完整反冲格计算一次', '从能谱相干算出电子脉冲列',
    '四个参考相位如何', '有限分辨率、有限窗口与近场',
    '热光输入：由生成函数', '有限高斯波包：解析解',
]
compact = lambda s: re.sub(r'\s+', '', s)
selected = {1}
ranges = []
for title in titles:
    found = [(i,t) for i,t in enumerate(toc) if compact(title) in compact(t[1])]
    assert len(found)==1, (title, found)
    i,(level,name,start) = found[0]
    stop = next((p for lv,n,p in toc[i+1:] if lv<=level), len(doc))
    pages = list(range(max(1,start-1), min(len(doc),stop+1)+1))
    selected.update(pages)
    ranges.append({'title':name,'start':start,'next_section':stop,'pages':pages})

# Also inspect the frontmatter and changed convention definitions in their context.
for i,(level,name,start) in enumerate(toc):
    if any(k in compact(name) for k in ['概论','符号索引','时间透镜']) or ('Bloch' in name and '纤维' in name):
        stop = next((p for lv,n,p in toc[i+1:] if lv<=level), start+2)
        end = min(stop+1,len(doc)) if '符号索引' in name else min(stop+1,start+5,len(doc))
        selected.update(range(start, end+1))
for p in range(len(doc)):
    s=compact(doc[p].get_text())
    if any(k in s for k in ['原始耦合','正频振幅','真实矩阵元的记号','光模自由演化','有限包络下的结果','各纯态分量的结果按概率加权']):
        selected.add(p+1)

outside=[]
for i,page in enumerate(doc):
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                x0,y0,x1,y1=span['bbox']
                if span['text'].strip() and (x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5):
                    outside.append({'page':i+1,'bbox':span['bbox'],'text':span['text']})
for n in sorted(selected):
    doc[n-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4), alpha=False).save(OUT/f'page-{n:04d}.png')

pages=sorted(selected)
for k in range(0,len(pages),4):
    group=pages[k:k+4]
    sheet=Image.new('RGB',(1240,1800),'#e7e7e7')
    draw=ImageDraw.Draw(sheet)
    for j,n in enumerate(group):
        im=Image.open(OUT/f'page-{n:04d}.png').convert('RGB')
        im.thumbnail((600,855))
        x=(j%2)*620+(620-im.width)//2
        y=(j//2)*900+30
        sheet.paste(im,(x,y))
        draw.text(((j%2)*620+14,(j//2)*900+8),f'PDF page {n}',fill='black')
    sheet.save(OUT/f'contact-{k//4+1:02d}.jpg',quality=93)

report={'pdf_pages':len(doc),'sections':ranges,'rendered_pages':pages,'text_outside_page':outside}
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
