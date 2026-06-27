# -*- coding: utf-8 -*-
"""
Campana "PLANCHA 2 - COMPROMETIDOS CON LOS CAFETEROS".
Jhon Esneider Prieto Prieto (Principal) y Nelson Ferned Orozco Castano (Suplente).

Diseno: composicion por bloques de color (alto contraste y legibilidad), fotos
NATURALES enmarcadas en recuadros sutiles con paspartu calido, texto apilado con
interlineado seguro (sin solapes), e incorporacion de cafetales, Nevado y cafeteros.
"""
import base64, os, html, xml.dom.minidom as minidom

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(BASE)
OUT = BASE
ASSETS = os.path.join(BASE, "assets")

def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")

def opt(path, fallback):
    return data_uri(path) if os.path.exists(path) else fallback

_caf = data_uri(os.path.join(SRC, "CAFETALES.jpg"))
IMG = {
    "cafetales": _caf,
    "jhon":   data_uri(os.path.join(SRC, "Jhon Esneider Prieto Prieto.jpeg")),
    "nelson": data_uri(os.path.join(SRC, "Nelson Ferned Orozco Castaño.jpeg")),
    "nevado": data_uri(os.path.join(SRC, "NEVADO DEL RUIZ.jfif")),
    "cafeteros": opt(os.path.join(ASSETS, "cafeteros.jpg"), _caf),
    "cafetero2": opt(os.path.join(ASSETS, "cafetero2.jpg"), _caf),
}

C = {
    "espresso": "#241710", "brown": "#4A2C1C", "coffee": "#6F4A2E", "caramel": "#B07D49",
    "red": "#C32026", "red_dark": "#911A1F",
    "gold": "#E0A23B", "gold_lt": "#F6D488", "gold_dk": "#B07E26",
    "green": "#2F7D34", "green_dk": "#1C5A23",
    "cream": "#FBF4E6", "cream2": "#F3E6CB", "white": "#FFFFFF",
}
ORG = "COMITÉ DEPARTAMENTAL DE CAFETEROS"
SLOGAN = "COMPROMETIDOS CON LOS CAFETEROS"
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

# --------------------------------------------------------------------------- texto
def T(x, y, text, size, max_w=None, anchor="start", weight="900",
      fill="#000", family=HEAVY, spacing=0.0, flt=None, opacity=None):
    factor = 0.64 if weight in ("900", "800") else 0.55
    est = len(text) * size * factor + max(0, len(text) - 1) * spacing
    extra = f' textLength="{max_w:.0f}" lengthAdjust="spacingAndGlyphs"' if (max_w and est > max_w) else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    fl = f' filter="url(#{flt})"' if flt else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{family}" '
            f'font-weight="{weight}" font-size="{size:.1f}" fill="{fill}"{sp}{fl}{op}{extra}>{esc(text)}</text>')

def stack(cx, top, lines, anchor="middle"):
    """Apila lineas con interlineado seguro. Devuelve (svg, y_final, baselines)."""
    out, y, bl = [], top, []
    for i, ln in enumerate(lines):
        s = ln["size"]
        y += (0 if i == 0 else ln.get("gap", 16)) + s
        bl.append(y)
        out.append(T(cx, y, ln["text"], s, ln.get("max_w"), anchor, ln.get("weight", "900"),
                     ln.get("fill", "#000"), ln.get("family", HEAVY), ln.get("spacing", 0), ln.get("flt")))
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

# --------------------------------------------------------------------------- motivos
def cherry(cx, cy, r, color=None):
    color = color or C["red"]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}"/>'
            f'<ellipse cx="{cx-r*0.3:.1f}" cy="{cy-r*0.32:.1f}" rx="{r*0.3:.1f}" ry="{r*0.22:.1f}" fill="#fff" opacity="0.45"/>')

def leaf(cx, cy, L, W, ang, color=None):
    color = color or C["green"]
    h = W / 2
    d = f'M0,0 C {L*0.28:.1f},{-h:.1f} {L*0.72:.1f},{-h:.1f} {L:.1f},0 C {L*0.72:.1f},{h:.1f} {L*0.28:.1f},{h:.1f} 0,0 Z'
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})"><path d="{d}" fill="{color}"/>'
            f'<path d="M{L*0.05:.1f},0 L{L*0.9:.1f},0" stroke="{C["green_dk"]}" stroke-width="{max(W*0.05,1):.1f}" opacity="0.5"/></g>')

def sprig(x, y, scale=1.0, ang=0.0, flip=False):
    fl = -1 if flip else 1
    p = [f'<g transform="translate({x:.1f},{y:.1f}) scale({scale*fl:.3f},{scale:.3f}) rotate({ang:.1f})" opacity="0.96">',
         f'<path d="M0,0 C 70,-8 150,-28 250,-22" stroke="{C["brown"]}" stroke-width="7" fill="none" stroke-linecap="round"/>']
    for lx, ly, ll, lw, la in [(55,-6,70,30,-38),(55,-6,66,28,28),(120,-20,76,33,-32),
                               (120,-20,70,30,34),(185,-26,70,30,-28),(185,-26,64,28,40)]:
        p.append(leaf(lx, ly, ll, lw, la))
    for chx, chy, chr_ in [(238,-30,15),(252,-16,16),(236,-8,14),(258,-30,13),(248,-44,12)]:
        p.append(cherry(chx, chy, chr_))
    p.append('</g>')
    return "".join(p)

def bean(cx, cy, r, ang=0, color=None):
    color = color or C["gold"]
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})"><ellipse rx="{r:.1f}" ry="{r*0.64:.1f}" fill="{color}"/>'
            f'<path d="M{-r*0.7:.1f},{-r*0.26:.1f} C {-r*0.1:.1f},{r*0.16:.1f} {r*0.1:.1f},{-r*0.16:.1f} {r*0.7:.1f},{r*0.26:.1f}" '
            f'stroke="{C["espresso"]}" stroke-width="{max(r*0.12,1):.1f}" fill="none" opacity="0.7"/></g>')

def check(cx, cy, r, bg=None, fg="#fff"):
    bg = bg or C["green"]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{bg}"/>'
            f'<path d="M{cx-r*0.45:.1f},{cy:.1f} L{cx-r*0.1:.1f},{cy+r*0.35:.1f} L{cx+r*0.5:.1f},{cy-r*0.4:.1f}" '
            f'stroke="{fg}" stroke-width="{r*0.22:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def badge(cx, cy, r, flt="soft"):
    return (f'<g filter="url(#{flt})"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gBadge)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.9:.1f}" fill="none" stroke="{C["gold_lt"]}" stroke-width="{r*0.04:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["white"]}" stroke-width="{r*0.05:.1f}"/></g>'
            + T(cx, cy - r*0.30, "PLANCHA", r*0.23, r*1.4, "middle", "800", C["gold_lt"], BOLD, 3)
            + T(cx, cy + r*0.66, "2", r*1.15, None, "middle", "900", C["white"], HEAVY))

# --------------------------------------------------------------------------- fotos
def photo(img_key, x, y, w, h, defs, rad=18, border=None, bw=6, bias="xMidYMid", mat=True):
    border = border or C["white"]
    cid = f"cp{img_key}{int(x)}_{int(y)}"
    defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rad}"/></clipPath>')
    s = []
    if mat:
        m = 9
        s.append(f'<g filter="url(#soft)"><rect x="{x-m:.1f}" y="{y-m:.1f}" width="{w+2*m:.1f}" height="{h+2*m:.1f}" rx="{rad+5}" fill="url(#gWarm)"/></g>')
    img = IMG[img_key]
    s.append(f'<image href="{img}" xlink:href="{img}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
             f'preserveAspectRatio="{bias} slice" clip-path="url(#{cid})"/>')
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rad}" fill="none" stroke="{border}" stroke-width="{bw}"/>')
    return "".join(s)

def candidate_card(cx, top, w, key, defs, name_size=26, role_size=20, short=False, ratio=0.80):
    h = w / ratio
    x = cx - w / 2
    cand = CAND[key]
    rc = C["red"] if key == "principal" else C["green"]
    s = [photo(cand["img"], x, top, w, h, defs, 16, C["white"], 6, "xMidYMin")]
    py = top + h - role_size * 0.9
    pw = role_size * len(cand["rol"]) * 0.66 + 40
    ph = role_size + 14
    s.append(f'<g filter="url(#soft)"><rect x="{cx-pw/2:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="{ph/2:.1f}" fill="{rc}"/></g>')
    s.append(T(cx, py + role_size + 0.5, cand["rol"], role_size, pw - 14, "middle", "800", "#fff", BOLD, 1.5))
    if short:
        s.append(T(cx, top + h + role_size + 26, cand["corto"], name_size, w + 30, "middle", "900", C["espresso"], HEAVY))
    else:
        l1, l2 = two_lines(cand["nombre"])
        blk, _, _ = stack(cx, top + h + 10, [{"text": l1, "size": name_size, "fill": C["espresso"], "gap": 0},
                                             {"text": l2, "size": name_size, "fill": C["espresso"]}])
        s.append(blk)
    return "".join(s)

# --------------------------------------------------------------------------- estructura
def defs(extra=""):
    return f'''<defs>
  <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['cream']}"/><stop offset="1" stop-color="{C['cream2']}"/></linearGradient>
  <linearGradient id="gWarm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F8E8D2"/><stop offset="1" stop-color="#E7C49E"/></linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['gold_lt']}"/><stop offset="1" stop-color="{C['gold']}"/></linearGradient>
  <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['green']}"/><stop offset="1" stop-color="{C['green_dk']}"/></linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['red']}"/><stop offset="1" stop-color="{C['red_dark']}"/></linearGradient>
  <linearGradient id="gBrown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['brown']}"/><stop offset="1" stop-color="{C['espresso']}"/></linearGradient>
  <linearGradient id="gScrimL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['espresso']}" stop-opacity="0.85"/><stop offset="1" stop-color="{C['espresso']}" stop-opacity="0.05"/></linearGradient>
  <radialGradient id="gBadge" cx="38%" cy="32%" r="80%"><stop offset="0" stop-color="#DA3A40"/><stop offset="60%" stop-color="{C['red']}"/><stop offset="100%" stop-color="{C['red_dark']}"/></radialGradient>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="{C['espresso']}" flood-opacity="0.35"/></filter>
  {extra}
</defs>'''

def topbar(W, h=110, org=True):
    s = [f'<rect x="0" y="0" width="{W}" height="{h}" fill="url(#gRed)"/>',
         f'<rect x="0" y="{h}" width="{W}" height="{max(h*0.06,5):.0f}" fill="url(#gGold)"/>']
    if org:
        s.append(T(W/2, h*0.63, ORG, h*0.30, W*0.92, "middle", "800", "#fff", BOLD, 3))
    return "".join(s)

def goldbar(W, y, h, text):
    return (f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="url(#gGold)"/>'
            + T(W/2, y + h*0.66, text, h*0.42, W*0.92, "middle", "900", C["espresso"], HEAVY, 1))

def greenbar(W, y, h, l1, l2=None):
    s = [f'<rect x="0" y="{y-6}" width="{W}" height="6" fill="url(#gGold)"/>',
         f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="url(#gGreen)"/>']
    if l2:
        b, _, _ = stack(W/2, y + h*0.12, [{"text": l1, "size": h*0.34, "fill": C["gold_lt"]},
                                          {"text": l2, "size": h*0.20, "fill": "#fff", "family": BOLD, "weight": "700", "spacing": 2, "gap": 8}])
        s.append(b)
    else:
        s.append(T(W/2, y + h*0.66, l1, h*0.46, W*0.9, "middle", "900", C["gold_lt"], HEAVY))
    return "".join(s)

def slogan_block(cx, top, big, small, lema_size=30, anchor="middle", max_w=900):
    b, yend, bl = stack(cx, top, [
        {"text": LEMA, "size": lema_size, "fill": C["gold_dk"], "family": BOLD, "weight": "800", "spacing": 1, "gap": 0, "max_w": max_w},
        {"text": "COMPROMETIDOS", "size": big, "fill": C["espresso"], "max_w": max_w, "gap": 12},
        {"text": "CON LOS CAFETEROS", "size": small, "fill": C["red"], "max_w": max_w, "gap": 10},
    ], anchor)
    # subrayado entre las dos lineas grandes
    uy = bl[1] + big * 0.16
    if anchor == "middle":
        ul = f'<rect x="{cx-max_w*0.2:.1f}" y="{uy:.1f}" width="{max_w*0.4:.1f}" height="{max(big*0.07,5):.1f}" rx="3" fill="url(#gGold)"/>'
    else:
        ul = f'<rect x="{cx:.1f}" y="{uy:.1f}" width="{max_w*0.42:.1f}" height="{max(big*0.07,5):.1f}" rx="3" fill="url(#gGold)"/>'
    return b + ul, yend

def svg(W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    minidom.parseString(content.encode("utf-8"))
    print(f"  OK {name} ({len(content)//1024} KB)")



# ======================================================================================
ACC = [C["green"], C["gold_dk"], C["red"], C["green_dk"], C["coffee"]]

def prop_card(body, x, y, w, h, i, t, desc, title_size=31, desc_size=21, desc_chars=58):
    col = ACC[i]
    body.append(f'<g filter="url(#soft)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#fff"/></g>')
    body.append(f'<rect x="{x}" y="{y}" width="15" height="{h}" rx="7" fill="{col}"/>')
    body.append(T(x + w - 22, y + h*0.5, str(i+1), h*0.62, None, "end", "900", col, HEAVY, 0, None, 0.15))
    body.append(check(x + 70, y + h*0.5, h*0.22, col))
    body.append(T(x + 116, y + h*0.36, t, title_size, w - 230, "start", "900", C["espresso"], HEAVY))
    for j, ln in enumerate(multiline(desc, desc_chars)[:2]):
        body.append(T(x + 116, y + h*0.58 + j*(desc_size + 7), ln, desc_size, w - 200, "start", "700", C["brown"], BOLD))


def afiche_principal():
    W, H = 1000, 1500
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    # mosaico de fotos (natural)
    b.append(photo("cafetales", 40, 132, 556, 444, d, 18))
    b.append(photo("nevado", 620, 132, 340, 212, d, 18))
    b.append(photo("cafeteros", 620, 364, 340, 212, d, 18))
    # etiquetas sutiles de las fotos
    b.append(f'<g filter="url(#soft)"><rect x="636" y="150" width="150" height="30" rx="15" fill="{C["espresso"]}" opacity="0.78"/></g>')
    b.append(T(711, 171, "NEVADO DEL RUIZ", 14, 130, "middle", "800", C["gold_lt"], BOLD, 1))
    b.append(f'<g filter="url(#soft)"><rect x="636" y="382" width="130" height="30" rx="15" fill="{C["espresso"]}" opacity="0.78"/></g>')
    b.append(T(701, 403, "NUESTROS CAFETEROS", 12, 116, "middle", "800", C["gold_lt"], BOLD, 1))
    b.append(topbar(W, 112))
    b.append(badge(126, 540, 80))
    sb, yend = slogan_block(W/2, 600, 90, 60)
    b.append(sb)
    b.append(candidate_card(285, 902, 300, "principal", d, 24, 19))
    b.append(candidate_card(715, 902, 300, "suplente", d, 24, 19))
    b.append(greenbar(W, 1374, 126, "VOTA PLANCHA 2", "TU VOTO, NUESTRO COMPROMISO"))
    b.append(bean(70, 1452, 22, 18)); b.append(bean(930, 1452, 22, -18))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("01-afiche-principal.svg", "".join(s))


def afiche_propuestas():
    W, H = 1000, 1500
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>', topbar(W, 110)]
    tt, _, _ = stack(60, 130, [{"text": "NUESTRAS", "size": 52, "fill": C["espresso"], "gap": 0},
                               {"text": "PROPUESTAS", "size": 52, "fill": C["red"], "gap": 8}], "start")
    b.append(tt)
    b.append(T(62, 322, LEMA, 22, 520, "start", "800", C["gold_dk"], BOLD, 1))
    b.append(badge(870, 205, 80))
    b.append(candidate_card(560, 140, 120, "principal", d, 18, 15, short=True))
    b.append(candidate_card(700, 140, 120, "suplente", d, 18, 15, short=True))
    y0, rh, gap = 360, 176, 10
    for i, (t, desc) in enumerate(PROPUESTAS):
        prop_card(b, 48, y0 + i*(rh+gap), 904, rh, i, t, desc, 30, 20, 56)
    # franja de fotos (cafetales, nevado, cafeteros)
    sy = 1294
    b.append(photo("cafetales", 48, sy, 290, 104, d, 12))
    b.append(photo("nevado", 355, sy, 290, 104, d, 12))
    b.append(photo("cafeteros", 662, sy, 290, 104, d, 12))
    b.append(greenbar(W, 1418, 82, "VOTA PLANCHA 2"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("02-afiche-propuestas.svg", "".join(s))


def pasacalle():
    W, H = 2400, 480
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>', topbar(W, 54)]
    b.append(badge(175, 280, 120))
    b.append(candidate_card(385, 90, 150, "principal", d, 19, 15, short=True))
    b.append(candidate_card(580, 90, 150, "suplente", d, 19, 15, short=True))
    sb, _ = slogan_block(880, 118, 86, 64, 30, "start", 1450)
    b.append(sb)
    b.append(goldbar(W, 442, 38, "PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("03-pasacalle.svg", "".join(s))


def valla():
    W, H = 2400, 1200
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    b.append(photo("cafetales", 1980, 400, 380, 210, d, 16))
    b.append(photo("nevado", 1980, 622, 380, 210, d, 16))
    b.append(photo("cafeteros", 1980, 844, 380, 210, d, 16))
    b.append(topbar(W, 110))
    b.append(candidate_card(380, 188, 420, "principal", d, 36, 28))
    b.append(candidate_card(870, 188, 420, "suplente", d, 36, 28))
    b.append(badge(2170, 252, 132))
    sb, _ = slogan_block(1180, 178, 96, 72, 40, "start", 760)
    b.append(sb)
    ejes = ["Vías para el campo", "Renovación del café", "Beneficiaderos",
            "Proyectos para la mujer cafetera", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 560 + i*82
        b.append(check(1208, ey, 30, ACC[i]))
        b.append(T(1260, ey + 12, e, 38, 700, "start", "800", C["espresso"], HEAVY))
    b.append(goldbar(W, 1090, 110, "VOTA PLANCHA 2   ·   COMPROMETIDOS CON LOS CAFETEROS"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("04-valla.svg", "".join(s))


def tarjeta_frente():
    W, H = 1050, 600
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>']
    # panel fotografico izquierdo (cafe)
    d.append('<clipPath id="cpTF"><rect x="0" y="0" width="372" height="600"/></clipPath>')
    b.append(f'<g clip-path="url(#cpTF)"><image href="{IMG["cafetales"]}" xlink:href="{IMG["cafetales"]}" x="0" y="0" width="372" height="600" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect x="0" y="0" width="372" height="600" fill="url(#gScrimL)"/></g>')
    b.append(badge(186, 230, 96))
    b.append(T(186, 430, "VOTA 2", 54, 300, "middle", "900", "#fff", HEAVY, 1, "soft"))
    b.append(T(186, 478, LEMA, 16, 320, "middle", "800", C["gold_lt"], BOLD, 1))
    # bloque derecho
    b.append(T(410, 74, ORG, 15, 600, "start", "800", C["green_dk"], BOLD, 1))
    sl, _, bl = stack(410, 82, [{"text": "COMPROMETIDOS", "size": 40, "fill": C["espresso"], "gap": 0, "max_w": 600},
                                {"text": "CON LOS CAFETEROS", "size": 29, "fill": C["red"], "gap": 8, "max_w": 600}], "start")
    b.append(sl)
    b.append(f'<rect x="412" y="{bl[0]+8:.0f}" width="250" height="5" rx="2" fill="url(#gGold)"/>')
    b.append(candidate_card(560, 200, 120, "principal", d, 18, 15, short=True))
    b.append(candidate_card(720, 200, 120, "suplente", d, 18, 15, short=True))
    b.append(bean(900, 250, 16, 20)); b.append(bean(940, 280, 14, -10))
    b.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="16" fill="none" stroke="{C["gold"]}" stroke-width="2"/>')
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("05a-tarjeta-frente.svg", "".join(s))


def tarjeta_respaldo():
    W, H = 1050, 600
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gBrown)"/>']
    b.append(T(60, 92, "NUESTRAS PROPUESTAS", 38, 700, "start", "900", C["gold_lt"], HEAVY, 1))
    ejes = ["Vías para el campo cafetero", "Incentivos a la renovación del café",
            "Mejores beneficiaderos", "Proyectos productivos para la mujer", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 158 + i*62
        b.append(check(86, ey, 21, C["gold"]))
        b.append(T(124, ey + 8, e, 25, 580, "start", "700", "#fff", BOLD))
    b.append(badge(885, 195, 102))
    b.append(photo("cafetales", 782, 318, 206, 132, d, 12, C["gold_lt"], 4))
    b.append(goldbar(W, 540, 60, "PLANCHA 2   ·   POR UNOS CAFETEROS PRÓSPEROS"))
    b.append(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="16" fill="none" stroke="{C["gold"]}" stroke-width="2"/>')
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("05b-tarjeta-respaldo.svg", "".join(s))


def redes_post():
    W = H = 1080
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>', topbar(W, 84)]
    sb, yend = slogan_block(W/2, 100, 72, 54, 28, "middle", 1000)
    b.append(sb)
    b.append(badge(958, 190, 76))
    b.append(candidate_card(300, 358, 280, "principal", d, 23, 18))
    b.append(candidate_card(780, 358, 280, "suplente", d, 23, 18))
    sy = 820
    b.append(photo("cafetales", 40, sy, 318, 110, d, 12))
    b.append(photo("nevado", 381, sy, 318, 110, d, 12))
    b.append(photo("cafeteros", 722, sy, 318, 110, d, 12))
    b.append(greenbar(W, 960, 120, "VOTA PLANCHA 2"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("06-redes-post.svg", "".join(s))


def redes_historia():
    W, H = 1080, 1920
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>', topbar(W, 110)]
    sb, yend = slogan_block(W/2, 150, 80, 60, 30, "middle", 1000)
    b.append(sb)
    b.append(badge(W/2, 502, 104))
    b.append(candidate_card(330, 620, 340, "principal", d, 27, 21))
    b.append(candidate_card(750, 620, 340, "suplente", d, 27, 21))
    sy = 1150
    b.append(photo("cafetales", 60, sy, 300, 168, d, 14))
    b.append(photo("nevado", 390, sy, 300, 168, d, 14))
    b.append(photo("cafeteros", 720, sy, 300, 168, d, 14))
    ejes = ["Vías para el campo", "Renovación del café", "Beneficiaderos",
            "Mujer cafetera", "Defensoría del cafetero"]
    for i, e in enumerate(ejes):
        ey = 1392 + i*64
        b.append(check(210, ey, 24, ACC[i]))
        b.append(T(256, ey + 10, e, 32, 700, "start", "800", C["espresso"], HEAVY))
    b.append(greenbar(W, 1740, 180, "VOTA PLANCHA 2", "TU VOTO, NUESTRO COMPROMISO"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("07-redes-historia.svg", "".join(s))


def volante():
    W, H = 1000, 1414
    d = []
    b = [f'<rect width="{W}" height="{H}" fill="url(#gSky)"/>', topbar(W, 96)]
    sb, yend = slogan_block(W/2, 110, 58, 44, 24, "middle", 900)
    b.append(sb)
    b.append(badge(W/2, 392, 66))
    b.append(candidate_card(300, 300, 180, "principal", d, 22, 16, short=True))
    b.append(candidate_card(700, 300, 180, "suplente", d, 22, 16, short=True))
    sy = 600
    b.append(photo("cafetales", 40, sy, 290, 92, d, 12))
    b.append(photo("nevado", 355, sy, 290, 92, d, 12))
    b.append(photo("cafeteros", 670, sy, 290, 92, d, 12))
    b.append(T(W/2, 748, "NUESTRAS PROPUESTAS", 32, 700, "middle", "900", C["espresso"], HEAVY, 1))
    y0, rh, gap = 768, 104, 8
    for i, (t, desc) in enumerate(PROPUESTAS):
        prop_card(b, 48, y0 + i*(rh+gap), 904, rh, i, t, desc, 25, 18, 60)
    b.append(greenbar(W, 1330, 84, "VOTA PLANCHA 2"))
    s = [svg(W, H), defs("".join(d))] + b + ["</svg>"]
    save("08-volante.svg", "".join(s))


def build_exporter():
    import re, json
    piezas = [("01-afiche-principal", "Afiche principal"), ("02-afiche-propuestas", "Afiche de propuestas"),
              ("03-pasacalle", "Pasacalle"), ("04-valla", "Valla publicitaria"),
              ("05a-tarjeta-frente", "Tarjeta — frente"), ("05b-tarjeta-respaldo", "Tarjeta — respaldo"),
              ("06-redes-post", "Post de redes"), ("07-redes-historia", "Historia de redes"), ("08-volante", "Volante")]
    items = []
    for fn, title in piezas:
        txt = open(os.path.join(OUT, fn + ".svg"), encoding="utf-8").read()
        m = re.search(r'width="(\d+)"\s+height="(\d+)"', txt)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (1000, 1000)
        items.append({"n": fn, "t": title, "w": w, "h": h, "b": base64.b64encode(txt.encode()).decode()})
    doc = '''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Exportar a PNG · Plancha 2</title><style>
:root{--esp:#241710;--brown:#4A2C1C;--gold:#E0A23B;--goldl:#F6D488;--red:#C32026;--green:#2F7D34;--cream:#FBF4E6}
*{box-sizing:border-box;margin:0;padding:0;font-family:Arial,Helvetica,sans-serif}body{background:var(--cream);color:var(--esp)}
header{background:linear-gradient(135deg,var(--brown),var(--esp));color:#fff;padding:28px 20px;text-align:center;border-bottom:7px solid var(--gold)}
header p{color:var(--goldl);margin-top:6px}
.bar{position:sticky;top:0;z-index:5;background:#fff;box-shadow:0 3px 12px rgba(0,0,0,.12);padding:14px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;justify-content:center}
select,button{font-size:15px;padding:10px 16px;border-radius:10px;border:2px solid var(--gold);background:#fff;font-weight:700;cursor:pointer}
button.all{background:var(--red);color:#fff;border-color:var(--red)}button.primary{background:var(--green);color:#fff;border-color:var(--green)}
.wrap{max-width:1150px;margin:0 auto;padding:24px 18px 70px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 7px 20px rgba(0,0,0,.12)}
.thumb{background:repeating-conic-gradient(#eee 0 25%,#f8f8f8 0 50%) 50%/20px 20px;padding:12px;display:flex;align-items:center;justify-content:center;min-height:160px}
.thumb img{max-width:100%;max-height:230px;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.2)}
.meta{padding:13px 15px}.meta h3{color:var(--brown);font-size:16px}.meta .d{font-size:12px;color:#8a7b66;margin:3px 0 9px}
.note{background:#fff;border-left:6px solid var(--gold);padding:15px 18px;border-radius:10px;margin:18px 0;line-height:1.5;font-size:14px}
#st{text-align:center;font-weight:700;color:var(--green)}</style></head><body>
<header><h1>Descargar la campaña en PNG</h1><p>Plancha 2 · Comprometidos con los Cafeteros</p></header>
<div class="bar"><label>Resolución:</label><select id="scale"><option value="1">1x</option><option value="2" selected>2x (imprenta)</option><option value="3">3x</option></select>
<button class="all" onclick="todas()">⬇ Descargar TODAS</button><span id="st"></span></div>
<div class="wrap"><div class="note"><b>Cómo usar:</b> elige resolución y pulsa <b>Descargar TODAS</b>, o el botón de cada pieza. Se guardan en tu carpeta de Descargas. Para vallas/pasacalles, entrega el <b>.svg</b> a la imprenta (vectorial, sin pérdida).</div>
<div class="grid" id="g"></div></div>
<script>const P=__DATA__;
function du(p){return 'data:image/svg+xml;base64,'+p.b}
function ld(p){return new Promise((ok,er)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>er(Error(p.n));i.src=du(p)})}
async function png(p,s){const im=await ld(p);const c=document.createElement('canvas');c.width=Math.round(p.w*s);c.height=Math.round(p.h*s);const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.imageSmoothingQuality='high';x.drawImage(im,0,0,c.width,c.height);return await new Promise((r,j)=>c.toBlob(b=>b?r(b):j(Error('blob')),'image/png'))}
function dl(b,n){const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=n;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),5000)}
async function una(i){const p=P[i],s=+scale.value;try{dl(await png(p,s),p.n+'.png')}catch(e){alert('Error '+p.n+': '+e.message)}}
async function todas(){const s=+scale.value;for(let i=0;i<P.length;i++){st.textContent='Generando '+(i+1)+'/'+P.length+'…';try{dl(await png(P[i],s),P[i].n+'.png')}catch(e){}await new Promise(r=>setTimeout(r,600))}st.textContent='¡Listo! Revisa Descargas.'}
P.forEach((p,i)=>{g.insertAdjacentHTML('beforeend',`<div class="card"><div class="thumb"><img src="${du(p)}"></div><div class="meta"><h3>${p.t}</h3><div class="d">${p.w}×${p.h}px (vector)</div><button class="primary" onclick="una(${i})">⬇ Descargar PNG</button></div></div>`)})</script></body></html>'''
    doc = doc.replace("__DATA__", json.dumps(items))
    with open(os.path.join(OUT, "exportar-png.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  OK exportar-png.html ({len(doc)//1024} KB)")


if __name__ == "__main__":
    print("Generando piezas...")
    afiche_principal(); afiche_propuestas(); pasacalle(); valla()
    tarjeta_frente(); tarjeta_respaldo(); redes_post(); redes_historia(); volante()
    build_exporter()
    print("Listo.")
