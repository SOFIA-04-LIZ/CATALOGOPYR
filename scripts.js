'use strict';

const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const cards = [...document.querySelectorAll('.card')];
const searchIndex = new Map();
const categoryFilter = document.getElementById('filtro-categoria');
const typeFilter = document.getElementById('filtro-subcategoria');
function indexCard(card) {
    searchIndex.set(card, normalize(card.textContent + ' ' + (card.dataset.skus || '') + ' ' + (card.dataset.productos || '')));
}
function buscarProducto() {
    const query = normalize(document.getElementById('buscador').value.trim());
    let count = 0;
    for (const card of cards) {
        const visible = searchIndex.get(card).includes(query) &&
            (!categoryFilter?.value || card.dataset.category === categoryFilter.value) &&
            (!typeFilter?.value || card.dataset.subcategory === typeFilter.value);
        card.hidden = !visible;
        if (visible) count++;
    }
    document.getElementById('sin-resultados').hidden = count > 0;
    const counter = document.getElementById('result-count');
    if (counter) counter.textContent = `${count} de ${cards.length} materiales`;
}

for (const card of cards) {
    const image = card.querySelector('img');
    if (image) image.alt = card.querySelector('h3').textContent.trim();
    const products = JSON.parse(card.dataset.productos || '{}');
    const sizes = JSON.parse(card.dataset.skus || '{}');
    const buttons = [...card.querySelectorAll('.opcion-btn')];
    const display = card.querySelector('.sku-display');
    function selectVariant(button) {
        const product = products[button.textContent.trim()];
        if (!product) return;
        buttons.forEach(item => {
            item.classList.toggle('active', item === button);
            item.setAttribute('aria-pressed', String(item === button));
        });
        // Avoid resetting an image request when the selected source is unchanged.
        if (image.getAttribute('src') !== product.img) image.src = product.img;
        display.textContent = product.sku;
    }
    if (Object.keys(products).length) {
        buttons.forEach(button => button.addEventListener('click', () => selectVariant(button)));
        const active = card.querySelector('.opcion-btn.active') || buttons[0];
        if (active) selectVariant(active);
    }
    const selector = card.querySelector('select');
    if (selector) {
        selector.setAttribute('aria-label', 'Talla de ' + card.querySelector('h3').textContent.trim());
        if (Object.keys(sizes).length) {
            const update = () => { display.textContent = sizes[selector.value]; };
            selector.addEventListener('change', update);
            update();
        } else {
            selector.dispatchEvent(new Event('change'));
        }
    }
    indexCard(card);
}
let searchFrame;
document.getElementById('buscador').addEventListener('input', () => {
    cancelAnimationFrame(searchFrame);
    searchFrame = requestAnimationFrame(buscarProducto);
});
categoryFilter?.addEventListener('change', () => {
    const page = location.pathname.split('/').pop();
    if (page && page !== 'index.html') {
        location.href = categoryFilter.value ? categoryFilter.value + '.html' : 'index.html';
        return;
    }
    typeFilter.value = '';
    buscarProducto();
});
typeFilter?.addEventListener('change', buscarProducto);
buscarProducto();

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
    const variant = card.querySelector('.opcion-btn.active');
    const size = card.querySelector('select');
    const option = size ? size.value : variant?.textContent.trim();
    carrito.push({
        nombre: card.querySelector('h3').textContent.trim() + (option ? ' — ' + option : ''),
        sku: card.querySelector('span').textContent.trim(),
        img: card.querySelector('img')?.getAttribute('src') || 'Images/placeholder.svg'
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
