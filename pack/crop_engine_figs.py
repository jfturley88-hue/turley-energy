#!/usr/bin/env python3
"""Cut app_eurates_full.png into the three page-sized figures documents 05 uses.

These three were hand-cropped and had no generator in the repo, so every change to
the Rate Settings panel silently left them stale. They are slices of one real
capture, never composited: run shot_engine_full.js first, then this.

The slices are anchored from the BOTTOM. The panel grows at the top when a rate or
a note gains a line, and anchoring that way keeps the lower two figures identical
instead of shifting every boundary. Check the output if the panel is restructured.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'app_eurates_full.png')

# heights as first cropped, bottom-anchored; the top figure absorbs any growth
H_B, H_C = 2940, 1686
OUT = ('app_eng_a.png', 'app_eng_b.png', 'app_eng_c.png')

def main():
    im = Image.open(SRC)
    w, h = im.size
    cuts = [(0, 0, w, h - H_B - H_C),
            (0, h - H_B - H_C, w, h - H_C),
            (0, h - H_C, w, h)]
    top = cuts[0][3]
    if top < 400:
        raise SystemExit(f'top slice would be {top}px — the panel shrank; check the crops by eye')
    for name, box in zip(OUT, cuts):
        im.crop(box).save(os.path.join(HERE, name))
        print(f'  {name:16s} {box[2]-box[0]} x {box[3]-box[1]}')
    print(f'source {w} x {h} -> three slices, bottom-anchored')

if __name__ == '__main__':
    main()
