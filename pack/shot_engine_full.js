// The whole EU Rates tab, top to bottom, for document 07. The Rate Settings panel is a
// fixed, scrolling overlay, so a viewport screenshot shows a window onto it and nothing
// more. Here the overlay is let grow to its content and captured in one frame, then cut
// into page-sized slices on section boundaries so nothing is split mid-table.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport:{width:1240, height:900}, deviceScaleFactor:2 });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
  await p.waitForTimeout(500);
  await p.evaluate(() => toggleMatOverlay());
  await p.waitForTimeout(300);
  await p.evaluate(() => { const btn=[...document.querySelectorAll('.mdb-tab-btn')].find(x=>x.textContent.trim()==='EU Rates'); btn.click(); });
  await p.waitForTimeout(500);
  // Let the overlay grow to its content so one element screenshot holds all of it.
  const dims = await p.evaluate(() => {
    const o = document.getElementById('mat-overlay');
    o.style.position = 'absolute'; o.style.top = '0'; o.style.height = 'auto';
    o.style.maxHeight = 'none'; o.style.overflow = 'visible';
    document.body.style.overflow = 'visible';
    return { h: o.scrollHeight, w: o.scrollWidth };
  });
  await p.setViewportSize({ width: 1240, height: dims.h + 40 });
  await p.waitForTimeout(400);
  // Section heads inside the EU tab, with their y positions in page pixels.
  const heads = await p.evaluate(() => {
    const o = document.getElementById('mat-overlay');
    const oy = o.getBoundingClientRect().top + window.scrollY;
    const out = [];
    for (const e of o.querySelectorAll('*')) {
      if (e.children.length > 2) continue;
      const t = (e.textContent || '').trim();
      if (t.length < 4 || t.length > 70) continue;
      const cs = getComputedStyle(e);
      if (!(cs.fontWeight === '700' || parseInt(cs.fontWeight) >= 600)) continue;
      if (!/\(|Variations|CATEGORY|RATE OVERRIDES|Roof|Floor|Windows|Doors|Solar|Heat|Vent|Wall/i.test(t)) continue;
      const r = e.getBoundingClientRect();
      if (r.height === 0 || r.width === 0) continue;
      out.push({ t: t.replace(/\s+/g,' ').slice(0,60), y: Math.round(r.top + window.scrollY - oy) });
    }
    out.sort((a,b)=>a.y-b.y);
    return out.filter((h,i)=> i===0 || h.y - out[i-1].y > 8);
  });
  await (await p.$('#mat-overlay')).screenshot({ path: __dirname + '/app_eurates_full.png' });
  fs.writeFileSync(__dirname + '/app_eurates_heads.json', JSON.stringify({ height: dims.h, heads }, null, 1));
  console.log('captured', dims.w + 'x' + dims.h, 'css px;', heads.length, 'section heads');
  heads.forEach(h => console.log(String(h.y).padStart(5), h.t));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
