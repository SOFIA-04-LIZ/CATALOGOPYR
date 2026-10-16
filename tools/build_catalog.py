"""Generate static catalog pages from one product list; no dependencies required."""
import csv
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render_card(product, categories):
    def e(value):
        return escape(str(value), quote=True)
    sizes = product['sizes']
    attrs = (f'data-id="{e(product["id"])}" data-category="{e(product["category"])}" '
             f'data-subcategory="{e(product["subcategory"])}"')
    if sizes:
        attrs += f' data-skus="{e(json.dumps({key: "SKU: " + sku for key, sku in sizes.items()}, ensure_ascii=False))}"'
    options = ''
    if sizes:
        selector_label = 'Llaves' if product['name'] == 'Candado de Seguridad Color Azul' else 'Talla'
        options = (f'<label>{selector_label}: <select class="selector-talla">' +
                   ''.join(f'<option value="{e(key)}">{e(key)}</option>' for key in sizes) +
                   '</select></label>')
    note = f'<p class="product-note">{e(product["note"])}</p>' if product.get('note') else ''
    sku = next(iter(sizes.values())) if sizes else product['sku']
    return f'''<div class="card" {attrs}>
    <img loading="lazy" decoding="async" width="240" height="200" src="{e(product['image'])}" alt="{e(product['name'])}">
    <h3>{e(product['name'])}</h3>
    <p>{e(categories[product['category']])}</p>
    <p class="product-type">{e(product['subcategory'])}</p>
    {options}
    <span class="sku-display">SKU: {e(sku)}</span>
    {note}
    <button type="button" onclick="agregarAlCarrito(this)">Agregar al carrito</button>
</div>'''


def build():
    catalog = json.loads((ROOT / 'data/catalog.json').read_text())
    categories, products = catalog['categories'], catalog['products']
    template = (ROOT / 'tools/page-template.html').read_text()
    links = '<ul>\n' + '\n'.join(f'<li><a href="{key}.html">{escape(name)}</a></li>' for key, name in categories.items()) + '\n</ul>'
    counts = {}
    for category in [None, *categories]:
        selected = [p for p in products if category is None or p['category'] == category]
        counts[category or 'index'] = len(selected)
        heading = categories[category] if category else 'Todos los materiales'
        category_options = '<option value="">Todas las categorías</option>'
        for key, name in categories.items():
            attr = ' selected' if key == category else ''
            category_options += f'<option value="{key}"{attr}>{escape(name)}</option>'
        subcategory_options = '<option value="">Todos los tipos</option>'
        subcategory_options += ''.join(f'<option value="{escape(name, quote=True)}">{escape(name)}</option>' for name in sorted({p['subcategory'] for p in selected if p['subcategory']}))
        values = dict(TITLE='Catálogo PYR — ' + heading, HEADING=escape(heading), CATEGORY_LINKS=links,
                      CATEGORY_OPTIONS=category_options, SUBCATEGORY_OPTIONS=subcategory_options,
                      CARDS='\n'.join(render_card(p, categories) for p in selected))
        page = template
        for key, value in values.items():
            page = page.replace('{{' + key + '}}', value)
        page = '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
        (ROOT / ((category or 'index') + '.html')).write_text(page)
    with (ROOT / 'data/inventario-clasificado.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['SKU', 'Material', 'Variante', 'Categoría', 'Tipo de material', 'Origen', 'Observaciones'])
        for product in products:
            variants = product['sizes'].items() if product['sizes'] else [('', product['sku'])]
            for label, sku in variants:
                writer.writerow([sku, product['name'], label, categories[product['category']], product['subcategory'], product['source'], product.get('note', '')])
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
