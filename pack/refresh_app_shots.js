// Regenerate the doc-04 app screenshots from the live engine. They had drifted badly:
// captured while contingency was still in the loading, so they showed €58,966 / €35,696
// against a current Westport price of €51,169 / €29,499, under a caption that reads
// "live software, unedited". The selector shot also still offered "Window reveal liners
// & internal sills" as a tickable measure, which has since moved to the not-included
// catalogue. Same project and framing as before — only the figures move.
const { chromium } = require('playwright');
const OUT = __dirname;

const WESTPORT = {
  addr: 'Carrowbeg, Westport, Co. Mayo', dwelling: 'Bungalow', county: 'Mayo', scheme: 'beh',
  ber: ['E', 'A'], age: '1978–1982', floor: [118, 46, '2.4'], wall: 108,
  roofs: [['ceiling', 70], ['rafter', 48]], win: [11, 19], doors: 2,
  measures: ['eu-cavity','eu-roof-ceiling','eu-roof-rafter','eu-windows','eu-ashp','eu-hw-cyl','eu-mvhr','eu-pv'],
};

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

const fresh = async (b, w, h) => {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
  await p.evaluate(() => { window.print = () => {}; });
  await p.waitForTimeout(400);
  return p;
};

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const errs = [];

  // 2 · the survey screen — project tab with the status sidebar filled
  let p = await fresh(b, 1240, 780);
  p.on('pageerror', e => errs.push('selector: ' + e.message));
  await build(p, WESTPORT);
  await p.waitForTimeout(700);
  await p.evaluate(() => switchTab(0));
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/app_selector.png' });
  const measures = await p.evaluate(() =>
    [...document.querySelectorAll('#status-measures li, .status-measure')].map(x => x.textContent.trim()));
  await p.close();

  // 3 · the grant route strip, and 4 · the plan on screen — one build, two frames
  p = await fresh(b, 1240, 780);
  p.on('pageerror', e => errs.push('plan: ' + e.message));
  await build(p, WESTPORT);
  await p.waitForTimeout(600);
  await p.evaluate(() => generate());
  await p.waitForTimeout(1600);
  const totals = await p.evaluate(() => {
    const t = planTotals(BOQ);
    return { total: t.totalEst, grants: t.grantTotal, net: t.net,
             header: (document.getElementById('rpt-total') || {}).textContent,
             sub: (document.getElementById('rpt-total-sub') || {}).textContent };
  });

  const strip = await p.$('.plan-routes-wrap');
  if (strip) await strip.screenshot({ path: OUT + '/app_routes.png' });
  else errs.push('route strip not found');

  // the plan table, framed from its total header down, as before
  await p.evaluate(() => {
    const h = document.getElementById('rpt-total');
    if (h) h.scrollIntoView({ block: 'start' });
    // back off far enough to keep the "TOTAL BUDGET GUIDE" label above the figure
    const sc = document.scrollingElement || document.documentElement;
    sc.scrollTop = Math.max(0, sc.scrollTop - 34);
    let n = h && h.parentElement;
    while (n) { if (n.scrollHeight > n.clientHeight) n.scrollTop = Math.max(0, n.scrollTop - 34); n = n.parentElement; }
  });
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/app_plan.png' });
  await p.close();

  console.log('westport now  :', JSON.stringify(totals));
  console.log('measures shown:', measures.length ? measures.join(' | ') : '(sidebar list not matched)');
  console.log('page errors   :', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
