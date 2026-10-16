"""Organize presentation families without changing the original inventory records."""


def material_variants(product, label=''):
    sizes = product['sizes']
    selector_label = 'Llaves' if product['id'] == 'dispatch-68' else 'Talla'
    variants = []
    for size, sku in (sizes.items() if sizes else [('', product['sku'])]):
        size_label = (f'{size} llave' + ('s' if size != '1' else '')) if selector_label == 'Llaves' else size
        option = ' — '.join(value for value in [label, size_label] if value)
        variants.append(dict(
            sku=sku, label=option, image=product['image'], name=product['name'],
            source_id=product['id'], source=product['source'],
            cart_name=product['name'] + (f' — {selector_label}: {size}' if size else ''),
            note=product.get('note', ''), unit=product.get('unit', ''),
            aliases=product.get('aliases', []),
        ))
    return variants


def organize_catalog(catalog, groups):
    products = {product['id']: product for product in catalog['products']}
    memberships = {}
    group_views = {}
    for group in groups:
        variants = []
        members = group['members']
        if len(members) < 2:
            raise ValueError(f'Group must have at least two materials: {group["id"]}')
        category = products[members[0][0]]['category']
        for product_id, label in members:
            if product_id in memberships:
                raise ValueError(f'Material is grouped twice: {product_id}')
            product = products[product_id]
            if product['category'] != category:
                raise ValueError(f'Group crosses categories: {group["id"]}')
            memberships[product_id] = group['id']
            variants.extend(material_variants(product, label))
        first = products[members[0][0]]
        group_views[group['id']] = dict(
            id=group['id'], name=group['name'], category=category,
            subcategory=first['subcategory'], selector_label=group['label'], variants=variants,
        )
    views = []
    emitted = set()
    for product in catalog['products']:
        group_id = memberships.get(product['id'])
        if group_id:
            if group_id not in emitted:
                views.append(group_views[group_id])
                emitted.add(group_id)
        else:
            views.append(dict(
                id=product['id'], name=product['name'], category=product['category'],
                subcategory=product['subcategory'],
                selector_label='Llaves' if product['id'] == 'dispatch-68' else 'Talla',
                variants=material_variants(product),
            ))
    return views
