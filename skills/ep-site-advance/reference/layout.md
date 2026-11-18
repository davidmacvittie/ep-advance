# Site advance PDF: layout rules

Read this file before you write the code that builds the packet. It gives every size, color and position, so each packet follows the same 7-page layout. The pictures in `reference/pages/` show the finished pages of the Kennedy Center test; look at them first and match them. All venue facts go in one `venue.json` shaped like `examples/venue-example.json`.

Write the build code yourself in Python: `pillow` for the map pictures and `reportlab` for the PDF. Draw the PDF straight onto a canvas (fixed positions, no flowing pages). Build page 1 first, look at it, then add the rest. Fix anything that does not match the pictures before you hand the PDF over.

## 1. Page frame

- **Paper:** US Letter, landscape (792 x 612 pt). Margin **M = 28 pt** on every side. Coordinates below are in points from the bottom-left corner, as reportlab uses them.
- **Header on every page:** a navy rounded rectangle (6 pt corners) from x = M to 792 - M, 42 pt tall, its top at 612 - M. In it: a white circle radius 12 at (M + 22, 612 - M - 21) with the page number in bold 11 navy centered; the page title in bold 15 white at (M + 44, 612 - M - 19); the subtitle (`sub`) in 7.6 white at (M + 44, 612 - M - 33). At the right, a pill in #2A3A55, 108 x 16 with 8 pt corners, its left at 792 - M - 118 and bottom at 612 - M - 29, with "SITE ADVANCE  |  <CODE>" in bold 7 white centered.
- Page titles: "<short>: At a Glance", "<short>: Overview Map", "Site Advance Checklist", "<short>: Entrances Up Close", "<short>: Advance Report", "<short>: After-Event Report", "<short>: How Sure Are We".
- **Footer on every page:** a navy band from x = M to 792 - M, 16 pt tall, bottom at M - 6. Left (M + 8, M - 1), bold 6.6 white: "<footer_tag>  |  SITE ADVANCE  |  <CODE>". Centered at 396 + 40: "Draft. Confirm on your visit and with current conditions before use. Team only. Do not forward." in 6.6 white. Right-aligned at 792 - M - 8: "Page n of 7" in bold 6.6.
- **Content top:** TOP = 612 - M - 56 (the first line under the header).
- PDF title "Site Advance: <short> (<CODE>)".

## 2. Fonts

Use the fonts built into reportlab: **Helvetica**, **Helvetica-Bold**, **Helvetica-Oblique**, registered as one family so `<b>` and `<i>` work inside paragraphs. Keep text plain ASCII. For the map pictures (pillow), use a bold TrueType font found on the system (for example DejaVuSans-Bold or LiberationSans-Bold under /usr/share/fonts); if none is found, use `ImageFont.load_default(size=...)`. Never ship or download a font.

## 3. Colors

Navy #0F1B2D, Ink #18202B, Slate #5A6577, Line #DDE1E7, Pale #F4F6F9, Amber #E3A33B, Amber pale #FBF1DF, Red pale #F6D9D9, Green #2F7D57, Green pale #E6F2EB, Red #B83A3A, Blue #2E5E9E, Link blue #1F5FBF, Orange #D9772B (confirm on your visit), Purple #6B4FA0, Grey #5A6577, Sub-band #2A3A55. On the map pictures the arrows are dark purple (96, 38, 128).

## 4. Text styles

| Style | Font, size / line height | Color |
|---|---|---|
| b | 9 / 11.6 | ink |
| c | 8.7 / 10.8 | ink |
| s | 8 / 10.2 | ink |
| sm | 7.4 / 9.4 | slate |
| th (table header) | bold 7.8 / 9.6 | white |

Paragraphs are drawn with their top at a given y and return the y under them, so the next item follows.

## 5. Building blocks

- **Section title:** at (x, y): a navy circle radius 7 at (x + 7, y - 6) with a white bold 8 "i" (or an icon of that radius instead, for example the sunset or warning icon), and the title in UPPER CASE, bold 10 navy, at (x + 19, y - 9.5). The next item starts 20 pt lower.
- **Table:** cells are paragraphs in style s; header row navy with style th; 4 pt side padding, 2.6 pt top and bottom; a 0.4 pt line under every row; every second row pale unless zebra is off; vertically centered. Fill-in tables use a 0.4 pt line grid and 4.5 pt top and bottom padding, no zebra.
- **Tick box:** an empty 7 x 7 pt square with a 0.7 pt slate border, its top 1 pt under the line's y.
- **Band:** a rounded rectangle (4 pt corners) 18 pt tall (14 pt for a sub-band) with its title in UPPER CASE, bold 9 white (8 for a sub-band), 8 pt in.
- **Point mark:** 12 pt across: a filled circle in the point's color (blue = link blue, navy, amber, grey) with a 0.8 pt white outline and its letter or number in white bold (font size 0.62 x 12 for one character, 0.5 x 12 for two); an orange ring (1.4 pt, radius 7.6) around it when the spot was read from the map.
- **Icons** (radius r, drawn with shapes): hospital = red circle with a white plus; police = blue circle with a white shield; fire = orange circle with a white flame; secure = green circle with a white house; car = gray (#8A94A6) circle with a white car; event = purple circle with a white ticket; warn = amber triangle with a white "!"; spot = red circle with a white bold "!"; sunset = amber circle; moon = pale blue (#C9D3E3) circle.
- **QR code:** reportlab's own QR widget, scaled to a square, and a tap link over the same square.

## 6. Map pictures (pillow)

The satellite image is `img/site.jpg`, 2000 x 1600 pixels (Mapbox static, satellite, @2x, centered on `map.center` at `map.zoom`, 17 or 18). Every pixel position in `venue.json` is on that image.

**Pixel to lat/lon:** with the center pixel (1000, 800) at `map.center`, KX = 256 x 2^zoom x 2 / 360 pixels per degree of longitude and KY = KX / cos(center latitude) pixels per degree of latitude. A pixel (x, y) is at longitude center_lon + (x - 1000) / KX and latitude center_lat - (y - 800) / KY.

**Overview (`img/overview.jpg`, quality 88)**, drawn on a transparent layer over the image, in this order:

1. Crowd zones: each polygon filled amber at 35% opacity with an amber outline.
2. Arrows: a hand-drawn look. Split each path into 8 steps per segment and nudge each step up to 2.5 px at random (seed it by the arrow's number so it is the same each run). Draw that line 16 px wide in white (80% opacity), then 9 px wide in dark purple on top, joints rounded, ending both at the arrowhead's base so nothing pokes past its tip. At the end, a filled purple arrowhead 34 px long with a white outline, opening 0.5 radians either side.
3. Points: a filled circle radius 34 in the point's color with a 5 px white outline; an orange ring (radius 43, 8 px) around it unless `ring` is false; the mark in bold 30 white centered. Then its label: bold 30 white text on a navy rounded box (8 px corners, 10 px padding, 92% opacity), placed `dx` (default 50) and `dy` (default 0) from the point, the text anchored at its left-middle.
4. Arrow labels: bold 30 purple text with a 5 px white outline, centered on `label_xy`.
5. Warnings: an amber triangle (40 px up, 44 px either side, 34 px down) with a white outline and a bold white "!".
6. Notes: the same label box, size 28, the text's left-middle at `xy`: amber box with navy text (style amber) or dark grey box with white text (style grey).
7. Scale bar: 50 m long (meters per pixel = 156543.03392 x cos(lat) / 2^zoom / 2), navy, 8 px thick with end ticks, on a white box at 86% opacity, starting at (70, 1500), with "50 m" in bold 30 navy above it.
8. North arrow: a white circle radius 50 at (120, 120) with a navy arrow shape pointing up and "N" in bold 32 white under it.
9. Place labels (river, park names): bold 34 white at 78% opacity, centered.

**Close-ups (`img/crop-<key>.jpg`, quality 90):** draw the same layers without the point labels, notes, scale, north arrow and place labels, then cut each crop box (700 x 560 px). In the bottom-left corner of each close-up, 10 px in, put a locator: the whole satellite image shrunk to 230 x 184 on a white border 4 px wide, with a red (220, 40, 40) 4 px box showing where the close-up is, and the `locator_label` in bold 14 white with a 3 px navy outline at `locator_xy` (a pixel on the full 2000 x 1600 image, scaled down with it).

**Street View viewpoints:** turn each `map.viewpoints` pixel into lat/lon (6 decimals) and keep its heading. Links:
- Street View: `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=<lat>,<lon>&heading=<deg>` (leave out `&heading=` when there is none).
- Plain map: `https://www.google.com/maps/search/?api=1&query=<lat>,<lon>`.

Look at the overview before going on. Fix any mark or label that sits on the wrong spot.

## 7. Page 1: At a Glance

Left column x = M, 380 pt wide. Right column from x = M + 398 to 792 - M.

- Left: section "The venue", then `venue_rows` as a two-column table (64 pt label, no header). 10 pt gap. Section "Nearest help", then `help_rows` (84 pt label), then `help_note` in sm, 4 pt under. 8 pt gap. Section "Getting there", then `getting_there` (84 pt label).
- Right: section "Data inputs required", `inputs` as a table (96 pt label), then the line "That's all the user gave. Everything else in this packet was pulled from public sources." in sm. 10 pt gap. Section "Light" with the sunset icon: the three `light` entries side by side, each a radius 8 icon, the time in bold 9 ink and its label in 6.8 slate under it. 32 pt gap. Section "Worth knowing" with the warn icon: each line with its icon (radius 6.5) and the text in s, 5 pt apart.
- **The Clash**, across the bottom, base line at y = 98: title "THE CLASH: PUBLIC ACTIVITY VS. <CODE>" in bold 10 navy at y = 150. The time axis runs from x = M + 70 to 792 - M - 20 between `clash.start` and `clash.end`. A thin line-color tick every 30 minutes from y = 68 to 136, with the time ("6:30 PM") in 6.5 slate at y = 58. Row labels at the left in bold 7.2 slate: "Public" at y = 115 and the code name at y = 83. Public bars: 16 pt tall from y = 108, amber pale (or red pale when `color` is red), text in bold 6.8 ink 6 pt in. The visit bar: link blue, 16 pt tall from y = 76, from arrival to leaving, with the event text in bold 6.8 white. Red dots radius 4 at arrival and leaving on the visit bar; their labels in bold 6.8 red at y = 46 (arrival left-aligned 4 pt left of its dot, leaving right-aligned 30 pt past its dot but never past 792 - M).

## 8. Page 2: Overview Map

- The overview picture at x = M, 500 pt wide and 400 tall, its top at TOP. The credit line in 6.2 slate 9 pt under it.
- Right column from x = M + 514: section "Every known point", then a table with header ("", Point, Source, Link), columns 22, 118, 52 and the rest: a point mark (12 pt), the point text, its source, and a blue underlined "View" link to its Street View.
- 8 pt under the table: an orange ring (radius 5) and "Orange ring: spot read from the map. Confirm on your visit." in 7.4 ink. Then in sm: "**Purple arrows** show the ways in and out from the street. **Street View links** open Google Maps at the street outside each point." and "Options are every entrance found in public sources. Your visit decides which one gets used; this page only shows what's there."

## 9. Page 3: Site Advance Checklist

The checklist words are fixed in SKILL.md. Print them exactly; never change a line for a venue.

- The intro line in style b at the top.
- Three columns, each (792 - 2M - 24) / 3 wide with 12 pt between, starting 22 pt under TOP:
  - Column 1: navy band "1  Before you go", then the Before lines in style b, 6 pt apart.
  - Columns 2 and 3: one navy band "2  During the advance" across both, then sub-bands 21 pt lower: "Outside" over column 2 and "Inside: meet the manager, walk through" over column 3. Lines start 42 pt under the band top, in style c, 4.2 pt apart. Column 1's lines start 26 pt under its band top.
  - Each line has a tick box at its left and the text 16 pt in.
- 6 pt under the lowest column: a full-width band "3  Close out, before you leave", then its four lines in two columns, 17 pt per row, style b.
- The footnote in sm at y = M + 22: "Checklist paraphrased from *Introduction to Executive Protection* (ch. 3), the EPI course manual *Providing Executive Protection* (2020, ch. 4-5) and the course modules."
- It must stay on one page; if it would run over, tighten the line gaps, never drop a line.

## 10. Page 4: Entrances Up Close

- Intro line in s at the top: "Each entrance found: a close-up from the overhead image (the corner map shows where it sits). Scan the QR code or tap the link to see it at street level in Google Street View."
- A 2 x 2 grid of cells (one per entry in `cells`, up to four): cell width (792 - 2M - 14) / 2, height (TOP - 22 - (M + 20)) / 2, 14 pt between columns and 6 pt between rows, the first row's top 18 pt under TOP. Each cell is a pale box (5 pt corners) holding: the title in UPPER CASE bold 9 navy, 7 pt in and 14 pt down; the close-up picture 6 pt in and 21 pt down, as tall as the cell less 30 pt and 700/560 as wide; to its right (10 pt gap) a white-backed QR code as wide as the space left, at most 96 pt, opening that entrance's Street View; under it "**Scan for Street View**" and a blue underlined "or tap to open" link in s; then the note in sm.
- Credit in sm with its top at y = M + 20, just under the bottom row of cells: "Overhead imagery (c) Maxar (c) Mapbox (c) OpenStreetMap. Street View may not cover pedestrian-only spots; if it opens elsewhere, drag the figure to the nearest street."

## 11. Page 5: Advance Report (fill in)

All tables here are fill-in tables (grid, no zebra), full width unless noted, 6 pt apart.

- Intro in b (words in SKILL.md).
- Visit table: Visited (date, time) 180 / Advance by 150 / Met with (role) 230 / Same weekday and hour? (the rest), one empty row with "Yes  /  No" in the last cell.
- Entrance table: Entrance 104 / Open when 66 / Staffed / locked 76 / Steps? Y/N 48 / What gets you in 96 / Overlooked by 100 / Notes (lighting, cameras, crowd, curb) (the rest). One row per `report_entrances` entry, then "S  Service / loading" and "Other found:".
- Below, left (380 pt wide): Inside / Where / notes (140 pt label): Holding room; Shelter room (locks, no windows); Event space; Restrooms; Two ways out of each room; AED, bleed kit, medical staff; Screening, armed check-in; Elevator held / freight; Guest list, effects, press areas; Phone signal / Wi-Fi.
- Right (from 14 pt past the left table): Movement (walk it, time it) 130 / Door / route / Time 50: Car stop to door; Door to holding room; Holding room to event; Event back to the car; Event to backup car. Then 6 pt lower: Venue contact 130 / Name 120 / Direct number: Event manager; Head of security; Greeter at the door.
- 8 pt under the lower of the two: four write-in lines, 16 pt apart, each a label in bold 8 ink followed by a line to the right margin: "Car stop and pick-up spot:", "Backup car spot, keys with:", "Ambulance pull-up:", "Issues found:".
- Then "YOUR CALL" in bold 8 navy and three tick boxes, 70 pt apart, each beside a 44 x 13 pill: GREEN, AMBER, RED (white bold 7 text).
- It must stay on one page.

## 12. Page 6: After-Event Report (fill in)

- Intro in b (words in SKILL.md).
- Table: Event date 150 / Venue 220 / Team lead 170 / Filled in by (name, date), one row 8 pt padded.
- 8 pt lower: What went to plan 130 / As planned? 70 / What changed: Arrival, Inside the venue, Departure, Other, each with "Yes  /  No".
- 8 pt lower: Incidents 52 / Time 50 / What happened 260 / Action taken 210 / Who was told, rows 1 to 5.
- 10 pt lower: "WHAT TO IMPROVE NEXT TIME" in bold 9 navy with 4 ruled lines, 18 pt apart; then "NOTES FOR THE NEXT VISIT TO THIS VENUE" with 3.

## 13. Page 7: How Sure Are We

- Two boxes side by side at the top, each (792 - 2M - 12) / 2 wide and 236 tall, 5 pt corners: left green pale with a green pill "CHECKED FROM PUBLIC SOURCES", right amber pale with an orange pill "NOT CHECKED: CONFIRM ON YOUR VISIT" (pills 16 pt tall, bold 8 white). Each pill sits 8 pt in from the box's left and 6 pt down from its top. Items start 34 pt under the box top, in style b, 7 pt apart, text 28 pt in: a green tick (1.6 pt line from 12 to 15 to 20 pt in) before each checked item, an orange ring (radius 4, 1.3 pt, centered 16 pt in) before each item not checked.
- 248 pt under TOP: section "What we couldn't get" with `couldnt_get`; section "Not in this packet" with "This packet covers the venue only. Routes to and from it, the turn-by-turn drive to the hospital, weather and code words are planned separately."; section "Sources" with `sources`. 10 pt between sections.

## 14. Checks before you hand it over

- Exactly 7 pages. Nothing runs past the footer band on any page: if it would, shorten the venue text (never the fixed checklist or report lines).
- Render every page to a picture and look at it. Every QR code opens the right Street View point.
- File name "site-advance-<venue>-<YYYY-MM-DD>.pdf" unless the user names one.
