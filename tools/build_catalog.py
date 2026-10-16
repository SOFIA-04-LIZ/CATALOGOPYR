"""Generate the static catalog from inventory records and curated product families."""
import csv
import json
from html import escape
from pathlib import Path

from catalog_model import organize_catalog

ROOT = Path(__file__).resolve().parents[1]


def render_card(product, categories):
    def e(value):
        return escape(str(value), quote=True)
    variants = product['variants']
    first = variants[0]
    attrs = (f'data-id="{e(product["id"])}" data-category="{e(product["category"])}" '
             f'data-variants="{e(json.dumps(variants, ensure_ascii=False))}"')
    options = ''
    if len(variants) > 1:
        options = (f'<label class="variant-field">{e(product["selector_label"])}'
                   f'<select class="variant-select" aria-label="{e(product["selector_label"] + " de " + product["name"])}">' +
                   ''.join(f'<option value="{e(variant["sku"])}">{e(variant["label"])}</option>' for variant in variants) +
                   '</select></label>')
    note = f'<p class="product-note"{ "" if first["note"] else " hidden"}>{e(first["note"])}</p>'
    return f'''<div class="card" {attrs}>
    <img loading="lazy" decoding="async" width="240" height="200" src="{e(first['image'])}" alt="{e(first['name'])}">
    <h3>{e(product['name'])}</h3>
    <p>{e(categories[product['category']])}</p>
    <p class="product-type">{e(product['subcategory'])}</p>
    {options}
    <span class="sku-display">SKU: {e(first['sku'])}</span>
    <p class="product-unit"{'' if first['unit'] else ' hidden'}>{e('Unidad: ' + first['unit']) if first['unit'] else ''}</p>
    {note}
    <button type="button" onclick="agregarAlCarrito(this)">Agregar al carrito</button>
</div>'''


def build():
    catalog = json.loads((ROOT / 'data/catalog.json').read_text())
    groups = json.loads((ROOT / 'data/product-groups.json').read_text())
    categories = catalog['categories']
    products = organize_catalog(catalog, groups)
    template = (ROOT / 'tools/page-template.html').read_text()
    counts = {}
    for category in [None, *categories]:
        selected = [p for p in products if category is None or p['category'] == category]
        counts[category or 'index'] = len(selected)
        heading = categories[category] if category else 'Todos los materiales'
        links = '<ul id="categories-menu" hidden>\n'
        for key, name in categories.items():
            current = ' aria-current="page"' if key == category else ''
            links += f'<li><a href="{key}.html"{current}>{escape(name)}</a></li>\n'
        links += '</ul>'
        values = dict(TITLE='Catálogo PYR — ' + heading, CATEGORY_LINKS=links,
                      CURRENT_CATEGORY=escape(categories[category] if category else 'Inicio · Todos los materiales'),
                      CARDS='\n'.join(render_card(p, categories) for p in selected))
        page = template
        for key, value in values.items():
            page = page.replace('{{' + key + '}}', value)
        if category is None:
            page = page.replace('<a href="index.html">Inicio</a>', '<a href="index.html" aria-current="page">Inicio</a>')
        page = '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
        (ROOT / ((category or 'index') + '.html')).write_text(page)
    # Keep previously shared URLs useful, while exposing only Consumibles in the menu.
    consumables = (ROOT / 'CONSUMIBLES.html').read_text()
    legacy_page = consumables.replace('</head>', '<link rel="canonical" href="CONSUMIBLES.html">\n</head>')
    for legacy_name in ['HERRAMIENTAS.html', 'INSUMOS.html']:
        (ROOT / legacy_name).write_text(legacy_page)
    with (ROOT / 'data/inventario-clasificado.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(['SKU', 'Material', 'Grupo', 'Opción', 'Categoría', 'Tipo de material', 'Origen', 'Observaciones', 'UM'])
        for product in products:
            for variant in product['variants']:
                writer.writerow([variant['sku'], variant['name'], product['name'], variant['label'],
                                 categories[product['category']], product['subcategory'], variant['source'], variant['note'], variant['unit']])
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
