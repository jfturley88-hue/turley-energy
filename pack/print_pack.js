const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const n of ['01','02','03','04','05','06']) {
    const p = await b.newPage();
    await p.goto('file://' + __dirname + '/pack_' + n + '.html');
    await p.waitForTimeout(700);
    const fit = await p.evaluate(() => [...document.querySelectorAll('.sheet')].map((sh,i) =>
      ({ pg:i+1, over: sh.scrollHeight - sh.clientHeight })));
    const bad = fit.filter(f=>f.over>0);
    console.log('pack_'+n, bad.length ? 'OVERFLOW '+JSON.stringify(bad) : 'fits ('+fit.length+' pages)');
    await p.pdf({ path: __dirname + '/pack_' + n + '_print.pdf', preferCSSPageSize: true, printBackground: true });
    await p.close();
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
