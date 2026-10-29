import math,re,json,sys,datetime as dt
L='https://celestial.cable.comcast.com/knowledge/article-info/?query=240319165608377'
GROUPS=["Ashton, Brianna &amp; Joseph","Kevin &amp; Daisy","Kenneth, Justin &amp; Nancy","De-Jon &amp; Andrew","Albert &amp; Jayme"]
ZONES=["A Front &amp; Windows","B Sales Floor","C Register Area","D Back Room","E Restroom &amp; Supply"]

# Black Friday 2026 promo calendar. Each row: (name, start, end, savings). start=None means
# always-on (no promo window). Re-run build_board.py any day and the card below will show
# what's live today, what's starting soon, and what's already expired — no manual edits needed
# until the deals themselves change.
BF_START=dt.date(2026,11,11); BF_END=dt.date(2026,12,1)
TIPS=[  # trade-in required, DPP required
 ('Google — new lines', BF_START, BF_END, '$1,500'),
 ('Google — upgrade', BF_START, BF_END, '$1,230'),
 ('Samsung — new lines', BF_START, BF_END, '$1,300'),
 ('Samsung — upgrade', BF_START, BF_END, '$1,100'),
 ('Apple &amp; Moto — new lines', BF_START, BF_END, '$1,200'),
 ('Apple &amp; Moto — upgrade', BF_START, BF_END, '$930'),
 ('Diamond: iPhone Duo — upgrade', dt.date(2026,10,16), BF_END, '$1,000'),
]
NOTRADE=[  # DPP required, no trade-in
 ('Google — new lines', BF_START, BF_END, '$750'),
 ('Google — upgrade', BF_START, BF_END, '$550'),
 ('Samsung — new lines', dt.date(2026,10,9), BF_END, '$500'),
 ('Samsung — upgrade', dt.date(2026,10,9), BF_END, '$300'),
 ('Apple &amp; Moto — new lines', BF_START, BF_END, '$400'),
 ('Apple &amp; Moto — upgrade', BF_START, BF_END, '$200'),
 ('Diamond/Platinum: Galaxy S26FE "On Us" — new line', BF_START, BF_END, '$699.99'),
]
ANYTIME=[  # upgrade-anytime, existing lines (NDEL) only
 ('Apple &amp; Moto', BF_START, BF_END, '$200'),
 ('Samsung', BF_START, BF_END, '$300'),
 ('Google', dt.date(2026,10,9), BF_END, '$300'),
]
TABLETS=[
 ('iPad A16', BF_START, BF_END, '50% off ($599.99 MSRP)'),
 ('Galaxy Tab S10FE', BF_START, BF_END, '50% off ($649.99 MSRP)'),
 ('Galaxy Tab S12+', BF_START, BF_END, '50% off ($1,349.99 MSRP)'),
]
WATCH=[
 ('Gold members', BF_START, BF_END, '$300'),
 ('Platinum members', dt.date(2026,10,28), BF_END, '$300'),
 ('Diamond members', dt.date(2026,5,11), BF_END, '$300'),
 ('Employees', dt.date(2026,1,21), BF_END, '$300'),
]
SERVICE=[
 ('First line free — Mobile Select $0/mo x 12mo (new XM, 300 Mbps+ internet)', None, None, ''),
 ('Targeted: $30 off/mo (3+ new lines, same order)', dt.date(2026,11,19), dt.date(2027,3,31), ''),
 ('Targeted: $60 off/mo (4+ new lines, same order)', dt.date(2026,11,19), dt.date(2027,3,31), ''),
 ('Waived $25 activation fee', dt.date(2026,5,11), BF_END, ''),
]
def _timing(s,e):
    if s is None: return 'Ongoing'
    t=f'{s.month}/{s.day}'+(f'/{s.year-2000}' if s.year!=2026 else '')
    t+='–'+f'{e.month}/{e.day}'+(f'/{e.year-2000}' if e.year!=2026 else '')
    return t
def _status(s,e,pub):
    if s is None: return ''
    if pub<s: return f' <span class="mut">(starts {s.month}/{s.day})</span>'
    if 0<=(e-pub).days<=3: return f' <span class="mut">(ends {e.month}/{e.day})</span>'
    return ''
def bf_table(rows,pub,cols=('Deal','Timing','Savings')):
    trs=''.join(f'<tr><td class="nm">{n}</td><td>{_timing(s,e)}</td><td>{sv}{_status(s,e,pub)}</td></tr>' for n,s,e,sv in rows)
    return '<table><thead><tr>'+''.join(f'<th>{c}</th>' for c in cols)+f'</tr></thead><tbody>{trs}</tbody></table>'
def bf_card(pub):
    allrows=[(c,*r) for c,rows in (('TIPs (trade-in)',TIPS),('No trade-in',NOTRADE),('Upgrade anytime',ANYTIME),('Tablets &amp; watches',TABLETS+WATCH)) for r in rows]
    live=lambda s,e: s is not None and s<=pub<=e
    early=[(c,n,sv) for c,n,s,e,sv in allrows if live(s,e) and s<BF_START]
    main=[(c,n,sv) for c,n,s,e,sv in allrows if s==BF_START and pub<=e]
    bullets=''
    if early:
        bullets+='<li><b>Early/live now (ends 12/1):</b> '+' · '.join(f'{n} {sv}' for c,n,sv in early)+'</li>'
    if main:
        bullets+=f'<li><b>Black Friday window ({_timing(BF_START,BF_END)}):</b> '+' · '.join(f'{n} {sv}' for c,n,sv in main)+'</li>'
    bullets+='<li><b>Also:</b> First line free (Mobile Select, new XM + 300Mbps+ internet) · waived $25 activation (thru 12/1) · 11/19–3/31/27: targeted $30 off (3+ lines) / $60 off (4+ lines) — check Members Hub/Einstein360 eligibility first</li>'
    details=(
        '<details><summary>Show deal tables &amp; links</summary><div class="tw">'
        f'<b><a href="{L}#TIPSdeals">TIPs — trade-in required</a></b>{bf_table(TIPS,pub)}</div>'
        f'<div class="tw" style="margin-top:6px"><b><a href="{L}#flagship">No trade-in</a></b>{bf_table(NOTRADE,pub)}</div>'
        f'<div class="tw" style="margin-top:6px"><b><a href="{L}#anytime">Upgrade anytime</a> (existing lines only)</b>{bf_table(ANYTIME,pub)}</div>'
        f'<div class="tw" style="margin-top:6px"><b>Smartwatches &amp; tablets</b>{bf_table(TABLETS+WATCH,pub)}</div>'
        f'<div class="tw" style="margin-top:6px"><b>Service discounts</b>{bf_table(SERVICE,pub,cols=("Deal","Timing","Notes"))}</div>'
        '</details>')
    return f'<div class="card"><h3>🖤 Black Friday deals — {_timing(BF_START,BF_END)}</h3><ul>{bullets}</ul>{details}</div>'
def clean_html(pub):
    w=(pub-dt.date(2026,10,12)).days//7
    mon=dt.date(2026,10,12)+dt.timedelta(days=7*w); sun=mon+dt.timedelta(days=6); nm=mon+dt.timedelta(days=7)
    t1=''.join(f'<tr><td class="nm">{ZONES[k]}</td><td>{GROUPS[(k-w)%5]}</td></tr>' for k in range(5))
    t2=''.join(f'<tr><td class="nm">{ZONES[k][0]}</td><td>{GROUPS[(k-w-1)%5]}</td></tr>' for k in range(5))
    return (f'<div class="card"><h3>🧹 Cleaning — this week ({mon.month}/{mon.day}–{sun.month}/{sun.day})</h3><table class="nowrap"><tbody>{t1}</tbody></table>'
      f'<details><summary>Show next week ({nm.month}/{nm.day})</summary><table class="nowrap"><tbody>{t2}</tbody></table><div class="mut" style="margin-top:4px"><a href="https://claude.ai/artifact/SDrzApSmTQHCg9NvVd3Q9Z">Task checklists &amp; full schedule</a></div></details></div>')
def build(state,pub,out):
    S=state['store']; d=dt.date.fromisoformat(state['date'])
    DAY=d.day; DIM=31; LEFT=DIM-DAY; TGT=state['target']; GOAL=math.ceil(TGT*1.25); ACT=S['rgu']; GAP=GOAL-ACT; PACE=ACT/DAY; SELL=35
    DATE_LONG=d.strftime('%B ')+str(d.day)+', 2026'; DATE_MD=f'{d.month}/{d.day}'
    PLAN_HIST=' → '.join(str(x) for x in state['plan_history'])
    reps=state['reps']; n=len(reps)
    R=[(r['name'],r['rgu'],r['rgu']/(60*DAY/DIM)*100,r['int'],r['tv'],r['voice'],r['home'],r['mt'],r['mo'],r['sel'],r['plus'],r['leg'],r['wear'],r['acc'],0) for r in reps]
    SHARE=math.ceil((ACT+SELL*LEFT)/n)
    m=lambda x:f"${x:,.2f}"
    nps=state['nps']['59010'][1]
    MO=S['mo']; PL=S['plus']; Mtot=MO/DAY*LEFT; Ptot=0.65*(MO+Mtot); RATE=(Ptot-PL)/Mtot*100
    ATT0=PL/MO*100; STAB=S['mt']-S['mo']
    TVN=max(0,4*n-S['tv']); TABN=max(0,8*n-STAB); WN=max(0,4*n-S['wear'])
    def fl(b): return ' class="bad"' if b else ''
    slim=""
    for nme,g,t,i,tv,v,h,mt,mo,se,pl,lg,w,acc,cm in R:
        att=pl/mo*100 if mo else 0
        slim+=f'<tr><td class="nm">{nme}</td><td>{g}</td><td>{g/75*100:.0f}%</td><td{fl(tv<=0)}>{tv}</td><td>{mt-mo}</td><td{fl(att<65)}>{att:.0f}%</td><td{fl(acc==0)}>${acc:,.0f}</td></tr>'
    full=""
    for nme,g,t,i,tv,v,h,mt,mo,se,pl,lg,w,acc,cm in R:
        att=pl/mo*100 if mo else 0
        full+=f'<tr><td class="nm">{nme}</td><td>{g}</td><td>{t:.1f}%</td><td>{i}</td><td>{tv}</td><td>{mt}</td><td>{mt-mo}</td><td>{pl}</td><td{fl(att<65)}>{att:.2f}%</td><td>${pl*40:,}</td><td>{m(acc)}</td></tr>'
    full+=f'<tr class="tot"><td class="nm">STORE</td><td>{ACT}</td><td>{ACT/(TGT*DAY/DIM)*100:.1f}%</td><td>{S["int"]}</td><td>{S["tv"]}</td><td>{S["mt"]}</td><td>{STAB}</td><td>{PL}</td><td>{ATT0:.2f}%</td><td>${PL*40:,}</td><td>{m(S["acc"])}</td></tr>'
    mk_rows=[]
    for c,s in state['market'].items():
        mk_rows.append(dict(c=c,name=s['name'],tg=s['target'],a=s['rgu'],t=s['rgu']/(s['target']*DAY/DIM)*100,conv=s['rgu']/s['traffic']*100,tv=s['tv'],tab=s['mt']-s['mo'],w=s['wear'],at=s['plus']/s['mo']*100 if s['mo'] else 0,acc=s['acc'],nps=(state['nps'].get(c) or [0,None])[1]))
    mk_rows.sort(key=lambda x:-x['t'])
    mk=""
    for k,x in enumerate(mk_rows,1):
        me=x['c']=='59010'; nm=x['name']+(' (us)' if me else '')
        npsc='' if x['nps'] is None else f"{x['nps']:.1f}"
        mk+=f'<tr{" class=\"me\"" if me else ""}><td>{k}</td><td class="nm">{nm}</td><td>{x["a"]}/{x["tg"]}</td><td>{x["t"]:.1f}%</td><td>{x["conv"]:.1f}%</td><td>{x["tv"]}</td><td>{x["tab"]}</td><td>{x["w"]}</td><td{fl(x["at"]<65)}>{x["at"]:.0f}%</td><td>{m(x["acc"])}</td><td>{npsc}</td></tr>'
    rank=[x['c'] for x in mk_rows].index('59010')+1
    gp=""
    for nme,g,t,i,tv,v,h,mt,mo,se,pl,lg,w,acc,cm in R:
        tab=mt-mo; need=(SHARE-g)/LEFT; pace=g/DAY
        gp+=f'<tr><td class="nm">{nme}</td><td{fl(need>pace)}>{need:.1f} <span class="mut">(now {pace:.1f})</span></td><td>{max(0,4-tv)}</td><td>{max(0,8-tab)}</td><td>{max(0,4-w)}</td><td>${max(0,450-acc):,.0f}</td></tr>'
    cp=""
    for lab,dd in [("Sun 10/18",18),("Sun 10/25",25),("Sat 10/31",31)]:
        if dd<=DAY: continue
        f=(dd-DAY)/LEFT; mo_=MO+Mtot*f; pl_=PL+(Ptot-PL)*f; rg=ACT+round(SELL*LEFT*f)
        cp+=f'<tr><td class="nm">{lab}</td><td>{rg} <span class="mut">({rg/GOAL*100:.0f}% of {GOAL})</span></td><td>{pl_/mo_*100:.0f}%</td><td>{S["tv"]+round(TVN*f)}</td><td>{STAB+round(TABN*f)}</td><td>{S["wear"]+round(WN*f)}</td></tr>'
    ystore=state.get('daily_store_rgu',0)
    mv=sorted([(r['daily'],r['name'].split()[0]) for r in reps if r.get('daily')],reverse=True)
    wins=[f'<li><b>Store +{ystore} RGUs yesterday</b> ({ACT-ystore} → {ACT})</li>']
    if mv: wins.append('<li><b>'+mv[0][1]+f' +{mv[0][0]}</b>'+''.join(f' · {nm_} +{v}' for v,nm_ in mv[1:3])+'</li>')
    tv4=[r['name'].split()[0] for r in reps if r['tv']>=4]
    wins.append('<li>TV minimum (4) hit: '+', '.join(tv4)+'</li>' if tv4 else f"<li>Tablets: Sunrise has {STAB}</li>")
    lead=[k for k,v in (('tablets',max(mk_rows,key=lambda x:x['tab'])['c']=='59010'),('accessories',max(mk_rows,key=lambda x:x['acc'])['c']=='59010'),('watches',max(mk_rows,key=lambda x:x['w'])['c']=='59010')) if v]
    if lead: wins.append('<li>Sunrise leads the market in '+', '.join(lead)+'</li>')
    flat=[r['name'].split()[0] for r in reps if r.get('daily',1)==0]
    above=[r['name'].split()[0] for r in reps if r['mo'] and r['plus']/r['mo']>=.65]
    tv0=[r['name'].split()[0] for r in reps if r['tv']==0]
    foc=[f'<li><b>NPS {nps:.1f}</b> — '+('under' if nps<90 else 'at')+f' our 90 goal ({state["nps"]["59010"][0]} responses)</li>',
         f'<li><b>XM+ Attach {ATT0:.0f}%</b> — goal 65%'+(' · above 65%: '+', '.join(above) if above else '')+'</li>']
    extra=[]
    if flat: extra.append('flat yesterday: '+', '.join(flat))
    if tv0: extra.append('0 TVs: '+', '.join(tv0))
    pr=state.get('prev_rank')
    if pr and pr!=rank: extra.append(f'market rank {"up" if rank<pr else "down"} to #{rank}')
    if extra: foc.append('<li>'+' · '.join(extra)+'</li>')
    WINS=''.join(wins); FOCUS=''.join(foc)
    MKT_SENT=f'<div class="card" style="margin-top:10px"><b>Market: Sunrise is #{rank} of {len(mk_rows)}</b> on trend ({mk_rows[rank-1]["t"]:.1f}%).'+(f' Next up: {mk_rows[rank-2]["name"]} at {mk_rows[rank-2]["t"]:.1f}%.' if rank>1 else '')
    NPS_STYLE='' if nps>=90 else ' style="color:var(--r)"'
    NPS_SCORE=nps
    NPS_TEXT='<b>'+('Still under our 90 goal.' if nps<90 else 'At goal — keep it there.')+f'</b> {state["nps"]["59010"][0]} responses this month. <b>Ask every customer for the survey</b> and set the expectation of a 9–10 experience before they leave. <br><a href="nps/"><b>Open the NPS Focus page →</b></a>'
    CLEAN=clean_html(pub)
    BF_CARD=bf_card(pub)
    html=f'''<!DOCTYPE html>
    <html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Daily Huddle Board — Bridge Xfinity #59010 — {DATE_LONG} (MTD 10/1-{DATE_MD})</title>
    <style>
    :root{{--p:#6E2C91;--pl:#F5F0FA;--bd:#E3DCEC;--g:#1E7E34;--r:#C00000;--a:#B8720C;--t:#241F2E;--mut:#777}}
    *{{box-sizing:border-box}} body{{margin:0;font-family:'Segoe UI',Arial,sans-serif;color:var(--t);background:#fff;font-size:15px;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
    .wrap{{max-width:1040px;margin:0 auto;padding:14px 16px 30px}}
    header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:4px solid var(--p);padding-bottom:8px;gap:10px;flex-wrap:wrap}}
    header h1{{margin:0;font-size:24px;color:var(--p)}} header .s{{font-size:13px;color:#555}} header .d{{text-align:right;font-weight:700}} header .d small{{display:block;font-weight:400;color:#555}}
    .goalbar{{background:#FFF4CE;border:2px solid #E8B800;border-radius:8px;padding:8px 12px;margin:10px 0;text-align:center;font-weight:700;color:#6b5200}}
    nav{{display:flex;gap:6px;margin:8px 0;position:sticky;top:0;background:#fff;padding:6px 0;z-index:5}}
    nav a{{flex:1;text-align:center;background:var(--pl);border:1px solid #D9C7EC;border-radius:6px;padding:7px 2px;color:var(--p);font-weight:700;text-decoration:none;font-size:13px}}
    .sec{{margin-top:18px}}
    .band{{display:flex;align-items:center;gap:10px;background:var(--p);color:#fff;border-radius:8px;padding:8px 12px;margin-bottom:10px}}
    .band .n{{background:#fff;color:var(--p);width:26px;height:26px;border-radius:50%;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none}}
    .band b{{font-size:17px;text-transform:uppercase;letter-spacing:.3px}} .band span.sub{{display:block;font-size:12px;opacity:.9}}
    .grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
    .card{{border:1px solid var(--bd);border-radius:8px;padding:10px 12px;background:#fff}}
    .card h3{{margin:0 0 6px;font-size:14px;color:var(--p);text-transform:uppercase;letter-spacing:.3px}}
    .card.alert{{background:#FDECEA;border-color:var(--r)}} .card.alert h3{{color:var(--r)}}
    .card.green{{background:#EEF6EF;border-color:var(--g)}} .card.green h3{{color:var(--g)}}
    .card ul{{margin:0;padding-left:18px}} .card li{{margin:2px 0}}
    .tiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px}}
    .tile{{background:var(--pl);border:1px solid #D9C7EC;border-radius:8px;padding:8px 10px;text-align:center}}
    .tile .l{{font-size:11px;text-transform:uppercase;color:var(--p);font-weight:700}} .tile .v{{font-size:26px;font-weight:800;line-height:1.15}} .tile .x{{font-size:12px;color:var(--mut)}}
    .tile .v.red{{color:var(--r)}}
    table{{width:100%;border-collapse:collapse;font-size:14px}}
    th{{background:var(--p);color:#fff;font-size:11px;text-transform:uppercase;padding:6px 7px;text-align:right}} th:first-child,td.nm{{text-align:left}}
    td{{padding:6px 7px;text-align:right;border-bottom:1px solid #eee}} td.nm{{font-weight:600}}
    tr:nth-child(even) td{{background:#FBFAFC}} td.bad{{background:#FDE0E0!important;color:var(--r);font-weight:800}} tr.tot td{{background:#EDE3F5!important;font-weight:800}} tr.me td{{background:#F5F0FA!important;font-weight:800}}
    .tw{{overflow-x:auto;border:1px solid #eee;border-radius:8px}}
    .mut{{color:var(--mut);font-size:.85em;font-weight:400}}
    details{{margin-top:8px}} details:not([open])>*:not(summary){{display:none!important}} summary{{cursor:pointer;color:var(--p);font-weight:700;font-size:13px;padding:6px 0;list-style:none}} summary::before{{content:"▸ "}} details[open] summary::before{{content:"▾ "}}
    .nps{{display:flex;gap:18px;align-items:center;border:1px solid var(--bd);border-radius:8px;padding:10px 14px;flex-wrap:wrap}}
    .nps .big{{font-size:42px;font-weight:800;color:var(--r);line-height:1;text-align:center}} .nps .big small{{display:block;font-size:11px;color:var(--mut);font-weight:600}}
    .two{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}}
    .nowrap td,.nowrap th{{white-space:nowrap}}
    a{{color:var(--p)}} .goalbox{{background:#EAF6EC;border:2px solid var(--g);border-radius:8px;padding:10px 14px;margin-bottom:10px}}
    .goalbox b.t{{color:var(--g);text-transform:uppercase}}
    .foot{{font-size:11px;color:#999;margin-top:16px;text-align:center}}
    @media(max-width:760px){{.grid,.two{{grid-template-columns:1fr}} .tiles{{grid-template-columns:repeat(2,1fr)}} header h1{{font-size:20px}} header .d{{text-align:left}} table{{font-size:13px}}}}
    @page{{size:11in 8.5in landscape;margin:.3in}}
    @media print{{body{{font-size:11px}} nav{{display:none}} .wrap{{max-width:none;padding:0}} .sec{{break-after:page;margin-top:0}} .sec:last-of-type{{break-after:auto}} table{{font-size:10.5px}} .tile .v{{font-size:20px}} th{{font-size:9px}} td{{padding:3px 6px}} summary{{display:none}} details:not([open]){{display:none}} #ops{{break-after:auto}} #nps{{break-after:page}} .card{{break-inside:avoid}}}}
    </style></head><body><div class="wrap">
    <header><div><h1>Daily Huddle Board</h1><div class="s">Bridge Xfinity Store #59010 — Sunrise Plaza</div></div><div class="d">{DATE_LONG} (MTD 10/1-{DATE_MD})<small>Day {DAY} of {DIM} · {LEFT} days left</small></div></header>
    <div class="goalbar">🎯 GOAL: 125% OF PLAN = {GOAL} RGUs &nbsp;·&nbsp; we're at {ACT} &nbsp;·&nbsp; sell 35 a day to cover chargebacks &amp; refunds</div>
    <nav><a href="#ops">① Operations</a><a href="#nps">② NPS</a><a href="#results">③ Results</a><a href="#plan">④ Game Plan</a></nav>

    <section class="sec" id="ops"><div class="band"><span class="n">1</span><div><b>Operations &amp; Updates</b><span class="sub">Start here</span></div></div>
    <div class="grid">
    {BF_CARD}
    <div class="card"><h3>🌐 Internet pricing &amp; CSG codes</h3><details><summary>Show pricing table</summary><div class="tw"><table class="nowrap"><thead><tr><th>Speed tier</th><th>300 Mbps</th><th>500 Mbps</th><th>1 Gig</th><th>1.2 Gig</th><th>2 Gig</th></tr></thead><tbody>
    <tr><td class="nm">WiFi gateway · Unlimited data · Free line deal</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
    <tr><td class="nm">Peacock Premium</td><td>✗</td><td>✗</td><td>✓</td><td>✓</td><td>✓</td></tr>
    <tr><td class="nm">5-year deal ($ · CSG)</td><td>$45 · 2XC</td><td>$50 · 2XA</td><td>$60 · 2X6</td><td>$85 · 2X8</td><td>$85 · 2XB</td></tr>
    <tr><td class="nm">1-year deal ($ · CSG)</td><td>$40 · 2X7</td><td>$45 · 2X9</td><td>$50 · 2XE</td><td>$80 · 2X5</td><td>$80 · 2XD</td></tr>
    <tr><td class="nm">Everyday Price (EDP)</td><td>$70</td><td>$85</td><td>$100</td><td>$130</td><td>$130</td></tr></tbody></table></div></details></div>
    <div class="card green"><h3>⌚ New: Smartwatch Data Plan</h3><b>$10/mo · $0 activation · 5 GB talk &amp; text · its own phone number.</b> Works for new lines or BYOD, XMC eligible.<ul><li>Pitch it to <b>parents of young kids</b> and workout/errand customers</li><li>Apple &amp; Samsung only — <b>Google not eligible yet</b></li></ul>
    <details><summary>Show standalone vs. paired</summary><div class="tw"><table><thead><tr><th></th><th>Standalone (Data Plan)</th><th>Paired (Smartwatch fee)</th></tr></thead><tbody>
    <tr><td class="nm">Cost</td><td>$10/mo</td><td>$10/mo</td></tr><tr><td class="nm">Own number</td><td>Yes</td><td>No</td></tr><tr><td class="nm">Data</td><td>5 GB, then 5/2 Mbps</td><td>Uses phone's data</td></tr><tr><td class="nm">Watches</td><td>Apple, Samsung</td><td>Apple, Samsung, Google</td></tr><tr><td class="nm">Apple needs</td><td>iPhone 11+ · OS 26.1+</td><td>iPhone 6s+ · iOS 14+</td></tr></tbody></table></div><div class="mut" style="margin-top:4px">No international roaming or travel passes on watches ($0.30/MB pay-as-you-go on the paired line).</div></details></div>
    {CLEAN}
    </div>
    <div class="mut" style="margin-top:8px">BMOR standards: inventory counts solid · overtime ≤2% · zero Disco/Reco · No Usage under 10%</div></section>

    <section class="sec" id="nps"><div class="band"><span class="n">2</span><div><b>NPS</b><span class="sub">How customers rate us</span></div></div>
    <div class="nps"><div class="big"{NPS_STYLE}>{NPS_SCORE:.1f}<small>MTD · goal 90</small></div>
    <div style="flex:1;min-width:240px">{NPS_TEXT}</div></div></section>

    <section class="sec" id="results"><div class="band"><span class="n">3</span><div><b>Results</b><span class="sub">Where we are after Day {DAY}</span></div></div>
    <div class="tiles">
    <div class="tile"><div class="l">RGUs MTD</div><div class="v">{ACT}</div><div class="x">{ACT/TGT*100:.1f}% of {TGT} plan</div></div>
    <div class="tile"><div class="l">Goal (125%)</div><div class="v red">{GAP}</div><div class="x">to go · {GAP/LEFT:.1f}/day net</div></div>
    <div class="tile"><div class="l">Pace</div><div class="v">{PACE:.1f}/day</div><div class="x">need 35 · +{SELL-PACE:.1f} more</div></div>
    <div class="tile"><div class="l">XM+ Attach</div><div class="v{' red' if ATT0<65 else ''}">{ATT0:.0f}%</div><div class="x">goal 65% · {S['plus']} Plus units</div></div></div>
    <div class="two"><div class="card green"><h3>🏆 Wins</h3><ul>{WINS}</ul></div>
    <div class="card alert"><h3>👀 Focus</h3><ul>{FOCUS}</ul></div></div>
    <div class="tw"><table><thead><tr><th>Rep</th><th>RGUs</th><th>% of 75</th><th>TV</th><th>Tablets</th><th>XM+ Attach</th><th>ACC</th></tr></thead><tbody>{slim}</tbody></table></div>
    <div class="mut" style="margin-top:4px">Red = TV at 0, XM+ Attach under 65%, or $0 accessories.</div>
    <details open><summary>Show full rep detail (Internet, mobile, XM+ units, commissions)</summary><div class="tw"><table class="nowrap"><thead><tr><th>Rep</th><th>RGUs</th><th>Trend</th><th>Internet</th><th>TV</th><th>Mobile</th><th>Tablets</th><th>XM+ units</th><th>XM+ attach</th><th>XM+ earned</th><th>ACC</th></tr></thead><tbody>{full}</tbody></table></div></details>
    {MKT_SENT}
    <details open><summary>Show market table</summary><div class="tw"><table class="nowrap"><thead><tr><th>#</th><th>Store</th><th>RGUs / plan</th><th>Trend</th><th>Conv</th><th>TV</th><th>Tablets</th><th>Watches</th><th>XM+ attach</th><th>ACC</th><th>NPS</th></tr></thead><tbody>{mk}</tbody></table></div></details></div></section>

    <section class="sec" id="plan"><div class="band"><span class="n">4</span><div><b>Game Plan</b><span class="sub">What we do from here</span></div></div>
    <div class="goalbox"><b class="t">🎯 Goal: {GOAL} RGUs (125% of the {TGT} plan)</b> — 100% doesn't pay.<br>We need <b>{GAP} more, {GAP/LEFT:.1f} a day net</b>. Chargebacks and refunds pull RGUs back out, so <b>sell 35 a day</b> ({SELL*7} a week) for about {SELL*LEFT+ACT-GOAL} RGUs of cushion. We're at {PACE:.1f} a day — that's <b>about {math.ceil((SELL-PACE)*7/11)} more RGUs per rep, per week.</b><div class="mut" style="margin-top:4px">The plan moves with traffic and chargebacks ({PLAN_HIST}), so this resets daily.</div></div>
    <div class="two"><div class="card"><h3>The play call — every interaction</h3><ul><li><b>Internet → ask for TV</b> (only {S['tv']/S['int']*100:.0f}% attach today)</li><li><b>Every mobile line → Plus first</b>, Select as the step-down</li><li><b>Every walk-in → Internet + tablet + XM</b></li><li><b>Every device → accessory + a watch</b> ($10 Smartwatch Data Plan)</li></ul></div>
    <div class="card"><h3>This week, as a store</h3><ul><li><b>{SELL*7} RGUs</b> (35 a day)</li><li><b>~{RATE:.0f}% XM+ Attach</b> on every mobile-only sale</li><li><b>{round(TVN/LEFT*7)} TVs · {round(TABN/LEFT*7)} tablets · {round(WN/LEFT*7)} watches</b></li><li>Everyone: 75 RGUs · 4 TVs · 40 Plus · 65% attach · $450 ACC · 4 watches · 8 tablets · 90% NPS</li></ul></div></div>
    <div class="tw"><table><thead><tr><th>Rep — what you still need</th><th>RGUs per day to {SHARE}</th><th>TVs to 4</th><th>Tablets to 8</th><th>Watches to 4</th><th>ACC to $450</th></tr></thead><tbody>{gp}</tbody></table></div>
    <div class="mut" style="margin-top:4px">{SHARE} RGUs = each rep's equal share of selling 35 a day. Red = needing more than your current pace.</div>
    <details open><summary>Show store checkpoints</summary><div class="tw"><table class="nowrap"><thead><tr><th>By end of</th><th>RGUs @ 35/day</th><th>XM+ attach</th><th>TVs</th><th>Tablets</th><th>Watches</th></tr></thead><tbody><tr class="me"><td class="nm">Today (Day {DAY})</td><td>{ACT}</td><td>{ATT0:.0f}%</td><td>{S['tv']}</td><td>{STAB}</td><td>{S['wear']}</td></tr>{cp}</tbody></table></div><div class="mut" style="margin-top:4px">Only the RGU line moves with the plan; the rest are the fixed individual minimums spread evenly.</div></details>
    <details><summary>Show TV tiers (NFL/CFB)</summary><div class="tw"><table><thead><tr><th>Tier</th><th>$/mo</th><th>Key channels</th></tr></thead><tbody><tr><td class="nm">TV Core</td><td>$65</td><td>ABC, CBS, FOX, NBC</td></tr><tr><td class="nm">Sports &amp; News</td><td>$90</td><td>+ESPN/2, FS1/2, conf. networks (in-state), Peacock Premium</td></tr><tr><td class="nm">World Soccer Ticket</td><td>$95</td><td>+Deportes channels, X1 Box</td></tr><tr><td class="nm">TV Premium</td><td>$135</td><td>+NFL Network, ESPNU, ESPNEWS, conf. networks (out-of-state)</td></tr><tr><td class="nm">+ More Sports/Ent</td><td>$9.99</td><td>BTN (out-of-state), NFL RedZone</td></tr></tbody></table></div></details></section>
    <div class="foot">XM+ Attach = Plus ÷ Mobile Only · XM+ earned = Plus × $40 · Tablets = Mobile &amp; Tablet − Mobile Only</div>
    </div>
    </body></html>'''
    open(out,'w').write(html)
    print('div depth',len(re.findall(r'<div[\s>]',html))-len(re.findall(r'</div>',html)),len(html))

if __name__=='__main__':
    st=json.load(open(sys.argv[1])); pub=dt.date.fromisoformat(sys.argv[2]); build(st,pub,sys.argv[3])
