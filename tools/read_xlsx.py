"""Read this inventory workbook, including Excel in-cell and floating images.

Uses only the standard library. Cell values are data; formulas are never executed.
"""
from pathlib import PurePosixPath
from zipfile import ZipFile
import posixpath
import xml.etree.ElementTree as ET

S = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
D = 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
RV = 'http://schemas.microsoft.com/office/spreadsheetml/2017/richdata'


def relations(archive, path):
    root = ET.fromstring(archive.read(path))
    base = posixpath.dirname(posixpath.dirname(path))
    return {node.get('Id'): posixpath.normpath(posixpath.join(base, node.get('Target')))
            for node in root if node.get('TargetMode') != 'External'}


def read_inventory(path, *, images_by_row=False):
    with ZipFile(path) as archive:
        strings = [''.join(node.itertext()) for node in
                   ET.fromstring(archive.read('xl/sharedStrings.xml')).findall(f'{{{S}}}si')]
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        sheet = workbook.find(f'{{{S}}}sheets')[0]
        sheet_path = relations(archive, 'xl/_rels/workbook.xml.rels')[sheet.get(f'{{{R}}}id')]
        rich_rels = relations(archive, 'xl/richData/_rels/richValueRel.xml.rels')
        ordered_rels = [node.get(f'{{{R}}}id') for node in
                        ET.fromstring(archive.read('xl/richData/richValueRel.xml'))]
        rich_values = [int(node.find(f'{{{RV}}}v').text) for node in
                       ET.fromstring(archive.read('xl/richData/rdrichvalue.xml'))]
        metadata = ET.fromstring(archive.read('xl/metadata.xml'))
        future = [int(node.find(f'.//{{{RV}}}rvb').get('i')) for node in
                  metadata.find(f'{{{S}}}futureMetadata')]
        value_metadata = [int(node.find(f'{{{S}}}rc').get('v')) for node in
                          metadata.find(f'{{{S}}}valueMetadata')]
        floating_images = {}
        drawing_rels = relations(archive, 'xl/drawings/_rels/drawing1.xml.rels')
        for anchor in ET.fromstring(archive.read('xl/drawings/drawing1.xml')):
            row_node = anchor.find(f'{{{D}}}from/{{{D}}}row')
            blip = anchor.find(f'.//{{{A}}}blip')
            if row_node is not None and blip is not None:
                floating_images[int(row_node.text) + 1] = drawing_rels[blip.get(f'{{{R}}}embed')]
        rows = []
        images = {}
        for row in ET.fromstring(archive.read(sheet_path)).findall(f'{{{S}}}sheetData/{{{S}}}row'):
            values = {}
            image_path = floating_images.get(int(row.get('r')))
            for cell in row.findall(f'{{{S}}}c'):
                column = ''.join(char for char in cell.get('r') if char.isalpha())
                node = cell.find(f'{{{S}}}v')
                value = node.text if node is not None else ''
                if cell.get('t') == 's' and value:
                    value = strings[int(value)]
                values[column] = (value or '').strip()
                if column == 'D' and cell.get('vm'):
                    value_index = value_metadata[int(cell.get('vm')) - 1]
                    rich_index = future[value_index]
                    image_index = rich_values[rich_index]
                    image_path = rich_rels[ordered_rels[image_index]]
            if not values.get('B', '').isdigit():
                continue
            sku = values['B']
            if image_path:
                image_key = int(row.get('r')) if images_by_row else sku
                images[image_key] = (PurePosixPath(image_path).suffix, archive.read(image_path))
            rows.append(dict(row=int(row.get('r')), sku=sku, name=values.get('C', ''),
                             category=values.get('E', ''), unit=values.get('F', ''),
                             image_embedded=bool(image_path)))
        return sheet.get('name'), rows, images
