#!/usr/bin/env python3
"""RTE春夏巡游北京站-ColinVFinal.pptx → 结构化版面模型 JSON。

  只做一件事：把 36 张 slide 的每个 shape 的绝对坐标 / 填充 / 描边 / 文本 run 属性，
  以及 <p:timing> 的点击分组，原样抽成 JSON。不做任何美学判断。
  用法：cd <解包目录> && python3 model.py > robot26-bj-model.json
"""
import os, sys, json
from xml.etree import ElementTree as ET

NS = {
 'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
 'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
def q(t):
    p,l=t.split(':'); return '{%s}%s'%(NS[p],l)

EMU = 9525.0          # 18288000 EMU / 1920 px —— 1920×1080 舞台正好等比
DEF_SZ = 18.0         # presentation.xml defaultTextStyle lvl1 sz=1800
SCHEME = {'bg1':'#FFFFFF','tx1':'#000000','lt1':'#FFFFFF','dk1':'#000000',
          'bg2':'#E7E6E6','tx2':'#44546A','lt2':'#E7E6E6','dk2':'#44546A',
          'accent1':'#4472C4','accent2':'#ED7D31','accent3':'#A5A5A5',
          'accent4':'#FFC000','accent5':'#5B9BD5','accent6':'#70AD47'}

def rnd(v): return round(v,2)

def color_of(el):
    """<a:solidFill> 之类的父元素 → #RRGGBB 或 #RRGGBBAA"""
    if el is None: return None
    c = el.find(q('a:srgbClr'))
    if c is not None:
        hexv = '#'+c.get('val').upper()
        al = c.find(q('a:alpha'))
        if al is not None:
            hexv += '%02X' % round(int(al.get('val'))/100000*255)
        return hexv
    c = el.find(q('a:schemeClr'))
    if c is not None:
        base = SCHEME.get(c.get('val'), '#000000')
        al = c.find(q('a:alpha'))
        if al is not None:
            base += '%02X' % round(int(al.get('val'))/100000*255)
        return base
    c = el.find(q('a:prstClr'))
    if c is not None:
        return {'black':'#000000','white':'#FFFFFF'}.get(c.get('val'),'#000000')
    return None

def fill_of(spPr):
    if spPr is None: return None
    if spPr.find(q('a:noFill')) is not None: return None
    sf = spPr.find(q('a:solidFill'))
    if sf is not None: return color_of(sf)
    gf = spPr.find(q('a:gradFill'))
    if gf is not None:
        stops=[]
        for gs in gf.iter(q('a:gs')):
            stops.append([int(gs.get('pos'))/1000.0, color_of(gs)])
        ang = gf.find(q('a:lin'))
        return {'grad':stops,'ang':(int(ang.get('ang'))/60000 if ang is not None and ang.get('ang') else 0)}
    return None

def line_of(spPr):
    if spPr is None: return None
    ln = spPr.find(q('a:ln'))
    if ln is None: return None
    if ln.find(q('a:noFill')) is not None: return None
    d = {}
    d['w'] = round(int(ln.get('w'))/12700.0*4/3, 2) if ln.get('w') else 1.0   # pt → px
    sf = ln.find(q('a:solidFill'))
    d['c'] = color_of(sf) if sf is not None else '#000000'
    dash = ln.find(q('a:prstDash'))
    if dash is not None and dash.get('val') not in (None,'solid'): d['dash']=dash.get('val')
    return d

def xfrm_of(el):
    sp = el.find(q('p:spPr')) if el.find(q('p:spPr')) is not None else el
    x = sp.find(q('a:xfrm'))
    if x is None:
        x = el.find('.//'+q('a:xfrm'))
    if x is None: return None
    off, ext = x.find(q('a:off')), x.find(q('a:ext'))
    d = {}
    if off is not None: d['x']=rnd(int(off.get('x'))/EMU); d['y']=rnd(int(off.get('y'))/EMU)
    if ext is not None: d['w']=rnd(int(ext.get('cx'))/EMU); d['h']=rnd(int(ext.get('cy'))/EMU)
    if x.get('rot'): d['rot']=round(int(x.get('rot'))/60000.0,2)
    if x.get('flipH')=='1': d['fh']=1
    if x.get('flipV')=='1': d['fv']=1
    return d

def body_of(txb):
    bp = txb.find(q('a:bodyPr'))
    d = {'anchor':'t','ins':[2.67,2.67,2.67,2.67],'wrap':'square'}
    if bp is None: return d
    if bp.get('anchor'): d['anchor']=bp.get('anchor')
    if bp.get('wrap'): d['wrap']=bp.get('wrap')
    ins=[]
    for k,dv in (('lIns',91440),('tIns',45720),('rIns',91440),('bIns',45720)):
        v = int(bp.get(k)) if bp.get(k) is not None else dv
        ins.append(rnd(v/EMU))
    d['ins']=ins
    naf = bp.find(q('a:normAutofit'))
    if naf is not None:
        d['af'] = 1   # PowerPoint「溢出时缩排文字」——渲染端可继续按需微缩
        if naf.get('fontScale'): d['fs']=int(naf.get('fontScale'))/100000.0
        if naf.get('lnSpcReduction'): d['lsr']=int(naf.get('lnSpcReduction'))/100000.0
    if bp.find(q('a:spAutoFit')) is not None: d['spAuto']=1
    return d

def runs_of(para):
    out=[]
    for r in para:
        tag = r.tag.split('}')[1]
        if tag=='r':
            t = r.find(q('a:t'))
            rPr = r.find(q('a:rPr'))
            info={'t': (t.text if t is not None and t.text is not None else '')}
            if rPr is not None:
                info['sz'] = int(rPr.get('sz'))/100.0 if rPr.get('sz') else None
                if rPr.get('b')=='1': info['b']=1
                if rPr.get('i')=='1': info['i']=1
                if rPr.get('u') and rPr.get('u')!='none': info['u']=1
                if rPr.get('strike') and rPr.get('strike')!='noStrike': info['s']=1
                if rPr.get('spc'): info['spc']=rnd(int(rPr.get('spc'))/100.0*4/3)
                sf = rPr.find(q('a:solidFill'))
                if sf is not None: info['c']=color_of(sf)
                lat = rPr.find(q('a:latin'))
                if lat is not None: info['f']=lat.get('typeface')
            out.append(info)
        elif tag=='br':
            out.append({'br':1})
        elif tag=='fld':
            t = r.find(q('a:t'))
            out.append({'t': (t.text or '') if t is not None else ''})
    return out

def paras_of(txb):
    out=[]
    for para in txb.findall(q('a:p')):
        pPr = para.find(q('a:pPr'))
        d = {}
        if pPr is not None:
            if pPr.get('algn'): d['algn']=pPr.get('algn')
            if pPr.get('marL'): d['marL']=rnd(int(pPr.get('marL'))/EMU)
            if pPr.get('indent'): d['ind']=rnd(int(pPr.get('indent'))/EMU)
            ln = pPr.find(q('a:lnSpc')+'/'+q('a:spcPct'))
            if ln is not None: d['ln']=int(ln.get('val'))/100000.0
            lnp = pPr.find(q('a:lnSpc')+'/'+q('a:spcPts'))
            if lnp is not None: d['lnpt']=int(lnp.get('val'))/100.0*4/3
            for k,tag in (('bef','a:spcBef'),('aft','a:spcAft')):
                e = pPr.find(q(tag)+'/'+q('a:spcPts'))
                if e is not None: d[k]=rnd(int(e.get('val'))/100.0*4/3)
                e2 = pPr.find(q(tag)+'/'+q('a:spcPct'))
                if e2 is not None: d[k+'p']=int(e2.get('val'))/100000.0
            if pPr.find(q('a:buNone')) is not None: d['bu']='none'
            bc = pPr.find(q('a:buChar'))
            if bc is not None: d['bu']=bc.get('char')
        rs = runs_of(para)
        if rs or out: d['runs']=rs; out.append(d)
    # 去掉尾部空段
    while out and not any(r.get('t','').strip() or r.get('br') for r in out[-1].get('runs',[])):
        out.pop()
    return out

def load_rels(path):
    d={}
    if os.path.exists(path):
        for rel in ET.parse(path).getroot():
            d[rel.get('Id')]=(os.path.basename(rel.get('Target')), rel.get('Type').rsplit('/',1)[-1])
    return d

def walk(node, rels, out, depth=0, off=None):
    for el in node:
        tag = el.tag.split('}')[1]
        if tag not in ('sp','pic','graphicFrame','cxnSp','grpSp'): continue
        nv = el.find('.//'+q('p:cNvPr'))
        it = {'kind':tag,'id':nv.get('id'),'name':nv.get('name') or ''}
        xf = xfrm_of(el)
        if xf: it.update(xf)
        spPr = el.find(q('p:spPr')) or el.find(q('p:grpSpPr'))
        if spPr is not None:
            pg = spPr.find(q('a:prstGeom'))
            it['geom'] = pg.get('prst') if pg is not None else ('custom' if spPr.find(q('a:custGeom')) is not None else 'rect')
            f = fill_of(spPr)
            if f: it['fill']=f
            l = line_of(spPr)
            if l: it['line']=l
        if tag=='pic':
            blip = el.find('.//'+q('a:blip'))
            if blip is not None:
                rid = blip.get(q('r:embed'))
                if rid in rels: it['img']=rels[rid][0]
            sr = el.find('.//'+q('a:srcRect'))
            if sr is not None and sr.attrib:
                it['crop']={k:int(v)/100000.0 for k,v in sr.attrib.items()}
        if tag=='graphicFrame':
            for m in el.iter():
                if m.tag.endswith('}videoFile'):
                    lk = m.get(q('r:link')) or m.get(q('r:embed'))
                    if lk in rels: it['video']=rels[lk][0]
        txb = el.find(q('p:txBody'))
        if txb is not None:
            it['body']=body_of(txb)
            ps = paras_of(txb)
            if ps: it['paras']=ps
        out.append(it)
        if tag=='grpSp':
            walk(el, rels, out, depth+1)

# ─────────── timing ───────────
def timing_of(root):
    tim = root.find(q('p:timing'))
    if tim is None: return []
    groups=[]
    for seq in tim.iter(q('p:seq')):
        sct = seq.find(q('p:cTn'))
        if sct is None or sct.get('nodeType')!='mainSeq': continue
        top = sct.find(q('p:childTnLst'))
        if top is None: continue
        for clickpar in top:
            ct = clickpar.find(q('p:cTn'))
            if ct is None: continue
            ids=[]
            for lct in ct.iter(q('p:cTn')):
                if not lct.get('presetID'): continue
                if lct.get('presetClass')!='entr': continue
                st = lct.find('.//'+q('p:spTgt'))
                if st is None: continue
                spid = st.get('spid')
                if spid and spid not in ids: ids.append(spid)
            groups.append(ids)
    return groups

def main():
    out={'slides':[]}
    for n in range(1,37):
        path='ppt/slides/slide%d.xml'%n
        root=ET.parse(path).getroot()
        rels=load_rels('ppt/slides/_rels/slide%d.xml.rels'%n)
        layout=[v[0] for v in rels.values() if v[1]=='slideLayout']
        shapes=[]
        walk(root.find(q('p:cSld')+'/'+q('p:spTree')), rels, shapes)
        # 版式底：layout15=纯黑无角标 / layout16=纯黑+右上角标 image4 / layout14=纯黑+右上 image3
        lay = layout[0] if layout else ''
        logo = {'slideLayout16.xml':('image4.png',1527.0,49.2,335.0,37.3),
                'slideLayout14.xml':('image3.png',1579.0,23.3,316.1,88.1)}.get(lay)
        out['slides'].append({'n':n,'layout':lay,'bg':'#000000',
                              'logo':(list(logo) if logo else None),
                              'shapes':shapes,'clicks':timing_of(root)})
    json.dump(out, sys.stdout, ensure_ascii=False, separators=(',',':'))

main()
