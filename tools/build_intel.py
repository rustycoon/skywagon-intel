#!/usr/bin/env python3
"""Skywagon Intel page generator.
Usage: python3 build_intel.py <listings.json> <photos dir> <serial_index.csv> <damage_digest.csv> <out dir>
Writes <out dir>/index.html, <out dir>/photos/*.jpg (thumbnails), <out dir>/data/<run_date>.json
"""
import json, csv, re, os, sys, html as H, statistics, datetime, shutil
from PIL import Image

LIST, PHOTOS, SIDX, DIG, OUT = sys.argv[1:6]
data = json.load(open(LIST))
L = data["listings"]
RUN = data["run_date"]
esc = H.escape
norm = lambda s: re.sub(r'[^A-Z0-9]', '', (s or '').upper()).lstrip('0')

# ---------- serial-spine lookups ----------
idx = list(csv.DictReader(open(SIDX)))
dig = list(csv.DictReader(open(DIG)))
by_serial = {norm(r['serial']): r for r in idx}
by_mark = {}
for r in idx:
    for m in re.split(r'[|,]', r['marks']):
        by_mark.setdefault(norm(m), []).append(r)
def screen(l):
    """returns (status, row, entries). status: ok | multi | none(no serial/tail) | nomatch"""
    row = None
    if l.get('serial'):
        row = by_serial.get(norm(l['serial']))
        if row is None: return ('nomatch', None, [])
    elif l.get('tail'):
        rows = by_mark.get(norm(l['tail']), [])
        if len(rows) > 1: return ('multi', None, [])
        if not rows: return ('nomatch', None, [])
        row = rows[0]
    else:
        return ('none', None, [])
    marks = [norm(m) for m in re.split(r'[|,]', row['marks'])]
    ents = [e for e in dig if norm(e['serial']) == norm(row['serial']) or norm(e['mark']) in marks]
    ents.sort(key=lambda e: e['date'])
    return ('ok', row, ents)

# ---------- helpers ----------
DMG={'SUBS':'SUBSTANTIAL','DEST':'DESTROYED','MIN':'MINOR','MINOR':'MINOR','NONE':'NONE','UNK':'UNKNOWN','SUBSTANTIAL':'SUBSTANTIAL','DESTROYED':'DESTROYED','INCIDENT':'INCIDENT'}
FLAG = {"US":"🇺🇸","CA":"🇨🇦","VE":"🇻🇪","CH":"🇨🇭","BE":"🇧🇪","FR":"🇫🇷","GB":"🇬🇧","PL":"🇵🇱","NO":"🇳🇴","ZA":"🇿🇦","NA":"🇳🇦","NZ":"🇳🇿","IS":"🇮🇸"}
def flag(l):
    c = l.get('country','')
    f = FLAG.get(c, '🏳️')
    return f if c in ('US','CA') else f + ' <span class="foreign">foreign</span>'
def money(n):
    return "$%s" % format(n, ",") if n is not None else ""
def kprice(n):
    if n is None: return "call"
    return "$%dk" % round(n/1000) if n % 1000 == 0 or n >= 100000 else money(n)

# Likely installed engine from the type certificates (TCDS 3A24 for the 185, 5A6 for the 180).
def likely_engine(l):
    if l.get('engine'): return None
    m = (l.get('model') or '').upper()
    if m in ('185','185A','185B','185C','185D','185E'): return "Continental IO-470-F, 260 hp"
    if m in ('A185E','A185F','185F'): return "Continental IO-520-D, 300 hp"
    if m in ('180',): return "Continental O-470-A, O-470-J or O-470-K, 225–230 hp"
    if m in ('180A','180B'): return "Continental O-470-K, 230 hp"
    if m in ('180C','180D','180E','180F','180G','180H'): return "Continental O-470-L or O-470-R, 230 hp"
    if m == '180J': return "Continental O-470-R or O-470-S, 230 hp"
    if m == '180K': return "Continental O-470-U, 230 hp"
    return None

# ---------- thumbnails ----------
os.makedirs(os.path.join(OUT,'photos'), exist_ok=True)
os.makedirs(os.path.join(OUT,'data'), exist_ok=True)
for l in L:
    k = l.get('photo')
    if not k: continue
    src = os.path.join(PHOTOS, k + '.jpg')
    if not os.path.exists(src): l['photo'] = None; continue
    im = Image.open(src).convert('RGB')
    w, h = im.size; tw = 224; th = round(h * tw / w)
    im = im.resize((tw, th));
    # crop to 4:3
    ch = round(tw * 3/4)
    if th > ch: top = (th-ch)//2; im = im.crop((0, top, tw, top+ch))
    im.save(os.path.join(OUT,'photos', k + '.jpg'), quality=72, optimize=True)

# ---------- numbers ----------
priced = [l['price'] for l in L if l.get('price') is not None]
median = statistics.median(priced); mean = statistics.mean(priced)
n_us = sum(1 for l in L if l['country']=='US'); n_ca = sum(1 for l in L if l['country']=='CA'); n_other = len(L)-n_us-n_ca
n180 = sum(1 for l in L if (l.get('model') or '').startswith('180'))

# ---------- rows ----------
def sort_key(l):
    return (l.get('price') is None, l.get('price') or 0)
L_sorted = sorted(L, key=sort_key)

def record_summary(l):
    st, row, ents = screen(l)
    if st == 'none': return ('nosn', 'no serial or tail published · not screened')
    if st == 'multi': return ('multi', 'more than one aircraft has worn this mark · not screened')
    if st == 'nomatch': return ('nomatch', 'serial not in the record · not screened')
    c = sum(int(row[k]) for k in ('ntsb','tsb','sdr','aids'))
    if c == 0: return ('clean', 'no entries found')
    parts = [f"{row[k]} {k.upper()}" for k in ('ntsb','tsb','sdr','aids') if int(row[k])]
    return ('entries', ' · '.join(parts))

def row_html(l):
    st, row, ents = screen(l)
    rk, rtext = record_summary(l)
    ymodel = f"{l.get('year') or ''} Cessna {esc(l.get('model') or '')}".strip()
    tail = f'<span class="tail">{esc(l["tail"])}</span>' if l.get('tail') else '<span class="tail mute">tail not published</span>'
    thumb = f'<img src="photos/{l["photo"]}.jpg" alt="" loading="lazy">' if l.get('photo') else '<div class="noimg">no photo</div>'
    pm = ''
    if l.get('price_was') is not None and l.get('price') is not None:
        up = l['price'] > l['price_was']
        pm = f'<div class="pm {"up" if up else "down"}">{"up" if up else "down"} from {money(l["price_was"])}</div>'
    mnum = re.search(r'[0-9][0-9,]*(?:\.[0-9]+)?', l.get('tt') or '')
    hrs = (('about ' if (l.get('tt') or '').lower().startswith('about') else '') + f'{esc(mnum.group(0))} hrs') if mnum else 'hours not published'
    loc = esc(l.get('location','').split(' (')[0])
    # details
    fields = []
    def F(label, val):
        if val: fields.append((label, val))
    F('Asking', (money(l['price']) if l.get('price') is not None else '') + (f' <span class="mute">· {esc(l["price_note"])}</span>' if l.get('price_note') else ''))
    F('Serial', f'<span class="mono">{esc(l["serial"])}</span>' if l.get('serial') else (esc(l.get('serial_note')) if l.get('serial_note') else None))
    F('Airframe', esc(l['tt']) + ' hrs, as advertised' if l.get('tt') else None)
    le = likely_engine(l)
    if l.get('engine'): F('Engine', esc(l['engine']))
    elif le: F('Engine', f'Not named in the ad. <span class="likely">Likely installed: {esc(le)} — the factory engine for this model per the type certificate. Not confirmed by the ad.</span>')
    F('Prop', esc(l.get('prop','')))
    F('Gear', esc(l.get('gear','')))
    F('Fuel', esc(l.get('fuel','')))
    F('Mods', esc(l.get('mods','')) + (' · as advertised' if l.get('mods') else ''))
    F('Panel', esc(l.get('panel','')))
    F('Weights', ' · '.join(x for x in [('empty ' + l['empty_weight']) if l.get('empty_weight') else '', ('useful load ' + l['useful_load']) if l.get('useful_load') else ''] if x))
    F('Annual', esc(l.get('annual','')))
    F('History', esc(l.get('history','')))
    F('Registry', esc(l.get('registry','')))
    if l.get('tail_note'): F('Tail', esc(l['tail_note']))
    if l.get('posted'): F('Posted', esc(l['posted']))
    # record line
    if rk == 'entries':
        F('Record', esc(rtext) + f' · <a href="#rec-{l["key"]}">see the entries below</a>' + (f' <span class="mute">(matched by registration; the record lists serial {esc(row["serial"])})</span>' if not l.get('serial') else ''))
    elif rk == 'clean':
        F('Record', 'NTSB 0 · TSB 0 · SDR 0 · AIDS 0 · no entries found' + (f' <span class="mute">(matched by registration; the record lists serial {esc(row["serial"])})</span>' if not l.get('serial') else ''))
    else:
        F('Record', esc(rtext))
    F('Seen', ('first ' + esc(l['first_seen']) + ' · ' if l.get('first_seen') else '') + 'last ' + RUN)
    dl = ''.join(f'<div class="k">{k}</div><div class="v">{v}</div>' for k, v in fields)
    # contact
    btns = ''.join(f'<a class="btn" href="tel:{re.sub(r"[^0-9+]","",p)}">Call {esc(p)}</a>' for p in l.get('phone', []))
    btns += ''.join(f'<a class="btn" href="mailto:{esc(e)}">Email</a>' for e in l.get('email', []))
    seller = esc(l.get('seller','Contact through the ad'))
    srcs = ''.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a>' for n, u in l.get('sources', []))
    pnum = l['price'] if l.get('price') is not None else 10**12
    ynum = l.get('year') or 0
    hnum = float(mnum.group(0).replace(',','')) if mnum else 10**9
    return f'''<details class="row" id="r-{l["key"]}" data-price="{pnum}" data-year="{ynum}" data-hrs="{hnum}" data-country="{esc(l["country"])}" data-rec="{rk}">
<summary>
<div class="ph">{thumb}</div>
<div class="mid"><div class="ym">{ymodel} {tail}</div><div class="sub">{flag(l)} {loc} · {hrs} · {esc(rtext)}</div></div>
<div class="right"><div class="price">{kprice(l.get("price"))}</div>{pm}</div>
</summary>
<div class="det">
<div class="dl">{dl}</div>
<div class="contact"><div class="seller">{seller}</div><div class="btns">{btns}</div></div>
<div class="srcs"><div class="mute small">Advertised on</div><div class="srclinks">{srcs}</div></div>
</div>
</details>'''

rows = '\n'.join(row_html(l) for l in L_sorted)

# ---------- record per tail ----------
recs = []
for l in L_sorted:
    st, row, ents = screen(l)
    if st != 'ok': continue
    c = sum(int(row[k]) for k in ('ntsb','tsb','sdr','aids'))
    if c == 0: continue
    ymodel = f"{l.get('year') or ''} Cessna {esc(l.get('model') or '')}".strip()
    head = (f'<span class="tail">{esc(l["tail"])}</span>' if l.get('tail') else 'tail not published') + f' · serial <span class="mono">{esc(row["serial"])}</span> · {ymodel} · {flag(l)} {esc(l.get("location","").split(" (")[0])} · {money(l["price"]) if l.get("price") is not None else "price not published"}'
    lines = ''
    if l.get('registry'): lines += f'<div class="k">Registry</div><div class="v">{esc(l["registry"])}</div>'
    counts = ' · '.join(f"{k.upper()} {row[k]}" for k in ('ntsb','tsb','sdr','aids'))
    lines += f'<div class="k">Counts</div><div class="v">{counts}</div>'
    if ents:
        for e in ents:
            lines += f'<div class="k">{esc(e["source"])}</div><div class="v">{esc(e["date"])} · <b>{esc(DMG.get(e["damage"].strip().upper(), e["damage"]))}</b> · {esc(e["summary"])}' + (f' <span class="mute">(as {esc(e["mark"])})</span>' if norm(e["mark"]) != norm(l.get("tail") or "") else '') + '</div>'
    else:
        lines += '<div class="k">Entries</div><div class="v">Counts are on file for this serial; the entry text is not yet in this record.</div>'
    if len(re.split(r'[|,]', row['marks'])) > 1:
        lines += f'<div class="k">Marks</div><div class="v">This serial has also been registered as {esc(row["marks"].replace("|", ", ").replace(",", ", "))}</div>'
    recs.append(f'<div class="rec" id="rec-{l["key"]}"><div class="rech">{head}</div><div class="dl">{lines}</div></div>')
recs_html = '\n'.join(recs)

# ---------- since yesterday ----------
since = data.get('since_text') or ''
if not since:
    parts = []
    if data.get('new'): parts.append(f"{len(data['new'])} new listing{'s' if len(data['new'])!=1 else ''} came on.")
    else: parts.append("Nothing new came on the market.")
    for d in data.get('departed', []):
        parts.append(f"The {d['year']} {d['model']} in {d['location']} has gone: {d['how']} Last asking {money(d['last_price'])} at {d['tt']} hours.")
    moves = [l for l in L if l.get('price_was') is not None and l.get('price') is not None]
    if moves:
        ms = []
        for l in moves:
            name = f"{l['tail']}" if l.get('tail') else f"the {l.get('year','')} {l.get('model','')} in {l.get('location','').split(' (')[0]}"
            ms.append(f"{name} went {'up' if l['price']>l['price_was'] else 'down'} from {money(l['price_was'])} to {money(l['price'])}")
        parts.append(("One price moved: " if len(ms)==1 else f"{len(ms)} prices moved: ") + '; '.join(ms) + '.')
    else: parts.append("No asking price moved.")
    since = ' '.join(parts)

sources_ok = data.get('sources_ok') or []
sources_fail = data.get('sources_fail') or []
sources_skip = data.get('sources_skip') or []

CSS = r'''
:root{--bg:#F2F3F0;--card:#FFFFFF;--ink:#1B2430;--mute:#5C6670;--line:#D9DCD6;--acc:#B5185C;--link:#1F4E79;--ok:#1D6F5B;--warn:#8A5A00;--warnbg:#FBEFD2;--bad:#A3261E;--tint:#B8BDB7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#151A20;--card:#1E252E;--ink:#ECEEF0;--mute:#A3ACB6;--line:#333C47;--acc:#F06A9F;--link:#8FBCE8;--ok:#8FD4BE;--warn:#F2C56B;--warnbg:#4A3810;--bad:#F4A19A;--tint:#2A323C}}
:root[data-theme="dark"]{--bg:#151A20;--card:#1E252E;--ink:#ECEEF0;--mute:#A3ACB6;--line:#333C47;--acc:#F06A9F;--link:#8FBCE8;--ok:#8FD4BE;--warn:#F2C56B;--warnbg:#4A3810;--bad:#F4A19A;--tint:#2A323C}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:14px;line-height:1.45}
a{color:var(--link)} a:hover{color:var(--acc)}
.wrap{max-width:1040px;margin:0 auto;padding:18px 16px 48px}
h1{font-family:"Barlow Condensed","Arial Narrow",sans-serif;font-weight:600;font-size:34px;line-height:1;letter-spacing:.01em;margin:0}
h2{font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:22px;margin:0;border-bottom:2px solid var(--acc);display:inline-block;padding-bottom:2px}
.sec{margin-top:22px;display:flex;flex-direction:column;gap:8px}
.sub{color:var(--mute);font-size:13px}
.mute{color:var(--mute)} .small{font-size:12px}
.mono{font-family:"IBM Plex Mono",monospace;font-size:12.5px}
.caveat{border:2px solid var(--acc);padding:10px 12px;display:flex;flex-direction:column;gap:6px;margin-top:14px}
.caveat .h{font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:19px;color:var(--acc)}
.caveat .src{font-size:12.5px;color:var(--mute);border-top:1px solid var(--line);padding-top:6px}
.caveat .src b{color:var(--ink);font-weight:500}
.tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
@media (min-width:700px){.tiles{grid-template-columns:repeat(4,minmax(0,1fr))}}
.tile{background:var(--card);border:1px solid var(--line);padding:8px 10px}
.tile .l{font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--mute)}
.tile .v{font-family:"Barlow Condensed",sans-serif;font-size:26px;font-weight:600;line-height:1.1;font-variant-numeric:tabular-nums}
.tile .d{font-size:11.5px;color:var(--mute)}
.tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12.5px;color:var(--mute)}
.tools button{font:inherit;font-size:12.5px;background:var(--card);border:1px solid var(--line);color:var(--ink);padding:6px 10px;min-height:32px;cursor:pointer}
.tools button[aria-pressed="true"]{border-color:var(--acc);color:var(--acc)}
.rows{display:flex;flex-direction:column;gap:6px}
.row{background:var(--card);border:1px solid var(--line)}
.row[open]{border-color:var(--acc)}
.row summary{list-style:none;display:grid;grid-template-columns:56px 1fr auto;gap:10px;align-items:center;padding:8px;cursor:pointer;min-height:58px}
.row summary::-webkit-details-marker{display:none}
.ph{width:56px;height:42px;background:var(--tint);display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.noimg{font-size:10px;color:var(--mute)}
.mid{min-width:0}
.ym{font-weight:500}
.tail{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--acc)} .tail.mute{color:var(--mute)}
.sub2,.sub{font-size:12.5px;color:var(--mute)}
.mid .sub{overflow:hidden;text-overflow:ellipsis}
.right{text-align:right}
.price{font-family:"Barlow Condensed",sans-serif;font-size:24px;font-weight:600;line-height:1;white-space:nowrap}
.pm{font-size:11px;white-space:nowrap} .pm.up{color:var(--bad)} .pm.down{color:var(--ok)}
.foreign{color:var(--bad);font-weight:600}
.det{border-top:1px solid var(--line);padding:10px 10px 12px;display:flex;flex-direction:column;gap:10px;font-size:13px}
.dl{display:grid;grid-template-columns:92px 1fr;row-gap:5px;column-gap:8px}
.dl .k{color:var(--mute)} .dl .v{min-width:0;overflow-wrap:anywhere}
.likely{background:var(--warnbg);color:var(--warn);padding:1px 6px;font-size:12px}
.contact{border-top:1px solid var(--line);padding-top:8px;display:flex;flex-direction:column;gap:4px}
.seller{font-weight:500}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--link);color:var(--link);text-decoration:none;font-weight:500}
.srcs{border-top:1px solid var(--line);padding-top:8px}
.srclinks{display:flex;gap:10px;flex-wrap:wrap;font-size:13px}
.rec{background:var(--card);border:1px solid var(--line);padding:10px;font-size:13px;display:flex;flex-direction:column;gap:6px}
.rech{overflow-wrap:anywhere}
.srcgrid{display:grid;grid-template-columns:120px 1fr;gap:4px 8px;font-size:13px}
.foot{margin-top:26px;font-size:12px;color:var(--mute);border-top:1px solid var(--line);padding-top:10px}
@media (min-width:700px){.row summary{grid-template-columns:72px 1fr auto}.ph{width:72px;height:54px}.dl{grid-template-columns:110px 1fr}}
'''

JS = r'''
(function(){
  var rows=document.getElementById('rows');
  function sortBy(key,dir){
    var items=Array.prototype.slice.call(rows.querySelectorAll('.row'));
    items.sort(function(a,b){
      var av=a.dataset[key], bv=b.dataset[key];
      if(key==='country'){ var o={US:0,CA:1}; av=(o[av]!==undefined?o[av]:2)+av; bv=(o[bv]!==undefined?o[bv]:2)+bv; return av<bv?-1:av>bv?1:0; }
      av=parseFloat(av); bv=parseFloat(bv); return dir*(av-bv);
    });
    items.forEach(function(el){rows.appendChild(el)});
    document.querySelectorAll('.tools button').forEach(function(b){b.setAttribute('aria-pressed', b.dataset.key===key && String(b.dataset.dir)===String(dir));});
  }
  document.querySelectorAll('.tools button').forEach(function(b){
    b.addEventListener('click',function(){sortBy(b.dataset.key,parseInt(b.dataset.dir,10));});
  });
  var h=location.hash.replace('#','');
  if(h){var el=document.getElementById(h); if(el&&el.tagName==='DETAILS'){el.open=true;}}
})();
'''

date_long = datetime.date.fromisoformat(RUN).strftime('%A, %B %-d, %Y')
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skywagon Intel</title>
<meta name="description" content="A facts-only record of every Cessna 180 and 185 advertised for sale, refreshed daily. Asking prices, airframe and engine times, equipment, seller contact, and the public accident and service record for each serial.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Skywagon Intel</h1>
<div class="sub">Cessna 180 and 185 market record · {date_long}</div>

<div class="caveat">
<div class="h">A clean record is not proof.</div>
<div>Nothing found in the accident and service databases is a strong sign, not a guarantee. Form 337s and the logbooks are still mandatory before any purchase.</div>
<div class="src"><b>Where this comes from.</b> Asking prices, times and equipment are copied from each seller's advertisement on Trade-A-Plane, Controller, Barnstormers, Hangar67, Craigslist, Facebook Marketplace, AircraftForSale, GlobalAir, GlobalPlaneSearch, FindAircraft, Kijiji and dealer sites, and are not verified. Tail, serial, owner and airworthiness class come from the FAA and Transport Canada registries. Records come from the NTSB, the Transportation Safety Board of Canada, FAA Service Difficulty Reports and the FAA Accident/Incident Data System. Nothing here is this site's opinion. Where two sites disagree, both figures are shown.</div>
</div>

<div class="sec">
<h2>Since yesterday</h2>
<p style="margin:0">{esc(since)}</p>
</div>

<div class="sec">
<div class="tiles">
<div class="tile"><div class="l">Listings</div><div class="v">{len(L)}</div><div class="d">{len(priced)} with a price</div></div>
<div class="tile"><div class="l">Median ask</div><div class="v">${median/1000:,.0f}k</div><div class="d">USD, priced only</div></div>
<div class="tile"><div class="l">Mean ask</div><div class="v">${mean/1000:,.0f}k</div><div class="d">USD, priced only</div></div>
<div class="tile"><div class="l">Where</div><div class="v">{n_us} · {n_ca} · {n_other}</div><div class="d">US · Canada · elsewhere</div></div>
</div>
</div>

<div class="sec">
<div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px"><h2>The market</h2><div class="sub">tap a row for the full ad facts</div></div>
<div class="tools">Sort:
<button data-key="price" data-dir="1" aria-pressed="true">cheapest first</button>
<button data-key="price" data-dir="-1">dearest first</button>
<button data-key="hrs" data-dir="1">lowest hours</button>
<button data-key="year" data-dir="-1">newest</button>
<button data-key="year" data-dir="1">oldest</button>
<button data-key="country" data-dir="1">by country</button>
</div>
<div class="rows" id="rows">
{rows}
</div>
</div>

<div class="sec">
<h2>Record per tail</h2>
<div class="sub">Every serial in the table with an entry in the NTSB, TSB, SDR or AIDS databases, as the source recorded it. An entry here is a matter of public record, not a judgment about the aircraft or the seller.</div>
{recs_html}
</div>

<div class="sec">
<h2>Sources</h2>
<div class="srcgrid">
<div class="mute">Checked today</div><div>{esc(', '.join(sources_ok))}</div>
<div class="mute">Did not answer</div><div>{esc(', '.join(sources_fail)) or 'none'}</div>
<div class="mute">Not checked</div><div>{esc(', '.join(sources_skip)) or 'none'}</div>
</div>
<div class="sub">Run at {esc(data.get('run_time',''))}. {esc(data.get('provenance',''))}</div>
</div>

<div class="foot">Skywagon Intel is an automated daily record. Listings leave this page the day their advertisement can no longer be found. Nothing is sold here and no seller is affiliated with this site.</div>
</div>
<script>{JS}</script>
</body>
</html>'''
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page)
shutil.copy(LIST, os.path.join(OUT,'data', f'{RUN}.json'))
print('wrote', os.path.join(OUT,'index.html'), len(page)//1024, 'KB;', len(L), 'rows;', len(recs), 'records;', sum(1 for l in L if l.get('photo')), 'photos')