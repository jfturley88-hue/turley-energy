// A sample Dwelling Details Report, for the pack's screenshots.
//
// The reader's screens have to show a house, and no client's report can go into a document
// that leaves the office. This writes a report for the pack's own worked example — Carrowbeg,
// Westport — with every label and figure at the position DEAP puts it, so the reader parses
// it exactly as it parses a real one and the screens in document 05 show the live software
// reading a real file. Figures match the Westport example used for the other screenshots.
//
//   node pack/make_sample_report.js     →  pack/sample_dwelling_report.pdf
const { chromium } = require('playwright');
const path = require('path');

const OUT = path.join(__dirname, 'sample_dwelling_report.pdf');

// Column positions in points, as they come out of a DEAP report: two label columns on the
// details page, and one column per figure in the element tables.
const X = { labL: 49.9, valL: 175, labR: 311.9, valR: 446, type: 41.8, desc: 200, mid: 320, age: 385, area: 445, u: 495, hl: 540 };
const TOP = 74;      // first line of a section, measured down the page
const LINE = 17.4;   // line pitch

const H = {
  mprn: '10012345678', address: ['CARROWBEG', 'WESTPORT', ''], county: 'Co. Mayo',
  dwelling: 'Bungalow', year: 1979, storeys: 1,
  ground: [118.0, 2.40, 283.20],
  floors: [['Ground Floor - Solid', '150mm PIR', 118.0, 0.19, 22.42]],
  roofs: [['Pitched Roof - Insulated on Ceiling', '150mm Fibreglass', 70.0, 0.25, 17.50],
          ['Pitched Roof - Insulated on Rafter', '80mm PIR between rafters', 48.0, 0.30, 14.40]],
  walls: [['300mm Filled Cavity', 'Bonded bead 50mm cavity', 108.0, 0.55, 59.40]],
  doors: [['1.4', 'Front - solid', 2.20, 1.40, 3.08], ['1.4', 'Rear - solid', 2.20, 1.40, 3.08]],
  windows: [['South', 7.60], ['North', 4.20], ['East', 3.80], ['West', 3.40]],
  fabric: 168.4, totalHeatLoss: 247.8, perM2: 2.1, cylinder: 300,
};
const m2 = n => Number(n).toFixed(2);
const sum = (rows, i) => rows.reduce((a, r) => a + r[i], 0);

const T = [];                                    // [page, x, top, text, bold]
let pg = 0, y = TOP;
const at = (x, text, bold) => { if (text !== '' && text != null) T.push([pg, x, y, String(text), !!bold]); };
const line = (n) => { y += LINE * (n === undefined ? 1 : n); };
const newPage = () => {
  pg++; y = 24; at(390, 'Dwelling Details Report'); at(505, 'Page ' + pg + '/8');
  y = 36; at(390, 'Date report created: 20/09/2026'); y = TOP;
};
const section = t => { at(X.labL, t, true); line(1.5); };
const kv = (l, v, l2, v2) => { at(X.labL, l); at(X.valL, v); at(X.labR, l2); at(X.valR, v2); line(); };
const heads = cols => {
  // DEAP wraps its column headings, so "Area" sits on a line of its own above the figures.
  const top = y, depth = Math.max(...cols.map(([, t]) => String(t).split('|').length));
  cols.forEach(([x, t]) => String(t).split('|').forEach((part, i) => { y = top + i * 9; at(x, part); }));
  y = top + depth * 9 + 6;
};
const totalLine = total => { line(0.5); at(X.type, 'Total area [m2]'); at(X.area, m2(total)); };

// 1 · property details and dimensions
newPage();
section('Property details');
kv('MPRN', H.mprn, 'Shared MPRN', 'No');
kv('BER Number', 'N/A', 'Type of Rating', 'New Dwelling - Provisional');
kv('Address line 1', H.address[0], 'Purpose of Rating', 'New dwelling for owner occupation');
kv('Address line 2', H.address[1], 'Building Regulations', '2022 TGD L');
kv('Address line 3', H.address[2], 'Date of Plans', '01/09/2026');
kv('County', H.county, 'Assessor Name', 'John Turley');
kv('Eircode', '', 'Assessor Number', '100615');
kv('Dwelling Type', H.dwelling, 'Date of Assessment', '18/09/2026');
kv('Year of construction', H.year, 'Assessor Comments', 'Sample report — demonstration only');
kv('Dwelling Extension', 'No', '', '');
kv('Storeys', H.storeys, '', '');
line(0.8);
section('Dimension details');
heads([[X.valL, 'Area|[m2]'], [X.age, 'Height [m]'], [X.valR, 'Volume|[m3]']]);
[['Ground floor', H.ground], ['First floor', [0, 0, 0]], ['Second floor', [0, 0, 0]],
 ['Third and other floors', [0, 0, 0]], ['Room in Roof', [0, 0, 0]]].forEach(([n, d]) => {
  at(X.labL, n); at(X.valL, m2(d[0])); at(X.age, m2(d[1])); at(X.valR, m2(d[2])); line();
});
at(X.labL, 'Totals'); at(X.valL, m2(H.ground[0])); at(X.valR, m2(H.ground[2])); line(1.4);
at(X.labL, 'Living Area'); at(X.valL, '31.00 m2'); line();
at(X.labL, 'Living Area Percentage'); at(X.valL, '26.27 %');

// 2 · ventilation
newPage();
section('Ventilation details');
kv('Ventilation method', 'Whole-house extract ventilation', 'Number of sides sheltered', '2');
kv('How many wetrooms (inc. kitchen)?', '3', 'Effective air change rate [ac/h]', '0.52');

// 3 · floors — and the other element tables, each with its own header row
const elementPage = (title, cols, rows, draw, total) => {
  newPage();
  section(title);
  heads(cols);
  rows.forEach(r => { draw(r); line(); });
  totalLine(total);
};
const AREA_COLS = [[X.area, 'Area|[m2]'], [X.u, 'U-Value|[W/m2K]'], [X.hl, 'Heat|Loss|(AU)|[W/K]']];

elementPage('Building Elements - Floors',
  [[X.type, 'Type'], [X.desc, 'Description'], [X.mid, 'Include in|compliance|check'], [X.age, 'Age Band'], ...AREA_COLS],
  H.floors,
  f => { at(X.type, f[0]); at(X.desc, f[1]); at(X.mid, 'Yes'); at(X.age, '1978 - 1982'); at(X.area, m2(f[2])); at(X.u, m2(f[3])); at(X.hl, m2(f[4])); },
  sum(H.floors, 2));

elementPage('Building Elements - Roofs',
  [[X.type, 'Type'], [X.desc, 'Description'], [X.mid, 'Include in|compliance|check'], [X.age, 'Age Band'], ...AREA_COLS],
  H.roofs,
  r => { at(X.type, r[0]); at(X.desc, r[1]); at(X.mid, 'Yes'); at(X.age, '1978 - 1982'); at(X.area, m2(r[2])); at(X.u, m2(r[3])); at(X.hl, m2(r[4])); },
  sum(H.roofs, 2));

elementPage('Building Elements - Walls',
  [[X.type, 'Type'], [X.desc, 'Description'], [X.mid, 'Wall is|semi-|exposed'], [X.age, 'Age Band'], ...AREA_COLS],
  H.walls,
  w => { at(X.type, w[0]); at(X.desc, w[1]); at(X.mid, 'No'); at(X.age, '1978 - 1982'); at(X.area, m2(w[2])); at(X.u, m2(w[3])); at(X.hl, m2(w[4])); },
  sum(H.walls, 2));

elementPage('Building Elements - Doors',
  [[X.type, 'Count'], [95, 'Type'], [200, 'Description'], ...AREA_COLS],
  H.doors,
  d => { at(X.type, '1'); at(95, d[0]); at(200, d[1]); at(X.area, m2(d[2])); at(X.u, m2(d[3])); at(X.hl, m2(d[4])); },
  H.doors.reduce((a, d) => a + d[2], 0));

elementPage('Building Elements - Windows',
  [[X.type, 'Count'], [95, 'Glazing Type'], [250, 'Frame|Type'], [330, 'In Roof'], [385, 'Orient.'], [X.area, 'Area|[m2]'], [X.u, 'U-value|[W/m2K]']],
  H.windows,
  w => { at(X.type, '1'); at(95, 'Double-glazed, air filled'); at(250, 'Wood/PVC'); at(330, 'No'); at(385, w[0]); at(X.area, m2(w[1])); at(X.u, '2.80'); },
  sum(H.windows, 1));

// 8 · heat loss and water heating
newPage();
section('Heat loss details');
kv('Total glazed area [m2]', m2(sum(H.windows, 1)), 'Glazing ratio', '0.16');
kv('Fabric heat loss [W/K]', m2(H.fabric), 'Total heat loss [W/K]', m2(H.totalHeatLoss));
kv('Per m2', m2(H.perM2), '', '');
line(0.8);
section('Water heating details');
kv('Water storage volume [Litres]', m2(H.cylinder), 'Storage Type', 'Cylinder, indirect');
kv('Number of baths', '1', 'Number of mixer showers', '1');

const esc = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const pages = [];
for (let p = 1; p <= pg; p++) {
  pages.push('<section class="pg">' + T.filter(t => t[0] === p)
    .map(([, x, top, text, bold]) => `<span style="left:${x}pt;top:${top}pt;${bold ? 'font-weight:700;' : ''}">${esc(text)}</span>`)
    .join('') + '</section>');
}
const HTML = `<!doctype html><meta charset="utf-8"><style>
  @page { size: A4 portrait; margin: 0; }
  body { margin: 0; font-family: Arial, Helvetica, sans-serif; font-size: 8pt; color: #111; }
  .pg { position: relative; width: 595pt; height: 842pt; page-break-after: always; }
  .pg span { position: absolute; white-space: nowrap; }
</style>${pages.join('')}`;

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  const p = await b.newPage();
  await p.setContent(HTML, { waitUntil: 'load' });
  await p.pdf({ path: OUT, printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log('wrote', OUT, '·', pg, 'pages');
})().catch(e => { console.error(e); process.exit(1); });
