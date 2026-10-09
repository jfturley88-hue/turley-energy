"""Two corrections to document 07, the DPIA, made in the printed PDF.

Document 07 is written outside this repository and arrives as a finished PDF. Two statements
in it cannot go to SEAI:

  1. the controller block reads "John Turley, trading as PlanitBER" — that business name is
     not registered, so the claim is not true;
  2. the Sources list cites document 06 as "issued 8 October 2026", where document 06 says
     10 October. 8 October is the day the build it describes was made, not the day it issued.

Fix them where the document was written as well, or the next export brings them back. This
is what makes the copy bound into the pack correct in the meantime.

How it works
------------
The fonts are Identity-H subsets, so the content stream holds glyph ids rather than
characters, and this generator draws one glyph per operator:

    <0070> Tj
    19.616043 0 Td <00FB> Tj

Each font carries a ToUnicode CMap, which maps glyph id back to the character it draws;
invert it and the stream becomes readable.

Td is cumulative: it moves the text line matrix, so each glyph's offset is measured from the
glyph before it. Delete a glyph's operators and everything after it on the line closes up by
exactly that glyph's advance — which is what deleting text should look like. But the same
shift carries into the next line of the same BT block, which would drag the rest of the
paragraph sideways. So after an edit, the first following Td that moves down a line gets the
width change added back, and every line below it stays where the generator put it.

An inserted glyph needs an advance. It is measured from a real occurrence of the same
character in the same font at the same size on the same page, not from the font's width
table, so whatever letter spacing the generator applied is reproduced.

    python pack/fix_doc_07.py            # report what it finds, change nothing
    python pack/fix_doc_07.py --write    # rewrite pack/doc_07_dpia.pdf in place
"""
import os
import re
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, 'doc_07_dpia.pdf')

# (page, the text as the stream spells it, what it should say)
EDITS = [
    (1, 'John Turley, trading as PlanitBER, Killyleen', 'John Turley, Killyleen'),
    (9, 'Data Protection, issued 8 October 2026', 'Data Protection, issued 10 October 2026'),
]

GLYPH = re.compile(r'(?:([-\d.]+)\s+([-\d.]+)\s+Td\s*)?<([0-9A-Fa-f]{4,})>\s*Tj')
FONT = re.compile(r'/(F\d+)\s+([\d.]+)\s+Tf')
ANY_TD = re.compile(r'([-\d.]+)\s+([-\d.]+)\s+Td')


def tounicode(font):
    """glyph id -> the character it draws, from the font's own ToUnicode CMap."""
    cmap = font.get('/ToUnicode')
    if cmap is None:
        return {}
    data = cmap.get_object().get_data().decode('latin-1')
    out = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', data, re.S):
        for g, u in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            out[int(g, 16)] = ''.join(chr(int(u[i:i + 4], 16)) for i in range(0, len(u), 4))
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', data, re.S):
        for lo, hi, u in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            base = int(u, 16)
            for n, g in enumerate(range(int(lo, 16), int(hi, 16) + 1)):
                out[g] = chr(base + n)
    return out


def page_fonts(page):
    """Each font on the page, keyed as the content stream names it."""
    return {str(k).lstrip('/'): tounicode(v.get_object())
            for k, v in page['/Resources']['/Font'].items()}


def glyphs(stream, fonts):
    """Every glyph the page draws, in order, with where its operators sit in the stream."""
    font_at = [(m.start(), m.group(1), float(m.group(2))) for m in FONT.finditer(stream)]
    out = []
    for m in GLYPH.finditer(stream):
        name = size = None
        for pos, f, s in font_at:
            if pos < m.start():
                name, size = f, s
            else:
                break
        hexes = m.group(3)
        ids = [int(hexes[i:i + 4], 16) for i in range(0, len(hexes), 4)]
        out.append({
            'start': m.start(), 'end': m.end(),
            'dx': float(m.group(1)) if m.group(1) else None,
            'dy': float(m.group(2)) if m.group(2) else None,
            'font': name, 'size': size, 'hex': hexes,
            'text': ''.join(fonts[name].get(g, '�') for g in ids) if name in fonts else '�',
        })
    return out


def advance_of(char, font, size, gl):
    """What this generator leaves between `char` and the next glyph, measured on the page."""
    for a, b in zip(gl, gl[1:]):
        if (a['text'] == char and a['font'] == font and a['size'] == size
                and b['dx'] is not None and b['dy'] == 0):
            return b['dx'], a['hex']
    return None, None


def plan(page, find, replace, note):
    """The new content stream for one edit, or None if it cannot be made safely."""
    fonts = page_fonts(page)
    stream = page.get_contents().get_data().decode('latin-1')
    gl = glyphs(stream, fonts)
    text = ''.join(g['text'] for g in gl)

    at = text.find(find)
    if at == -1:
        note.append(f'not found, nothing to do: {find!r}')
        return None
    if text.find(find, at + 1) != -1:
        note.append(f'REFUSED: {find!r} appears more than once on this page')
        return None

    # Only the part that actually differs is touched. The two ends can claim the same
    # characters — "John Turley, trading as PlanitBER, Killyleen" and "John Turley,
    # Killyleen" share ", " at both ends — so the tail is clamped to what the head left,
    # or the edit would keep one of them twice and write "John Turley, , Killyleen".
    head = len(os.path.commonprefix([find, replace]))
    tail = min(len(os.path.commonprefix([find[::-1], replace[::-1]])),
               len(find) - head, len(replace) - head)
    cut = gl[at + head:at + len(find) - tail]
    add = replace[head:len(replace) - tail]
    if not cut:
        note.append('REFUSED: this edit only inserts, so there is nothing to anchor it to')
        return None

    ops, shift = [], 0.0
    if add:
        first = cut[0]
        adv, hexes = {}, {}
        for ch in sorted(set(add)):
            a, h = advance_of(ch, first['font'], first['size'], gl)
            if h is None:
                note.append(f'REFUSED: no {ch!r} in {first["font"]} at {first["size"]}pt to measure')
                return None
            adv[ch], hexes[ch] = a, h
        for n, ch in enumerate(add):
            if n == 0:
                lead = f"{first['dx']} {first['dy']} Td " if first['dx'] is not None else ''
                ops.append(f'{lead}<{hexes[ch]}> Tj')
            else:
                ops.append(f'{adv[add[n - 1]]:.6f} 0 Td <{hexes[ch]}> Tj')
        # the line grows by the new glyphs' advances and loses the cut glyphs' offsets
        shift = sum(adv[c] for c in add[:-1]) - sum(g['dx'] or 0 for g in cut[1:])
        if len(cut) == 1 and len(add) >= 1:
            note.append(f'replacing {find[head]!r} with {add!r}; '
                        f'advance of {add[0]!r} measured at {adv[add[0]]}')
    else:
        shift = -sum(g['dx'] or 0 for g in cut)

    drawn = ' '.join(ops)
    new = stream[:cut[0]['start']] + drawn + stream[cut[-1]['end']:]

    # put the next line back where it was
    after_at = cut[0]['start'] + len(drawn)
    rest = new[after_at:]
    stop = rest.find('ET')
    for m in ANY_TD.finditer(rest if stop == -1 else rest[:stop]):
        if float(m.group(2)) != 0:
            fixed = f'{float(m.group(1)) - shift:.6f} {m.group(2)} Td'
            new = new[:after_at + m.start()] + fixed + new[after_at + m.end():]
            note.append(f'line below re-based by {-shift:+.3f}, so nothing under it moves')
            break
    else:
        note.append('no further line in this block to re-base')

    note.append(f'{len(cut)} glyphs out, {len(add)} in, stream {len(new) - len(stream):+d} bytes')
    return new


def main(write):
    reader = PdfReader(PDF)
    planned, ok = [], True
    for page_no, find, replace in EDITS:
        note = []
        new = plan(reader.pages[page_no - 1], find, replace, note)
        print(f'  page {page_no}: {find!r}\n        -> {replace!r}')
        for line in note:
            print('      ', line)
        if new is None:
            ok = False
        else:
            planned.append((reader.pages[page_no - 1], new))

    if not write:
        print('\nreport only; pass --write to change the file')
        return 0
    if not ok:
        print('\nnothing written: not every edit could be made')
        return 1

    # The writer owns the objects it will save, so the new streams are attached to its own
    # copy of each page rather than to the reader's.
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    for (page, stream), out in zip(planned, [writer.pages[n - 1] for n, _, _ in EDITS]):
        obj = DecodedStreamObject()
        obj.set_data(stream.encode('latin-1'))
        out[NameObject('/Contents')] = writer._add_object(obj)
    with open(PDF, 'wb') as fh:
        writer.write(fh)
    print(f'\nwrote {PDF}')

    after = PdfReader(PDF)
    txt = re.sub(r'\s+', ' ', ' '.join((p.extract_text() or '') for p in after.pages))
    print('pages:', len(after.pages))
    for _, find, replace in EDITS:
        print(f'   gone: {find not in txt}  |  in place: {replace in txt}  |  {replace}')
    return 0


if __name__ == '__main__':
    sys.exit(main('--write' in sys.argv))
