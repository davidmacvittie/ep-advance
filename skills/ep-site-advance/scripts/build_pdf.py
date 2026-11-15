"""Site advance packet builder (skill v0.12). Same 7 pages for every venue; everything venue-specific comes from venue.json.
Usage: python3 build_pdf.py <folder>/venue.json   (images and viewpoints paths in the JSON are relative to that folder)
See venue-example.json (Kennedy Center test) for every field."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
D = json.load(open(sys.argv[1])); os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
CODE = D.get("code", "ATLAS"); SHORT = D["short"]
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing, Circle, String
from reportlab.graphics import renderPDF
for w in ["Regular", "Medium", "SemiBold", "Bold", "Italic"]:
    pdfmetrics.registerFont(TTFont(f"Inter-{w}", os.path.join(HERE, "fonts", f"Inter-{w}.ttf")))
# "Inter-ExtraBold" is drawn with the bold file (no extra-bold font is shipped)
pdfmetrics.registerFont(TTFont("Inter-ExtraBold", os.path.join(HERE, "fonts", "Inter-Bold.ttf")))
pdfmetrics.registerFontFamily("Inter-Regular", normal="Inter-Regular", bold="Inter-Bold", italic="Inter-Italic", boldItalic="Inter-Bold")
from route_icons import draw_icon, NAVY, INK, SLATE, LINE, AMBER, GREEN, RED, BLUE, PALE, ORANGE, LBLUE

W, H = landscape(letter); M = 28; TOTAL = 7
PURPLE = colors.HexColor("#6B4FA0"); GREY = colors.HexColor("#5A6577"); AMBERPALE = colors.HexColor("#FBF1DF"); GREENPALE = colors.HexColor("#E6F2EB")
OUT = D["out"]
st = {"b": ParagraphStyle("b", fontName="Inter-Regular", fontSize=9, leading=11.6, textColor=INK),
      "c": ParagraphStyle("c", fontName="Inter-Regular", fontSize=8.7, leading=10.8, textColor=INK),
      "s": ParagraphStyle("s", fontName="Inter-Regular", fontSize=8, leading=10.2, textColor=INK),
      "sm": ParagraphStyle("sm", fontName="Inter-Regular", fontSize=7.4, leading=9.4, textColor=SLATE),
      "th": ParagraphStyle("th", fontName="Inter-Bold", fontSize=7.8, leading=9.6, textColor=colors.white)}
def P(t, k="s"): return Paragraph(t, st[k])
VP = json.load(open(D.get("viewpoints", "img/viewpoints.json")))
def sv_url(k):
    v = VP[k]; u = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={v['lat']},{v['lon']}"
    return u + (f"&heading={v['heading']}" if v["heading"] is not None else "")
def map_url(k): v = VP[k]; return f"https://www.google.com/maps/search/?api=1&query={v['lat']},{v['lon']}"
def link(k, t="Street View"): return f"<link href='{sv_url(k)}' color='#1F5FBF'><u>{t}</u></link>"

SUB = D["sub"]
def header(c, n, title):
    c.setFillColor(NAVY); c.roundRect(M, H - M - 42, W - 2 * M, 42, 6, stroke=0, fill=1)
    c.setFillColor(colors.white); c.circle(M + 22, H - M - 21, 12, stroke=0, fill=1)
    c.setFillColor(NAVY); c.setFont("Inter-Bold", 11); c.drawCentredString(M + 22, H - M - 25, str(n))
    c.setFillColor(colors.white); c.setFont("Inter-Bold", 15); c.drawString(M + 44, H - M - 19, title)
    c.setFont("Inter-Regular", 7.6); c.drawString(M + 44, H - M - 33, SUB)
    c.setFillColor(colors.HexColor("#2A3A55")); c.roundRect(W - M - 118, H - M - 29, 108, 16, 8, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Inter-Bold", 7); c.drawCentredString(W - M - 64, H - M - 24, f"SITE ADVANCE  |  {CODE}")
def footer(c, n):
    c.setFillColor(NAVY); c.rect(M, M - 6, W - 2 * M, 16, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Inter-Bold", 6.6); c.drawString(M + 8, M - 1, D.get("footer_tag", "SITE ADVANCE") + f"  |  SITE ADVANCE  |  {CODE}")
    c.setFont("Inter-Regular", 6.6); c.drawCentredString(W / 2 + 40, M - 1, "Draft. Confirm on your visit and with current conditions before use. Team only. Do not forward.")
    c.setFont("Inter-Bold", 6.6); c.drawRightString(W - M - 8, M - 1, f"Page {n} of {TOTAL}")
def sec(c, x, y, title, kind="info", col=NAVY):
    if kind == "info":
        c.setFillColor(col); c.circle(x + 7, y - 6, 7, stroke=0, fill=1); c.setFillColor(colors.white); c.setFont("Inter-Bold", 8); c.drawCentredString(x + 7, y - 9, "i")
    else: draw_icon(c, kind, x + 7, y - 6, 7)
    c.setFillColor(NAVY); c.setFont("Inter-Bold", 10); c.drawString(x + 19, y - 9.5, title.upper()); return y - 20
def para(c, text, x, y, w, k="s"):
    p = P(text, k); _, h = p.wrap(w, 1000); p.drawOn(c, x, y - h); return y - h
def table(c, data, x, y, widths, head=True, zebra=True, styles=()):
    rows = [[P(v, "th") if (head and i == 0 and isinstance(v, str)) else (P(v) if isinstance(v, str) else v) for v in r] for i, r in enumerate(data)]
    t = Table(rows, colWidths=widths)
    ts = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE)]
    if head: ts.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra: ts += [("BACKGROUND", (0, i), (-1, i), PALE) for i in range(1 if head else 0, len(rows)) if i % 2 == 0]
    t.setStyle(TableStyle(ts + list(styles))); _, h = t.wrap(sum(widths), 1000); t.drawOn(c, x, y - h); return y - h
def box(c, x, y, w, h, fill=PALE): c.setFillColor(fill); c.roundRect(x, y - h, w, h, 5, stroke=0, fill=1)
def cbox(c, x, y): c.setStrokeColor(SLATE); c.setLineWidth(0.7); c.rect(x, y - 8, 7, 7, stroke=1, fill=0)
def mark(text, col, size=12, ring=False):
    d = Drawing(size + 4, size + 4)
    if ring: d.add(Circle(size / 2 + 2, size / 2 + 2, size / 2 + 1.6, fillColor=None, strokeColor=ORANGE, strokeWidth=1.4))
    d.add(Circle(size / 2 + 2, size / 2 + 2, size / 2 - 0.3, fillColor=col, strokeColor=colors.white, strokeWidth=0.8))
    d.add(String(size / 2 + 2, size / 2 - 0.4, text, fontName="Inter-Bold", fontSize=size * (0.5 if len(text) > 1 else 0.62), fillColor=colors.white, textAnchor="middle"))
    return d
def qr(c, url, x, y, s):
    w = QrCodeWidget(url); b = w.getBounds(); d = Drawing(s, s, transform=[s / (b[2] - b[0]), 0, 0, s / (b[3] - b[1]), 0, 0]); d.add(w); renderPDF.draw(d, c, x, y)
    c.linkURL(url, (x, y, x + s, y + s), relative=0)

c = canvas.Canvas(OUT, pagesize=(W, H)); c.setTitle(f"Site Advance: {SHORT} ({CODE})"); c.setAuthor("EP site advance")
TOP = H - M - 56

# ======================= PAGE 1: AT A GLANCE (information only)
header(c, 1, f"{SHORT}: At a Glance")
LW = 380; RX = M + LW + 18; RW = W - M - RX
y = sec(c, M, TOP, "The venue")
y = table(c, D["venue_rows"], M, y, [64, LW - 64], head=False)
y -= 10
y = sec(c, M, y, "Nearest help")
y = table(c, D["help_rows"], M, y, [84, LW - 84], head=False)
y = para(c, D["help_note"], M, y - 4, LW, "sm") - 8
y = sec(c, M, y, "Getting there")
table(c, D["getting_there"], M, y, [84, LW - 84], head=False)

y = sec(c, RX, TOP, "Data inputs required")
y = table(c, D["inputs"], RX, y, [96, RW - 96], head=False)
y = para(c, D.get("inputs_note", "That's all the user gave. Everything else in this packet was pulled from public sources."), RX, y - 4, RW, "sm") - 10
y = sec(c, RX, y, "Light", "sunset")
for i, (k, a, b) in enumerate(D["light"]):
    xx = RX + i * (RW / 3); draw_icon(c, k, xx + 9, y - 8, 8)
    c.setFillColor(INK); c.setFont("Inter-Bold", 9); c.drawString(xx + 21, y - 7, a); c.setFillColor(SLATE); c.setFont("Inter-Regular", 6.8); c.drawString(xx + 21, y - 16, b)
y -= 32
y = sec(c, RX, y, "Worth knowing", "warn")
for k, t in D["worth"]:
    draw_icon(c, k, RX + 7, y - 6, 6.5); y = para(c, t, RX + 19, y, RW - 19, "s") - 5

ty = 98
CL = D["clash"]
def tm(t): h, m = t.split(":"); return int(h) * 60 + int(m)
def lab12(v): h, m = divmod(v, 60); return f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"
c.setFillColor(NAVY); c.setFont("Inter-Bold", 10); c.drawString(M, ty + 52, f"THE CLASH: PUBLIC ACTIVITY VS. {CODE}")
x0, x1 = M + 70, W - M - 20; t0, t1 = tm(CL["start"]), tm(CL["end"])
X = lambda v: x0 + (v - t0) / (t1 - t0) * (x1 - x0)
c.setStrokeColor(LINE); c.setLineWidth(1)
for v in range(t0 - t0 % 30, t1 + 1, 30):
    if v >= t0:
        xx = X(v); c.line(xx, ty - 30, xx, ty + 38); c.setFillColor(SLATE); c.setFont("Inter-Regular", 6.5); c.drawCentredString(xx, ty - 40, lab12(v))
c.setFillColor(SLATE); c.setFont("Inter-Bold", 7.2); c.drawString(M, ty + 17, "Public"); c.drawString(M, ty - 15, CODE)
for b in CL["public"]:
    c.setFillColor(AMBERPALE if b.get("color", "amber") == "amber" else colors.HexColor("#F6D9D9")); c.rect(X(tm(b["from"])), ty + 10, X(tm(b["to"])) - X(tm(b["from"])), 16, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont("Inter-SemiBold", 6.8); c.drawString(X(tm(b["from"])) + 6, ty + 15, b["text"])
ev = CL["event"]; a, l = tm(CL["arrive"]), tm(CL["leave"])
c.setFillColor(LBLUE); c.rect(X(a), ty - 22, X(l) - X(a), 16, stroke=0, fill=1)
c.setFillColor(colors.white); c.setFont("Inter-SemiBold", 6.8); c.drawString(X(max(a, tm(ev["from"]))) + 4, ty - 17, ev["text"])
for v in (a, l): c.setFillColor(RED); c.circle(X(v), ty - 14, 4, stroke=0, fill=1)
c.setFillColor(RED); c.setFont("Inter-Bold", 6.8)
c.drawString(X(a) - 4, ty - 52, CL["arrive_label"]); c.drawRightString(min(X(l) + 30, W - M), ty - 52, CL["leave_label"])
footer(c, 1); c.showPage()

# ======================= PAGE 2: OVERVIEW MAP
header(c, 2, f"{SHORT}: Overview Map")
iw = 500; ih = iw * 0.8
c.drawImage(D["overview"]["image"], M, TOP - ih, iw, ih)
c.setFillColor(SLATE); c.setFont("Inter-Regular", 6.2)
c.drawString(M, TOP - ih - 9, D["overview"]["credit"])
RX2 = M + iw + 14; RW2 = W - M - RX2
y = sec(c, RX2, TOP, "Every known point")
MC = {"blue": LBLUE, "navy": NAVY, "amber": AMBER, "grey": GREY}
rows = [["", "Point", "Source", "Link"]] + [[mark(m, MC[col], ring=ring), t, src, P(link(vk, "View"))] for m, col, ring, t, src, vk in D["points"]]
y = table(c, rows, RX2, y, [22, 118, 52, RW2 - 192])
y -= 8
c.setStrokeColor(ORANGE); c.setLineWidth(1.4); c.circle(RX2 + 7, y - 5, 5, stroke=1, fill=0)
c.setFillColor(INK); c.setFont("Inter-Regular", 7.4); c.drawString(RX2 + 18, y - 8, "Orange ring: spot read from the map. Confirm on your visit.")
y -= 18
y = para(c, "<b>Purple arrows</b> show the ways in and out from the street. <b>Street View links</b> open Google Maps at the street outside each point.", RX2, y, RW2, "sm") - 4
para(c, "Options are every entrance found in public sources. Your visit decides which one gets used; this page only shows what's there.", RX2, y, RW2, "sm")
footer(c, 2); c.showPage()

# ======================= PAGE 3: ADVANCE CHECKLIST (one page)
header(c, 3, "Site Advance Checklist")
para(c, "The same checklist for every venue: skip any line that doesn't apply. Write what you find on the advance report (page 5).", M, TOP + 2, W - 2 * M, "b")
CW = (W - 2 * M - 24) / 3; y0 = TOP - 22
BEFORE = ["Read pages 1-2; open each entrance in Street View",
    "Read the After-Event Report from any earlier visit here",
    "<b>Call the venue ahead and book a walk-through</b> with the security manager, same weekday and arrival hour if you can",
    "<b>Send them your walk-through request list</b> so they can prepare to show you each item",
    "Ask for the floor plan and spec sheet",
    "Check the venue calendar and nearby events on the date",
    "Search for posts about the event or the principal's visit",
    "Save the nearest hospital, fire and police (page 1)"]
OUTSIDE = ["Walk the entire outside of the building, every side",
    "Walk the surrounding blocks so you know what's around the area",
    "Stand at every entrance option (page 2); note what you see",
    "Photograph each entrance for your advance report",
    "Find the service or loading door and who controls it",
    "Find where an ambulance pulls up if the front is packed (a loading dock?)",
    "See where public lines or crowds form, and when",
    "Note lighting, steps, glass and cameras at each door",
    "Note windows, balconies and roofs that overlook each door",
    "Can a car reach each entrance, or do bollards or pedestrian zones stop it short? Where it stops, time the walk",
    "Pick a backup car spot away from the main car; keys go to the main PPS",
    "Look at it as an attacker would: where would you wait?"]
INSIDE = ["Meet the manager: who runs the event and security; get direct numbers",
    "Who greets the principal and walks them in; guest list?",
    "What gets the principal and team through each door",
    "Guest screening (metal detectors?); where armed team members check in with venue security",
    "Which entrances are open, staffed and locked, and when",
    "Holding room: where, who has keys, who else uses it",
    "Shelter room: lockable, inside, no windows",
    "Two ways out of every room the principal uses",
    "Mark holding room, event space, restrooms and ways out on the floor plan",
    "Walk car to door to room to event and back; time each leg",
    "Elevators: can one be held or keyed off, or use the freight elevator?",
    "Pyro, strobes, loud effects; press or photo areas",
    "Evacuation plan, alarm sound, where the public gathers",
    "AED, bleeding control kit, fire extinguishers, first aid; event medical staff on shift at arrival?",
    "Check phone signal at each door and in each room",
    "Past problems at similar events; ask staff not to post"]
CLOSE = ["Fill in the advance report (page 5) before you leave", "Send the team lead the car stop, pick-up spot, timing and backup car spot",
         "Update \"How sure are we\" (page 7): move items you checked", "Make sure any copy for the venue leaves out the principal's details"]
def band(x, y, w, t, col=NAVY, h=18, size=9):
    c.setFillColor(col); c.roundRect(x, y - h, w, h, 4, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Inter-Bold", size); c.drawString(x + 8, y - h + 5.5, t.upper())
def items(x, y, w, lst, k="s", gap=4.6):
    for it in lst:
        cbox(c, x + 4, y); y = para(c, it, x + 16, y, w - 18, k) - gap
    return y
x1 = M; x2 = M + CW + 12; x3 = M + 2 * (CW + 12)
band(x1, y0, CW, "1  Before you go")
band(x2, y0, 2 * CW + 12, "2  During the advance")
SUBC = colors.HexColor("#2A3A55")
band(x2, y0 - 21, CW, "Outside", SUBC, 14, 8); band(x3, y0 - 21, CW, "Inside: meet the manager, walk through", SUBC, 14, 8)
e1 = items(x1, y0 - 26, CW, BEFORE, "b", 6)
e2 = items(x2, y0 - 42, CW, OUTSIDE, "c", 4.2)
e3 = items(x3, y0 - 42, CW, INSIDE, "c", 4.2)
y = min(e1, e2, e3) - 6
band(M, y, W - 2 * M, "3  Close out, before you leave")
y -= 26
for i, it in enumerate(CLOSE):
    x = M + (i % 2) * ((W - 2 * M) / 2); yy = y - (i // 2) * 17
    cbox(c, x + 4, yy); para(c, it, x + 16, yy, (W - 2 * M) / 2 - 20, "b")
print("checklist bottom", y - 34, "footnote at", M + 22)
para(c, "Checklist paraphrased from <i>Introduction to Executive Protection</i> (ch. 3), the EPI course manual <i>Providing Executive Protection</i> (2020, ch. 4-5) and the course modules.", M, M + 22, W - 2 * M, "sm")
footer(c, 3); c.showPage()

# ======================= PAGE 4: ENTRANCES UP CLOSE
header(c, 4, f"{SHORT}: Entrances Up Close")
para(c, "Each entrance found: a close-up from the overhead image (the corner map shows where it sits). Scan the QR code or tap the link to see it at street level in Google Street View.", M, TOP + 2, W - 2 * M, "s")
cells = [tuple(x) for x in D["cells"]]
gw = (W - 2 * M - 14) / 2; gh = (TOP - 22 - (M + 20)) / 2
for i, (k, t, sk, note) in enumerate(cells):
    x = M + (i % 2) * (gw + 14); ytop = TOP - 18 - (i // 2) * (gh + 6)
    box(c, x, ytop, gw, gh - 4)
    c.setFillColor(NAVY); c.setFont("Inter-Bold", 9); c.drawString(x + 7, ytop - 14, t.upper())
    ih = gh - 30; iw2 = ih * 700 / 560; iy = ytop - 21 - ih
    c.drawImage(D.get("crop_pattern", "img/crop-{}.jpg").format(k), x + 6, iy, iw2, ih)
    rx = x + 6 + iw2 + 10; rw = gw - (iw2 + 22)
    qs = min(rw, 96); qy = ytop - 21 - qs
    c.setFillColor(colors.white); c.rect(rx - 2, qy - 2, qs + 4, qs + 4, stroke=0, fill=1)
    qr(c, sv_url(sk), rx, qy, qs)
    yy = para(c, "<b>Scan for Street View</b><br/>" + link(sk, "or tap to open"), rx, qy - 5, rw, "s")
    para(c, note, rx, yy - 6, rw, "sm")
para(c, "Overhead imagery (c) Maxar (c) Mapbox (c) OpenStreetMap. Street View may not cover pedestrian-only spots; if it opens elsewhere, drag the figure to the nearest street.", M, M + 20, W - 2 * M, "sm")
footer(c, 4); c.showPage()

# ======================= PAGE 5: ADVANCE REPORT (one page, fill in)
header(c, 5, f"{SHORT}: Advance Report")
para(c, "Fill this in during or right after your advance visit, before the event. It goes to the team lead and whoever drives. Skip any line that doesn't apply.", M, TOP + 2, W - 2 * M, "b")
y = TOP - 16
G = [("GRID", (0, 1), (-1, -1), 0.4, LINE), ("TOPPADDING", (0, 1), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 1), (-1, -1), 4.5)]
y = table(c, [["Visited (date, time)", "Advance by", "Met with (role)", "Same weekday and hour?"], ["", "", "", "Yes  /  No"]], M, y, [180, 150, 230, W - 2 * M - 560], zebra=False, styles=G)
y -= 6
y = table(c, [["Entrance", "Open when", "Staffed / locked", "Steps? Y/N", "What gets you in", "Overlooked by", "Notes (lighting, cameras, crowd, curb)"],
              ] + [[e, "", "", "", "", "", ""] for e in D["report_entrances"]] + [["S  Service / loading", "", "", "", "", "", ""], ["Other found:", "", "", "", "", "", ""]], M, y, [104, 66, 76, 48, 96, 100, W - 2 * M - 490], zebra=False, styles=G)
y -= 6
LW5 = 380; RX5 = M + LW5 + 14; RW5 = W - M - RX5
yl = table(c, [["Inside", "Where / notes"], ["Holding room", ""], ["Shelter room (locks, no windows)", ""], ["Event space", ""], ["Restrooms", ""],
               ["Two ways out of each room", ""], ["AED, bleed kit, medical staff", ""], ["Screening, armed check-in", ""], ["Elevator held / freight", ""], ["Guest list, effects, press areas", ""], ["Phone signal / Wi-Fi", ""]],
               M, y, [140, LW5 - 140], zebra=False, styles=G)
yr = table(c, [["Movement (walk it, time it)", "Door / route", "Time"], ["Car stop to door", "", ""], ["Door to holding room", "", ""],
               ["Holding room to event", "", ""], ["Event back to the car", "", ""], ["Event to backup car", "", ""]], RX5, y, [130, RW5 - 180, 50], zebra=False, styles=G)
yr -= 6
yr = table(c, [["Venue contact", "Name", "Direct number"], ["Event manager", "", ""], ["Head of security", "", ""], ["Greeter at the door", "", ""]],
           RX5, yr, [130, 120, RW5 - 250], zebra=False, styles=G)
yy = min(yl, yr) - 8
for lab in ["Car stop and pick-up spot:", "Backup car spot, keys with:", "Ambulance pull-up:", "Issues found:"]:
    c.setFillColor(INK); c.setFont("Inter-SemiBold", 8); c.drawString(M, yy - 9, lab)
    lw = pdfmetrics.stringWidth(lab, "Inter-SemiBold", 8) + 8
    c.setStrokeColor(LINE); c.line(M + lw, yy - 10, W - M, yy - 10); yy -= 16
c.setFillColor(NAVY); c.setFont("Inter-Bold", 8); c.drawString(M, yy - 9, "YOUR CALL")
xx = M + 70
for lab, col in [("GREEN", GREEN), ("AMBER", AMBER), ("RED", RED)]:
    cbox(c, xx, yy - 2); c.setFillColor(col); c.roundRect(xx + 11, yy - 12, 44, 13, 6.5, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Inter-Bold", 7); c.drawCentredString(xx + 33, yy - 8, lab); xx += 70
print("report bottom", yy - 12, "limit", M + 12)
footer(c, 5); c.showPage()

# ======================= PAGE 6: AFTER-EVENT REPORT (fill in after the event)
header(c, 6, f"{SHORT}: After-Event Report")
para(c, "Fill this in after the event. Keep it with the venue file: the next advance here starts with it. Skip any line that doesn't apply.", M, TOP + 2, W - 2 * M, "b")
y = TOP - 16
y = table(c, [["Event date", "Venue", "Team lead", "Filled in by (name, date)"], ["", "", "", ""]], M, y, [150, 220, 170, W - 2 * M - 540], zebra=False, styles=G + [("TOPPADDING", (0, 1), (-1, 1), 8), ("BOTTOMPADDING", (0, 1), (-1, 1), 8)])
y -= 8
y = table(c, [["What went to plan", "As planned?", "What changed"], ["Arrival", "Yes  /  No", ""], ["Inside the venue", "Yes  /  No", ""],
              ["Departure", "Yes  /  No", ""], ["Other", "Yes  /  No", ""]], M, y, [130, 70, W - 2 * M - 200], zebra=False, styles=G)
y -= 8
y = table(c, [["Incidents", "Time", "What happened", "Action taken", "Who was told"]] + [[str(i), "", "", "", ""] for i in range(1, 6)],
          M, y, [52, 50, 260, 210, W - 2 * M - 572], zebra=False, styles=G)
y -= 10
for title, n in [("What to improve next time", 4), ("Notes for the next visit to this venue", 3)]:
    c.setFillColor(NAVY); c.setFont("Inter-Bold", 9); c.drawString(M, y - 9, title.upper()); y -= 14
    for _ in range(n):
        c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M, y - 14, W - M, y - 14); y -= 18
    y -= 6
print("after-event bottom", y, "limit", M + 12)
footer(c, 6); c.showPage()

# ======================= PAGE 7: HOW SURE ARE WE + SOURCES
header(c, 7, f"{SHORT}: How Sure Are We")
y = TOP
bw = (W - 2 * M - 12) / 2
CK = [("Checked from public sources", GREEN, GREENPALE, D["checked"]), ("Not checked: confirm on your visit", ORANGE, AMBERPALE, D["not_checked"])]
for i, (t, col, pale, items) in enumerate(CK):
    x = M + i * (bw + 12); box(c, x, y, bw, 236, pale)
    c.setFillColor(col); c.roundRect(x + 8, y - 22, pdfmetrics.stringWidth(t.upper(), "Inter-Bold", 8) + 16, 16, 8, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Inter-Bold", 8); c.drawString(x + 16, y - 17, t.upper())
    yy = y - 34
    for it in items:
        if i == 0: c.setStrokeColor(GREEN); c.setLineWidth(1.6); c.line(x + 12, yy - 6, x + 15, yy - 9); c.line(x + 15, yy - 9, x + 20, yy - 2)
        else: c.setStrokeColor(ORANGE); c.setLineWidth(1.3); c.circle(x + 16, yy - 5, 4, stroke=1, fill=0)
        yy = para(c, it, x + 28, yy, bw - 40, "b") - 7
y -= 248
y = sec(c, M, y, "What we couldn't get")
y = para(c, D["couldnt_get"], M, y, W - 2 * M, "s") - 10
y = sec(c, M, y, "Not in this packet")
y = para(c, "This packet covers the venue only. Routes to and from it, the turn-by-turn drive to the hospital, weather and code words are planned separately.", M, y, W - 2 * M, "s") - 10
y = sec(c, M, y, "Sources")
para(c, D["sources"], M, y, W - 2 * M, "s")
footer(c, 7); c.showPage(); c.save(); print("wrote", OUT)
