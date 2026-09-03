const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport:{width:820,height:1160}, deviceScaleFactor:1.6 });
  await p.goto('file://' + __dirname + '/pack_01.html'); await p.waitForTimeout(800);
  await (await p.$('.sheet')).screenshot({ path: __dirname + '/_v1.png' });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
