// The one worked example, printed exactly as the app prints it: the full detailed Cost
// Plan and the blank Contractor Pricing Schedule for the same house.
//
// A semi-detached house on Better Energy Homes — the route most retrofits actually take —
// with the measure set agreed for the pack: attic insulation, windows & external doors,
// air-to-water heat pump with its cylinder, and decentralised ventilation. The HLI is set
// as it would be in practice: read off the provisional BER (2.2 W/m²K, inside the ≤2.3
// heat-pump grant threshold), not the indicative seed.
const { chromium } = require('playwright');
const OUT = __dirname;

const HOUSES = {
  ex: { addr: '3 Bed Semi, Mullingar, Co. Westmeath', dwelling: 'Semi-Detached', county: 'Westmeath',
        scheme: 'beh', ber: ['D', 'A'], age: '1983–1993', floor: [110, 34, '2.4'], wall: 90,
        roofs: [['ceiling', 55]], win: [12, 17], doors: 2, baths: 1, ensuites: 1,
        measures: ['eu-cavity', 'eu-roof-ceiling', 'eu-windows', 'eu-doors', 'eu-ashp', 'eu-hw-cyl', 'eu-dmev'],
        // Attic is a top-up over existing quilt, the cavity is a 50mm bonded-bead pump, and
        // the windows are double-glazed — the specification the reviewer marked up.
        atticType: 'mw-200-topup', cavityType: 'bonded-bead', cavityWidth: '50', glazing: 'double',
        hli: 2.2 },
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
  if (c.baths != null)   s('t5-bathrooms', c.baths);
  if (c.ensuites != null) s('t5-ensuites', c.ensuites);
  if (typeof mirrorDynamicToLegacy === 'function') mirrorDynamicToLegacy();
  c.measures.forEach(ck);
  if (c.gables) { const g = document.getElementById('eu-ewi-peaks'); if (g) { g.value = c.gables; g.dispatchEvent(new Event('change')); } }
  if (c.atticType)   s('eu-roof-ceiling-type', c.atticType);
  if (c.cavityType)  s('eu-cavity-type',  c.cavityType);
  if (c.cavityWidth) s('eu-cavity-width', c.cavityWidth);
  if (c.glazing)     s('eu-windows-glazing', c.glazing);
  if (typeof euAutoHLI === 'function') euAutoHLI();
  // The provisional BER figure, entered as an assessor would enter it
  if (c.hli) { s('eu-hli', c.hli); s('eu-hli-source', 'ber'); if (typeof euUpdateHeatLoad === 'function') euUpdateHeatLoad(); }
  if (typeof euAutoFinish === 'function') euAutoFinish();
  openProjectSections();
}, cfg);

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [key, cfg] of Object.entries(HOUSES)) {
    for (const [doc, trigger] of [['plan', 'exportEUPDF'], ['appx', 'exportEUAppendix'], ['sched', 'exportContractorSchedule']]) {
      const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
      p.on('pageerror', e => console.log('ERR', key, e.message));
      await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
      await p.evaluate(() => { window.print = () => {}; });
      await p.waitForTimeout(400);
      await build(p, cfg);
      await p.waitForTimeout(500);
      await p.evaluate(() => generate());
      await p.waitForTimeout(1400);
      if (doc === 'plan') {
        // the figures the pack prose quotes, straight from the same build the PDF prints
        const t = await p.evaluate(() => {
          // planTotals() is the single source of truth — the same call the printed Cost
          // Plan prices from. BOQ.summary's cost fields are the older flat-13.5% path:
          // they overcharge VAT on the 9% heat pump and omit the post-works BER, which
          // is why the pack once quoted 35,945 against a plan that printed 35,700.
          const T = planTotals(BOQ);
          const grants = (BOQ && BOQ.grants || []).map(g => g.description + ': ' + (g.amount || 0));
          const heat = (BOQ.sections || []).find(s => /AIR-TO-WATER/.test(s.title));
          const hp = heat && heat.items.find(i => /heat pump \(/.test(i.description));
          return { total: T.totalEst, works: T.works, ber: T.berCost, grants: T.grantTotal, net: T.net, list: grants, hp: hp && hp.description };
        });
        console.log(key, 'figures:', JSON.stringify(t, null, 1));
      }
      await p.evaluate(t => t === 'exportEUPDF' ? exportEUPDF('detailed')
                        : t === 'exportEUAppendix' ? exportEUPDF('appendix')
                        : exportContractorSchedule(), trigger);
      await p.waitForTimeout(900);
      // the pack is portrait; print these documents portrait too (the app's own
      // narrow-page fallback keeps the figures from breaking mid-number)
      await p.addStyleTag({ content: '@media print { @page { size: A4 portrait; margin: 10mm 12mm 14mm 12mm; } }' });
      await p.pdf({ path: OUT + '/' + key + '_' + doc + '.pdf', preferCSSPageSize: true, printBackground: true });
      await p.close();
    }
    console.log(key, 'plan + schedule printed');
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
