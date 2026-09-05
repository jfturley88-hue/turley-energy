const { chromium } = require('playwright');
const APP = 'file://' + require('path').resolve(__dirname, '..', '..', 'ber_build_planner.html');
const results = []; const log = m => { results.push(m); console.log(m); };
async function fresh(b, label) {
  const p = await b.newPage({ viewport: { width: 1300, height: 950 } }); const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|ERR_CONNECTION|Failed to load resource/.test(m.text())) errs.push('console.error: ' + m.text().slice(0, 200)); });
  await p.goto(APP); await p.evaluate(() => { window.print = () => {}; }); await p.waitForTimeout(500);
  return { p, errs, label };
}
async function step(ctx, name, fn) {
  const before = ctx.errs.length;
  try { const r = await fn(ctx.p); await ctx.p.waitForTimeout(200); const n = ctx.errs.length - before;
    const bad = n || (r && r.FAIL);
    log(`${bad ? 'FAIL' : 'ok  '} [${ctx.label}] ${name}${r !== undefined ? ' -> ' + JSON.stringify(r).slice(0, 220) : ''}${n ? '\n      ' + ctx.errs.slice(before).join('\n      ') : ''}`);
  } catch (e) { log(`FAIL [${ctx.label}] ${name}: ${e.message.split('\n')[0].slice(0, 220)}`); }
}
const T = p => p.evaluate(() => { const t = planTotals(BOQ); return { total: t.totalEst, grants: t.grantTotal, net: t.net }; });
const gen = async p => { await p.evaluate(() => generate()); await p.waitForTimeout(1800); };
const printScan = async (p, k) => { await p.evaluate(k => { if (k==='plan') exportEUPDF('detailed'); else if (k==='appendix') exportEUPDF('appendix'); else if (k==='schedule') exportContractorSchedule(); else if (k==='form-eu') exportSelectionForm('eu'); else exportSelectionForm('nb'); }, k); await p.waitForTimeout(400);
  return p.evaluate(() => { const t = (document.getElementById('pdf-print-view')||{}).textContent||''; const m = t.match(/\bundefined\b|\bNaN\b|\[object Object\]|\bnull\b|€NaN|€undefined/g); return m ? { FAIL: true, found: [...new Set(m)] } : 'clean'; }); };
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  let ctx;

  // ── A. save → snapshot → reload → restore → same figures ──
  ctx = await fresh(b, 'RESTORE');
  let before;
  await step(ctx, 'EU example + generate', async p => { await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); before = await T(p); return before; });
  await step(ctx, 'record an Actual before snapshot', p => p.evaluate(() => { const a=document.querySelector('.eu-act-input'); a.value='2222'; a.dispatchEvent(new Event('input',{bubbles:true})); a.dispatchEvent(new Event('change',{bubbles:true})); return 'set'; }));
  await step(ctx, 'buildSnapshot', p => p.evaluate(() => { const s = buildSnapshot('T-RESTORE'); localStorage.setItem('__drive_snap', JSON.stringify(s)); return { keys: Object.keys(s).slice(0,12) }; }));
  await step(ctx, 'reload + restoreSnapshot + generate', async p => { await p.reload(); await p.evaluate(() => { window.print = () => {}; }); await p.waitForTimeout(600);
    await p.evaluate(() => restoreSnapshot(JSON.parse(localStorage.getItem('__drive_snap')))); await p.waitForTimeout(800); await gen(p); const after = await T(p);
    const act = await p.evaluate(() => (document.querySelector('.eu-act-input')||{}).value);
    const same = JSON.stringify(after) === JSON.stringify(before);
    return { before, after, actualSurvived: act, FAIL: !same }; });
  await ctx.p.close();

  // ── B. Refurbishment routes actually move ──
  ctx = await fresh(b, 'RF-ROUTES');
  await step(ctx, 'refurb example + generate', async p => { await p.evaluate(() => { selectProjectType('Refurbishment'); loadRefurbExample(); }); await gen(p); return { scheme: await p.evaluate(() => document.getElementById('t0-grantScheme').value), ...(await T(p)) }; });
  const rf = {};
  for (const r of ['beh','ceg','oss','none']) await step(ctx, 'route -> ' + r, async p => { await p.evaluate(r => selectPlanRoute(r), r); await p.waitForTimeout(1500); rf[r] = await T(p); return rf[r]; });
  await step(ctx, 'refurb: total constant across routes (no scheme fee by design), grants move', () => { const t = new Set(Object.values(rf).map(x => x.total)); const g = new Set(Object.values(rf).map(x => x.grants)); return { distinctTotals: t.size, distinctGrants: g.size, FAIL: !(t.size === 1 && g.size >= 2) }; });
  await ctx.p.close();

  // ── C. HLI from provisional BER → heat pump sizing text ──
  ctx = await fresh(b, 'HLI');
  await step(ctx, 'EU example, HLI 2.4 from BER, generate', async p => { await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); const s=(i,v)=>{const e=document.getElementById(i); if(e) e.value=v;}; s('eu-hli','2.4'); s('eu-hli-source','ber'); euUpdateHeatLoad(); }); await gen(p);
    return p.evaluate(() => { const h=(BOQ.sections||[]).find(s=>/AIR-TO-WATER/.test(s.title)); if(!h) return {FAIL:true, why:'no heat pump section'}; const pb=_euPricingBasis(h, BOQ.euInputs||{}); const hli=pb.find(x=>/Heat Loss/.test(x)); const dl=pb.find(x=>/Design load/.test(x)); return { hli, dl, FAIL: !(hli && /provisional BER/.test(hli) && dl && /kW/.test(dl)) }; }); });
  await step(ctx, 'HLI indicative path', async p => { await p.evaluate(() => { const s=(i,v)=>{const e=document.getElementById(i); if(e) e.value=v;}; s('eu-hli-source','indicative'); euAutoHLI(); euUpdateHeatLoad(); }); await gen(p);
    return p.evaluate(() => { const h=(BOQ.sections||[]).find(s=>/AIR-TO-WATER/.test(s.title)); const pb=_euPricingBasis(h, BOQ.euInputs||{}); return { hli: pb.find(x=>/Heat Loss/.test(x)), FAIL: false }; }); });
  await ctx.p.close();

  // ── D. Not-included: tick moves item into priced section and out of exclusions ──
  ctx = await fresh(b, 'TICK');
  await step(ctx, 'EU example, build tab, tick first item, generate', async p => {
    await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p);
    const picked = await p.evaluate(() => { document.getElementById('screen-report').style.display='none'; document.getElementById('screen-input').style.display='flex'; euBuildExclTab(); const cbs=[...document.querySelectorAll('#eu-excl-tab input[type=checkbox], [id^=eu-excl-] input[type=checkbox]')]; if(!cbs.length) return null; const cb=cbs[0]; cb.checked=true; cb.dispatchEvent(new Event('change',{bubbles:true})); return cb.id; });
    await gen(p);
    return p.evaluate(id => { const secs=BOQ.sections||[]; const added=[]; const stillExcl=[];
      secs.forEach(s=>{ (s.items||[]).forEach(i=>{ if(/Not Included checklist/.test(i.note||'')) added.push(s.title.slice(0,30)+' :: '+i.description.slice(0,50)); }); });
      const addedNames = added.map(a=>a.split(' :: ')[1].toLowerCase());
      secs.forEach(s=>{ (s.exclusions||[]).forEach(e=>{ if(addedNames.some(n=>n.startsWith((e.item||'').toLowerCase().slice(0,12)))) stillExcl.push(e.item); }); });
      return { picked: id, added, stillListedAsExcluded: stillExcl, FAIL: !added.length || stillExcl.length>0 }; }, picked); });
  await ctx.p.close();

  // ── E. Rate override reaches the plan; Reset All restores ──
  ctx = await fresh(b, 'RATES');
  await step(ctx, 'EU example + baseline generate', async p => { await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); return T(p); });
  let baseRate;
  await step(ctx, 'read storage platform rate', p => p.evaluate(() => { for (const s of BOQ.sections) for (const i of s.items||[]) if (/Raised storage platform/.test(i.description)) return { mat: i.matRate }; return { FAIL:true, why:'no storage item (attic not in example?)' }; }).then(r => { baseRate = r.mat; return r; }));
  await step(ctx, 'override attic_store=99, regenerate', async p => { await p.evaluate(() => { toggleMatOverlay(); const b=[...document.querySelectorAll('.mdb-tab-btn')].find(x=>x.textContent.trim()==='EU Rates'); b&&b.click(); }); await p.waitForTimeout(300);
    const set = await p.evaluate(() => { const el=document.getElementById('eur-attic_store'); if(!el) return 'no #eur-attic_store'; el.value='99'; el.dispatchEvent(new Event('input',{bubbles:true})); return 'set 99'; });
    await p.evaluate(() => toggleMatOverlay()); await gen(p);
    return p.evaluate(base => { for (const s of BOQ.sections) for (const i of s.items||[]) if (/Raised storage platform/.test(i.description)) return { matNow: i.matRate, base, FAIL: !(i.matRate > base*2) }; return { FAIL:true }; }, baseRate); });
  await step(ctx, 'Reset All, regenerate', async p => { await p.evaluate(() => toggleMatOverlay()); await p.waitForTimeout(200);
    const clicked = await p.evaluate(() => { const btn=[...document.querySelectorAll('button')].find(x=>/Reset All/.test(x.textContent)); if(!btn) return 'no Reset All button'; window.confirm=()=>true; btn.click(); return 'clicked'; });
    await p.waitForTimeout(300); await p.evaluate(() => { const o=document.getElementById('mat-overlay'); if(o && o.style.display!=='none') toggleMatOverlay(); }); await gen(p);
    return p.evaluate(base => { for (const s of BOQ.sections) for (const i of s.items||[]) if (/Raised storage platform/.test(i.description)) return { clicked: true, matNow: i.matRate, base, FAIL: Math.abs(i.matRate-base) > 0.01 }; return { FAIL:true }; }, baseRate); });
  await ctx.p.close();

  // ── F. Schedule scope parity with plan; and print views free of undefined/NaN ──
  for (const [mode, loader, forms] of [['Energy Upgrade','loadEUExample1',['form-eu']], ['New Build','loadNewBuildExample',['form-nb']], ['Refurbishment','loadRefurbExample2',[]]]) {
    ctx = await fresh(b, 'PRINT:' + mode.split(' ')[0]);
    await step(ctx, 'load + generate', async p => { await p.evaluate(([m,l]) => { selectProjectType(m); window[l](); }, [mode, loader]); await gen(p); return T(p); });
    await step(ctx, 'schedule scope == plan scope', async p => { await p.evaluate(() => exportEUPDF('detailed')); await p.waitForTimeout(300); const plan = await p.evaluate(() => (BOQ.sections||[]).filter(s=>!s.isExtras).map(s=>s.title));
      await p.evaluate(() => exportContractorSchedule()); await p.waitForTimeout(300); const sched = await p.evaluate(() => (document.getElementById('pdf-print-view')||{}).textContent||'');
      const missing = plan.filter(t => !sched.includes(t)); return { sections: plan.length, missingFromSchedule: missing, FAIL: missing.length>0 }; });
    for (const k of ['plan','appendix','schedule',...forms]) await step(ctx, 'print scan ' + k, p => printScan(p, k));
    await ctx.p.close();
  }

  // ── G. Refurbishment with an extension ──
  ctx = await fresh(b, 'EXT');
  await step(ctx, 'refurb example + addExtension + generate', async p => { await p.evaluate(() => { selectProjectType('Refurbishment'); loadRefurbExample(); addExtension(); const s=(i,v)=>{const e=document.getElementById(i); if(e) e.value=v;}; s('ext1-area','25'); s('ext1-floorArea','25'); }); await gen(p);
    return p.evaluate(() => ({ exts: (typeof readExtensions==='function'? readExtensions().length : 'n/a'), sections: BOQ.sections.length, parts: [...new Set(BOQ.sections.map(s=>s.part))], ...{ total: planTotals(BOQ).totalEst } })); });
  await step(ctx, 'print scan plan (with extension)', p => printScan(p, 'plan'));
  await step(ctx, 'removeExtension(1) + generate', async p => { await p.evaluate(() => removeExtension(1)); await gen(p); return T(p); });
  await ctx.p.close();

  // ── H. Mode switching leaves no state behind ──
  ctx = await fresh(b, 'SWITCH');
  let nb1, eu1;
  await step(ctx, 'NB generate', async p => { await p.evaluate(() => { selectProjectType('New Build'); loadNewBuildExample(); }); await gen(p); nb1 = await T(p); return nb1; });
  await step(ctx, 'goHome -> EU generate', async p => { await p.evaluate(() => goHome()); await p.waitForTimeout(300); await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); eu1 = await T(p); return eu1; });
  await step(ctx, 'goHome -> NB again == first NB', async p => { await p.evaluate(() => goHome()); await p.waitForTimeout(300); await p.evaluate(() => { selectProjectType('New Build'); loadNewBuildExample(); }); await gen(p); const nb2 = await T(p); return { nb1, nb2, FAIL: JSON.stringify(nb1)!==JSON.stringify(nb2) }; });
  await step(ctx, 'goHome -> EU again == first EU', async p => { await p.evaluate(() => goHome()); await p.waitForTimeout(300); await p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }); await gen(p); const eu2 = await T(p); return { eu1, eu2, FAIL: JSON.stringify(eu1)!==JSON.stringify(eu2) }; });
  await ctx.p.close();

  await b.close();
  const fails = results.filter(r => r.startsWith('FAIL')).length;
  console.log('\n==== ' + results.length + ' steps, ' + fails + ' FAIL ====');
})().catch(e => { console.error('DRIVER CRASH', e); process.exit(1); });
