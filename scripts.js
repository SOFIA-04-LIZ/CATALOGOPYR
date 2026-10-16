'use strict';

const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const cards = [...document.querySelectorAll('.card')];
const searchIndex = new Map();
const cardVariants = new Map();
const selectedVariants = new Map();

function selectVariant(card, variant) {
    const image = card.querySelector('img');
    if (image.getAttribute('src') !== variant.image) image.src = variant.image;
    image.alt = variant.name;
    card.querySelector('.sku-display').textContent = 'SKU: ' + variant.sku;
    const selector = card.querySelector('.variant-select');
    if (selector) selector.value = variant.sku;
    const note = card.querySelector('.product-note');
    note.textContent = variant.note;
    note.hidden = !variant.note;
    selectedVariants.set(card, variant);
}

for (const card of cards) {
    const variants = JSON.parse(card.dataset.variants);
    cardVariants.set(card, variants);
    selectVariant(card, variants[0]);
    card.querySelector('.variant-select')?.addEventListener('change', event => {
        const variant = variants.find(item => item.sku === event.target.value);
        if (variant) selectVariant(card, variant);
    });
    searchIndex.set(card, normalize(card.textContent + ' ' + variants.map(item =>
        [item.name, item.label, item.sku].join(' ')).join(' ')));
}

function buscarProducto() {
    const query = normalize(document.getElementById('buscador').value.trim());
    let count = 0;
    for (const card of cards) {
        const visible = searchIndex.get(card).includes(query);
        card.hidden = !visible;
        if (!visible) continue;
        count++;
        // Searching for a specific SKU or color also displays the matching option.
        if (query) {
            const matches = variant => normalize([variant.name, variant.label, variant.sku].join(' ')).includes(query);
            if (!matches(selectedVariants.get(card))) {
                const variant = cardVariants.get(card).find(matches);
                if (variant) selectVariant(card, variant);
            }
        }
    }
    document.getElementById('sin-resultados').hidden = count > 0;
}
let searchFrame;
document.getElementById('buscador').addEventListener('input', () => {
    cancelAnimationFrame(searchFrame);
    searchFrame = requestAnimationFrame(buscarProducto);
});
buscarProducto();

const categoryToggle = document.querySelector('.categories-toggle');
const categoryMenu = document.getElementById('categories-menu');
function closeCategories() {
    categoryMenu.hidden = true;
    categoryToggle.setAttribute('aria-expanded', 'false');
}
categoryToggle.addEventListener('click', () => {
    categoryMenu.hidden = !categoryMenu.hidden;
    categoryToggle.setAttribute('aria-expanded', String(!categoryMenu.hidden));
});
document.addEventListener('click', event => {
    if (!categoryToggle.contains(event.target) && !categoryMenu.contains(event.target)) closeCategories();
});
document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !categoryMenu.hidden) {
        closeCategories();
        categoryToggle.focus();
    }
});

let carrito = [];
try {
    const stored = JSON.parse(localStorage.getItem('pyr-cart') || '[]');
    if (Array.isArray(stored)) carrito = stored.filter(item => item && typeof item.nombre === 'string' && typeof item.sku === 'string' && typeof item.img === 'string');
} catch { /* The catalog also works when storage is unavailable. */ }
function actualizarCarrito() {
    document.getElementById('cart-count').textContent = carrito.length;
    try { localStorage.setItem('pyr-cart', JSON.stringify(carrito)); } catch { /* Storage can be disabled. */ }
}
function agregarAlCarrito(button) {
    const card = button.closest('.card');
    const variant = selectedVariants.get(card);
    carrito.push({
        nombre: variant.cart_name,
        sku: 'SKU: ' + variant.sku,
        img: variant.image
    });
    actualizarCarrito();
    renderCarrito();
}
function toggleCarrito() {
    const panel = document.getElementById('cart-panel');
    const open = getComputedStyle(panel).display === 'none';
    panel.style.display = open ? 'block' : 'none';
    document.querySelector('.cart-container').setAttribute('aria-expanded', String(open));
}
function renderCarrito() {
    const fragment = document.createDocumentFragment();
    carrito.forEach((product, index) => {
        const row = document.createElement('div');
        row.className = 'cart-item';
        const image = document.createElement('img');
        // Only local catalog assets may be restored from storage.
        image.src = /^Images\//.test(product.img) ? product.img : 'Images/placeholder.svg';
        image.alt = '';
        image.className = 'cart-img';
        const info = document.createElement('div');
        info.className = 'cart-info';
        for (const [value, className] of [[product.nombre, 'cart-nombre'], [product.sku, 'cart-sku']]) {
            const span = document.createElement('span');
            span.className = className;
            span.textContent = value;
            info.append(span);
        }
        const remove = document.createElement('button');
        remove.className = 'btn-eliminar';
        remove.textContent = 'X';
        remove.setAttribute('aria-label', 'Eliminar ' + product.nombre);
        remove.addEventListener('click', () => eliminarProducto(index));
        row.append(image, info, remove);
        fragment.append(row);
    });
    document.getElementById('cart-items').replaceChildren(fragment);
}
function eliminarProducto(index) {
    carrito.splice(index, 1);
    actualizarCarrito();
    renderCarrito();
}
function vaciarCarrito() {
    carrito = [];
    actualizarCarrito();
    renderCarrito();
}
actualizarCarrito();
renderCarrito();
