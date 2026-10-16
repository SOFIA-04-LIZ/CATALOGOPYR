"""Validate all static pages without installing dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.assets = []
        self.cards = 0
        self.product_ids = []
        self.skus = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('img', 'script', 'link'):
            self.assets.append(attrs.get('src', attrs.get('href', '')))
        if 'card' in attrs.get('class', '').split():
            self.cards += 1
            self.product_ids.append(attrs.get('data-id'))
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

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'data/catalog.json').read_text())
        self.source = json.loads((ROOT / 'data/source-dispatch.json').read_text())

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
            expected = [p['id'] for p in self.catalog['products'] if p['category'] == category]
            self.assertCountEqual(page.product_ids, expected)
            ids.extend(page.product_ids)
        self.assertCountEqual(ids, [p['id'] for p in self.catalog['products']])
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

    def test_conflicting_local_sku_is_preserved(self):
        local = [p for p in self.catalog['products'] if p['source'] == 'local']
        self.assertEqual([p['sku'] for p in local], ['5537478'])
        self.assertTrue(local[0].get('note'))


if __name__ == '__main__':
    unittest.main()
