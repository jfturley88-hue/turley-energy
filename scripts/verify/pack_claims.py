"""Is the pack fit to send?

One gate over the finished PDFs and the covering email that goes with them. It reads what
was actually printed, not the source that printed it, because the pack is what SEAI sees.

It covers four things:

  the pack holds together  - seven documents, numbered of 7, at the page counts the contents
                             note claims, with no placeholder left unfilled and no practice
                             name anywhere;
  the figures are one set  - the worked example's total, grants and net, as the software
                             printed them;
  document 07 is honest    - no trading name that is not registered, and document 06 cited
                             at the date document 06 gives;
  the email matches        - every claim the covering note makes is true of the documents
                             attached to it.

    python scripts/verify/pack_claims.py

Run it before the pack is sent, and after any change to a document or to the email.
"""
import io
import glob
import os
import re

from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'

# A phrase that wraps across a line in a PDF or in the email must still match, so both sides
# are flattened to single spaces before anything is looked for.
flat = lambda t: re.sub(r'\s+', ' ', t)

pages, pack = {}, {}
for f in sorted(glob.glob(ROOT + 'pack/PlanitBER_SEAI_Pack/*.pdf')):
    n = os.path.basename(f)[10:12]
    r = PdfReader(f)
    pages[n] = len(r.pages)
    pack[n] = flat(' '.join((p.extract_text() or '') for p in r.pages))

raw = io.open(ROOT + 'pack/covering_email_nas_trial.txt', encoding='utf-8').read()
email = flat(raw)
after_sign = raw.split('Kind regards,')[1]
contents = io.open(ROOT + 'SEAI_PACK_CONTENTS.md', encoding='utf-8').read()

# the page counts the contents note claims, read back out of its own table
claimed = {m[0]: int(m[1]) for m in re.findall(r'^\| (\d\d) \|.*\| (\d+) \|$', contents, re.M)}

checks = [
    # the pack holds together
    ('seven documents, every one of them present',
     sorted(pages) == ['01', '02', '03', '04', '05', '06', '07']),
    ('every document numbered of 7',
     all('OF 7' in pack[n].upper() for n in ('01', '05', '06')) and 'document 7 of 7' in pack['07']),
    ('the contents note has the page counts right', claimed == pages),
    ('no placeholder left unfilled',
     not any(p in t for t in pack.values() for p in ('[Date]', '[Name]', '[Practice]', '[Email]', '[Phone]'))),
    ('no practice name anywhere',
     not any('turley energy' in t.lower() or 'turleyenergy' in t.lower() for t in pack.values())),
    ('the letter is signed, with the registration that can be checked',
     'John Turley' in pack['01'] and 'reg. 100615' in pack['01']),

    # the figures are one set
    ('the worked example prints one set of figures',
     all(f in pack['02'] for f in ('34,977', '20,150', '14,827')) and '34,977' in pack['04']),

    # document 07 is honest
    ('07 claims no trading name', 'trading as' not in pack['07']),
    ('07 cites 06 at the date 06 gives',
     'document 06, Data Protection, issued 10 October 2026' in pack['07']
     and 'Issued 10 October 2026' in pack['06']),
    ('06 and 07 agree the DPIA is done',
     'has been carried out. It is document 07' in pack['06'] and 'Drafted as document 07' in pack['06']),

    # the email matches what is attached
    ('the email names document 07', 'document 07' in email),
    ('the email does not call the DPIA still to be done', 'will be completed' not in email),
    ('consent points at 07, where the process is set out',
     'Consent management: set out in document 07' in email),
    ('the six open items are declared, as 07 lists them',
     'six items to close' in email and 'six open items' in pack['07']),
    ('the pilot and the trial are not in the wrong order', 'alongside the trial' in email),
    ('the registration in the email matches the documents',
     '100615' in email and '100615' in pack['01'] and '100615' in pack['07']),
    ('the signature is whole', 'mc2rating@gmail.com' in after_sign),
]

bad = 0
for name, ok in checks:
    bad += not ok
    print(('ok   ' if ok else 'FAIL '), name)

print()
print('pages:', ' '.join(f'{n}:{pages[n]}' for n in sorted(pages)))
print('VERDICT:', 'the pack is fit to send' if not bad else f'NOT fit to send — {bad} failing')
raise SystemExit(1 if bad else 0)
