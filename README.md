# skywagon-intel

A facts-only daily record of every Cessna 180 and 185 advertised for sale. Published at https://skywagon-intel.pages.dev — Cloudflare Pages redeploys on every push to `main`.

- `index.html` — the page for the latest run
- `data/<date>.json` — the listings record for each run (machine record; the next run diffs against it)
- `photos/` — one thumbnail per listing where the ad had a photo
- `tools/build_intel.py` — renders `index.html` from a listings JSON, the photo folder and the serial-spine CSVs
- `tools/listings_<date>.py` — how the first run's dataset was assembled

Nothing here is an opinion about any aircraft or seller. A clean record is not proof; Form 337s and logbooks are mandatory before any purchase.
