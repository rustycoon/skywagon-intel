#!/usr/bin/env python3
"""Render check for index.html, run before every push.
Usage: python3 tools/check_page.py <index.html> <listings.json>
At 390 px and 1100 px: row count = listing count; zero broken images (the lightbox <img> has
no src and is excluded); body text colour not pure black (measured); every sort button
reorders; unpriced rows sit at the bottom on every sort; every row's count of listed facts
equals the count in its ad_facts (from/read excluded); no horizontal scroll at 390 px with
every row open; console clean except the Google Fonts stylesheet, which the container's
egress proxy blocks (filtered by the failed request's URL, not the console message).
Exit code 1 and a FAIL line for every defect found.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

INDEX, LIST = sys.argv[1:3]
data = json.load(open(LIST))
L = data["listings"]
expect_facts = {}
for l in L:
    af = l.get("ad_facts") or {}
    expect_facts[l["key"]] = sum(len(v) for k, v in af.items() if k not in ("from", "read") and isinstance(v, list))
url = "file://" + os.path.abspath(INDEX)
fails = []

def check(width):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": 900})
        console, failed = [], []
        pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(600)
        # force lazy images to load, then wait for them
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        pg.wait_for_function("[...document.querySelectorAll('img')].every(i => !i.getAttribute('src') || i.complete)", timeout=60000)
        tag = f"[{width}px]"
        n = pg.locator("details.row").count()
        if n != len(L): fails.append(f"{tag} row count {n} != {len(L)}")
        broken = pg.evaluate("""() => [...document.querySelectorAll('img')]
            .filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'))""")
        if broken: fails.append(f"{tag} broken images: {broken[:5]}")
        color = pg.evaluate("getComputedStyle(document.body).color")
        if color.replace(" ", "") in ("rgb(0,0,0)", "rgba(0,0,0,1)"): fails.append(f"{tag} body colour is pure black ({color})")
        # facts per row
        counts = pg.evaluate("""() => Object.fromEntries([...document.querySelectorAll('details.row')]
            .map(d => [d.id.replace(/^r-/, ''), d.querySelectorAll('ul.adl li').length]))""")
        for k, e in expect_facts.items():
            if k not in counts: fails.append(f"{tag} row #r-{k} missing")
            elif counts[k] != e: fails.append(f"{tag} facts on page {counts[k]} != ad_facts {e} for {k}")
        # sorts
        def order():
            return pg.evaluate("""() => [...document.querySelectorAll('details.row')].map(d => [d.id, d.dataset.price, d.dataset.hrs, d.dataset.year])""")
        base = [r[0] for r in order()]
        btns = pg.locator("button[data-key]")
        for i in range(btns.count()):
            bt = btns.nth(i); label = bt.inner_text()
            if bt.get_attribute("aria-pressed") == "true": continue
            bt.click(); pg.wait_for_timeout(200)
            o = order()
            if [r[0] for r in o] == base: fails.append(f"{tag} sort '{label}' did not reorder")
            priced = [r[1] not in (None, "", "null") for r in o]
            if "price" in (bt.get_attribute("data-key") or "") and any(priced[i] and not priced[i-1] for i in range(1, len(priced)) if not priced[i-1]):
                fails.append(f"{tag} unpriced row above a priced row on sort '{label}'")
            tail_unpriced = priced[::-1]
            k = 0
            while k < len(tail_unpriced) and not tail_unpriced[k]: k += 1
            if any(not x for x in tail_unpriced[k:]): fails.append(f"{tag} unpriced rows not all at the bottom on sort '{label}'")
        if width <= 420:
            pg.evaluate("document.querySelectorAll('details.row').forEach(d => d.open = true)")
            pg.wait_for_timeout(300)
            sw, cw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            if sw > cw: fails.append(f"{tag} horizontal scroll with every row open: {sw} > {cw}")
        bad_failed = [u for u in failed if "fonts.googleapis.com" not in u and "fonts.gstatic.com" not in u]
        if bad_failed: fails.append(f"{tag} failed requests: {bad_failed[:5]}")
        # a 'Failed to load resource' console line whose only failed request is the blocked fonts stylesheet is the proxy, not the page
        real_console = [c for c in console if not ("Failed to load resource" in c and not bad_failed)]
        if real_console: fails.append(f"{tag} console errors: {real_console[:5]}")
        b.close()

for w in (390, 1100):
    check(w)
if fails:
    for f in fails: print("FAIL", f)
    sys.exit(1)
print(f"PASS {len(L)} rows, both widths")
