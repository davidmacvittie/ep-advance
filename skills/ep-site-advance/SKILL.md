---
name: ep-site-advance
description: "Builds an executive protection site advance for one venue (event space, restaurant or hotel) for a 1-3 person team, in the same fixed 7-page format every time. Stands alone (no route advance needed) and gives the advance person information and a path: every public entrance shown as option 1, 2, 3 on an overview map, nearest help, a one-page advance checklist, entrance close-ups with a Street View QR code for each, an advance report to fill in, and what is and isn't confirmed. Use when someone asks for a site advance, venue advance, venue survey or \"advance the venue\" for a principal's visit."
---

# EP Site Advance

Version 0.12 (draft for review)

The packet gives the advance person information and a path to follow; they make the calls after visiting. It stands alone: the user needs no route advance or drive team to use it. This skill writes the packet for the person who advances the venue and greets the principal there.

Audience: 1-3 person teams protecting medium-threat executives or public figures in the US. Keep it simple: the packet pulls public information to help the person who advances the venue and greets the principal there, and the same checklist works for any venue with no per-client changes. The team skips any checklist line that doesn't apply. Keep only what prevents a real mistake. Icons and maps over text. Same pages, same order, same words every time.

## Rules
- Use only Claude's own tools: web search and fetch, the map connectors the user has (Mapbox, TomTom), and file and PDF tools. Nothing runs on the user's computer.
- Public information only. Never contact the venue, sign in anywhere, book, or fill in forms. Questions for the venue go on the checklist for the team to ask.
- Use a code name for the principal (default ATLAS, or the one the user gives). Never put the principal's real name, home address or phone in the packet.
- Mark every item seen only on a map, or guessed, as "confirm on recon" (orange on the map and in tables). Say where each fact came from in a few words.
- Never ask for or depend on a route advance. Routes, the turn-by-turn hospital drive and weather are out of scope; say so in one line on page 7.
- Show entrances as options 1, 2, 3 and on, for however many are found in public sources, plus S for a service side if seen. Options are what's there, never a chosen door.
- Paraphrase books and training material and credit the book by title. Never copy passages. Never use names, clients or details from anyone's private or company material.
- Any time from a page goes in as the source shows it; work out sunset with a standard formula and say so.
- End with: "Draft. Confirm on your visit and with current conditions before use."

## Inputs
The user gives three things; the skill pulls everything else itself (maps, entrances, nearest help, events, light, checklist):
1. Location: venue name or address.
2. Event date and time.
3. When the client arrives.

If any of the three is missing, ask for it in one short message. Never ask for anything else. Use these only if the user offers them; otherwise skip them: departure time (default: event end, or "not given"), code name (default ATLAS), what the client is doing there, team size. Work out the venue type yourself. List any defaults used on page 1.

## Research (do in this order)
0. **Is the venue open on the date?** Search the venue name with "closed", "closure", "renovation" and "reopening", and read the newest news. If it's closed, under renovation or the event may not happen, make that the first line of "Worth knowing" and the first "Status" row on page 1 (red), put "That the venue is open and the event is on" first under Not checked on page 7, and say it first in chat. Keep going and build the rest of the packet.
1. Venue's own site: entrances, accessibility page (step-free doors often reveal side entrances), FAQ (bag policy, lines, re-entry, coat check), rentals or private events page (rooms, capacity), parking. **If the venue's pages won't load:** read the entrances from the satellite image instead, name each by where it is (for example "plaza entrance, north door"), never a name you guessed, mark every one orange, write "Imagery only" as its source, and say on page 7 which pages failed.
2. Events at the venue and nearby on the date (venue calendar, ticket sites). Note doors and show times: public lines and crowd timing usually matter most. **If no calendar for the date can be read:** say so in "Worth knowing" and on the Clash public bar ("No event calendar found for <date>. Ask the venue what else is on."), and add "What else is on that night" to Not checked on page 7. Never write "no events" when you only couldn't find the calendar.
3. Satellite image of the block (Mapbox static image, about zoom 18). Find doors, curb lanes, alleys, loading areas, water or dead ends.
4. Nearest help: look up the nearest Level I or II trauma center, the fire station and the police station that cover the venue, with drive times (Mapbox, typical traffic; say when read). **If the nearest city police station is more than about 10 minutes away**, or the grounds belong to a federal, state or park agency, a campus or a port, also list who polices the grounds (for example U.S. Park Police, campus police) and the venue's own security, and add "Who responds: venue security or police" to Not checked on page 7.
5. Light: sunset and full dark for the date.
6. Social leak check: search the venue and event names, and the principal's name with the venue, for public posts that announce the visit.

## The packet (fixed format, landscape letter, 7 pages)
The packet gives information and a path to follow. It does not pick the principal's door or tell the team how to run the visit: the advance person decides that after going in person. Header on every page: "<Venue>: <Page name>", subtitle with address, date, arrival and departure times, "Orange = check on your visit". Tag "SITE ADVANCE | <CODE NAME>". Footer: sample or classification line, the draft line, "Team only. Do not forward.", page x of 7.

1. **At a glance**: a "Data inputs required" box listing the three things the user gave (site location, event date and time, principal's ETA), with the line "That's all the user gave. Everything else in this packet was pulled from public sources."; venue facts table (type and capacity, every public entrance, box office, public rules such as bag search and re-entry, what's known inside, parking); nearest help (hospital with trauma level, fire and EMS, police, each with drive time and the date read); getting there (car stop: pick on the visit; backup car: optional, away from the main car, keys with the main PPS); light (sunset, full dark, arrival); "Worth knowing" lines with icons, stated as facts; **The Clash** timeline of public activity vs. the visit on one time axis.
2. **Overview map**: satellite image, north up, 50 m scale. Label every public entrance found as an option (1, 2, 3...), the service or loading side if seen (S, marked unknown), garage entrances (G) and any public line or crowd zone. Draw hand-drawn style purple arrows with short labels for the ways in from the street (for example "walk in from District Sq, ~60 m", "in from Maine Ave"). Arrows show what's there, not a chosen door. Orange ring = spot read from the map. Side table: every point, its source, and a Street View link.
3. **Site advance checklist (one page; may run to two if it ever needs to stay readable)**: the fixed checklist below, word for word, the same for every venue. Never add, drop or reword a line for the venue; the user skips what doesn't apply. Page title "Site Advance Checklist". Layout: 1 Before you go; 2 During the advance, with two sub-columns, Outside and Inside: meet the manager, walk through; 3 Close out, before you leave. Venue facts belong on the other pages.
4. **Entrances up close**: one cell per entrance option (up to four; add the service side if there's room), each with a close-up cropped from the overhead image with the same arrows and a small locator map in the corner (the whole overhead image with a red box on the close-up area), a large QR code (about 1.3 in) that opens Street View at that entrance, a tap-to-open link under it, and a short factual note. No photo boxes: the packet is a one-time pull of public information that users print or read, not edit.
5. **Advance report (fill in, one page)**: filled in during or right after the advance visit, before the event. Intro: "Fill this in during or right after your advance visit, before the event. It goes to the team lead and whoever drives. Skip any line that doesn't apply." Visit details; entrance table (open when, staffed or locked, "Steps? Y/N" (Y means the entrance has steps), what gets you in, overlooked by, notes); inside table (holding room, shelter room, event space, restrooms, two ways out of each room, AED, bleeding control kit and medical staff, guest screening and armed check-in, elevator held or freight, guest list, effects and press areas, phone signal); movement table (car stop to door, door to holding room, holding room to event, event back to the car, event to backup car: door or route, time); venue contacts (event manager, head of security, greeter); lines for the car stop and pick-up spot, the backup car spot and who holds the keys, the ambulance pull-up point, and issues; the advance person's own green / amber / red call.
6. **After-event report (fill in after the event, one page)**: intro "Fill this in after the event. Keep it with the venue file: the next advance here starts with it. Skip any line that doesn't apply." Event date, venue, team lead, filled in by; what went to plan (arrival, inside the venue, departure, other: as planned yes or no, what changed); incidents (up to 5: time, what happened, action taken, who was told); lines for what to improve next time and notes for the next visit to this venue.
7. **How sure are we**: "Checked from public sources" vs. "Not checked: confirm on your visit"; what we couldn't get; a one-line "Not in this packet" (routes, hospital drive, weather, code words); sources with the date read.

## Fixed checklist (page 3, print exactly)
Intro line: "The same checklist for every venue: skip any line that doesn't apply. Write what you find on the advance report (page 5)."

**1 Before you go**
- Read pages 1-2; open each entrance in Street View
- Read the After-Event Report from any earlier visit here
- **Call the venue ahead and book a walk-through** with the security manager, same weekday and arrival hour if you can
- **Send them your walk-through request list** so they can prepare to show you each item
- Ask for the floor plan and spec sheet
- Check the venue calendar and nearby events on the date
- Search for posts about the event or the principal's visit
- Save the nearest hospital, fire and police (page 1)

**2 During the advance**

*Outside*
- Walk the entire outside of the building, every side
- Walk the surrounding blocks so you know what's around the area
- Stand at every entrance option (page 2); note what you see
- Photograph each entrance for your advance report
- Find the service or loading door and who controls it
- Find where an ambulance pulls up if the front is packed (a loading dock?)
- See where public lines or crowds form, and when
- Note lighting, steps, glass and cameras at each door
- Note windows, balconies and roofs that overlook each door
- Can a car reach each entrance, or do bollards or pedestrian zones stop it short? Where it stops, time the walk
- Pick a backup car spot away from the main car; keys go to the main PPS
- Look at it as an attacker would: where would you wait?

*Inside: meet the manager, walk through*
- Meet the manager: who runs the event and security; get direct numbers
- Who greets the principal and walks them in; guest list?
- What gets the principal and team through each door
- Guest screening (metal detectors?); where armed team members check in with venue security
- Which entrances are open, staffed and locked, and when
- Holding room: where, who has keys, who else uses it
- Shelter room: lockable, inside, no windows
- Two ways out of every room the principal uses
- Mark holding room, event space, restrooms and ways out on the floor plan
- Walk car to door to room to event and back; time each leg
- Elevators: can one be held or keyed off, or use the freight elevator?
- Pyro, strobes, loud effects; press or photo areas
- Evacuation plan, alarm sound, where the public gathers
- AED, bleeding control kit, fire extinguishers, first aid; event medical staff on shift at arrival?
- Check phone signal at each door and in each room
- Past problems at similar events; ask staff not to post

**3 Close out, before you leave**
- Fill in the advance report (page 5) before you leave
- Send the team lead the car stop, pick-up spot, timing and backup car spot
- Update "How sure are we" (page 7): move items you checked
- Make sure any copy for the venue leaves out the principal's details

Footnote: "Checklist paraphrased from *Introduction to Executive Protection* (ch. 3), the EPI course manual *Providing Executive Protection* (2020, ch. 4-5) and the course modules."

Not in this packet: comms plans and code words (each team uses its own), emergency drills, routes and hospital drives.

## Street View
Google's geo guidelines don't allow Street View pictures in print, so never put Street View images in the PDF. Each entrance gets a Google Maps link (allowed in print, including as a QR code) that opens Street View at the street outside it:
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=LAT,LON&heading=DEG
Pick the viewpoint on the street in front of the entrance and the heading toward it. For a point with no useful heading, use a plain map link: https://www.google.com/maps/search/?api=1&query=LAT,LON

## Visual standards
Navy header band, Inter font, palette: navy #0F1B2D, amber #E3A33B, green #2F7D57, red #B83A3A, blue #1F5FBF, orange #D9772B for "confirm on recon". Icons: red cross hospital, blue shield police, orange flame fire, green house secure or door, amber triangle warning, grey car. Keep each page to one screen; no page runs over.

## How to build it (scripts in this skill's scripts/ folder)
The same two scripts build every venue; never write new layout code. All venue facts go in one venue.json; copy scripts/venue-example.json (the Kennedy Center test) and replace every value.
1. Make a work folder with an img/ subfolder. Save the Mapbox satellite image as img/site.jpg: 2000x1600 at @2x, centered on the venue, zoom 17 (18 for a small site). Put the same center and zoom in venue.json under "map".
2. Look at the image and fill in "map": entrance points (pixel x, y on the 2000x1600 image), arrows, crowd zones, notes, four 700x560 crop boxes, and a Street View viewpoint on the street outside each point with the heading toward it.
3. Run `python3 scripts/make_map.py <folder>/venue.json`. It writes img/overview.jpg, the crops and img/viewpoints.json. Look at the overview and fix any label that sits on the wrong spot before going on.
4. Fill in the rest of venue.json (page 1 rows, help, light, worth knowing, the Clash, points table, entrance cells, report entrance rows, checked and not checked, sources) and run `python3 scripts/build_pdf.py <folder>/venue.json`. The checklist and both reports are built in; never change them per venue. It prints how close each page comes to its bottom margin; if any is below its limit, shorten text.
5. Render every page to an image and look at each one before sending.

## Output
- One PDF, file name "site-advance-<venue>-<date>.pdf" (lower case, hyphens, date as YYYY-MM-DD, for example site-advance-kennedy-center-2026-12-12.pdf), unless the user names the file.
- In chat: the one or two facts that matter most (for example a public line at the main entrance at arrival time) and the top three things to confirm on the visit.
