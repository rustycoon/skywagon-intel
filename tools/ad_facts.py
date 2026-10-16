"""Skywagon Intel: turn an ad's text into lists of facts (engine, prop, avionics, equipment,
airframe, interior, exterior, inspection, history). Used by the daily run when it reads an ad.

  from ad_facts import classify, split_free, add, clean, CATS
  F = {}
  for line in split_free(text, aggressive=True): add(F, classify(clean(line), hint), line)

hint is the ad's own section ('avionics', 'engine', 'prop', 'interior', 'exterior') or None.
Automatic splitting is good for structured ads (Trade-A-Plane sections, Hangar67 tables).
Short run-on ads (Barnstormers, Facebook, Craigslist) are read by hand: write the lists directly.
"""
import re
CATS = ('engine','prop','avionics','equipment','airframe','interior','exterior','inspection','history')
AV = re.compile(r"(garmin|bendix|\bking\b|\bk[xtmnryia] ?-?\d|\bkma|\bkap|gtx|gtn|gns|gnc|gni|gma|gmx|gfc|gi[ -]?275|gi-?106|\bg5s?\b|g3x|g500|g1000|gdl|gtr|gdu|gps|nav/?com|\bcom ?\d|\bnav ?\d|comm\b|transponder|xpdr|xponder|ads-?b|audio panel|intercom|autopilot|auto pilot|s-?tec|\bstec|century [i1]|aspen|dynon|avidyne|uavionix|skybeacon|tail ?beacon|ps engineering|pma ?\d|pm-?\d{3,4}|narco|icom|\bifr\b|\bvor\b|\bloc\b|localizer|glide ?slope|\bhsi\b|\badi\b|efis|\bmfd\b|\bpfd\b|\belt\b|artex|kannad|jpi|edm-?\d|engine (monitor|analy[sz]er|indication)|ei mvp|mvp-?50|cgr-?30|\begt\b|\bcht\b|fuel ?flow|fuel (scan|totalizer|computer)|stratus|flightstream|flight stream|ipad|stormscope|\btraffic|ahrs|attitude|altimeter|encoder|\bvsi\b|turn coordinator|annunciator|push.to.talk|\bptt\b|headset|bose|lynx|aera|avmap|apollo|mid.?continent|lightspeed|smartglide|\bwaas|\blpv|digital tach|\bclock|chronometer|radio|avionics|\badf\b|\bdme\b|trig\b|sl ?[34]0|gpss|usb|glass panel|instrument panel|panel[- ]mounted)", re.I)
ENG = re.compile(r"\b(io-?\d{3}|o-?\d{3}|xp-?\d{3}|continental|lycoming|\btcm\b|smoh|stoh|snew|tsn|tsmoh|sfrm|sfoh|since (major |factory )?overhaul|since new|top overhaul|reman|engine|cylinders?|crankshaft|magneto|mags?\b|fuel injectors|gami|muffler|exhaust|oil cooler|oil filter|pre-?heat|preheat|tanis|reiff|starter|alternator|carb)\b", re.I)
PROP = re.compile(r"\b(prop|propeller|mccauley|hartzell|voyager|spoh|tspoh|black mac|bear paw|mt prop|\bmt\b composite|3[- ]blade|2[- ]blade|three[- ]blade)", re.I)
INT = re.compile(r"\b(interior|upholster|headliner|carpet|leather|seats?|seat belts?|harness|side ?panels?|selkirk int)", re.I)
EXT = re.compile(r"\b(paint|painted|exterior|windshield|windows?)\b", re.I)
INSP = re.compile(r"\b(annual|inspection|ifr cert|pitot|static check|ad'?s (complied|up to date|current)|all ad|sb'?s|100 ?hr)\b", re.I)
HIST = re.compile(r"(damage|\blogs?\b|logbook|history|accident|owner|hangar|corrosion|ground ?loop|records|commercial|part 135|hail|no salt|salt water|restor)", re.I)
AIRF = re.compile(r"(total time|ttaf|\btt\b|ttsn|airframe|useful load|empty weight|gross weight|\blbs?\b|max takeoff|seats:)", re.I)
JUNK = re.compile(r"(financ|insurance|subject to (prior sale|verification|change)|call (today|now|or text)|contact (us|the seller|this seller|me)|aircraftcash|lending|terms of use|see more from|view (all|more|larger)|offered subject|specifications are subject|serious (buyers|inquir)|price|make (an )?offer|located (in|at)|location|available for (viewing|inspection)|https?://|www\.|e-?mail|phone|\btext\b|call for|for sale|listed (a |\d)|send seller|^send$|^save$|^share$|^details$|^condition$|used - |location is approximate|see less|days active|offered by|registration:|s/n:|price:|^\$|\(click\)|whatsapp|messenger|our loss|your gain|don.t miss|won.t last|dream|opportunity|beautiful|gorgeous|stunning|turn-?key|ready to (go|fly)|fly (it )?home|pre-?buy welcome|trade|delivery|deliver|ferry|checkout|spared|feel free|any questions|excellent history|snag free|good overall|well maintained|^\s*\$?[\d,.]+\s*(usd|cad|eur|gbp)?\s*$|^engine( & propeller)?$|^propeller$|^prop$|^airframe$|^avionics$|^additional equipment$|^standard equipment$|^remarks$|^new$|^interior$|^exterior$|^equipment$|^seller|^posted|^updated|disclaimer|every effort|errors and omissions|representations or warranties|rely on your own|introductory information|brings to market|^inc$|call \w+ \w+ at|@|per month|hard pressed|what a bird|re-imagined|formidable|no broker|deal direct|bragging|have fun|like brand new|not another one|perfect airframe|extremely low time|amazing condition!?$|incredible|^features$|^extras$|^performance$|^inspection status$|^additional items$|^airframe options$|^details$|good fall/winter project|sound working|^at lake hood$|^n\d{1,5}[a-z]{0,2}$|^serial(#| number)?:? ?\d|^sn: ?\d)", re.I)
def clean(s):
    s = s.replace('͏','').replace('​','').replace(' ',' ')
    s = re.sub(r'^[\s\-•*·▪►✓✔–—]+\s*', '', s)
    s = re.sub(r'^(details|remarks|additional details)\s*:\s*', '', s, flags=re.I)
    s = re.sub(r'\$\s?[\d,.]+\s*(usd|cad|us)?\b', '', s, flags=re.I)
    s = re.sub(r'\b(estimate|asking)\s+to fix it', 'estimated to fix', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(' ,;.')
    return s
def classify(s, hint=None):
    if re.search(r'damage|accident|incident|ground ?loop|overturn', s, re.I) and not re.search(r'no (known )?damage', s, re.I) and hint != 'avionics': return 'history'
    if re.search(r'no (known |recorded )?damage|no accident', s, re.I): return 'history'
    if hint in ('engine','prop') and not (ENG.search(s) or PROP.search(s) or re.search(r'\d.*(hrs?|hours|smoh|tbo|snew|since)|serial|s/n|tbo|blade|overhaul|reman|installed|time', s, re.I)):
        hint = None
    if hint in ('avionics',) : return 'avionics'
    if hint in ('interior','exterior'):
        if re.fullmatch(r'(rated:?\s*)?[\d.+]+\s*(/\s*10|out of 10)|rated\s*[“"]?[\d.]+[”"]?', s.strip(), re.I): return hint
        if re.search(r'paint|exterior|white|red|blue|grey|gray|black|green|yellow|stripe|scheme|color', s, re.I) and not INT.search(s): return 'exterior'
        if re.search(r'interior|upholster|headliner|carpet|leather|vinyl|fabric|side ?panels?|seat (covers|belts)|rated|/10|out of 10|\d\.?\d? ?/ ?10', s, re.I): return 'interior' if not re.search(r'paint|exterior', s, re.I) else 'exterior'
        hint = None
    if hint == 'engine':
        return 'prop' if PROP.search(s) and not re.search(r'\b(io-?\d{3}|o-?\d{3}|engine)\b', s, re.I) else 'engine'
    if hint == 'prop': return 'prop'
    # free classification
    if re.match(r'^(prop(eller)?\b|mccauley|hartzell|mt[- ]?prop|mtv|sensenich|black mac|3[- ]blade|2[- ]blade|three[- ]blade)', s, re.I): return 'prop'
    if PROP.search(s) and not re.search(r'\b(io-?\d{3}|o-?\d{3}|engine|smoh)\b', s, re.I) and len(s) < 120: return 'prop'
    if re.search(r'\b(io-?\d{3}|o-?\d{3}|xp-?\d{3})\b|smoh|stoh|snew|since (major |factory )?overhaul|top overhaul|reman', s, re.I): return 'engine'
    if INSP.search(s) and len(s) < 140: return 'inspection'
    if re.search(r'damage|accident|ground ?loop|\blogs?\b|logbook|corrosion|hail|hangar(ed)?\b|hangar kept|owners? since|same owner|one owner', s, re.I): return 'history'
    if AV.search(s) and not re.search(r'stol|float|wheel|tire|gear|tank|fuel cap|bubble', s, re.I): return 'avionics'
    if AIRF.search(s) and re.search(r'\d', s): return 'airframe'
    if hint == 'history' and HIST.search(s): return 'history'
    if INT.search(s) and not re.search(r'jump seat|seat rail|stop|harness', s, re.I) and re.search(r'interior|leather|carpet|upholster|headliner|rated|/10', s, re.I): return 'interior'
    if EXT.search(s) and re.search(r'paint|exterior', s, re.I): return 'exterior'
    if ENG.search(s) and not re.search(r'stol|vortex|float|wheel', s, re.I): return 'engine'
    if HIST.search(s) and len(s) > 25: return 'history'
    return 'equipment'
def split_free(text, aggressive=False):
    """split a free-text ad into short fact items"""
    t = text.replace('͏','')
    parts = []
    for line in re.split(r'\n+', t):
        line = line.strip()
        if not line: continue
        # long comma/period run-on lines -> split
        if len(line) > (55 if aggressive else 110):
            pat = r'(?<=[A-Za-z0-9\)"”])\.\s+|\s*,\s*|;\s+|\s+•\s+|\s+-\s+' if aggressive else r'(?<=[a-z0-9\)])\.\s+(?=[A-Z0-9])|,\s+(?=[A-Z0-9\(])|;\s+|\s+•\s+'
            for p in re.split(pat, line):
                parts.append(p)
        else:
            parts.append(line)
    return parts
PROSE = re.compile(r"\b(is|are|was|were|has been|have been|comes|sits|sitting|shows|currently|offers|we |you |your |our |i |i'm|i've)\b", re.I)
def keep(s):
    if not s or len(s) < 3: return False
    if s.endswith(':'): return False
    if len(s.split()) > 22: return False
    if len(s) > 95 and PROSE.search(s): return False
    if len(s) > 170: return False
    if JUNK.search(s): return False
    if re.fullmatch(r'[\d\s,.$:/-]+', s): return False
    return True
def norm_key(s): return re.sub(r'[^a-z0-9]', '', s.lower())
def add(facts, cat, s, force=False):
    s = clean(s) if not force else re.sub(r'\s+', ' ', s).strip()
    if not force and not keep(s): return
    lst = facts.setdefault(cat, [])
    k = norm_key(s)
    if not k: return
    for i, x in enumerate(lst):
        kx = norm_key(x)
        if k == kx or k in kx: return
        if kx in k and len(kx) > 5: lst[i] = s; return
    lst.append(s)
