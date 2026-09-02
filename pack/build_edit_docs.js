// One A4 Word document per pack document, carrying every editable block with its tag.
// Bold inside a block is preserved as real bold so it survives the round trip.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, ShadingType, Footer, PageNumber,
} = require('docx');

const MAP = JSON.parse(fs.readFileSync(__dirname + '/editable_map.json', 'utf8'));
const NAVY = '1E293B', GOLD = 'B07D1A', GREY = '8090A8', SLATE = '475569';
const noB = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: noB, bottom: noB, left: noB, right: noB };

// innerHTML → runs, keeping <strong>/<b> as bold. Everything else is flattened.
function runs(html) {
  const parts = [];
  const re = /<(\/?)(strong|b)[^>]*>|([^<]+)|<[^>]+>/gi;
  let bold = 0, m;
  while ((m = re.exec(html)) !== null) {
    if (m[2]) { bold += m[1] ? -1 : 1; if (bold < 0) bold = 0; continue; }
    if (m[3]) {
      const t = m[3].replace(/&mdash;/g, '—').replace(/&ndash;/g, '–')
                    .replace(/&middot;/g, '·').replace(/&euro;/g, '€')
                    .replace(/&rsquo;/g, '’').replace(/&amp;/g, '&')
                    .replace(/&nbsp;/g, ' ').replace(/&plusmn;/g, '±')
                    .replace(/&rarr;/g, '→').replace(/&sup2;/g, '²')
                    .replace(/&thinsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
      if (t.trim()) parts.push(new TextRun({ text: t, font: 'Calibri', size: 21, bold: bold > 0, color: '1F2937' }));
    }
  }
  return parts.length ? parts : [new TextRun({ text: '', font: 'Calibri', size: 21 })];
}

const tagRow = (tag, kind, page) => new Table({
  width: { size: 9700, type: WidthType.DXA }, columnWidths: [9700], borders: noBorders,
  rows: [new TableRow({ children: [new TableCell({
    width: { size: 9700, type: WidthType.DXA }, borders: noBorders,
    shading: { type: ShadingType.CLEAR, fill: 'F1F5F9' }, margins: { top: 40, bottom: 40, left: 100, right: 100 },
    children: [new Paragraph({ spacing: { after: 0 }, children: [
      new TextRun({ text: tag, font: 'Consolas', size: 16, bold: true, color: GOLD }),
      new TextRun({ text: '   page ' + page + '   ' + kind, font: 'Calibri', size: 14, color: GREY }),
    ] })],
  })] })],
});

function buildDoc(n, info) {
  const children = [
    new Paragraph({ spacing: { after: 60 }, children: [
      new TextRun({ text: 'Planit', font: 'Calibri', size: 34, bold: true, color: NAVY }),
      new TextRun({ text: 'BER', font: 'Calibri', size: 34, bold: true, color: 'E8A020' }),
      new TextRun({ text: '   editable text', font: 'Calibri', size: 20, color: GREY }),
    ] }),
    new Paragraph({ spacing: { after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 6 } },
      children: [new TextRun({ text: 'Document ' + n + ' — ' + info.title, font: 'Georgia', size: 30, bold: true, color: NAVY })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({
      text: 'Edit the wording under each tag. Leave the tags themselves alone and do not reorder or delete ' +
            'blocks — they are how the text finds its way back into the designed page. Bold shows where the ' +
            'layout emphasises a phrase; keep or move it as you like. Figures that come from the software ' +
            'are best left as they are: change them in the app and they reprint correctly everywhere.',
      font: 'Calibri', size: 19, color: SLATE, italics: true })] }),
  ];

  let page = 0;
  info.blocks.forEach(b => {
    if (b.page !== page) {
      page = b.page;
      children.push(new Paragraph({ spacing: { before: 260, after: 100 }, children: [
        new TextRun({ text: 'PAGE ' + page, font: 'Calibri', size: 18, bold: true, color: GOLD }),
      ] }));
    }
    children.push(tagRow(b.tag, b.kind, b.page));
    children.push(new Paragraph({ spacing: { before: 60, after: 180, line: 290 }, children: runs(b.html) }));
  });

  return new Document({
    sections: [{
      properties: { page: { margin: { top: 1000, bottom: 1000, left: 1000, right: 1000 } } },
      footers: { default: new Footer({ children: [new Paragraph({ children: [
        new TextRun({ text: 'PlanitBER editable text · document ' + n + ' · page ', font: 'Calibri', size: 15, color: GREY }),
        new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 15, color: GREY }),
      ] })] }) },
      children,
    }],
  });
}

(async () => {
  for (const [n, info] of Object.entries(MAP)) {
    const buf = await Packer.toBuffer(buildDoc(n, info));
    const name = __dirname + '/EDIT_' + n + '_' + info.title.split(' —')[0].replace(/\s+/g, '_') + '.docx';
    fs.writeFileSync(name, buf);
    console.log('wrote', name.split('/').pop(), '·', info.blocks.length, 'blocks ·', Math.round(buf.length / 1024), 'KB');
  }
})();
