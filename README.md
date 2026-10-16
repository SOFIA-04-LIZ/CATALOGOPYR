# Catálogo PYR

Catálogo estático en español, sin dependencias ni compilación obligatoria. Publicar los HTML, `styles.css`, `scripts.js` y la carpeta `Images` juntos, conservando los nombres y mayúsculas.

Para revisar localmente, ejecutar `python3 -m http.server 8000` desde esta carpeta y abrir http://localhost:8000.

## Inventario y categorías

La comparación del 16 de octubre de 2026 con [Productos Despacho](https://almacengeneral.github.io/Productos-Despacho/index.html) cubre sus **321 fichas y 377 SKU**, incluidas tallas y número de llaves. El proyecto conserva además el SKU local `5537478`, que difiere del SKU `4056842` que el enlace asigna al mismo limpiador de espuma. Ambos están visibles y el SKU local lleva una nota para confirmar con inventario.

- `data/catalog.json`: lista central de 322 fichas / 378 SKU y su clasificación.
- `data/source-dispatch.json`: datos extraídos del enlace para comprobar la cobertura.
- `data/inventario-clasificado.csv`: inventario por SKU, para abrir en Excel.
- `data/reconciliation.json`: faltantes recuperados y diferencias detectadas.
- `REVISION-CATALOGO.md`: resultados y criterios de clasificación.

Cada material aparece en Inicio y en una sola categoría. Las variantes por talla permanecen en el mismo producto; los colores, prendas y presentaciones del enlace tienen fichas individuales para mostrar su imagen y SKU correctos. EPP también se divide por tipo de protección. Los filtros de categoría, tipo y búsqueda se pueden combinar.

## Actualizar productos

Editar `data/catalog.json` y ejecutar:

```sh
python3 tools/build_catalog.py
```

Esto regenera Inicio, las 13 categorías y el CSV. Para cambiar la estructura compartida, editar `tools/page-template.html`. No editar las páginas generadas por separado, porque la siguiente generación reemplaza esos cambios.

El importador `python3 tools/import_dispatch.py ruta/al/index-descargado.html` permite reconstruir los datos a partir de una copia del enlace. **Reemplaza** `data/catalog.json` y `data/source-dispatch.json`; usarlo al actualizar la fuente y revisar las diferencias antes de regenerar. Los cambios manuales en la lista central deben preservarse antes de otra importación.

## Validación

```sh
python3 tests/validate.py
node --check scripts.js
```

Las pruebas verifican cobertura exacta de materiales y SKU de la fuente, tallas, imágenes locales, categorías sin omisiones ni duplicados, JSON e identificadores HTML. Abrir `tests/browser.html` desde el servidor local para probar búsqueda, filtros, selección de tallas y carrito en las 14 páginas. Usar un perfil de pruebas: la comprobación vacía el carrito local.

Las imágenes se cargan de forma diferida; el buscador utiliza un índice en memoria y admite consultas sin acentos. El carrito conserva los productos entre páginas mediante almacenamiento local y funciona también si el navegador lo bloquea.
