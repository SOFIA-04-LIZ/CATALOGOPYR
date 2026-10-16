# Revisión del catálogo — 16 de octubre de 2026

Fuente: [Productos Despacho](https://almacengeneral.github.io/Productos-Despacho/index.html).

Se cotejaron las 321 fichas del HTML y todos los SKU de sus selectores, sin confundir números de modelo con SKU. El resultado incluye los 377 SKU distintos de la fuente y conserva un SKU adicional del proyecto: **322 registros y 378 SKU antes del Excel**. No se eliminaron identificadores locales sin equivalencia confirmada.

## Recuperados

Se añadieron o corrigieron 11 SKU ausentes: borrador para pizarrón `5530050`, candado dieléctrico `5536106`, cascos Infracap `5533306`, `5506506`, `5533305`, `5526770`, cloro Cloralex `5506859`, faja lumbar en tallas M/G/XG `5506402`, `5506419`, `5506472` y limpiador de espuma `4056842`. La talla S de la faja usa `5507916`; el valor de la opción S estaba incorrecto en el HTML de la fuente y se reconstruyó a partir de su tabla de SKU.

Se recuperaron las imágenes del candado dieléctrico, la tarjeta PVC y la camisa caqui ignífuga desde la fuente. Todas las fichas usan archivos locales existentes.

## Separación

| Categoría | Tarjetas agrupadas |
| --- | ---: |
| Limpieza | 38 |
| EPP | 71 |
| Papelería | 62 |
| Solventes | 6 |
| Lubricantes | 34 |
| Químicos | 21 |
| Uniformes | 10 |
| Refacciones | 5 |
| Gases | 4 |
| Adhesivos y selladores | 12 |
| Pinturas y recubrimientos | 5 |
| Herramientas y consumibles | 9 |
| Insumos generales | 1 |
| Consumibles | 4 |

La clasificación se hizo por uso del material. Las grasas, aceites y lubricadores quedaron en Lubricantes; los fijadores, resinas y siliconas en Adhesivos y selladores; los barnices, esmaltes y pinturas en Pinturas y recubrimientos. Los gases tienen categoría propia. La bombilla quedó en Refacciones. La cinta métrica, brochas y pastas de trabajo quedaron en Herramientas y consumibles; las placas acrílicas y el papel aluminio en Insumos generales. Se conservaron las denominaciones comerciales de la fuente.

EPP se separó además por protección de manos, calzado, cabeza, ojos/cara, oído, respiración, ropa corporal, bloqueo y señalización. Los cartuchos respiratorios se separaron del bloqueo LOTOTO, aunque la fuente los mezclaba.

## Agrupaciones y navegación

Se organizaron 33 familias con desplegables para color, género, manga, medida o presentación. Los cascos BUM CAP, MCA e Infracap tienen una tarjeta por modelo; las batas y chamarras permiten elegir Hombre/Mujer. También se agruparon blusas, camisas, playeras, bolígrafos, marcadores, cartuchos de impresión por modelo, viniles de colores y otras presentaciones equivalentes. Las botas y los guantes conservan sus tallas por modelo. No se mezclaron cartuchos respiratorios con funciones distintas, prendas ignífugas con ropa normal ni lubricantes con formulaciones distintas.

Cada selección muestra su foto y SKU y se guarda con el nombre concreto de la variante en el carrito. Se conservan los 399 SKU del catálogo actualizado y sus imágenes locales. El buscador encuentra nombres originales y SKU de cualquier opción, y muestra la variante encontrada. Las categorías permanecen en el menú superior, junto a Inicio; se retiraron los controles, título y contador inferiores.

## Diferencias que requieren cotejo con inventario

- **Limpiador de espuma de 400 g:** la fuente usa `4056842` y el proyecto tenía `5537478`. Se mantienen dos opciones en una sola tarjeta; la opción local muestra una nota al seleccionarla. No se asume que uno sustituye al otro.
- **Mobil Glygoyle:** el proyecto tenía los SKU intercambiados. Se adoptó la relación del enlace: Glygoyle 30 = `4056384`; Glygoyle 460 = `4057131`.

El CSV contiene una fila por SKU con grupo, opción, categoría, tipo de material, origen y observaciones. La comprobación se refiere al contenido del enlace consultado; no verifica existencias físicas.


## Incorporación de Libro1 (005).xlsx

La hoja `SKUS NUEVOS` contiene 23 materiales. Los SKU `4056625` y `4056931` (placas acrílicas) ya existían; se actualizaron su unidad de manejo y clasificación en Refacciones. Se añadieron los otros 21 SKU sin eliminar los anteriores. El catálogo final contiene **343 registros, 399 SKU y 282 tarjetas**.

Se recuperaron todas las imágenes del Excel; las de los 21 materiales nuevos se guardaron localmente y se limitaron a 640 px para reducir peso. Se añadieron 16 unidades de manejo a los registros nuevos y dos a las placas; las celdas vacías se conservaron sin asignar unidades supuestas. Las descripciones originales del libro siguen disponibles como alias para buscar por los nombres del inventario.

Se creó Consumibles, con cuatro tarjetas: pilas (cinco opciones), vasos desechables, masking tape y sellos de seguridad. Las plumas retráctiles Paper Mate tienen un selector de color independiente de los bolígrafos anteriores. Las mangas y cubrebocas se ubicaron en EPP; el adhesivo Loctite en Adhesivos y selladores; el disco, navaja, candado, linterna y flexómetro en Herramientas. El tejido de rafia, la lámina y la manguera se ubicaron en Refacciones conforme al libro.

El SKU `4024835` especifica 1.5 V y dos unidades, sin indicar tamaño: el desplegable lo señala así. El detalle por fila, las unidades originales y el hash del archivo se conservan en `data/source-excel.json`.
