"""Site advance map builder (skill v0.12): overview map, four close-ups and Street View viewpoints for any venue.
Usage: python3 make_map.py <folder>/venue.json
Needs <folder>/img/site.jpg: a Mapbox satellite image, 2000x1600 at @2x, centered on map.center at map.zoom (17 or 18).
Every pixel position in the JSON is on that 2000x1600 image. See venue-example.json for every field."""
import math, json, os, random, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(sys.argv[1])); os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
MP = D["map"]
LON0, LAT0 = MP["center"]; Z = MP.get("zoom", 17); CX, CY = 1000, 800
KX = 256 * 2 ** Z * 2 / 360.0; KY = KX / math.cos(math.radians(LAT0))
def ll(x, y): return (LAT0 - (y - CY) / KY, LON0 + (x - CX) / KX)
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, "fonts", f"Inter-{w}.ttf"), s)
NAVY = (15, 27, 45); AMBER = (227, 163, 59); BLUE = (31, 95, 191); ORANGE = (217, 119, 43); WHITE = (255, 255, 255); INK2 = (96, 38, 128)
COL = {"blue": BLUE, "navy": NAVY, "amber": AMBER, "grey": (90, 101, 119)}


def wobble(pts, seed):
    random.seed(seed); out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for t in [i / 8 for i in range(8)]:
            out.append((x0 + (x1 - x0) * t + random.uniform(-2.5, 2.5), y0 + (y1 - y0) * t + random.uniform(-2.5, 2.5)))
    out.append(tuple(pts[-1])); return out


def arrow(d, pts, seed):
    w = wobble(pts, seed)
    d.line(w, fill=WHITE + (200,), width=16, joint="curve"); d.line(w, fill=INK2 + (255,), width=9, joint="curve")
    (x0, y0), (x1, y1) = pts[-2], pts[-1]; a = math.atan2(y1 - y0, x1 - x0); L = 34
    d.polygon([(x1, y1), (x1 - L * math.cos(a - 0.5), y1 - L * math.sin(a - 0.5)), (x1 - L * math.cos(a + 0.5), y1 - L * math.sin(a + 0.5))],
              fill=INK2 + (255,), outline=WHITE + (255,))


def lab(d, t, xy, fill=NAVY, fg=WHITE, size=30):
    f = F("SemiBold", size); bb = d.textbbox(tuple(xy), t, font=f, anchor="lm")
    d.rounded_rectangle([bb[0] - 10, bb[1] - 10, bb[2] + 10, bb[3] + 10], 8, fill=tuple(fill) + (235,)); d.text(tuple(xy), t, font=f, fill=fg, anchor="lm")


def draw(labels):
    im = Image.open("img/site.jpg").convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for z in MP.get("zones", []):  # amber areas: crowds, lines
        d.polygon([tuple(p) for p in z["polygon"]], fill=AMBER + (90,), outline=AMBER + (255,))
    for i, a in enumerate(MP.get("arrows", [])):
        arrow(d, a["path"], i)
    for p in MP["points"]:
        x, y = p["xy"]; r = 34
        if p.get("ring", True): d.ellipse([x - r - 9, y - r - 9, x + r + 9, y + r + 9], outline=ORANGE + (255,), width=8)
        d.ellipse([x - r, y - r, x + r, y + r], fill=COL[p.get("color", "blue")] + (255,), outline=WHITE + (255,), width=5)
        d.text((x, y + 1), p["mark"], font=F("Bold", 30), fill=WHITE, anchor="mm")
        if labels: lab(d, p["label"], (x + p.get("dx", 50), y + p.get("dy", 0)))
    for a in MP.get("arrows", []):
        d.text(tuple(a["label_xy"]), a["label"], font=F("Bold", 30), fill=INK2 + (255,), anchor="mm", stroke_width=5, stroke_fill=WHITE + (255,))
    for wx, wy in MP.get("warnings", []):
        d.polygon([(wx, wy - 40), (wx + 44, wy + 34), (wx - 44, wy + 34)], fill=AMBER + (255,), outline=WHITE + (255,))
        d.text((wx, wy + 10), "!", font=F("ExtraBold", 44), fill=WHITE, anchor="mm")
    if labels:
        for n in MP.get("notes", []):  # {"text", "xy", "style": "amber"|"grey"}
            st = n.get("style", "amber")
            lab(d, n["text"], n["xy"], AMBER if st == "amber" else (60, 60, 60), NAVY if st == "amber" else WHITE, 28)
        mpp = 156543.03392 * math.cos(math.radians(LAT0)) / (2 ** Z) / 2; s = 50 / mpp; x0, y0 = 70, 1500
        d.rectangle([x0 - 20, y0 - 60, x0 + s + 20, y0 + 30], fill=(255, 255, 255, 220)); d.line([(x0, y0), (x0 + s, y0)], fill=NAVY + (255,), width=8)
        for xx in (x0, x0 + s): d.line([(xx, y0 - 14), (xx, y0 + 14)], fill=NAVY + (255,), width=6)
        d.text((x0 + s / 2, y0 - 32), "50 m", font=F("Bold", 30), fill=NAVY, anchor="mm")
        nx, ny = 120, 120; d.ellipse([nx - 50, ny - 50, nx + 50, ny + 50], fill=(255, 255, 255, 220))
        d.polygon([(nx, ny - 38), (nx + 22, ny + 26), (nx, ny + 12), (nx - 22, ny + 26)], fill=NAVY + (255,))
        d.text((nx, ny + 70), "N", font=F("Bold", 32), fill=WHITE, anchor="mm")
        for t in MP.get("place_labels", []):  # e.g. river or park names
            d.text(tuple(t["xy"]), t["text"], font=F("Bold", 34), fill=(255, 255, 255, 200), anchor="mm")
    return Image.alpha_composite(im, ov).convert("RGB")


draw(True).save("img/overview.jpg", quality=88)
m = draw(False)
thumb = Image.open("img/site.jpg").convert("RGB")
for k, b in MP["crops"].items():  # 700x560 boxes: [x0, y0, x0+700, y0+560]
    cr = m.crop(tuple(b)); tw, th = 230, 184; t = thumb.resize((tw, th)); td = ImageDraw.Draw(t)
    sx, sy = tw / 2000, th / 1600
    td.rectangle([b[0] * sx, b[1] * sy, b[2] * sx, b[3] * sy], outline=(220, 40, 40), width=4)
    lx, ly = MP.get("locator_xy", [1000, 800])
    td.text((lx * sx, ly * sy), MP.get("locator_label", D["short"]), font=F("Bold", 14), fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=NAVY)
    bx, by = 10, cr.size[1] - th - 10; cd = ImageDraw.Draw(cr)
    cd.rectangle([bx - 4, by - 4, bx + tw + 3, by + th + 3], fill=(255, 255, 255)); cr.paste(t, (bx, by))
    cr.save(f"img/crop-{k}.jpg", quality=90)
# Street View viewpoints: a spot on the street outside each point, with the heading that faces the building
out = {k: {"lat": round(ll(*v["xy"])[0], 6), "lon": round(ll(*v["xy"])[1], 6), "heading": v.get("heading")} for k, v in MP["viewpoints"].items()}
json.dump(out, open("img/viewpoints.json", "w"), indent=1); print("wrote img/overview.jpg, crops and img/viewpoints.json")
