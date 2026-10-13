import re
def num(x):
    if x is None: return None
    s=str(x).strip().replace('$','').replace(',','')
    if s in ('','—','-'): return None
    pct=s.endswith('%')
    try:
        v=float(s.rstrip('%'))
    except ValueError:
        return str(x).strip()
    return v/100 if pct else v
def parse_dump(text):
    """connector read_resource text of the workbook -> {sheet: [row lists]} (first 4 daily sheets are complete)"""
    sheets={}; cur=None
    for line in text.split('\n'):
        m=re.match(r'## Sheet: (.+?) — ',line)
        if m: cur=m.group(1); sheets[cur]=[]; continue
        if cur and '\t' in line: sheets[cur].append([num(c) for c in line.rstrip('\r').split('\t')])
    return sheets
def find_rows(rows,pred): return [r for r in rows if pred(r)]
