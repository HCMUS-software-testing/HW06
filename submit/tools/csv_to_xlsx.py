import csv, html, os, zipfile
ROOT=os.path.dirname(os.path.dirname(__file__)); src=os.path.join(ROOT,'test-cases','member-4.csv'); out=os.path.join(ROOT,'test-cases','member-4.xlsx')
with open(src,encoding='utf-8',newline='') as f: rows=list(csv.reader(f))
def col(n):
    s=''
    while n:
        n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def cell(c,r,v,header=False):
    v=html.escape(str(v),quote=True); style=' s="1"' if header else ''
    return f'<c r="{col(c)}{r}" t="inlineStr"{style}><is><t xml:space="preserve">{v}</t></is></c>'
sheet=['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView showGridLines="0" workbookViewId="0"/></sheetViews><cols><col min="1" max="19" width="24"/></cols><sheetData>']
for ri,row in enumerate(rows,1): sheet.append(f'<row r="{ri}">'+''.join(cell(ci,ri,v,ri==1) for ci,v in enumerate(row,1))+'</row>')
sheet += ['</sheetData><autoFilter ref="A1:S141"/></worksheet>']; content=''.join(sheet)
files={
'[Content_Types].xml':'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
'_rels/.rels':'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
'xl/workbook.xml':'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Member4 Test Cases" sheetId="1" r:id="rId1"/></sheets></workbook>',
'xl/_rels/workbook.xml.rels':'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
'xl/styles.xml':'<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Arial"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Arial"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="1F4E78"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf fontId="0" fillId="0" borderId="0"/><xf fontId="1" fillId="2" borderId="0" applyFill="1"/></cellXfs></styleSheet>',
'xl/worksheets/sheet1.xml':content}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p,v in files.items(): z.writestr(p,v)
print(out,os.path.getsize(out))
