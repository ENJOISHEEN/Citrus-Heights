import re,json,sys
CODES={'59041':'Lodi','59083':'Antelope','59112':'Placerville','59007':'Downtown Sacramento','59005':'Elk Grove','59010':'Sunrise Plaza','59004':'Rancho Cordova','59095':'Florin Towne Center'}
def parse_nps(raw):
    """raw = JSON/HTML of the read_resource email result. returns {code:(responses,score)}"""
    t=re.sub(r'<[^>]+>',' ',raw); t=t.replace('\\r',' ').replace('\\n',' '); t=re.sub(r'\s+',' ',t)
    i=t.find('STORE NPS:'); t=t[i:] if i>=0 else t
    out={}
    for m in re.finditer(r'(\d{5}) - .+?\((?:XF|BP)\) (\d+) ([\d.]+)',t):
        if m.group(1) in CODES and m.group(1) not in out: out[m.group(1)]=(int(m.group(2)),float(m.group(3)))
    return out
if __name__=='__main__':
    print(parse_nps(open(sys.argv[1]).read()))
