// Drive every mode of the planner end to end in a real browser and collect every error.
const { chromium } = require('playwright');
const APP = 'file://' + require('path').resolve(__dirname, '..', '..', 'ber_build_planner.html');
const results = []; const log = (m) => { results.push(m); console.log(m); };
async function fresh(b, label) {
  const p = await b.newPage({ viewport: { width: 1300, height: 950 } });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('console.error: ' + m.text().slice(0, 200)); });
  await p.goto(APP); await p.evaluate(() => { window.print = () => {}; }); await p.waitForTimeout(500);
  return { p, errs, label };
}
async function step(ctx, name, fn) {
  const before = ctx.errs.length;
  try { const r = await fn(ctx.p); await ctx.p.waitForTimeout(250);
        const n = ctx.errs.length - before;
        log(`${n ? 'ERR ' : 'ok  '} [${ctx.label}] ${name}${r !== undefined ? ' -> ' + JSON.stringify(r).slice(0, 140) : ''}${n ? '\n      ' + ctx.errs.slice(before).join('\n      ') : ''}`);
  } catch (e) { ctx.errs.push('throw: ' + e.message); log(`ERR [${ctx.label}] ${name}: ${e.message.split('\n')[0].slice(0, 200)}`); }
}
const totals = p => p.evaluate(() => { const T = planTotals(BOQ); const s = BOQ.summary || {}; return { total: T.totalEst, grants: T.grantTotal, net: T.net, sections: (BOQ.sections||[]).length, hdr: (document.getElementById('rpt-total')||{}).textContent }; });
const exportsFor = async (ctx, kinds) => {
  for (const k of kinds) await step(ctx, 'export ' + k, async p => {
    await p.evaluate(k => {
      if (k === 'plan') exportEUPDF('detailed'); else if (k === 'appendix') exportEUPDF('appendix');
      else if (k === 'schedule') exportContractorSchedule(); else if (k === 'form-eu') exportSelectionForm('eu'); else if (k === 'form-nb') exportSelectionForm('nb');
    }, k);
    await p.waitForTimeout(400);
    return p.evaluate(() => { const v = document.getElementById('pdf-print-view'); return v ? { chars: v.textContent.length, eur: (v.textContent.match(/€\s?[\d,]{3,}/g)||[]).length } : 'no print view'; });
  });
};
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

  // ── Energy Upgrade ──
  let ctx = await fresh(b, 'EU');
  await step(ctx, 'load example 1', p => p.evaluate(() => { selectProjectType('Energy Upgrade'); loadEUExample1(); }));
  await step(ctx, 'generate', async p => { await p.evaluate(() => generate()); await p.waitForTimeout(1800); return totals(p); });
  await step(ctx, 'route -> oss', async p => { await p.evaluate(() => selectPlanRoute('oss')); await p.waitForTimeout(1500); return totals(p); });
  await step(ctx, 'route -> ceg', async p => { await p.evaluate(() => selectPlanRoute('ceg')); await p.waitForTimeout(1500); return totals(p); });
  await step(ctx, 'route -> beh', async p => { await p.evaluate(() => selectPlanRoute('beh')); await p.waitForTimeout(1500); return totals(p); });
  await step(ctx, 'route -> none', async p => { await p.evaluate(() => selectPlanRoute('none')); await p.waitForTimeout(1500); return totals(p); });
  await step(ctx, 'type an Actual + note', async p => p.evaluate(() => { const a=document.querySelector('.eu-act-input'); const n=document.querySelector('.eu-note-input'); if(!a) return 'no inputs'; a.value='1234'; a.dispatchEvent(new Event('input',{bubbles:true})); n.value='site note'; n.dispatchEvent(new Event('input',{bubbles:true})); return document.querySelector('.eu-c-diff').textContent; }));
  await exportsFor(ctx, ['plan', 'appendix', 'schedule', 'form-eu']);
  await step(ctx, 'rate settings: every tab', async p => { await p.evaluate(() => toggleMatOverlay()); await p.waitForTimeout(300);
    return p.evaluate(async () => { const out=[]; for (const btn of document.querySelectorAll('.mdb-tab-btn')) { btn.click(); await new Promise(r=>setTimeout(r,150)); out.push(btn.textContent.trim()); } return out; }); });
  await step(ctx, 'rate settings: close', p => p.evaluate(() => toggleMatOverlay()));
  await step(ctx, 'not-included tab: build + tick one', async p => { await p.evaluate(() => { document.getElementById('screen-report').style.display='none'; document.getElementById('screen-input').style.display='flex'; euBuildExclTab(); }); await p.waitForTimeout(200);
    return p.evaluate(() => { const cbs=[...document.querySelectorAll('#eu-excl-tab input[type=checkbox], [id^=eu-excl-] input[type=checkbox]')]; if(!cbs.length) return 'no checkboxes found'; cbs[0].checked=true; cbs[0].dispatchEvent(new Event('change',{bubbles:true})); return cbs.length + ' checkboxes; ticked first'; }); });
  await step(ctx, 'regenerate after tick', async p => { await p.evaluate(() => generate()); await p.waitForTimeout(1800); return totals(p); });
  await step(ctx, 'save project', async p => { const r = await p.evaluate(async () => { const code = await saveProject(); return code || 'saved'; }); return r; });
  await step(ctx, 'reload + restore', async p => { await p.reload(); await p.evaluate(() => { window.print = () => {}; }); await p.waitForTimeout(600);
    return p.evaluate(() => { const keys=Object.keys(localStorage).filter(k=>/proj|planit|snap/i.test(k)); return keys.slice(0,6); }); });
  await ctx.p.close();

  // ── New Build ──
  ctx = await fresh(b, 'NB');
  await step(ctx, 'load example', p => p.evaluate(() => { selectProjectType('New Build'); loadNewBuildExample(); }));
  await step(ctx, 'generate', async p => { await p.evaluate(() => generate()); await p.waitForTimeout(2000); return totals(p); });
  await step(ctx, 'type an Actual', p => p.evaluate(() => { const a=document.querySelector('.eu-act-input'); if(!a) return 'no inputs'; a.value='5000'; a.dispatchEvent(new Event('input',{bubbles:true})); return (document.querySelector('.eu-c-diff')||{}).textContent; }));
  await exportsFor(ctx, ['plan', 'appendix', 'schedule', 'form-nb']);
  await ctx.p.close();

  // ── Refurbishment ──
  for (const [ex, label] of [['loadRefurbExample','RF1'], ['loadRefurbExample2','RF2']]) {
    ctx = await fresh(b, label);
    await step(ctx, 'load ' + ex, p => p.evaluate(ex => { selectProjectType('Refurbishment'); window[ex](); }, ex));
    await step(ctx, 'generate', async p => { await p.evaluate(() => generate()); await p.waitForTimeout(2000); return totals(p); });
    await step(ctx, 'route -> oss', async p => { await p.evaluate(() => selectPlanRoute('oss')); await p.waitForTimeout(1500); return totals(p); });
    await exportsFor(ctx, ['plan', 'appendix', 'schedule']);
    await ctx.p.close();
  }

  // ── Empty / edge: generate with nothing entered ──
  ctx = await fresh(b, 'EMPTY');
  await step(ctx, 'EU generate with no inputs', async p => { await p.evaluate(() => { selectProjectType('Energy Upgrade'); }); await p.evaluate(() => generate()); await p.waitForTimeout(1500); return p.evaluate(() => ({ boq: typeof BOQ, shown: (document.getElementById('screen-report')||{}).style.display })); });
  await ctx.p.close();
  await b.close();
  const errCount = results.filter(r => r.startsWith('ERR')).length;
  console.log('\n==== ' + results.length + ' steps, ' + errCount + ' with errors ====');
})().catch(e => { console.error('DRIVER CRASH', e); process.exit(1); });
