# The SEAI pack: six connected A4 PDFs sharing one design system.
#   01 The Value Proposition — text only: what it is, why, and where each other document fits
#   02 The Cost Plan         — a page of notes, then the Mullingar semi-D's plan bound behind
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
EX_ADDR   = '3 Bed Semi, Mullingar, Co. Westmeath'
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
        'The Appendix', 'The Software']
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
    arrow = '' if last else f'<div style="padding:1mm 0 0.6mm;">{DOWN_ARROW}</div>'
    # The existing steps are context, so they recede: grey discs, no accent edge. Gold is
    # spent on the one step being proposed, which is what the page is for.
    edge  = '#B07D1A' if add else '#D8D2C4'
    bg    = '#FFFAF0' if add else '#FFFFFF'
    disc  = '#B07D1A' if add else '#AEB4BE'
    ncol  = '#B07D1A' if add else '#A0A8B4'
    return f'''<div style="background:{bg};border:0.6pt solid #D8D2C4;border-left:{"3.6pt" if add else "2.4pt"} solid {edge};border-radius:2pt;padding:3.4mm 4.2mm;max-width:174mm;margin:0 auto;text-align:left;">
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
      <div style="color:#1E293B;font-weight:700;font-size:8.4pt;">Turley Energy Consultants</div>
      <div>Co. Monaghan &middot; info@turleyenergy.ie</div><div>[Date]</div>
    </div>
  </div>
  <h1 style="font-size:16pt;line-height:1.2;margin:2.6mm 0 1.6mm;">Empowering homeowners with tender
    documents to engage in the retrofit process with confidence</h1>
  <p class="body" style="font-size:9.8pt;line-height:1.46;margin-bottom:1.6mm;color:#1E293B;">PlanitBER
    is software that turns a provisional BER into homeowner tender documents. It takes the measured
    geometry and the Heat Loss Indicator from a Dwelling Details Report and applies rates to the measures
    agreed with the homeowner, producing a <strong>Baseline Cost Plan</strong>, a <strong>Contractors
    Pricing Schedule</strong> and an <strong>Appendix</strong> of guide prices.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">These three bespoke documents, issued with the provisional BER before a
    contractor has been contacted, designed to empower homeowners to engage with confidence in the
    retrofit process. Each measure on the <strong>Baseline Cost Plan</strong> carries a Baseline Scope
    &amp; Quantities and Budget Estimate column. Contractors then price against that same Baseline Scope
    &amp; Quantities, which is in the <strong>Contractors Pricing Schedule</strong>, so quotes compare
    like with like and include potential variations. The <strong>Appendix</strong> then serves the
    homeowner in two ways. It puts a guide price on every item marked &lsquo;not included&rsquo;, so if a
    contractor&rsquo;s survey finds one is needed, the homeowner already knows what it should cost before
    agreeing it. It also shows how each Baseline Budget Estimate was built &mdash; from measured
    quantities and published rates to the loaded figure &mdash; so no number on the plan is taken on
    trust.</p>

  {vk('Some of the problems it solves')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Issued before a contractor is contacted, the <strong>Baseline Cost Plan</strong>,
    <strong>Pricing Schedule</strong> and <strong>Appendix</strong> put the same scope and the same
    starting figure in front of both sides. A bigger grant solves none of what follows.</p>
  <table style="width:100%;border-collapse:collapse;table-layout:fixed;margin-top:0.6mm;">
    <colgroup><col style="width:47%"/><col style="width:6%"/><col style="width:47%"/></colgroup>
    <tr>
      <td style="font-size:7.6pt;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#8090A8;padding:0 0 1.4mm;">The problem</td>
      <td></td>
      <td style="font-size:7.6pt;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#8090A8;padding:0 0 1.4mm;">How the documents answer it</td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Grants look like they inflate the price</div>When every figure a homeowner sees comes from the contractors quoting, the grant becomes invisible margin, and nobody can show whether it happens.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A baseline before any contractor names a price</div>The missing piece is not an increase in grants but a baseline that exists first &mdash; independently produced by the energy assessor from a published rate book.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Nothing to judge a quote against</div>No scope, no quantities, no sense of what the work should cost, so the decision rests on trust alone. That is where homeowners stall: told what to do, with no way to price it.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A reference point for every quote</div>The <strong>Baseline Cost Plan</strong> and <strong>Pricing Schedule</strong> give both sides a basis to negotiate on. Every contractor prices the same scope and quantities, so quotes compare like with like.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Variations are argued, not agreed</div>When a contractor&rsquo;s survey finds work the quote did not cover, the homeowner has no idea what it should cost.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">A guide price for everything not included</div>The <strong>Appendix</strong> prices every item marked not included, so when one is needed the homeowner agrees the variation from a figure they already hold.</div></td>
    </tr>
    <tr>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFFFF;border-left:2.4pt solid #D8D2C4;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">The contractor&rsquo;s work goes unpaid</div>Site visits are made and quotations prepared for homeowners who have not yet decided what they can afford, and much of that work is never answered.</div></td>
      <td style="width:6%;vertical-align:middle;padding:0 0 1.4mm;">{RIGHT_ARROW}</td>
      <td style="width:47%;vertical-align:top;padding:0 0 1.4mm;"><div style="border:0.6pt solid #D8D2C4;border-radius:2pt;padding:1.8mm 3mm 1.9mm;font-size:8.4pt;line-height:1.36;color:#3F4A5A;background:#FFFAF0;border-left:3.6pt solid #B07D1A;"><div style="font-family:'Fraunces',Georgia,serif;font-size:9.9pt;font-weight:800;color:#1E293B;line-height:1.15;margin-bottom:1mm;">Fewer wasted visits, fewer dead quotations</div>The three documents prime the homeowner for what the work should cost, so the contractor meets someone who has already decided they are comfortable with proceeding.</div></td>
    </tr>
  </table>

  <div class="fine">{FINE1}</div>
  {footer(1, '1', '3')}
</div>

<div class="sheet">
  {strip(1)}

  {vk('What each document is for')}
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:2.2mm 0 0.8mm;">The Baseline Cost Plan <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_02_The_Baseline_Cost_Plan.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The document the homeowner works from for the length of the job.
    Every measure carries its scope, the grant it earns and a budget estimate, all fixed at the date of
    issue, and beside them a live half left blank for quotes, variations and what was actually paid. It is
    the reference the homeowner keeps, not a quote and not a tender return.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:2.2mm 0 0.8mm;">The Pricing Schedule <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_03_The_Pricing_Schedule.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The same measured scope with every figure removed, issued to each
    contractor asked to quote. Because they all price the same scope and the same quantities, the returns
    compare like with like, and anything a contractor&rsquo;s own survey finds beyond that scope is entered
    as a variation rather than buried in a single number.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:2.2mm 0 0.8mm;">The Appendix <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_04_The_Appendix.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The arithmetic behind the plan and the guide prices for what it
    deliberately leaves out. Materials and labour, the contractor&rsquo;s overhead and profit, and the VAT
    band, measure by measure &mdash; so the homeowner can see how a figure was reached, and holds a guide
    price before a variation is ever discussed.</p>
  <div style="font-size:9.6pt;font-weight:700;color:#1E293B;margin:2.2mm 0 0.8mm;">The Software <span style="font-weight:400;font-size:7.8pt;color:#64748B;letter-spacing:.01em;">&nbsp;&middot;&nbsp; PlanitBER_05_The_Software.pdf</span></div>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Live and running after close to a year in development: the survey
    goes in, the intended measures are selected, the three documents print, and the grant route can be
    switched at the moment of download. Document 05 shows the journey on screen and, behind it, the rate
    book the figures come from.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>The rate settings.</strong> Every figure in a plan comes from a rate
    book with a version number and an effective date. Base rates are taken from the SCSI Tender Price
    Index and House Rebuilding Guide; labour from the SEO construction sector wage agreement, at the
    second-phase rates effective 1 August 2026; the county multiplier from the SCSI Regional Cost
    Supplement; grants at SEAI&rsquo;s published amounts; and VAT as Revenue applies it. Each block of the
    book names its own source beneath it. The book is held in one place &mdash; under the pilot, by SEAI
    &mdash; so the assessor prices from it and cannot change it, and every plan is priced on the same
    rates. Any rate still to be calibrated is marked as such, so recorded outturns can settle it.</p>

  <div class="fine">{FINE1}</div>
  {footer(1, '2', '3')}
</div>

<div class="sheet">
  {strip(1)}

  {vk('The BER Assessor workflow')}
  {wfstep('1', 'Survey and agree the measures',
    'The assessor surveys the dwelling and agrees the intended measures with the homeowner.')}
  {wfstep('2', 'The dwelling goes into DEAP',
    'The house as it stands is entered, then the agreed measures are added until the heat loss '
    'indicator suits the intended heating system.')}
  {wfstep('3', 'The report goes into PlanitBER',
    'The standard DEAP dwelling details report, as issued today. Its geometry and heat loss indicator '
    'fill the survey, the upgraded measures are selected, and the three documents are produced.',
    add=True)}
  {wfstep('4', 'Issued to the homeowner',
    'The three documents go out with the dwelling details report and the assessor&rsquo;s invoice for '
    'the advisory work. The homeowner holds their heat loss indicator, the scope and the guide prices, '
    'and can tender with confidence.')}
  {wfstep('5', 'The works happen and the final BER is issued',
    'The final BER is commissioned after the works, as it is today, and the grants are claimed '
    'against it.',
    last=True)}

  {vk('What we are asking for')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">A meeting to demonstrate the software live. The measures go in, the
    documents print, and every figure can be traced to its source on screen.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">From there, we would like to discuss a small pilot &mdash; a fixed number
    of plans, with recorded spend measured against the estimates and SEAI holding full access to the data
    &mdash; and, if the pilot shows what we expect, participation in the NAS Trusted Partner API trial.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The practice combines registered BER assessors, years of tendering
    experience, and the software built for this purpose. More retrofits is the aim, and it is
    SEAI&rsquo;s target as much as ours.</p>

  <div style="margin-top:3mm;font-size:9pt;line-height:1.7;">
    <span style="font-weight:700;color:#1E293B;">[Name] &middot; Turley Energy Consultants</span>
    <span style="color:#64748B;"> &middot; SEAI-registered BER assessor &middot; [Phone] &middot; info@turleyenergy.ie</span>
  </div>

  <div class="fine">{FINE1}</div>
  {footer(1, '3', '3')}
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
    <strong>Part one</strong> is the journey on screen: the survey goes in, the grant route is chosen,
    and the three documents print at the end. <strong>Part two</strong> is the rate book behind those
    figures, which the assessor can open but not edit.</p>
  <div class="kick" style="margin-top:3mm;">Part one &mdash; the journey on screen</div>

  {appfig('home', '152mm', '1 &middot; Choose the project type.',
    'New Build, Refurbishment and Energy Upgrade share one engine and one rate base.')}
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('sel', '152mm', '2 &middot; The survey becomes a project.',
    'DEAP geometry, the measures the homeowner wants, the county and the grant scheme &mdash; the status bar and sidebar fill as it goes in, and nothing is measured twice.')}

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '1', '7')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="arrowrow" style="padding:0 0 1.5mm;">{DOWN_ARROW}</div>
  <div class="appshot" style="margin-bottom:2mm;">
    <img src="{IMG['routes']}" alt="">
    <div class="ac" style="font-size:8pt;"><strong>3 &middot; The grant route, chosen on the figures.</strong>
      Three tiles, one per SEAI route &mdash; the same measured works in each, the scheme fee and the grants
      changing, and the route that leaves least to fund marked. The homeowner picks a route knowing exactly
      what each one leaves them to pay &mdash; before the plan is issued.</div>
  </div>
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('appplan', '162mm', '4 &middot; The plan on screen.',
    'The baseline fixed at issue, the grant named on every line, and the live half ready to record quotes and payments as the job runs.')}

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '2', '7')}
</div>

<div class="sheet">
  {strip(5)}
  <div class="arrowrow" style="padding:0 0 1.5mm;">{DOWN_ARROW}</div>
  <h2 style="font-size:14pt;"><span style="color:#B07D1A;">5 &middot;</span> All the way to print</h2>
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

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '3', '7')}
</div>

<div class="sheet">
  {strip(5)}
  {appfig('rates', '134mm', '6 &middot; Rate Settings, open to inspection.',
    'Labour at the SEO August 2026 rates &mdash; every unit price, labour rate and county multiplier visible, each with its source. Nothing is a black box.')}
  {appfig('grants', '134mm', '7 &middot; The SEAI grant table the plans draw from.',
    'Every amount dated and visible &mdash; when SEAI changes a rate, one number changes and every new plan follows.')}

  <p class="body" style="font-size:8pt;color:#64748B;margin-top:2mm;">Where each rate comes from, and how the
    book is versioned and inspected, is in part two of this document.</p>

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '4', '7')}
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
  <div class="kick">Part two &mdash; the rate book behind it</div>
  <h2 style="font-size:21pt;margin-bottom:3mm;">Where the figures come from</h2>
  <p class="body" style="{ENG_P}">Every figure in a plan comes from a rate book with a version number and
    an effective date. The assessor prices from it and cannot change it: the book is held in one place and
    published by one administrator &mdash; under the pilot, SEAI &mdash; so every plan is priced on the
    same rates. The three pages that follow are that book, top to bottom, exactly as it appears on screen.</p>
  <p class="body" style="{ENG_P}"><strong>Where the rates come from.</strong> Base rates from the SCSI
    Tender Price Index and House Rebuilding Guide; labour from the SEO Construction Sector wage agreement,
    at the second-phase rates effective 1 August 2026; the county multiplier from the SCSI Regional Cost
    Supplement; grants at SEAI&rsquo;s published amounts; VAT as Revenue applies it. Each block names its
    own source beneath it.</p>
  <p class="body" style="{ENG_P}"><strong>Held in one place.</strong> Every rate shows its published value and
    its source. A change is made once, centrally, and every plan priced afterwards follows. The panel
    marks any rate still to be calibrated, so the pilot&rsquo;s recorded outturns can settle it.</p>
  {engfig('eng_a', '156mm', 'Walls, heat pump and ventilation.',
    'Category uplift by trade on the left; supply-only material rates on the right, the published figure in every box and the source under each group.')}
  <div class="fine">{FINE1}</div>
  {footer(5, '5', '7')}
</div>

<div class="sheet">
  {strip(5)}
  {engfig('eng_b', '172mm', 'Fascia and soffit, ventilation units, windows and doors, solar PV and battery, and the attic ancillaries.',
    'The frame and style multipliers for windows are written out under the table, so a triple-glazed alu-clad sash window can be traced from the base rate. The attic ancillaries are the items every attic top-up carries as standard: the tank jacket, the pipe lagging, the walkway and the storage deck.')}
  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '6', '7')}
</div>

<div class="sheet">
  {strip(5)}
  <h2 style="font-size:16pt;margin-bottom:2mm;">The not-included rates</h2>
  <p class="body" style="{ENG_P}">This is the engine behind the guide prices in the Appendix. Every item a
    measure leaves out is priced here, per unit, with the measure it belongs to named beside it. When a
    contractor proposes a variation, the figure the homeowner holds against it comes from this table; and
    when an item is ticked into a plan after the survey, its priced line uses the same rate. One number, in
    one place, feeding both.</p>
  {engfig('eng_c', '172mm', 'Variations &mdash; not included guide rates.',
    'Material per unit, labour from the Labour Rates tab, loaded like the plan: overhead and profit at 12%, then VAT. The flag at the foot marks a rate still to be calibrated against recorded outturns.')}
  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(5, '7', '7')}
</div>'''

TPL = '''<!doctype html><html><head><meta charset="utf-8"><title>%s</title>
<style>%s</style></head><body>%s</body></html>'''

for name, content in [('pack_01', doc1), ('pack_05', doc6 + doc7)]:
    open(name + '.html', 'w').write(TPL % ('PlanitBER — ' + name, CSS, content))
    print('wrote', name + '.html')
