// Rate Settings tabs for document 07. The argument there is governance, not a rate
// catalogue: named sources, dated versions, every figure visible and overridable. These
// are the tabs that show that, captured from the live app.
const { chromium } = require('playwright');
const TABS = [['Labour Rates','app_rates.png',820], ['EU Rates','app_eurates.png',980],
              ['Regional Multipliers','app_regional.png',760]];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [tab, out, h] of TABS) {
    const p = await b.newPage({ viewport:{width:1240, height:h}, deviceScaleFactor:2 });
    p.on('pageerror', e => console.log('ERR', tab, e.message));
    await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
    await p.waitForTimeout(500);
    await p.evaluate(() => { toggleMatOverlay(); });
    await p.waitForTimeout(350);
    const hit = await p.evaluate(t => {
      const btn = [...document.querySelectorAll('.mdb-tab-btn')].find(x => x.textContent.trim() === t);
      if (btn) { btn.click(); return true; } return false;
    }, tab);
    if (!hit) { console.log('TAB NOT FOUND:', tab); await p.close(); continue; }
    await p.waitForTimeout(450);
    await p.screenshot({ path: __dirname + '/' + out });
    console.log('captured', tab, '->', out);
    await p.close();
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
