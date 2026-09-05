const { chromium } = require('playwright');
const APP = 'file://' + require('path').resolve(__dirname, '..', '..', 'ber_build_planner.html');
const EXE = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const T = p => p.evaluate(() => { const t = planTotals(BOQ); return t.totalEst; });
const gen = async (p, wait=1800) => { await p.evaluate(() => generate()); await p.waitForTimeout(wait); };
const snapInputs = p => p.evaluate(() => { const o={}; document.querySelectorAll('input,select,textarea').forEach(e=>{ if(!e.id) return; o[e.id] = e.type==='checkbox' ? (e.checked?'☑':'☐') : e.value; }); return o; });
(async () => {
  const out = {};
  // (a) three separate launches, identical steps
  for (let i=0;i<3;i++) { const b = await chromium.launch({ executablePath: EXE }); const p = await b.newPage(); await p.goto(APP); await p.evaluate(()=>{window.print=()=>{}}); await p.waitForTimeout(500);
    await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); out['launch'+i] = await T(p); await b.close(); }
  const b = await chromium.launch({ executablePath: EXE });
  // (b) same page: generate twice; (c) long wait before generate; (d) example loaded twice
  let p = await b.newPage(); await p.goto(APP); await p.evaluate(()=>{window.print=()=>{}}); await p.waitForTimeout(500);
  await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await p.waitForTimeout(3000); await gen(p); out.longWait = await T(p);
  await gen(p); out.genTwice = await T(p);
  await p.evaluate(() => loadEUExample1()); await gen(p); out.exampleTwice = await T(p);
  const cleanInputs = await snapInputs(p);
  await p.close();
  // (e) NB first, goHome, then EU -- and diff every input against the clean EU load
  p = await b.newPage(); await p.goto(APP); await p.evaluate(()=>{window.print=()=>{}}); await p.waitForTimeout(500);
  await p.evaluate(() => { selectProjectType('New Build'); loadNewBuildExample(); }); await gen(p);
  await p.evaluate(() => goHome()); await p.waitForTimeout(300);
  await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); out.afterNB = await T(p);
  const leakedInputs = await snapInputs(p);
  const diffs = [];
  for (const k of new Set([...Object.keys(cleanInputs), ...Object.keys(leakedInputs)])) if (cleanInputs[k] !== leakedInputs[k]) diffs.push(`${k}: clean=${JSON.stringify(cleanInputs[k])} afterNB=${JSON.stringify(leakedInputs[k])}`);
  // section-level diff of the BOQ too
  const secsAfter = await p.evaluate(() => (BOQ.sections||[]).map(s=>[s.title, Math.round(s.subtotal||0)]));
  await p.close();
  p = await b.newPage(); await p.goto(APP); await p.evaluate(()=>{window.print=()=>{}}); await p.waitForTimeout(500);
  await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p);
  const secsClean = await p.evaluate(() => (BOQ.sections||[]).map(s=>[s.title, Math.round(s.subtotal||0)]));
  const lsKeys = await p.evaluate(() => Object.keys(localStorage));
  await b.close();
  console.log('TOTALS', JSON.stringify(out));
  console.log('localStorage keys in a fresh launch:', JSON.stringify(lsKeys));
  console.log('\nINPUT DIFFS after NB session (' + diffs.length + '):'); diffs.slice(0,40).forEach(d => console.log('  ' + d));
  console.log('\nSECTION DIFFS:'); const m = Object.fromEntries(secsClean);
  for (const [t,v] of secsAfter) if (m[t] !== v) console.log(`  ${t}: clean=${m[t]} afterNB=${v}`);
  for (const [t,v] of secsClean) if (!secsAfter.find(x=>x[0]===t)) console.log(`  ${t}: clean=${v} afterNB=(missing)`);
})().catch(e => { console.error('CRASH', e); process.exit(1); });
