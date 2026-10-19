"""python3 build_nps.py state.json publish_date(YYYY-MM-DD) out.html
Builds the NPS Focus page from state.json: nps{code:[surveys,score]} and nps_detail{weeks,resp,yoy,yoy_n,week_labels}."""
import sys,json,math,datetime as dt
NAMES={'59041':'Lodi','59083':'Antelope','59112':'Placerville','59007':'Downtown Sacramento','59005':'Elk Grove','59010':'Sunrise Plaza','59004':'Rancho Cordova','59095':'Florin Towne Center'}
def main(sp,pub,out):
    s=json.load(open(sp)); d=s['nps_detail']; pub=dt.date.fromisoformat(pub)
    n,sc=s['nps']['59010']; net=round(sc*n/100)
    goal=86; sat=dt.date(2026,10,31); days=max((sat-pub).days+1,0)
    pace=n/max(int(s['date'][-2:]),1)
    need=max(math.ceil((goal/100*n-net)/(1-goal/100)),0)
    reach=need<=pace*days
    cur=[i for i,r in enumerate(d['resp']) if r][-1]
    wk,wn=d['weeks'][cur],d['resp'][cur]; prev=[(d['weeks'][i],d['resp'][i]) for i in range(cur) if d['resp'][i]]
    def f(x,q): return (net+q*x)/(n+x)*100
    sce=''.join(f'<tr><td class="nm">+{x} surveys</td><td>{f(x,1):.1f}</td><td>{f(x,.9):.1f}</td></tr>' for x in (10,20,30,40))
    rows=sorted(((c,v) for c,v in s['nps'].items()),key=lambda kv:-kv[1][1])
    rk=[c for c,_ in rows].index('59010')+1
    mk=''.join(f'<tr class="{"me" if c=="59010" else ""}"><td>{i+1}</td><td class="nm">{NAMES[c]}</td><td>{v[1]}</td><td>{v[0]}</td></tr>' for i,(c,v) in enumerate(rows))
    top=rows[0]
    ydiff=sc-d['yoy']
    ytxt=(f'{abs(ydiff):.1f} pts ahead' if ydiff>=0 else f'{abs(ydiff):.1f} pts behind')
    if reach: reality=f'<li>To reach 86 MTD we need about <b>{need} more 9–10 surveys with zero detractors</b>. At our pace (about {pace:.0f} a day) that is <b>within reach by Saturday</b> if every survey is a 9–10.</li>'
    else: reality=f'<li>MTD is {net} net points over {n} surveys. To reach 86 MTD we need about <b>{need} more 9–10 surveys with zero detractors</b>.</li><li>At our pace (about {pace:.0f} a day, {days} days left) that is about {round(pace*days)} surveys, so <b>MTD 86 by Saturday is a stretch</b>. The win we control: <b>every survey from now on is a 9–10, and this week\'s score goes above 86</b>.</li>'
    css=open(__file__.replace('build_nps.py','nps.css')).read()
    prevtxt=' / '.join(f'{a:g}' for a,_ in prev[-2:]); prevn=' / '.join(str(b) for _,b in prev[-2:])
    wl=d['week_labels'][cur]
    html=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NPS Focus — Bridge Xfinity #59010 — Back to 86% by Saturday</title>
<style>{css}</style></head><body><div class="wrap">
<header><div><h1>NPS Focus</h1><div class="s">Bridge Xfinity #59010 · Sunrise Plaza</div></div><div class="d">{pub.strftime("%a %b %-d")}<small>Data through {s["date"][5:7].lstrip("0")}/{s["date"][8:].lstrip("0")}</small></div></header>
<div class="goalbar">GOAL: BACK TO 86% BY SATURDAY 10/31 — EVERY CUSTOMER. EVERY TIME. NO MISSES.</div>
<div class="tiles">
<div class="tile"><div class="l">Month to date</div><div class="v red">{sc:g}</div><div class="x">{n} surveys</div></div>
<div class="tile"><div class="l">Goal</div><div class="v">86</div><div class="x">{goal-sc:.1f} pts to go</div></div>
<div class="tile"><div class="l">This week ({wl})</div><div class="v {"red" if wk<goal else ""}">{wk:g}</div><div class="x">{wn} surveys</div></div>
<div class="tile"><div class="l">Weeks before</div><div class="v">{prevtxt}</div><div class="x">{prevn} surveys</div></div></div>
<div class="grid">
<div class="card alert"><h3>What the numbers say</h3><ul>
<li>Earlier weeks were {prevtxt}. <b>This week is the problem: {wk:g} on {wn} surveys.</b></li>
<li>Only {n} surveys on {s["store"]["traffic"]:,} visits MTD — very few visits turn into surveys. <b>Pitch every customer and set the 9–10 expectation.</b></li>
<li><b>Same period last year: {d["yoy"]} on {d["yoy_n"]} surveys.</b> We are {ytxt}, with {d["yoy_n"]-n} fewer surveys.</li>
<li>Rank #{rk} of 8. {NAMES[top[0]]} is at {top[1][1]} — it can be done in this market.</li></ul></div>
<div class="card green"><h3>Reality check on Saturday</h3><ul>{reality}</ul></div></div>
<details open><summary>Show: what MTD becomes</summary>
<div class="tw"><table><thead><tr><th>New surveys</th><th>If all 9–10</th><th>If 90% are 9–10, rest passive</th></tr></thead><tbody>{sce}</tbody></table></div></details>
{open(__file__.replace('build_nps.py','nps_plan.html')).read()}
<details open><summary>Show market NPS</summary><div class="tw"><table class="nowrap"><thead><tr><th>#</th><th>Store</th><th>NPS</th><th>Surveys</th></tr></thead><tbody>{mk}</tbody></table></div></details>
<div class="foot">Source: company stack ranking and NPS email. Rep-level NPS is not in the file.</div>
</div></body></html>'''
    open(out,'w').write(html)
main(*sys.argv[1:4])
