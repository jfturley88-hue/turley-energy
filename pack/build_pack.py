#!/usr/bin/env python3
"""Assemble the six-PDF SEAI pack and the editable text, from the printed parts.

The pack used to be put together by hand, which is how it came to ship a stale set of
figures: the prints were regenerated but the folder was not. Everything here is derived,
so the only way to change the pack is to change its source.

Order matters: documents 02-04 are the software's own output, each bound behind one page
of notes saying who that document is for and how long it lives.
"""
import glob, os, re, shutil, zipfile
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, 'PlanitBER_SEAI_Pack')
EDIT = os.path.join(HERE, 'PlanitBER_Editable_Text')

# (output name, [parts]) — a part is a printed pack page or a document from the software
DOCS = [
    ('PlanitBER_01_The_Value_Proposition.pdf', ['pack_01_print.pdf']),
    ('PlanitBER_02_The_Cost_Plan.pdf',         ['pack_02_print.pdf', 'ex_plan.pdf']),
    ('PlanitBER_03_The_Pricing_Schedule.pdf',  ['pack_03_print.pdf', 'ex_sched.pdf']),
    ('PlanitBER_04_The_Appendix.pdf',          ['pack_04_print.pdf', 'ex_appx.pdf']),
    ('PlanitBER_05_The_Workflow.pdf',          ['pack_05_print.pdf']),
    ('PlanitBER_06_The_Software.pdf',          ['pack_06_print.pdf']),
    ('PlanitBER_07_The_Engine.pdf',            ['pack_07_print.pdf']),
]

def build():
    for d in (PACK, EDIT):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    for out, parts in DOCS:
        missing = [f for f in parts if not os.path.exists(os.path.join(HERE, f))]
        if missing:
            raise SystemExit('missing part(s) for %s: %s' % (out, ', '.join(missing)))
        if len(parts) == 1:
            shutil.copy(os.path.join(HERE, parts[0]), os.path.join(PACK, out))
        else:
            w = pypdf.PdfWriter()
            for f in parts:
                w.append(os.path.join(HERE, f))
            w.write(os.path.join(PACK, out))
            w.close()

    for f in sorted(glob.glob(os.path.join(HERE, 'EDIT_0*.docx'))):
        shutil.copy(f, os.path.join(EDIT, os.path.basename(f)))

    for d in (PACK, EDIT):
        z = d + '.zip'
        if os.path.exists(z):
            os.remove(z)
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(glob.glob(os.path.join(d, '*'))):
                zf.write(f, os.path.join(os.path.basename(d), os.path.basename(f)))

def report():
    # Read the figures back out of the finished PDFs rather than trusting the build: a
    # stale part would otherwise ship silently, which is exactly what happened before.
    print('== pack ==')
    for out, _ in DOCS:
        f = os.path.join(PACK, out)
        r = pypdf.PdfReader(f)
        t = re.sub(r'\s+', ' ', '\n'.join(p.extract_text() or '' for p in r.pages))
        money = sorted(set(re.findall(r'€[\d,]{4,}', t)))
        ber   = sorted(set(re.findall(r'[A-G]\d?\s*→\s*[A-G]0?', t)))
        docn  = sorted(set(re.findall(r'DOCUMENT \d OF \d', t, re.I)))
        print('  %2dp  %-42s %s %s %s' % (len(r.pages), os.path.basename(f),
              ber or '', docn or '', ' '.join(money[:4])))
    print('== editable ==')
    for f in sorted(glob.glob(os.path.join(EDIT, '*.docx'))):
        print('  %3dK  %s' % (os.path.getsize(f) // 1024, os.path.basename(f)))

if __name__ == '__main__':
    build()
    report()
