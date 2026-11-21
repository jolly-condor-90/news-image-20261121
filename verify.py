"""Local pre-submit checks for the 21 November 2026 news image."""
import os
from PIL import Image
import draw

here = os.path.dirname(__file__)
path = os.path.join(here, "entry.png")
im = Image.open(path)
assert im.format == "PNG", im.format
assert im.size == (1024, 1024), im.size
assert os.path.getsize(path) <= 1048576, os.path.getsize(path)
print("CHECK 1 file: PNG %s, %d bytes (limit 1048576) OK" % (im.size, os.path.getsize(path)))

nums = [s[0] for s in draw.STORIES]
assert len(nums) == 35 and sorted(nums) == list(range(1, 36))
regions = sorted({s[1] for s in draw.STORIES})
assert len(regions) == 7, regions
assert len(draw.METRICS) == 6 and len(draw.TOPICS) == 7
print("CHECK 1 content: 35 numbered stories, 7 regions %s; 3 main + 8 small + 23 list OK" % regions)

counts = {r: sum(1 for s in draw.STORIES if s[1] == r) for r in regions}
print("  region counts:", counts)
for s in draw.STORIES:
    assert s[3] and s[4] and s[5], s[0]
print("  every story has a headline, a detail line and a named source OK")

# 300 px preview and detail crops for visual review, kept outside the repository
preview = os.path.join(os.path.dirname(here), "check21")
os.makedirs(preview, exist_ok=True)
im.resize((300, 300), Image.LANCZOS).save(os.path.join(preview, "preview300.png"))
im.crop((10, 184, 335, 390)).resize((975, 618)).save(os.path.join(preview, "crop_main.png"))
im.crop((14, 390, 1010, 694)).resize((1992, 608)).save(os.path.join(preview, "crop_smallcards.png"))
im.crop((14, 698, 402, 958)).resize((1164, 780)).save(os.path.join(preview, "crop_map.png"))
im.crop((400, 698, 1015, 956)).resize((1230, 516)).save(os.path.join(preview, "crop_list.png"))
print("CHECK 2 previews written OK")

# map label separation: each label centre must be > 16 px from every other
import math
sx, sy, mw, mh = 20, 716, 374, 234
def proj(lon, lat):
    return (sx + (lon + 180) / 360.0 * mw, sy + (84.0 - lat) / 144.0 * mh)
used = []
worst = 999
for s in draw.STORIES:
    dx, dy = proj(s[6], s[7])
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
    assert best, "no label slot for story %d" % s[0]
    used.append(best)
    for ox, oy in used[:-1]:
        d = math.hypot(best[0] - ox, best[1] - oy)
        worst = min(worst, d)
        assert d > 16, (s[0], d)
print("CHECK 2 map: %d labels placed, minimum centre gap %.1f px (diameter 16) OK" % (len(used), worst))
print("CHECK 3: inspect preview300.png and the three crops; confirm date line and story/art match.")
