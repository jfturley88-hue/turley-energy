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

# Six documents. Three of them (02-04) are the software's own output bound in whole, each
# behind a short page of notes saying who it is for and how long it lives; the other three
# are the argument, the workflow and the software itself.
DOCS = ['The Value Proposition', 'The Cost Plan', 'The Pricing Schedule',
        'The Appendix', 'The Workflow', 'The Software', 'The Engine']
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
  <h1 style="font-size:17.5pt;line-height:1.18;margin:4mm 0 2mm;">Empowering homeowners with tender documents to engage in the retrofit process with confidence</h1>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Three bespoke documents,
    issued with the provisional BER. Each measure carries a <strong>benchmark</strong> &mdash; an
    estimate with what&rsquo;s included and what&rsquo;s not. Contractors price that scope on the
    <strong>schedule</strong>, so quotes compare like with like. Variations get agreed rather than argued,
    because the homeowner already holds guide prices for the not-included items in the
    <strong>appendix</strong>. That empowers the homeowner and levels the playing field.</p>

  {vk('Why it is needed')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>The common belief is that grants inflate the price.</strong> When every
    figure a homeowner sees comes from the contractors quoting, the grant becomes invisible margin, and
    nobody can show whether it happens. The missing piece is not more money but a benchmark that exists
    before any contractor names a price.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>Trust between homeowner and contractor has nowhere to
    start.</strong> A quote today is one number, with nothing to check it against. The homeowner is
    empowered with the scope each measure includes and a guide price for what it leaves out &mdash; both
    held before a contractor is asked to price anything. A quote is judged against that scope, and the
    honest contractor is judged on the same terms as everyone else quoting.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>The energy assessor becomes a paid consultant.</strong> A fee
    for helping the homeowner create the document, earned at the moment the retrofit decision is being
    made &mdash; not for selling installation or taking commission, so the figure does not move with who
    wins the work. The same survey and the same provisional BER now also produce the three documents.</p>

  {vk('The three documents &mdash; 02, 03 and 04')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The <strong>Cost Plan</strong> the homeowner works from, the blank
    <strong>Pricing Schedule</strong> their contractors quote on, and the <strong>Appendix</strong>
    behind both &mdash; each bound in full behind a page of notes, exactly as the software prints it.
    Every figure traces to this house rather than a house of its type.</p>

  {vk('The workflow &mdash; document 05')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">The workflow already happens &mdash; assessment, measures agreed with the
    homeowner, provisional report, works, post-works BER. The provisional report stage is expanded: it now
    also produces the three documents, issued to the homeowner together with the report.</p>

  {vk('The software and the engine &mdash; documents 06 and 07')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;">Live and running after close to a year in development: the survey goes in, the intended measures are
    selected, the three documents print, and the grant route can be switched at the moment of download. Behind it sits a rate book with a version and an effective date, sourced line by line and held in one place, with any rate still to be calibrated marked as such.</p>

  {vk('The proposition')}
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>A pilot programme.</strong> A few registered assessors, a fixed number
    of plans, with recorded spend measured against the accuracy band. SEAI observes throughout, and the
    outturns refine the rate book.</p>
  <p class="body" style="font-size:9.2pt;line-height:1.50;margin-bottom:2.1mm;"><strong>A trusted partnership.</strong> Plans generated from BER data
    through an API, so the three documents can be produced for any home on the register. The goal is
    SEAI&rsquo;s own: <strong>more retrofits.</strong></p>

  <div style="margin-top:3mm;font-size:9pt;line-height:1.7;">
    <span style="font-weight:700;color:#1E293B;">[Name] &middot; Turley Energy Consultants</span>
    <span style="color:#64748B;"> &middot; SEAI-registered BER assessor &middot; [Phone] &middot; info@turleyenergy.ie</span>
  </div>

  <div class="fine">{FINE1}</div>
  {footer(1)}
</div>'''

# ── 02 · THE COST PLAN — notes, then the real document bound behind ──────────
# One house priced three ways. Each of documents 02-04 opens with a page of notes saying
# who that document is for and how long it lives, then binds in the software's own print.
EX_HOUSE = (f'a {EX_AREA}&thinsp;m&sup2; 3-bed semi in Mullingar, Co. Westmeath, built {EX_BUILT}, '
            f'{EX_BER}, on {EX_SCHEME}')

def notes(n, title, lead, blocks, foot_pages='1'):
    body = ''.join(
        f'<p class="body" style="font-size:11.0pt;line-height:1.62;max-width:172mm;margin-bottom:3.4mm;">'
        f'<strong>{h}</strong> {t}</p>' for h, t in blocks)
    return f'''<div class="sheet">
  {strip(n)}
  <h2 style="font-size:21pt;margin-bottom:3.5mm;">{title}</h2>
  <p class="body" style="font-size:11.0pt;line-height:1.62;max-width:172mm;margin-bottom:3.4mm;">{lead}</p>
  {body}
  <div class="fine">{FINE1}</div>
  {footer(n, '1', foot_pages)}
</div>'''

doc2 = notes(2, 'The Cost Plan', (
    f'The document the homeowner works from for the length of the job. One house &mdash; {EX_HOUSE} '
    f'&mdash; with an attic top-up, a cavity fill, new windows and external doors, an air-to-water heat '
    f'pump with its cylinder, and decentralised ventilation with its air-tightness test. It follows in '
    f'full, exactly as the software prints it.'), [
  ('The benchmark is on every row, not at the bottom.',
   'This is the part that does the work. Each measure carries its own measured scope and its own '
   'figure &mdash; the attic top-up, the cavity fill, the windows and doors, the heat pump, the '
   'ventilation &mdash; and that figure is the benchmark for <em>that measure</em>. Beside it sits what '
   'the figure covers &mdash; the scope and the measured quantities &mdash; and under that, shaded, what it leaves '
   'out. Cavity fill, for instance: pump 90&thinsp;m&sup2; of 50&thinsp;mm bonded bead, making good '
   'included; not included, the room-by-room air intake vents a filled cavity makes necessary. A quote '
   'is judged line by line against all three: the figure, the scope, and what is left out. A contractor '
   'pricing the attic at twice the benchmark has '
   'to account for the attic, on that line, where the homeowner can see it; there is nowhere to lose it '
   'inside a single total.'),
  ('The totals, and what has to be raised.',
   f'Those rows add to <strong>&euro;{EX_TOTAL}</strong> &mdash; the whole job, VAT and the '
   f'contractor&rsquo;s overhead included. SEAI grants of <strong>&euro;{EX_GRANTS}</strong> are named '
   f'beside the measures that earn them, leaving <strong>&euro;{EX_NET}</strong> as what the work costs '
   f'in the end. On {EX_SCHEME} the grants are paid <em>after</em> the works, so it is the whole '
   f'&euro;{EX_TOTAL} that has to be available first; the &euro;{EX_GRANTS} comes back once the job is done. Both are '
   f'named because both are needed: one to borrow against, one to judge the job by.'),
  ('Where the figures come from.',
   f'Quantities are taken from the standard BER survey the provisional certificate is built from &mdash; '
   f'nothing is measured twice. Every rate comes from the published rate book &mdash; {RATE_BOOK} &mdash; '
   f'with the Co. Westmeath labour multiplier applied, and the contractor&rsquo;s overhead and VAT added '
   f'on top. The guide prices for the items left out are in the Appendix, document 04.'),
  ('How the heat pump is sized.',
   f'From the provisional BER&rsquo;s Heat Loss Indicator &mdash; {EX_HLI}&thinsp;W/m&sup2;K here &mdash; '
   f'giving a <strong>{EX_KW}&thinsp;kW design load at {EX_FLOW}&deg;C flow</strong>. The sum is printed '
   f'on the plan for any contractor to check; the installer&rsquo;s room-by-room calculation confirms the '
   f'unit and prices any variation.'),
])

# ── 03 · THE PRICING SCHEDULE ────────────────────────────────────────────────
doc3 = notes(3, 'The Pricing Schedule', (
    'The benchmark&rsquo;s scope, measure by measure, with every figure removed &mdash; no estimate, no '
    'grant amounts, no totals. Each measure keeps what it includes and what it leaves out. One goes to each '
    'contractor asked to quote, so every contractor prices the same work the benchmark priced.'), [
  ('It keeps the tender an open market.',
   'A contractor who can see the homeowner&rsquo;s budget prices against the budget. With the figures '
   'gone they price the work. Every contractor quotes the same measured scope with no sight of the '
   'homeowner&rsquo;s figure, so the job goes to the best price for the same work rather than to whoever '
   'guesses the budget closest &mdash; and a small firm competes on equal terms with a large one. When '
   'the quotes come back the homeowner lays them side by side, against each other and against their own '
   'plan: tendering the way a business does.'),
  ('What&rsquo;s not included is still named.',
   'The same shaded boxes appear here, so a contractor sees exactly what sits outside the scope. Without '
   'that an honest one assumes the item is included and pads the quote, a sharp one prices without it and '
   'raises a variation later, and the tenders stop being comparable. The guide prices stay in the '
   'homeowner&rsquo;s Appendix: a figure here would become a floor to quote up to.'),
  ('The Variations column is where site knowledge goes.',
   'A contractor&rsquo;s own survey will find things an assessor could not &mdash; a lintel, a threshold, '
   'a cavity that will not take the fill. This is where they price them: explicitly, itemised, at tender '
   'rather than mid-job. That is where variations come from, and putting them in writing before work '
   'starts keeps the process open and honest on both sides.'),
])

# ── 04 · THE APPENDIX ────────────────────────────────────────────────────────
doc4 = notes(4, 'The Appendix', (
    'The reference behind the Cost Plan, fixed at the date of issue. How every figure was reached, the '
    'itemised measurements and rates beneath each measure, and the guide prices for everything the plan '
    'leaves out. It follows in full, exactly as the software prints it.'), [
  ('How the estimate &mdash; the benchmark &mdash; was calculated.',
   'The estimate on the Cost Plan is the benchmark; this is the arithmetic behind it. '
   'Measure by measure: the inputs used, the base cost of materials and labour, the contractor&rsquo;s '
   'overhead and profit, and the VAT that applies to that measure. The loaded column ties back to the '
   'Cost Plan line for line. Each measure also repeats what it '
   'leaves out, so what a figure covers and what it does not can be read together.'),
  ('The itemised index.',
   'Beneath every bundled measure, the individual items at base rates &mdash; quantity, unit, material '
   'and labour per unit. This is the level a quantity surveyor would work at, and it is what makes the '
   'headline figure checkable rather than merely stated.'),
  ('Not included &mdash; variation guide prices. The part that matters most at tender.',
   'Every item shaded &ldquo;not included&rdquo; on the Cost Plan and the Schedule, with a guide price '
   'attached. These are the homeowner&rsquo;s figures, not the contractor&rsquo;s, and they are what '
   'empowers the homeowner at tender: they already know what the work should '
   'cost <em>and</em> what anything beyond it should cost. A fair variation is agreed in minutes and a '
   'padded one is visible in the same minutes &mdash; before work starts, not once the job is open.'),
])

# ── 05 · THE WORKFLOW — where the one new step sits ───────────────────────────
# A numbered timeline: number in a disc, title left, status right, body left-aligned
# beneath. Left alignment because these are sentences, not captions — centred prose makes
# the eye hunt for each line start. The one new step is tinted and darker-edged so the
# page makes its argument at a glance.
def wfstep(n, title, body, note='', last=False, add=False):
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
    </div>
    {arrow}'''

doc5 = f'''<div class="sheet">
  {strip(5)}
  <h2>The workflow &mdash; where the three documents come in</h2>
  <div style="margin-top:4mm;">
  {wfstep('1', 'The dwelling survey',
    'Part of the technical assessment for a heat pump or window measures. Geometry, fabric and services recorded on site.',
    note='Already happens')}
  {wfstep('2', 'The measures, agreed with the homeowner',
    'Around the table, measure by measure: what the house needs, what each measure includes, and what it leaves out. The homeowner decides the scope.',
    note='Already happens')}
  {wfstep('3', 'The provisional BER report',
    'The surveyed geometry, the total heat loss and the post-works Heat Loss Indicator, in the one document everything after it is built from.',
    note='Already happens')}
  {wfstep('4', 'The three documents are produced and issued',
    'At a desk, after the survey. The geometry and Heat Loss Indicator are taken from the provisional report, the '
    'agreed measures are selected, the grant route is set, and the three documents print &mdash; the Cost Plan, '
    'the blank Pricing Schedule and the Appendix. They go to the homeowner with the provisional BER.',
    note='New &middot; minutes at a desk', add=True)}
  {wfstep('5', 'Variations and prices agreed with the contractor',
    'With the benchmark and the guide prices for what it leaves out, the homeowner tenders properly: the same '
    'measured scope to every contractor, quotes that compare like with like, and any variation priced and agreed '
    '<strong>before work starts</strong>.',
    note='Same step, new terms')}
  {wfstep('6', 'The post-works BER',
    'The assessor returns, completes the post-works BER and uploads it for the grant.',
    note='Already happens', last=True)}
  </div>
  <div class="fine">{FINE1}</div>
  {footer(5, '1', '1')}
</div>'''

# ── 06 · THE SOFTWARE — the journey on screen, survey to print (4 pages) ──────
def appfig(key, w, lead, rest):
    return f'''<div class="appshot" style="width:{w};margin:0 auto 2mm;">
      <img src="{IMG[key]}" alt="">
      <div class="ac" style="font-size:8pt;"><strong>{lead}</strong> {rest}</div>
    </div>'''

doc6 = f'''<div class="sheet">
  {strip(6)}
  <h2>The software behind it</h2>
  <p class="body" style="font-size:9pt;margin-bottom:2.5mm;">Live software, as it runs. These screens are the
    whole journey, in order: the survey goes in, the grant route is chosen with the figures on display,
    and the three documents print at the far end.</p>

  {appfig('home', '152mm', '1 &middot; Choose the project type.',
    'New Build, Refurbishment and Energy Upgrade share one engine and one rate base.')}
  <div class="arrowrow">{DOWN_ARROW}</div>
  {appfig('sel', '152mm', '2 &middot; The survey becomes a project.',
    'DEAP geometry, the measures the homeowner wants, the county and the grant scheme &mdash; the status bar and sidebar fill as it goes in, and nothing is measured twice.')}

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(6, '1', '4')}
</div>

<div class="sheet">
  {strip(6)}
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
    'The benchmark fixed at issue, the grant named on every line, and the live half ready to record quotes and payments as the job runs.')}

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(6, '2', '4')}
</div>

<div class="sheet">
  {strip(6)}
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
      <div class="pt-t" style="font-size:9.5pt;">The Retrofit Cost Plan</div>
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
  {footer(6, '3', '4')}
</div>

<div class="sheet">
  {strip(6)}
  {appfig('rates', '134mm', '6 &middot; Rate Settings, open to inspection.',
    'Labour at the SEO August 2026 rates &mdash; every unit price, labour rate and county multiplier visible, each with its source. Nothing is a black box.')}
  {appfig('grants', '134mm', '7 &middot; The SEAI grant table the plans draw from.',
    'Every amount dated and visible &mdash; when SEAI changes a rate, one number changes and every new plan follows.')}

  <p class="body" style="font-size:8pt;color:#64748B;margin-top:2mm;">Where each rate comes from, and how the
    book is versioned and inspected, is in document 07.</p>

  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(6, '4', '4')}
</div>'''

# ── 07 · THE ENGINE — the EU rate book, top to bottom, on three pages ─────────
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
  {strip(7)}
  <h2 style="font-size:21pt;margin-bottom:3mm;">The engine</h2>
  <p class="body" style="{ENG_P}">Every figure in a plan comes from a rate book with a version number and
    an effective date. The assessor prices from it and cannot change it: the book is held in one place and
    published by one administrator &mdash; under the pilot, SEAI &mdash; so every plan is priced on the
    same rates. These three pages are that book, top to bottom, exactly as it appears on screen.</p>
  <p class="body" style="{ENG_P}"><strong>Where the rates come from.</strong> Base rates from the SCSI
    Tender Price Index and House Rebuilding Guide; labour from the SEO Construction Sector wage agreement,
    at the second-phase rates effective 1 August 2026; the county multiplier from the SCSI Regional Cost
    Supplement; grants at SEAI&rsquo;s published amounts; VAT as Revenue applies it. Each block names its
    own source beneath it.</p>
  <p class="body" style="{ENG_P}"><strong>Held in one place.</strong> Every rate shows its published value and
    its source. A change is made once, centrally, and every plan priced afterwards follows. The panel
    marks any rate still to be calibrated, so the pilot&rsquo;s recorded outturns can settle it.</p>
  {engfig('eng_a', '160mm', 'Walls, heat pump and ventilation.',
    'Category uplift by trade on the left; supply-only material rates on the right, the published figure in every box and the source under each group.')}
  <div class="fine">{FINE1}</div>
  {footer(7, '1', '3')}
</div>

<div class="sheet">
  {strip(7)}
  {engfig('eng_b', '172mm', 'Fascia and soffit, ventilation units, windows and doors, solar PV and battery, and the attic ancillaries.',
    'The frame and style multipliers for windows are written out under the table, so a triple-glazed alu-clad sash window can be traced from the base rate. The attic ancillaries are the items every attic top-up carries as standard: the tank jacket, the pipe lagging, the walkway and the storage deck.')}
  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(7, '2', '3')}
</div>

<div class="sheet">
  {strip(7)}
  <h2 style="font-size:16pt;margin-bottom:2mm;">The not-included rates</h2>
  <p class="body" style="{ENG_P}">This is the engine behind the guide prices in the Appendix. Every item a
    measure leaves out is priced here, per unit, with the measure it belongs to named beside it. When a
    contractor proposes a variation, the figure the homeowner holds against it comes from this table; and
    when an item is ticked into a plan after the survey, its priced line uses the same rate. One number, in
    one place, feeding both.</p>
  {engfig('eng_c', '172mm', 'Variations &mdash; not included guide rates.',
    'Material per unit, labour from the Labour Rates tab, loaded like the plan: overhead and profit at 12%, then VAT. The flag at the foot marks a rate still to be calibrated against recorded outturns.')}
  <div class="fine">Screens from the live software, 2 September 2026, unedited.</div>
  {footer(7, '3', '3')}
</div>'''

TPL = '''<!doctype html><html><head><meta charset="utf-8"><title>%s</title>
<style>%s</style></head><body>%s</body></html>'''

for name, content in [('pack_01', doc1), ('pack_02', doc2), ('pack_03', doc3),
                      ('pack_04', doc4), ('pack_05', doc5), ('pack_06', doc6),
                      ('pack_07', doc7)]:
    open(name + '.html', 'w').write(TPL % ('PlanitBER — ' + name, CSS, content))
    print('wrote', name + '.html')
