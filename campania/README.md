# El Sello del Cafetero — PLANCHA 2 · «Comprometidos con los Cafeteros»

Sistema visual de campaña para la candidatura al **Comité Departamental de Cafeteros**.

- **Principal:** Jhon Esneider Prieto Prieto
- **Suplente:** Nelson Ferned Orozco Castaño
- **Eslogan:** Comprometidos con los Cafeteros · **Lema:** Por unos cafeteros prósperos

## Concepto
La candidatura se trata como una **marca de café de especialidad**: sobria, cálida y con arraigo.
Elementos del sistema:
- **Emblema-sello** circular como firma de marca.
- **Retratos en arco** (estilo editorial / herencia).
- **Líneas topográficas** que evocan la cordillera y el Nevado del Ruiz.
- **Íconos de línea** propios para cada propuesta.
- **Marca de tarjetón electoral** (casilla con X · «marca el 2»).
- Paleta cálida: crema, espresso, terracota, verde olivo y dorado.

## Cómo ver
Abre **`index.html`** (galería con la pieza animada y todas las piezas).

## Piezas (`campania/`)
| Archivo | Pieza | Tamaño |
|---|---|---|
| `00-marca.svg` | Emblema / sello | 1000×1000 |
| `01-afiche-principal.svg` | Afiche principal | 1000×1414 |
| `02-afiche-propuestas.svg` | Afiche de propuestas | 1000×1414 |
| `03-pasacalle.svg` | Pasacalle | 2400×480 |
| `04-valla.svg` | Valla publicitaria | 2400×1200 |
| `05a-tarjeta-frente.svg` | Tarjeta (frente) | 1050×600 |
| `05b-tarjeta-respaldo.svg` | Tarjeta (respaldo) | 1050×600 |
| `06-redes-post.svg` | Post de redes | 1080×1080 |
| `07-redes-historia.svg` | Historia de redes | 1080×1920 |
| `08-volante.svg` | Volante | 1000×1414 |
| `09-hero-animado.svg` | Pieza animada (web/redes) | 1080×1080 |

## PNG para imprimir
Abre **`exportar-png.html`** y descarga cada pieza (o todas) en alta resolución.
Para vallas y pasacalles, entrega el **.svg** a la imprenta (vectorial, sin pérdida).

## Editar / regenerar
```bash
python3 generar.py
```
Textos, colores, propuestas y datos están al inicio de `generar.py`.

## Notas
- Las fotos `assets/cafeteros.jpg` (y `cafetero2.jpg`) se extrajeron del archivo `RECOLECTORES.html`
  y son de **baja resolución** (placeholder). Reemplázalas por fotos propias en alta (mismo nombre) y regenera.
- La pieza animada usa SVG/SMIL; se ve en navegador. No se exporta a PNG (es para uso digital).
