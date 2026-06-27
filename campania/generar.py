# -*- coding: utf-8 -*-
"""
Generador de la campaña publicitaria "PLANCHA 2 - COMPROMETIDOS CON LOS CAFETEROS"
Candidatos: Jhon Esneider Prieto Prieto (Principal) y Nelson Ferned Orozco Castaño (Suplente)
Comité Departamental de Cafeteros.

Produce piezas en SVG vectorial (escalable, listo para imprenta y redes) que incorporan
las fotos reales de los candidatos, la foto de cafetales y el Nevado del Ruiz, además de
ilustración vectorial cafetera (ramas, cerezas, recolección, montaña).
"""
import base64, os, html, xml.dom.minidom as minidom

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(BASE)  # carpeta del repo con las imagenes originales
OUT = BASE

# --------------------------------------------------------------------------------------
# 1. RECURSOS (fotos reales -> data URI base64)
# --------------------------------------------------------------------------------------
def data_uri(path, mime="image/jpeg"):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b}"

IMG = {
    "cafetales": data_uri(os.path.join(SRC, "CAFETALES.jpg")),
    "jhon":      data_uri(os.path.join(SRC, "Jhon Esneider Prieto Prieto.jpeg")),
    "nelson":    data_uri(os.path.join(SRC, "Nelson Ferned Orozco Castaño.jpeg")),
    "nevado":    data_uri(os.path.join(SRC, "NEVADO DEL RUIZ.jfif")),
}

# --------------------------------------------------------------------------------------
# 2. SISTEMA DE MARCA
# --------------------------------------------------------------------------------------
C = {
    "espresso": "#241410",   # café muy oscuro (fondos/typo)
    "brown":    "#43271A",   # café
    "coffee":   "#6F4A2E",   # café medio
    "red":      "#C0282D",   # rojo cereza (acento llamativo)
    "red_dark": "#8E1B20",
    "gold":     "#E0A23B",   # dorado tostado
    "gold_lt":  "#F4CE7E",   # dorado claro
    "green":    "#2E7D32",   # verde hoja
    "green_dk": "#1B5E20",
    "cream":    "#FBF4E5",   # crema fondo
    "cream2":   "#F0E2C4",
    "white":    "#FFFFFF",
}

SLOGAN = "COMPROMETIDOS CON LOS CAFETEROS"
ORG = "COMITÉ DEPARTAMENTAL DE CAFETEROS"
PLANCHA = "PLANCHA 2"

CANDIDATOS = {
    "principal": {"nombre": "JHON ESNEIDER PRIETO PRIETO", "rol": "PRINCIPAL", "img": "jhon"},
    "suplente":  {"nombre": "NELSON FERNED OROZCO CASTAÑO", "rol": "SUPLENTE", "img": "nelson"},
}

PROPUESTAS = [
    ("VÍAS PARA EL CAMPO", "Buenas vías de comunicación que conecten nuestras veredas y saquen el café a tiempo."),
    ("RENOVACIÓN DEL CAFÉ", "Mejores incentivos por la renovación de cafetales para cosechas más productivas."),
    ("BENEFICIADEROS", "Mejoramiento y construcción de beneficiaderos para un café de mayor calidad."),
    ("MUJER CAFETERA", "Proyectos productivos para las mujeres del campo y su autonomía económica."),
    ("DEFENSORÍA DEL CAFETERO", "Una defensoría que vele por los derechos y el bienestar de cada caficultor."),
]

def esc(t):
    return html.escape(str(t), quote=True)

# --------------------------------------------------------------------------------------
# 3. MOTIVOS VECTORIALES (ilustración cafetera)
# --------------------------------------------------------------------------------------
def cherry(cx, cy, r, color=None):
    color = color or C["red"]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["red_dark"]}" stroke-width="{r*0.12:.2f}" opacity="0.5"/>'
            f'<ellipse cx="{cx-r*0.32:.2f}" cy="{cy-r*0.34:.2f}" rx="{r*0.30:.2f}" ry="{r*0.22:.2f}" fill="#fff" opacity="0.45"/>')

def leaf(cx, cy, L, W, angle, color=None):
    color = color or C["green"]
    h = W / 2.0
    path = f'M0,0 C {L*0.28:.1f},{-h:.1f} {L*0.72:.1f},{-h:.1f} {L:.1f},0 C {L*0.72:.1f},{h:.1f} {L*0.28:.1f},{h:.1f} 0,0 Z'
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({angle:.1f})">'
            f'<path d="{path}" fill="{color}"/>'
            f'<path d="M{L*0.04:.1f},0 L {L*0.92:.1f},0" stroke="{C["green_dk"]}" stroke-width="{max(W*0.05,1):.1f}" opacity="0.55" fill="none"/>'
            f'</g>')

def sprig(x, y, scale=1.0, angle=0.0, flip=False, leaf_color=None, cherry_color=None):
    """Rama de café decorativa (sprig). Dibujada alrededor del origen y transformada."""
    lc = leaf_color or C["green"]
    cc = cherry_color or C["red"]
    fl = -1 if flip else 1
    p = [f'<g transform="translate({x:.1f},{y:.1f}) scale({scale*fl:.3f},{scale:.3f}) rotate({angle:.1f})">']
    # tallo
    p.append(f'<path d="M0,0 C 70,-8 150,-28 250,-22" stroke="{C["brown"]}" stroke-width="7" '
             f'fill="none" stroke-linecap="round"/>')
    # hojas a lo largo del tallo
    for (lx, ly, ll, lw, la) in [(55,-6,70,30,-38),(55,-6,66,28,28),(120,-20,76,33,-32),
                                  (120,-20,70,30,34),(185,-26,70,30,-28),(185,-26,64,28,40)]:
        p.append(leaf(lx, ly, ll, lw, la, lc))
    # racimo de cerezas al final
    for (chx, chy, chr_) in [(238,-30,15),(252,-16,16),(236,-8,14),(258,-30,13),(248,-44,12)]:
        p.append(cherry(chx, chy, chr_, cc))
    p.append('</g>')
    return "".join(p)

def bean(cx, cy, r, angle=0, color=None):
    color = color or C["brown"]
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({angle:.1f})">'
            f'<ellipse cx="0" cy="0" rx="{r:.1f}" ry="{r*0.66:.1f}" fill="{color}"/>'
            f'<path d="M{-r*0.7:.1f},{-r*0.28:.1f} C {-r*0.1:.1f},{r*0.18:.1f} {r*0.1:.1f},{-r*0.18:.1f} {r*0.7:.1f},{r*0.28:.1f}" '
            f'stroke="{C["espresso"]}" stroke-width="{max(r*0.12,1):.1f}" fill="none" opacity="0.7"/>'
            f'</g>')

def mountain(x, y, w, h, body=None, snow="#FFFFFF", opacity=1.0):
    """Silueta del Nevado del Ruiz con casquete de nieve."""
    body = body or C["coffee"]
    return (f'<g transform="translate({x:.1f},{y:.1f})" opacity="{opacity}">'
            f'<path d="M0,{h:.1f} L {w*0.30:.1f},{h*0.18:.1f} L {w*0.42:.1f},{h*0.40:.1f} '
            f'L {w*0.55:.1f},{h*0.06:.1f} L {w*0.70:.1f},{h*0.42:.1f} L {w*0.82:.1f},{h*0.24:.1f} L {w:.1f},{h:.1f} Z" fill="{body}"/>'
            f'<path d="M {w*0.30:.1f},{h*0.18:.1f} L {w*0.36:.1f},{h*0.30:.1f} L {w*0.40:.1f},{h*0.24:.1f} '
            f'L {w*0.44:.1f},{h*0.34:.1f} L {w*0.49:.1f},{h*0.22:.1f} L {w*0.55:.1f},{h*0.06:.1f} '
            f'L {w*0.62:.1f},{h*0.26:.1f} L {w*0.66:.1f},{h*0.20:.1f} L {w*0.70:.1f},{h*0.42:.1f} '
            f'L {w*0.74:.1f},{h*0.34:.1f} L {w*0.78:.1f},{h*0.40:.1f} L {w*0.82:.1f},{h*0.24:.1f} '
            f'L {w*0.30:.1f},{h*0.18:.1f} Z" fill="{snow}" opacity="0.92"/>'
            f'</g>')

def check_icon(cx, cy, r, bg=None, fg="#FFFFFF"):
    bg = bg or C["green"]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
            f'<path d="M{cx-r*0.45:.1f},{cy:.1f} L {cx-r*0.12:.1f},{cy+r*0.35:.1f} L {cx+r*0.5:.1f},{cy-r*0.4:.1f}" '
            f'stroke="{fg}" stroke-width="{r*0.22:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def plancha_badge(cx, cy, r):
    """Sello circular grande con el numero 2."""
    return (
        f'<g>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gBadge)" stroke="{C["white"]}" stroke-width="{r*0.06:.1f}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.88:.1f}" fill="none" stroke="{C["gold_lt"]}" stroke-width="{r*0.03:.1f}" opacity="0.9"/>'
        f'<text x="{cx}" y="{cy-r*0.42:.1f}" text-anchor="middle" font-family="Arial, sans-serif" '
        f'font-weight="700" font-size="{r*0.26:.1f}" fill="{C["gold_lt"]}" letter-spacing="2">PLANCHA</text>'
        f'<text x="{cx}" y="{cy+r*0.52:.1f}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" '
        f'font-weight="900" font-size="{r*1.35:.1f}" fill="{C["white"]}">2</text>'
        f'</g>'
    )

# --------------------------------------------------------------------------------------
# 4. UTILIDADES SVG
# --------------------------------------------------------------------------------------
def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">')

def image_clipped(img_key, x, y, w, h, clip_id, radius=0, shape="rect", preserve='xMidYMid slice'):
    """Coloca una foto recortada dentro de un rect redondeado o un circulo."""
    if shape == "circle":
        clip = f'<clipPath id="{clip_id}"><circle cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" r="{min(w,h)/2:.1f}"/></clipPath>'
    else:
        clip = f'<clipPath id="{clip_id}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius:.1f}" ry="{radius:.1f}"/></clipPath>'
    img = (f'<image href="{IMG[img_key]}" xlink:href="{IMG[img_key]}" x="{x:.1f}" y="{y:.1f}" '
           f'width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="{preserve}" clip-path="url(#{clip_id})"/>')
    return clip, img

def multiline(text, max_chars):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def save(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    # validar XML
    minidom.parseString(content.encode("utf-8"))
    print(f"  OK {name} ({len(content)//1024} KB)")
    return path



# --------------------------------------------------------------------------------------
# 5. DEFS COMUNES (degradados, filtros)
# --------------------------------------------------------------------------------------
def build_defs(extra=""):
    return f'''<defs>
  <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{C['cream']}"/>
    <stop offset="100%" stop-color="{C['cream2']}"/>
  </linearGradient>
  <linearGradient id="gBrownDown" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{C['espresso']}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{C['espresso']}" stop-opacity="0.92"/>
  </linearGradient>
  <linearGradient id="gBrownTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{C['espresso']}" stop-opacity="0.65"/>
    <stop offset="60%" stop-color="{C['espresso']}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{C['gold_lt']}"/>
    <stop offset="100%" stop-color="{C['gold']}"/>
  </linearGradient>
  <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{C['green']}"/>
    <stop offset="100%" stop-color="{C['green_dk']}"/>
  </linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{C['red']}"/>
    <stop offset="100%" stop-color="{C['red_dark']}"/>
  </linearGradient>
  <linearGradient id="gBrownBar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{C['brown']}"/>
    <stop offset="100%" stop-color="{C['espresso']}"/>
  </linearGradient>
  <radialGradient id="gBadge" cx="38%" cy="32%" r="78%">
    <stop offset="0%" stop-color="#D83A3F"/>
    <stop offset="62%" stop-color="{C['red']}"/>
    <stop offset="100%" stop-color="{C['red_dark']}"/>
  </radialGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="{C['espresso']}" flood-opacity="0.35"/>
  </filter>
  <filter id="softSmall" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="{C['espresso']}" flood-opacity="0.30"/>
  </filter>
  {extra}
</defs>'''

def two_lines(name):
    words = name.split()
    if len(words) <= 1:
        return [name, ""]
    mid = (len(words) + 1) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]

def nevado_medallion(cx, cy, r, clip_id, label=True):
    clip = f'<clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    out = (f'<g filter="url(#softSmall)">'
           f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{C["white"]}"/>'
           f'<image href="{IMG["nevado"]}" xlink:href="{IMG["nevado"]}" x="{cx-r:.1f}" y="{cy-r:.1f}" '
           f'width="{2*r:.1f}" height="{2*r:.1f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#gGold)" stroke-width="{r*0.10:.1f}"/>'
           f'</g>')
    if label:
        out += (f'<g transform="translate({cx},{cy+r+22})">'
                f'<rect x="-78" y="-15" width="156" height="30" rx="15" fill="{C["espresso"]}"/>'
                f'<text x="0" y="6" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" '
                f'font-size="14" letter-spacing="1.5" fill="{C["gold_lt"]}">NEVADO DEL RUIZ</text></g>')
    return clip, out

# --------------------------------------------------------------------------------------
# 6. PIEZA: AFICHE PRINCIPAL  (1000 x 1500)
# --------------------------------------------------------------------------------------
def afiche_principal():
    W, H = 1000, 1500
    # clips de fotos
    clip_hero, img_hero = image_clipped("cafetales", 0, 74, W, 500, "clipHero", 0)
    nev_clip, nev = nevado_medallion(150, 540, 72, "clipNevA")

    # tarjetas de candidatos
    cards = []
    card_defs = []
    cw, ph = 392, 452
    positions = [("principal", 70), ("suplente", 538)]
    for key, cx in positions:
        cand = CANDIDATOS[key]
        py = 792
        cid = f"clipCand_{key}"
        clip, img = image_clipped(cand["img"], cx, py, cw, ph, cid, 22)
        card_defs.append(clip)
        l1, l2 = two_lines(cand["nombre"])
        rolecolor = C["red"] if key == "principal" else C["green"]
        cards.append(f'''
    <g filter="url(#soft)">
      <rect x="{cx-6}" y="{py-6}" width="{cw+12}" height="{ph+150}" rx="26" fill="{C['white']}"/>
    </g>
    {img}
    <rect x="{cx}" y="{py}" width="{cw}" height="{ph}" rx="22" fill="none" stroke="{C['white']}" stroke-width="4"/>
    <rect x="{cx}" y="{py+ph}" width="{cw}" height="150" fill="url(#gBrownBar)"/>
    <rect x="{cx}" y="{py+ph}" width="{cw}" height="150" rx="0" fill="none"/>
    <g transform="translate({cx+cw/2},{py+ph})">
      <rect x="-92" y="-22" width="184" height="40" rx="20" fill="{rolecolor}"/>
      <text x="0" y="5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="20" letter-spacing="2" fill="#fff">{esc(cand['rol'])}</text>
    </g>
    <text x="{cx+cw/2}" y="{py+ph+72}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="26" fill="#fff">{esc(l1)}</text>
    <text x="{cx+cw/2}" y="{py+ph+108}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="26" fill="#fff">{esc(l2)}</text>
    ''')

    extra = clip_hero + nev_clip + "".join(card_defs)
    s = []
    s.append(svg_open(W, H))
    s.append(build_defs(extra))
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    # hero
    s.append(img_hero)
    s.append(f'<rect x="0" y="74" width="{W}" height="500" fill="url(#gBrownTop)"/>')
    s.append(f'<rect x="0" y="360" width="{W}" height="214" fill="url(#gBrownDown)"/>')
    # ribbon superior
    s.append(f'<rect x="0" y="0" width="{W}" height="74" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="48" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="26" letter-spacing="4" fill="#fff">{esc(ORG)}</text>')
    s.append(f'<rect x="0" y="74" width="{W}" height="7" fill="url(#gGold)"/>')
    # sprigs decorativos sobre el hero
    s.append(sprig(15, 150, scale=0.8, angle=8))
    s.append(sprig(W-15, 130, scale=0.85, angle=-6, flip=True))
    # badge plancha 2
    s.append(f'<g filter="url(#soft)">{plancha_badge(845, 200, 112)}</g>')
    # medallon nevado
    s.append(nev)
    # bloque titular
    s.append(f'<text x="{W/2}" y="636" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="3" fill="{C["green_dk"]}">POR UNOS CAFETEROS PRÓSPEROS</text>')
    s.append(f'<text x="{W/2}" y="706" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="74" fill="{C["espresso"]}">COMPROMETIDOS</text>')
    s.append(f'<text x="{W/2}" y="772" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="58" fill="{C["red"]}">CON LOS CAFETEROS</text>')
    # subrayado dorado
    s.append(f'<rect x="{W/2-180}" y="724" width="360" height="6" rx="3" fill="url(#gGold)"/>')
    # tarjetas
    s.append("".join(cards))
    # franja inferior CTA
    s.append(f'<rect x="0" y="1410" width="{W}" height="90" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="1404" width="{W}" height="6" fill="url(#gGold)"/>')
    s.append(bean(60, 1455, 22, 20, C["gold"]))
    s.append(bean(940, 1455, 22, -20, C["gold"]))
    s.append(f'<text x="{W/2}" y="1448" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="34" fill="{C["gold_lt"]}">TU VOTO, NUESTRO COMPROMISO</text>')
    s.append(f'<text x="{W/2}" y="1482" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="22" letter-spacing="3" fill="#fff">MARCA LA PLANCHA 2</text>')
    s.append('</svg>')
    return save("01-afiche-principal.svg", "".join(s))


def cand_circle(cx, cy, r, key, clip_id):
    """Retrato circular enmarcado del candidato."""
    cand = CANDIDATOS[key]
    clip = f'<clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    g = (f'<g filter="url(#softSmall)"><circle cx="{cx}" cy="{cy}" r="{r+r*0.07:.1f}" fill="{C["white"]}"/></g>'
         f'<image href="{IMG[cand["img"]]}" xlink:href="{IMG[cand["img"]]}" x="{cx-r:.1f}" y="{cy-r:.1f}" '
         f'width="{2*r:.1f}" height="{2*r:.1f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#gGold)" stroke-width="{r*0.07:.1f}"/>')
    return clip, g


# --------------------------------------------------------------------------------------
# 7. PIEZA: AFICHE DE PROPUESTAS  (1000 x 1500)
# --------------------------------------------------------------------------------------
def afiche_propuestas():
    W, H = 1000, 1500
    clip_a, ca = cand_circle(360, 250, 78, "principal", "clipPropA")
    clip_b, cb = cand_circle(560, 250, 78, "suplente", "clipPropB")
    nev_clip, nev = nevado_medallion(W-120, 230, 60, "clipNevP", label=False)

    rows = []
    accent = [C["green"], C["gold"], C["red"], C["green_dk"], C["brown"]]
    y0, rh, gap = 392, 188, 18
    for i, (titulo, desc) in enumerate(PROPUESTAS):
        y = y0 + i * (rh + gap)
        col = accent[i % len(accent)]
        dl = multiline(desc, 58)
        desc_t = "".join(
            f'<text x="190" y="{y+96+j*30}" font-family="Arial, sans-serif" font-size="22" fill="{C["brown"]}">{esc(line)}</text>'
            for j, line in enumerate(dl[:2]))
        rows.append(f'''
    <g filter="url(#softSmall)"><rect x="50" y="{y}" width="900" height="{rh}" rx="20" fill="#fff"/></g>
    <rect x="50" y="{y}" width="16" height="{rh}" rx="8" fill="{col}"/>
    {check_icon(120, y+rh/2, 42, col)}
    <text x="190" y="{y+58}" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="32" fill="{C['espresso']}">{esc(titulo)}</text>
    {desc_t}
    <text x="905" y="{y+62}" text-anchor="end" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="64" fill="{col}" opacity="0.18">{i+1}</text>
    ''')

    extra = clip_a + clip_b + nev_clip
    s = [svg_open(W, H), build_defs(extra)]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    # cabecera
    s.append(f'<rect x="0" y="0" width="{W}" height="360" fill="url(#gBrownBar)"/>')
    s.append(sprig(0, 70, scale=0.7, angle=6))
    s.append(sprig(W, 60, scale=0.72, angle=-6, flip=True))
    s.append(f'<rect x="0" y="360" width="{W}" height="8" fill="url(#gGold)"/>')
    s.append(f'<text x="{W/2}" y="80" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="22" letter-spacing="4" fill="{C["gold_lt"]}">{esc(ORG)}</text>')
    s.append(f'<text x="{W/2}" y="140" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="58" fill="#fff">NUESTRAS PROPUESTAS</text>')
    s.append(f'<text x="{W/2}" y="178" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="22" letter-spacing="3" fill="{C["gold_lt"]}">{esc(SLOGAN)}</text>')
    s.append(nev)
    s.append(ca); s.append(cb)
    s.append(plancha_badge(150, 250, 70))
    s.append(f'<text x="360" y="358" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="16" fill="{C["gold_lt"]}">PRINCIPAL</text>')
    s.append(f'<text x="560" y="358" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="16" fill="{C["gold_lt"]}">SUPLENTE</text>')
    s.append("".join(rows))
    # footer
    s.append(f'<rect x="0" y="1418" width="{W}" height="82" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="1470" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="34" fill="#fff">VOTA PLANCHA 2</text>')
    s.append('</svg>')
    return save("02-afiche-propuestas.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 8. PIEZA: REDES - POST CUADRADO  (1080 x 1080)
# --------------------------------------------------------------------------------------
def redes_post():
    W = H = 1080
    clip_hero, img_hero = image_clipped("cafetales", 0, 0, W, 470, "clipPostHero", 0)
    clip_a, ca = cand_circle(380, 560, 132, "principal", "clipPostA")
    clip_b, cb = cand_circle(700, 560, 132, "suplente", "clipPostB")
    extra = clip_hero + clip_a + clip_b
    s = [svg_open(W, H), build_defs(extra)]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    s.append(img_hero)
    s.append(f'<rect x="0" y="0" width="{W}" height="470" fill="url(#gBrownTop)"/>')
    s.append(f'<rect x="0" y="250" width="{W}" height="220" fill="url(#gBrownDown)"/>')
    s.append(f'<rect x="0" y="60" width="{W}" height="64" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="102" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="24" letter-spacing="4" fill="#fff">{esc(ORG)}</text>')
    s.append(sprig(10, 200, scale=0.7, angle=8))
    s.append(sprig(W-10, 190, scale=0.72, angle=-6, flip=True))
    s.append(f'<g filter="url(#soft)">{plancha_badge(W/2, 470, 104)}</g>')
    s.append(ca); s.append(cb)
    # nombres bajo retratos
    for cx, key in [(380, "principal"), (700, "suplente")]:
        cand = CANDIDATOS[key]; l1, l2 = two_lines(cand["nombre"])
        rc = C["red"] if key == "principal" else C["green"]
        s.append(f'<g transform="translate({cx},712)"><rect x="-78" y="-20" width="156" height="36" rx="18" fill="{rc}"/>'
                 f'<text x="0" y="6" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="18" letter-spacing="1" fill="#fff">{esc(cand["rol"])}</text></g>')
        s.append(f'<text x="{cx}" y="756" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="22" fill="{C["espresso"]}">{esc(l1)}</text>')
        s.append(f'<text x="{cx}" y="784" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="22" fill="{C["espresso"]}">{esc(l2)}</text>')
    # eslogan grande
    s.append(f'<text x="{W/2}" y="868" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="50" fill="{C["espresso"]}">COMPROMETIDOS</text>')
    s.append(f'<text x="{W/2}" y="924" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="46" fill="{C["red"]}">CON LOS CAFETEROS</text>')
    s.append(f'<rect x="{W/2-150}" y="884" width="300" height="5" rx="3" fill="url(#gGold)"/>')
    s.append(f'<rect x="0" y="1000" width="{W}" height="80" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="994" width="{W}" height="6" fill="url(#gGold)"/>')
    s.append(f'<text x="{W/2}" y="1052" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="30" fill="{C["gold_lt"]}">POR UNOS CAFETEROS PRÓSPEROS</text>')
    s.append('</svg>')
    return save("06-redes-post.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 9. PIEZA: REDES - HISTORIA  (1080 x 1920)
# --------------------------------------------------------------------------------------
def redes_historia():
    W, H = 1080, 1920
    clip_hero, img_hero = image_clipped("cafetales", 0, 0, W, 760, "clipStHero", 0)
    clip_a, ca = cand_circle(360, 980, 150, "principal", "clipStA")
    clip_b, cb = cand_circle(720, 980, 150, "suplente", "clipStB")
    nev_clip, nev = nevado_medallion(W/2, 1300, 86, "clipStNev")
    extra = clip_hero + clip_a + clip_b + nev_clip
    s = [svg_open(W, H), build_defs(extra)]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    s.append(img_hero)
    s.append(f'<rect x="0" y="0" width="{W}" height="760" fill="url(#gBrownTop)"/>')
    s.append(f'<rect x="0" y="470" width="{W}" height="290" fill="url(#gBrownDown)"/>')
    s.append(f'<rect x="0" y="120" width="{W}" height="74" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="170" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="28" letter-spacing="4" fill="#fff">{esc(ORG)}</text>')
    s.append(f'<g filter="url(#soft)">{plancha_badge(W/2, 740, 130)}</g>')
    s.append(ca); s.append(cb)
    for cx, key in [(360, "principal"), (720, "suplente")]:
        cand = CANDIDATOS[key]; l1, l2 = two_lines(cand["nombre"])
        rc = C["red"] if key == "principal" else C["green"]
        s.append(f'<g transform="translate({cx},1158)"><rect x="-86" y="-22" width="172" height="40" rx="20" fill="{rc}"/>'
                 f'<text x="0" y="6" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="20" letter-spacing="1" fill="#fff">{esc(cand["rol"])}</text></g>')
        s.append(f'<text x="{cx}" y="1206" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="24" fill="{C["espresso"]}">{esc(l1)}</text>')
        s.append(f'<text x="{cx}" y="1238" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="24" fill="{C["espresso"]}">{esc(l2)}</text>')
    s.append(nev)
    s.append(f'<text x="{W/2}" y="1480" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="62" fill="{C["espresso"]}">COMPROMETIDOS</text>')
    s.append(f'<text x="{W/2}" y="1548" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="54" fill="{C["red"]}">CON LOS CAFETEROS</text>')
    s.append(f'<rect x="{W/2-190}" y="1500" width="380" height="6" rx="3" fill="url(#gGold)"/>')
    s.append(f'<rect x="0" y="1760" width="{W}" height="160" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="1752" width="{W}" height="8" fill="url(#gGold)"/>')
    s.append(f'<text x="{W/2}" y="1832" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="44" fill="{C["gold_lt"]}">VOTA PLANCHA 2</text>')
    s.append(f'<text x="{W/2}" y="1882" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="26" letter-spacing="3" fill="#fff">TU VOTO, NUESTRO COMPROMISO</text>')
    s.append('</svg>')
    return save("07-redes-historia.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 10. PIEZA: PASACALLE  (2400 x 480, relación 5:1)
# --------------------------------------------------------------------------------------
def pasacalle():
    W, H = 2400, 480
    clip_hero, img_hero = image_clipped("cafetales", 0, 0, W, H, "clipPasa", 0)
    clip_a, ca = cand_circle(560, 235, 112, "principal", "clipPasaA")
    clip_b, cb = cand_circle(810, 235, 112, "suplente", "clipPasaB")
    extra = clip_hero + clip_a + clip_b
    s = [svg_open(W, H), build_defs(extra)]
    s.append(img_hero)
    s.append(f'<rect width="{W}" height="{H}" fill="{C["espresso"]}" opacity="0.55"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gBrownTop)"/>')
    # marco
    s.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="url(#gGold)" stroke-width="6" rx="10"/>')
    # ribbon org
    s.append(f'<rect x="0" y="0" width="{W}" height="56" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="39" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="26" letter-spacing="6" fill="#fff">{esc(ORG)}</text>')
    # badge
    s.append(f'<g filter="url(#soft)">{plancha_badge(220, 250, 150)}</g>')
    # candidatos
    s.append(ca); s.append(cb)
    for cx, key in [(560, "principal"), (810, "suplente")]:
        cand = CANDIDATOS[key]; rc = C["red"] if key == "principal" else C["green"]
        s.append(f'<g transform="translate({cx},382)"><rect x="-70" y="-19" width="140" height="34" rx="17" fill="{rc}"/>'
                 f'<text x="0" y="5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="17" fill="#fff">{esc(cand["rol"])}</text></g>')
    s.append(f'<text x="685" y="438" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="20" fill="{C["gold_lt"]}">JHON E. PRIETO  ·  NELSON F. OROZCO</text>')
    # eslogan
    s.append(f'<text x="1000" y="190" font-family="Arial, sans-serif" font-weight="800" font-size="34" letter-spacing="3" fill="{C["gold_lt"]}">POR UNOS CAFETEROS PRÓSPEROS</text>')
    s.append(f'<text x="1000" y="280" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="90" fill="#fff">COMPROMETIDOS</text>')
    s.append(f'<text x="1000" y="370" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="74" fill="{C["gold_lt"]}">CON LOS CAFETEROS</text>')
    s.append(f'<rect x="1000" y="218" width="560" height="6" rx="3" fill="url(#gGold)"/>')
    s.append(sprig(2360, 120, scale=0.8, angle=-10, flip=True))
    s.append('</svg>')
    return save("03-pasacalle.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 11. PIEZA: VALLA PUBLICITARIA  (2400 x 1200, relación 2:1)
# --------------------------------------------------------------------------------------
def valla(contacto="@PLANCHA2CAFETEROS", informes="INFORMES: 300 000 0000"):
    W, H = 2400, 1200
    clip_hero, img_hero = image_clipped("cafetales", 0, 0, W, H, "clipValla", 0)
    clip_a, ca = cand_circle(470, 560, 250, "principal", "clipVallaA")
    clip_b, cb = cand_circle(990, 560, 250, "suplente", "clipVallaB")
    nev_clip, nev = nevado_medallion(2230, 250, 92, "clipVallaNev", label=False)
    extra = clip_hero + clip_a + clip_b + nev_clip
    s = [svg_open(W, H), build_defs(extra)]
    s.append(img_hero)
    s.append(f'<rect width="{W}" height="{H}" fill="{C["espresso"]}" opacity="0.5"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#gBrownDown)" opacity="0.7"/>')
    # ribbon
    s.append(f'<rect x="0" y="0" width="{W}" height="96" fill="url(#gRed)"/>')
    s.append(f'<text x="80" y="64" font-family="Arial, sans-serif" font-weight="800" font-size="44" letter-spacing="4" fill="#fff">{esc(ORG)}</text>')
    s.append(f'<rect x="0" y="96" width="{W}" height="9" fill="url(#gGold)"/>')
    s.append(nev)
    # candidatos
    s.append(ca); s.append(cb)
    for cx, key in [(470, "principal"), (990, "suplente")]:
        cand = CANDIDATOS[key]; l1, l2 = two_lines(cand["nombre"]); rc = C["red"] if key == "principal" else C["green"]
        s.append(f'<g transform="translate({cx},858)"><rect x="-130" y="-32" width="260" height="58" rx="29" fill="{rc}"/>'
                 f'<text x="0" y="9" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="1" fill="#fff">{esc(cand["rol"])}</text></g>')
        s.append(f'<text x="{cx}" y="930" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="34" fill="#fff">{esc(l1)}</text>')
        s.append(f'<text x="{cx}" y="972" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="34" fill="#fff">{esc(l2)}</text>')
    # badge entre franja y candidatos
    s.append(f'<g filter="url(#soft)">{plancha_badge(730, 250, 150)}</g>')
    # bloque derecho: eslogan + ejes
    bx = 1320
    s.append(f'<text x="{bx}" y="320" font-family="Arial, sans-serif" font-weight="800" font-size="42" letter-spacing="2" fill="{C["gold_lt"]}">POR UNOS CAFETEROS PRÓSPEROS</text>')
    s.append(f'<text x="{bx}" y="430" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="120" fill="#fff">COMPROMETIDOS</text>')
    s.append(f'<text x="{bx}" y="540" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="96" fill="{C["gold_lt"]}">CON LOS CAFETEROS</text>')
    s.append(f'<rect x="{bx}" y="360" width="760" height="8" rx="4" fill="url(#gGold)"/>')
    ejes = ["Vías para el campo", "Renovación del café", "Beneficiaderos", "Mujer cafetera", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 640 + i * 78
        s.append(check_icon(bx + 26, ey, 30, C["gold"]))
        s.append(f'<text x="{bx+78}" y="{ey+12}" font-family="Arial, sans-serif" font-weight="700" font-size="38" fill="#fff">{esc(e)}</text>')
    # franja inferior contacto / CTA
    s.append(f'<rect x="0" y="1080" width="{W}" height="120" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="1072" width="{W}" height="8" fill="url(#gGold)"/>')
    s.append(f'<text x="80" y="1158" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="64" fill="{C["gold_lt"]}">VOTA PLANCHA 2</text>')
    s.append(f'<text x="{W-80}" y="1140" text-anchor="end" font-family="Arial, sans-serif" font-weight="700" font-size="36" fill="#fff">{esc(informes)}</text>')
    s.append(f'<text x="{W-80}" y="1182" text-anchor="end" font-family="Arial, sans-serif" font-weight="700" font-size="32" fill="{C["gold_lt"]}">{esc(contacto)}</text>')
    s.append('</svg>')
    return save("04-valla.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 12. PIEZA: TARJETA - FRENTE  (1050 x 600, 3.5x2 in @300dpi)
# --------------------------------------------------------------------------------------
def tarjeta_frente():
    W, H = 1050, 600
    clip_a, ca = cand_circle(760, 200, 92, "principal", "clipTfA")
    clip_b, cb = cand_circle(940, 200, 92, "suplente", "clipTfB")
    extra = clip_a + clip_b
    s = [svg_open(W, H), build_defs(extra)]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="14" fill="url(#gRed)"/>')
    s.append(f'<rect x="0" y="{H-14}" width="{W}" height="14" fill="url(#gGreen)"/>')
    s.append(sprig(-10, 150, scale=0.55, angle=10))
    s.append(f'<g filter="url(#soft)">{plancha_badge(170, 270, 128)}</g>')
    s.append(ca); s.append(cb)
    s.append(f'<text x="760" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="16" fill="{C["red"]}">PRINCIPAL</text>')
    s.append(f'<text x="940" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="16" fill="{C["green_dk"]}">SUPLENTE</text>')
    s.append(f'<text x="370" y="120" font-family="Arial, sans-serif" font-weight="700" font-size="18" letter-spacing="2" fill="{C["green_dk"]}">{esc(ORG)}</text>')
    s.append(f'<text x="370" y="200" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="58" fill="{C["espresso"]}">COMPROMETIDOS</text>')
    s.append(f'<text x="370" y="250" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="40" fill="{C["red"]}">CON LOS CAFETEROS</text>')
    s.append(f'<rect x="370" y="222" width="300" height="5" rx="3" fill="url(#gGold)"/>')
    s.append(f'<text x="525" y="430" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="26" fill="{C["espresso"]}">JHON ESNEIDER PRIETO PRIETO</text>')
    s.append(f'<text x="525" y="470" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="26" fill="{C["espresso"]}">NELSON FERNED OROZCO CASTAÑO</text>')
    s.append(f'<text x="525" y="540" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="24" letter-spacing="3" fill="{C["green_dk"]}">POR UNOS CAFETEROS PRÓSPEROS</text>')
    s.append('</svg>')
    return save("05a-tarjeta-frente.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 13. PIEZA: TARJETA - RESPALDO  (1050 x 600)
# --------------------------------------------------------------------------------------
def tarjeta_respaldo(telefono="300 000 0000", correo="contacto@plancha2.co", redes="@Plancha2Cafeteros"):
    W, H = 1050, 600
    s = [svg_open(W, H), build_defs("")]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="10" fill="url(#gGold)"/>')
    s.append(f'<rect x="0" y="{H-10}" width="{W}" height="10" fill="url(#gGold)"/>')
    s.append(sprig(W+10, 130, scale=0.6, angle=-10, flip=True))
    s.append(f'<text x="60" y="90" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="40" fill="{C["gold_lt"]}">NUESTRAS PROPUESTAS</text>')
    ejes = ["Vías para el campo", "Incentivos a la renovación del café", "Mejores beneficiaderos",
            "Proyectos productivos para la mujer", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 160 + i * 62
        s.append(check_icon(85, ey, 22, C["gold"]))
        s.append(f'<text x="125" y="{ey+9}" font-family="Arial, sans-serif" font-weight="700" font-size="26" fill="#fff">{esc(e)}</text>')
    s.append(f'<g filter="url(#softSmall)">{plancha_badge(880, 250, 120)}</g>')
    # contacto
    s.append(f'<rect x="60" y="500" width="930" height="2" fill="{C["gold"]}" opacity="0.5"/>')
    s.append(f'<text x="60" y="552" font-family="Arial, sans-serif" font-weight="700" font-size="24" fill="{C["gold_lt"]}">Tel: {esc(telefono)}   ·   {esc(correo)}   ·   {esc(redes)}</text>')
    s.append('</svg>')
    return save("05b-tarjeta-respaldo.svg", "".join(s))


# --------------------------------------------------------------------------------------
# 14. PIEZA: VOLANTE  (1000 x 1414, A)
# --------------------------------------------------------------------------------------
def volante():
    W, H = 1000, 1414
    clip_hero, img_hero = image_clipped("cafetales", 0, 74, W, 340, "clipVolHero", 0)
    clip_a, ca = cand_circle(360, 400, 96, "principal", "clipVolA")
    clip_b, cb = cand_circle(640, 400, 96, "suplente", "clipVolB")
    extra = clip_hero + clip_a + clip_b
    s = [svg_open(W, H), build_defs(extra)]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>')
    s.append(img_hero)
    s.append(f'<rect x="0" y="74" width="{W}" height="340" fill="url(#gBrownTop)"/>')
    s.append(f'<rect x="0" y="250" width="{W}" height="164" fill="url(#gBrownDown)"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="74" fill="url(#gRed)"/>')
    s.append(f'<text x="{W/2}" y="48" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="25" letter-spacing="4" fill="#fff">{esc(ORG)}</text>')
    s.append(f'<text x="{W/2}" y="170" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="52" fill="#fff">COMPROMETIDOS</text>')
    s.append(f'<text x="{W/2}" y="222" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="40" fill="{C["gold_lt"]}">CON LOS CAFETEROS</text>')
    s.append(f'<g filter="url(#softSmall)">{plancha_badge(845, 150, 70)}</g>')
    # candidatos
    s.append(ca); s.append(cb)
    for cx, key in [(360, "principal"), (640, "suplente")]:
        cand = CANDIDATOS[key]; l1, l2 = two_lines(cand["nombre"]); rc = C["red"] if key == "principal" else C["green"]
        s.append(f'<g transform="translate({cx},516)"><rect x="-66" y="-18" width="132" height="32" rx="16" fill="{rc}"/>'
                 f'<text x="0" y="5" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="15" fill="#fff">{esc(cand["rol"])}</text></g>')
        s.append(f'<text x="{cx}" y="560" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="19" fill="{C["espresso"]}">{esc(l1)}</text>')
        s.append(f'<text x="{cx}" y="585" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="19" fill="{C["espresso"]}">{esc(l2)}</text>')
    s.append(f'<text x="{W/2}" y="648" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="34" fill="{C["green_dk"]}">NUESTRAS PROPUESTAS</text>')
    # lista compacta
    y0, rh, gap = 686, 118, 14
    accent = [C["green"], C["gold"], C["red"], C["green_dk"], C["brown"]]
    for i, (titulo, desc) in enumerate(PROPUESTAS):
        y = y0 + i * (rh + gap)
        col = accent[i % len(accent)]
        dl = multiline(desc, 64)
        s.append(f'<g filter="url(#softSmall)"><rect x="50" y="{y}" width="900" height="{rh}" rx="16" fill="#fff"/></g>')
        s.append(f'<rect x="50" y="{y}" width="14" height="{rh}" rx="7" fill="{col}"/>')
        s.append(check_icon(112, y + rh / 2, 34, col))
        s.append(f'<text x="168" y="{y+50}" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="26" fill="{C["espresso"]}">{esc(titulo)}</text>')
        for j, line in enumerate(dl[:2]):
            s.append(f'<text x="168" y="{y+84+j*26}" font-family="Arial, sans-serif" font-size="19" fill="{C["brown"]}">{esc(line)}</text>')
    s.append(f'<rect x="0" y="1330" width="{W}" height="84" fill="url(#gBrownBar)"/>')
    s.append(f'<rect x="0" y="1324" width="{W}" height="6" fill="url(#gGold)"/>')
    s.append(f'<text x="{W/2}" y="1385" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="38" fill="{C["gold_lt"]}">VOTA PLANCHA 2</text>')
    s.append('</svg>')
    return save("08-volante.svg", "".join(s))


if __name__ == "__main__":
    print("Generando piezas...")
    afiche_principal()
    afiche_propuestas()
    pasacalle()
    valla()
    tarjeta_frente()
    tarjeta_respaldo()
    redes_post()
    redes_historia()
    volante()
    print("Listo.")
