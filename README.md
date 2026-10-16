# Catálogo PYR

Catálogo estático en español, sin dependencias ni compilación obligatoria. Publicar los HTML, `styles.css`, `scripts.js` y la carpeta `Images` juntos, conservando los nombres y mayúsculas.

Para revisar localmente, ejecutar `python3 -m http.server 8000` desde esta carpeta y abrir http://localhost:8000.

## Inventario y categorías

La comparación del 16 de octubre de 2026 con [Productos Despacho](https://almacengeneral.github.io/Productos-Despacho/index.html) cubre sus **321 fichas y 377 SKU**, incluidas tallas y número de llaves. El proyecto conserva además el SKU local `5537478`, que difiere del SKU `4056842` que el enlace asigna al mismo limpiador de espuma. Ambos están visibles y el SKU local lleva una nota para confirmar con inventario.

- `data/catalog.json`: lista central de 366 registros / 422 SKU y su clasificación.
- `data/product-groups.json`: familias, nombres y opciones de los desplegables.
- `data/source-dispatch.json`: datos extraídos del enlace para comprobar la cobertura.
- `data/inventario-clasificado.csv`: inventario por SKU, para abrir en Excel.
- `data/source-libro4.json`: comparación por fila de Libro4, materiales añadidos, existentes y dos registros con SKU pendiente de confirmar.
- `data/source-excel.json`: registro de los 23 materiales del Excel, filas de origen, unidades, clasificación y resultado de la comparación.
- `data/reconciliation.json`: faltantes recuperados y diferencias detectadas.
- `REVISION-CATALOGO.md`: resultados y criterios de clasificación.

Los 366 registros se presentan en **309 tarjetas**, con 32 familias agrupadas por color, género, manga, medida o presentación. Todos los 422 SKU están disponibles. Cada opción de un desplegable actualiza imagen, SKU y datos del carrito. Los cascos se agrupan por modelo (BUM CAP, MCA e Infracap); los modelos y funciones de protección distintos conservan tarjetas independientes.

Cada tarjeta aparece en Inicio y en una sola categoría. Las categorías se abren desde el menú superior junto a Inicio; se retiró el bloque inferior de filtros, título y contador. El buscador reconoce también los nombres y SKU de las variantes y selecciona automáticamente la opción coincidente.

## Materiales del Excel

Se incorporaron los 23 materiales de `Libro1 (005).xlsx`, hoja `SKUS NUEVOS`: 21 SKU nuevos y dos placas acrílicas existentes, sin duplicados. El archivo central mantiene las descripciones originales como alias de búsqueda y las unidades de manejo del Excel. Los 21 materiales añadidos usan sus imágenes extraídas del libro, optimizadas a un máximo de 640 px.

Se creó Consumibles para pilas, desechables, cintas y sellos. Los adhesivos, herramientas y EPP conservan sus categorías específicas. Las placas acrílicas pasaron a Refacciones, de acuerdo con el archivo recibido. Las plumas Paper Mate se agrupan por color y las pilas se muestran en cinco tarjetas individuales; el tamaño no indicado de la pila `4024835` se conserva sin inventar un valor.

`tools/read_xlsx.py` lee los valores y las imágenes del libro mediante los metadatos XML, incluidos los dibujos flotantes y las imágenes en celdas, sin ejecutar fórmulas. El registro de importación incluye el hash SHA-256 del archivo de origen. La copia del Excel permanece fuera del repositorio.

## Actualizar productos

Editar los materiales en `data/catalog.json` y sus agrupaciones en `data/product-groups.json`; después ejecutar:

```sh
python3 tools/build_catalog.py
```

Esto regenera Inicio, las 12 categorías y el CSV. Para cambiar la estructura compartida, editar `tools/page-template.html`. No editar las páginas generadas por separado, porque la siguiente generación reemplaza esos cambios.

El importador `python3 tools/import_dispatch.py ruta/al/index-descargado.html` permite reconstruir los datos a partir de una copia del enlace. **Reemplaza** `data/catalog.json` y `data/source-dispatch.json`; usarlo al actualizar la fuente y revisar las diferencias antes de regenerar. Los cambios manuales en la lista central deben preservarse antes de otra importación.

## Validación

```sh
python3 tests/validate.py
node --check scripts.js
```

Las pruebas verifican cobertura exacta de materiales y SKU de la fuente, tallas, imágenes locales, categorías sin omisiones ni duplicados, JSON e identificadores HTML. Abrir `tests/browser.html` desde el servidor local para probar búsqueda, navegación superior, todas las opciones y carrito en las 15 páginas, con anchos de escritorio y celular. Usar un perfil de pruebas: la comprobación vacía el carrito local.

Las imágenes se cargan de forma diferida; el buscador utiliza un índice en memoria y admite consultas sin acentos. El carrito conserva los productos entre páginas mediante almacenamiento local y funciona también si el navegador lo bloquea.

## Diseño para celulares

El catálogo conserva tres columnas desde 320 px y pasa a cuatro, cinco o seis en pantallas grandes. En celulares se ajustan imágenes, texto, espaciado y controles; los botones y selectores mantienen una altura mínima de 44 px. Las categorías están únicamente en la navegación superior, sin filtros ni contadores debajo del buscador. Los recursos compartidos llevan una versión en su URL para solicitar el diseño actualizado al publicar.

## Pie de página visible

La página ocupa la altura disponible de la pantalla (`100dvh`, con respaldo `100vh`). El encabezado, menú y pie tienen su espacio propio; solo `#catalog-content` se desplaza. El pie se mantiene visible también cuando la búsqueda no encuentra productos. Las pruebas del navegador comprueban la posición y que el pie sea el elemento pintado en pantalla.

## Categorías unificadas

Por solicitud del usuario, Herramientas y consumibles e Insumos generales se integraron en Consumibles. El papel aluminio y todos los materiales de esas categorías aparecen ahora ahí. El menú muestra 12 categorías; las direcciones antiguas `HERRAMIENTAS.html` e `INSUMOS.html` conservan una copia de Consumibles para que sigan funcionando los enlaces compartidos.

Las pilas C, AAA, de 9 V, de 1.5 V sin tamaño indicado y AA se muestran en tarjetas separadas, cada una con su foto, SKU y unidad de manejo.

## Actualización de Libro4.xlsx

La hoja `SKUS NUEVOS` contiene 49 renglones: 24 ya estaban registrados; se añadieron 23 materiales con SKU sin conflicto, sus imágenes y sus descripciones originales como alias de búsqueda. Los dos renglones restantes comparten `4300806` para materiales distintos: `RUEDA DENT REXNORD` (fila 43) y `BUCHACA MEDIA` (fila 45). Ambos se conservaron en el registro de importación y con imágenes independientes, pendientes de confirmar sus códigos antes de incorporarlos al catálogo público.

Las 23 altas se distribuyen en 21 Refacciones y dos Consumibles (diablito y cinta aislante). El archivo no indica unidades de manejo para ellas; se conservaron vacías. El catálogo tiene 366 registros, 422 SKU y 309 tarjetas. Los materiales existentes mantienen sus fotos, unidades y organización, incluidas las pilas en tarjetas individuales. El lector admite imágenes por fila para evitar que un código duplicado reemplace la imagen de otro material.
