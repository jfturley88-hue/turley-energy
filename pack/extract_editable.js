// Pull every editable prose block out of the rendered pack pages, tagged, so the text can
// be edited in Word and put back in the right slot. Page furniture (page numbers, the
// PlanitBER wordmark, the running crumb) and images are deliberately left out.
const { chromium } = require('playwright');
const fs = require('fs');

const DOCS = [
  ['01', 'The Value Proposition'],
  ['02', 'The Cost Plan — notes page'],
  ['03', 'The Pricing Schedule — notes page'],
  ['04', 'The Appendix — notes page'],
  ['05', 'The Workflow'],
  ['06', 'The Software'],
  ['07', 'The Engine'],
];

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [n, title] of DOCS) {
    const p = await b.newPage();
    await p.goto('file://' + process.cwd() + '/pack_' + n + '.html');
    await p.waitForTimeout(600);
    const blocks = await p.evaluate(() => {
      const SEL = 'h1, h2, p, li, .pt-t, .pt-b, .stept, .stepb, .ac, .cap, .at, .ab, .dt, .db, ' +
                  '.nv, .nl, .kick, .fine, .tlh, .tl, .rt, .rr, .exhead, .exsub, .doct, .docb, .who .wt, .who .wb, .wft, .wfb';
      const SKIP = ['pageno', 'nextdoc', 'crumb', 'word'];
      const all = [...document.querySelectorAll(SEL)]
        .filter(e => !SKIP.some(c => e.classList.contains(c)))
        .filter(e => !e.closest('.pageno, .nextdoc, .strip'));
      // keep only the innermost captured element for any nested pair
      const set = new Set(all);
      const leaves = all.filter(e => !all.some(o => o !== e && set.has(o) && e.contains(o)));
      return leaves.map((e, i) => {
        const sheet = e.closest('.sheet');
        const pageNo = sheet ? [...document.querySelectorAll('.sheet')].indexOf(sheet) + 1 : 0;
        return {
          page: pageNo,
          html: e.innerHTML.replace(/\s+/g, ' ').trim(),
          text: (e.innerText || '').replace(/\s+/g, ' ').trim(),
          kind: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : ''),
        };
      }).filter(x => x.text.length > 2);
    });
    out[n] = { title, blocks: blocks.map((x, i) => Object.assign({ tag: n + '.' + (i + 1) }, x)) };
    console.log('doc ' + n + ' (' + title + '): ' + blocks.length + ' editable blocks');
    await p.close();
  }
  fs.writeFileSync('editable_map.json', JSON.stringify(out, null, 1));
  console.log('\nwrote editable_map.json');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
