// The home screen, step 1 of document 05: the three project types.
//
// This used to be a hand-made capture that went stale the moment the home screen changed —
// it still showed the old strapline and no dwelling details report panel. It is framed to
// the question and the three cards, because the panel below them is step 2's own figure.
//
//   node pack/shot_home.js     →  pack/app_home.png
const { chromium } = require('playwright');
const path = require('path');
const url = require('url');

const APP = url.pathToFileURL(path.resolve(__dirname, '..', 'ber_build_planner.html')).href;

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME });
  const p = await b.newPage({ viewport: { width: 1420, height: 1020 }, deviceScaleFactor: 2 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('dialog', d => d.accept());
  await p.goto(APP);
  await p.waitForTimeout(500);
  // Energy Upgrade, because the rest of the journey in this document is an energy upgrade
  await p.click('#card-upgrade');
  await p.evaluate(() => {
    document.querySelectorAll('[id^="demo-btn-"]').forEach(b => { b.style.display = 'none'; });
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
  });
  await p.waitForTimeout(300);
  const box = await p.evaluate(() => {
    const cards = document.getElementById('card-upgrade').getBoundingClientRect();
    return { bottom: cards.bottom };
  });
  await p.screenshot({ path: path.join(__dirname, 'app_home.png'), clip: { x: 0, y: 0, width: 1420, height: Math.round(box.bottom + 22) } });
  console.log('wrote app_home.png · page errors:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
