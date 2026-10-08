# The SEAI pack: six connected A4 PDFs sharing one design system.
#   01 The Value Proposition — text only: what it is, why, and where each other document fits
#   02 The Cost Plan         — a page of notes, then the example semi-D's plan bound behind
#   03 The Pricing Schedule  — notes, then the same measured scope with every figure removed
#   04 The Appendix          — notes, then the workings, itemised rates and guide prices
#   05 The Workflow          — the six agreed steps, provisional BER to post-works BER
#   06 The Software          — live screenshots + where every number comes from
#   07 The Engine            — how the rate book is sourced, versioned and inspected
# 02-04 are one house printed three ways; each binds the software's own output whole.
import base64, html as H

def b64(path):
    return 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

# Only what document 06 actually embeds. The pack used to declare a dozen more -- the
# three-worked-example structure it had before -- and loaded every one of them on import,
# so a missing leftover stopped the build for a file nothing referenced.
IMG = {k: b64(f) for k, f in {
    'home':    'app_home.png',     'sel':     'app_selector.png',
    'appplan': 'app_plan.png',     'rates':   'app_rates.png',
    'grants':  'app_grants.png',   'routes':  'app_routes.png',
    'preview': 'app_preview_dialog.png',
    'ddr': 'app_ddr.png', 'ddrtabs': 'app_ddr_tabs.png',
    'routedl': 'shot_routedl.png',
    'eurates': 'app_eurates.png', 'regional': 'app_regional.png',
    'eng_a': 'app_eng_a.png', 'eng_b': 'app_eng_b.png', 'eng_c': 'app_eng_c.png',
}.items()}

GLOBE = '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" class="globe">
  <defs>
    <radialGradient id="pgP" cx="35%" cy="30%" r="65%"><stop offset="0%" stop-color="#62AADF"/><stop offset="100%" stop-color="#2464A0"/></radialGradient>
    <clipPath id="pcP"><circle cx="60" cy="60" r="55"/></clipPath>
  </defs>
  <circle cx="60" cy="60" r="55" fill="url(#pgP)"/>
  <g clip-path="url(#pcP)" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="0.9">
    <ellipse cx="60" cy="37" rx="52" ry="9"/><ellipse cx="60" cy="60" rx="55" ry="11"/><ellipse cx="60" cy="83" rx="52" ry="9"/>
    <ellipse cx="60" cy="60" rx="10" ry="55"/><ellipse cx="60" cy="60" rx="30" ry="55"/><line x1="60" y1="5" x2="60" y2="115"/>
  </g>
  <g clip-path="url(#pcP)">
    <ellipse cx="53" cy="27" rx="21" ry="13" transform="rotate(-15 53 27)" fill="#2D7A4F" opacity="0.9"/>
    <ellipse cx="77" cy="45" rx="14" ry="9" transform="rotate(12 77 45)" fill="#2D7A4F" opacity="0.85"/>
    <ellipse cx="39" cy="64" rx="13" ry="22" transform="rotate(4 39 64)" fill="#2D7A4F" opacity="0.9"/>
    <ellipse cx="71" cy="77" rx="10" ry="7" transform="rotate(-10 71 77)" fill="#2D7A4F" opacity="0.82"/>
    <ellipse cx="59" cy="50" rx="6" ry="4" fill="#4ab870" opacity="0.65"/>
    <ellipse cx="47" cy="84" rx="9" ry="5" transform="rotate(15 47 84)" fill="#2D7A4F" opacity="0.75"/>
  </g>
  <circle cx="60" cy="60" r="55" fill="none" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
</svg>'''

RIGHT_ARROW = '''<svg viewBox="0 0 34 24" xmlns="http://www.w3.org/2000/svg" style="width:22px;height:16px;display:block;margin:0 auto;">
  <path d="M2 12 H24 M17 4 L27 12 L17 20" fill="none" stroke="#B07D1A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
DOWN_ARROW = '''<svg viewBox="0 0 24 34" xmlns="http://www.w3.org/2000/svg" style="width:16px;height:24px;display:block;margin:0 auto;">
  <path d="M12 2 V24 M4 17 L12 27 L20 17" fill="none" stroke="#B07D1A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

# ── THE FACTS AND CLAIMS THIS PACK REPEATS, DEFINED ONCE ─────────────────────
# Everything below appears in more than one document. Hand-typing them let the figures
# drift apart once, and let the sizing claim and the assessor-burden line end up in two
# different wordings. Correct them here and every document follows.

# The worked example
EX_ADDR   = '3 Bed Semi, Co. Westmeath'
EX_AREA   = '110'                       # m² floor area
EX_BUILT  = '1983&ndash;93'
EX_BER    = 'BER D&thinsp;&rarr;&thinsp;A'
EX_SCHEME = 'Better Energy Homes'
EX_HLI    = '2.2'                       # W/m²K, post-works, off the provisional BER
EX_KW     = '6'                         # kW design load
EX_FLOW   = '45'                        # °C flow temperature
# Straight from planTotals(BOQ) in gen_ex_pdfs.js — the same call the printed Cost Plan
# prices from. Do not take these from BOQ.summary: that path charges a flat 13.5% VAT
# (the heat pump is 9%) and omits the post-works BER, which is where 35,945 came from.
EX_TOTAL, EX_GRANTS, EX_NET = '34,977', '20,150', '14,827'

# The rate book every figure is priced on
RATE_BOOK = 'v2026.2, effective 26 August 2026'

# Load-bearing claims. Each states what the plan does or does not do, and each has already
# been corrected in one document while standing wrong in another.
SIZING_BASIS = 'the same basis the SEAI heat pump technical assessment works to'
# used in document 01; the workflow makes the same point by describing the survey as normal
ASSESSOR_ASK = 'nothing asked of them beyond producing it'
FONTS = open('fonts_embedded.css').read()

CSS = FONTS + '''
  @page { size: A4 portrait; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; }
  body { font-family: 'DM Sans', Calibri, sans-serif; color: #1E293B; font-size: 9pt;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .sheet { width: 210mm; height: 297mm; padding: 11mm 13mm 9mm; background: #FBFAF7;
           display: flex; flex-direction: column; overflow: hidden; page-break-after: always; position: relative; }
  .sheet:last-child { page-break-after: auto; }
  .globe { width: 30px; height: 30px; flex-shrink: 0; }
  .strip { display: flex; align-items: center; justify-content: space-between; padding-bottom: 2.5mm;
           border-bottom: 1.5pt solid #B07D1A; margin-bottom: 4.5mm; }
  .strip .word { font-size: 12pt; font-weight: 700; letter-spacing: -0.4px; }
  .word .p { color: #1E293B; } .word .b { color: #E8A020; }
  .strip .crumb { font-size: 7.5pt; color: #8090A8; letter-spacing: 0.06em; text-transform: uppercase; font-weight: 700; }
  h1 { font-family: 'Fraunces', Georgia, serif; font-size: 21pt; font-weight: 800; margin: 0; line-height: 1.1; }
  h2 { font-family: 'Fraunces', Georgia, serif; font-size: 16pt; font-weight: 800; margin: 0 0 2mm; line-height: 1.15; }
  .kick { font-size: 8pt; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: #B07D1A; margin-bottom: 1.6mm; }
  p.body { font-size: 9.5pt; line-height: 1.55; margin: 0 0 2.6mm; color: #2B3648; }
  p.body strong { color: #1E293B; }
  .pageno { position: absolute; bottom: 9mm; left: 13mm; font-size: 7pt; color: #A0A8B4; }
  .nextdoc { position: absolute; bottom: 9mm; right: 13mm; font-size: 7pt; color: #B07D1A; font-weight: 700; }
  .fine { margin-top: auto; padding-top: 2mm; border-top: 0.5pt solid #DDD8CC; font-size: 6.6pt;
          color: #A0A8B4; line-height: 1.5; margin-bottom: 6mm; }
  .shotframe { background: #FFFFFF; border: 0.6pt solid #D8D2C4; border-radius: 2pt; padding: 2.5mm;
               box-shadow: 0 1.5mm 4mm rgba(30,41,59,0.10); }
  .shotframe img { width: 100%; display: block; }
  .cap { font-size: 7.4pt; color: #8090A8; font-style: italic; margin-top: 1.6mm; line-height: 1.4; }

  .nums { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
  .num { background: #FFFFFF; border: 0.5pt solid #E2DDD1; border-top: 2.4pt solid #B07D1A;
         border-radius: 2.5pt; padding: 3mm 3.2mm; }
  .nv { font-family: 'Fraunces', Georgia, serif; font-size: 17pt; font-weight: 800; color: #1E293B; }
  .nv.g { color: #046C4C; }
  .nl { font-size: 7.8pt; color: #64748B; line-height: 1.45; margin-top: 1.2mm; }

  .big3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
  .pt { background: #FFFFFF; border: 0.5pt solid #E2DDD1; border-radius: 2pt; padding: 2.8mm 3mm; }
  .pt .pt-t { font-family: 'Fraunces', Georgia, serif; font-size: 10.5pt; font-weight: 800; line-height: 1.2; margin-bottom: 1.4mm; }
  .pt .pt-b { font-size: 8pt; color: #3F4A5A; line-height: 1.48; }
  .pt .pt-b strong { color: #1E293B; }
  .pt.ho { border-top: 2.4pt solid #1E293B; } .pt.se { border-top: 2.4pt solid #059669; }
  .pt.asr { border-top: 2.4pt solid #B07D1A; }

  /* labelled working document */
  .lab { position: relative; margin: 0 auto; }
  .lab img { width: 100%; display: block; }
  .mark { position: absolute; width: 6.2mm; height: 6.2mm; border-radius: 50%; background: #B07D1A;
          color: #fff; font-weight: 800; font-size: 9.5pt; display: flex; align-items: center;
          justify-content: center; border: 1.5pt solid #FFFFFF; box-shadow: 0 0 0 1pt #B07D1A; }
  ul.legend { margin: 0; padding: 0; list-style: none; }
  ul.legend li { font-size: 8.6pt; line-height: 1.5; color: #2B3648; margin-bottom: 1.6mm;
                 display: flex; gap: 2.4mm; align-items: baseline; }
  ul.legend .lm { flex-shrink: 0; width: 5.4mm; height: 5.4mm; border-radius: 50%; background: #B07D1A;
                  color: #fff; font-weight: 800; font-size: 8.5pt; display: inline-flex; align-items: center;
                  justify-content: center; position: relative; top: 1mm; }
  ul.legend strong { color: #1E293B; }

  /* workflow steps */
  .sketchcard { background: #FFFFFF; border: 0.6pt solid #D8D2C4; border-radius: 2pt; padding: 3mm;
                box-shadow: 0 1mm 3mm rgba(30,41,59,0.08);
                background-image: linear-gradient(#EEF2F6 0.4pt, transparent 0.4pt),
                                  linear-gradient(90deg, #EEF2F6 0.4pt, transparent 0.4pt);
                background-size: 5mm 5mm; }
  .ticklist { background: #FFFFFF; border: 0.6pt solid #D8D2C4; border-radius: 2pt; padding: 3mm 3.4mm; }
  .ticklist .tlh { font-size: 8pt; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
                   color: #B07D1A; margin-bottom: 1.8mm; }
  .tl { display: flex; gap: 2.2mm; align-items: baseline; font-size: 8.4pt; color: #2B3648;
        line-height: 1.45; margin-bottom: 1.5mm; }
  .tl .bx { flex-shrink: 0; width: 3.4mm; height: 3.4mm; border: 1pt solid #94A3B8; border-radius: 0.6pt;
            position: relative; top: 0.5mm; display: inline-flex; align-items: center; justify-content: center;
            color: #046C4C; font-weight: 800; font-size: 8.5pt; }
  table.mapt { width: 100%; border-collapse: collapse; }
  table.mapt th { text-align: left; font-size: 7.6pt; font-weight: 700; letter-spacing: 0.06em;
                  text-transform: uppercase; color: #B07D1A; padding: 0 2mm 1.2mm 0; }
  table.mapt td { font-size: 8pt; color: #2B3648; line-height: 1.38; padding: 0.8mm 2.5mm 0.8mm 0;
                  border-top: 0.4pt solid #EFEBE1; vertical-align: top; }
  table.mapt td.m { font-weight: 700; color: #1E293B; white-space: nowrap; }
  table.mapt td.arr { color: #B07D1A; font-weight: 800; }
  .fullstep-img { display: flex; flex-direction: column; align-items: center; }
  .fullstep-img .shotframe { width: 134mm; }
  .notes2 { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; margin-top: 3mm; }
  .notes2 p { font-size: 8.8pt; line-height: 1.52; color: #2B3648; margin: 0; }
  .notes2 p.grey { color: #64748B; font-size: 8.2pt; }

  .step2 { display: grid; grid-template-columns: 72mm 1fr; gap: 6mm; align-items: center; }
  .step2 .im2 { height: 84mm; overflow: hidden; }
  .stepb2 { font-size: 8.8pt; color: #2B3648; line-height: 1.52; }
  .stepb2 p { margin: 0 0 1.8mm; }
  .stepb2 .grey { color: #64748B; font-size: 8.2pt; }
  .miniflow { display: flex; align-items: center; gap: 1.6mm; }
  .mf { flex: 1; background: #FFFFFF; border: 0.5pt solid #E2DDD1; border-top: 1.8pt solid #B07D1A;
        border-radius: 2pt; padding: 1.6mm 2mm; font-size: 7.4pt; font-weight: 700; color: #1E293B;
        text-align: center; }
  .mf .n { color: #B07D1A; margin-right: 1mm; }
  .mfarr { color: #B07D1A; font-weight: 800; font-size: 10pt; }

  .step { display: grid; grid-template-columns: 50mm 1fr; gap: 5mm; align-items: center; }
  .step .im { height: 40mm; overflow: hidden; }
  .stept { font-family: 'Fraunces', Georgia, serif; font-size: 11.5pt; font-weight: 800; margin-bottom: 0.9mm; }
  .stept .n { color: #B07D1A; margin-right: 1.6mm; }
  .stepb { font-size: 8.2pt; color: #2B3648; line-height: 1.45; }
  .stepdark { background: #1E293B; border-radius: 2.5pt; padding: 2.6mm 3.4mm; color: #C6D0DC; }
  .stepdark .stept { color: #FFFFFF; margin-bottom: 0.6mm; }
  .stepdark .stepb { color: #C6D0DC; }
  .arrowrow { padding: 1mm 0; }

  /* software grid */
  .appgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; }
  .appshot { background: #FFFFFF; border: 0.6pt solid #D8D2C4; border-radius: 2pt; padding: 1.8mm;
             box-shadow: 0 1mm 3mm rgba(30,41,59,0.08); }
  .appshot img { width: 100%; display: block; border-radius: 1pt; }
  .appshot .im3 { height: 42mm; overflow: hidden; }
  .appshot .im3.tall { height: 56mm; }
  .appshot .ac { font-size: 7.2pt; color: #475569; line-height: 1.4; margin-top: 1.2mm; }
  .appshot .ac strong { color: #1E293B; }
  ul.src { margin: 0; padding-left: 0; list-style: none; columns: 2; column-gap: 8mm; }
  ul.src li { font-size: 8pt; line-height: 1.45; color: #2B3648; padding-left: 4.5mm; position: relative;
              margin-bottom: 1.4mm; break-inside: avoid; }
  ul.src li::before { content: ''; position: absolute; left: 0; top: 1.5mm; width: 2.2mm; height: 2.2mm;
                      border-radius: 50%; background: #B07D1A; }

  /* worked examples */
  .exrow { display: grid; grid-template-columns: 1fr 44mm 44mm; gap: 4mm; align-items: start; }
  .exhead { font-family: 'Fraunces', Georgia, serif; font-size: 11.5pt; font-weight: 800; margin-bottom: 1mm; }
  .exsub { font-size: 7.6pt; color: #8090A8; margin-bottom: 2mm; }
  .rr { display: flex; justify-content: space-between; font-size: 8.4pt; color: #475569; padding: 0.9mm 0;
        border-bottom: 0.4pt solid #EFEBE1; }
  .rr span { white-space: nowrap; }
  .rr span + span { margin-left: 2mm; }
  .rr .v { font-weight: 700; color: #1E293B; }
  .rr.net { border-bottom: none; } .rr.net .v { color: #046C4C; font-size: 9.5pt; }
  .exthumb { background: #FFFFFF; border: 0.6pt solid #D8D2C4; border-radius: 2pt; padding: 1.6mm;
             box-shadow: 0 1mm 3mm rgba(30,41,59,0.08); }
  .exthumb .im { height: 52mm; overflow: hidden; }
  .exthumb img { width: 100%; display: block; }
  .exthumb .tc { font-size: 7pt; font-weight: 700; color: #1E293B; margin-top: 1mm; }
  .routes3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
  .route { background: #FFFFFF; border: 0.5pt solid #E2DDD1; border-radius: 2pt; padding: 2.4mm 2.8mm; }
  .route .rt { font-size: 8.4pt; font-weight: 700; margin-bottom: 1.2mm; }

  .ask { background: #FBF3E4; border: 0.5pt solid #EBD9B4; border-left: 2.6pt solid #B07D1A;
         border-radius: 2pt; padding: 3.2mm 3.6mm; }
  .ask .at { font-family: 'Fraunces', Georgia, serif; font-size: 12pt; font-weight: 800; margin-bottom: 1.4mm; }
  .ask .ab { font-size: 9pt; line-height: 1.55; color: #3F4A5A; }
  .dark { background: #1E293B; border-radius: 2.5pt; padding: 3mm 3.6mm; color: #C6D0DC; }
  .dark .dt { font-family: 'Fraunces', Georgia, serif; font-size: 11pt; font-weight: 800; color: #FFFFFF; margin-bottom: 1.2mm; }
  .dark .db { font-size: 8.2pt; line-height: 1.5; }
  .dark .db strong { color: #FFFFFF; }
  ul.tick { margin: 0 0 2.6mm; padding-left: 0; list-style: none; }
  ul.tick li { font-size: 9pt; line-height: 1.5; color: #2B3648; padding-left: 5mm; position: relative; margin-bottom: 1.6mm; }
  ul.tick li::before { content: ''; position: absolute; left: 0; top: 1.4mm; width: 2.6mm; height: 2.6mm;
                       border-radius: 50%; background: #E8A020; }
  ul.tick strong { color: #1E293B; }
'''

# Five documents. Three of them (02-04) are the software's own output, bound whole and with
# nothing in front of them: document 01 says what each is for, so the notes pages that used
# to front them are gone. Document 05 is the software and the rate book behind it.
DOCS = ['The Value Proposition', 'The Baseline Cost Plan', 'The Pricing Schedule',
        'The Appendix', 'The Software', 'Data Protection']
NDOC = len(DOCS)

def strip(n):
    crumb = 'PlanitBER pack &middot; document %d of %d &middot; %s' % (n, NDOC, DOCS[n-1])
    return f'''<div class="strip">
      <div style="display:flex;align-items:center;gap:2mm;">{GLOBE}<div class="word"><span class="p">Planit</span><span class="b">BER</span></div></div>
      <div class="crumb">{crumb}</div>
    </div>'''

def footer(n, page='', total=''):
    nxt = ('<div class="nextdoc">next: %02d &middot; %s &rarr;</div>' % (n+1, DOCS[n])) if n < NDOC else ''
    pg = (' &middot; page %s of %s' % (page, total)) if page else ''
    return f'<div class="pageno">PlanitBER &middot; document {n} of {NDOC}{pg}</div>{nxt}'

FINE1 = ('PlanitBER V1 &middot; '
         f'Worked example throughout: {EX_ADDR} &mdash; {EX_AREA}&thinsp;m&sup2; semi-detached, {EX_BER}, '
         f'{EX_SCHEME} route &middot; All figures produced by the software on rate book {RATE_BOOK} '
         '&middot; Independent estimate &mdash; not prepared by any contractor.')

# ── the workflow steps, drawn for document 01 ────────────────────────────────
# A numbered timeline: number in a disc, title left, status right, body left-aligned
# beneath. Left alignment because these are sentences, not captions — centred prose makes
# the eye hunt for each line start. The one new step is tinted and darker-edged so the
# page makes its argument at a glance.
def wfstep(n, title, body, note='', last=False, add=False, sub=''):
    arrow = '' if last else f'<div style="padding:0.5mm 0 0.2mm;">{DOWN_ARROW}</div>'
    # The existing steps are context, so they recede: grey discs, no accent edge. Gold is
    # spent on the one step being proposed, which is what the page is for.
    edge  = '#B07D1A' if add else '#D8D2C4'
    bg    = '#FFFAF0' if add else '#FFFFFF'
    disc  = '#B07D1A' if add else '#AEB4BE'
    ncol  = '#B07D1A' if add else '#A0A8B4'
    return f'''<div style="background:{bg};border:0.6pt solid #D8D2C4;border-left:{"3.6pt" if add else "2.4pt"} solid {edge};border-radius:2pt;padding:2.9mm 4.2mm;max-width:174mm;margin:0 auto;text-align:left;">
      <div style="display:flex;align-items:center;gap:3mm;margin-bottom:1.6mm;">
        <span style="flex-shrink:0;width:6.4mm;height:6.4mm;border-radius:50%;background:{disc};color:#fff;
                     font-family:'Fraunces',Georgia,serif;font-size:9.5pt;font-weight:800;
                     display:inline-flex;align-items:center;justify-content:center;">{n}</span>
        <span class="wft" style="flex:1;font-family:'Fraunces',Georgia,serif;font-size:{'12.8pt' if add else '12pt'};font-weight:800;color:#1E293B;line-height:1.15;">{title}</span>
        <span style="flex-shrink:0;font-size:7.4pt;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:{ncol};white-space:nowrap;">{note}</span>
      </div>
      <div class="wfb" style="font-size:9.9pt;color:#3F4A5A;line-height:1.6;padding-left:9.4mm;">{body}</div>
      {f'<div class="wfs" style="font-size:8.3pt;color:#64748B;line-height:1.5;padding-left:9.4mm;margin-top:1.3mm;">{sub}</div>' if sub else ''}
    </div>
    {arrow}'''

# ── 01 · THE VALUE PROPOSITION — text only, one page, references the other three ─
def vk(t):
    return f'<div class="kick" style="margin-top:2.3mm;">{t}</div>'

doc1 = f'''<div class="sheet">
  <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:3mm;border-bottom:2pt solid #B07D1A;">
    <div style="display:flex;align-items:center;gap:2.5mm;">{GLOBE}<div class="word" style="font-size:19pt;"><span class="p">Planit</span><span class="b">BER</span></div></div>
    <div style="text-align:right;font-size:7.4pt;color:#8090A8;line-height:1.65;">
      <div>Killyleen, Ballinode, Co. Monaghan</div>
      <div>mc2rating@gmail.com &middot; 087 981 0150</div><div>[Date]</div>
    </div>
  </div>
  <h1 style="font-size:16pt;line-height:1.2;margin:2.6mm 0 1.6mm;">Empowering homeowners with tender
    documents to engage in the retrofit process with confidence</h1>
  <p class="body" style="font-size:9.8pt;line-height:1.46;margin-bottom:1.6mm;color:#1E293B;">PlanitBER
    is software that turns a provisional BER into homeowner tender documents. It takes the measured
    geometry and the Heat Loss Indicator from a Dwelling Details Report and applies rates to the measures
    agreed with the homeowner, producing a <strong>Baseline Cost Plan</strong>, a <strong>Contractor
    Pricing Schedule</strong> and an <strong>Appendix</strong> of guide prices.</p>
  {vk('The three documents, and variations')}
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:1.1mm 0 0.4mm;">The Baseline Cost Plan <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_02_The_Baseline_Cost_Plan.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:1.5mm;">Is a priced bill of quantities, eliminating possible variations. e.g. Cavity wall insulation &mdash; wall area 90&thinsp;m&sup2;, blown bonded bead to the 50&thinsp;mm cavity, making good included. Not included: room ventilation and air intake vents. It also acts as a budget guide for the homeowner
    throughout the works.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:1.1mm 0 0.4mm;">The Pricing Schedule <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_03_The_Pricing_Schedule.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:1.5mm;">Is tendered to the contractor. It is a baseline bill of quantities with a
    defined scope. e.g. Cavity wall insulation &mdash; wall area 90&thinsp;m&sup2;, blown bonded bead to the 50&thinsp;mm cavity, making good included. Not included: room ventilation and air intake vents.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:1.1mm 0 0.4mm;">Variations</div>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:1.5mm;">Are required measures that are not included in the Baseline Cost Plan.
    Post survey, the contractor can add required variations to the Pricing Schedule.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:1.1mm 0 0.4mm;">The Appendix <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_04_The_Appendix.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:1.5mm;">Is a list of priced variations which empowers the homeowner to finalise a
    deal with the contractor. The Appendix also includes the scope of each measure included in the
    Baseline Cost Plan.</p>
  <p class="body" style="font-size:11pt;line-height:1.40;margin:1.6mm 0 1mm;font-weight:600;color:#1E293B;">PlanitBER enables both
    parties to achieve mutual agreement. Confidence in the agreement empowers the homeowner to proceed.</p>

  {vk('Some of the problems it solves')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Issued before a contractor is contacted, the <strong>Baseline Cost Plan</strong>,
    <strong>Pricing Schedule</strong> and <strong>Appendix</strong> put the same scope and the same
    starting figure in front of both sides.</p>
  <table style="width:100%;border-collapse:collapse;table-layout:fixed;margin-top:0.6mm;">
    <colgroup><col style="width:47%"/><col style="width:6%"/><col style="width:47%"/></colgroup>
    <tr>
      <td style="font-size:7.6pt;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#8090A8;padding:0 0 1.4mm;">The problem</td>
      <td></td>
      <td style="font-size:7.6pt;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#8090A8;padding:0 0 1.4mm;">How the documents answer it</td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Grants look like they inflate the price</div>When every figure a homeowner sees comes from the contractors quoting, the grant becomes invisible margin and nobody can show whether it happens.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A baseline before any contractor names a price</div>The missing piece is not an increase in grants but a baseline that exists first &mdash; independently produced by the energy assessor from a published rate book.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Nothing to judge a quote against</div>No scope, no quantities, no sense of what the work should cost, so the decision rests on trust alone. That is where homeowners stall: told what they should do but unsure of grants and what it could cost.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A reference point for every quote</div>The <strong>Baseline Cost Plan</strong> and <strong>Pricing Schedule</strong> give both sides a basis to negotiate on. Every contractor prices the same scope and quantities, so quotes compare like with like.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Variations are argued, not agreed</div>When a contractor&rsquo;s survey finds work the quote did not cover, the homeowner has no idea what it should cost.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A guide price for everything not included</div>The <strong>Appendix</strong> prices every item marked not included, so when one is needed the homeowner agrees the variation from a figure they already hold.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">The contractor&rsquo;s work goes unpaid</div>Site visits are made and quotations prepared for homeowners who do not yet know whether they can afford to proceed, because they do not know what it will cost and are guessing.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.5mm 3mm 1.6mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Fewer wasted visits, fewer dead quotations</div>The three documents prime the homeowner for what the work should cost, so the contractor meets someone who has already decided they are comfortable with proceeding.</div></td>
    </tr>
  </table>

  {footer(1, '1', '2')}
</div>

<div class="sheet">
  {strip(1)}

  {vk('The BER Assessor workflow')}
  {wfstep('1', 'Survey and agree the measures',
    'The assessor surveys the dwelling, counts the rooms on each floor, notes the roof form and its gables, and agrees the intended measures with the homeowner.')}
  {wfstep('2', 'The dwelling goes into DEAP',
    'The house as it stands is entered, then the agreed measures are added until the heat loss '
    'indicator suits the intended heating system.')}
  {wfstep('3', 'The report goes into PlanitBER',
    'The standard DEAP dwelling details report, as issued today. Its geometry and heat loss indicator '
    'are taken from the report and used, along with the selected measures, to create three bespoke '
    'documents for each house.',
    add=True)}
  {wfstep('4', 'Issued to the homeowner',
    'The three documents go out with the dwelling details report. The homeowner holds their '
    'baseline scope, schedule and guide prices, so they can tender with confidence.',
    last=True)}

  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:3.4mm 0 0.5mm;">The Software</div>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Live and running: the survey goes in, the measures are selected, the
    three documents print, and the grant route can be switched at the moment of download. Document 05 shows the journey on screen and, behind it, the rate
    book the figures come from.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Every figure in a plan comes from a rate
    book with a version number and an effective date. Base rates are taken from the SCSI Tender Price
    Index and House Rebuilding Guide; labour from the SEO construction sector wage agreement, at the
    second-phase rates effective 1 August 2026; the county multiplier from the SCSI Regional Cost
    Supplement; grants at SEAI&rsquo;s published amounts; and VAT as Revenue applies it. Each block of the
    book names its own source beneath it. The book is held in one place, by SEAI, so the assessor prices from it and cannot change it, and every plan is priced on the same
    rates. Any rate still to be calibrated is marked as such, so recorded outcomes during a pilot can settle it.</p>

  {vk('What we are asking for')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">A meeting to demonstrate the software live. The measures go in, the
    documents print, and every figure can be traced to its source on screen.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">From there, we would like to discuss a pilot: a fixed number of
    plans, with recorded spend measured against the estimates, and SEAI holding full access to the data.
    If the pilot shows what we expect, the next step is participation in the NAS Trusted Partner API
    trial. Households which already hold a BER but have not gone ahead could then be offered the three
    documents, with their consent, and the trial would measure how many commit.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Behind PlanitBER are registered BER assessors, years of tendering
    experience and software built for this purpose. More retrofits is the aim and it is
    SEAI&rsquo;s target as much as ours.</p>

  <div style="margin-top:3mm;font-size:9pt;line-height:1.7;">
    <span style="font-weight:700;color:#1E293B;">John Turley</span>
    <span style="color:#64748B;"> &middot; SEAI-registered BER assessor, reg. 100615 &middot; 087 981 0150 &middot; mc2rating@gmail.com</span>
  </div>

  {footer(1, '2', '2')}
</div>'''

# ── 05 · THE SOFTWARE — part one, the journey on screen ──────────────────────
def appfig(key, w, lead, rest):
    return f'''<div class="appshot" style="width:{w};margin:0 auto 2mm;">
      <img src="{IMG[key]}" alt="">
      <div class="ac" style="font-size:8pt;"><strong>{lead}</strong> {rest}</div>
    </div>'''

doc6 = f'''<div class="sheet">
  {strip(5)}
  <h2>The software behind it</h2>
  <p class="body" style="font-size:9pt;margin-bottom:2.5mm;">Live software, in two parts.
    <strong>Part one</strong> is the journey on screen: the dwelling details report is read, the measures
    are ticked, the grant route is chosen, and the three documents print at the end. <strong>Part two</strong> is the rate book behind those
    figures, which the assessor can open but not edit.</p>
  <div class="kick" style="margin-top:3mm;">Part one &mdash; the journey on screen</div>

  {appfig('home', '152mm', '1 &middot; Choose the project type.',
    'New Build, Refurbishment and Energy Upgrade share one engine and one rate base.')}
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('ddr', '150mm', '2 &middot; The dwelling details report goes in.',
    'The DEAP report is read on the assessor&rsquo;s own computer &mdash; it is not uploaded and nothing is sent anywhere. It fills the address, the dwelling and every measured area, checks each table against the report&rsquo;s own total, and asks for the few counts a report cannot carry: rooms, wet rooms, perimeter and gable ends.')}

  <div class="fine">Screens from the live software, September 2026, unedited. The report read here is a sample written for this pack, not a client&rsquo;s.</div>
  {footer(5, '1', '8')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="arrowrow" style="padding:0 0 1.5mm;">{DOWN_ARROW}</div>
  {appfig('ddrtabs', '138mm', '3 &middot; What it filled, open to edit.',
    'Every element keeps its own card, named as the report names it, so ceiling-level and rafter-level roofs are priced as what they are. Anything the survey finds different is typed over.')}
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('sel', '152mm', '4 &middot; The measures go in.',
    'Every measure to be carried out is ticked. Quantities come from the geometry already entered, the sidebar fills as it goes in, and nothing is measured twice.')}

  <div class="fine">Screens from the live software, September 2026, unedited.</div>
  {footer(5, '2', '8')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="arrowrow" style="padding:0 0 1.5mm;">{DOWN_ARROW}</div>
  <div class="appshot" style="margin-bottom:2mm;">
    <img src="{IMG['routes']}" alt="">
    <div class="ac" style="font-size:8pt;"><strong>5 &middot; The grant route, chosen on the figures.</strong>
      Three tiles, one per SEAI route &mdash; the same measured works in each, the scheme fee and the grants
      changing, and the route that leaves least to fund marked. The homeowner picks a route knowing exactly
      what each one leaves them to pay &mdash; before the plan is issued.</div>
  </div>
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('appplan', '162mm', '6 &middot; The plan on screen.',
    'The baseline fixed at issue, the grant named on every line, and the live half ready to record quotes and payments as the job runs.')}

  <div class="fine">Screens from the live software, September 2026, unedited.</div>
  {footer(5, '3', '8')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="arrowrow" style="padding:0 0 1.5mm;">{DOWN_ARROW}</div>
  <h2 style="font-size:14pt;"><span style="color:#B07D1A;">7 &middot;</span> All the way to print</h2>
  <p class="body" style="font-size:9pt;margin-bottom:2.5mm;">Three buttons, one for each document. Each
    opens the browser&rsquo;s own print dialog on its own, ready to print on paper or save as a PDF &mdash;
    they go to different people, so they never print as one bundle.</p>
  <div class="appshot">
    <img src="{IMG['routedl']}" alt="">
    <div class="ac" style="font-size:8pt;"><strong>The grant route, switchable at the moment of download.</strong>
      The selector sits beside the download buttons: change the route and the plan re-prices there and
      then &mdash; same measured works, the scheme fee and grants updating &mdash; with the homeowner
      watching. Nothing is locked in until the paper prints.</div>
  </div>
  <div class="appshot" style="margin-top:2mm;">
    <img src="{IMG['preview']}" alt="">
    <div class="ac" style="font-size:8pt;"><strong>The print preview, exactly as the assessor sees it.</strong>
      The document in this pack is this print &mdash; nothing is retouched between the screen and the
      paper.</div>
  </div>

  <div class="kick" style="margin-top:4mm;">What prints from this screen</div>
  <div class="big3">
    <div class="pt asr">
      <div class="pt-t" style="font-size:9.5pt;">The Baseline Cost Plan</div>
      <div class="pt-b">For the homeowner, issued with the BER and worked from for the length of
        the job.</div>
    </div>
    <div class="pt ho">
      <div class="pt-t" style="font-size:9.5pt;">The Contractor Pricing Schedule</div>
      <div class="pt-b">One copy for each contractor asked to quote, priced and returned.</div>
    </div>
    <div class="pt se">
      <div class="pt-t" style="font-size:9.5pt;">The Appendix</div>
      <div class="pt-b">The homeowner&rsquo;s reference, fixed at issue &mdash; the workings behind
        every figure.</div>
    </div>
  </div>

  <div class="fine">Screens from the live software, September 2026, unedited.</div>
  {footer(5, '4', '8')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="kick">Part two &mdash; the rate book behind it</div>
  <h2 style="font-size:21pt;margin-bottom:3mm;">Where the figures come from</h2>
  <p class="body" style="font-size:10.4pt;line-height:1.55;max-width:172mm;margin-bottom:3mm;">Every figure in a plan comes from a rate book with a version number and
    an effective date. The assessor prices from it and cannot change it: the book is held in one place and
    published by one administrator, SEAI, so every plan is priced on the
    same rates. Base rates come from the SCSI Tender Price Index and House Rebuilding Guide; labour from
    the SEO Construction Sector wage agreement, at the second-phase rates effective 1 August 2026; the
    county multiplier from the SCSI Regional Cost Supplement; grants at SEAI&rsquo;s published amounts;
    VAT as Revenue applies it. Each block names its own source beneath it, and any rate still to be
    calibrated is marked, so recorded outcomes during a pilot can settle it.</p>
  <p class="body" style="font-size:10.4pt;line-height:1.55;max-width:172mm;margin-bottom:3mm;">The pages that follow are that book as it appears on screen: the labour
    rates and the grant table first, then the unit rates, top to bottom.</p>
  {appfig('rates', '140mm', 'Labour, at the SEO August 2026 rates.',
    'Every labour rate and county multiplier visible, each with its source. Nothing is a black box.')}
  <div class="fine">{FINE1}</div>
  {footer(5, '5', '8')}
</div>'''

# ── 05 · THE SOFTWARE — part two, the rate book behind it ────────────────────
# One capture of the whole EU Rates tab, cut on section boundaries so no table is split.
# The third page is the not-included guide rates: the engine behind the figures the
# homeowner holds for variations, which is the part of the message document 04 makes.
ENG_P = 'font-size:10.4pt;line-height:1.55;max-width:172mm;margin-bottom:3mm;'
def engfig(key, w, lead, rest):
    return f'''<div class="appshot" style="width:{w};margin:0 auto 2mm;">
      <img src="{IMG[key]}" alt="">
      <div class="ac" style="font-size:8pt;"><strong>{lead}</strong> {rest}</div>
    </div>'''

doc7 = f'''<div class="sheet">
  {strip(5)}
  {appfig('grants', '140mm', 'The SEAI grant table the plans draw from.',
    'Every amount dated and visible &mdash; when SEAI changes a rate, one number changes and every new plan follows.')}
  {engfig('eng_a', '140mm', 'Walls, heat pump and ventilation.',
    'Category uplift by trade on the left; supply-only material rates on the right, the published figure in every box and the source under each group.')}
  <div class="fine">{FINE1}</div>
  {footer(5, '6', '8')}
</div>

<div class="sheet">
  {strip(5)}
  {engfig('eng_b', '140mm', 'Fascia and soffit, ventilation units, windows and doors, solar PV and battery, and the attic ancillaries.',
    'The frame and style multipliers for windows are written out under the table, so a triple-glazed alu-clad sash window can be traced from the base rate. The attic ancillaries are the items every attic top-up carries as standard: the tank jacket, the pipe lagging, the walkway and the storage deck.')}
  <div class="fine">Screens from the live software, September 2026, unedited.</div>
  {footer(5, '7', '8')}
</div>

<div class="sheet">
  {strip(5)}
  <h2 style="font-size:16pt;margin-bottom:2mm;">The not-included rates</h2>
  <p class="body" style="{ENG_P}">This is the engine behind the guide prices in the Appendix. Every item a
    measure leaves out is priced here, per unit, with the measure it belongs to named beside it. When a
    contractor proposes a variation, the figure the homeowner holds against it comes from this table; and
    when an item is ticked into a plan after the survey, its priced line uses the same rate. One number, in
    one place, feeding both.</p>
  {engfig('eng_c', '140mm', 'Variations &mdash; not included guide rates.',
    'Material per unit, labour from the Labour Rates tab, loaded like the plan: overhead and profit at 12%, then VAT. The flag at the foot marks a rate still to be calibrated against recorded outcomes.')}
  <div class="fine">Screens from the live software, September 2026, unedited.</div>
  {footer(5, '8', '8')}
</div>'''

# ── 06 · DATA PROTECTION — where the data lives, and what is owed to the homeowner ─
# Written from what the software actually does, checked against the file before printing:
# no account, no server, no database, nothing transmitted but the typefaces the page is set
# in. Every sentence here has to stay true of the build that ships with the pack.
docdp = f'''<div class="sheet">
  {strip(6)}
  <h1 style="font-size:16pt;line-height:1.2;margin:1mm 0 1.6mm;">Data protection and the homeowner&rsquo;s data</h1>
  <p class="body" style="font-size:9.6pt;line-height:1.5;margin-bottom:2mm;">PlanitBER is one file that runs
    in the assessor&rsquo;s own browser. There is no account to create, no server to sign in to and no database
    behind it. The dwelling details report is read on that computer and is never uploaded; the plan is built
    there and printed there. That is a design decision, not a configuration, and it decides most of what
    follows: the homeowner&rsquo;s data stays with the assessor they engaged.</p>

  {vk('Every piece of data, and where it lives')}
  <table class="mapt">
    <tr><th style="width:27%;">What is held</th><th style="width:29%;">Why it is needed</th><th>Where it is, and who else can see it</th></tr>
    <tr><td class="m">Homeowner name and site address</td><td>To address the three documents and identify the dwelling</td><td>Typed into the browser and kept in that browser&rsquo;s own storage on that computer, and printed on the documents. Nobody else sees it unless the assessor sends the documents on.</td></tr>
    <tr><td class="m">The dwelling details report</td><td>Read for the measured geometry and the heat loss indicator</td><td>Opened from the assessor&rsquo;s own disk and read inside the page. The file is never uploaded, never copied and never seen by anybody else.</td></tr>
    <tr><td class="m">Measured areas and elements, room and vent counts</td><td>To quantify and price the works</td><td>The same browser storage, and the printed documents. The quantities &mdash; not the homeowner&rsquo;s name &mdash; reach the contractors asked to price, through the Pricing Schedule.</td></tr>
    <tr><td class="m">BER rating, age band, heat loss indicator</td><td>To size the heat pump and choose the grant route</td><td>The same again. These come from the dwelling details report and are not asked of the homeowner.</td></tr>
    <tr><td class="m">The three printed documents</td><td>The purpose of the exercise</td><td>Given to the homeowner, who decides who else sees them; a copy kept by the assessor with the BER records for that dwelling.</td></tr>
  </table>

  {vk('What the software never asks for')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">No PPS number, no date of birth,
    no bank, card or payment details, no income or means information, no photographs of the dwelling or its
    occupants, and no special category data of any kind. No children&rsquo;s data is sought or used. The software
    carries no analytics, no tracking, no cookies and no telemetry: it does not count its own users, and it
    cannot, because nothing reports back to anybody.</p>

  {vk('Who is responsible')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">The BER assessor is the
    <strong>data controller</strong> for the homeowner&rsquo;s personal data: they collect it, they hold it, they
    decide what is done with it, and the homeowner engaged them. There is no processor, because there is no
    service &mdash; the software runs on the assessor&rsquo;s own equipment, in the way a spreadsheet does. If a
    hosted version is ever offered, that creates a processor relationship, and a written data processing
    agreement and a completed DPIA would come before it, not after.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.46;">In a pilot, SEAI would be a controller of what it
    receives &mdash; which is aggregated and anonymised, as page three sets out.</p>

  <div class="fine">Document 06 describes the build issued with this pack. It is written to be checked:
    every statement here can be tested by opening the software and watching what it asks of the network.</div>
  {footer(6, '1', '3')}
</div>

<div class="sheet">
  {strip(6)}
  {vk('Lawful basis')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">The homeowner&rsquo;s data is
    processed to perform the contract they entered into with the assessor &mdash; Article 6(1)(b) &mdash; and for
    no other purpose. Nothing is processed on the basis of legitimate interests for marketing, profiling or
    resale, because none of those happen. Anything shared with SEAI during a pilot rests on the
    homeowner&rsquo;s consent, recorded before it is shared and withdrawable afterwards; a withdrawal removes
    them from the next return, and the data already aggregated cannot identify them to begin with.</p>

  {vk('How long it is kept')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">A saved project sits in the
    browser on the assessor&rsquo;s computer until it is deleted there; the printed documents are kept with the
    assessor&rsquo;s BER records for that dwelling, for the period SEAI&rsquo;s Code of Practice requires of a
    registered assessor, and are then destroyed. A short written retention schedule, naming that period and who
    carries it out, is one of the items listed on page three.</p>

  {vk('The homeowner&rsquo;s rights, and how each is met')}
  <table class="mapt">
    <tr><th style="width:26%;">The right</th><th>How it is met</th></tr>
    <tr><td class="m">Access</td><td>The assessor holds everything in one place and can give a copy of the project and the three documents on request</td></tr>
    <tr><td class="m">Rectification</td><td>Every figure the report filled can be typed over and the documents reissued; nothing is locked</td></tr>
    <tr><td class="m">Erasure</td><td>The saved project is deleted in the browser and the document copies destroyed, subject only to records a registered assessor is required to keep</td></tr>
    <tr><td class="m">Portability</td><td>The three documents are the data in a readable form, and they are the homeowner&rsquo;s already</td></tr>
    <tr><td class="m">Objection and restriction</td><td>Addressed to the assessor, who is the controller; there is no second party to approach</td></tr>
  </table>

  {vk('Security')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">The design removes most of what
    is usually attacked: there are no accounts to compromise, no password to leak, no API to abuse and no
    central store to breach. What remains is ordinary and physical &mdash; the assessor&rsquo;s own computer. The
    controls are therefore device controls: full-disk encryption, a locking screen, current operating system
    updates, and encrypted backup. The real exposure is the one every practice has: documents sent to
    homeowners and contractors by email. They carry a name, an address and a scope of works, and they are sent
    deliberately, to people entitled to them.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">The page makes one request of
    anyone else when it opens &mdash; for the two typefaces it is set in. It carries no project data, only the
    fact that a browser asked for a font. Those files will be served from the software itself before any
    pilot, after which an ordinary session reaches nobody at all. A spreadsheet library is fetched only if
    somebody exports a spreadsheet, and it too carries nothing out.</p>

  {vk('If something goes wrong')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;">A breach here would be a lost or stolen computer, a
    document sent to the wrong address, or a backup left unprotected. Any of these is recorded in a breach log
    with what happened, what data was involved and what was done; where there is a risk to the people
    concerned, the Data Protection Commission is notified within 72 hours and the homeowner told without undue
    delay where the risk is high.</p>

  <div class="fine">The controls described here are the assessor&rsquo;s own, because the data never leaves the
    assessor&rsquo;s own equipment.</div>
  {footer(6, '2', '3')}
</div>

<div class="sheet">
  {strip(6)}
  {vk('What changed before this pack was issued')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">An earlier build offered an
    optional cloud save: a project could be written to a hosted database and reloaded elsewhere with an
    eight-character code. It was convenient and it was wrong &mdash; anyone holding the code could read the
    project, and nothing expired. It was removed on 8 October 2026, before this pack was issued and before any
    pilot. The current software has no path to any database; the projects that feature stored are being
    deleted from the hosted service it used.</p>

  {vk('The data protection impact assessment')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">A DPIA assesses a defined
    processing operation, so the honest position is this: as the software stands, no processing happens outside
    the assessor&rsquo;s own equipment and the threshold for a mandatory DPIA under Article 35 is not met. A full
    DPIA will be completed, and given to SEAI, <strong>before any pilot begins</strong> &mdash; because a pilot
    introduces processing that does not exist today. It would cover:</p>
  <div class="ticklist" style="margin-bottom:2.4mm;">
    <div class="tlh">What the DPIA will cover</div>
    <div class="tl"><span class="bx">&#10003;</span><span>The processing in scope: what is collected at survey, what is derived by the software, what is printed, and what would be returned to SEAI during the pilot.</span></div>
    <div class="tl"><span class="bx">&#10003;</span><span>Necessity and proportionality: why each field is needed to price the works, and what is deliberately not collected.</span></div>
    <div class="tl"><span class="bx">&#10003;</span><span>The aggregation and anonymisation method for pilot returns, and a test that an individual dwelling cannot be re-identified from them.</span></div>
    <div class="tl"><span class="bx">&#10003;</span><span>Consent: how it is sought, recorded and withdrawn, and what a withdrawal does.</span></div>
    <div class="tl"><span class="bx">&#10003;</span><span>Risks to the people concerned, the measures against each, and the residual risk accepted in writing.</span></div>
    <div class="tl"><span class="bx">&#10003;</span><span>Retention, deletion and the breach procedure, as a schedule rather than an intention.</span></div>
  </div>
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">It would be redone, not amended,
    if any of three things happened: a hosted version of the software, an integration with the NAS Trusted
    Partner API, or any decision about a household taken automatically from the data. None of the three is
    proposed today.</p>

  {vk('What SEAI would receive in a pilot')}
  <p class="body" style="font-size:9.2pt;line-height:1.46;margin-bottom:2mm;">Aggregated and anonymised
    figures, with the homeowner&rsquo;s consent: county, dwelling type and age band, the measures planned, the
    estimate, the grants, and &mdash; the point of the exercise &mdash; the recorded outcome against the estimate.
    No name, no address, no Eircode, no MPRN and no BER number. SEAI holds full access to that data, which is
    what makes the accuracy claim testable rather than asserted.</p>

  {vk('Open items, to be closed before a pilot')}
  <table class="mapt">
    <tr><th style="width:34%;">Item</th><th>What has to happen</th></tr>
    <tr><td class="m">Typefaces served locally</td><td>So an ordinary session makes no request of any third party at all</td></tr>
    <tr><td class="m">Retention schedule</td><td>One page: what is kept, for how long, by whom, and how it is destroyed</td></tr>
    <tr><td class="m">Full DPIA</td><td>Completed and given to SEAI before the first pilot plan is issued</td></tr>
    <tr><td class="m">Consent wording</td><td>Written for the homeowner, to be reviewed before use</td></tr>
    <tr><td class="m">Processing agreement</td><td>Only if a hosted version is ever offered; there is nothing to process today</td></tr>
  </table>

  <div class="fine">Prepared to be read alongside document 01. Comments on this document are welcome and
    expected: it is easier to settle the data questions before a pilot than during one.</div>
  {footer(6, '3', '3')}
</div>'''

TPL = '''<!doctype html><html><head><meta charset="utf-8"><title>%s</title>
<style>%s</style></head><body>%s</body></html>'''

for name, content in [('pack_01', doc1), ('pack_05', doc6 + doc7), ('pack_06', docdp)]:
    open(name + '.html', 'w').write(TPL % ('PlanitBER — ' + name, CSS, content))
    print('wrote', name + '.html')
