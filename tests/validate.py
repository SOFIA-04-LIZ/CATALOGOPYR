"""Validate all static pages without installing dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import json
import unittest
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from catalog_model import organize_catalog

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.assets = []
        self.cards = 0
        self.product_ids = []
        self.skus = set()
        self.variants = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('img', 'script', 'link'):
            self.assets.append(attrs.get('src', attrs.get('href', '')).split('?', 1)[0])
        if 'card' in attrs.get('class', '').split():
            self.cards += 1
            self.product_ids.append(attrs.get('data-id'))
        if 'data-variants' in attrs:
            variants = json.loads(attrs['data-variants'])
            self.variants.extend(variants)
            self.assets.extend(item['image'] for item in variants)
        for key in ('data-productos', 'data-skus'):
            if key in attrs:
                data = json.loads(attrs[key])
                if key == 'data-productos':
                    self.assets.extend(item['img'] for item in data.values())

class CatalogTests(unittest.TestCase):
    def test_pages(self):
        for path in ROOT.glob('*.html'):
            with self.subTest(page=path.name):
                page = Page()
                page.feed(path.read_text())
                self.assertEqual(len(page.ids), len(set(page.ids)), 'Duplicate IDs')
                for asset in page.assets:
                    self.assertTrue((ROOT / asset).is_file(), asset)
                self.assertIn('sin-resultados', page.ids)
                self.assertIn('catalogo', page.ids)
                self.assertIn('categories-menu', page.ids)
                self.assertNotIn('filtro-categoria', page.ids)
                self.assertNotIn('filtro-subcategoria', page.ids)
                self.assertNotIn('result-count', page.ids)

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'data/catalog.json').read_text())
        self.source = json.loads((ROOT / 'data/source-dispatch.json').read_text())
        groups = json.loads((ROOT / 'data/product-groups.json').read_text())
        self.views = organize_catalog(self.catalog, groups)

    def test_every_source_material_and_variant_is_present(self):
        products = {p.get('source_name'): p for p in self.catalog['products'] if p['source'] == 'dispatch'}
        self.assertEqual(len(products), len(self.source['products']))
        for row in self.source['products']:
            with self.subTest(product=row['name']):
                product = products[row['name']]
                self.assertEqual(set(row['skus']), {product['sku'], *product['sizes'].values()})
                self.assertEqual(row['sizes'], product['sizes'])

    def test_each_product_is_listed_in_exactly_one_category(self):
        ids = []
        for category in self.catalog['categories']:
            page = Page()
            page.feed((ROOT / (category + '.html')).read_text())
            expected = [p['id'] for p in self.views if p['category'] == category]
            self.assertCountEqual(page.product_ids, expected)
            ids.extend(page.product_ids)
        self.assertCountEqual(ids, [p['id'] for p in self.views])
        self.assertEqual(len(ids), len(set(ids)))
        page = Page()
        page.feed((ROOT / 'index.html').read_text())
        self.assertCountEqual(page.product_ids, ids)

    def test_all_products_have_real_skus_and_local_images(self):
        for product in self.catalog['products']:
            with self.subTest(product=product['name']):
                self.assertTrue(product['sku'].isdigit())
                self.assertIn(product['category'], self.catalog['categories'])
                self.assertTrue((ROOT / product['image']).is_file())
                self.assertNotEqual(product['image'], 'Images/placeholder.svg')
                if product['sizes']:
                    self.assertIn(product['sku'], product['sizes'].values())

    def test_grouping_keeps_every_sku_name_and_image(self):
        page = Page()
        page.feed((ROOT / 'index.html').read_text())
        expected = []
        for product in self.catalog['products']:
            for sku in (product['sizes'].values() if product['sizes'] else [product['sku']]):
                expected.append((product['id'], sku, product['name'], product['image']))
        actual = [(v['source_id'], v['sku'], v['name'], v['image']) for v in page.variants]
        self.assertCountEqual(actual, expected)
        self.assertEqual(len({v['sku'] for v in page.variants}), len(page.variants))
        with (ROOT / 'data/inventario-clasificado.csv').open(encoding='utf-8-sig') as file:
            rows = list(csv.DictReader(file))
        self.assertCountEqual([r['SKU'] for r in rows], [v['sku'] for v in page.variants])

    def test_color_and_gender_families_are_grouped(self):
        views = {p['id']: p for p in self.views}
        expected = {
            'cascos-bum-cap': {'5517586', '5517584'},
            'cascos-infracap': {'5533306', '5506506', '5533305', '5526770'},
            'cascos-mca': {'5541826', '5541827'},
            'batas-laboratorio': {'5539468', '5539469'},
            'candados-seguridad': {'5541030', '4233278', '5524014', '4231438'},
        }
        for group, skus in expected.items():
            self.assertEqual({v['sku'] for v in views[group]['variants']}, skus)
        # Safety functions and different models remain separate products.
        for product_id in ['dispatch-67', 'dispatch-71', 'dispatch-97', 'dispatch-98']:
            self.assertIn(product_id, views)

    def test_every_excel_material_is_present_once(self):
        workbook = json.loads((ROOT / 'data/source-excel.json').read_text())
        products = {sku: p for p in self.catalog['products'] for sku in [p['sku'], *p['sizes'].values()]}
        page = Page()
        page.feed((ROOT / 'index.html').read_text())
        rendered_skus = [v['sku'] for v in page.variants]
        self.assertEqual(len(workbook['materials']), 23)
        self.assertEqual(sum(row['status'] == 'added' for row in workbook['materials']), 21)
        for row in workbook['materials']:
            with self.subTest(sku=row['sku']):
                product = products[row['sku']]
                self.assertEqual(rendered_skus.count(row['sku']), 1)
                self.assertEqual(product.get('unit'), row['unit'])
                self.assertIn(row['name'], product['aliases'])
                self.assertEqual(product['category'], row['catalog_category'])
                if row['status'] == 'added':
                    self.assertEqual(product['source'], 'excel')
                    self.assertEqual(product['image'], row['image'])

    def test_conflicting_local_sku_is_preserved(self):
        local = [p for p in self.catalog['products'] if p['source'] == 'local']
        self.assertEqual([p['sku'] for p in local], ['5537478'])
        self.assertTrue(local[0].get('note'))


if __name__ == '__main__':
    unittest.main()
