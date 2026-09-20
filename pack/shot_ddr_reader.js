// The Dwelling Details Report reader, for document 05.
//
// Two screens: the report read on the home screen with the survey counts it asks for, and
// the Roof tab it filled. The report read is pack/sample_dwelling_report.pdf — the pack's own
// Westport example, written by make_sample_report.js, so no client's file appears in a
// document that leaves the office.
//
//   node pack/make_sample_report.js && node pack/shot_ddr_reader.js
const { chromium } = require('playwright');
const path = require('path');
const url = require('url');

const APP = url.pathToFileURL(path.resolve(__dirname, '..', 'ber_build_planner.html')).href;
const REPORT = path.join(__dirname, 'sample_dwelling_report.pdf');

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  const errs = [];
  const p = await b.newPage({ viewport: { width: 1420, height: 1020 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => errs.push(e.message));
  p.on('dialog', d => d.accept());
  await p.goto(APP);
  await p.evaluate(() => { window.print = () => {}; });
  await p.waitForTimeout(500);

  await p.click('#card-upgrade');
  await p.setInputFiles('#ddr-panel input[type=file]', REPORT);
  await p.waitForFunction(() => /Additional survey counts/.test(document.getElementById('ddr-result').textContent), null, { timeout: 60000 });

  // the counts the report cannot give, as the assessor takes them off the survey
  const fill = async (target, value) => {
    const el = await p.$(`#ddr-result input[data-ddr-target="${target}"]`);
    if (el) await el.fill(value);
  };
  for (const box of await p.$$('#ddr-result input[data-ddr-target^="fc-t5r-total-"]')) await box.fill('6');
  await fill('t5-bathsWhole', '1');
  await fill('t5-kitchens', '1');
  await fill('t5-utilities', '1');
  for (const box of await p.$$('#ddr-result input[data-ddr-target*="perim"]')) await box.fill('46');
  await fill('t3-gablePeaks', '2');
  // the example loaders are an internal convenience, not part of the assessor's journey
  await p.evaluate(() => {
    document.querySelectorAll('[id^="demo-btn-"]').forEach(b => { b.style.display = 'none'; });
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
  });
  await p.waitForTimeout(300);
  await p.locator('#ddr-panel').screenshot({ path: path.join(__dirname, 'app_ddr.png') });

  // and the tab it filled: the roof, where each element keeps its own card and caption
  await p.evaluate(() => {
    openProjectSections(); switchTab(3);
    // the status rail floats over the tab; it has its own screen elsewhere in this document
    const rail = document.getElementById('preview-rail');
    if (rail) rail.style.display = 'none';
  });
  await p.waitForTimeout(500);
  await p.locator('#tab-3').screenshot({ path: path.join(__dirname, 'app_ddr_tabs.png') });

  const read = await p.evaluate(() => {
    const S = window._ddrState, r = S.report;
    return {
      site: document.getElementById('t0-projName').value,
      county: document.getElementById('t0-county').value,
      hli: document.getElementById('eu-hli').value,
      cylinder: (document.getElementById('t0-ddrCylinder') || {}).value,
      roofs: r.roofs.rows.map(x => x.kind + ' ' + x.area).join(', '),
      filled: S.filled.length,
      flags: S.flags,
    };
  });
  console.log('read from the sample report:', JSON.stringify(read));
  console.log('page errors:', errs.length ? errs : 'none');
  await p.close();
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
