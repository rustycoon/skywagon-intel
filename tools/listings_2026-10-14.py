# Skywagon Intel — listings for the 2026-10-14 run.
# Hand-assembled from the frozen board (Version 44) and the 10/14 daily sweep doc.
# Only listings with a live advertisement on 10/14 are included.
import json

TAP = "https://www.trade-a-plane.com/search?s-type=aircraft&category_level1=Single%20Engine%20Piston&make=CESSNA&model_group=CESSNA+185+SERIES&s-page_size=96"
def tap(i): return f"https://www.trade-a-plane.com/search?s-type=aircraft&listing_id={i}"
CTRL = "https://www.controller.com/listings/for-sale/cessna/185/piston-single-aircraft"
BARN = "https://www.barnstormers.com/category-17400-Cessna--C-185.html"
BARN1 = "https://www.barnstormers.com/category-17401-Cessna--C-185.html"
BARNF = "https://www.barnstormers.com/category-16268-Cessna--Amphibian.html"
H67 = "https://www.hangar67.com/aircraft-for-sale"
GPS = "https://www.globalplanesearch.com/"
AFS = "https://www.aircraftforsale.com/aircraft/single-engine-piston/cessna/185"
GA = "https://www.globalair.com/aircraft-for-sale/single-engine-piston/cessna-185"
FA = "https://www.findaircraft.com/"
CSP = "https://www.csplane.com/"
KIJ = "https://www.kijiji.ca/b-canada/cessna-185/k0l0"
CLA = "https://anchorage.craigslist.org/search/sss?query=cessna%20185"
ADC = "https://www.aircraftdealer.com/"
def fb(i): return f"https://www.facebook.com/marketplace/item/{i}/"

L = []
def add(**k): L.append(k)

# ---------- United States ----------
add(key="N115AW", price=220000, year=1976, model="A185F", tail="N115AW", serial="18502941", tt="3,940",
    engine="Continental IO-520-D · 950 since overhaul · top overhaul 50 hrs ago", prop="McCauley C58 three-blade · 250 since overhaul",
    gear="Wheels · factory float kit installed", fuel="84 gallons long range", mods="Factory extended baggage, Atlee Dodge middle seats, P-Ponk gear legs, bubble windows, 6-bolt wheels and brakes",
    panel="KX-175B, KX-170B, Apollo GX55, KT76 transponder", annual="Due September 2027",
    registry="Standard airworthiness · registered owner in Anchorage, AK", history="Private, non-commercial Alaska history, as advertised",
    location="Placerville, CA", country="US", seller="Skywagons LLC · Mark Pilkington", phone=["530-642-2806"], photo="N115AW", first_seen="2026-09-09",
    sources=[("Barnstormers","https://www.barnstormers.com/classified-2072084-1976-Cessna-A185F.html?catid=17400"),("Trade-A-Plane",tap(2460353)),("Controller",CTRL),("Hangar67",H67),("GlobalPlaneSearch",GPS),("FindAircraft",FA)])
add(key="N8536T", price=250000, year=1970, model="A185E", tail="N8536T", serial="18501784", tt="6,009",
    engine="Continental IO-550-D factory reman · 170 since overhaul", gear="Wheels", fuel="Tip tanks, as advertised",
    history="Hail damage disclosed in the ad", useful_load="1,550 lb, as advertised",
    location="Minden, NV (dealer in Tulsa, OK)", country="US", seller="Dan Howard Aircraft Sales", phone=["918-498-7073"], photo="N8536T",
    price_note="Barnstormers, GlobalPlaneSearch and aircraftdealer.com still print $265,000",
    sources=[("Trade-A-Plane",tap(2448106)),("Controller",CTRL),("Barnstormers",BARN1),("GlobalPlaneSearch",GPS),("aircraftdealer.com",ADC)])
add(key="N91PH", price=265000, year=1973, model="A185F", tail="N91PH", serial="18502325", tt="3,550",
    engine="1,020 since overhaul", gear="Wipline 3730 amphibious floats", panel="GNS 430",
    location="Pampa, TX", country="US", seller="Hudson Flight Ltd · Ron Fernuik", phone=["806-662-5823"], photo="N91PH",
    sources=[("Trade-A-Plane",tap(2459651)),("GlobalPlaneSearch",GPS),("FindAircraft",FA),("aircraftdealer.com",ADC)])
add(key="N6307B", price=285000, year=1979, model="A185F", tail="N6307B", serial="18503742", tt="7,145",
    engine="Continental IO-520-D · 1,110 since overhaul · 340 since top", gear="EDO 3430 floats", mods="Wing-X STOL",
    location="Palmer, AK", country="US", seller="Private seller, Wasilla AK", photo="N6307B", tail_note="Tail read from the ad photo",
    sources=[("Facebook Marketplace",fb(809408015382816))])
add(key="N93033", price=295000, year=1976, model="A185F", tail="N93033", serial="18503166", tt="1,623",
    engine="1,180 since overhaul", gear="Amphibious floats", annual="Fresh annual March 2026",
    location="Plymouth, MA", country="US", seller="Yankee Aviation Services", phone=["508-565-8208"], photo="N93033",
    sources=[("Trade-A-Plane",tap(2454518))])
add(key="N5830J", price=299000, year=1970, model="A185E", tail="N5830J", serial="18501799", tt="3,470",
    engine="Continental IO-550-D · 780 since overhaul", gear="Amphibious floats", fuel="Long range fuel", panel="WAAS IFR",
    location="Fort Myers, FL", country="US", seller="Southwind Aviation", phone=["239-278-3113"], photo="N5830J",
    sources=[("Trade-A-Plane",tap(2459533)),("Trade-A-Plane (second ad)",tap(2459529)),("Barnstormers",BARN1),("Barnstormers amphibian",BARNF)])
add(key="mesa", price=85000, year=1964, model="185C", tail=None, serial=None, tt="2,100",
    engine="1,100 since overhaul", history="Prop strike, wing and vertical fin damage disclosed in the ad; seller estimates $65,000 to repair",
    location="Mesa, AZ", country="US", seller="Contact through the ad", sources=[("Barnstormers",BARN)])
add(key="N1795R", price=190000, price_was=180000, year=1974, model="A185F", tail="N1795R", serial="18502511", tt="5,313",
    engine="Continental IO-520-D · 1,231 since new · 75 since top", gear="Aerocet 3500L floats",
    location="Anchorage, AK", country="US", seller="Black Dog Holding · Steven Styles",
    price_note="aerogurus still prints $180,000; the Facebook tile shows a placeholder figure",
    sources=[("Trade-A-Plane",tap(2460907)),("Barnstormers",BARN),("Barnstormers",BARN1),("Hangar67",H67)])
add(key="N70713", price=190000, year=1971, model="A185E", tail="N70713", serial="18501878", tt="7,963",
    engine="Continental IO-520-D factory rebuilt · 351 since overhaul", gear="Wheels · ski fittings",
    location="Anchorage, AK", country="US", seller="Contact through the ad", photo="N70713", sources=[("Trade-A-Plane",TAP),("Controller",CTRL)])
add(key="N111EY", price=195000, year=1974, model="185E", tail="N111EY", serial="18502407", tt="4,500 (the ad also prints 4,400)",
    engine="Continental IO-520 · 1,300 since overhaul · 200 since top", gear="Wheels",
    location="Viola, ID", country="US", seller="Private seller · Jared", phone=["208-301-0683"], photo="N111EY", sources=[("Trade-A-Plane",tap(2452517))])
add(key="N185EE", price=200000, year=1961, model="185", tail="N185EE", serial="1850105", tt="7,300",
    engine="430 since field overhaul", gear="Wheels / wheel-skis", history="Previously C-FNNQ and N4419C",
    location="Boulder, CO", country="US", seller="Contact through the ad", sources=[("Barnstormers",BARN)])
add(key="spokane", price=205000, year=1962, model="185A", tail=None, serial=None, tt=None,
    engine="Continental IO-470-F · times not in the ad", gear="Wheels",
    location="Spokane, WA", country="US", seller="Doug Colley (for the owner)", sources=[("Barnstormers",BARN),("Barnstormers",BARN1)])
add(key="N9998X", price=205000, year=1961, model="185", tail="N9998X", serial="1850198", tt="4,440",
    engine="Continental IO-470 · 110 since factory overhaul", gear="Wheels",
    location="Peachtree City, GA", country="US", seller="Private seller · James Sells", sources=[("Trade-A-Plane",tap(2456187))])
add(key="N4841C", price=219000, year=1975, model="A185F", tail="N4841C", serial="18502609", tt="5,530",
    engine="Continental IO-520", gear="Wheels · factory float kit, never on floats", fuel="80 gallons", mods="Robertson STOL",
    location="Mount Vernon, WA", country="US", seller="Seitz Aviation · Evan Seitz", phone=["425-478-7163"], photo="N4841C",
    sources=[("Trade-A-Plane",TAP),("AircraftForSale",AFS),("Facebook Marketplace","https://www.facebook.com/marketplace/seattle/search?query=cessna%20185")])
add(key="N9911X", price=219900, year=1961, model="185", tail="N9911X", serial="1850111", tt="4,500",
    gear="EDO 2960 floats", mods="Robertson STOL", registry="Standard airworthiness · registry lists an IO-470 engine",
    location="Bend, OR", country="US", seller="Contact through the ad", sources=[("Controller","https://www.controller.com/listing/for-sale/261154307/1961-cessna-185-piston-single-aircraft")])
add(key="N185DL", price=235000, year=1964, model="185C", tail="N185DL", serial="1850690", tt="5,463",
    engine="Continental IO-470 · 270 since factory reman", gear="Wheels / skis",
    location="Sheridan, MI", country="US", seller="Contact through the ad", photo="N185DL", tail_note="Tail read from the ad photo", sources=[("Facebook Marketplace",fb(2172659143355197))])
add(key="N103AM", price=249000, year=1975, model="A185F", tail="N103AM", serial="18502615", tt="7,653",
    engine="Continental IO-520-D · 431 since overhaul (October 2022)", gear="Wheels", history="Part 135 history, as advertised",
    location="La Grande, OR", country="US", seller="Contact through the ad", photo="N103AM",
    sources=[("Trade-A-Plane",tap(2457083)),("AircraftForSale",AFS)])
add(key="N4448R", price=250000, year=1976, model="185F", tail="N4448R", serial=None, tt="4,681.6",
    engine="Continental IO-520-F reman February 2009 · 222.7 since", gear="EDO 2960 floats", mods="Robertson STOL",
    location="Anchorage, AK", country="US", seller="Contact through the ad", sources=[("Facebook Marketplace",fb(1399740905369736))])
add(key="N969WM", price=250000, year=1962, model="185A", tail="N969WM", serial="1850506", tt="9,524",
    engine="Continental IO-470-F · 249 since overhaul", gear="Wheels · float kit", mods="Sportsman STOL, Bushwheels",
    empty_weight="1,868 lb, as advertised", useful_load="1,322 lb, as advertised",
    location="Little Rock, AR (registry)", country="US", seller="Contact through the ad", photo="N969WM", sources=[("Trade-A-Plane",tap(2453669))])
add(key="N18500", price=250000, price_was=255000, year=1977, model="A185F", tail="N18500", serial="18503305", tt="661.8, as advertised",
    engine="Continental IO-520-D · 661.8 since new · disassembled, sold as-is", gear="Wheels · factory float kit, never on floats", fuel="84 gallons in bladders", mods="Robertson STOL",
    location="Anchorage, AK", country="US", seller="Private seller · Dennis Thompson (Craigslist relay)", tail_note="Tail read from the panel photo", posted="Ad dated 2026-09-23",
    sources=[("Craigslist","https://www.craigslist.org/view/d/anchorage-1977-cessna-185-one-of-kind/tVHLWyNru81PSLjbqTzrtN")])
add(key="N4761Q", price=275000, year=1967, model="185E", tail="N4761Q", serial="1851226", tt="9,788",
    engine="Continental IO-520 · 297.2 since overhaul", gear="Wipline 3800 floats", mods="Sportsman STOL",
    location="Anchorage, AK", country="US", seller="Seaplanes North", sources=[("Craigslist","https://www.craigslist.org/view/d/anchorage-1967-cessna-185e/pYXqN7oXFPykVwcmi1oN9B"),("Hangar67",H67)])
add(key="N666SB", price=285000, year=1980, model="A185F", tail="N666SB", serial=None, tt="2,620",
    engine="Continental IO-520-D · 1,392 since overhaul", gear="Wheels · factory float kit",
    location="Santa Paula, CA", country="US", seller="Contact through the ad", photo="N666SB", sources=[("Trade-A-Plane",tap(2458523)),("Barnstormers",BARN)])
add(key="N4757Q", price=288000, year=1967, model="185E", tail="N4757Q", serial="1851216", tt="about 3,850 (the Trade-A-Plane header prints 850)",
    engine="Continental IO-520-D · about 410 since overhaul", gear="Wheels", mods="P-Ponk gear",
    location="Willow / Wasilla, AK", country="US", seller="Backcountry Aircraft Group (broker, $288,000) · owner John Bradley ($285,000)", phone=["682-407-7957"], photo="N4757Q",
    sources=[("Trade-A-Plane",TAP),("Barnstormers",BARN),("Facebook Marketplace","https://www.facebook.com/marketplace/anchorage/search?query=cessna%20185")])
add(key="N5227R", price=295000, year=1976, model="A185F", tail="N5227R", serial="18503023", tt="3,070 (prop total time as printed)",
    engine="Continental IO-550-D · Western Skyways reman April 2022 · 325 since", gear="CAP 3000 floats",
    registry="Restricted category · Other, Aerial Advertising, Agriculture and Pest Control",
    location="Fairbanks, AK", country="US", seller="Contact through the ad", sources=[("Barnstormers",BARN1)])
add(key="anch80", price=300000, year=1980, model="A185F", tail=None, serial=None, tt="2,200",
    engine="500 since overhaul (the ad does not say when)", gear="Wheels and EDO 2960 floats", mods="Robertson STOL",
    location="Wasilla, AK", country="US", seller="Private seller · Gar Jordan", posted="Ad dated 2026-09-12",
    sources=[("Craigslist",CLA),("Facebook Marketplace","https://www.facebook.com/marketplace/anchorage/search?query=cessna%20a185f")])
add(key="N93183", price=315000, year=1976, model="A185F", tail="N93183", serial="18503190", tt="2,194",
    engine="550 engine and prop upgrade, as advertised", gear="Aerocet floats · hydraulic wheel skis", mods="Sportsman leading edge, VGs, HID lights",
    history="Privately owned 44 years; the ad discloses minor wingtip damage in 1978; complete logs, as advertised",
    registry="Restricted category · Other", location="Anchorage, AK", country="US", seller="Alaska Aircraft Sales", phone=["907-243-1966"],
    sources=[("Trade-A-Plane",tap(2458037)),("Hangar67",H67)])
add(key="N1089F", price=325000, year=None, model="A185F", tail="N1089F", serial=None, tt="2,776",
    location="Alaska", country="US", seller="Seaplanes North", sources=[("Hangar67",H67)])
add(key="N866PH", price=357500, year=1976, model="A185F", tail="N866PH", serial="18503167", tt=None,
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL),("Trade-A-Plane",tap(2457588))])
add(key="alpena", price=359000, price_note="Make offer", year=1975, model="A185F", tail=None, serial=None, tt="3,000",
    engine="1,060 since factory new", prop="McCauley on the P-Ponk STC · 144 since", gear="Wipline 3000A amphibious floats · land gear included", mods="Wing-X, VGs", panel="S-Tec 30 autopilot",
    location="Alpena, MI", country="US", seller="Air Devices · Randy Patterson", sources=[("Barnstormers amphibian",BARNF),("Barnstormers",BARN)])
add(key="N78BL", price=369900, year=1977, model="A185F", tail="N78BL", serial="18503324", tt=None,
    location="Hampstead, NH", country="US", seller="Contact through the ad", sources=[("Facebook Marketplace","https://www.facebook.com/marketplace/boston/search?query=cessna%20185")])
add(key="N4711E", price=379000, year=None, model="A185F", tail="N4711E", serial="18503845", tt=None, mods="Robertson STOL",
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N7802F", price=389000, year=None, model="A185F", tail="N7802F", serial=None, tt=None, mods="Robertson STOL",
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N1790R", price=395000, year=None, model="A185F", tail="N1790R", serial=None, tt="2,400 on Trade-A-Plane; 2,200 on Barnstormers",
    engine="550 since new on Trade-A-Plane; 590 on Barnstormers", prop="25 since new on Trade-A-Plane; 20 on Barnstormers",
    price_note="The Barnstormers ad says NEW PRICE and prints no figure",
    location="United States", country="US", seller="Contact through the ad", sources=[("Trade-A-Plane",tap(2460909)),("Barnstormers",BARN)])
add(key="N185KS", price=399000, year=None, model="A185F", tail="N185KS", serial=None, tt=None,
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N87TM", price=399900, year=None, model="A185E", tail="N87TM", serial="18501786", tt=None,
    location="United States", country="US", seller="Contact through the ad", sources=[("Trade-A-Plane",TAP)])
add(key="N86SS", price=349900, year=None, model="A185F", tail="N86SS", serial=None, tt=None,
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N185HR", price=540000, year=1975, model="A185F", tail="N185HR", serial="18502815", tt="459",
    location="Liberal, KS", country="US", seller="Ron Drosselmeyer, Aurora CO (buyers referred to Lyddon Aero Center)", phone=["719-602-3578"],
    sources=[("Controller","https://www.controller.com/listing/for-sale/257412531/1975-cessna-a185f-piston-single-aircraft")])
add(key="N185GG", price=650000, year=None, model="A185F", tail="N185GG", serial="18502787", tt=None,
    location="Loveland, CO", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N4800Q", price=899500, year=None, model="A185F", tail="N4800Q", serial="18503562", tt=None,
    location="United States", country="US", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N53044", price=None, price_note="Call for price (a $520,000 figure was published earlier)", year=None, model="A185F", tail="N53044", serial="18502334", tt="650",
    location="Punta Gorda, FL (GlobalAir prints Minnesota)", country="US", seller="Contact through the ad", sources=[("Controller",CTRL),("GlobalAir",GA)])
add(key="fla82", price=None, price_note="Call for price", year=1982, model="A185F", tail=None, serial=None, tt="5,620", gear="Amphibious floats",
    location="Florida", country="US", seller="Contact through the ad", sources=[("FindAircraft",FA)])
# the one 180 sighted this run
add(key="chatham180", make="Cessna", price=185000, year=1965, model="180H", tail=None, serial=None, tt=None, gear="Amphibious floats",
    location="Chatham, NY", country="US", seller="Jim McMahon", sources=[("Barnstormers amphibian",BARNF)])

# ---------- Canada ----------
add(key="siouxlookout", price=135000, year=1976, model="A185F", tail=None, serial=None, tt="8,807 (on wheels)",
    engine="667 since overhaul", prop="168 since overhaul", gear="Wheels · float kit · ski plumbing", mods="Bubble windows",
    location="Sioux Lookout, ON", country="CA", seller="Allen Airways · David Allen", sources=[("Barnstormers",BARN),("Barnstormers",BARN1)])
add(key="CGIAL", price=209000, price_note="Accepting offers", year=1980, model="A185F", tail="C-GIAL", serial="18504138", tt="10,427 (Barnstormers prints 10,407.2)",
    engine="Continental IO-520-D · 1,429.7 since overhaul", gear="Float and ski fittings",
    location="Port Elgin, ON", country="CA", seller="Contact through the ad", sources=[("Trade-A-Plane",tap(2460410)),("Barnstormers",BARN1)])
add(key="whiterock", price=211000, price_note="CAD 295,000 · seller says the price is firm", year=1973, model="A185F", tail=None, serial=None, tt="9,400",
    engine="Continental IO-520-D · 25 since overhaul · 7-stud case by Pro Aero", prop="McCauley 401 88-inch Bear Paw · 0 since overhaul", gear="Wheels · Seaplanes West float mount",
    location="White Rock, BC", country="CA", seller="Contact through the ad", sources=[("Barnstormers","https://www.barnstormers.com/classified-2073292-A185F-Fresh-Engine-and-Mac-401.html")])
add(key="CFNHM", price=230000, year=1961, model="185", tail="C-FNHM", serial="1850064", tt="3,155",
    engine="Continental IO-470-F · 15 since overhaul", gear="Aero Set 3500 floats",
    location="Nipawin, SK (Hangar67 prints Alberta)", country="CA", seller="Aircraft Canada", phone=["587-583-5013"], sources=[("Controller",CTRL),("Hangar67",H67)])
add(key="CGUIC", price=268000, price_note="GlobalAir prints $286,000; the dealer's own site prints CAD 369,000, reduced", year=1976, model="A185F", tail="C-GUIC", serial="18503009", tt="4,825",
    engine="Continental IO-550-D · 150 since overhaul (2018)", prop="Hartzell three-blade · overhauled 2025", gear="EDO 3430 floats",
    location="Hawkesbury, ON", country="CA", seller="Canadian Aircraft Sales · Pier Labelle", phone=["613-632-0123"], photo="CGUIC", tail_note="Tail read from the ad photo",
    sources=[("Trade-A-Plane",tap(2436256)),("GlobalAir",GA),("Canadian Aircraft Sales",CSP)])
add(key="TFORN", price=275000, year=1974, model="A185F", tail="TF-ORN", serial="18502355", tt="4,503.7",
    engine="Continental IO-520-D 300 hp", gear="Wheels", empty_weight="1,971 lb, as advertised",
    registry="Icelandic registration · previously N53068", location="Gimli, MB", country="CA", seller="Private seller · Sijo Zach", photo="TFORN",
    sources=[("Controller",CTRL),("AircraftForSale","https://www.aircraftforsale.com/listing/1974-cessna-a185f-skywagon-c7147970"),("Hangar67",H67),("Kijiji",KIJ)])
add(key="CGGKA", price=280000, year=1979, model="A185F", tail="C-GGKA", serial="18503844", tt="5,569",
    gear="Amphibious floats", history="Previously N185ME and N4695E",
    location="Mill Bay / Victoria, BC", country="CA", seller="Contact through the ad", sources=[("Barnstormers","https://www.barnstormers.com/classified-2057932-1979-Cessna-A185F-Amphibian.html")])
add(key="CGAIX", price=285000, year=1979, model="A185F", tail="C-GAIX", serial=None, tt="16,965",
    engine="Continental IO-520-F · 0 since overhaul", gear="Wipline 3730 amphibious floats", mods="Robertson STOL, Flint tips",
    location="Fort Smith, NT", country="CA", seller="Contact through the ad", photo="CGAIX", sources=[("Trade-A-Plane",tap(2440682)),("Controller",CTRL),("Hangar67",H67)])
add(key="CFSEC", price=299000, year=1973, model="185", tail="C-FSEC", serial="18502152", tt="6,883",
    engine="Continental IO-520 · 558 since overhaul", prop="0 since overhaul", gear="Wipline 3730 amphibious floats",
    location="Hawkesbury, ON", country="CA", seller="Canadian Aircraft Sales · Pier Labelle", phone=["613-632-0123"], photo="CFSEC", tail_note="Tail read from the ad photo",
    sources=[("Trade-A-Plane",tap(2452630)),("GlobalAir",GA),("Canadian Aircraft Sales",CSP)])
add(key="alberta78", price=310000, price_note="aircraftdealer.com labels it recently reduced; the figure has not changed in weeks", year=1978, model="A185F", tail=None, serial=None, tt=None,
    location="Alberta", country="CA", seller="Front Sight · Dennis", phone=["780-849-0583"], sources=[("GlobalPlaneSearch",GPS),("aircraftdealer.com",ADC)])
add(key="CFGCG", price=335000, year=None, model="A185F", tail="CF-GCG", serial=None, tt=None,
    location="Canada", country="CA", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="N1050F", price=340000, year=None, model="A185F", tail="N1050F", serial=None, tt=None,
    location="British Columbia", country="CA", seller="Contact through the ad", sources=[("Hangar67",H67),("GlobalPlaneSearch",GPS),("aircraftdealer.com",ADC)])
add(key="CGGKJ", price=379000, year=None, model="A185F", tail="C-GGKJ", serial=None, tt=None, history="Previously N78011",
    location="Canada", country="CA", seller="Contact through the ad", sources=[("Hangar67",H67),("GlobalPlaneSearch",GPS)])
add(key="CGGMP", price=429900, year=None, model="A185F", tail="C-GGMP", serial=None, tt=None,
    location="Canada", country="CA", seller="Contact through the ad", sources=[("Trade-A-Plane",tap(2457405))])
add(key="CFTLM", price=495000, year=None, model="A185F", tail="C-FTLM", serial="18502952", tt=None,
    location="Canada", country="CA", seller="Contact through the ad", sources=[("Controller",CTRL)])
add(key="CGYIS", price=None, price_note="Please call", year=None, model="A185F", tail="C-GYIS", serial=None, tt=None,
    location="Pinehouse, SK", country="CA", seller="Contact through the ad", sources=[("Controller",CTRL),("AircraftForSale",AFS),("Hangar67",H67)])
add(key="CFCUK", price=None, price_note="Call for price", year=None, model="A185F", tail="C-FCUK", serial="18502270", tt="6,927", history="Previously N477H",
    location="Delta, BC", country="CA", seller="Contact through the ad", sources=[("Trade-A-Plane",tap(2444847))])
add(key="fairley76", price=None, price_note="No price in the ad", year=1976, model="A185F", tail=None, serial=None, tt="7,270.1",
    engine="Continental IO-520 · 293.4 since overhaul", prop="C58 · 12.8 since overhaul", gear="3500L floats", mods="Sportsman STOL, VGs, Atlee Dodge rear seats",
    location="Vancouver, BC", country="CA", seller="Kevin Fairley", sources=[("Barnstormers",BARN),("Barnstormers",BARN1),("Barnstormers float plane","https://www.barnstormers.com/category-17450-Cessna--C-185.html")])

# ---------- Everywhere else ----------
add(key="YV1742", price=210000, year=1978, model="A185F", tail="YV-1742", serial="18503641", tt="7,430",
    engine="19.3 since overhaul", prop="20.8 since overhaul", history="Previously N3106Y",
    location="Venezuela (Trade-A-Plane prints Tampa, FL; aerogurus prints Charallave)", country="VE", seller="YVFLEET · Alejandro Bermúdez", phone=["941-288-0291"],
    sources=[("Trade-A-Plane",tap(2461340)),("Barnstormers",BARN),("Barnstormers",BARN1)])
add(key="N4095L", price=313809, price_was=312891, price_note="GlobalPlaneSearch prints $321,412", year=None, model="A185F", tail="N4095L", serial=None, tt="10,904.2 (GlobalPlaneSearch prints 10,889)",
    engine="Continental IO-520-D · 2,280 total · 179 since overhaul (2019)", prop="328.5 since overhaul",
    location="Locarno, Switzerland", country="CH", seller="Aeromeccanica SA", sources=[("Controller",CTRL),("GlobalPlaneSearch",GPS),("aircraftdealer.com",ADC)])
add(key="brasschaat", price=265000, year=1961, model="185", tail=None, serial=None, tt="about 6,031",
    engine="Continental IO-520 · 36 hours", gear="EDO floats",
    location="Brasschaat, Belgium", country="BE", seller="US1 Exports · Ricardo Birsa (broker address San Isidro, Argentina)", sources=[("Barnstormers",BARN1),("Barnstormers amphibian",BARNF),("Hangar67",H67)])
add(key="OODUK", price=None, price_note="Call for price", year=1961, model="185", tail="OO-DUK", serial=None, tt=None,
    location="Paris, France", country="FR", seller="Tregor Air Services", sources=[("GlobalPlaneSearch",GPS)])
add(key="GOMUD", price=None, price_note="Call for price on Controller and GlobalPlaneSearch; aerogurus prints $211,459", year=1972, model="A185F", tail="G-OMUD", serial=None, tt="3,050",
    history="Nearly £100,000 spent restoring the airframe, as advertised", location="Maidenhead, United Kingdom", country="GB", seller="Europlane Sales", sources=[("Controller",CTRL),("GlobalPlaneSearch",GPS)])
add(key="uk80", price=360000, year=1980, model="185F", tail=None, serial=None, tt="6,458",
    location="United Kingdom", country="GB", seller="Contact through the ad", sources=[("FindAircraft",FA)])
add(key="poland79", price=None, price_note="Call for price · open to a trade for a C182R or newer", year=1979, model="A185F", tail=None, serial=None, tt=None,
    engine="Continental IO-520-D 300 hp", panel="GFC 500 autopilot", history="Bought in the USA in 2021, shipped containerised, assembled by North Service",
    location="Białystok, Poland", country="PL", seller="Contact through the ad", sources=[("GlobalPlaneSearch",GPS)])
add(key="norway81", price=None, price_note="Call for price", year=1981, model="A185F", tail=None, serial=None, tt="1,139",
    location="Norway", country="NO", seller="Contact through the ad", sources=[("GlobalPlaneSearch",GPS)])
add(key="norway77", price=None, price_note="Call for price", year=1977, model="A185F", tail=None, serial=None, tt=None, gear="Amphibious floats",
    location="Rakkestad, Norway", country="NO", seller="Contact through the ad", sources=[("GlobalPlaneSearch",GPS)])
add(key="ZSCVI", price=160000, price_note="$150,000 also printed; plus VAT for South African buyers", year=1962, model="185A", tail="ZS-CVI", serial=None, tt="about 10,123",
    engine="Continental IO-470-F", location="South Africa", country="ZA", seller="Absolute Aircraft Sales", sources=[("GlobalPlaneSearch",GPS)])
add(key="ZSFNF", price=360000, price_note="R4,750,000", year=None, model="A185F", tail="ZS-FNF", serial=None, serial_note="Controller prints serial 185-04095, which the registries file under a different aircraft; not screened", tt="6,540",
    location="Sandton / Mosselbay / Johannesburg, South Africa (three sites, three locations)", country="ZA", seller="Contact through the ad", sources=[("Controller",CTRL),("Hangar67",H67),("GlobalPlaneSearch",GPS)])
add(key="V5RED", price=None, price_note="Call for price", year=None, model="A185F", tail="V5-RED", serial="18503573", tt="5,112",
    location="Namibia (listed from Sandton, South Africa)", country="NA", seller="Contact through the ad", sources=[("Controller",CTRL)])

DEPARTED = [
    {"tail":"N185TK","year":1982,"model":"A185F","last_price":265000,"tt":"17,192","how":"The Trade-A-Plane ad now reads Sold. The FAA registry has not yet changed hands.","location":"Santa Paula, CA"},
]
PRICE_MOVES = [k for k in L if k.get("price_was")]
NEW = []

SINCE = ("Quiet day. Nothing new came on the market. One airplane sold: the 1982 A185F in Santa Paula, California, N185TK, "
         "last asking $265,000 at 17,192 hours — the Trade-A-Plane ad now reads Sold, and the FAA registry has not changed hands yet. "
         "Two prices moved, both in Anchorage: N1795R went up from $180,000 to $190,000, and N18500 came down $5,000 to $250,000. "
         "In Switzerland, N4095L nudged up $918 to $313,809 on Controller. Every other asking price is where it was yesterday. "
         "This is the first day the record carries Cessna 180s; only one was sighted today, the 1965 180H in Chatham, New York, because the sweep was not yet looking for them. "
         "It will be from tomorrow.")
SOURCES_OK = ["Trade-A-Plane","Controller","Barnstormers","Hangar67","Craigslist","Facebook Marketplace","AircraftForSale","GlobalAir","GlobalPlaneSearch","FindAircraft","Kijiji","Canadian Aircraft Sales (csplane.com)","aircraftdealer.com","aerogurus","FAA registry"]
SOURCES_FAIL = ["AvPay"]
SOURCES_SKIP = ["ASO","planephd"]
PROV = "Every source above was reached except AvPay. Facebook Marketplace is searched at fourteen cities with a 40-mile radius each, so an ad far from any of them can be missed. aerogurus repeats sold inventory as live, so nothing from it is counted unless another site confirms it."
json.dump({"run_date":"2026-10-14","run_time":"6:12 AM Central","listings":L,"departed":DEPARTED,"new":NEW,"since_text":SINCE,
           "sources_ok":SOURCES_OK,"sources_fail":SOURCES_FAIL,"sources_skip":SOURCES_SKIP,"provenance":PROV},open("listings_2026-10-14.json","w"),indent=1,ensure_ascii=False)
print(len(L),"listings")
