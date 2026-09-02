// The download bar on the report screen, showing the grant-route selector beside the three
// document buttons. Regenerated whenever that bar changes -- it sat stale once, showing two
// buttons next to text that said three.
const { chromium } = require('playwright');
const CFG = { addr:'3 Bed Semi, Mullingar, Co. Westmeath', dwelling:'Semi-Detached', county:'Westmeath',
  scheme:'beh', ber:['D','A'], age:'1983–1993', floor:[110,34,'2.4'], wall:90, roofs:[['ceiling',55]],
  win:[12,17], doors:2, baths:1, ensuites:1,
  measures:['eu-cavity','eu-roof-ceiling','eu-windows','eu-doors','eu-ashp','eu-hw-cyl','eu-dmev'],
  atticType:'mw-200-topup', cavityType:'bonded-bead', cavityWidth:'50', glazing:'double', hli:2.2 };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport:{width:1500,height:900}, deviceScaleFactor:2 });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
  await p.evaluate(() => { window.print = () => {}; });
  await p.waitForTimeout(400);
  await p.evaluate(c => {
    selectProjectType('Energy Upgrade');
    const s=(i,v)=>{const e=document.getElementById(i); if(e) e.value=v;};
    const ck=i=>{const e=document.getElementById(i); if(e&&!e.checked){e.checked=true;e.dispatchEvent(new Event('change'));}};
    s('t0-projName',c.addr); s('t0-dwellingType',c.dwelling); s('t0-county',c.county); s('t0-grantScheme',c.scheme);
    s('eu-currentBER',c.ber[0]); s('eu-targetBER',c.ber[1]); s('eu-ageBand',c.age);
    addFloorCard(); s('fc-t1-area-1',c.floor[0]); s('fc-t1-perim-1',c.floor[1]); s('fc-t1-height-1',c.floor[2]);
    addWallCard(); s('fc-t2-area-1',c.wall);
    c.roofs.forEach((r,i)=>{addRoofCard(); s('fc-t3-type-'+(i+1),r[0]); s('fc-t3-area-'+(i+1),r[1]);});
    addWindowCard(); s('fc-t4-count-1',c.win[0]); s('fc-t4-area-1',c.win[1]); s('t4-doorCount',c.doors);
    s('t5-bathrooms',c.baths); s('t5-ensuites',c.ensuites);
    if (typeof mirrorDynamicToLegacy==='function') mirrorDynamicToLegacy();
    c.measures.forEach(ck);
    s('eu-roof-ceiling-type',c.atticType); s('eu-cavity-type',c.cavityType);
    s('eu-cavity-width',c.cavityWidth); s('eu-windows-glazing',c.glazing);
    if (typeof euAutoHLI==='function') euAutoHLI();
    s('eu-hli',c.hli); s('eu-hli-source','ber'); if (typeof euUpdateHeatLoad==='function') euUpdateHeatLoad();
    if (typeof euAutoFinish==='function') euAutoFinish();
    openProjectSections();
  }, CFG);
  await p.waitForTimeout(600);
  await p.evaluate(() => generate());
  await p.waitForTimeout(1800);
  const bar = await p.$('#pdf-btn-wrap');
  const btns = await p.evaluate(() => [...document.querySelectorAll('#pdf-btn-wrap button')].map(b => b.textContent.trim()));
  console.log('buttons:', JSON.stringify(btns));
  await bar.screenshot({ path: __dirname + '/shot_routedl.png' });
  await p.close(); await b.close();
})().catch(e => { console.error(e); process.exit(1); });
