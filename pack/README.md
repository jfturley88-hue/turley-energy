# The SEAI pack

Everything that builds the six-PDF pack. It used to live in a session scratchpad, which
is ephemeral — this directory is the source of record.

## The six documents

| | Document | Made from |
|---|---|---|
| 01 | The Value Proposition | `pack_01.html` |
| 02 | The Cost Plan | `pack_02.html` + `ex_plan.pdf` |
| 03 | The Pricing Schedule | `pack_03.html` + `ex_sched.pdf` |
| 04 | The Appendix | `pack_04.html` + `ex_appx.pdf` |
| 05 | The Workflow | `pack_05.html` |
| 06 | The Software | `pack_06.html` |

Documents 02–04 are the software's own output bound whole, each behind one page of notes
saying who it is for and how long it lives. They are printed by `gen_ex_pdfs.js` driving
`../ber_build_planner.html` — not written by hand — so the pack cannot drift from what the
software actually prints.

## Rebuilding

```sh
npm i docx playwright          # docx for the editable Word files
pip install pypdf pillow       # pypdf assembles, pillow crops the print-dialog shot

node gen_ex_pdfs.js            # 1. the three documents, from the live app
python3 seai_pack.py           # 2. pack_01..06.html
node print_pack.js             # 3. those to PDF; reports any page that overflows
node extract_editable.js       # 4. pull the editable prose blocks out again
node build_edit_docs.js        # 5. one Word file per document
python3 build_pack.py          # 6. assemble both folders and zips, and verify
```

`build_pack.py` reads the figures back out of the finished PDFs and prints them. Check
them. The pack shipped a stale set of figures once because the parts were regenerated and
the folder was assembled by hand from the previous run.

## Screenshots

`refresh_app_shots.js` regenerates the app screenshots in document 06 (`app_plan`,
`app_routes`, `app_selector`). `pack_shots.js` regenerates the Cost Plan / Schedule /
grants shots.

`shot_preview.js` is the odd one. The print-preview figure is Chrome's own dialog, which
is browser chrome rather than page content, so no headless screenshot API can see it. It
launches a *headed* Chromium on an Xvfb display, lets the app call `window.print()` for
real, and grabs the whole X screen from outside the browser:

```sh
Xvfb :99 -screen 0 1600x1200x24 &
DISPLAY=:99 node shot_preview.js
```

That figure is captioned as unedited, so it must stay a real capture — never composite it.

## Figures

Every money figure in the prose comes from the `EX_*` constants at the top of
`seai_pack.py`, which are copied from `gen_ex_pdfs.js`'s own output. Do not retype them
anywhere else in the prose: the same figure appearing twice is how they drift apart.

Take them from `planTotals()`, never from `BOQ.summary` — the summary path applies a flat
13.5% VAT (heat pumps are 9%) and omits the post-works BER.
