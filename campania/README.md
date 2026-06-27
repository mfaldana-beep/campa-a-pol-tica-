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

## Notas
- La imagen de **recolectores** entregada era una página web guardada (`RECOLECTORES.html`) cuyas
  imágenes internas son miniaturas de baja resolución y con posibles derechos de autor, por lo que
  **no se usaron**. El tema de la recolección se representa con la foto de cafetales e ilustración
  vectorial. Si envías una foto propia de recolectores en buena resolución, se integra fácilmente.
- En la **valla** y la **tarjeta** los datos de contacto (teléfono, correo, redes) son provisionales
  y se cambian en `generar.py`.
