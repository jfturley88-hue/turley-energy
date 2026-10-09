"""Every claim the covering email makes, checked against the printed pack."""
import io, re, glob, os
from pypdf import PdfReader

ROOT = 'G:/My Drive/Claude project/fibe/turley/BER-BOQ/planitber/'
# A phrase that wraps across a line in the PDF or the email must still match, so both
# sides are flattened to single spaces before anything is looked for.
flat = lambda t: re.sub(r'\s+', ' ', t)
pack = {os.path.basename(f)[10:12]: flat(' '.join((p.extract_text() or '') for p in PdfReader(f).pages))
        for f in glob.glob(ROOT + 'pack/PlanitBER_SEAI_Pack/*.pdf')}
raw = io.open(ROOT + 'pack/covering_email_nas_trial.txt', encoding='utf-8').read()
email = flat(raw)
after_sign = raw.split('Kind regards,')[1]

checks = [
    ('the registration matches 01 and 07',
     '100615' in email and '100615' in pack['01'] and '100615' in pack['07']),
    ('the email names document 07', 'document 07' in email),
    ('the DPIA is not described as still to be done', 'will be completed' not in email),
    ('consent points at 07, where the process is', 'Consent management: set out in document 07' in email),
    ('the six open items are declared', 'six items to close' in email and 'six open items' in pack['07']),
    ('06 agrees the DPIA is done', 'has been carried out. It is document 07' in pack['06']),
    ('06 open item matches the email', 'Drafted as document 07' in pack['06']),
    ('the pilot/trial sequencing is addressed', 'alongside the trial' in email),
    ('the signature is complete', 'mc2rating@gmail.com' in after_sign),
    ('every document numbered of 7',
     all('OF 7' in pack[n].upper() for n in ('01', '05', '06')) and 'document 7 of 7' in pack['07']),
]
bad = 0
for name, ok in checks:
    bad += not ok
    print(('ok   ' if ok else 'FAIL '), name)

stale = 'document 06, Data Protection, issued 8 October 2026' in pack['07'].replace('\n', ' ')
print(('OPEN ' if stale else 'ok   '), '07 cites 06 with the right issue date')
print('\nfailures:', bad, '| open, to be fixed in the tool that wrote 07:', int(stale))
