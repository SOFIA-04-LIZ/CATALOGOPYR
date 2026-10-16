# Revisión del catálogo — 16 de octubre de 2026

Fuente: [Productos Despacho](https://almacengeneral.github.io/Productos-Despacho/index.html).

Se cotejaron las 321 fichas del HTML y todos los SKU de sus selectores, sin confundir números de modelo con SKU. El resultado incluye los 377 SKU distintos de la fuente y conserva un SKU adicional del proyecto: **322 fichas y 378 SKU**. No se eliminaron identificadores locales sin equivalencia confirmada.

## Recuperados

Se añadieron o corrigieron 11 SKU ausentes: borrador para pizarrón `5530050`, candado dieléctrico `5536106`, cascos Infracap `5533306`, `5506506`, `5533305`, `5526770`, cloro Cloralex `5506859`, faja lumbar en tallas M/G/XG `5506402`, `5506419`, `5506472` y limpiador de espuma `4056842`. La talla S de la faja usa `5507916`; el valor de la opción S estaba incorrecto en el HTML de la fuente y se reconstruyó a partir de su tabla de SKU.

Se recuperaron las imágenes del candado dieléctrico, la tarjeta PVC y la camisa caqui ignífuga desde la fuente. Todas las fichas usan archivos locales existentes.

## Separación

| Categoría | Fichas |
| --- | ---: |
| Limpieza | 44 |
| EPP | 77 |
| Papelería | 91 |
| Solventes | 6 |
| Lubricantes | 34 |
| Químicos | 21 |
| Uniformes | 19 |
| Refacciones | 1 |
| Gases | 4 |
| Adhesivos y selladores | 12 |
| Pinturas y recubrimientos | 5 |
| Herramientas y consumibles | 5 |
| Insumos generales | 3 |

La clasificación se hizo por uso del material. Las grasas, aceites y lubricadores quedaron en Lubricantes; los fijadores, resinas y siliconas en Adhesivos y selladores; los barnices, esmaltes y pinturas en Pinturas y recubrimientos. Los gases tienen categoría propia. La bombilla quedó en Refacciones. La cinta métrica, brochas y pastas de trabajo quedaron en Herramientas y consumibles; las placas acrílicas y el papel aluminio en Insumos generales. Se conservaron las denominaciones comerciales de la fuente.

EPP se separó además por protección de manos, calzado, cabeza, ojos/cara, oído, respiración, ropa corporal, bloqueo y señalización. Los cartuchos respiratorios se separaron del bloqueo LOTOTO, aunque la fuente los mezclaba.

## Diferencias que requieren cotejo con inventario

- **Limpiador de espuma de 400 g:** la fuente usa `4056842` y el proyecto tenía `5537478`. Se mantienen dos registros; el local lleva una nota visible. No se asume que uno sustituye al otro.
- **Mobil Glygoyle:** el proyecto tenía los SKU intercambiados. Se adoptó la relación del enlace: Glygoyle 30 = `4056384`; Glygoyle 460 = `4057131`.

El CSV contiene una fila por SKU con categoría, tipo de material, variante, origen y observaciones. La comprobación se refiere al contenido del enlace consultado; no verifica existencias físicas.
