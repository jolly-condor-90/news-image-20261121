"""Draw the 21 November 2026 world-news front page.

All artwork, the map and the layout are drawn in code with Pillow.
The day's stories were researched from public news reports dated 21 Nov 2026.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 229)
INK = (26, 25, 23)
RED = (166, 36, 39)
MUTED = (92, 84, 72)
HAIR = (120, 110, 94)
OCEAN = (206, 226, 238)
LAND = (217, 202, 164)
LAND_EDGE = (150, 137, 108)

REGIONS = [
    ("EUROPE", (35, 98, 158)),
    ("ASIA", (188, 112, 38)),
    ("MIDDLE EAST", (172, 143, 38)),
    ("AFRICA", (38, 132, 86)),
    ("AMERICAS", (120, 73, 174)),
    ("OCEANIA", (191, 54, 46)),
    ("WORLD", (91, 99, 108)),
]
RCOL = {name: col for name, col in REGIONS}

# number, region, place, headline, detail, source, lon, lat, heat
STORIES = [
    (1, "EUROPE", "ANTALYA, TÜRKIYE", "COP31 climate talks run into Saturday with no deal",
     "Talks passed Friday's deadline. A draft with no fossil-fuel text splits nearly 200 nations; a third text is due Saturday.",
     "AFP · AP · BBC", 36.9, 36.9, 12),
    (2, "MIDDLE EAST", "RIYADH, SAUDI ARABIA", "Three Houthi missiles shot down over Riyadh",
     "Coalition says air defences destroyed three ballistic missiles after two blasts. Third night of alerts; no casualties reported.",
     "Reuters · AFP", 46.7, 24.7, 11),
    (3, "AMERICAS", "JUNÍN, PERU", "Magnitude 6.7 quake shakes Peru's Andes",
     "Deep tremor near Carhuamayo was felt in Lima at 00:09 UTC. Officials report no damage, deaths or tsunami threat.",
     "USGS · IGP · AP", -75.5, -11.0, 10),
    (4, "EUROPE", "KYIV, UKRAINE", "Russian barrage kills at least eight in Kyiv",
     "Overnight strikes hit the power grid; Poland says two Russian missiles and a drone entered its airspace.",
     "AP · Reuters", 30.5, 50.5, 9),
    (5, "AMERICAS", "WASHINGTON, USA", "Trump threatens 'tremendous tax' on AI data centres abroad",
     "The president gave no details after returning from the China summit, and said his own staff had not been briefed.",
     "AP", -77.0, 38.9, 8),
    (6, "WORLD", "NEW YORK, USA", "Wall Street rout: S&P 500 −3.7%, Nasdaq −5.3%",
     "AI sell-off pushes the S&P and Dow into correction; Bitcoin slides below $56,000, a two-year low.",
     "AP · Reuters", -74.0, 40.7, 8),
    (7, "WORLD", "MERCURY ORBIT", "BepiColombo reaches Mercury after eight years",
     "ESA/JAXA craft fires its arrival burn; only the second mission ever to orbit the innermost planet.",
     "ESA · Sky & Telescope", 0.0, 76.0, 7),
    (8, "EUROPE", "BRUSSELS, BELGIUM", "UK and EU seal trade and youth-mobility deals",
     "A second annual summit agrees food trade, linked carbon markets and easier study and travel for young people.",
     "Xinhua · Guardian", 4.4, 50.9, 7),
    (9, "WORLD", "GENEVA, SWITZERLAND", "Countries open path to a 'killer robot' treaty",
     "The 128 states party to the weapons convention agree to elaborate rules for autonomous arms over two years.",
     "AFP", 6.1, 46.2, 6),
    (10, "OCEANIA", "WELLINGTON, NZ", "Rahul's 136 puts India ahead of New Zealand",
     "India reach 486-4 at stumps on day three in Wellington, a lead of 118 runs; Gill falls for 98.",
     "AP · RNZ", 174.8, -41.3, 6),
    (11, "ASIA", "MYANMAR", "Myanmar rejects UN court's genocide ruling",
     "The government calls the ICJ verdict unfair; Switzerland and the EU welcome it as a step for Rohingya justice.",
     "AP · Manila Times", 96.2, 16.8, 6),
    (12, "AFRICA", "BAYELSA, NIGERIA", "Ferry capsizes; at least four dead",
     "A boat carrying worshippers overturns; dozens are rescued and reported tolls differ between outlets.",
     "New Telegraph · Punch", 6.3, 4.9, 5),
    (13, "EUROPE", "COPENHAGEN", "Denmark expels Russian defence attaché",
     "Minister says 'enough is enough'; non-essential visas for Russians to stop.", "Anadolu", 12.6, 55.7, 5),
    (14, "EUROPE", "BERLIN", "Merz seeks '360-degree partnership' with Qatar",
     "Qatar pledges €15bn more in German investment; both sign defence pacts.", "Anadolu", 13.4, 52.5, 5),
    (15, "EUROPE", "PARIS", "France pushes fossil-fuel words into COP31 text",
     "Panama and island states back the demand; African group seeks adaptation cash.", "BBC · UN News", 2.4, 48.9, 5),
    (16, "OCEANIA", "SYDNEY", "Cricket Australia backs Pat Cummins as captain",
     "The board votes unanimously after the latest sandpaper-saga developments.", "ABC · RNZ", 151.2, -33.9, 5),
    (17, "ASIA", "TOKYO", "Nikkei plunges 5.1% on AI valuation fears",
     "The index closes at 56,436.65, its lowest since April, tracking Wall Street's sell-off.", "Xinhua", 139.7, 35.7, 5),
    (18, "ASIA", "NEW DELHI", "Delhi wakes to 'poor' air, AQI 279",
     "AIIMS and other hotspots record very poor air as smog settles over the capital.", "Indian Express", 77.2, 28.6, 4),
    (19, "ASIA", "MUMBAI", "Youth Congress workers held over Meta office vandalism",
     "Protest over suspended accounts leads to detentions in Hyderabad and Mumbai.", "Indian Express", 72.9, 19.1, 4),
    (20, "ASIA", "SINGAPORE", "Princess Aiko ends Singapore visit",
     "The Japanese princess visits Merlion Park on the last day of a 60th-anniversary trip.", "Kyodo", 103.8, 1.4, 4),
    (21, "ASIA", "KUALA LUMPUR", "Malaysia plans to resettle 10,000 Rohingya in Türkiye",
     "Announcement follows renewed international focus on the Rohingya crisis.", "AP · Manila Times", 101.7, 3.1, 4),
    (22, "OCEANIA", "AUCKLAND", "New Zealand may miss its 2030 HIV elimination target",
     "Auckland University research says access to prevention must improve; local diagnoses have fallen.", "NZ Herald", 174.8, -36.9, 4),
    (23, "ASIA", "FUKUSHIMA", "More than 1,000 isolated by heavy snow",
     "Fallen trees block roads around Kitashiobara village, stranding residents and hotel guests.", "Kyodo", 140.5, 37.8, 4),
    (24, "MIDDLE EAST", "STRAIT OF HORMUZ", "LPG tanker attacked; one Indian seafarer missing",
     "The Tara Gas is hit for a second time off Musandam; 21 of its 25 crew are Indian.", "The Hindu", 56.5, 26.5, 4),
    (25, "MIDDLE EAST", "TEHRAN", "Trump warns Iran over alleged 'dirty bomb' plot",
     "'Iran wants a deal, but not one acceptable to me,' the US president tells reporters.", "Anadolu · Xinhua", 51.4, 35.7, 4),
    (26, "MIDDLE EAST", "TEHRAN", "Iran: US naval blockade must end for oil exports to resume",
     "Foreign Minister Araghchi says Tehran is pursuing every route on exports and negotiations.", "Anadolu", 51.5, 35.6, 4),
    (27, "MIDDLE EAST", "RIYADH", "Japan agrees to buy up to 8m barrels of Saudi crude",
     "Deal for the national reserve also gives Saudi Arabia temporary Japanese storage.", "Anadolu", 46.8, 25.1, 3),
    (28, "MIDDLE EAST", "GAZA", "Displaced families brace for another winter in tents",
     "Floods worsen conditions in coastal camps as aid groups warn of the months ahead.", "Guardian", 34.5, 31.5, 3),
    (29, "AFRICA", "LAGOS", "Nigeria's petrol imports jump 47% in October",
     "Imports reach 15 million litres a day even as local refining expands.", "Punch", 3.4, 6.5, 3),
    (30, "AFRICA", "JOHANNESBURG", "South Africa mourns former deputy president Mlambo-Ngcuka",
     "The country's first female deputy president has died, news outlets report.", "IOL · Citizen", 28.0, -26.2, 3),
    (31, "AFRICA", "ACCRA", "Ghana meets euro convergence criteria",
     "The central bank says launch depends on logistics, not the economic tests.", "3News", -0.2, 5.6, 3),
    (32, "AFRICA", "NAIROBI", "Four jailed over Baringo land-dispute killings",
     "A court convicts four people in the case of a father and son killed over land.", "Citizen Digital", 36.8, -1.3, 3),
    (33, "AMERICAS", "MEXICO CITY", "Cartel leaders among 21 indicted in US court",
     "A grand jury charges La Nueva Familia Michoacana bosses with drugs, guns and people-smuggling.", "AP", -99.1, 19.4, 3),
    (34, "AMERICAS", "TAPACHULA", "Migrant caravan of about 250 enters Mexico",
     "The group crossed from Guatemala despite warnings from President Trump.", "AFP", -92.3, 14.9, 3),
    (35, "AMERICAS", "RIO GRANDE DO SUL", "Storm kills three and damages 8,000 homes",
     "Severe weather batters the Brazilian state; dozens more are injured.", "AGP · local reports", -51.2, -30.0, 3),
]

METRICS = [
    ("13", "DAY OF COP31, NO DEAL"),
    ("3", "MISSILES DOWN OVER RIYADH"),
    ("6.7", "MAGNITUDE, PERU QUAKE"),
    ("−3.7%", "S&P 500, FRIDAY CLOSE"),
    ("$55.6K", "BITCOIN, TWO-YEAR LOW"),
    ("8 YRS", "BEPICOLOMBO TO MERCURY"),
]

TOPICS = ["COP31 12", "SAUDI 9", "PERU 7", "MARKETS 6", "UKRAINE 5", "IRAN 4", "SPACE 3"]

FONT_DIR = r"C:\Windows\Fonts"
def font(size, bold=False, italic=False):
    name = "arialbd.ttf" if bold else ("ariali.ttf" if italic else "arial.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_KICK = font(13, True)
F_TINY = font(10)
F_MICRO = font(9)
F_BODY = font(12)
F_SMALL = font(11)
F_SMALLB = font(12, True)
F_CARD = font(19, True)
F_CARD2 = font(17, True)
F_LIST = font(10)
F_LISTB = font(11, True)
F_HEAD = font(54, True)
F_SUB = font(14, False, True)
F_MET = font(24, True)
F_LABEL = font(10, True)
F_MAPNUM = font(9, True)
F_BADGE = font(12, True)
F_TAG = font(10, True)
F_ISS = font(13, True)

def fit(d, s, f, width):
    """Longest prefix of s that fits width, measured in real pixels."""
    if d.textlength(s, font=f) <= width:
        return s
    lo, hi = 0, len(s)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if d.textlength(s[:mid], font=f) <= width:
            lo = mid
        else:
            hi = mid - 1
    return s[:max(0, lo - 1)].rstrip() + "…"

def text(d, xy, s, f, fill=INK, anchor=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def wrap(d, s, f, width):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def lines(d, xy, s, f, width, leading, fill=INK, max_lines=None):
    ls = wrap(d, s, f, width)
    if max_lines:
        ls = ls[:max_lines]
    y = xy[1]
    for line in ls:
        text(d, (xy[0], y), line, f, fill)
        y += leading
    return y

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def badge(d, x, y, num, region, size=17):
    col = RCOL[region]
    d.ellipse([x, y, x + size, y + size], fill=col, outline=PAPER, width=1)
    text(d, (x + size / 2, y + size / 2 + 0.5), str(num), F_MAPNUM, PAPER, "mm")

# ---------- illustrations ----------
def ill_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 233, 226))
    cx, cy, r = x + 58, y + 47, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 146, 168), outline=(35, 85, 100), width=2)
    for poly in [[(cx - 24, cy - 18), (cx - 8, cy - 24), (cx + 4, cy - 12), (cx - 6, cy - 2), (cx - 20, cy + 2)],
                 [(cx + 6, cy - 22), (cx + 26, cy - 16), (cx + 22, cy + 4), (cx + 8, cy + 10), (cx + 2, cy - 6)],
                 [(cx - 18, cy + 8), (cx - 2, cy + 6), (cx + 8, cy + 24), (cx - 10, cy + 28)]]:
        d.polygon(poly, fill=(116, 174, 124))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=1)
    # thermometer
    tx = x + 140
    d.rounded_rectangle([tx - 7, y + 18, tx + 7, y + 68], 7, fill=(250, 250, 246), outline=MUTED, width=2)
    d.ellipse([tx - 12, y + 61, tx + 12, y + 85], fill=RED)
    d.rectangle([tx - 3, y + 33, tx + 3, y + 72], fill=RED)
    for k in range(4):
        d.line([tx + 8, y + 28 + k * 10, tx + 14, y + 28 + k * 10], fill=MUTED, width=1)
    text(d, (tx + 16, y + 34), "+1.5°C", F_TAG, RED)
    # clock at 13:00
    ox, oy, orr = x + 216, y + 47, 21
    d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr], fill=(252, 251, 245), outline=MUTED, width=2)
    for k in range(12):
        a = k * math.pi / 6
        d.line([ox + 17 * math.sin(a), oy - 17 * math.cos(a), ox + 20 * math.sin(a), oy - 20 * math.cos(a)], fill=MUTED)
    d.line([ox, oy, ox, oy - 14], fill=INK, width=2)
    d.line([ox, oy, ox + 10, oy + 4], fill=INK, width=2)
    text(d, (ox, oy + orr + 5), "DAY 13", F_MICRO, RED, "ma")
    # draft papers
    px = x + 274
    for k in (0, 1, 2):
        d.rectangle([px + k * 6, y + 20 + k * 4, px + 30 + k * 6, y + 70 + k * 4],
                    fill=(255, 255, 250), outline=MUTED, width=1)
    text(d, (px + 20, y + 62), "DRAFT 3", F_MICRO, INK, "ma")
    rrect(d, [x + 4, y + h - 18, x + 128, y + h - 3], 3, fill=RED)
    text(d, (x + 10, y + h - 16), "NO DEAL · OVERTIME", F_TAG, (255, 255, 255))

def ill_missiles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 35, 60))
    for k in range(26):
        sx = x + 7 + k * 12
        sy = y + 9 + (k * 17) % 40
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(172, 190, 214))
    # skyline
    heights = [22, 34, 26, 46, 30, 38, 24, 42, 28]
    bx = x + 12
    for k, hh in enumerate(heights):
        d.rectangle([bx + k * 34, y + h - hh, bx + k * 34 + 27, y + h], fill=(48, 60, 88))
        for wy in range(y + h - hh + 6, y + h - 4, 9):
            for wx in range(bx + k * 34 + 5, bx + k * 34 + 23, 8):
                d.rectangle([wx, wy, wx + 2, wy + 3], fill=(222, 186, 96))
    for k, off in enumerate((0, 16, 32)):
        pts = []
        for t in range(25):
            px = x + 28 + t * 8.6
            py = y + 64 - off - 38 * math.sin(t / 24 * math.pi) + t * 0.42
            pts.append((px, py))
        d.line(pts, fill=(240, 213, 138), width=2)
        ex, ey = pts[-1]
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(238, 154, 63))
        d.line([ex - 11, ey, ex + 11, ey], fill=(255, 222, 140), width=1)
        d.line([ex, ey - 11, ex, ey + 11], fill=(255, 222, 140), width=1)
    rrect(d, [x + 8, y + 7, x + 106, y + 26], 3, fill=(190, 44, 44))
    text(d, (x + 14, y + 10), "3 DOWNED", F_TAG, (255, 255, 255))
    text(d, (x + w - 8, y + h - 15), "RIYADH · 01:45 UTC", F_MICRO, (208, 218, 235), "ra")

def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    d.polygon([(x, y + h), (x + 60, y + 34), (x + 112, y + h)], fill=(182, 166, 133))
    d.polygon([(x + 82, y + h), (x + 150, y + 44), (x + 220, y + h)], fill=(160, 145, 115))
    for k in range(3):
        hx = x + 185 + k * 38
        hy = y + h - 30
        d.rectangle([hx, hy - 16, hx + 24, hy], fill=(228, 216, 190), outline=LAND_EDGE)
        d.polygon([(hx - 3, hy - 16), (hx + 12, hy - 27), (hx + 27, hy - 16)], fill=(168, 86, 66))
    pts = []
    for k in range(70):
        px = x + 8 + k * 4.4
        base = y + 62
        if 18 < k < 26:
            base -= 10
        if 26 <= k < 46:
            base += ((-1) ** k) * (16 - abs(32 - k))
        pts.append((px, base))
    d.line(pts, fill=RED, width=2)
    rrect(d, [x + 8, y + 6, x + 74, y + 24], 3, fill=RED)
    text(d, (x + 14, y + 9), "M6.7", F_TAG, (255, 255, 255))
    text(d, (x + w - 8, y + 8), "00:09 UTC · 108 km", F_MICRO, MUTED, "ra")

MINI = ["fire", "AI", "chart", "planet", "deal", "robot", "bat", "boat"]
def ill_mini(d, x, y, w, h, kind, col):
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 220))
    cx = x + 18
    if kind == "fire":
        d.rectangle([cx - 8, y + 4, cx + 8, y + 21], fill=(120, 128, 140))
        d.polygon([(cx - 5, y + 4), (cx, y - 3), (cx + 6, y + 5)], fill=(210, 90, 50))
    elif kind == "AI":
        d.rectangle([cx - 9, y + 2, cx + 9, y + 20], fill=(60, 70, 95))
        for k in range(3):
            d.line([cx - 6, y + 6 + k * 5, cx + 6, y + 6 + k * 5], fill=(150, 205, 230), width=1)
        text(d, (cx + 15, y + 6), "AI", F_MICRO, RED)
    elif kind == "chart":
        d.line([(cx - 9, y + 4), (cx - 3, y + 10), (cx + 2, y + 7), (cx + 9, y + 19)], fill=RED, width=2)
        d.line([cx - 10, y + 20, cx + 10, y + 20], fill=MUTED)
    elif kind == "planet":
        d.ellipse([cx - 8, y + 3, cx + 8, y + 19], fill=(168, 142, 106))
        d.ellipse([cx - 13, y + 8, cx + 13, y + 14], outline=(130, 110, 80), width=1)
    elif kind == "deal":
        d.polygon([(cx - 10, y + 12), (cx - 2, y + 6), (cx + 3, y + 13), (cx + 10, y + 8)],
                  fill=(196, 152, 108))
    elif kind == "robot":
        d.rectangle([cx - 7, y + 5, cx + 7, y + 18], fill=(100, 106, 122))
        d.line([cx, y + 18, cx + 7, y + 22, cx + 12, y + 14], fill=(100, 106, 122), width=2)
    elif kind == "bat":
        d.line([cx - 9, y + 19, cx + 9, y + 3], fill=(150, 118, 78), width=3)
        d.ellipse([cx + 6, y + 1, cx + 12, y + 7], fill=RED)
    else:
        d.polygon([(cx - 11, y + 14), (cx + 11, y + 14), (cx + 5, y + 21), (cx - 6, y + 21)], fill=(86, 130, 156))
        d.line([cx, y + 14, cx + 3, y + 2], fill=MUTED)

def draw_map(d, sx, sy, mw, mh):
    d.rectangle([sx, sy, sx + mw, sy + mh], fill=OCEAN, outline=HAIR)
    geo = json.load(open(os.path.join(os.path.dirname(__file__), "world110.geojson"), encoding="utf-8"))
    def proj(lon, lat):
        return (sx + (lon + 180) / 360.0 * mw,
                sy + (84.0 - lat) / 144.0 * mh)
    for lon in range(-150, 181, 30):
        a = proj(lon, 84); b = proj(lon, -60)
        d.line([a, b], fill=(188, 211, 225), width=1)
    for lat in range(-40, 81, 20):
        a = proj(-180, lat); b = proj(180, lat)
        d.line([a, b], fill=(188, 211, 225), width=1)
    for feat in geo["features"]:
        g = feat["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = poly[0]
            pts = [proj(p[0], p[1]) for p in ring if -60 <= p[1] <= 84]
            if len(pts) > 2:
                d.polygon(pts, fill=LAND)
                d.line(pts + [pts[0]], fill=LAND_EDGE, width=1)
    used = []
    for s in STORIES:
        n, reg, _place, _h, _b, _src, lon, lat, _heat = s
        dx, dy = proj(lon, lat)
        col = RCOL[reg]
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=col, outline=(255, 255, 255), width=1)
        best = None
        for rad in (11, 17, 24, 31, 38, 45):
            for k in range(12):
                a = k * math.pi / 6 + (rad / 11.0)
                lx = dx + rad * math.cos(a)
                ly = dy + rad * math.sin(a) * 0.78
                if not (sx + 10 < lx < sx + mw - 10 and sy + 10 < ly < sy + mh - 10):
                    continue
                if all((lx - ox) ** 2 + (ly - oy) ** 2 > 17 ** 2 for ox, oy in used):
                    best = (lx, ly)
                    break
            if best:
                break
        if best is None:
            best = (dx, dy - 12)
        lx, ly = best
        used.append(best)
        d.line([dx, dy, lx, ly], fill=col, width=1)
        d.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=col, outline=PAPER, width=1)
        text(d, (lx, ly + 0.5), str(n), F_MAPNUM, (255, 255, 255), "mm")

def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # masthead
    text(d, (14, 10), "THE WORLD IN ONE DAY", F_KICK, RED)
    text(d, (W - 14, 12), "35 STORIES · 7 REGIONS · EVERY STORY DATED SATURDAY 21 NOVEMBER 2026",
         F_TINY, MUTED, "ra")
    text(d, (W / 2, 56), "Saturday 21 November 2026", F_HEAD, INK, "mm")
    text(d, (W / 2, 99), "COP31 overtime  ·  three missiles down over Riyadh  ·  M6.7 Peru quake  ·  Bitcoin below $56k",
         F_SUB, RED, "mm")
    d.line([14, 112, W - 14, 112], fill=INK, width=2)

    # six big numbers
    cw = (W - 28) / 6
    for k, (val, lab) in enumerate(METRICS):
        x = 14 + k * cw
        if k:
            d.line([x, 118, x, 160], fill=HAIR, width=1)
        text(d, (x + 8, 116), val, F_MET, RED)
        text(d, (x + 8, 147), lab, F_LABEL, MUTED)
    d.line([14, 166, W - 14, 166], fill=INK, width=1)

    # most-reported topics, ordered by number of reports
    text(d, (14, 171), "MOST-REPORTED TOPICS →", F_LABEL, INK)
    tx = 168
    for k, t in enumerate(TOPICS):
        col = REGIONS[k % 7][1]
        tw = d.textlength(t, font=F_TAG) + 14
        rrect(d, [tx, 169, tx + tw, 184], 3, fill=col)
        text(d, (tx + 7, 170), t, F_TAG, (255, 255, 255))
        tx += tw + 5
    d.line([14, 190, W - 14, 190], fill=HAIR, width=1)

    # region legend
    counts = {}
    for s in STORIES:
        counts[s[1]] = counts.get(s[1], 0) + 1
    lx = 14
    for name, col in REGIONS:
        lab = "%s %d" % (name, counts.get(name, 0))
        lw = d.textlength(lab, font=F_LABEL) + 12
        d.rectangle([lx, 195, lx + lw, 210], fill=col)
        text(d, (lx + 6, 197), lab, F_LABEL, (255, 255, 255))
        lx += lw + 4
    d.line([14, 215, W - 14, 215], fill=INK, width=2)

    # three main cards
    ills = [ill_globe, ill_missiles, ill_quake]
    for i in range(3):
        s = STORIES[i]
        x = 14 + i * 338
        y = 220
        w, h = 322, 216
        d.rectangle([x, y, x + w, y + h], fill=(255, 254, 249), outline=HAIR, width=1)
        ills[i](d, x + 1, y + 1, w - 2, 90)
        d.rectangle([x + 1, y + 91, x + w - 1, y + 110], fill=RCOL[s[1]])
        text(d, (x + 7, y + 94), str(s[0]), F_BADGE, (255, 255, 255))
        place = fit(d, s[2] + "  ·  " + s[1], F_SMALL, w - 108)
        text(d, (x + 28, y + 95), place, F_SMALL, (255, 255, 255))
        text(d, (x + w - 6, y + 96), s[5], F_MICRO, (255, 255, 255), "ra")
        yy = lines(d, (x + 8, y + 115), s[3], F_CARD, w - 16, 22, INK, 2)
        lines(d, (x + 8, yy + 4), s[4], F_BODY, w - 16, 15, INK, 3)

    # eight small cards
    for i in range(8):
        s = STORIES[3 + i]
        row, col = divmod(i, 4)
        x = 14 + col * 250
        y = 442 + row * 107
        w, h = 244, 101
        d.rectangle([x, y, x + w, y + h], fill=(255, 254, 249), outline=HAIR, width=1)
        d.rectangle([x + 1, y + 1, x + w - 1, y + 24], fill=(236, 231, 217))
        badge(d, x + 5, y + 4, s[0], s[1], 16)
        ill_mini(d, x + 30, y + 3, 40, 20, MINI[i], RCOL[s[1]])
        text(d, (x + w - 6, y + 6), s[1], F_MICRO, MUTED, "ra")
        lines(d, (x + 7, y + 29), s[3], F_CARD2, w - 14, 19, INK, 2)
        lines(d, (x + 7, y + 69), s[4] + " (" + s[5] + ")", F_TINY, w - 14, 13, MUTED, 2)

    # bottom: map left, story list right
    d.line([14, 655, W - 14, 655], fill=INK, width=2)
    rrect(d, [14, 662, 400, 934], 3, fill=(255, 254, 249), outline=HAIR)
    text(d, (20, 665), "WHERE IT HAPPENED", F_LABEL, INK)
    draw_map(d, 20, 681, 374, 235)
    text(d, (20, 920), "Numbers 1–35, coloured by region · dots and leader lines keep labels apart", F_MICRO, MUTED)

    text(d, (408, 665), "ALSO ON SATURDAY 21 NOVEMBER — 23 MORE STORIES", F_LABEL, INK)
    for idx, s in enumerate(STORIES[12:]):
        col, row = divmod(idx, 12)
        x = 408 + col * 300
        y = 684 + row * 20
        d.rectangle([x, y + 1, x + 13, y + 13], fill=RCOL[s[1]])
        text(d, (x + 6.5, y + 7), str(s[0]), F_MICRO, (255, 255, 255), "mm")
        label = s[3]
        if d.textlength(s[2].title() + " — " + label, font=F_LIST) <= 279:
            label = s[2].title() + " — " + label
        text(d, (x + 17, y + 1), fit(d, label, F_LIST, 279), F_LIST, INK)

    # footer
    rrect(d, [14, 940, W - 14, 991], 3, fill=(252, 246, 230), outline=RED, width=1)
    text(d, (21, 944), "DATE CHECK:", F_LISTB, RED)
    lines(d, (108, 944),
          "Every story above happened, or was first reported, on Saturday 21 November 2026 in at least one time zone. "
          "Nothing from 19 or 20 November is counted; disputed claims are attributed to their source.",
          F_SMALL, W - 140, 14, INK, 2)
    text(d, (14, 997),
         "Sources: Reuters · AP · AFP · BBC · Al Jazeera · ESA · USGS · Kyodo · Anadolu · Guardian · Punch · ABC · RNZ. "
         "Map from Natural Earth 110m; all illustrations and layout drawn in code.",
         F_MICRO, MUTED)

    out = os.path.join(os.path.dirname(__file__), "entry.png")
    im.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    build()
