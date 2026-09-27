// The print-preview figure, captured on Windows.
//
// Same job as shot_preview.js and the same rule: Chrome's print preview is browser chrome,
// not page content, so no headless screenshot API can see it, and the caption promises the
// figure is unedited — it has to be the real dialog over the real document, never composited.
// shot_preview.js does this on an Xvfb display; this one drives a headed Chrome on the
// Windows desktop and grabs the screen.
//
// The app is served over 127.0.0.1 rather than opened from disk, so the address bar shows
// a neutral URL instead of the folder the repository happens to sit in.
//
//   node pack/shot_preview_win.js     →  pack/app_preview_dialog.png
//
// A Chrome window opens on the desktop for about fifteen seconds. Leave it alone while it
// works — anything covering it lands in the capture.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const APP = path.resolve(__dirname, '..', 'ber_build_planner.html');
const PORT = 8099;
const W = 1536, H = 960;   // the desktop this is captured on
const PY = process.env.PYTHON || 'python';

const CFG = {
  addr: '3 Bed Semi, Mullingar, Co. Westmeath', dwelling: 'Semi-Detached', county: 'Westmeath',
  scheme: 'beh', ber: ['D', 'A'], age: '1983–1993', floor: [110, 34, '2.4'], wall: 90,
  roofs: [['ceiling', 55]], win: [12, 17], doors: 2, baths: 1, ensuites: 1,
  measures: ['eu-cavity', 'eu-roof-ceiling', 'eu-windows', 'eu-doors', 'eu-ashp', 'eu-hw-cyl', 'eu-dmev'],
  atticType: 'mw-200-topup', cavityType: 'bonded-bead', cavityWidth: '50', glazing: 'double', hli: 2.2,
};

(async () => {
  const html = fs.readFileSync(APP);
  const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
  });
  await new Promise(r => server.listen(PORT, '127.0.0.1', r));

  const b = await chromium.launch({
    executablePath: process.env.CHROME,
    headless: false,
    args: [`--window-size=${W},${H}`, '--window-position=0,0'],
  });
  const p = await b.newPage({ viewport: null });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto(`http://127.0.0.1:${PORT}/planitber.html`);
  await p.waitForTimeout(700);
  await p.evaluate(c => {
    selectProjectType('Energy Upgrade');
    const s = (i, v) => { const e = document.getElementById(i); if (e) e.value = v; };
    const ck = i => { const e = document.getElementById(i); if (e && !e.checked) { e.checked = true; e.dispatchEvent(new Event('change')); } };
    s('t0-projName', c.addr); s('t0-dwellingType', c.dwelling);
    s('t0-county', c.county); s('t0-grantScheme', c.scheme);
    s('eu-currentBER', c.ber[0]); s('eu-targetBER', c.ber[1]); s('eu-ageBand', c.age);
    addFloorCard(); s('fc-t1-area-1', c.floor[0]); s('fc-t1-perim-1', c.floor[1]); s('fc-t1-height-1', c.floor[2]);
    addWallCard(); s('fc-t2-area-1', c.wall);
    c.roofs.forEach((r, i) => { addRoofCard(); s('fc-t3-type-' + (i + 1), r[0]); s('fc-t3-area-' + (i + 1), r[1]); });
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
  console.log('plan on screen:', await p.evaluate(() => { const T = planTotals(BOQ); return T.totalEst + '/' + T.net; }));

  // Real print, real dialog. window.print() is NOT stubbed here.
  p.evaluate(() => exportEUPDF('detailed')).catch(() => {});
  await p.waitForTimeout(9000);

  // Grab the desktop, then cut the taskbar. The window fills the screen, so the browser ends
  // at the foot of the work area — read from the system rather than guessed, and scaled by
  // the capture's own size because the desktop may be running at 125%.
  //
  // A capture that is one flat colour means this process cannot see the signed-in screen (a
  // service or a remote session). Say so and leave the existing figure alone rather than
  // writing a blank one over it.
  execFileSync(PY, ['-c', `
import ctypes, sys
from PIL import ImageGrab
class R(ctypes.Structure):
    _fields_ = [('l', ctypes.c_long), ('t', ctypes.c_long), ('r', ctypes.c_long), ('b', ctypes.c_long)]
wa = R()
ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(wa), 0)
im = ImageGrab.grab().convert('RGB')
if im.getcolors(2):
    sys.exit('the desktop is not visible to this process - run this from your own terminal, signed in at the screen')
scale = im.width / ctypes.windll.user32.GetSystemMetrics(0)
im = im.crop((0, 0, min(im.width, int(${W} * scale)), min(im.height, int(wa.b * scale))))
im.save(r'${path.join(__dirname, 'app_preview_dialog.png').replace(/\\/g, '\\\\')}')
print('captured', im.size)
`], { stdio: 'inherit' });

  await b.close();
  server.close();
})().catch(e => { console.error(e); process.exit(1); });
