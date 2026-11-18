# Route advance PDF: layout rules

Read this file before you write the code that builds the packet. It gives every size, color and position, so each packet looks the same. The pictures in `reference/pages/` show the finished pages of the DC sample; look at them first and match them. The trip data comes from one JSON file shaped like `examples/dc-atlas.json` (fields in `schema.md`).

Write the build code yourself, in Python with the `reportlab` library (and `pillow` to read image sizes). Build in this order and look at each page as you go: page frame, page 1, cover, trip map, one leg map page, one strip page, then the rest. Fix anything that does not match the pictures before you hand the PDF over.

## 1. Page frame

- **Paper:** US Letter. Portrait for every page except strip pages, which are landscape.
- **Margins:** 0.65 in on every side (portrait). Landscape strip pages: content box starts 0.65 in from left, 0.6 in from bottom, and is (page width - 1.3 in) by (page height - 1.2 in), with no inner padding. Content width on portrait pages is called **W** below (8.5 in - 1.3 in = 7.2 in).
- **Header bar on every page:** a navy band across the full page width, 0.42 in tall, at the very top. In it, at 0.65 in from the left and 0.27 in down from the top edge: `ROUTE ADVANCE  |  <code name>  |  <date label>` in bold 9 pt white (two spaces either side of each bar). If `meta.header_tag` is not empty, draw it right-aligned at 0.65 in from the right edge, same baseline, bold 8 pt amber.
- **Footer on every page:** 0.4 in up from the bottom edge. Left: the footer text ("Draft plan. Confirm by recon and current conditions before use.  Drive team only. Do not forward.") in 7.5 pt slate. Right-aligned at the right margin: "Page n".
- PDF title "Route advance - <code name>".

## 2. Fonts

Use the fonts built into reportlab, so no font files are needed: **Helvetica** for regular text, **Helvetica-Bold** for bold, semibold and extra-bold, **Helvetica-Oblique** for italic. Register them as one family so `<b>` inside a paragraph turns bold. Keep all text plain ASCII (straight quotes, no arrows or symbols); the built-in fonts have no other characters.

## 3. Colors

| Name | Hex | Used for |
|---|---|---|
| Navy | #0F1B2D | header bar, H1 and H2 text, table headers |
| Ink | #18202B | body text, the strip line, weather card background |
| Slate | #5A6577 | small notes, captions, footer |
| Line | #DDE1E7 | rules and table lines |
| Pale | #F4F6F9 | panel backgrounds, zebra rows |
| Amber | #E3A33B | kickers, alternate route, warn icon, amber pill |
| Amber pale | #FBF1DF | end note box |
| Green | #2F7D57 | green pill, secure-lobby icon |
| Red | #B83A3A | spots, trauma icon, hospital run heads |
| Blue | #2E5E9E | primary route, police icon, primary strip title |
| Orange | #D9772B | alternate strip title, fire icon |
| Teal | #178A86 | alternate 2 route and its strip title |
| Left blue | #1F5FBF | left turns on the strip |
| Right green | #2E8540 | right turns on the strip |
| Event purple | #6B4FA0 | event icon |
| Car gray | #8A94A6 | car icon |

Verdict text colors inside sentences: GREEN #2F7D57, AMBER #B7791F.

## 4. Text styles

| Style | Font, size / line height | Color | Notes |
|---|---|---|---|
| Kicker | bold 8.5 / 11 | amber | small caps-style label above each title, 2 pt after |
| H1 | bold 20 / 24 | navy | 4 pt after |
| H2 | bold 11.5 / 14 | navy | 6 pt before, 3 pt after |
| Body | 9 / 12.2 | ink | |
| Body small | 8 / 10.5 | ink | most panel text |
| Note | 7.5 / 9.8 | slate | captions and notes |
| Table header | bold 8 / 10 | white on navy | |
| Panel title | bold 11 / 13.5 | navy | 5 pt after |

## 5. Building blocks

- **Panel:** a block with a pale background and 6 pt rounded corners, padding 9 pt left, right and bottom and 7 pt on top, a panel title, then its content. Panels on one page are separated by 11 pt of clear space (14 pt on the checklist page, 18 pt on the medical page). Numbered panels have titles like "1.  Recon drive" (two spaces after the period).
- **Two columns:** two blocks side by side with an 18 pt gap (11 pt where two panels sit side by side).
- **Key-value list:** label in bold 8 pt, value in 8 pt, top-aligned, a 0.3 pt line rule under each row except the last.
- **Data table:** navy header row with white bold 8 pt text, rows in 8 pt with a 0.4 pt line under each, every second row pale, 5 pt side padding, 3.5 pt top and bottom.
- **Image:** scaled to the given width, keeping its shape. If the file is missing, draw instead a pale box with a thin line border, the given width wide and half as tall, with "Image not available: <path>" centered in note style. Never fail the build over a missing image.
- **Map legend row:** one row across the width with equal columns, each an 18 pt swatch cell (a 14 by 5 pt color bar, or a 9 pt red spot) and its label in note style.
- **Icon row:** a 11 pt icon, a 6 pt gap, then the text, top-aligned.
- **Tick box line:** an empty 9 by 9 pt square with a 0.8 pt ink border, then the text in 8.8 / 11.4.
- **End note box:** amber pale background with a 3 pt amber bar down its left edge, text in body small.

## 6. Drawn symbols

All are drawn with shapes, no images. Sizes are radii unless said otherwise.

- **Spot:** red filled circle with a 1.2 pt white outline and the white bold number centered (font size 1.15 x radius). Default radius 6.5.
- **Checkpoint (CP):** white circle with a 1 pt ink outline, "CP" in bold ink centered (font size 0.75 x radius).
- **Stop badge:** filled circle in the badge color with white bold text (font size 1.05 x radius). Default diameter 15. Color follows the stop's verdict (green or amber) unless `badge_color` is given; navy if no verdict.
- **Verdict pill:** rounded rectangle (fully round ends) in green, amber or red, the level word in bold 7 pt centered: white on green or red, ink on amber. Sizes: 46 x 13 on page 1, 52 x 15 for the cover's overall, 42 x 12 on the cover timeline, 56 x 15 on a leg page.
- **Icons**, each a filled circle with a white mark: trauma = red circle with a white plus; police = blue circle with a white shield; fire = orange circle with a white flame; secure lobby = green circle with a white house; event = purple circle with a white ticket (a small rectangle with a thin purple stripe); car = gray circle with a white car body; rally = navy circle with a white bold "R"; warning = an amber triangle (no circle) with a white bold "!".

## 7. Page order and numbering

1. How to read this plan
2. Cover
3. Trip map
4. Leg 1 map page, then one landscape strip page per route of leg 1 (primary, alternate, alternate 2)
5. The same for each later leg
6. Medical and safe havens
7. Checklist before the move
8. Recon log
9. After-move note

Work out every page number before building (leg n's map page, its strip pages, the checklist page), because page 1 and the leg pages quote them. After the build, count the pages. If the count is not what you worked out, a page ran over: shorten that page's text and build again.

## 8. Page 1: How to read this plan

Kicker "START HERE", H1 "How to read this plan", then one body-small line: "A quick outline of the public information a small drive team needs for this move. It does not replace the advance drive: the team drives the routes, checks them and decides. Work through the checklist on page N before the move." Then five panels, 11 pt apart:

1. **"1.  Information needed to build this plan"**: two columns. Left: "Required" in bold 8 pt, then a key-value list (Locations: Start, each stop in order, and the end. / Date: The day of the move. / Departure time: When the principal leaves the start.). Right: "Optional, with the default if left blank", then a key-value list (Principal code name: ATLAS (never the real name). / Number of cars: 1. / Routes per leg: 3. Or 2 if you ask. / Greeter at the event site: None. / Time at each stop: 1 hour. / Risk level: Medium. For reviewers only.). Key-value text here is 8 / 10.4.
2. **"2.  Symbols"**: a grid of 3 columns, filled top to bottom, each cell a symbol then "<b>Label:</b> meaning": Blue line: primary route. / Amber line: alternate route (teal: second alternate). / Red number: predictable spot. / CP1 to CP3: checkpoint calls. / Numbered circle: a stop. / Red cross: trauma center. / Blue shield: police. / Orange flame: fire station. / Green house: secure lobby. / Amber triangle: watch-out. / Purple ticket: event or crowd. / a navy "D" badge with "On stop photos: D car stops, B backup, R rally." Line symbols are 16 x 4 pt bars.
3. **"3.  Key terms"**: two columns of key-value rows, or `terms` from the JSON if given. Defaults: Leg: One drive from one place to the next. / Primary / alternates: The planned route, and two more on different roads. / Predictable spot: A place we must pass at a known time, like a curb. / Choke point: No way out, like a tunnel or one-way block. / If blocked, go: Where to go if a spot is blocked. Decided now. / Backup point: A second curb if the planned one is blocked. / Rally point: Where everyone meets if separated or comms fail. / Safe haven: Police, fire, hospital or a staffed lobby nearby. / Recon to confirm: Not visible on a map. Check it on the drive. / Hand-off: Drive team owns route and curb; site advance owns past the door.
4. and 5. side by side, each half the width:
   - **"4.  How to read a strip map"**: a small worked example drawn 86 pt tall (a thick ink line with an arrowhead at the right, a START dot, a blue left turn above the line labeled "Left turn", a CP labeled "CP2: call in", a green right turn below labeled "Right turn", a red spot 2 labeled "Spot 2" with "tunnel, no turnaround" under a tick, and miles 0.1, 0.5, 0.2, 0.4 on the line), then: "Drive left to right. **Above the line = left turn.** (left blue) **Below the line = right turn.** (right green) A tick on the line is a straight-on event like a tunnel or merge. Numbers on the line are miles between turns. Not to scale. **QR codes** say what they open. Each strip page's route code opens that route in Google Maps; the app may reroute in traffic."
   - **"5.  Verdicts"**: three rows, each a pill and a line: GREEN "**Go as planned.** Nothing public found that should change the plan." AMBER "**Go, with the notes.** Something public could slow or crowd you: an event, a closure, one way in, a tight closing time, weather." RED "**The team's call only.** After the advance drive, the team marks a leg or stop red if it should not be driven as written. This plan never sets red." Then a note: "Every leg and stop gets green or amber with its reason, from public data. The worst one sets the overall verdict."

The whole page must fit on one page.

## 9. Page 2: Cover

Kicker "DRIVE TEAM PACKET", H1 from `cover.title`, the intro line in note style, then:

- **"General info"** panel, full width: two columns of key-value rows (Principal: "<code> (code name)", Date, Departs, Cars ("1 (default)" if empty), Routes per leg ("3 (default)"), Greeter at the event site ("None given"), Risk level: "<risk>. For reviewers; the plan is the same at any level."), then a 6 pt gap and the stops as a key-value list (label column 14% wide).
- Below it, two panels side by side, the left one 56% of W:
  - **"Time and verdicts"**: the overall pill (52 x 15) with "**Overall.** <why>" in 8.6 / 11; 8 pt gap; the timeline as a table with columns 24 pt, 62 pt, the rest, 48 pt. A stop row: badge, time, name and fact (8.6 / 11), pill (42 x 12), with a pale background behind all but the badge. A drive row: car icon (13 pt), the drive time in 8 / 10 slate spanning the middle two columns, pill if any. Then `drive_times_note` in note style.
  - **"Weather and watch-outs"**: the weather card the full inner width, 8 pt gap, then each watch-out as an icon row (8 / 10.4).
- **Weather card:** ink background, 8 pt rounded corners. Height 112 pt plus the wrapped lines. From the top: the source in 8 pt white at 18 pt down, 14 pt in; a thin #3A4556 rule at 27 pt down. The day in bold 13 white at 52 pt down; the date in 8 pt #AAB3C2 under it. A moon icon (a #E8EDF5 circle radius 13 cut by an ink circle radius 11, offset up-right, with two small dots) centered 66 pt in. The high in bold 28 white at 96 pt in, and the low after it in 16 pt #8A94A6. The tag under the high in bold 6.3 amber (shrink to fit). At 92 pt down: a small amber sunset dot with "Sunset <time>" and, 112 pt in, a pale moon dot with "Dark <time>", 8 pt white. A rule at 102 pt down. Then each line in 7.6 / 9.6, wrapped to the card: "note" white, "muted" #AAB3C2, "impact" amber, 4 pt between lines.

## 10. Page 3: Trip map

Kicker "TRIP MAP", H1 from `trip_map.title`, the trip map image at 86% of W, a legend row, the caption in note style, 6 pt gap. Then:

- H2 "Place codes: a pin and a Street View for each place". One column pair per place (the start, then the end of each leg, skipping a place within about 150 m of one already listed). Over each pair, centered: "**Name** (start and end)" or "(stop 1)", "(end)". Under it two QR boxes: **Location** ("pin, not directions") and **Street View** ("the curb"). A thin line separates places. QR size is the smaller of 66 pt and the column width less 16.
- A note: "Each route's code, which loads the whole route into Google Maps, is on its strip page."
- H2 "Events that touch the route", then up to three `events.key` lines as icon rows with the event icon, then `events.note` in note style.

**QR box:** the code centered, its label under it in bold 8.5 navy, the sub-label under that in 7.2 slate. Every QR code is also a tap link in the PDF over the same square. Use reportlab's own QR widget (error level L).

**Link formats:**
- Location: `https://www.google.com/maps/search/?api=1&query=<lat>,<lon>` (5 decimals).
- Street View: `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=<lat>,<lon>&heading=<whole degrees>&pitch=0`.
- Route: `https://www.google.com/maps/dir/?api=1&origin=<lat>,<lon>&destination=<lat>,<lon>&travelmode=driving&waypoints=<lat>,<lon>%7C<lat>,<lon>` (origin and destination are the first and last points of the route's line).

**Street View point for a drop-off:** walk back from the end of the leg's primary line while the street keeps its direction (within 25 degrees) to find the last straight stretch. Put the point on the line, set back from the end by 40% of that stretch, at least 12 m and at most 30 m. Heading: from that point toward `dropoff_view.look_at`; with no `look_at`, face the right-hand curb (the left one if the arrive text says "on the left"). `dropoff_view.pt` and `heading` override by hand. For the start of a one-way trip, use the first point of leg 1's line, facing right of its first direction.

## 11. Leg map page (portrait, one per leg)

- Kicker: `LEG n  |  DEPART <time>  |  TURN BY TURN ON PAGES 5, 6 AND 7`.
- H1: the leg title.
- The verdict line: pill (56 x 15) and the reason in 9 / 11.5.
- The leg map image at 74% of W, a legend row (Primary blue, Alternate amber, Alternate 2 teal if there is one, Predictable spot, Trauma center navy), then one line: "**Primary** 1.2 mi, 6 min.  **Alternate** ...".
- Bottom row: the drop-off stop's overhead image at 62% of W with "**Drop-off:** <name>" above it in bold 9 navy and its `points` line under it in note style. Beside it a narrow column: "**QR codes**", "Pin and Street View for each place: page 3.", "Route codes for this leg: pages 5, 6 and 7, with the turns, spots, closures and where to go if blocked." If two overheads share the page (the start of a one-way trip goes on leg 1), put them side by side and the QR note under them.
- No tables and no QR codes on this page.
- If the leg has alternate 2 but `map_routes` is under 3, warn the user that the map image does not show the third route.

## 12. Strip page (landscape, one per route)

Accent color: blue for primary, orange for alternate, teal for alternate 2. Coordinates below are from the top-left of the content box; w is its width.

- **Title** at 16 pt down: "Primary Route  |  Leg 1 of 3: Willard > The Anthem" in bold 17 in the accent color (shrink to as small as 11 to fit). Right-aligned at 15 pt down: "Linear view of the leg 1 map on page 4" in bold 9 slate.
- **Subtitle** at 30 pt down, 8.5 slate, shrunk (not below 6.5) to fit the width left of the route QR code (w - 76): "Depart 5:30 PM, arrive 5:36 PM.  1.2 mi / about 6 min (Mapbox, typical traffic for that time).  Not to scale; miles between turns on the line.  <source>".
- **Legend box** with its bottom at 72 pt down, 32 pt tall, pale with a line border and 5 pt corners, only as wide as its three columns: column 1 "ABOVE THE LINE = LEFT TURN" (bold 8, left blue) over "BELOW THE LINE = RIGHT TURN" (bold 8, right green); column 2 a small CP with "Checkpoint (call it in)" over a small cross-tick with "Straight-on event (tunnel, merge)"; column 3 a red spot with "Predictable spot:" over "if blocked, see notes" (bold 8 red).
- **Route QR code**, 66 pt square, at the top right (right edge at w, top 8 pt above the legend box top). To its left, right-aligned and wrapped: "Route: primary, opens in Google Maps" in bold 8.6 accent, then "Scan or tap. Follows this route through 3 points on it. The app may reroute in traffic." in 7.2 slate.
- **The strip** at 190 pt down: a 3.2 pt ink line from x = 34 to x = w - 40, with a filled arrowhead 12 pt long at the right end. Space the events evenly from x = 34 to w - 70 (first at the start, last at the end).
  - Miles between each pair of events in bold 8 ink, centered over the gap, 5 pt above the line ("0.25" style under 0.1 mi, "0.3" style otherwise).
  - START (first event): an ink dot of radius 7, "START" in bold 7.5 above it, the label in bold 8 under it at 20 pt and the sub in 7 slate at 30 pt.
  - ARRIVE (last event): the label and the wrapped sub in bold 8 left blue, centered 6 pt right of the line's end, starting 22 pt below the line.
  - Left turn: a 1.6 pt left-blue stem up from the line, 34 pt tall, alternating with 64 pt for every second left turn; at the top a short bar to the left ending in a filled arrowhead pointing left. The label in bold 8 left blue above it (wrapped to 1.75 x the event spacing), the sub in 6.8 slate above that.
  - Right turn: the same in right green, going down, arrow pointing right, the label under the arrow.
  - Straight-on event: a 1.4 pt ink tick across the line, 16 pt tall, the label in bold 7.5 under it at 18 pt, the sub in 6.8 slate under that.
  - A CP on an event: radius 8, 13 pt left of the event, 15 pt above the line (below it for a left turn). On the start: 32 pt above the dot.
  - A red spot on an event: radius 6.5, 12 pt right of the event, 15 pt above the line (below for a left turn). On the start: 19 pt right, 32 pt up. On the arrive: above the end at 16 pt.
- **Cumulative miles** row 106 pt below the strip: "Cumulative miles:" in bold 7 slate at the left edge, 10 pt higher, and each event's mile in 7.2 slate under its x. A 0.6 pt line rule 8 pt below, the full width.
- **Step table** on the left, 60% of w wide: its heading "STEP BY STEP: LEG 1 PRIMARY" in bold 9 accent with its baseline 14 pt under the rule, and the table's top 20 pt under the rule. Columns 5%, 8%, 10%, 60%, 17%: #, Mile, Turn, Instruction, Call in. Navy header with bold 7.6 white text, rows 7.6 / 9.6 with a 0.3 pt line, 1.6 pt top and bottom padding. Turn is "LEFT" bold left blue or "RIGHT" bold right green. A spot puts "Spot n." in bold red before the instruction.
- **Notes** on the right, from 18 pt right of the table to w, with a thin vertical line 9 pt left of them from 8 pt under the rule to the bottom: heading "NOTES FOR THIS ROUTE" in bold 9 accent on the same baseline as the table heading, the first note 14 pt lower, then each note: its icon (radius 5; a spot of radius 5.5 for spots) and its head in bold 7.8 (red for spots, ink otherwise), then the body wrapped in 7.4 / 9.2 slate, 4 pt between notes.
- Everything must fit on the one landscape page. If the table or notes run long, shorten the text.

**Miles along the route:** project each event's point onto the route line (searching forward from the last event, so a route that passes the same corner twice is measured right) and take its distance from the start, measured along the line. Scale every distance so the line's total equals the routing tool's `meters`, then convert to miles. The first event is mile 0 and the last is the full distance.

**Turns from geometry,** when the routing tool gives turn text but no turn points: merge line points closer than 15 m, then walk the line; where the direction changes by 20 degrees or more, mark a turn (right if clockwise, left if counterclockwise). Join two bends of the same side within 40 m into one. Keep turns of 35 degrees or more. Match them in order to the tool's turn list.

**Route code points (up to 3):** for each left or right turn on the route, take the point 50 m past it along the line (not within 60 m of either end, and not within 80 m of another). If there are more than 3, keep the ones where this route is farthest from the leg's other routes, spread out at least 12% of the route apart, in driving order. With no turns, use the points at 25%, 50% and 75% of the way. A route's own `waypoints` in the JSON replaces these. Print each route's link so you can check it with the directions tool.

## 13. Medical and safe havens

Kicker "MEDICAL AND SAFE HAVENS", H1 "Hospital runs and help nearby", then:

1. Panel **"1.  Help nearby: hospitals, police, fire and safe places"**: a data table (header navy, rows white, no zebra) with columns Place 31%, Type 19% (with a 9 pt icon before Police, Fire, Secure venue or any type naming Trauma), one "From <stop>" column per stop sharing 30%, and Check 20%. Then `times_note` in note style.
2. Panel **"2.  <runs_title>"**: the hospital runs side by side in white boxes with 5 pt corners and 8 pt between them. Each box: the head in bold 8.6 red, the sub in note style, then the numbered steps in 7.8 / 10.2. Then `runs_note`.
3. Panel **"3.  Not in this packet"** with `kit_note`, if given.

Panels are 18 pt apart.

## 14. Checklist before the move

Kicker "RECON, DAY-OF AND COMMS", H1 "Checklist before the move", `intro_short` in note style, then numbered panels 14 pt apart, each holding a white rounded box of tick box lines (a 0.3 pt rule between lines):

1. "1.  Recon drive": one line per `recon.rows` entry: "**<where>:** <confirm>".
2. "2.  Day before and day of": `day_of`.
3. "3.  Comms": `comms_checks`.
4. "4.  How sure are we": the `confidence` lines in note style (no boxes).

No paragraphs or tables.

## 15. Recon log (form)

Kicker "FORM  |  FILL IN ON THE RECON DRIVE", H1 "Recon log: planned vs driven", a key-value list (Driven by / Date and time: "Same weekday and time of day as the move, if possible" / Vehicle). Then:

- H2 "Routes": a form table with a navy header (Leg and route 27%, Planned min 10%, Driven min 10%, Planned mi 10%, Driven mi 10%, Traffic, closures, notes 33%), at least 6 rows, prefilled from `forms.recon_routes` in slate, a 0.5 pt line grid, row height 240 / rows (24 pt at most).
- H2 "Red spots and stops": a form table (Spot or stop 30%, What we saw 45%, If blocked option driven? 25%), at least 6 rows of 26 pt, prefilled from `forms.recon_spots`.
- H2 "Day-before re-check": tick boxes in two columns: Closures and roadworks re-read / Events check re-run (page 3) / Forecast read / Rally point lobbies still open late / Changes since recon driven again / Packet updated and re-sent.

## 16. After-move note (form)

Kicker "FORM  |  FILL IN WITHIN 24 HOURS OF THE MOVE", H1 "After-move note", the note "Two minutes, while it is fresh. It starts the next advance for this principal or these places.", a key-value list (Move and date / Filled in by). Then six boxes, 6 pt apart, each a pale header row with the question in bold and an empty writing area: What went to plan (52 pt) / What changed (route, timing, curb, door) (52) / Red spots that were blocked, and what we did (52) / Times driven vs planned (40) / Anything to fix in the next packet (52) / Places to add or drop (stops, havens, rally points) (40). End with the end note box: "Draft plan. Confirm by recon and current conditions before use."

## 17. Checks before you hand it over

- Any RED verdict in the data becomes AMBER, and tell the user you changed it.
- The page count matches what you worked out (a three-leg move with 3 routes per leg is 19 pages; with 2 routes it is 16).
- Look at every page as a picture. Nothing overlaps, nothing runs off the page, every strip page fits on one page.
- Decode or read back the QR links: each route link follows its own route, and each Street View point sits on the drop-off street facing the building.
