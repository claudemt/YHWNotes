"""Inspect rewritten concept introductions and all analytic teaching modules."""
from pathlib import Path
import re, json
import fitz
from PIL import Image, ImageDraw
BOOK=Path(__file__).resolve().parents[1]
ROOT=BOOK.parents[1]
OUT=BOOK/'validation/render-narrative'
OUT.mkdir(exist_ok=True)
doc=fitz.open(ROOT/'example/FreeElectronQuantumOptics.pdf')
toc=doc.get_toc()
titles=['自由电子与量子激发','外场、反冲与量子交换','周期势与量子反冲',
        '自由传播、开放系统与量子测量','介质响应、辐射通道与实验反演']
compact=lambda x:re.sub(r'\s+','',x)
selected={1}
sections=[]
for i,(lv,name,page) in enumerate(toc):
    if any(title in compact(name) for title in titles):
        stop=next((p for ll,n,p in toc[i+1:] if ll<=lv),len(doc)+1)
        selected.update(range(page,min(page+3,stop)))
        focus=['QED 投影','正常模与 Green','连续谱耦合','传播子与平均场',
               '正能包络','单模交换哈密顿量','Magnus','Floquet--Sambe',
               'Wigner--Moyal','时间透镜','约化动力学','正算符值测度',
               '可扫描参考','实验尺度与反演']
        for l,n,p in toc[i+1:]:
            if p>=stop: break
            if l<=2 or any(compact(k) in compact(n) for k in focus):
                selected.update(range(p,min(p+2,stop)))
            sections.append(dict(title=n,start=p))
modules=[]
for p in (BOOK/'sections').glob('electron-*.tex'):
    m=re.search(r'\\subsection\{([^}]+)\}',p.read_text(encoding='utf-8'))
    if not m: continue
    target=compact(m[1])
    matches=[(i,t) for i,t in enumerate(toc) if target in compact(t[1])]
    assert len(matches)==1,(p.name,matches)
    i,(lv,name,start)=matches[0]
    stop=next((p for ll,n,p in toc[i+1:] if ll<=lv),len(doc))
    selected.update(range(start,min(stop+1,len(doc)+1)))
    modules.append(dict(title=name,start=start,end=stop))
anchors=['对偶映射','Weyl符号','第一项的高斯积分','完全正保迹','记为累积耦合与整体相位']
outside=[]
for i,page in enumerate(doc):
    text=compact(page.get_text())
    if i>440 and any(a in text for a in anchors): selected.add(i+1)
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            for span in line['spans']:
                x0,y0,x1,y1=span['bbox']
                if span['text'].strip() and (x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5):
                    outside.append(dict(page=i+1,text=span['text'],bbox=span['bbox']))
for n in sorted(selected):
    doc[n-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(OUT/f'page-{n:04d}.png')
pages=sorted(selected)
for k in range(0,len(pages),4):
    sheet=Image.new('RGB',(1240,1800),'#e7e7e7');draw=ImageDraw.Draw(sheet)
    for j,n in enumerate(pages[k:k+4]):
        im=Image.open(OUT/f'page-{n:04d}.png').convert('RGB'); im.thumbnail((600,855))
        x=(j%2)*620+(620-im.width)//2; y=(j//2)*900+30
        sheet.paste(im,(x,y));draw.text(((j%2)*620+14,(j//2)*900+8),f'PDF page {n}',fill='black')
    sheet.save(OUT/f'contact-{k//4+1:02d}.jpg',quality=93)
report=dict(pdf_pages=len(doc),rendered_pages=pages,sections=sections,modules=modules,
            contact_sheets=(len(pages)+3)//4,text_outside_page=outside)
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Rendered',len(pages),'pages;',report['contact_sheets'],'contact sheets; outside text:',len(outside))
