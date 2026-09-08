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

## Two things to decide before building

**Where pdf.js lives.** Loading it from cdnjs matches how the app already loads SheetJS,
and sends no data anywhere. Inlining it makes the app fully self-contained at the cost of
roughly 1.5 MB on a 1.4 MB file. Either satisfies the no-third-party rule; inline is the
stronger answer if the file itself is ever handed to SEAI.

**The existing AI path.** The app already has a feature that sends a BER PDF to Anthropic
for extraction, behind a user-entered key. Given the rule above, it should be removed or
clearly fenced off from this feature, or the pack's claim is undermined by the software.

## Before it is built

Three provisionals for existing dwellings, one new-build report and one refurbishment with
an extension, all from the author. The sample here is a single-storey new build; existing
dwellings will show multi-storey floor tables, several wall constructions, and the
"Dwelling Extension: Yes" case, which the parser has to handle before it is trusted.
