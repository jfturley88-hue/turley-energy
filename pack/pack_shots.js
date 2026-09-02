// Every image the 5-PDF pack needs, captured from the live app at rate book v2026.2
// with the flipped Difference colours. Westport is built exactly as routes_check builds
// it (openProjectSections included) so the figures match the canonical totals.
const { chromium } = require('playwright');
const OUT = __dirname;

const build = (p, cfg) => p.evaluate(c => {
  selectProjectType('Energy Upgrade');
  const s = (i, v) => { const e = document.getElementById(i); if (e) e.value = v; };
  const ck = i => { const e = document.getElementById(i); if (e && !e.checked) { e.checked = true; e.dispatchEvent(new Event('change')); } };
  s('t0-projName', c.addr); s('t0-dwellingType', c.dwelling);
  s('t0-county', c.county); s('t0-grantScheme', c.scheme);
  s('eu-currentBER', c.ber[0]); s('eu-targetBER', c.ber[1]); s('eu-ageBand', c.age);
  addFloorCard(); s('fc-t1-area-1', c.floor[0]); s('fc-t1-perim-1', c.floor[1]); s('fc-t1-height-1', c.floor[2]);
  addWallCard(); s('fc-t2-area-1', c.wall);
  c.roofs.forEach((r, i) => { addRoofCard(); s('fc-t3-type-' + (i+1), r[0]); s('fc-t3-area-' + (i+1), r[1]); });
  addWindowCard(); s('fc-t4-count-1', c.win[0]); s('fc-t4-area-1', c.win[1]); s('t4-doorCount', c.doors);
  if (typeof mirrorDynamicToLegacy === 'function') mirrorDynamicToLegacy();
  c.measures.forEach(ck);
  if (typeof euAutoHLI === 'function') euAutoHLI();
  if (typeof euAutoFinish === 'function') euAutoFinish();
  openProjectSections();
}, cfg);

const WESTPORT = {
  addr: 'Carrowbeg, Westport, Co. Mayo', dwelling: 'Bungalow', county: 'Mayo', scheme: 'beh',
  ber: ['E', 'A'], age: '1978–1982', floor: [118, 46, '2.4'], wall: 108,
  roofs: [['ceiling', 70], ['rafter', 48]], win: [11, 19], doors: 2,
  measures: ['eu-cavity','eu-roof-ceiling','eu-roof-rafter','eu-windows','eu-ashp','eu-hw-cyl','eu-mvhr','eu-pv'],
};
const KILDARE = {
  addr: '2 Meadow Court, Naas, Co. Kildare', dwelling: 'Semi-Detached', county: 'Kildare', scheme: 'oss',
  ber: ['D1', 'B2'], age: '1994–1999', floor: [92, 34, '2.5'], wall: 78,
  roofs: [['ceiling', 92]], win: [9, 14], doors: 2,
  measures: ['eu-cavity','eu-roof-ceiling','eu-windows','eu-pv'],
};

const fresh = async (b, w, h) => {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
  await p.evaluate(() => { window.print = () => {}; });
  await p.waitForTimeout(400);
  return p;
};

// Trim the detailed export to its first page and scale into an A4 box.
const trimToPage1 = p => p.evaluate(() => {
  const root = document.getElementById('pdf-print-view');
  let hiding = false;
  Array.from(root.children).forEach(c => {
    if (hiding || /How Your Estimate Was Calculated|Appendix — Itemised/.test(c.textContent || '')) {
      c.style.display = 'none'; hiding = true;
    }
  });
  Array.from(root.querySelectorAll('div')).forEach(d => {
    const t = (d.textContent || '').trim();
    if (/^Better Energy Homes — grants are paid/.test(t) || /^One Stop Shop —/.test(t) ||
        /^How to use this document/.test(t) || /^What this estimate includes/.test(t)) d.style.display = 'none';
  });
  const W = 860, H = Math.round(W / 0.707);
  const box = document.createElement('div'); box.id = '__fit';
  box.style.cssText = 'width:' + W + 'px;height:' + H + 'px;background:#fff;overflow:hidden;';
  root.parentNode.insertBefore(box, root); box.appendChild(root);
  root.style.background = '#fff'; root.style.width = W + 'px';
  const scale = Math.min(1, H / root.scrollHeight);
  root.style.transformOrigin = 'top left';
  root.style.transform = 'scale(' + scale + ')';
  root.style.width = (W / scale) + 'px';
});

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const errs = [];
  const totals = {};

  const planDoc = async (cfg, out, fill) => {
    const p = await fresh(b, 780, 1400);
    p.on('pageerror', e => errs.push(e.message));
    await build(p, cfg);
    await p.waitForTimeout(600); await p.evaluate(() => generate()); await p.waitForTimeout(1400);
    totals[out] = await p.evaluate(() => {
      const t = planTotals(BOQ);
      return { total: t.totalEst, grants: t.grantTotal, net: t.net };
    });
    if (fill) {
      await p.evaluate(entries => {
        const rows = Array.from(document.querySelectorAll('.eu-act-input'));
        const notes = Array.from(document.querySelectorAll('.eu-note-input'));
        entries.forEach(([idx, act, note]) => {
          if (rows[idx]) { rows[idx].value = act; rows[idx].dispatchEvent(new Event('input', { bubbles: true })); rows[idx].dispatchEvent(new Event('change', { bubbles: true })); }
          if (note && notes[idx]) { notes[idx].value = note; notes[idx].dispatchEvent(new Event('input', { bubbles: true })); notes[idx].dispatchEvent(new Event('change', { bubbles: true })); }
        });
      }, fill);
      await p.waitForTimeout(400);
    }
    await p.evaluate(() => exportEUPDF('detailed')); await p.waitForTimeout(900);
    await trimToPage1(p); await p.waitForTimeout(400);
    await (await p.$('#__fit')).screenshot({ path: OUT + '/' + out });
    await p.close();
  };

  const scheduleDoc = async (cfg, out) => {
    const p = await fresh(b, 1150, 1300);
    p.on('pageerror', e => errs.push(e.message));
    await build(p, cfg);
    await p.waitForTimeout(600); await p.evaluate(() => generate()); await p.waitForTimeout(1400);
    await p.evaluate(() => exportContractorSchedule()); await p.waitForTimeout(900);
    await p.evaluate(() => { const v = document.getElementById('pdf-print-view'); v.style.background = '#fff'; v.style.padding = '0 0 10px'; });
    await p.waitForTimeout(200);
    await (await p.$('#pdf-print-view')).screenshot({ path: OUT + '/' + out });
    await p.close();
  };

  // Westport — clean plan, live plan (actuals + notes with the new colours), schedule
  await planDoc(WESTPORT, 'shot_costplan.png');
  console.log('westport plan', JSON.stringify(totals['shot_costplan.png']));
  await planDoc(WESTPORT, 'shot_live.png', [
    [0, '2400', 'Quote from McHale Bros accepted'],
    [1, '3450', ''],
    [3, '11900', 'Upgraded to flush casement frames'],
    [4, '15400', 'Includes moving cylinder to hot press'],
  ]);
  await scheduleDoc(WESTPORT, 'shot_schedule.png');

  // Kildare — second worked example on One Stop Shop
  await planDoc(KILDARE, 'ex2_plan.png');
  console.log('kildare plan ', JSON.stringify(totals['ex2_plan.png']));
  await scheduleDoc(KILDARE, 'ex2_schedule.png');

  // Rate Settings — SEAI Grants tab
  const p = await fresh(b, 1240, 820);
  p.on('pageerror', e => errs.push(e.message));
  await p.evaluate(() => { toggleMatOverlay(); });
  await p.waitForTimeout(300);
  await p.evaluate(() => {
    const btns = [...document.querySelectorAll('.mdb-tab-btn')];
    const g = btns.find(x => x.textContent.trim() === 'SEAI Grants');
    if (g) g.click();
  });
  await p.waitForTimeout(300);
  await p.screenshot({ path: OUT + '/app_grants.png' });
  await p.close();

  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
