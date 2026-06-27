# Campaña publicitaria — PLANCHA 2 · «Comprometidos con los Cafeteros»

Material gráfico para la candidatura al **Comité Departamental de Cafeteros**.

- **Principal:** Jhon Esneider Prieto Prieto
- **Suplente:** Nelson Ferned Orozco Castaño
- **Eslogan:** COMPROMETIDOS CON LOS CAFETEROS
- **Lema de campaña:** Por unos cafeteros prósperos

## Cómo ver las piezas
Abre **`index.html`** en el navegador: es una galería con todas las piezas. También puedes abrir
cada archivo `.svg` directamente (GitHub y cualquier navegador los muestran).

## Piezas incluidas
| Archivo | Pieza | Tamaño | Uso |
|---|---|---|---|
| `01-afiche-principal.svg` | Afiche principal | 1000×1500 | Cartel insignia |
| `02-afiche-propuestas.svg` | Afiche de propuestas | 1000×1500 | 5 ejes programáticos |
| `03-pasacalle.svg` | Pasacalle | 2400×480 | Banner de calle |
| `04-valla.svg` | Valla publicitaria | 2400×1200 | Gran formato |
| `05a-tarjeta-frente.svg` | Tarjeta (frente) | 1050×600 | Tarjeta de presentación |
| `05b-tarjeta-respaldo.svg` | Tarjeta (respaldo) | 1050×600 | Propuestas + contacto |
| `06-redes-post.svg` | Post de redes | 1080×1080 | Instagram/Facebook |
| `07-redes-historia.svg` | Historia de redes | 1080×1920 | Stories/WhatsApp |
| `08-volante.svg` | Volante | 1000×1414 | Volante de mano |

## Sistema de marca
Identidad cafetera: café tostado, rojo cereza, dorado del grano y verde de la hoja.

| Color | HEX | Uso |
|---|---|---|
| Espresso | `#241410` | Fondos oscuros y texto |
| Café | `#43271A` | Franjas |
| Rojo cereza | `#C0282D` | Acentos llamativos |
| Dorado | `#E0A23B` | Detalles, sello Plancha 2 |
| Verde hoja | `#2E7D32` | Naturaleza / prosperidad |
| Crema | `#FBF4E5` | Fondos claros |

## Cómo obtener PNG para imprimir
Abre **`exportar-png.html`** en cualquier navegador (doble clic). Lleva las 9 piezas incrustadas y te permite
**descargar cada una (o todas) en PNG** de alta resolución con un clic. Elige 2x para imprenta.

> Para gran formato (vallas, pasacalles) lo ideal es entregar el **.svg** a la imprenta: es vectorial y no pierde
> calidad a ningún tamaño. El PNG sirve para digital, redes y formatos pequeños/medianos.

## Cómo editar / regenerar
Todas las piezas se generan con un único script:
```bash
python3 generar.py
```
Edita `generar.py` para cambiar textos, colores (diccionario `C`), propuestas (`PROPUESTAS`)
o datos de contacto de la valla y la tarjeta. Las fotos se leen de la carpeta raíz del repositorio.

## Exportar a PNG / JPG / PDF (imprenta)
Los SVG son **vectoriales**, escalan sin perder calidad (sirven igual para una tarjeta o una valla):
- **Rápido:** abre el SVG en el navegador → Imprimir → Guardar como PDF.
- **Profesional:** ábrelo en Figma, Adobe Illustrator o Inkscape y exporta a la resolución que necesites.

## Notas de diseño
- **Composición por bloques de color** para máxima legibilidad y un look más llamativo.
- **Fotos naturales** (sin opacar) en **recuadros con marco sutil y paspartú cálido** que favorece los tonos de piel.
- Se incorporan **cafetales, Nevado del Ruiz y cafeteros** en varias piezas.
- **Texto con interlineado seguro** (sin solapes) y títulos con ajuste automático de ancho.
- Se **eliminaron** los datos de "Informes" y redes (@) de la valla y la tarjeta.
- **Importante:** las fotos `assets/cafeteros.jpg` y `assets/cafetero2.jpg` se extrajeron del archivo
  `RECOLECTORES.html` y son de **baja resolución** (placeholder). Reemplázalas por fotos propias de cafeteros
  en alta resolución (mismo nombre en `assets/`) y vuelve a ejecutar `python3 generar.py`.
