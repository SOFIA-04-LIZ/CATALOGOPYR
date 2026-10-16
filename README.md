# Catálogo PYR

Catálogo estático en español, sin dependencias ni compilación obligatoria. Publicar los HTML, `styles.css`, `scripts.js` y la carpeta `Images` juntos, conservando los nombres y mayúsculas.

Para revisar localmente, ejecutar `python3 -m http.server 8000` desde esta carpeta y abrir http://localhost:8000.

## Inventario y categorías

La comparación del 16 de octubre de 2026 con [Productos Despacho](https://almacengeneral.github.io/Productos-Despacho/index.html) cubre sus **321 fichas y 377 SKU**, incluidas tallas y número de llaves. El proyecto conserva además el SKU local `5537478`, que difiere del SKU `4056842` que el enlace asigna al mismo limpiador de espuma. Ambos están visibles y el SKU local lleva una nota para confirmar con inventario.

- `data/catalog.json`: lista central de 322 fichas / 378 SKU y su clasificación.
- `data/product-groups.json`: familias, nombres y opciones de los desplegables.
- `data/source-dispatch.json`: datos extraídos del enlace para comprobar la cobertura.
- `data/inventario-clasificado.csv`: inventario por SKU, para abrir en Excel.
- `data/reconciliation.json`: faltantes recuperados y diferencias detectadas.
- `REVISION-CATALOGO.md`: resultados y criterios de clasificación.

Los 322 registros se presentan en **266 tarjetas**, con 31 familias agrupadas por color, género, manga, medida o presentación. Todos los 378 SKU siguen disponibles. Cada opción de un desplegable actualiza imagen, SKU y datos del carrito. Los cascos se agrupan por modelo (BUM CAP, MCA e Infracap); los modelos y funciones de protección distintos conservan tarjetas independientes.

Cada tarjeta aparece en Inicio y en una sola categoría. Las categorías se abren desde el menú superior junto a Inicio; se retiró el bloque inferior de filtros, título y contador. El buscador reconoce también los nombres y SKU de las variantes y selecciona automáticamente la opción coincidente.

## Actualizar productos

Editar los materiales en `data/catalog.json` y sus agrupaciones en `data/product-groups.json`; después ejecutar:

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

Las pruebas verifican cobertura exacta de materiales y SKU de la fuente, tallas, imágenes locales, categorías sin omisiones ni duplicados, JSON e identificadores HTML. Abrir `tests/browser.html` desde el servidor local para probar búsqueda, navegación superior, todas las opciones y carrito en las 14 páginas, con anchos de escritorio y celular. Usar un perfil de pruebas: la comprobación vacía el carrito local.

Las imágenes se cargan de forma diferida; el buscador utiliza un índice en memoria y admite consultas sin acentos. El carrito conserva los productos entre páginas mediante almacenamiento local y funciona también si el navegador lo bloquea.

## Diseño para celulares

El catálogo conserva tres columnas desde 320 px y pasa a cuatro, cinco o seis en pantallas grandes. En celulares se ajustan imágenes, texto, espaciado y controles; los botones y selectores mantienen una altura mínima de 44 px. Las categorías están únicamente en la navegación superior, sin filtros ni contadores debajo del buscador. Los recursos compartidos llevan una versión en su URL para solicitar el diseño actualizado al publicar.
