// The Dwelling Details Report reader, driven in the real app.
//
// Every report given is read in all three project types, and the result is checked against
// the report itself rather than against remembered figures, so no client data lives here:
//   - every element table adds up to the report's own total
//   - the cards hold exactly the report's areas (house and extension together)
//   - Energy Upgrade carries the report's Heat Loss Indicator
//   - the survey counts typed on the panel land in the tabs
//   - a save and restore keeps what was filled
//   - the plan generates with no page error
//   - nothing is requested from any server while the report is read
//
//   DDR_SAMPLES="C:/reports/new build;C:/reports/refurb/one.pdf" node scripts/verify/ddr.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const url = require('url');

const APP = url.pathToFileURL(path.resolve(__dirname, '..', '..', 'ber_build_planner.html')).href;
const NOT_A_REPORT = path.resolve(__dirname, '..', '..', 'pack', 'PlanitBER_SEAI_Pack', 'PlanitBER_02_The_Baseline_Cost_Plan.pdf');

function samples() {
  const out = [];
  (process.env.DDR_SAMPLES || '').split(';').map(s => s.trim()).filter(Boolean).forEach(p => {
    if (!fs.existsSync(p)) { console.log('missing sample path:', p); return; }
    if (fs.statSync(p).isDirectory()) fs.readdirSync(p).filter(f => /\.pdf$/i.test(f)).forEach(f => out.push(path.join(p, f)));
    else out.push(p);
  });
  return out;
}

const near = (a, b) => Math.abs((a || 0) - (b || 0)) < 0.06;

(async () => {
  const files = samples();
  if (!files.length) { console.log('No reports given. Set DDR_SAMPLES to report files or folders.'); process.exit(2); }
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  let fail = 0, steps = 0;
  const ok = (cond, label, detail) => { steps++; if (!cond) fail++; console.log((cond ? 'ok   ' : 'FAIL ') + label + (detail ? ' -> ' + detail : '')); };

  for (const file of [...files, NOT_A_REPORT]) {
    const tag = path.basename(file).slice(0, 18) + '\u2026';
    for (const mode of ['New Build', 'Refurbishment', 'Energy Upgrade']) {
      if (file === NOT_A_REPORT && mode !== 'New Build') continue;
      const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
      const errors = [];
      p.on('pageerror', e => errors.push(e.message));
      p.on('dialog', d => d.accept());
      await p.goto(APP);
      await p.evaluate(() => { window.print = () => {}; });
      await p.waitForTimeout(500);
      await p.evaluate(m => selectProjectType(m), mode);

      // from here on, anything leaving the page is a failure
      const requests = [];
      p.on('request', r => { if (!/^(file|blob|data):/.test(r.url())) requests.push(r.url()); });
      await p.setInputFiles('#ddr-panel input[type=file]', file);
      await p.waitForFunction(() => {
        const t = (document.getElementById('ddr-result') || {}).textContent || '';
        return /Additional survey counts|could not be read|No dwelling details|not a PDF/.test(t);
      }, null, { timeout: 60000 });

      if (file === NOT_A_REPORT) {
        const t = await p.evaluate(() => document.getElementById('ddr-result').textContent);
        ok(/No dwelling details were found/.test(t), `[${tag}] a PDF that is not a report is refused, nothing filled`, t.slice(0, 80));
        ok(errors.length === 0, `[${tag}] no page errors`, errors.join(' | '));
        await p.close();
        continue;
      }

      const got = await p.evaluate(() => {
        const S = window._ddrState, r = S.report;
        const num = id => parseFloat((document.getElementById(id) || {}).value) || 0;
        const cards = (prefix, field) => [...document.querySelectorAll(`[id^="fc-${prefix}-${field}-"]`)].reduce((a, e) => a + (parseFloat(e.value) || 0), 0);
        // extensionCount is a script-level let, not a window property
        const ext = (typeof extensionCount !== 'undefined' && extensionCount) ? (() => {
          let fl = 0;
          for (let fc = 1; fc <= (extFloorCounts[1] || 0); fc++) fl += num('ext1-fl' + fc + '-area');
          return { floors: fl, walls: num('ext1-wa'), roofs: num('ext1-ra'), read: readExtensions()[0] };
        })() : null;
        return {
          applied: S.applied,
          bad: document.querySelectorAll('#ddr-result .ddr-bad').length,
          split: !!ext,
          rpt: {
            dims: r.dims.reduce((a, d) => a + d.area, 0), floors: r.floors.total, walls: r.walls.total, roofs: r.roofs.total,
            windows: r.windows.rows.filter(w => !w.inRoof).reduce((a, w) => a + w.area, 0),
            doors: r.doors.rows.reduce((a, d) => a + (d.count || 1), 0), hli: r.hli,
            winCount: r.windows.rows.filter(w => !w.inRoof).reduce((a, w) => a + (w.count || 1), 0),
            roofLights: r.windows.rows.filter(w => w.inRoof).reduce((a, w) => a + (w.count || 1), 0),
            storeys: r.dims.filter(d => d.area > 0).map(d => d.level),
          },
          cards: { floors: cards('t1', 'area'), walls: cards('t2', 'area'), roofs: cards('t3', 'area'), windows: cards('t4', 'area') },
          doors: num('t4-doorCount'), hli: num('eu-hli'), hliSource: (document.getElementById('eu-hli-source') || {}).value,
          ext, flags: S.flags.slice(),
          winCount: [...document.querySelectorAll('[id^="fc-t4-count-"]')].reduce((a, e) => a + (parseInt(e.value) || 0), 0),
          roofLights: parseInt((document.getElementById('t4-roofLights') || {}).value) || 0,
          doorText: (document.getElementById('t4-doorCount') || {}).value,
          project: {
            line1: r.meta.address[0] || '', mprn: r.meta.mprn, assessor: r.meta.assessor,
            names: (!r.meta.mprn || /^0+$/.test(r.meta.mprn)) && !/\d/.test(r.meta.address[0] || '') && r.meta.address.slice(1).some(Boolean),
            client: document.getElementById('t0-clientName').value, site: document.getElementById('t0-projName').value,
            prepared: document.getElementById('t0-preparedBy').value,
          },
          parts: (() => {
            const ext = t => r[t].rows.filter(x => x.part === 'extension').reduce((a, x) => a + x.area, 0);
            const onCards = tab => [...document.querySelectorAll(`[id^="fc-${tab}-"] .ddr-cap`)]
              .filter(c => /^Extension\b/.test(c.textContent))
              .reduce((a, c) => a + (parseFloat((document.getElementById(`fc-${tab}-area-` + c.parentElement.id.split('-').pop()) || {}).value) || 0), 0);
            return { has: ['floors', 'walls', 'roofs'].some(t => ext(t) > 0), floors: ext('floors'), walls: ext('walls'), roofs: ext('roofs'),
                     cFloors: onCards('t1'), cWalls: onCards('t2'), cRoofs: onCards('t3'),
                     perim: [...document.querySelectorAll('#ddr-result .tab-field label')].some(l => /perimeter, extension/.test(l.textContent)) };
          })(),
          asked: [...document.querySelectorAll('#ddr-result input[data-ddr-target]')].map(i => i.dataset.ddrTarget),
          roomLabels: [...document.querySelectorAll('#ddr-result input[data-ddr-target^="fc-t5r-total-"]')].map(i => i.closest('.tab-field').querySelector('label').textContent.replace(/^Rooms, /, '')),
        };
      });
      ok(got.applied && got.bad === 0, `[${tag}] ${mode}: read and every table matches its report total`);
      {
        const J = got.project, low = x => String(x).toLowerCase();
        ok(J.names ? (low(J.client) === low(J.line1) && low(J.site).indexOf(low(J.line1)) === -1) : (J.client === '' && low(J.site).indexOf(low(J.line1)) === 0),
           `[${tag}] ${mode}: client name from address line 1 only when the dwelling has no MPRN`, JSON.stringify({ client: !!J.client, names: J.names }));
        ok(J.prepared === J.assessor, `[${tag}] ${mode}: Prepared by is the assessor named on the report`);
      }
      const f = got.cards.floors + (got.ext ? got.ext.floors : 0);
      const w = got.cards.walls + (got.ext ? got.ext.walls : 0);
      const rf = got.cards.roofs + (got.ext ? got.ext.roofs : 0);
      ok(near(f, got.rpt.dims) && near(f, got.rpt.floors), `[${tag}] ${mode}: floor areas carried whole`, `${f} vs ${got.rpt.floors}`);
      ok(near(w, got.rpt.walls), `[${tag}] ${mode}: wall areas carried whole`, `${w} vs ${got.rpt.walls}`);
      ok(near(rf, got.rpt.roofs), `[${tag}] ${mode}: roof areas carried whole`, `${rf} vs ${got.rpt.roofs}`);
      ok(near(got.cards.windows, got.rpt.windows), `[${tag}] ${mode}: window area carried, roof windows kept out`, `${got.cards.windows} vs ${got.rpt.windows}`);
      ok(got.rpt.doors ? got.doors === got.rpt.doors : got.doorText === '', `[${tag}] ${mode}: doors as the report counts them`);
      ok(got.winCount === got.rpt.winCount && got.roofLights === got.rpt.roofLights, `[${tag}] ${mode}: window and roof light counts from the report`, JSON.stringify({ w: got.winCount, rl: got.roofLights }));
      ok(!got.asked.some(t => /fc-t4-count|t4-roofLights/.test(t)) && got.asked.includes('t4-doorCount') === !got.rpt.doors,
         `[${tag}] ${mode}: windows and roof lights never asked for; doors only when the report lists none`);
      ok(JSON.stringify(got.roomLabels) === JSON.stringify(got.rpt.storeys.map(x => x.toLowerCase())), `[${tag}] ${mode}: a room count for exactly the storeys in the report`, JSON.stringify(got.roomLabels));
      if (mode === 'Energy Upgrade') ok(near(got.hli, got.rpt.hli) && got.hliSource === 'ber', `[${tag}] Energy Upgrade: Heat Loss Indicator from the report`, `${got.hli} (${got.hliSource})`);
      if (got.ext) ok(got.ext.read.windowArea === 0 && got.ext.read.doorCount === 0, `[${tag}] Refurbishment: extension carries no invented windows or doors`, JSON.stringify({ w: got.ext.read.windowArea, d: got.ext.read.doorCount }));
      if (got.ext) {
        const perim = await p.evaluate(() => {
          const blank = [...document.querySelectorAll('[id^="ext1-fl"][id$="-perim"]')].every(e => e.value === '');
          const box = document.querySelector('#ddr-result input[data-ddr-target="ext1-fl1-perim"]');
          if (box) { box.value = '30'; box.dispatchEvent(new Event('input', { bubbles: true })); }
          return { blank, box: !!box, priced: readExtensions()[0].perimeter };
        });
        ok(perim.blank, `[${tag}] Refurbishment: extension perimeter left for the survey, not estimated`);
        ok(perim.box && perim.priced === 30, `[${tag}] Refurbishment: the surveyed extension perimeter is what pricing reads`, JSON.stringify(perim));
      }
      if (mode !== 'Refurbishment') ok(!got.split, `[${tag}] ${mode}: no extension card outside Refurbishment`);
      if (got.parts.has) {
        const P = got.parts;
        const extF = got.ext ? got.ext.floors : P.cFloors, extW = got.ext ? got.ext.walls : P.cWalls, extR = got.ext ? got.ext.roofs : P.cRoofs;
        ok(near(extF, P.floors) && near(extW, P.walls) && near(extR, P.roofs), `[${tag}] ${mode}: extension areas kept apart from the existing house`,
           JSON.stringify({ floors: [extF, P.floors], walls: [extW, P.walls], roofs: [extR, P.roofs] }));
        ok(P.perim, `[${tag}] ${mode}: the extension's ground floor perimeter is asked for separately`);
      }

      // survey counts typed on the panel go through to the tabs
      const typed = await p.evaluate(() => {
        const set = (sel, v) => { const el = document.querySelector(sel); if (!el) return false; el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); return true; };
        const g = set('#ddr-result input[data-ddr-target="t3-gablePeaks"]', '2');
        const per = document.querySelector('#ddr-result input[data-ddr-target^="fc-t1-perim-"]');
        if (per) { per.value = '41.5'; per.dispatchEvent(new Event('input', { bubbles: true })); }
        const tot = document.querySelector('#ddr-result input[data-ddr-target^="fc-t5r-total-"]');
        const wet = document.querySelector('#ddr-result input[data-ddr-target="t5-wetRooms"]');
        if (tot) { tot.value = '5'; tot.dispatchEvent(new Event('input', { bubbles: true })); }
        if (wet) { wet.value = '1'; wet.dispatchEvent(new Event('input', { bubbles: true })); }
        const rc = getCurrentRoomCounts();
        return {
          g, gables: document.getElementById('t3-gablePeaks').value, eu: (document.getElementById('eu-ewi-peaks') || {}).value,
          perim: per ? document.getElementById(per.dataset.ddrTarget).value : null, sumPerim: getCurrentPerimeterSum(),
          rooms: rc.rooms, wet: rc.wetRooms, note: (document.querySelector('#ddr-result .ddr-vent') || {}).textContent,
          others: !document.querySelector('#ddr-result input[data-ddr-target*="-wet-"]'),
        };
      });
      ok(typed.g && typed.gables === '2' && typed.eu === '2', `[${tag}] ${mode}: gable peaks reach the Roof tab and external wall insulation`, JSON.stringify(typed));
      ok(typed.perim === '41.5' && near(typed.sumPerim, 41.5), `[${tag}] ${mode}: ground floor perimeter reaches the Floors tab`);
      ok(typed.rooms === 5 && typed.wet === 1 && typed.others, `[${tag}] ${mode}: rooms per storey and wet rooms for the dwelling reach the Rooms tab`, JSON.stringify({ r: typed.rooms, w: typed.wet }));
      ok(/1 extract · 4 air inlets/.test(typed.note || ''), `[${tag}] ${mode}: the panel shows the extracts and air inlets they make`, typed.note);

      // save and restore keeps it
      const kept = await p.evaluate(() => {
        const before = [...document.querySelectorAll('[id^="fc-t"][id*="-area-"], #t3-gablePeaks, #t4-doorCount')].map(e => e.id + '=' + e.value).sort().join('|');
        const snap = buildSnapshot('TESTCODE');
        resetAllInputs();
        restoreSnapshot(snap);
        const after = [...document.querySelectorAll('[id^="fc-t"][id*="-area-"], #t3-gablePeaks, #t4-doorCount')].map(e => e.id + '=' + e.value).sort().join('|');
        return { same: before === after, before: before.slice(0, 120), after: after.slice(0, 120) };
      });
      ok(kept.same, `[${tag}] ${mode}: save and restore keep the filled survey`, kept.same ? '' : kept.before + ' / ' + kept.after);

      // it prices
      await p.evaluate(m => {
        const tick = id => { const e = document.getElementById(id); if (e && !e.checked) { e.checked = true; e.dispatchEvent(new Event('change', { bubbles: true })); } };
        if (m === 'Energy Upgrade') { tick('eu-roof-ceiling'); tick('eu-mev'); }
        if (m === 'Refurbishment') { tick('ws-making-good'); tick('ref-eu-mev'); }
      }, mode);
      await p.evaluate(() => generate());
      await p.waitForTimeout(2500);
      const priced = await p.evaluate(() => ({ boq: !!(window.BOQ || (typeof BOQ !== 'undefined' && BOQ)), err: (document.getElementById('error-msg') || {}).textContent || '' }));
      ok(priced.boq, `[${tag}] ${mode}: the plan generates from the filled survey`, priced.err.slice(0, 100));
      if (mode !== 'New Build') {
        const vent = await p.evaluate(() => {
          const sec = (BOQ.sections || []).find(x => /MECHANICAL EXTRACT VENTILATION \(MEV\)/.test(x.title));
          if (!sec) return null;
          const q = re => { const it = sec.items.find(i => re.test(i.description)); return it ? it.quantity : null; };
          return { terms: q(/Extract terminals/), inlets: q(/^Air inlets/) };
        });
        ok(vent && vent.terms === 1 && vent.inlets === 4, `[${tag}] ${mode}: MEV prices 1 extract for the wet room and 4 air inlets for the rest`, JSON.stringify(vent));
      }
      ok(errors.length === 0, `[${tag}] ${mode}: no page errors`, errors.join(' | ').slice(0, 200));
      ok(requests.length === 0, `[${tag}] ${mode}: nothing sent from the page while reading and pricing`, requests.slice(0, 3).join(' '));
      await p.close();
    }
  }

  // a change of project type clears the survey but keeps the report, ready to fill again
  {
    const p = await b.newPage();
    const errors = []; p.on('pageerror', e => errors.push(e.message)); p.on('dialog', d => d.accept());
    await p.goto(APP); await p.waitForTimeout(500);
    await p.evaluate(() => selectProjectType('New Build'));
    await p.setInputFiles('#ddr-panel input[type=file]', files[0]);
    await p.waitForFunction(() => /Additional survey counts/.test(document.getElementById('ddr-result').textContent), null, { timeout: 60000 });
    await p.evaluate(() => selectProjectType('Energy Upgrade'));
    const btn = await p.evaluate(() => (document.querySelector('#ddr-result .ddr-go') || {}).textContent || '');
    ok(/Fill the Energy Upgrade survey/.test(btn), '[type change] the report waits to fill the new project type', btn);
    await p.click('#ddr-result .ddr-go');
    const refilled = await p.evaluate(() => document.querySelectorAll('[id^="fc-t1-area-"]').length > 0 && !!document.getElementById('eu-hli').value);
    ok(refilled, '[type change] filling again works');
    ok(errors.length === 0, '[type change] no page errors', errors.join(' | '));
    await p.close();
  }

  await b.close();
  console.log(`\n==== ${steps} steps, ${fail} FAIL ====`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
