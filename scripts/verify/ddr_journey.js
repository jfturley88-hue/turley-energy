// The whole journey with a Dwelling Details Report, the way an assessor works it:
// click the project type, choose the report, type the additional survey counts, open the
// inputs, tick measures, generate, then print the Cost Plan, the Appendix and the Schedule.
//
// Checked at each stage against the report itself, so no client figures live here.
//   DDR_SAMPLES="dir;file.pdf" node scripts/verify/ddr_journey.js [outDir]
// With outDir, each Cost Plan is also saved as a PDF there for a look by eye.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const url = require('url');

const APP = url.pathToFileURL(path.resolve(__dirname, '..', '..', 'ber_build_planner.html')).href;
const OUT = process.argv[2] || '';
const CARD = { 'New Build': '#card-newbuild', 'Refurbishment': '#card-refurb', 'Energy Upgrade': '#card-upgrade' };
// the measures ticked in each mode: enough to use areas, perimeter, gables and room counts
const MEASURES = {
  'New Build': [],
  'Refurbishment': ['ws-making-good', 'ref-eu-mev'],
  'Energy Upgrade': ['eu-roof-ceiling', 'eu-ewi', 'eu-mev'],
};

function samples() {
  const out = [];
  (process.env.DDR_SAMPLES || '').split(';').map(s => s.trim()).filter(Boolean).forEach(p => {
    if (!fs.existsSync(p)) return;
    if (fs.statSync(p).isDirectory()) fs.readdirSync(p).filter(f => /\.pdf$/i.test(f)).forEach(f => out.push(path.join(p, f)));
    else out.push(p);
  });
  return out;
}

(async () => {
  const files = samples();
  if (!files.length) { console.log('No reports given. Set DDR_SAMPLES.'); process.exit(2); }
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  let fail = 0, steps = 0;
  const ok = (cond, label, detail) => { steps++; if (!cond) fail++; console.log((cond ? 'ok   ' : 'FAIL ') + label + (detail ? ' -> ' + detail : '')); };

  for (const [fi, file] of files.entries()) {
    for (const mode of Object.keys(CARD)) {
      const tag = `[report ${fi + 1} · ${mode}]`;
      const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
      const errors = [], requests = [];
      p.on('pageerror', e => errors.push(e.message));
      p.on('dialog', d => d.accept());
      await p.goto(APP);
      await p.evaluate(() => { window.print = () => {}; });
      await p.waitForTimeout(600);
      p.on('request', r => { if (!/^(file|blob|data):/.test(r.url())) requests.push(r.url()); });

      // 1. project type, by its card
      await p.click(CARD[mode]);
      const tickedBefore = await p.evaluate(() => [...document.querySelectorAll('#screen-input input[type=checkbox]')].filter(c => c.checked).map(c => c.id).sort().join(','));
      // 2. the report
      await p.setInputFiles('#ddr-panel input[type=file]', file);
      await p.waitForFunction(() => /Additional survey counts|could not be read|No dwelling details/.test(document.getElementById('ddr-result').textContent), null, { timeout: 60000 });
      const read = await p.evaluate(() => {
        const r = window._ddrState.report;
        return {
          addr: document.getElementById('t0-projName').value, county: document.getElementById('t0-county').value,
          storeys: r.dims.filter(d => d.area > 0).length, hli: r.hli,
          ext: ['floors', 'walls', 'roofs'].some(t => r[t].rows.some(x => x.part === 'extension')),
          walls: r.walls.total, bad: document.querySelectorAll('#ddr-result .ddr-bad').length,
        };
      });
      ok(read.addr && read.county && read.bad === 0, `${tag} report read into Project details, totals match`, `${read.county}`);

      // 3. additional survey counts, typed as a person types them
      const boxes = await p.$$('#ddr-result input[data-ddr-target^="fc-t5r-total-"]');
      for (const bx of boxes) await bx.fill('4');
      await p.fill('#ddr-result input[data-ddr-target="t5-bathsWhole"]', '1');
      await p.fill('#ddr-result input[data-ddr-target="t5-kitchens"]', '1');
      await p.fill('#ddr-result input[data-ddr-target="t5-utilities"]', '1');
      for (const bx of await p.$$('#ddr-result input[data-ddr-target*="perim"]')) await bx.fill('38');
      await p.fill('#ddr-result input[data-ddr-target="t3-gablePeaks"]', '2');
      const rooms = boxes.length * 4, inlets = rooms - 3;
      const note = await p.textContent('#ddr-result .ddr-vent');
      ok(new RegExp(`3 extracts · ${inlets} air inlets? from ${rooms} rooms`).test(note), `${tag} counts typed, the panel shows extracts and inlets`, note);

      // 4. open the inputs and look at the tabs
      // the button's label changes with the project type; it is the one that opens the inputs
      await p.click('button[onclick="openProjectSections()"] >> visible=true');
      await p.waitForTimeout(700);
      const tabs = await p.evaluate(() => {
        const vals = sel => [...document.querySelectorAll(sel)].map(e => parseFloat(e.value) || 0);
        const sum = a => a.reduce((x, y) => x + y, 0);
        return {
          inputsShown: getComputedStyle(document.getElementById('screen-input')).display !== 'none',
          floors: vals('[id^="fc-t1-area-"]').length, walls: sum(vals('[id^="fc-t2-area-"]')),
          perim: getCurrentPerimeterSum(), gables: document.getElementById('t3-gablePeaks').value,
          rooms: getCurrentRoomCounts().rooms, wet: getCurrentRoomCounts().wetRooms,
          hli: parseFloat((document.getElementById('eu-hli') || {}).value) || null,
          ticked: [...document.querySelectorAll('#screen-input input[type=checkbox]')].filter(c => c.checked).map(c => c.id).sort().join(','),
        };
      });
      ok(tabs.inputsShown && tabs.floors >= 1, `${tag} Open Inputs shows the filled tabs`, `${tabs.floors} floor cards`);
      ok(tabs.rooms === rooms && tabs.wet === 3 && tabs.gables === '2', `${tag} counts are in the Rooms and Roof tabs`, JSON.stringify({ r: tabs.rooms, w: tabs.wet, g: tabs.gables }));
      ok(tabs.perim >= 38, `${tag} perimeter is in the Floors tab`, String(tabs.perim));
      ok(tabs.ticked === tickedBefore, `${tag} the reader ticks nothing; the assessor selects the measures`);
      if (mode === 'Energy Upgrade') ok(Math.abs(tabs.hli - read.hli) < 0.001, `${tag} Heat Loss Indicator in place`, String(tabs.hli));

      // 5. the assessor ticks measures
      for (const id of MEASURES[mode]) {
        await p.evaluate(id => { const c = document.getElementById(id); if (c && !c.checked) c.click(); }, id);
        await p.waitForTimeout(150);
      }

      // 6. generate, from the button on screen
      await p.evaluate(() => {
        const btn = [...document.querySelectorAll('#generate-boq-btn, #generate-btn-wrapper .generate-btn')].find(x => x.offsetParent !== null);
        if (btn) btn.click(); else generate();
      });
      await p.waitForFunction(() => typeof BOQ !== 'undefined' && BOQ && document.getElementById('screen-report') && getComputedStyle(document.getElementById('screen-report')).display !== 'none', null, { timeout: 30000 }).catch(() => {});
      await p.waitForTimeout(1200);
      const plan = await p.evaluate(() => {
        const T = typeof planTotals === 'function' ? planTotals(BOQ) : null;
        const txt = document.getElementById('screen-report').innerText;
        return { total: T && T.totalEst, bad: /\bNaN\b|undefined/.test(txt), err: document.getElementById('error-msg').textContent };
      });
      ok(plan.total > 0 && !plan.bad, `${tag} generated: a priced plan with no NaN or undefined`, `total ${plan.total} ${plan.err}`);

      // 7. the three documents
      for (const [kind, call] of [['Cost Plan', "exportEUPDF('detailed')"], ['Appendix', "exportEUPDF('appendix')"], ['Schedule', 'exportContractorSchedule()']]) {
        const doc = await p.evaluate(call => {
          (new Function(call))();
          const v = document.getElementById('pdf-print-view');
          const t = v ? v.innerText : '';
          return { chars: t.length, bad: /\bNaN\b|undefined/.test(t), addr: t, text: t };
        }, call);
        await p.waitForTimeout(500);
        ok(doc.chars > 500 && !doc.bad && doc.addr.indexOf(read.addr.split(',')[0]) >= 0, `${tag} ${kind} prints with the site address, no NaN or undefined`, `${doc.chars} chars`);
        if (kind === 'Cost Plan' && mode === 'Energy Upgrade') {
          ok(new RegExp(`Air inlets: ${inlets} nr`).test(doc.text) && /Extract terminals: 3 nr/.test(doc.text), `${tag} Cost Plan scope: 3 extract terminals and ${inlets} air inlets`);
          ok(/gable peak/i.test(doc.text), `${tag} Cost Plan scope: external wall insulation carries the gable peaks`);
        }
        if (kind === 'Cost Plan' && mode === 'Refurbishment' && read.ext) {
          ok(/EXTENSION/i.test(doc.text), `${tag} Cost Plan prices the extension`);
        }
        if (kind === 'Cost Plan' && OUT) {
          await p.addStyleTag({ content: '@media print { @page { size: A4 portrait; margin: 10mm 12mm 14mm 12mm; } }' });
          await p.pdf({ path: path.join(OUT, `journey_${fi + 1}_${mode.replace(/ /g, '_')}.pdf`), preferCSSPageSize: true, printBackground: true });
        }
        await p.evaluate(() => { const v = document.getElementById('pdf-print-view'); if (v) v.remove(); });
      }

      ok(errors.length === 0, `${tag} no page errors`, errors.join(' | ').slice(0, 200));
      ok(requests.length === 0, `${tag} nothing sent from the page`, requests.slice(0, 2).join(' '));
      await p.close();
    }
  }
  await b.close();
  console.log(`\n==== ${steps} steps, ${fail} FAIL ====`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
