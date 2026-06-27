# -*- coding: utf-8 -*-
"""
Generador de la campana publicitaria "PLANCHA 2 - COMPROMETIDOS CON LOS CAFETEROS"
Candidatos: Jhon Esneider Prieto Prieto (Principal) y Nelson Ferned Orozco Castano (Suplente).
Comite Departamental de Cafeteros.

Piezas en SVG vectorial de alta gama:
 - Fondo fotografico unificado con tratamiento DUOTONO cafe (armonia cromatica total).
 - Retratos con FUNDIDO suave en los bordes (las caras emergen, sin recuadros duros).
 - Foco de luz detras de cada candidato + sombra de texto para legibilidad.
 - Ajuste automatico de texto (textLength) para que ningun titulo se desborde.
"""
import base64, os, html, xml.dom.minidom as minidom

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(BASE)
OUT = BASE

# --------------------------------------------------------------------------------------
# 1. RECURSOS
# --------------------------------------------------------------------------------------
def data_uri(path, mime="image/jpeg"):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")

IMG = {
    "cafetales": data_uri(os.path.join(SRC, "CAFETALES.jpg")),
    "jhon":      data_uri(os.path.join(SRC, "Jhon Esneider Prieto Prieto.jpeg")),
    "nelson":    data_uri(os.path.join(SRC, "Nelson Ferned Orozco Castaño.jpeg")),
    "nevado":    data_uri(os.path.join(SRC, "NEVADO DEL RUIZ.jfif")),
}

# --------------------------------------------------------------------------------------
# 2. MARCA
# --------------------------------------------------------------------------------------
C = {
    "espresso": "#22130C", "brown": "#43271A", "coffee": "#6F4A2E", "caramel": "#A6703F",
    "red": "#C32026", "red_dark": "#8C161B",
    "gold": "#E3A53C", "gold_lt": "#F6D488", "gold_dk": "#B97E26",
    "green": "#2F7D34", "green_dk": "#1C5A23",
    "cream": "#FBF3E2", "cream2": "#F1E2C4", "white": "#FFFFFF",
}
SLOGAN = "COMPROMETIDOS CON LOS CAFETEROS"
ORG = "COMITÉ DEPARTAMENTAL DE CAFETEROS"
LEMA = "POR UNOS CAFETEROS PRÓSPEROS"

CAND = {
    "principal": {"nombre": "JHON ESNEIDER PRIETO PRIETO", "corto": "JHON E. PRIETO", "rol": "PRINCIPAL", "img": "jhon"},
    "suplente":  {"nombre": "NELSON FERNED OROZCO CASTAÑO", "corto": "NELSON F. OROZCO", "rol": "SUPLENTE", "img": "nelson"},
}
PROPUESTAS = [
    ("VÍAS PARA EL CAMPO", "Vías de comunicación que conecten las veredas y saquen el café a tiempo."),
    ("RENOVACIÓN DEL CAFÉ", "Mejores incentivos por la renovación de cafetales y cosechas productivas."),
    ("BENEFICIADEROS", "Mejoramiento y construcción de beneficiaderos para un café de calidad."),
    ("MUJER CAFETERA", "Proyectos productivos para las mujeres del campo y su autonomía."),
    ("DEFENSORÍA DEL CAFETERO", "Una defensoría que vele por los derechos de cada caficultor."),
]

HEAVY = "'Arial Black','Helvetica Neue',Arial,sans-serif"
BOLD = "'Helvetica Neue',Arial,sans-serif"

def esc(t):
    return html.escape(str(t), quote=True)

# --------------------------------------------------------------------------------------
# 3. TEXTO QUE NUNCA SE DESBORDA
# --------------------------------------------------------------------------------------
def T(x, y, text, size, max_w=None, anchor="start", weight="900",
      fill="#000", family=HEAVY, spacing=0.0, opacity=None, flt=None):
    factor = 0.64 if weight in ("900", "800") else 0.55
    est = len(text) * size * factor + max(0, len(text) - 1) * spacing
    extra = ""
    if max_w and est > max_w:
        extra = f' textLength="{max_w:.0f}" lengthAdjust="spacingAndGlyphs"'
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    fl = f' filter="url(#{flt})"' if flt else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{family}" '
            f'font-weight="{weight}" font-size="{size:.1f}" fill="{fill}"{sp}{op}{fl}{extra}>{esc(text)}</text>')

def two_lines(name):
    w = name.split()
    if len(w) <= 1:
        return [name, ""]
    mid = (len(w) + 1) // 2
    return [" ".join(w[:mid]), " ".join(w[mid:])]

def multiline(text, max_chars):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out

# --------------------------------------------------------------------------------------
# 4. MOTIVOS VECTORIALES
# --------------------------------------------------------------------------------------
def cherry(cx, cy, r, color=None):
    color = color or C["red"]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}"/>'
            f'<ellipse cx="{cx-r*0.3:.1f}" cy="{cy-r*0.32:.1f}" rx="{r*0.3:.1f}" ry="{r*0.22:.1f}" fill="#fff" opacity="0.45"/>')

def leaf(cx, cy, L, W, ang, color=None):
    color = color or C["green"]
    h = W / 2
    d = f'M0,0 C {L*0.28:.1f},{-h:.1f} {L*0.72:.1f},{-h:.1f} {L:.1f},0 C {L*0.72:.1f},{h:.1f} {L*0.28:.1f},{h:.1f} 0,0 Z'
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})">'
            f'<path d="{d}" fill="{color}"/>'
            f'<path d="M{L*0.05:.1f},0 L{L*0.9:.1f},0" stroke="{C["green_dk"]}" stroke-width="{max(W*0.05,1):.1f}" opacity="0.5"/></g>')

def sprig(x, y, scale=1.0, ang=0.0, flip=False):
    fl = -1 if flip else 1
    p = [f'<g transform="translate({x:.1f},{y:.1f}) scale({scale*fl:.3f},{scale:.3f}) rotate({ang:.1f})" opacity="0.96">']
    p.append(f'<path d="M0,0 C 70,-8 150,-28 250,-22" stroke="{C["brown"]}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    for lx, ly, ll, lw, la in [(55,-6,70,30,-38),(55,-6,66,28,28),(120,-20,76,33,-32),
                               (120,-20,70,30,34),(185,-26,70,30,-28),(185,-26,64,28,40)]:
        p.append(leaf(lx, ly, ll, lw, la))
    for chx, chy, chr_ in [(238,-30,15),(252,-16,16),(236,-8,14),(258,-30,13),(248,-44,12)]:
        p.append(cherry(chx, chy, chr_))
    p.append('</g>')
    return "".join(p)

def bean(cx, cy, r, ang=0, color=None):
    color = color or C["gold"]
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})">'
            f'<ellipse rx="{r:.1f}" ry="{r*0.64:.1f}" fill="{color}"/>'
            f'<path d="M{-r*0.7:.1f},{-r*0.26:.1f} C {-r*0.1:.1f},{r*0.16:.1f} {r*0.1:.1f},{-r*0.16:.1f} {r*0.7:.1f},{r*0.26:.1f}" '
            f'stroke="{C["espresso"]}" stroke-width="{max(r*0.12,1):.1f}" fill="none" opacity="0.7"/></g>')

def check(cx, cy, r, bg=None, fg="#fff"):
    bg = bg or C["green"]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{bg}"/>'
            f'<path d="M{cx-r*0.45:.1f},{cy:.1f} L{cx-r*0.1:.1f},{cy+r*0.35:.1f} L{cx+r*0.5:.1f},{cy-r*0.4:.1f}" '
            f'stroke="{fg}" stroke-width="{r*0.22:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def badge(cx, cy, r, flt="soft"):
    return (f'<g filter="url(#{flt})">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gBadge)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.9:.1f}" fill="none" stroke="{C["gold_lt"]}" stroke-width="{r*0.045:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["white"]}" stroke-width="{r*0.05:.1f}"/></g>'
            + T(cx, cy - r*0.36, "PLANCHA", r*0.27, r*1.4, "middle", "800", C["gold_lt"], BOLD, 3)
            + T(cx, cy + r*0.54, "2", r*1.45, None, "middle", "900", C["white"], HEAVY))

def nevado(cx, cy, r, mid, ring=True):
    d = (f'<image href="{IMG["nevado"]}" xlink:href="{IMG["nevado"]}" x="{cx-r:.1f}" y="{cy-r:.1f}" '
         f'width="{2*r:.1f}" height="{2*r:.1f}" preserveAspectRatio="xMidYMid slice" '
         f'clip-path="url(#{mid})" filter="url(#duo)"/>')
    out = (f'<g filter="url(#soft)"><circle cx="{cx}" cy="{cy}" r="{r+r*0.06:.1f}" fill="{C["cream"]}"/></g>' + d)
    if ring:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#gGold)" stroke-width="{r*0.08:.1f}"/>'
    return out, f'<clipPath id="{mid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'

# --------------------------------------------------------------------------------------
# 5. RETRATO CON FUNDIDO (la cara emerge del fondo)
# --------------------------------------------------------------------------------------
def candidate(cx, top, box_w, key, defs, name_size=26, role_size=20,
              dark_text=False, spotlight=True, ratio=0.852, show_name=True):
    box_h = box_w / ratio
    cy = top + box_h / 2
    x = cx - box_w / 2
    s = []
    if spotlight:
        s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{box_w*0.66:.1f}" ry="{box_h*0.6:.1f}" fill="url(#gSpot)"/>')
    mid = f"mk{key}{int(cx)}{int(top)}"
    defs.append(f'<mask id="{mid}" maskContentUnits="userSpaceOnUse">'
                f'<rect x="{x:.1f}" y="{top:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="url(#gFeather)"/></mask>')
    img = IMG[CAND[key]["img"]]
    s.append(f'<image href="{img}" xlink:href="{img}" x="{x:.1f}" y="{top:.1f}" width="{box_w:.1f}" '
             f'height="{box_h:.1f}" preserveAspectRatio="xMidYMid slice" mask="url(#{mid})"/>')
    cand = CAND[key]
    rc = C["red"] if key == "principal" else C["green"]
    py = cy + box_h * 0.46
    if not show_name:
        pw0 = role_size * len(cand["rol"]) * 0.66 + 46
        ph0 = role_size + 16
        s.append(f'<g filter="url(#soft)"><rect x="{cx-pw0/2:.1f}" y="{py:.1f}" width="{pw0:.1f}" height="{ph0:.1f}" rx="{ph0/2:.1f}" fill="{rc}"/></g>')
        s.append(T(cx, py + role_size + 2, cand["rol"], role_size, pw0 - 18, "middle", "800", "#fff", BOLD, 1.5))
        return "".join(s)
    pw = role_size * len(cand["rol"]) * 0.66 + 46
    ph = role_size + 18
    s.append(f'<g filter="url(#soft)"><rect x="{cx-pw/2:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
             f'rx="{ph/2:.1f}" fill="{rc}"/></g>')
    s.append(T(cx, py + role_size + 3, cand["rol"], role_size, pw - 18, "middle", "800", "#fff", BOLD, 1.5))
    l1, l2 = two_lines(cand["nombre"])
    col = C["espresso"] if dark_text else "#fff"
    fl = None if dark_text else "txt"
    ny = py + ph + name_size + 6
    s.append(T(cx, ny, l1, name_size, box_w * 1.25, "middle", "900", col, HEAVY, 0, None, fl))
    s.append(T(cx, ny + name_size + 4, l2, name_size, box_w * 1.25, "middle", "900", col, HEAVY, 0, None, fl))
    return "".join(s)

# --------------------------------------------------------------------------------------
# 6. DEFS COMUNES
# --------------------------------------------------------------------------------------
def defs(extra=""):
    return f'''<defs>
  <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['cream']}"/><stop offset="1" stop-color="{C['cream2']}"/></linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{C['gold_lt']}"/><stop offset="1" stop-color="{C['gold']}"/></linearGradient>
  <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['green']}"/><stop offset="1" stop-color="{C['green_dk']}"/></linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{C['red']}"/><stop offset="1" stop-color="{C['red_dark']}"/></linearGradient>
  <linearGradient id="gBrown" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['brown']}"/><stop offset="1" stop-color="{C['espresso']}"/></linearGradient>
  <radialGradient id="gBadge" cx="38%" cy="32%" r="80%">
    <stop offset="0" stop-color="#DA3A40"/><stop offset="60%" stop-color="{C['red']}"/>
    <stop offset="100%" stop-color="{C['red_dark']}"/></radialGradient>
  <radialGradient id="gSpot" cx="50%" cy="46%" r="62%">
    <stop offset="0" stop-color="{C['espresso']}" stop-opacity="0.86"/>
    <stop offset="55%" stop-color="{C['espresso']}" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{C['espresso']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="gFeather" cx="50%" cy="44%" r="60%">
    <stop offset="0" stop-color="#fff"/><stop offset="60%" stop-color="#fff"/>
    <stop offset="100%" stop-color="#000"/></radialGradient>
  <linearGradient id="gVeil" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['espresso']}" stop-opacity="0.62"/>
    <stop offset="32%" stop-color="{C['espresso']}" stop-opacity="0.18"/>
    <stop offset="62%" stop-color="{C['espresso']}" stop-opacity="0.30"/>
    <stop offset="100%" stop-color="{C['espresso']}" stop-opacity="0.9"/></linearGradient>
  <filter id="duo" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values=".21 .72 .07 0 0 .21 .72 .07 0 0 .21 .72 .07 0 0 0 0 0 1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.13 0.62 0.97"/>
      <feFuncG type="table" tableValues="0.08 0.40 0.85"/>
      <feFuncB type="table" tableValues="0.05 0.19 0.56"/></feComponentTransfer>
  </filter>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="{C['espresso']}" flood-opacity="0.4"/></filter>
  <filter id="txt" x="-25%" y="-25%" width="150%" height="150%">
    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#160c07" flood-opacity="0.75"/></filter>
  {extra}
</defs>'''

def bg_duo(W, H, veil=True):
    """Fondo fotografico de cafetales con duotono cafe + velo para legibilidad."""
    s = [f'<rect width="{W}" height="{H}" fill="{C["espresso"]}"/>',
         f'<image href="{IMG["cafetales"]}" xlink:href="{IMG["cafetales"]}" x="0" y="0" width="{W}" '
         f'height="{H}" preserveAspectRatio="xMidYMid slice" filter="url(#duo)"/>']
    if veil:
        s.append(f'<rect width="{W}" height="{H}" fill="url(#gVeil)"/>')
    return "".join(s)

def head(W, h=70):
    return (f'<rect x="0" y="0" width="{W}" height="{h}" fill="{C["espresso"]}" opacity="0.55"/>'
            + T(W/2, h*0.64, ORG, h*0.34, W*0.9, "middle", "800", C["gold_lt"], BOLD, 4)
            + f'<rect x="0" y="{h}" width="{W}" height="{max(h*0.08,5):.0f}" fill="url(#gGold)"/>')

def cta(W, y, hgt, line1, line2=None):
    s = [f'<rect x="0" y="{y-6}" width="{W}" height="6" fill="url(#gGold)"/>',
         f'<rect x="0" y="{y}" width="{W}" height="{hgt}" fill="url(#gBrown)"/>']
    if line2:
        s.append(T(W/2, y + hgt*0.46, line1, hgt*0.34, W*0.92, "middle", "900", C["gold_lt"], HEAVY))
        s.append(T(W/2, y + hgt*0.82, line2, hgt*0.22, W*0.8, "middle", "700", "#fff", BOLD, 3))
    else:
        s.append(T(W/2, y + hgt*0.66, line1, hgt*0.44, W*0.92, "middle", "900", C["gold_lt"], HEAVY))
    return "".join(s)

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    minidom.parseString(content.encode("utf-8"))
    print(f"  OK {name} ({len(content)//1024} KB)")

def svg(W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')



# ======================================================================================
# PIEZAS
# ======================================================================================
def afiche_principal():
    W, H = 1000, 1500
    d = []
    s = [svg(W, H)]
    body = [bg_duo(W, H), head(W, 70)]
    body.append(badge(835, 208, 108))
    body.append(T(W/2, 304, LEMA, 31, 840, "middle", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(W/2, 398, "COMPROMETIDOS", 94, 900, "middle", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="{W/2-190}" y="418" width="380" height="6" rx="3" fill="url(#gGold)"/>')
    body.append(T(W/2, 478, "CON LOS CAFETEROS", 66, 900, "middle", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    body.append(candidate(262, 566, 402, "principal", d, 27, 21))
    body.append(candidate(738, 566, 402, "suplente", d, 27, 21))
    body.append(sprig(60, 1238, 0.62, 6))
    body.append(sprig(940, 1230, 0.64, -6, True))
    body.append(T(W/2, 1250, "JUNTOS POR EL CAFÉ DE NUESTRA REGIÓN", 28, 620, "middle", "800", C["gold_lt"], BOLD, 1, None, "txt"))
    body.append(cta(W, 1362, 138, "TU VOTO, NUESTRO COMPROMISO", "MARCA LA PLANCHA 2"))
    body.append(bean(70, 1455, 22, 18)); body.append(bean(930, 1455, 22, -18))
    s.append(defs("".join(d))); s += body; s.append("</svg>")
    save("01-afiche-principal.svg", "".join(s))


def afiche_propuestas():
    W, H = 1000, 1500
    d = ['<clipPath id="cpHead"><rect x="0" y="0" width="1000" height="372"/></clipPath>']
    s = [svg(W, H)]
    body = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    # cabecera fotografica
    body.append(f'<g clip-path="url(#cpHead)">{bg_duo(W, 372)}</g>')
    body.append(head(W, 64))
    body.append(T(W/2, 158, "NUESTRAS PROPUESTAS", 54, 880, "middle", "900", C["cream"], HEAVY, 1, None, "txt"))
    body.append(T(W/2, 200, SLOGAN, 23, 700, "middle", "700", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(badge(150, 290, 66))
    body.append(candidate(770, 232, 120, "principal", d, role_size=16, show_name=False))
    body.append(candidate(905, 232, 120, "suplente", d, role_size=16, show_name=False))
    body.append(f'<rect x="0" y="372" width="{W}" height="6" fill="url(#gGold)"/>')
    accent = [C["green"], C["gold_dk"], C["red"], C["green_dk"], C["coffee"]]
    y0, rh, gap = 398, 192, 14
    for i, (t, desc) in enumerate(PROPUESTAS):
        y = y0 + i * (rh + gap)
        col = accent[i]
        body.append(f'<g filter="url(#soft)"><rect x="48" y="{y}" width="904" height="{rh}" rx="20" fill="#fff"/></g>')
        body.append(f'<rect x="48" y="{y}" width="16" height="{rh}" rx="8" fill="{col}"/>')
        body.append(T(925, y + 70, str(i+1), 86, None, "end", "900", col, HEAVY, 0, 0.16))
        body.append(check(122, y + rh/2, 44, col))
        body.append(T(196, y + 64, t, 33, 660, "start", "900", C["espresso"], HEAVY))
        for j, ln in enumerate(multiline(desc, 56)[:2]):
            body.append(T(196, y + 104 + j*30, ln, 22, 700, "start", "700", C["brown"], BOLD))
    body.append(cta(W, 1418, 82, "VOTA PLANCHA 2"))
    s.append(defs("".join(d))); s += body; s.append("</svg>")
    save("02-afiche-propuestas.svg", "".join(s))


def pasacalle():
    W, H = 2400, 480
    d = []
    body = [bg_duo(W, H)]
    body.append(f'<rect x="0" y="0" width="{W}" height="50" fill="{C["espresso"]}" opacity="0.5"/>')
    body.append(T(W/2, 35, ORG, 24, W*0.8, "middle", "800", C["gold_lt"], BOLD, 6))
    body.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="12" fill="none" stroke="url(#gGold)" stroke-width="5"/>')
    body.append(badge(205, 268, 140))
    body.append(candidate(430, 80, 150, "principal", d, name_size=17, role_size=15))
    body.append(candidate(640, 80, 150, "suplente", d, name_size=17, role_size=15))
    bx = 880
    body.append(T(bx, 158, LEMA, 32, 1440, "start", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(bx, 262, "COMPROMETIDOS", 90, 1480, "start", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="{bx}" y="284" width="560" height="6" rx="3" fill="url(#gGold)"/>')
    body.append(T(bx, 350, "CON LOS CAFETEROS", 70, 1480, "start", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="0" y="440" width="{W}" height="40" fill="url(#gGold)"/>')
    body.append(T(W/2, 468, "PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS", 24, W*0.85, "middle", "900", C["espresso"], HEAVY, 2))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("03-pasacalle.svg", "".join(s))


def valla():
    W, H = 2400, 1200
    d = []
    body = [bg_duo(W, H), head(W, 92)]
    body.append(candidate(470, 280, 470, "principal", d, name_size=36, role_size=28))
    body.append(candidate(990, 280, 470, "suplente", d, name_size=36, role_size=28))
    body.append(badge(2180, 252, 150))
    bx = 1300
    body.append(T(bx, 300, LEMA, 42, 1040, "start", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(bx, 420, "COMPROMETIDOS", 104, 1050, "start", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="{bx}" y="444" width="640" height="7" rx="3" fill="url(#gGold)"/>')
    body.append(T(bx, 520, "CON LOS CAFETEROS", 80, 1050, "start", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    ejes = ["Vías para el campo", "Renovación del café", "Beneficiaderos",
            "Proyectos para la mujer cafetera", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 642 + i * 80
        body.append(check(bx + 28, ey, 30, C["gold"]))
        body.append(T(bx + 80, ey + 12, e, 38, 1000, "start", "700", "#fff", BOLD, 0, None, "txt"))
    body.append(f'<rect x="0" y="1080" width="{W}" height="120" fill="url(#gGold)"/>')
    body.append(T(W/2, 1158, "VOTA PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS", 46, W*0.92, "middle", "900", C["espresso"], HEAVY, 1))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("04-valla.svg", "".join(s))


def tarjeta_frente():
    W, H = 1050, 600
    d = []
    body = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    body.append(f'<rect x="0" y="0" width="{W}" height="12" fill="url(#gRed)"/>')
    body.append(f'<rect x="0" y="{H-12}" width="{W}" height="12" fill="url(#gGreen)"/>')
    body.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="16" fill="none" stroke="{C["gold"]}" stroke-width="2"/>')
    body.append(sprig(-8, 150, 0.5, 10))
    body.append(badge(165, 250, 112))
    body.append(T(60, 396, "COMPROMETIDOS", 42, 560, "start", "900", C["espresso"], HEAVY))
    body.append(f'<rect x="62" y="412" width="250" height="5" rx="2" fill="url(#gGold)"/>')
    body.append(T(60, 446, "CON LOS CAFETEROS", 30, 560, "start", "900", C["red"], HEAVY))
    body.append(T(60, 492, ORG, 16, 520, "start", "700", C["green_dk"], BOLD, 1))
    body.append(T(60, 520, LEMA, 18, 520, "start", "700", C["brown"], BOLD, 1))
    body.append(candidate(700, 70, 170, "principal", d, name_size=18, role_size=15, dark_text=True, spotlight=False))
    body.append(candidate(905, 70, 170, "suplente", d, name_size=18, role_size=15, dark_text=True, spotlight=False))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("05a-tarjeta-frente.svg", "".join(s))


def tarjeta_respaldo():
    W, H = 1050, 600
    body = [f'<rect width="{W}" height="{H}" fill="url(#gBrown)"/>']
    body.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="16" fill="none" stroke="{C["gold"]}" stroke-width="2"/>')
    body.append(sprig(W+8, 130, 0.5, -10, True))
    body.append(T(60, 96, "NUESTRAS PROPUESTAS", 40, 720, "start", "900", C["gold_lt"], HEAVY, 1))
    ejes = ["Vías para el campo cafetero", "Incentivos a la renovación del café",
            "Mejores beneficiaderos", "Proyectos productivos para la mujer", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 168 + i * 62
        body.append(check(86, ey, 22, C["gold"]))
        body.append(T(126, ey + 9, e, 26, 640, "start", "700", "#fff", BOLD))
    body.append(badge(885, 250, 115))
    body.append(f'<rect x="0" y="540" width="{W}" height="60" fill="url(#gGold)" opacity="0.95"/>')
    body.append(T(W/2, 580, "PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS", 24, W*0.9, "middle", "900", C["espresso"], HEAVY, 1))
    s = [svg(W, H), defs("")] + body + ["</svg>"]
    save("05b-tarjeta-respaldo.svg", "".join(s))


def redes_post():
    W = H = 1080
    d = []
    body = [bg_duo(W, H), head(W, 64)]
    body.append(T(W/2, 158, LEMA, 28, 900, "middle", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(W/2, 246, "COMPROMETIDOS", 72, 1000, "middle", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="{W/2-160}" y="266" width="320" height="6" rx="3" fill="url(#gGold)"/>')
    body.append(T(W/2, 312, "CON LOS CAFETEROS", 54, 1000, "middle", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    body.append(badge(540, 430, 96))
    body.append(candidate(322, 540, 320, "principal", d, name_size=24, role_size=18))
    body.append(candidate(758, 540, 320, "suplente", d, name_size=24, role_size=18))
    body.append(cta(W, 1000, 80, "VOTA PLANCHA 2"))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("06-redes-post.svg", "".join(s))


def redes_historia():
    W, H = 1080, 1920
    d = []
    body = [bg_duo(W, H), head(W, 74)]
    body.append(T(W/2, 234, LEMA, 30, 940, "middle", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(W/2, 330, "COMPROMETIDOS", 78, 1000, "middle", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="{W/2-180}" y="352" width="360" height="6" rx="3" fill="url(#gGold)"/>')
    body.append(T(W/2, 404, "CON LOS CAFETEROS", 60, 1000, "middle", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    body.append(badge(540, 560, 124))
    body.append(candidate(360, 720, 360, "principal", d, name_size=27, role_size=21))
    body.append(candidate(720, 720, 360, "suplente", d, name_size=27, role_size=21))
    ejes = ["Vías para el campo", "Renovación del café", "Beneficiaderos",
            "Mujer cafetera", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 1320 + i * 80
        body.append(check(210, ey, 26, C["gold"]))
        body.append(T(258, ey + 10, e, 34, 700, "start", "700", "#fff", BOLD, 0, None, "txt"))
    body.append(cta(W, 1740, 180, "VOTA PLANCHA 2", "TU VOTO, NUESTRO COMPROMISO"))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("07-redes-historia.svg", "".join(s))


def volante():
    W, H = 1000, 1414
    d = ['<clipPath id="cpVol"><rect x="0" y="0" width="1000" height="372"/></clipPath>']
    body = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    body.append(f'<g clip-path="url(#cpVol)">{bg_duo(W, 372)}</g>')
    body.append(head(W, 62))
    body.append(T(W/2, 150, LEMA, 26, 880, "middle", "800", C["gold_lt"], BOLD, 2, None, "txt"))
    body.append(T(W/2, 232, "COMPROMETIDOS", 60, 900, "middle", "900", C["cream"], HEAVY, 0, None, "txt"))
    body.append(T(W/2, 286, "CON LOS CAFETEROS", 44, 900, "middle", "900", C["gold_lt"], HEAVY, 0, None, "txt"))
    body.append(f'<rect x="0" y="372" width="{W}" height="6" fill="url(#gGold)"/>')
    body.append(candidate(310, 250, 180, "principal", d, name_size=20, role_size=16, dark_text=True))
    body.append(candidate(690, 250, 180, "suplente", d, name_size=20, role_size=16, dark_text=True))
    body.append(T(W/2, 612, "NUESTRAS PROPUESTAS", 34, 700, "middle", "900", C["espresso"], HEAVY, 1))
    accent = [C["green"], C["gold_dk"], C["red"], C["green_dk"], C["coffee"]]
    y0, rh, gap = 642, 124, 12
    for i, (t, desc) in enumerate(PROPUESTAS):
        y = y0 + i * (rh + gap)
        col = accent[i]
        body.append(f'<g filter="url(#soft)"><rect x="48" y="{y}" width="904" height="{rh}" rx="16" fill="#fff"/></g>')
        body.append(f'<rect x="48" y="{y}" width="14" height="{rh}" rx="7" fill="{col}"/>')
        body.append(check(112, y + rh/2, 34, col))
        body.append(T(168, y + 50, t, 27, 720, "start", "900", C["espresso"], HEAVY))
        for j, ln in enumerate(multiline(desc, 62)[:2]):
            body.append(T(168, y + 86 + j*26, ln, 19, 740, "start", "700", C["brown"], BOLD))
    body.append(cta(W, 1330, 84, "VOTA PLANCHA 2"))
    s = [svg(W, H), defs("".join(d))] + body + ["</svg>"]
    save("08-volante.svg", "".join(s))


def build_exporter():
    """Crea exportar-png.html autonomo: incrusta las piezas y las descarga en PNG (cliente)."""
    import re
    piezas = [
        ("01-afiche-principal", "Afiche principal"),
        ("02-afiche-propuestas", "Afiche de propuestas"),
        ("03-pasacalle", "Pasacalle"),
        ("04-valla", "Valla publicitaria"),
        ("05a-tarjeta-frente", "Tarjeta — frente"),
        ("05b-tarjeta-respaldo", "Tarjeta — respaldo"),
        ("06-redes-post", "Post de redes"),
        ("07-redes-historia", "Historia de redes"),
        ("08-volante", "Volante"),
    ]
    items = []
    for fn, title in piezas:
        svg_txt = open(os.path.join(OUT, fn + ".svg"), "r", encoding="utf-8").read()
        m = re.search(r'width="(\d+)"\s+height="(\d+)"', svg_txt)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (1000, 1000)
        b64 = base64.b64encode(svg_txt.encode("utf-8")).decode("ascii")
        items.append({"n": fn, "t": title, "w": w, "h": h, "b": b64})
    import json
    data = json.dumps(items)
    html_doc = '''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Exportar campaña a PNG · Plancha 2</title>
<style>
:root{--esp:#22130C;--brown:#43271A;--gold:#E3A53C;--goldl:#F6D488;--red:#C32026;--green:#2F7D34;--cream:#FBF3E2}
*{box-sizing:border-box;margin:0;padding:0;font-family:Arial,Helvetica,sans-serif}
body{background:var(--cream);color:var(--esp)}
header{background:linear-gradient(135deg,var(--brown),var(--esp));color:#fff;padding:30px 20px;text-align:center;border-bottom:7px solid var(--gold)}
header h1{font-size:clamp(22px,4vw,34px)}header p{color:var(--goldl);margin-top:6px}
.bar{position:sticky;top:0;z-index:5;background:#fff;box-shadow:0 3px 12px rgba(0,0,0,.12);padding:14px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;justify-content:center}
.bar label{font-weight:700}
select,button{font-size:15px;padding:10px 16px;border-radius:10px;border:2px solid var(--gold);background:#fff;font-weight:700;cursor:pointer}
button.primary{background:var(--green);color:#fff;border-color:var(--green)}
button.all{background:var(--red);color:#fff;border-color:var(--red)}
.wrap{max-width:1150px;margin:0 auto;padding:26px 18px 70px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 7px 22px rgba(0,0,0,.12);display:flex;flex-direction:column}
.thumb{background:repeating-conic-gradient(#eee 0 25%,#f8f8f8 0 50%) 50%/20px 20px;padding:12px;display:flex;align-items:center;justify-content:center;min-height:170px}
.thumb img{max-width:100%;max-height:240px;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.2)}
.meta{padding:14px 16px}.meta h3{color:var(--brown);font-size:17px}.meta .d{font-size:12px;color:#8a7b66;margin:3px 0 10px}
.note{background:#fff;border-left:6px solid var(--gold);padding:16px 20px;border-radius:10px;margin:20px 0;line-height:1.55;font-size:14px}
.status{text-align:center;padding:10px;font-weight:700;color:var(--green)}
</style></head><body>
<header><h1>Descargar la campaña en PNG</h1><p>Plancha 2 · Comprometidos con los Cafeteros</p></header>
<div class="bar">
  <label>Resolución:</label>
  <select id="scale"><option value="1">1x (rápido)</option><option value="2" selected>2x (recomendado imprenta)</option><option value="3">3x (máxima)</option></select>
  <button class="all" onclick="todas()">⬇ Descargar TODAS en PNG</button>
  <span id="status" class="status"></span>
</div>
<div class="wrap">
  <div class="note"><b>Cómo usar:</b> elige la resolución y pulsa <b>Descargar TODAS</b>, o el botón PNG de cada pieza.
  Los archivos se guardan en tu carpeta de Descargas. Para imprenta de gran formato (vallas, pasacalles) lo ideal
  es entregar el <b>.svg</b> directamente, ya que es vectorial y no pierde calidad a ningún tamaño.</div>
  <div class="grid" id="grid"></div>
</div>
<script>
const PIEZAS=__DATA__;
function durl(p){return 'data:image/svg+xml;base64,'+p.b;}
function load(p){return new Promise((ok,err)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>err(new Error('no carga '+p.n));i.src=durl(p);});}
async function toPng(p,scale){const img=await load(p);const cv=document.createElement('canvas');cv.width=Math.round(p.w*scale);cv.height=Math.round(p.h*scale);const ctx=cv.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,cv.width,cv.height);ctx.imageSmoothingQuality='high';ctx.drawImage(img,0,0,cv.width,cv.height);return await new Promise((res,rej)=>cv.toBlob(b=>b?res(b):rej(new Error('toBlob')),'image/png'));}
function dl(blob,name){const a=document.createElement('a');a.href=URL.createObjectURL(a._b=blob);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),5000);}
async function una(i){const p=PIEZAS[i];const s=+document.getElementById('scale').value;try{const b=await toPng(p,s);dl(b,p.n+'.png');}catch(e){alert('No se pudo exportar '+p.n+': '+e.message+'\\nAbre el .svg directamente y guárdalo como imagen.');}}
async function todas(){const s=+document.getElementById('scale').value;const st=document.getElementById('status');for(let i=0;i<PIEZAS.length;i++){st.textContent='Generando '+(i+1)+'/'+PIEZAS.length+'…';try{const b=await toPng(PIEZAS[i],s);dl(b,PIEZAS[i].n+'.png');}catch(e){console.error(e);}await new Promise(r=>setTimeout(r,600));}st.textContent='¡Listo! Revisa tu carpeta de Descargas.';}
const g=document.getElementById('grid');
PIEZAS.forEach((p,i)=>{g.insertAdjacentHTML('beforeend',`<div class="card"><div class="thumb"><img src="${durl(p)}" alt="${p.t}"></div><div class="meta"><h3>${p.t}</h3><div class="d">${p.w}×${p.h}px (vector)</div><button class="primary" onclick="una(${i})">⬇ Descargar PNG</button></div></div>`);});
</script></body></html>'''
    html_doc = html_doc.replace("__DATA__", data)
    with open(os.path.join(OUT, "exportar-png.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"  OK exportar-png.html ({len(html_doc)//1024} KB)")


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
    build_exporter()
    print("Listo.")
