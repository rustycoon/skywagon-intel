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
SPECIFIC = re.compile(r'listing_id=|/listing/|/listings?/for-sale/\d|/item/|/posts/|/permalink/|classified-\d|/aircraft/\d|/view/d/|/aircraft/[a-z0-9-]+-\d|/aircraft/\d{4}-')
def dedupe_sources(srcs):
    """One link per site, unless a site carries two different ads. Links that open the ad itself
    replace category or search pages for the same site."""
    groups = {}; order = []
    for n, u in srcs:
        base = re.sub(r'\s*\(.*\)$', '', n).strip()
        if base not in groups: order.append(base); groups[base] = []
        groups[base].append((n, u))
    out = []
    for b in order:
        items = groups[b]
        spec = []; seen = set()
        for n, u in items:
            if SPECIFIC.search(u or '') and u not in seen: spec.append((n, u)); seen.add(u)
        keep = spec if spec else items[:1]
        for i, (n, u) in enumerate(keep):
            if i and not re.search(r'\(.*\)$', n): n = f'{n} (another ad)'
            out.append((n, u))
    return out

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

# Likely installed engine from the type certificates. Verified 2026-10-14 against FAA TCDS 5A6 rev 68 (180 series)
# and TCDS 3A24 rev 40 (185 series): 185/185A-E IO-470-F 260 hp; A185E/A185F IO-520-D 300 hp; 180 O-470-A/J/K 225-230 hp;
# 180A-B O-470-K; 180C-H O-470-L/R; 180J O-470-R (s/n to 18052500) or O-470-S (18052501 up); 180K O-470-U. All 230 hp.
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
    if not os.path.exists(src):
        # no new source image: keep the thumbnail already published, drop the photo only if none exists
        if os.path.exists(os.path.join(OUT,'photos', k + '.jpg')): continue
        l['photo'] = None; continue
    im = Image.open(src).convert('RGB')
    big = im.copy()
    if big.size[0] > 896: big = big.resize((896, round(big.size[1]*896/big.size[0])))
    big.save(os.path.join(OUT,'photos', k + '_l.jpg'), quality=80, optimize=True)
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

def counts_from(row, ents):
    """Entries decide. The index's count columns are stale for ~400 rows (mostly 180s), so derive
    counts from the digest entries when they disagree. Returns (counts dict, disagree flag)."""
    idxc = {k: int(row[k]) for k in ('ntsb','tsb','sdr','aids')}
    dc = {'ntsb':0,'tsb':0,'sdr':0,'aids':0}
    for e in ents:
        src = e['source'].strip().upper()
        if src.startswith('NTSB'): dc['ntsb'] += 1
        elif src.startswith('TSB'): dc['tsb'] += 1
        elif src.startswith('SDR'): dc['sdr'] += 1
        elif src.startswith('AIDS'): dc['aids'] += 1
    use = {k: max(idxc[k], dc[k]) for k in idxc}
    return use, (sum(idxc.values()) == 0 and sum(dc.values()) > 0)

def record_summary(l):
    st, row, ents = screen(l)
    if st == 'none': return ('nosn', 'no serial or tail published · not screened')
    if st == 'multi': return ('multi', 'more than one aircraft has worn this mark · not screened')
    if st == 'nomatch': return ('nomatch', 'serial not in the record · not screened')
    use, _ = counts_from(row, ents)
    c = sum(use.values())
    if c == 0: return ('clean', 'no entries found')
    parts = [f"{use[k]} {k.upper()}" for k in ('ntsb','tsb','sdr','aids') if use[k]]
    return ('entries', ' · '.join(parts))

def row_html(l):
    st, row, ents = screen(l)
    rk, rtext = record_summary(l)
    ymodel = f"{l.get('year') or ''} Cessna {esc(l.get('model') or '')}".strip()
    tail = f'<div class="tail">{esc(l["tail"])}</div>' if l.get('tail') else '<div class="tail none">tail not published</div>'
    thumb = f'<a class="zoom" href="photos/{l["photo"]}_l.jpg" aria-label="Enlarge photo"><img src="photos/{l["photo"]}.jpg" alt="" loading="lazy"></a>' if l.get('photo') else '<div class="noimg">no photo</div>'
    pm = ''
    if l.get('price_was') is not None and l.get('price') is not None:
        up = l['price'] > l['price_was']
        pm = f'<div class="pm {"up" if up else "down"}">{"up" if up else "down"} from {money(l["price_was"])}</div>'
    mnum = re.search(r'[0-9][0-9,]*(?:\.[0-9]+)?', l.get('tt') or '')
    hrs = (('about ' if (l.get('tt') or '').lower().startswith('about') else '') + f'{esc(mnum.group(0))} airframe hrs') if mnum else 'airframe hours not published'
    loc = esc(l.get('location','').split(' (')[0])
    kind = f' · <span class="kind">{esc(l["kind"])}</span>' if l.get('kind') else ''
    # details
    fields = []
    def F(label, val):
        if val: fields.append((label, val))
    F('Asking', (money(l['price']) if l.get('price') is not None else '') + (f' <span class="mute">· {esc(l["price_note"])}</span>' if l.get('price_note') else ''))
    F('Serial', f'<span class="mono">{esc(l["serial"])}</span>' if l.get('serial') else (esc(l.get('serial_note')) if l.get('serial_note') else None))
    F('Airframe', esc(l['tt']) + ' airframe hrs, as advertised' if l.get('tt') else 'airframe hours not published')
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
    # the full ad, in the seller's own words
    full = ''
    for ad in l.get('ad_sections', []):
        secs = ''.join(f'<div class="adsec"><div class="adh">{esc(h)}</div><div class="adt">{esc(t.strip()).replace(chr(10), "<br>")}</div></div>' for h, t in ad['sections'].items() if t and t.strip())
        if secs: full += f'<div class="fullad"><div class="mute small">The full ad, as the seller wrote it on <a href="{esc(ad["url"])}" target="_blank" rel="noopener">{esc(ad["source"])}</a></div>{secs}</div>'
    # contact
    btns = ''.join(f'<a class="btn" href="tel:{re.sub(r"[^0-9+]","",p)}">Call {esc(p)}</a>' for p in l.get('phone', []))
    btns += ''.join(f'<a class="btn" href="mailto:{esc(e)}">Email</a>' for e in l.get('email', []))
    seller = esc(l.get('seller','Contact through the ad'))
    srcs = ''.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a>' for n, u in dedupe_sources(l.get('sources', [])))
    pnum = l['price'] if l.get('price') is not None else 10**12
    ynum = l.get('year') or 0
    hnum = float(mnum.group(0).replace(',','')) if mnum else 10**9
    return f'''<details class="row" id="r-{l["key"]}" data-price="{pnum}" data-year="{ynum}" data-hrs="{hnum}" data-country="{esc(l["country"])}" data-rec="{rk}">
<summary>
<div class="ph">{thumb}</div>
<div class="mid">{tail}<div class="ym">{ymodel}</div><div class="sub">{flag(l)} {loc}{kind} · {hrs} · {esc(rtext)}</div></div>
<div class="right"><div class="price">{kprice(l.get("price"))}</div>{pm}</div>
</summary>
<div class="det">
<div class="dl">{dl}</div>
{full}
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
    use, disagree = counts_from(row, ents)
    c = sum(use.values())
    if c == 0: continue
    ymodel = f"{l.get('year') or ''} Cessna {esc(l.get('model') or '')}".strip()
    head = (f'<span class="tail">{esc(l["tail"])}</span>' if l.get('tail') else 'tail not published') + f' · serial <span class="mono">{esc(row["serial"])}</span> · {ymodel} · {flag(l)} {esc(l.get("location","").split(" (")[0])} · {money(l["price"]) if l.get("price") is not None else "price not published"}'
    lines = ''
    if l.get('registry'): lines += f'<div class="k">Registry</div><div class="v">{esc(l["registry"])}</div>'
    counts = ' · '.join(f"{k.upper()} {use[k]}" for k in ('ntsb','tsb','sdr','aids'))
    if disagree: counts += ' <span class="mute">(the summary index listed none for this serial; the entries below are what the databases hold, and they are what this page reports)</span>'
    lines += f'<div class="k">Counts</div><div class="v">{counts}</div>'
    if ents:
        for e in ents:
            lines += f'<div class="k">{esc(e["source"])}</div><div class="v">{esc(e["date"])} · <b>{esc(DMG.get(e["damage"].strip().upper(), e["damage"]))}</b> · {esc(e["summary"])}' + (f' <span class="mute">(as {esc(e["mark"])})</span>' if norm(e["mark"]) != norm(l.get("tail") or "") else '') + '</div>'
    else:
        lines += '<div class="k">Entries</div><div class="v">Counts are on file for this serial; the entry text is not yet in this record.</div>'
    if len(re.split(r'[|,]', row['marks'])) > 1:
        lines += f'<div class="k">Marks</div><div class="v">This serial has also been registered as {esc(row["marks"].replace("|", ", ").replace(",", ", "))}</div>'
    recs.append(f'<div class="rec" id="rec-{l["key"]}"><div class="rech"><div>{head}</div><a class="back" href="#r-{l["key"]}">↑ back to this listing</a></div><div class="dl">{lines}</div></div>')
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
.zoom{display:block;width:100%;height:100%}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.82);display:none;align-items:center;justify-content:center;z-index:50;padding:16px}
#lb.on{display:flex}
#lb img{max-width:92vw;max-height:90vh;height:auto;box-shadow:0 8px 40px rgba(0,0,0,.5)}
#lb .x{position:absolute;top:10px;right:12px;min-width:44px;min-height:44px;background:transparent;border:0;color:#fff;font-size:28px;cursor:pointer}
.noimg{font-size:10px;color:var(--mute)}
.mid{min-width:0}
.ym{font-weight:500}
.tail{font-family:"IBM Plex Mono",monospace;font-size:24px;font-weight:500;line-height:1.05;color:var(--acc);letter-spacing:.01em}
.tail.none{font-size:13px;color:var(--mute);font-weight:400;line-height:1.3}
.sub2,.sub{font-size:12.5px;color:var(--mute)}
.mid .sub{overflow:hidden;text-overflow:ellipsis}
.right{text-align:right}
.price{font-family:"Barlow Condensed",sans-serif;font-size:24px;font-weight:600;line-height:1;white-space:nowrap}
.pm{font-size:11px;white-space:nowrap} .pm.up{color:var(--bad)} .pm.down{color:var(--ok)}
.foreign{color:var(--bad);font-weight:600}
.kind{color:var(--warn);font-weight:600}
.how{background:var(--card);border:1px solid var(--line)}
.how summary{list-style:none;cursor:pointer;padding:10px 12px;font-weight:500;display:flex;justify-content:space-between;align-items:center;min-height:44px}
.how summary::-webkit-details-marker{display:none}
.how summary::after{content:"show";color:var(--link);font-weight:400;font-size:13px}
.how[open] summary::after{content:"hide"}
.how .body{border-top:1px solid var(--line);padding:10px 12px 12px;font-size:13.5px;display:flex;flex-direction:column;gap:8px}
.how p{margin:0} .how b{font-weight:500}
.det{border-top:1px solid var(--line);padding:10px 10px 12px;display:flex;flex-direction:column;gap:10px;font-size:13px}
.dl{display:grid;grid-template-columns:92px 1fr;row-gap:5px;column-gap:8px}
.dl .k{color:var(--mute)} .dl .v{min-width:0;overflow-wrap:anywhere}
.fullad{border-top:1px solid var(--line);padding-top:8px;display:flex;flex-direction:column;gap:8px}
.adh{font-weight:500;margin-bottom:2px} .adt{overflow-wrap:anywhere;line-height:1.45}
.likely{background:var(--warnbg);color:var(--warn);padding:1px 6px;font-size:12px}
.contact{border-top:1px solid var(--line);padding-top:8px;display:flex;flex-direction:column;gap:4px}
.seller{font-weight:500}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--link);color:var(--link);text-decoration:none;font-weight:500}
.srcs{border-top:1px solid var(--line);padding-top:8px}
.srclinks{display:flex;gap:10px;flex-wrap:wrap;font-size:13px}
.rec{background:var(--card);border:1px solid var(--line);padding:10px;font-size:13px;display:flex;flex-direction:column;gap:6px}
.rech{overflow-wrap:anywhere;display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap} .rech .tail{font-size:20px;display:inline}
.back{white-space:nowrap;font-size:13px;min-height:44px;display:inline-flex;align-items:center}
.rec:target,.row:target{outline:2px solid var(--acc);outline-offset:2px}
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
      var U=1e11, au=parseFloat(a.dataset.price)>=U, bu=parseFloat(b.dataset.price)>=U; if(au!==bu) return au?1:-1;
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
  function openHash(){var h=location.hash.replace('#',''); if(!h) return; var el=document.getElementById(h); if(el&&el.tagName==='DETAILS'){el.open=true;}}
  openHash(); window.addEventListener('hashchange',openHash);
  var lb=document.getElementById('lb'), lbi=lb.querySelector('img');
  function closeLb(){lb.classList.remove('on'); lbi.src='';}
  document.querySelectorAll('a.zoom').forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault(); e.stopPropagation(); var tw=a.getBoundingClientRect().width||56; lbi.style.width=Math.min(window.innerWidth*0.92, Math.max(tw*8,448))+'px'; lbi.src=a.getAttribute('href'); lb.classList.add('on');});
  });
  lb.addEventListener('click',closeLb);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeLb();});
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


<details class="how">
<summary>How this page is put together, and where it looks</summary>
<div class="body">
<p><b>Every morning around six Central</b> an automated sweep reads the Cessna 180 and 185 pages of the main aircraft sales sites: Trade-A-Plane, Controller, Barnstormers, Hangar67, AircraftForSale, GlobalAir, GlobalPlaneSearch, FindAircraft and Kijiji, plus the dealer sites for Canadian Aircraft Sales and aircraftdealer.com. Those sites are national or worldwide, so one read covers everything they carry.</p>
<p><b>Facebook Marketplace works differently.</b> Facebook only shows ads within roughly forty miles of a chosen city, whatever radius you ask it for. So the sweep stands in fourteen cities in turn — Anchorage, Seattle, Portland, Boise, Spokane, Denver, San Francisco, Los Angeles, Minneapolis, Chicago, Dallas, Boston, Bangor and Miami — and searches each one for “cessna 180”, “cessna 185” and “cessna a185f”. An ad posted far from all fourteen, in Montana or the Dakotas say, will not be seen here unless it is also on another site.</p>
<p><b>Craigslist is searched from twenty-one points</b> across the lower 48 and Alaska, each reaching 500 miles, which covers the whole country with overlap. Same search words.</p>
<p><b>What is kept:</b> whole aircraft offered for sale, including projects, non-flying airframes and partial shares, which are marked as such in orange on the row. <b>What is left out:</b> parts ads (floats, props, engines, seats, wings on their own), ads the sweep cannot open, and anything a dealer’s own site marks sold. An ad that can no longer be found drops off the page the next morning.</p>
<p><b>Each aircraft is then matched to its serial number</b> from the ad or the registry, and that serial is checked against the NTSB, the Transportation Safety Board of Canada, FAA Service Difficulty Reports and the FAA Accident/Incident Data System. Where the ad gives no tail or serial, the row says “not screened”. Where more than one aircraft has worn the same registration over the years, it also says so rather than guess.</p>
<p><b>The record sources, for anyone who has not met them.</b> Each name links to that database’s own public search page, so you can look up any tail or serial yourself. <b><a href="https://data.ntsb.gov/carol-main-public/basic-search" target="_blank" rel="noopener">NTSB</a></b> is the US National Transportation Safety Board — it investigates accidents and records whether the damage was minor, substantial or destroyed, and the probable cause. <b><a href="https://www.tsb.gc.ca/eng/rapports-reports/aviation/index.html" target="_blank" rel="noopener">TSB</a></b> is the Transportation Safety Board of Canada, the same job north of the border. <b><a href="https://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-screaq/q.aspx?lang=eng" target="_blank" rel="noopener">CADORS</a></b> is Transport Canada’s daily log of occurrences, including minor ones the TSB never investigates — it is not part of the daily check here yet. Its search takes a Canadian registration, make and model, not a serial number, so a Canadian aircraft that has changed registration must be searched under each mark it has worn. <b><a href="https://sdrs.faa.gov/Query.aspx" target="_blank" rel="noopener">SDR</a></b> means Service Difficulty Report — a mechanic’s report to the FAA of a defect found during maintenance, which is how cracked spars and corroded bulkheads get on the record without an accident. <b><a href="https://www.asias.faa.gov/apex/f?p=100:12" target="_blank" rel="noopener">AIDS</a></b> is the FAA’s Accident/Incident Data System — the FAA’s own log, which catches incidents (a ground loop, a gear collapse) that never reached the NTSB. <b>The registry line</b> comes from the <a href="https://registry.faa.gov/aircraftinquiry/" target="_blank" rel="noopener">FAA register</a> or the <a href="https://wwwapps.tc.gc.ca/saf-sec-sur/2/ccarcs-riacc/RchSimp.aspx" target="_blank" rel="noopener">Transport Canada register</a>: who holds the registration and in what state, and whether the airworthiness certificate is Standard or something narrower like Restricted, which limits what the aircraft may legally be used for. <b><a href="https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/copies_aircraft_records" target="_blank" rel="noopener">Form 337s</a></b> are the FAA’s major repair and alteration records; they are not on any public database — you order the aircraft’s file from the FAA — which is why the box at the top says the logbooks are still mandatory.</p>
<p><b>Honest limits.</b> Figures are copied from the ads and are not verified. When two sites print different numbers for the same aircraft, both are shown. Some listing sites repeat airplanes that have already sold, so nothing is counted from them unless another site confirms it. The Sources section at the bottom says which sites answered today and which did not.</p>
</div>
</details>

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
<button data-key="price" data-dir="1" aria-pressed="true">lowest price</button>
<button data-key="price" data-dir="-1">highest price</button>
<button data-key="hrs" data-dir="1">lowest airframe hours</button>
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
<div id="lb" role="dialog" aria-modal="true" aria-label="Photo"><button class="x" aria-label="Close">×</button><img alt=""></div>
<script>{JS}</script>
</body>
</html>'''
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page)
dst=os.path.join(OUT,'data', f'{RUN}.json')
if os.path.abspath(LIST)!=os.path.abspath(dst): shutil.copy(LIST, dst)
print('wrote', os.path.join(OUT,'index.html'), len(page)//1024, 'KB;', len(L), 'rows;', len(recs), 'records;', sum(1 for l in L if l.get('photo')), 'photos')