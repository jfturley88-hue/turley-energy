// The one screenshot in the pack that cannot be taken headlessly: Chrome's own print
// preview is browser chrome, not page content, so Playwright's screenshot API never sees
// it. Launch a headed Chromium on an Xvfb display instead, let the app call window.print()
// for real, and grab the whole X screen from outside the browser.
//
// This shot carries a caption promising it is unedited, so it has to be the real dialog
// over the real document — no compositing, no retouching.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');

const CFG = {
  addr: '3 Bed Semi, Mullingar, Co. Westmeath', dwelling: 'Semi-Detached', county: 'Westmeath',
  scheme: 'beh', ber: ['D', 'A'], age: '1983–1993', floor: [110, 34, '2.4'], wall: 90,
  roofs: [['ceiling', 55]], win: [12, 17], doors: 2, baths: 1, ensuites: 1,
  measures: ['eu-cavity', 'eu-roof-ceiling', 'eu-windows', 'eu-doors', 'eu-ashp', 'eu-hw-cyl', 'eu-dmev'],
  atticType: 'mw-200-topup', cavityType: 'bonded-bead', cavityWidth: '50', glazing: 'double', hli: 2.2,
};

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    headless: false,
    args: ['--no-sandbox', '--window-size=1560,1160', '--window-position=0,0'],
  });
  const p = await b.newPage({ viewport: { width: 1560, height: 1000 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file:///home/user/turley-energy/ber_build_planner.html');
  await p.waitForTimeout(600);
  await p.evaluate(c => {
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
    s('t5-bathrooms', c.baths); s('t5-ensuites', c.ensuites);
    if (typeof mirrorDynamicToLegacy === 'function') mirrorDynamicToLegacy();
    c.measures.forEach(ck);
    s('eu-roof-ceiling-type', c.atticType); s('eu-cavity-type', c.cavityType);
    s('eu-cavity-width', c.cavityWidth); s('eu-windows-glazing', c.glazing);
    if (typeof euAutoHLI === 'function') euAutoHLI();
    s('eu-hli', c.hli); s('eu-hli-source', 'ber');
    if (typeof euUpdateHeatLoad === 'function') euUpdateHeatLoad();
    if (typeof euAutoFinish === 'function') euAutoFinish();
    openProjectSections();
  }, CFG);
  await p.waitForTimeout(700);
  await p.evaluate(() => generate());
  await p.waitForTimeout(2000);
  const t = await p.evaluate(() => { const T = planTotals(BOQ); return T.totalEst + '/' + T.net; });
  console.log('plan on screen:', t);

  // Real print, real dialog. window.print() is NOT stubbed here.
  p.evaluate(() => exportEUPDF('detailed')).catch(() => {});
  await p.waitForTimeout(9000);

  // Grab the whole virtual screen, then trim the letterboxing the X root leaves around the
  // browser window. Detected rather than hardcoded, so a different window size still crops
  // to the window and not to a guess.
  execFileSync('python3', ['-c', `
from PIL import Image, ImageGrab
im = ImageGrab.grab(xdisplay=':99').convert('RGB')
w, h = im.size
px = im.load()
# The X root shows as black; the window manager also leaves a uniform strip along the
# bottom edge. Trim both: anything near-black, and any trailing run of one flat colour.
def row_dark(y): return all(sum(px[x, y]) < 40 for x in range(0, w, 12))
def col_dark(x): return all(sum(px[x, y]) < 40 for y in range(0, h, 12))
SCROLLBAR = 15  # the page's own horizontal scrollbar, a grey band along the window's foot
r = h
while r > 1 and row_dark(r - 1): r -= 1
r -= SCROLLBAR
c = w
while c > 1 and col_dark(c - 1): c -= 1
im = im.crop((0, 0, c, r))
im.save('${__dirname}/app_preview_dialog.png')
print('captured', im.size)
`], { stdio: 'inherit' });

  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
