#!/usr/bin/env node
/**
 * Price one worked example through the real engine, outside the browser.
 *
 * WHY THIS EXISTS
 * Two printed documents disagreed on the total for the same house (EUR 35,945 vs
 * EUR 35,700). This runs the project through the live calculation functions and prints
 * the per-measure arithmetic so the current answer can be read off directly, without
 * opening the app or trusting either document.
 *
 * HOW IT GETS AT THE FUNCTIONS
 * The engine is not a module: it lives in inline <script> blocks in
 * ber_build_planner.html and assigns to globals. Nothing is exported, so this extracts
 * every non-module <script> block, concatenates them in document order, and evaluates
 * them in a Node vm context. No source file is modified.
 *
 * WHAT IT STUBS, AND WHY THAT IS SAFE
 * The pricing path reads exactly two things outside its own inputs, and both already
 * have fallbacks in the source, so stubbing them yields the shipped defaults:
 *
 *   document.getElementById(id) -> null
 *       getMaterialsFromUI() reads mat-* fields via `const el = ...; return el ? ... : def`
 *       and falls back to MATERIALS_DEFAULT. _xFASCIA_MAT() and euHLIFromBER() are
 *       likewise guarded. Returning null therefore gives the built-in rates, which is
 *       what a browser with an untouched Rate Settings panel gives too.
 *
 *   localStorage.getItem(key) -> null
 *       The rate-override IIFE (eu_ov / eu_cat) and seaiGrantTable()/cegRatesConfirmed()
 *       (planit_grants) each parse inside try/catch and fall back to the shipped rate
 *       book and GRANT_DEFAULTS. Returning null means "no overrides saved".
 *
 * Everything else the engine needs is passed in as the `inputs` object below, which is
 * the same shape readEUSelector() builds from the form. The DOM is never used to carry
 * project data into the calculation.
 *
 * Usage:  node scripts/price-worked-example.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML = path.join(__dirname, '..', 'ber_build_planner.html');

// ── the project under test ───────────────────────────────────────────────────
// Energy Upgrade, semi-detached, 110 m2, Co. Westmeath, Better Energy Homes,
// existing-BER basis. Measures: ceiling-level roof insulation, windows + external
// doors, air-to-water heat pump with cylinder, DMEV ventilation. Post-works BER at 300.
const PROJECT = {
  projName: '14 Ashfield Grove, Mullingar, Co. Westmeath',
  county: 'Westmeath',
  dwellingType: 'Semi-Detached',
  grantScheme: 'beh',

  inputs: {
    // geometry
    floorArea: 110,
    groundFloor: 55,
    perimeter: 34,
    wallArea: 88,
    netWallArea: 88,
    roofArea: 55,
    windowArea: 17,
    windowCount: 12,
    doorCount: 2,
    doorArea: 4,
    roomsDown: 4,
    roomsUp: 4,
    totalRooms: 8,
    bathrooms: 1,
    ensuites: 1,
    wc: 0,
    chimneyCount: 1,

    ageBand: '1983–1993',
    existWallType: 'Cavity Wall — uninsulated',
    existHeating: 'Oil Boiler',

    // measures selected
    measures: [
      'roof_ceiling',
      'windows_bundle', 'windows',
      'doors_bundle', 'doors',
      'heating',
      'hw_cylinder',
      'ventilation_dmev', 'ventilation',
    ],

    // roof — ceiling level, mineral wool 300mm
    roof_ceiling: true,
    roof_ceiling_type: 'mw-300',
    roof_ceiling_area: 55,
    roof_ceiling_makegood: true,

    // windows — 17 m2, 12 units, triple glazed uPVC casement
    windows_glazing: 'triple',
    windows_frame: 'upvc',
    windows_style: 'casement',
    windows_area: 17,
    windows_count: 12,
    windows_dispose: true,

    // doors — 2 composite
    doors_type: 'composite',
    doors_count: 2,
    doors_dispose: true,

    // heat pump — HLI 2.2 off the provisional BER, 6 kW, retain radiators, remove oil
    newHeating: 'ASHP',
    hli: 2.2,
    hliFromBER: true,
    emitterType: 'keep-rads',
    ashpRemove: 'oil',

    // ventilation — DMEV, 2 wet rooms + kitchen
    ventilation: 'DMEV',
    dmev_fan: 'humidity',
    dmev_mount: 'ceiling',

    // ancillaries — these mirror the Ancillary checkboxes, all unticked here.
    // The post-works BER is NOT a priced section: planTotals adds it as its own
    // EUR 300 row (BER_COST) whenever the post-works BER grant applies, which is how
    // the printed Cost Plan shows it.
    includeBER: false,
    includeSkip: false,
    includeMakingGood: false,
    includeAirTest: false,     // DMEV bundle carries its own air-tightness test
    includeStructEng: false,

    // Not Included tab — nothing ticked in, so every variation stays a variation
    exclTicked: {},
    exclQty: {},
  },
};

// ── build a context the engine can run in ────────────────────────────────────
function makeContext() {
  const noop = () => {};
  const elementStub = () => ({
    style: {}, dataset: {}, classList: { add: noop, remove: noop, contains: () => false },
    appendChild: noop, removeChild: noop, setAttribute: noop, addEventListener: noop,
    querySelector: () => null, querySelectorAll: () => [], insertAdjacentHTML: noop,
    scrollIntoView: noop, focus: noop, click: noop, remove: noop,
    innerHTML: '', textContent: '', value: '', checked: false, children: [], childElementCount: 0,
  });

  const documentStub = {
    // The only DOM reads on the pricing path are guarded lookups that fall back to
    // defaults, so null is the correct answer for all of them.
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: elementStub,
    addEventListener: noop,
    body: elementStub(),
    head: elementStub(),
    documentElement: elementStub(),
  };

  const storageStub = {
    getItem: () => null,          // no saved rate or grant overrides -> shipped defaults
    setItem: noop, removeItem: noop, clear: noop,
  };

  const ctx = {
    console, Math, Date, JSON, parseFloat, parseInt, isNaN, Number, String, Object,
    Array, Boolean, RegExp, Error, Intl, encodeURIComponent, decodeURIComponent,
    setTimeout: noop, clearTimeout: noop, setInterval: noop, clearInterval: noop,
    requestAnimationFrame: noop,
    document: documentStub,
    localStorage: storageStub,
    navigator: { userAgent: 'node' },
    location: { href: 'file:///ber_build_planner.html' },
    alert: noop, confirm: () => false, print: noop,
    XLSX: undefined,
  };
  ctx.window = ctx;
  ctx.globalThis = ctx;
  return vm.createContext(ctx);
}

// ── extract and evaluate every non-module inline script, in document order ────
function loadEngine(ctx) {
  const html = fs.readFileSync(HTML, 'utf8');
  const re = /<script([^>]*)>([\s\S]*?)<\/script>/g;
  let m, index = 0, loaded = 0, failed = [];
  while ((m = re.exec(html)) !== null) {
    index++;
    const attrs = m[1] || '';
    const code = m[2] || '';
    if (/\bsrc=/.test(attrs)) continue;        // external (SheetJS) — not needed
    if (/type\s*=\s*["']module["']/.test(attrs)) continue;  // ES module block
    if (!code.trim()) continue;
    try {
      vm.runInContext(code, ctx, { filename: `ber_build_planner.html#script${index}`, timeout: 20000 });
      loaded++;
    } catch (e) {
      // Blocks that wire up the UI can fail harmlessly against a stub DOM; the pricing
      // functions are what matter, and their presence is asserted below.
      failed.push({ index, message: e.message });
    }
  }
  return { loaded, failed };
}

// ── report helpers ───────────────────────────────────────────────────────────
const eur = n => '€' + Math.round(n).toLocaleString('en-IE');
const pad = (s, n) => String(s).padEnd(n);
const lpad = (s, n) => String(s).padStart(n);

function main() {
  const ctx = makeContext();
  const { loaded, failed } = loadEngine(ctx);

  const need = ['buildBOQRetrofit', 'planTotals', 'sectionLoad', 'sectionVatRate', 'calculateSEAIGrants'];
  const missing = need.filter(fn => typeof ctx[fn] !== 'function');
  if (missing.length) {
    console.error('Could not reach the engine. Missing: ' + missing.join(', '));
    console.error('Script blocks evaluated: ' + loaded + ', failed: ' + failed.length);
    failed.forEach(f => console.error('  block ' + f.index + ': ' + f.message));
    process.exit(1);
  }

  // Advanced Options. generate() always passes this for Energy Upgrade — see
  // readAdvancedOptions(): the mode returns includePrelimSection:false unconditionally,
  // so a retrofit plan carries no PRELIMINARIES section. Omitting `ao` entirely would
  // let one in, because buildBOQRetrofit's guard is `if (!ao || ao.includePrelimSection
  // !== false)`.
  const ao = {
    prelims: 0.12,              // 'ao-eu-prelims' ships checked -> 12% overhead & profit
    contingency: 0,             // the plan is a benchmark; no contingency in the loading
    proFees: null,              // 'ao-eu-pro-fees' ships unchecked
    includePrelimSection: false,
  };

  const boq = ctx.buildBOQRetrofit(
    PROJECT.inputs, PROJECT.projName, PROJECT.county,
    PROJECT.dwellingType, PROJECT.grantScheme, null, ao
  );

  // buildBOQRetrofit stamps projectInfo.type as 'Retrofit'; generate() overwrites it with
  // 'Energy Upgrade' straight afterwards (see the BOQ.projectInfo.type assignment in the
  // Energy Upgrade branch). planTotals gates the post-works BER row and its EUR 50 grant
  // on that exact string, so without this the total is EUR 300 light and the grant total
  // EUR 50 light. Replicating the assignment, not changing the engine.
  boq.projectInfo.type = 'Energy Upgrade';

  const T = ctx.planTotals(boq);

  console.log('PlanitBER — worked example priced through the live engine');
  console.log('  ' + PROJECT.projName);
  console.log('  Energy Upgrade · ' + PROJECT.dwellingType + ' · ' +
              PROJECT.inputs.floorArea + 'm² · Co. ' + PROJECT.county +
              ' · Better Energy Homes');
  if (typeof ctx.rateBookStamp === 'function') console.log('  ' + ctx.rateBookStamp());
  console.log('  script blocks evaluated: ' + loaded + (failed.length ? ', ' + failed.length + ' UI block(s) skipped' : ''));
  console.log('');

  // ── per measure ────────────────────────────────────────────────────────────
  console.log(pad('MEASURE', 44) + lpad('BASE', 11) + lpad('+O&P 12%', 12) + lpad('VAT', 7) + lpad('LOADED', 11));
  console.log('-'.repeat(85));

  let baseSum = 0, opSum = 0, loadedSum = 0;
  T.perSection.forEach(ps => {
    const s = ps.section;
    const base = s.subtotal || 0;
    const vat = ctx.sectionVatRate(s);
    const op = base * 1.12;
    baseSum += base; opSum += op; loadedSum += ps.est;
    console.log(
      pad(s.title.length > 43 ? s.title.slice(0, 42) + '…' : s.title, 44) +
      lpad(eur(base), 11) + lpad(eur(op), 12) +
      lpad((vat * 100).toFixed(1) + '%', 7) + lpad(eur(ps.est), 11)
    );
  });
  console.log('-'.repeat(85));
  console.log(pad('Measured works', 44) + lpad(eur(baseSum), 11) + lpad(eur(opSum), 12) +
              lpad('', 7) + lpad(eur(T.works), 11));

  // ── the rows that sit outside the measures ─────────────────────────────────
  if (T.berCost) console.log(pad('Post-works BER assessment', 44) + lpad('', 30) + lpad(eur(T.berCost), 11));
  if (T.fee)     console.log(pad('Scheme management fee', 44) + lpad('', 30) + lpad(eur(T.fee), 11));

  // ── totals ─────────────────────────────────────────────────────────────────
  console.log('');
  console.log('  TOTAL BUDGET EST.   ' + lpad(eur(T.totalEst), 12));
  console.log('  SEAI GRANTS         ' + lpad('-' + eur(T.grantTotal), 12));
  console.log('  NET TO FUND         ' + lpad(eur(T.net), 12));
  console.log('');

  (boq.grants || []).forEach(g => {
    console.log('    ' + pad(g.description, 52) + lpad(eur(g.amount || 0), 10));
  });

  // ── the question that prompted this ────────────────────────────────────────
  // The BOQ object carries TWO totals from two different code paths. planTotals() is the
  // one the Cost Plan, the on-screen table and the route strip all draw on. summary /
  // computeSummary() is an older parallel calculation that nothing in the printed plan
  // reads. They disagree, which is why two documents ended up quoting different figures.
  const su = boq.summary || {};
  const alt = su.totalProjectCost != null ? su.totalProjectCost : su.total;

  console.log('');
  console.log('WHICH TOTAL IS WHICH');
  console.log('  planTotals()          ' + lpad(eur(T.totalEst), 10) +
              '   <- printed on the Cost Plan and the screen');
  if (alt != null) {
    console.log('  summary.totalProject  ' + lpad(eur(alt), 10) +
                '   <- a second path; nothing printed reads it');
    const gap = Math.round(alt) - Math.round(T.totalEst);
    if (gap !== 0) console.log('  difference            ' + lpad((gap > 0 ? '+' : '−') + eur(Math.abs(gap)), 10));
  }

  console.log('');
  [35945, 35700].forEach(c => {
    const dP = Math.round(T.totalEst) - c;
    const dS = alt == null ? null : Math.round(alt) - c;
    const who = dP === 0 ? 'planTotals — the printed figure'
              : dS === 0 ? 'summary.totalProjectCost — NOT the printed figure'
              : 'neither path';
    console.log('  ' + lpad(eur(c), 9) + '  = ' + who);
  });

  if (failed.length) {
    console.log('');
    console.log('UI blocks that did not evaluate against the stub DOM (pricing unaffected):');
    failed.forEach(f => console.log('  block ' + f.index + ': ' + f.message));
  }
}

main();
