# Dwelling Details Report upload — feasibility and design

8 September 2026. Answers "can the DEAP dwelling details report fill the survey, with no AI
and nothing leaving the machine". Yes. Proven on one real report, in the browser.

**Constraints set by the author, and they are absolute.** No AI. No third party receives
the document. The parsed values land in the existing sidebar geometry fields, which the
assessor can already edit, so no separate review screen is needed. It must be an upload.

**The sample is not committed.** It is a real client's provisional BER and contains their
name, address and MPRN. Only this note and the spike page are in the repo.

---

## What the report is

A DEAP export, 19 pages, real text rather than a scanned image — every page extracts. It is
written in labelled sections, one per building element, each a table with one row per
element and a printed total:

| Page | Section | Ends with |
|---|---|---|
| 1 | Dwelling details: County, Dwelling Type, Storeys, Year of construction | — |
| 2 | Ventilation, including ventilation heat loss | — |
| 3 | Building Elements - Floors | Total area [m²] |
| 4 | Building Elements - Roofs, typed (insulated on rafter / at ceiling) | Total area [m²] |
| 5 | Building Elements - Walls, with construction description | Total area [m²] |
| 6 | Building Elements - Doors, with count | Total area [m²] |
| 7 | Building Elements - Windows, by orientation | Total area [m²] |
| 8 | Fabric heat loss, total heat loss, and **Per m2** — the heat loss indicator | — |
| 10 | Heating System — the main space heating | — |

The heat loss indicator is labelled "Per m2" beside the fabric heat loss. Checked
arithmetically: total heat loss ÷ floor area = the printed value, to two decimals.

## What the software asks for, and where each comes from

| Survey input | Source in the report |
|---|---|
| Floor area | page 3 total |
| Wall area | page 5 total |
| Roof area | page 4 total; per-type areas available for ceiling vs rafter measures |
| Window area | page 7 total |
| Door count | page 6, count of rows |
| Heat loss indicator | page 8, "Per m2" |
| Dwelling type, storeys, year | page 1 |
| Wall construction | page 5, description column |
| Existing heating | page 10, Heating System |
| County | page 1 |

The roof needs care. Attic-level insulation is priced on the ceiling area and rafter
insulation on the rafter area; the report gives each roof element with its type, so the
parser maps by type rather than using the total blindly.

## The spike, and what it showed

`design/spikes/ddr_read_spike.html` loads pdf.js (3.11.174, from cdnjs — library code
only; the document is read in the page and never sent anywhere), takes a file input,
and rebuilds table rows from the positioned text items by grouping on the y coordinate and
ordering on x. Served from 127.0.0.1 and driven in the browser, it read all 19 pages, and
the rows came out as clean columns:

```
p5: 425mm Filled Cavity | 150mm PIR | No | Yes | 2014 onwards | 113.50 | 0.16 | 18.16
p6: 1 | 1.4 | Front- Solid | 2.20 | 1.40 | 3.08
p8: Fabric heat loss [W/K] | 149.53 | Total heat loss [W/K] | 226.25
p8: Per m2 | 1.56
p1: Dwelling Type | Detached house
p10: Heating System | Air-to-water heat pump (electric)
```

Every "Total area [m²]" line came through with its figure. That was the one real unknown —
whether a browser-side reader would keep DEAP's table cells in order — and it does.

## Design

1. An **Upload dwelling details report** control in the survey sidebar, in all three
   modes; the report format is the same for new build, refurbishment and energy upgrade.
2. On file select, pdf.js reads the file **in the page**. No fetch, no upload, no key.
3. A deterministic parser finds each section by its label, reads the total line and the
   element rows, and maps them to the inputs above.
4. Values are written into the **existing** sidebar fields, each marked as read from the
   report, so the assessor sees what was filled and overrides in place.
5. Anything the parser cannot find is left blank and listed, never guessed.

## Decided

**pdf.js is built into the file.** Version 3.11.174, Mozilla, Apache 2.0, the last release
with a classic script build. Both parts sit at the foot of `ber_build_planner.html` as inert
text (`type="application/x-pdfjs"`) and are started only when a report is chosen, so the app
opens no slower. The worker code runs on the page's own thread, so there is no worker file
and no URL to fetch. The file grows by about 1.4 MB.

**The AI paths are gone.** The old BER PDF upload, which sent the document to an AI service
with a pasted key, and an energy upgrade generator that asked one for measures, were both
removed with the code only they used. Neither was reachable from the screen any more.

---

## As built, 15 September 2026

Tested on five of the author's reports, none committed: three new-build provisionals (one
single storey, two two-storey, one with a roof window), one refurbishment with an extension
labelled in mixed case with an unlabelled wall, and one provisional of an existing house
with an extension where the report itself says "Dwelling Extension: Yes".

### Reading

Each table row wraps over several text lines around the one line that carries its figures.
The parser finds that line by the Area column, gives every wrapped fragment to the nearest
such line, and splits text into Type and Description by the header positions. Every table
is then added up and compared with the report's own "Total area" line; on all five reports
every table matches to the hundredth. A mismatch is shown, never hidden.

What the samples showed, which the design had to take in:

- **Existing and extension are told apart only by the assessor's description.** The author
  labels floors, roofs and walls "Existing" or "Extension" only when the property has an
  extension; anything unlabelled is the existing house as standard. "EXISTING -",
  "Extension:" and "Extension" all occur. "Dwelling Extension" on page 1 says Yes on one
  report and N/A on another that is plainly an extension, so it is not relied on. Windows
  have no description column and cannot be split.
- **Upper floors are "Non-Heat Loss Floor" rows.** Ground floors are "Ground Floor - …". The
  split by storey comes from the dimension details on page 1, not the element rows.
- **Windows are counted in the Count column.** Rows marked In Roof are roof lights and go
  to the roof light count, not the window card.
- **Doors can be absent.** One report lists none; that is flagged, not filled.
- **Rafter roof areas are sloped areas.** The rate book already prices rafter insulation on
  the DEAP sloped area, so they go in unchanged.

### Where the values go

When the report labels an extension, its areas are kept apart from the existing house in
all three modes: on an extension card in Refurbishment, and on floor, wall and roof cards
captioned Existing or Extension in New Build and Energy Upgrade, each with its own ground
floor perimeter to count.

| From the report | New Build and Energy Upgrade | Refurbishment with extension rows |
|---|---|---|
| Address, dwelling type, county | Project details | Project details |
| Floor area and height per storey | a floor card per storey; with an extension, existing and extension cards per storey | house floors on floor cards, extension floors on the extension card |
| Walls, roofs | a card per element, captioned Existing or Extension and its description | house elements on cards, extension totals on the extension card |
| Windows and roof lights | one card with count and area; roof light count | the same; the extension card is set to none |
| Doors | door count and area | the same |
| Heat Loss Indicator, year of construction | Energy Upgrade only: HLI and age band | not used |

The report is chosen from a row at the top of Project Details, above the fields it fills, and what
it read, with the additional survey counts, opens inside that same panel, so the home screen
looks as it did before until a report is read. Filled fields carry a tooltip only; wall,
roof and floor cards carry a grey caption naming Existing or Extension and the report's
description. Wet rooms and gable end peaks sit at the foot of the Rooms and Roof tabs in the
same form as External Doors and Roof Lights in Openings. A room card is made for each storey.

### Counted on survey

The report cannot give these, so the panel asks for them straight after reading and writes
them into the tabs. It shows nothing else.

- **Rooms on each storey the report lists**, house and extension together, onto a Rooms tab
  card per storey ("Rooms (total)").
- **Wet rooms for the whole dwelling, kitchen included**, a single field at the top of the
  Rooms tab. Wet rooms take the extract and every other room an air inlet; the panel shows
  the result, for example "1 extract · 4 air inlets from 5 rooms".
- Ground floor perimeter, house and extension.
- Gable end peaks, a new Roof tab field for every project type, kept in step with the
  Energy Upgrade external wall insulation choice.

Windows, roof lights and doors are not asked for: the report's Count column gives them. Rows
marked In Roof are the roof lights.

Once counted, the ventilation measures price from rooms and wet rooms, in Energy Upgrade and
in the house measures of Refurbishment. MEV extract terminals and DMEV fans are one per wet
room. Air inlets are a new line, one per remaining room, at the rate book's room air intake
vent rate (the same rate as that Not Included item); MEV leaves them out when trickle vents
are chosen. MVHR takes one terminal per room. With no count entered the older estimate from
bathrooms, en-suites and an assumed kitchen stands, so existing plans price as before.

Two small changes to the extension card came with this. Its window area and door count now
take an entered zero as zero rather than replacing it with an estimate, and a measured
ground floor perimeter is used in pricing instead of the estimate from area.

### Checked by

`scripts/verify/ddr.js` reads every report it is given in all three project types and checks
the result against the report itself, so it holds no client figures: tables match their
totals, the cards carry the areas whole, the HLI arrives, survey counts reach the tabs, a
save and restore keeps it, the plan generates, and no request leaves the page. A PDF that is
not a report is refused. `scripts/verify/ddr_journey.js` runs the whole journey as the
assessor clicks it, through to all three documents printed.

### Accuracy audit, 16 September 2026

All five reports were priced in all three modes with a broad set of measures and survey
counts, and every priced quantity was set beside the report's own figures.

Right: floor, wall, ceiling, flat and rafter areas where the roof has that type; ground floor
area for floor insulation; first floor area for upper floors; window area; the heat pump
size (HLI × floor area × 23 K matches the kW on every report); extract terminals and air
inlets from the counts; gable peaks in the external wall insulation elevation.

Fixed in this pass:
- The extension builder turned an entered zero for windows and doors back into 8 m² and one
  door. It now keeps the zero.
- The extension's ceiling height now comes from its own floor card, not a default 2.7 m.
- New Build counted rooms only from the room-type boxes, so a survey with room totals priced
  one internal door. It now uses the surveyed total when that is larger.
- A report with no external doors made Energy Upgrade price two by default. The panel now
  asks for doors when the report lists none.

Decided by the author and done, 16 September 2026:
- **Windows are priced by area.** The report's Count column groups glazing by elevation, so
  no count is filled from it and the window description no longer states one.
- **Roofs are priced by type**, in New Build and in the Refurbishment extension. Pitched roofs
  get timbers, underlay and covering on the slope (ceiling-level plan area × 1.22 for the
  35° pitch assumed elsewhere; rafter and room-in-roof areas are already on the slope).
  Ceiling insulation is priced on ceiling-level roofs, rafter insulation on rafter-level
  roofs, and flat roofs get a deck, warm-deck insulation and a membrane, never tiles.
- **Bathrooms, kitchens and utility rooms are counted** for the whole dwelling, on the panel
  and in the Rooms tab; wet rooms are their sum. When the floor cards carry no room types,
  New Build prices wall tiling, sanitary accessories and drainage from the bathrooms, and
  kitchen and utility tiling and waste runs from the kitchens and utility rooms.
- **A roof measure for a roof type the Roof tab lacks stops generation** with a message naming
  the missing section, in Energy Upgrade and Refurbishment. It used to price the whole roof.
- **The report's HLI and cylinder volume are used** in every mode: heat pump size is HLI ×
  whole-dwelling floor area × 23 K, and the cylinder is the report's volume. In
  Refurbishment, whole-house plant (heat pump, extract ducting, MVHR) is sized on the house
  plus its extensions, not the house alone.

Re-audited on all five reports: the three modes give the same heat pump, cylinder and duct
run for each dwelling, and every roof, room and wet room quantity follows the counts.

### In the SEAI pack

The reader is step 2 of the Software document, on two screens: the panel with the report read
and the survey counts, and the Roof tab it filled. No client's report could go into a document
that leaves the office, so `pack/make_sample_report.js` writes one — a DEAP report for the
pack's own Westport example, every label and figure at the coordinate a real report puts it,
so the reader parses it the same way and the screens are the live software reading a real
file. It reads with no warnings: floors 118, roofs 118, walls 108, windows 19, doors 4.40,
HLI 2.1, cylinder 300. `pack/shot_ddr_reader.js` takes the two screens, and `pack/shot_home.js`
now takes the home screen too, which had been hand-made since the spring and still showed a
home screen with no reader on it.

Taking those screens found one fault of its own: the report date the app fills on load was
captured as pristine *before* it was filled, so choosing a project type cleared it and it
never came back. The date is now filled before the capture and after every reset.

### Open

- A saved project does not bring back extension cards on restore. That was already so for
  extensions entered by hand; the reader does not change it.
- A table long enough to run onto a second page has not been seen. The parser follows it
  across the page break, but no sample tests that.
- No published BER for an existing dwelling has been read yet; all five samples are
  provisional ratings.
