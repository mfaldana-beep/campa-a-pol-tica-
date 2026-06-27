# -*- coding: utf-8 -*-
"""
SISTEMA VISUAL "EL SELLO DEL CAFETERO"
Campana PLANCHA 2 - Comprometidos con los Cafeteros.
Jhon Esneider Prieto Prieto (Principal) · Nelson Ferned Orozco Castano (Suplente).

Estetica editorial / cafe de especialidad: emblema-sello, retratos en arco,
lineas topograficas (cordillera/Nevado), iconos de linea, marca de tarjeton
electoral, paleta calida y sofisticada. SVG vectorial (export a PNG incluido).
"""
import base64, os, html, math, xml.dom.minidom as minidom

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(BASE)
OUT = BASE
ASSETS = os.path.join(BASE, "assets")

def uri(p):
    with open(p, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")

def optd(p, fb):
    return uri(p) if os.path.exists(p) else fb

_caf = uri(os.path.join(SRC, "CAFETALES.jpg"))
IMG = {
    "cafetales": _caf,
    "jhon":   uri(os.path.join(SRC, "Jhon Esneider Prieto Prieto.jpeg")),
    "nelson": uri(os.path.join(SRC, "Nelson Ferned Orozco Castaño.jpeg")),
    "nevado": uri(os.path.join(SRC, "NEVADO DEL RUIZ.jfif")),
    "cafeteros": optd(os.path.join(ASSETS, "cafeteros.jpg"), _caf),
}

# Paleta calida editorial
INK = "#20140D"; ESP = "#33200F"; CREAM = "#F7EFDE"; SAND = "#EBDBBC"
CLAY = "#B5532E"; CLAYD = "#8C3F20"; GREEN = "#3C5A38"; GREEND = "#2A4128"
GOLD = "#C9962E"; GOLDL = "#E7C56B"; WHITE = "#FFFFFF"

DISP = "'Arial Black','Helvetica Neue',Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
SANS = "'Helvetica Neue',Arial,sans-serif"

ORG = "COMITÉ DEPARTAMENTAL DE CAFETEROS"
SLOGAN = "COMPROMETIDOS CON LOS CAFETEROS"
LEMA = "Por unos cafeteros prósperos"
CAND = {
    "principal": {"nombre": "JHON ESNEIDER PRIETO PRIETO", "corto": "JHON E. PRIETO", "rol": "CANDIDATO PRINCIPAL", "img": "jhon"},
    "suplente":  {"nombre": "NELSON FERNED OROZCO CASTAÑO", "corto": "NELSON F. OROZCO", "rol": "SUPLENTE", "img": "nelson"},
}
PROPUESTAS = [
    ("via", "VÍAS PARA EL CAMPO", "Vías de comunicación que conecten las veredas y saquen el café a tiempo."),
    ("cafe", "RENOVACIÓN DEL CAFÉ", "Incentivos reales por la renovación de cafetales y cosechas más productivas."),
    ("benef", "BENEFICIADEROS", "Mejoramiento y construcción de beneficiaderos para un café de calidad."),
    ("mujer", "MUJER CAFETERA", "Proyectos productivos para las mujeres del campo y su autonomía."),
    ("escudo", "DEFENSORÍA DEL CAFETERO", "Una defensoría que vele por los derechos de cada caficultor."),
]

def esc(t):
    return html.escape(str(t), quote=True)

# ------------------------------------------------------------------ texto seguro
def T(x, y, text, size, max_w=None, anchor="start", weight="900",
      fill=INK, family=DISP, spacing=0.0, style="", opacity=None):
    factor = 0.64 if weight in ("900", "800", "bold") else (0.5 if "serif" in family else 0.55)
    est = len(text) * size * factor + max(0, len(text) - 1) * spacing
    extra = f' textLength="{max_w:.0f}" lengthAdjust="spacingAndGlyphs"' if (max_w and est > max_w) else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    st = f' font-style="{style}"' if style else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{family}" '
            f'font-weight="{weight}" font-size="{size:.1f}" fill="{fill}"{sp}{st}{op}{extra}>{esc(text)}</text>')

def stack(cx, top, lines, anchor="middle"):
    out, y, bl = [], top, []
    for i, ln in enumerate(lines):
        s = ln["size"]
        y += (0 if i == 0 else ln.get("gap", 16)) + s
        bl.append(y)
        out.append(T(cx, y, ln["text"], s, ln.get("max_w"), anchor, ln.get("weight", "900"),
                     ln.get("fill", INK), ln.get("family", DISP), ln.get("spacing", 0), ln.get("style", "")))
        y += s * 0.22
    return "".join(out), y, bl

def two_lines(name):
    w = name.split()
    if len(w) <= 1:
        return [name, ""]
    m = (len(w) + 1) // 2
    return [" ".join(w[:m]), " ".join(w[m:])]

def multiline(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out

# ------------------------------------------------------------------ motivos
def eyebrow(cx, y, text, size=20, color=CLAY, rule=160, w=600):
    """Etiqueta serif con reglas doradas a los lados (editorial)."""
    t = T(cx, y, text, size, w, "middle", "700", color, SERIF, 4, "italic")
    half = (len(text) * size * 0.5) / 2 + 26
    r1 = f'<line x1="{cx-half-rule:.0f}" y1="{y-size*0.32:.0f}" x2="{cx-half:.0f}" y2="{y-size*0.32:.0f}" stroke="{GOLD}" stroke-width="2"/>'
    r2 = f'<line x1="{cx+half:.0f}" y1="{y-size*0.32:.0f}" x2="{cx+half+rule:.0f}" y2="{y-size*0.32:.0f}" stroke="{GOLD}" stroke-width="2"/>'
    return r1 + r2 + t

def bean(cx, cy, r, ang=0, color=GOLD):
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})"><ellipse rx="{r:.1f}" ry="{r*0.64:.1f}" fill="{color}"/>'
            f'<path d="M{-r*0.7:.1f},{-r*0.26:.1f} C {-r*0.1:.1f},{r*0.16:.1f} {r*0.1:.1f},{-r*0.16:.1f} {r*0.7:.1f},{r*0.26:.1f}" '
            f'stroke="{ESP}" stroke-width="{max(r*0.12,1):.1f}" fill="none" opacity="0.7"/></g>')

def ring_stain(cx, cy, r, color=CLAY, op=0.10, sw=None):
    sw = sw or r * 0.16
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw:.1f}" opacity="{op}"/>'

def contours(cx, cy, r0, n=7, step=26, color=ESP, op=0.10):
    """Anillos topograficos concentricos (terroir / curvas de nivel)."""
    s = [f'<g opacity="{op}">']
    for i in range(n):
        rr = r0 + i * step
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rr:.0f}" ry="{rr*0.86:.0f}" fill="none" stroke="{color}" stroke-width="2"/>')
    s.append('</g>')
    return "".join(s)

def ridge(x, y, w, amp=34, color=GREEN, op=0.18):
    """Silueta de cordillera (lineas de horizonte)."""
    pts = [(0, 0.55), (0.12, 0.2), (0.22, 0.5), (0.34, 0.05), (0.46, 0.42),
           (0.58, 0.12), (0.7, 0.5), (0.82, 0.18), (0.92, 0.46), (1, 0.3)]
    s = [f'<g opacity="{op}">']
    for k in range(3):
        off = k * amp * 0.7
        d = "M " + " L ".join(f"{x+px*w:.0f},{y+off+py*amp:.0f}" for px, py in pts)
        s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4"/>')
    s.append('</g>')
    return "".join(s)

def ballot(cx, cy, s, color=CLAY):
    """Marca de tarjeton electoral: casilla con X (VOTA 2)."""
    return (f'<rect x="{cx-s/2:.0f}" y="{cy-s/2:.0f}" width="{s:.0f}" height="{s:.0f}" rx="{s*0.14:.0f}" '
            f'fill="none" stroke="{color}" stroke-width="{s*0.1:.1f}"/>'
            f'<path d="M{cx-s*0.22:.0f},{cy-s*0.18:.0f} L{cx+s*0.26:.0f},{cy+s*0.26:.0f} M{cx+s*0.26:.0f},{cy-s*0.22:.0f} L{cx-s*0.24:.0f},{cy+s*0.28:.0f}" '
            f'stroke="{color}" stroke-width="{s*0.13:.1f}" stroke-linecap="round"/>')

# ------------------------------------------------------------------ iconos de linea
def _ic(cx, cy, s, color, paths, sw=None):
    sw = sw or s * 0.09
    return (f'<g transform="translate({cx},{cy})" fill="none" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</g>')

def icon(name, cx, cy, s, color=ESP):
    h = s / 2
    if name == "via":
        p = (f'<path d="M{-h*0.5},{h} C {-h*0.2},{h*0.2} {h*0.2},{-h*0.2} {h*0.5},{-h}"/>'
             f'<line x1="{-h*0.05}" y1="{-h*0.55}" x2="{h*0.18}" y2="{-h*0.45}" stroke-dasharray="2 6"/>')
    elif name == "cafe":
        p = (f'<path d="M0,{h} L0,{-h*0.1}"/>'
             f'<path d="M0,{-h*0.1} C {-h*0.7},{-h*0.2} {-h*0.75},{-h*0.8} {-h*0.05},{-h*0.85}"/>'
             f'<path d="M0,{-h*0.1} C {h*0.7},{-h*0.2} {h*0.75},{-h*0.8} {h*0.05},{-h*0.85}"/>'
             f'<circle cx="0" cy="{h*0.55}" r="{h*0.16}"/>')
    elif name == "benef":
        p = (f'<path d="M{-h*0.8},{-h*0.05} L0,{-h*0.75} L{h*0.8},{-h*0.05}"/>'
             f'<rect x="{-h*0.6}" y="{-h*0.05}" width="{h*1.2}" height="{h*0.8}"/>'
             f'<line x1="0" y1="{-h*0.05}" x2="0" y2="{h*0.75}"/>')
    elif name == "mujer":
        p = (f'<circle cx="0" cy="{-h*0.55}" r="{h*0.22}"/>'
             f'<path d="M0,{-h*0.33} L{-h*0.45},{h*0.8} L{h*0.45},{h*0.8} Z"/>')
    else:  # escudo
        p = (f'<path d="M0,{-h*0.85} L{h*0.7},{-h*0.5} C {h*0.7},{h*0.3} {h*0.3},{h*0.75} 0,{h*0.9} '
             f'C {-h*0.3},{h*0.75} {-h*0.7},{h*0.3} {-h*0.7},{-h*0.5} Z"/>'
             f'<path d="M{-h*0.28},0 L{-h*0.05},{h*0.28} L{h*0.35},{-h*0.25}"/>')
    return _ic(cx, cy, s, color, p)

# ------------------------------------------------------------------ emblema / sello
def seal(cx, cy, r, uid, solid=True):
    pid = f"sealtop{uid}"
    rt = r * 0.78
    top_path = f'M {cx-rt:.1f},{cy:.1f} A {rt:.1f},{rt:.1f} 0 0 1 {cx+rt:.1f},{cy:.1f}'
    s = []
    if solid:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ESP}"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.9:.1f}" fill="none" stroke="{GOLDL}" stroke-width="{r*0.018:.1f}"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.97:.1f}" fill="none" stroke="{GOLD}" stroke-width="{r*0.03:.1f}"/>')
        ringcol, ctr = GOLDL, CREAM
    else:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ESP}" stroke-width="{r*0.05:.1f}"/>')
        ringcol, ctr = ESP, ESP
    s.append(f'<defs><path id="{pid}" d="{top_path}"/></defs>')
    s.append(f'<text font-family="{SERIF}" font-weight="700" font-size="{r*0.135:.1f}" fill="{ringcol}" '
             f'letter-spacing="{r*0.03:.1f}"><textPath href="#{pid}" startOffset="50%" text-anchor="middle">'
             f'COMPROMETIDOS CON LOS CAFETEROS</textPath></text>')
    # estrellas/granos a los lados
    s.append(bean(cx - rt + 6, cy + 3, r*0.07, -20, ringcol))
    s.append(bean(cx + rt - 6, cy + 3, r*0.07, 20, ringcol))
    # centro
    s.append(bean(cx, cy - r*0.34, r*0.13, 0, GOLDL))
    s.append(T(cx, cy - r*0.05, "PLANCHA", r*0.16, r*1.2, "middle", "800", ctr, SANS, 2))
    s.append(T(cx, cy + r*0.55, "2", r*0.92, None, "middle", "900", GOLDL if solid else CLAY, DISP))
    s.append(T(cx, cy + r*0.8, "ELECCIONES CAFETERAS", r*0.075, r*1.3, "middle", "700", ringcol, SANS, 2))
    return "".join(s)

# ------------------------------------------------------------------ retrato en arco
def arch_path(x, y, w, h, ay):
    return (f'M {x:.1f},{y+h:.1f} L {x:.1f},{y+ay:.1f} Q {x:.1f},{y:.1f} {x+w/2:.1f},{y:.1f} '
            f'Q {x+w:.1f},{y:.1f} {x+w:.1f},{y+ay:.1f} L {x+w:.1f},{y+h:.1f} Z')

def arch_photo(img_key, x, y, w, h, defs, uid, border=GOLD, bw=6, bias="xMidYMin", mat=True):
    ay = w * 0.5
    d_ = arch_path(x, y, w, h, ay)
    defs.append(f'<clipPath id="ar{uid}"><path d="{d_}"/></clipPath>')
    s = []
    if mat:
        m = 10
        s.append(f'<g filter="url(#soft)"><path d="{arch_path(x-m, y-m, w+2*m, h+2*m, ay+m)}" fill="{SAND}"/></g>')
    im = IMG[img_key]
    s.append(f'<image href="{im}" xlink:href="{im}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
             f'preserveAspectRatio="{bias} slice" clip-path="url(#ar{uid})"/>')
    s.append(f'<path d="{d_}" fill="none" stroke="{border}" stroke-width="{bw}"/>')
    return "".join(s)

def candidate_arch(cx, top, w, key, defs, uid, name_size=26, role_size=15, h_ratio=1.18, short=False):
    h = w * h_ratio
    x = cx - w / 2
    cand = CAND[key]
    s = [arch_photo(cand["img"], x, top, w, h, defs, uid)]
    ny = top + h + 16
    s.append(T(cx, ny + role_size, cand["rol"], role_size, w + 80, "middle", "700", CLAY, SERIF, 2, "italic"))
    if short:
        s.append(T(cx, ny + role_size + name_size + 8, cand["corto"], name_size, w + 40, "middle", "900", INK, DISP))
    else:
        l1, l2 = two_lines(cand["nombre"])
        blk, yend, _ = stack(cx, ny + role_size + 8, [{"text": l1, "size": name_size, "fill": INK, "gap": 0},
                                                      {"text": l2, "size": name_size, "fill": INK}])
        s.append(blk)
    return "".join(s)

# ------------------------------------------------------------------ estructura
def defs(extra=""):
    return f'''<defs>
  <linearGradient id="gCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="#F0E4C8"/></linearGradient>
  <linearGradient id="gEsp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ESP}"/><stop offset="1" stop-color="{INK}"/></linearGradient>
  <linearGradient id="gClay" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CLAY}"/><stop offset="1" stop-color="{CLAYD}"/></linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLDL}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
  <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEND}"/></linearGradient>
  <linearGradient id="gScrim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity="0.8"/></linearGradient>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="{INK}" flood-opacity="0.30"/></filter>
  {extra}
</defs>'''

def label_eyebrow(cx, y, text):
    return eyebrow(cx, y, text, 18, CLAY, 150)

def svg(W, H, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"{extra}>')

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    minidom.parseString(content.encode("utf-8"))
    print(f"  OK {name} ({len(content)//1024} KB)")



# ====================================================================== piezas
def rphoto(img_key, x, y, w, h, defs, uid, rad=14, border=GOLD, bw=5, bias="xMidYMid", mat=True):
    cid = f"rp{uid}"
    defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rad}"/></clipPath>')
    s = []
    if mat:
        m = 8
        s.append(f'<g filter="url(#soft)"><rect x="{x-m:.1f}" y="{y-m:.1f}" width="{w+2*m:.1f}" height="{h+2*m:.1f}" rx="{rad+4}" fill="{SAND}"/></g>')
    im = IMG[img_key]
    s.append(f'<image href="{im}" xlink:href="{im}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="{bias} slice" clip-path="url(#{cid})"/>')
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rad}" fill="none" stroke="{border}" stroke-width="{bw}"/>')
    return "".join(s)

def icon_row(b, x, y, w, name, title, desc, idx):
    col = [CLAY, GREEN, GOLD, GREEND, CLAYD][idx]
    cyr = y + 42
    b.append(f'<circle cx="{x+44}" cy="{cyr}" r="40" fill="none" stroke="{col}" stroke-width="3"/>')
    b.append(icon(name, x + 44, cyr, 44, col))
    b.append(T(x + 110, y + 36, title, 30, w - 130, "start", "900", INK, DISP))
    for j, ln in enumerate(multiline(desc, 52)[:2]):
        b.append(T(x + 110, y + 70 + j*27, ln, 19, w - 120, "start", "400", "#5C4A38", SERIF))
    b.append(f'<line x1="{x}" y1="{y+128}" x2="{x+w}" y2="{y+128}" stroke="{GOLD}" stroke-width="1" opacity="0.55"/>')

def texture(b, W, H, cx, cy):
    b.append(contours(cx, cy, 60, 7, 30, ESP, 0.08))
    b.append(ring_stain(W*0.12, H*0.9, 70, CLAY, 0.10))
    b.append(ridge(0, H - 70, W, 30, GREEN, 0.14))


def marca():
    W = H = 1000
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    texture(b, W, H, 940, 70)
    b.append(label_eyebrow(W/2, 92, ORG))
    b.append(seal(W/2, 430, 215, "MK"))
    for cx, key in [(290, "principal"), (710, "suplente")]:
        cand = CAND[key]; l1, l2 = two_lines(cand["nombre"])
        b.append(T(cx, 752, cand["rol"], 17, 360, "middle", "700", CLAY, SERIF, 2, "italic"))
        bl, _, _ = stack(cx, 762, [{"text": l1, "size": 27, "fill": INK, "gap": 0}, {"text": l2, "size": 27, "fill": INK}])
        b.append(bl)
    b.append(T(W/2, 912, LEMA, 24, 600, "middle", "700", GREEN, SERIF, 1, "italic"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("00-marca.svg", "".join(s))


def afiche_principal():
    W, H = 1000, 1414
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    texture(b, W, H, 950, 60)
    b.append(label_eyebrow(W/2, 78, ORG))
    b.append(candidate_arch(285, 120, 300, "principal", d, "ap", 25))
    b.append(candidate_arch(715, 120, 300, "suplente", d, "as", 25))
    sl, yend, bl = stack(W/2, 640, [{"text": "COMPROMETIDOS", "size": 90, "fill": INK, "gap": 0, "max_w": 900},
                                    {"text": "CON LOS CAFETEROS", "size": 54, "fill": CLAY, "gap": 8, "max_w": 900}])
    b.append(sl)
    b.append(f'<rect x="{W/2-150}" y="{bl[0]+10:.0f}" width="300" height="6" rx="3" fill="url(#gGold)"/>')
    b.append(T(W/2, yend + 36, LEMA, 26, 700, "middle", "700", GREEN, SERIF, 1, "italic"))
    b.append(seal(W/2, 1070, 150, "AP"))
    b.append(ballot(180, 1070, 64)); b.append(T(180, 1170, "MARCA EL 2", 18, 200, "middle", "800", CLAY, SANS, 1))
    b.append(ballot(820, 1070, 64)); b.append(T(820, 1170, "TU VOTO CUENTA", 16, 220, "middle", "800", CLAY, SANS, 1))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("01-afiche-principal.svg", "".join(s))


def afiche_propuestas():
    W, H = 1000, 1414
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(contours(70, 1360, 50, 6, 28, ESP, 0.07))
    b.append(ring_stain(900, 120, 70, CLAY, 0.10))
    bt, _, _ = stack(70, 70, [{"text": "NUESTRAS", "size": 56, "fill": INK, "gap": 0}, {"text": "PROPUESTAS", "size": 56, "fill": CLAY, "gap": 6}], "start")
    b.append(bt)
    b.append(T(72, 296, ORG, 16, 520, "start", "700", GREEN, SERIF, 2, "italic"))
    b.append(seal(872, 150, 92, "PR"))
    y0 = 350
    for i, (ic, t, desc) in enumerate(PROPUESTAS):
        icon_row(b, 70, y0 + i*148, 860, ic, t, desc, i)
    sy = 1100
    b.append(rphoto("cafetales", 70, sy, 270, 120, d, "p1", 12))
    b.append(rphoto("nevado", 365, sy, 270, 120, d, "p2", 12))
    b.append(rphoto("cafeteros", 660, sy, 270, 120, d, "p3", 12))
    b.append(f'<rect x="0" y="1300" width="{W}" height="114" fill="url(#gEsp)"/>')
    b.append(ballot(90, 1357, 56, GOLDL))
    b.append(T(150, 1350, "VOTA PLANCHA 2", 42, 560, "start", "900", GOLDL, DISP))
    b.append(T(150, 1388, SLOGAN, 18, 560, "start", "700", CREAM, SERIF, 1, "italic"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("02-afiche-propuestas.svg", "".join(s))


def pasacalle():
    W, H = 2400, 480
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(ridge(0, 410, W, 26, GREEN, 0.13))
    b.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="14" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    b.append(seal(235, 235, 150, "PA"))
    b.append(candidate_arch(490, 70, 150, "principal", d, "qa", 19, 13, short=True))
    b.append(candidate_arch(680, 70, 150, "suplente", d, "qb", 19, 13, short=True))
    sl, yend, bl = stack(880, 120, [{"text": "COMPROMETIDOS", "size": 86, "fill": INK, "gap": 0, "max_w": 1380},
                                    {"text": "CON LOS CAFETEROS", "size": 60, "fill": CLAY, "gap": 8, "max_w": 1380}], "start")
    b.append(sl)
    b.append(f'<rect x="882" y="{bl[0]+8:.0f}" width="280" height="6" rx="3" fill="url(#gGold)"/>')
    b.append(T(880, yend + 34, LEMA, 26, 900, "start", "700", GREEN, SERIF, 1, "italic"))
    b.append(ballot(2250, 150, 90)); b.append(T(2250, 250, "VOTA 2", 30, 200, "middle", "900", CLAY, DISP))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("03-pasacalle.svg", "".join(s))


def valla():
    W, H = 2400, 1200
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(contours(120, 1120, 70, 7, 34, ESP, 0.07))
    b.append(ridge(0, 1010, W, 40, GREEN, 0.12))
    b.append(label_eyebrow(700, 96, ORG))
    b.append(candidate_arch(360, 150, 420, "principal", d, "va", 34))
    b.append(candidate_arch(840, 150, 420, "suplente", d, "vb", 34))
    sl, yend, bl = stack(1230, 220, [{"text": "COMPROMETIDOS", "size": 100, "fill": INK, "gap": 0, "max_w": 760},
                                     {"text": "CON LOS CAFETEROS", "size": 74, "fill": CLAY, "gap": 8, "max_w": 760}], "start")
    b.append(sl)
    b.append(f'<rect x="1232" y="{bl[0]+10:.0f}" width="360" height="7" rx="3" fill="url(#gGold)"/>')
    b.append(T(1230, yend + 40, LEMA, 30, 740, "start", "700", GREEN, SERIF, 1, "italic"))
    for i, (ic, t, desc) in enumerate(PROPUESTAS[:4]):
        ry = 560 + i*108
        b.append(f'<circle cx="1262" cy="{ry}" r="34" fill="none" stroke="{[CLAY,GREEN,GOLD,GREEND][i]}" stroke-width="3"/>')
        b.append(icon(ic, 1262, ry, 38, [CLAY, GREEN, GOLD, GREEND][i]))
        b.append(T(1318, ry + 12, t, 38, 760, "start", "900", INK, DISP))
    b.append(seal(2160, 250, 160, "VL"))
    b.append(rphoto("cafetales", 1990, 470, 360, 165, d, "v1", 14))
    b.append(rphoto("nevado", 1990, 650, 360, 165, d, "v2", 14))
    b.append(rphoto("cafeteros", 1990, 830, 360, 165, d, "v3", 14))
    b.append(f'<rect x="0" y="1070" width="{W}" height="130" fill="url(#gEsp)"/>')
    b.append(ballot(110, 1135, 70, GOLDL))
    b.append(T(180, 1152, "VOTA PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS", 46, 2150, "start", "900", GOLDL, DISP, 1))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("04-valla.svg", "".join(s))


def tarjeta_frente():
    W, H = 1050, 600
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(ring_stain(120, 520, 60, CLAY, 0.10))
    b.append(seal(220, 300, 150, "TF"))
    b.append(label_eyebrow(720, 78, "COMITÉ DE CAFETEROS"))
    sl, yend, bl = stack(720, 96, [{"text": "COMPROMETIDOS", "size": 40, "fill": INK, "gap": 0, "max_w": 600},
                                   {"text": "CON LOS CAFETEROS", "size": 28, "fill": CLAY, "gap": 6, "max_w": 600}])
    b.append(sl)
    b.append(f'<rect x="570" y="{bl[0]+8:.0f}" width="300" height="5" rx="2" fill="url(#gGold)"/>')
    b.append(candidate_arch(620, 250, 110, "principal", d, "ta", 17, 12, short=True))
    b.append(candidate_arch(810, 250, 110, "suplente", d, "tb", 17, 12, short=True))
    b.append(ballot(960, 300, 56, CLAY))
    b.append(T(720, 560, LEMA, 18, 600, "middle", "700", GREEN, SERIF, 1, "italic"))
    b.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" rx="16" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("05a-tarjeta-frente.svg", "".join(s))


def tarjeta_respaldo():
    W, H = 1050, 600
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gEsp)"/>']
    b.append(contours(950, 80, 40, 6, 26, GOLDL, 0.10))
    b.append(T(60, 90, "NUESTRAS PROPUESTAS", 38, 720, "start", "900", GOLDL, DISP, 1))
    for i, (ic, t, desc) in enumerate(PROPUESTAS):
        ry = 150 + i*72
        b.append(f'<circle cx="86" cy="{ry}" r="26" fill="none" stroke="{GOLDL}" stroke-width="2.5"/>')
        b.append(icon(ic, 86, ry, 28, GOLDL))
        b.append(T(130, ry + 9, t, 25, 560, "start", "800", CREAM, SANS, 1))
    b.append(seal(870, 220, 120, "TR"))
    b.append(rphoto("cafeteros", 770, 360, 200, 120, d, "tr1", 12, GOLDL, 4))
    b.append(f'<rect x="0" y="544" width="{W}" height="6" fill="url(#gGold)"/>')
    b.append(T(W/2, 582, "PLANCHA 2   ·   POR UNOS CAFETEROS PRÓSPEROS", 22, 900, "middle", "800", GOLDL, SANS, 1))
    b.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" rx="16" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("05b-tarjeta-respaldo.svg", "".join(s))


def redes_post():
    W = H = 1080
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    texture(b, W, H, 1010, 70)
    b.append(label_eyebrow(W/2, 80, ORG))
    sl, yend, bl = stack(W/2, 110, [{"text": "COMPROMETIDOS", "size": 72, "fill": INK, "gap": 0, "max_w": 1000},
                                    {"text": "CON LOS CAFETEROS", "size": 52, "fill": CLAY, "gap": 6, "max_w": 1000}])
    b.append(sl)
    b.append(seal(W/2, 372, 80, "RP"))
    b.append(candidate_arch(300, 452, 292, "principal", d, "ra", 24))
    b.append(candidate_arch(780, 452, 292, "suplente", d, "rb", 24))
    b.append(f'<rect x="0" y="958" width="{W}" height="122" fill="url(#gEsp)"/>')
    b.append(ballot(86, 1018, 54, GOLDL))
    b.append(T(146, 1010, "VOTA PLANCHA 2", 44, 600, "start", "900", GOLDL, DISP))
    b.append(T(146, 1050, LEMA, 18, 600, "start", "700", CREAM, SERIF, 1, "italic"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("06-redes-post.svg", "".join(s))


def redes_historia():
    W, H = 1080, 1920
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(contours(960, 120, 60, 7, 32, ESP, 0.07))
    b.append(ridge(0, 1640, W, 40, GREEN, 0.12))
    b.append(label_eyebrow(W/2, 150, ORG))
    sl, yend, bl = stack(W/2, 180, [{"text": "COMPROMETIDOS", "size": 82, "fill": INK, "gap": 0, "max_w": 1000},
                                    {"text": "CON LOS CAFETEROS", "size": 60, "fill": CLAY, "gap": 8, "max_w": 1000}])
    b.append(sl)
    b.append(T(W/2, yend + 40, LEMA, 28, 800, "middle", "700", GREEN, SERIF, 1, "italic"))
    b.append(seal(W/2, 560, 140, "RH"))
    b.append(candidate_arch(330, 760, 330, "principal", d, "ha", 27))
    b.append(candidate_arch(750, 760, 330, "suplente", d, "hb", 27))
    sy = 1340
    b.append(rphoto("cafetales", 60, sy, 300, 170, d, "h1", 14))
    b.append(rphoto("nevado", 390, sy, 300, 170, d, "h2", 14))
    b.append(rphoto("cafeteros", 720, sy, 300, 170, d, "h3", 14))
    b.append(f'<rect x="0" y="1740" width="{W}" height="180" fill="url(#gEsp)"/>')
    b.append(ballot(W/2 - 320, 1830, 64, GOLDL))
    b.append(T(W/2 + 30, 1820, "VOTA PLANCHA 2", 56, 700, "middle", "900", GOLDL, DISP))
    b.append(T(W/2 + 30, 1868, SLOGAN, 22, 700, "middle", "700", CREAM, SERIF, 1, "italic"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("07-redes-historia.svg", "".join(s))


def volante():
    W, H = 1000, 1414
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(ring_stain(900, 1320, 60, CLAY, 0.10))
    b.append(label_eyebrow(W/2, 70, ORG))
    sl, yend, bl = stack(W/2, 92, [{"text": "COMPROMETIDOS", "size": 58, "fill": INK, "gap": 0, "max_w": 900},
                                   {"text": "CON LOS CAFETEROS", "size": 42, "fill": CLAY, "gap": 6, "max_w": 900}])
    b.append(sl)
    b.append(candidate_arch(295, 280, 165, "principal", d, "oa", 18, 12, short=True))
    b.append(candidate_arch(705, 280, 165, "suplente", d, "ob", 18, 12, short=True))
    b.append(seal(W/2, 360, 72, "VO"))
    b.append(T(W/2, 552, "NUESTRAS PROPUESTAS", 32, 700, "middle", "900", INK, DISP, 1))
    y0 = 588
    for i, (ic, t, desc) in enumerate(PROPUESTAS):
        icon_row(b, 80, y0 + i*128, 840, ic, t, desc, i)
    b.append(f'<rect x="0" y="1318" width="{W}" height="96" fill="url(#gEsp)"/>')
    b.append(ballot(90, 1366, 50, GOLDL))
    b.append(T(150, 1380, "VOTA PLANCHA 2", 40, 760, "start", "900", GOLDL, DISP))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("08-volante.svg", "".join(s))


def hero_animado():
    """Pieza animada (SMIL) para web/redes."""
    W = H = 1080
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gCream)"/>']
    b.append(contours(1010, 70, 60, 7, 32, ESP, 0.07))
    # cordillera que se dibuja
    pts = [(0,0.55),(0.12,0.2),(0.22,0.5),(0.34,0.05),(0.46,0.42),(0.58,0.12),(0.7,0.5),(0.82,0.18),(0.92,0.46),(1,0.3)]
    dd = "M " + " L ".join(f"{px*W:.0f},{760+py*60:.0f}" for px, py in pts)
    b.append(f'<path d="{dd}" fill="none" stroke="{GREEN}" stroke-width="3" opacity="0.5" stroke-dasharray="2400" stroke-dashoffset="2400">'
             f'<animate attributeName="stroke-dashoffset" from="2400" to="0" dur="2.4s" fill="freeze"/></path>')
    # eslogan con aparicion
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="1s" fill="freeze"/>'
             + T(W/2, 230, "COMPROMETIDOS", 76, 1000, "middle", "900", INK, DISP)
             + T(W/2, 300, "CON LOS CAFETEROS", 54, 1000, "middle", "900", CLAY, DISP) + '</g>')
    # sello con pulso
    b.append(f'<g transform="translate({W/2},560)"><g>'
             f'<animateTransform attributeName="transform" type="scale" values="0.9;1;0.9" dur="3.5s" repeatCount="indefinite" additive="sum"/>'
             + seal(0, 0, 150, "HA") + '</g></g>')
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.1s" dur="1s" fill="freeze"/>'
             + ballot(W/2, 820, 70, CLAY)
             + T(W/2, 920, "MARCA LA PLANCHA 2", 34, 800, "middle", "900", INK, DISP, 1) + '</g>')
    # grano que cae
    b.append(f'<g>{bean(540, -40, 16, 25)}<animateTransform attributeName="transform" type="translate" '
             f'values="0,0; 0,1120" dur="2.6s" begin="0.6s" repeatCount="indefinite"/></g>')
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("09-hero-animado.svg", "".join(s))


def build_exporter():
    import re, json
    piezas = [("00-marca", "Emblema / sello"), ("01-afiche-principal", "Afiche principal"),
              ("02-afiche-propuestas", "Afiche de propuestas"), ("03-pasacalle", "Pasacalle"),
              ("04-valla", "Valla publicitaria"), ("05a-tarjeta-frente", "Tarjeta — frente"),
              ("05b-tarjeta-respaldo", "Tarjeta — respaldo"), ("06-redes-post", "Post de redes"),
              ("07-redes-historia", "Historia de redes"), ("08-volante", "Volante")]
    items = []
    for fn, title in piezas:
        txt = open(os.path.join(OUT, fn + ".svg"), encoding="utf-8").read()
        m = re.search(r'width="(\d+)"\s+height="(\d+)"', txt)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (1000, 1000)
        items.append({"n": fn, "t": title, "w": w, "h": h, "b": base64.b64encode(txt.encode()).decode()})
    doc = '''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Exportar a PNG · Plancha 2</title><style>
:root{--esp:#20140D;--cream:#F7EFDE;--clay:#B5532E;--green:#3C5A38;--gold:#C9962E;--goldl:#E7C56B}
*{box-sizing:border-box;margin:0;padding:0;font-family:Georgia,serif}body{background:var(--cream);color:var(--esp)}
header{background:var(--esp);color:#fff;padding:30px 20px;text-align:center;border-bottom:6px solid var(--gold)}
header p{color:var(--goldl);margin-top:6px;font-style:italic}
.bar{position:sticky;top:0;z-index:5;background:#fff;box-shadow:0 3px 12px rgba(0,0,0,.12);padding:14px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;justify-content:center;font-family:Arial}
select,button{font-size:15px;padding:10px 16px;border-radius:10px;border:2px solid var(--gold);background:#fff;font-weight:700;cursor:pointer;font-family:Arial}
button.all{background:var(--clay);color:#fff;border-color:var(--clay)}button.primary{background:var(--green);color:#fff;border-color:var(--green)}
.wrap{max-width:1150px;margin:0 auto;padding:24px 18px 70px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 7px 20px rgba(0,0,0,.12)}
.thumb{background:repeating-conic-gradient(#eee 0 25%,#f8f8f8 0 50%) 50%/20px 20px;padding:12px;display:flex;align-items:center;justify-content:center;min-height:160px}
.thumb img{max-width:100%;max-height:230px;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.2)}
.meta{padding:13px 15px;font-family:Arial}.meta h3{color:var(--esp);font-size:16px}.meta .d{font-size:12px;color:#8a7b66;margin:3px 0 9px}
.note{background:#fff;border-left:6px solid var(--gold);padding:15px 18px;border-radius:10px;margin:18px 0;line-height:1.5;font-size:14px;font-family:Arial}
#st{font-family:Arial;font-weight:700;color:var(--green)}</style></head><body>
<header><h1>Descargar la campaña en PNG</h1><p>Plancha 2 · Comprometidos con los Cafeteros</p></header>
<div class="bar"><label style="font-family:Arial;font-weight:700">Resolución:</label><select id="scale"><option value="1">1x</option><option value="2" selected>2x (imprenta)</option><option value="3">3x</option></select>
<button class="all" onclick="todas()">Descargar TODAS</button><span id="st"></span></div>
<div class="wrap"><div class="note"><b>Cómo usar:</b> elige resolución y pulsa <b>Descargar TODAS</b>, o el botón de cada pieza. Para vallas y pasacalles, entrega el <b>.svg</b> a la imprenta (vectorial, sin pérdida).</div>
<div class="grid" id="g"></div></div>
<script>const P=__DATA__;
function du(p){return 'data:image/svg+xml;base64,'+p.b}
function ld(p){return new Promise((ok,er)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>er(Error(p.n));i.src=du(p)})}
async function png(p,s){const im=await ld(p);const c=document.createElement('canvas');c.width=Math.round(p.w*s);c.height=Math.round(p.h*s);const x=c.getContext('2d');x.fillStyle='#F7EFDE';x.fillRect(0,0,c.width,c.height);x.imageSmoothingQuality='high';x.drawImage(im,0,0,c.width,c.height);return await new Promise((r,j)=>c.toBlob(b=>b?r(b):j(Error('blob')),'image/png'))}
function dl(b,n){const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=n;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),5000)}
async function una(i){const p=P[i],s=+scale.value;try{dl(await png(p,s),p.n+'.png')}catch(e){alert('Error '+p.n+': '+e.message)}}
async function todas(){const s=+scale.value;for(let i=0;i<P.length;i++){st.textContent='Generando '+(i+1)+'/'+P.length+'…';try{dl(await png(P[i],s),P[i].n+'.png')}catch(e){}await new Promise(r=>setTimeout(r,600))}st.textContent='¡Listo! Revisa Descargas.'}
P.forEach((p,i)=>{g.insertAdjacentHTML('beforeend',`<div class="card"><div class="thumb"><img src="${du(p)}"></div><div class="meta"><h3>${p.t}</h3><div class="d">${p.w}×${p.h}px (vector)</div><button class="primary" onclick="una(${i})">Descargar PNG</button></div></div>`)})</script></body></html>'''
    doc = doc.replace("__DATA__", json.dumps(items))
    with open(os.path.join(OUT, "exportar-png.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  OK exportar-png.html ({len(doc)//1024} KB)")


if __name__ == "__main__":
    print("Generando sistema visual...")
    marca(); afiche_principal(); afiche_propuestas(); pasacalle(); valla()
    tarjeta_frente(); tarjeta_respaldo(); redes_post(); redes_historia(); volante()
    hero_animado(); build_exporter()
    print("Listo.")
