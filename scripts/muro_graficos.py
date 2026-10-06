"""Todas las imágenes del muro (SVG animados con CSS, sin JavaScript).

Cada función recibe datos de perfil.toml y devuelve el texto de un SVG.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from muro_svg import (
    OSCURO, PAREJA, SIN_MOVIMIENTO, TEMAS, Fuente, Lienzo, brillo, cuadros, degradado,
    esquinas, hexagono, icono, mezclar, num, rectangulos,
)

P = OSCURO

# ═════════════════════════════════════════════════════════════════════════════
#  CABECERA
# ═════════════════════════════════════════════════════════════════════════════

LOOP = 16  # segundos del ciclo rostro → AC → escudo
FASES = {  # (empieza a formarse, formada, empieza a irse, ya se fue), en fracción del ciclo
    "rostro": (0.00, 0.09, 0.35, 0.44),
    "ac": (0.38, 0.47, 0.61, 0.70),
    "escudo": (0.64, 0.73, 0.87, 0.96),
}

# Colores de las partículas (de oscuro a brillante)
COLORES_ROSTRO = ["#4A2BC4", "#6A3DF0", "#5B5CF6", "#3B82F6", "#22A6F2", "#22D3EE", "#7DF3FF", "#F0FDFF"]
COLORES_ROSTRO_ROSA = ["#9D2BC9", "#C43BE0", "#8B5CF6", "#3B82F6", "#22A6F2", "#22D3EE", "#7DF3FF", "#F0FDFF"]
COLORES_AC = ["#1E5FA8", "#2278C4", "#22A6E0", "#22D3EE", "#3EE6E0", "#8B9CFA", "#B9A6FF", "#F0F4FF"]
COLORES_ESCUDO = ["#3D2FA8", "#5B3FD6", "#7C5CF6", "#A06BFA", "#C46BF0", "#4FA5F7", "#9BE3FF", "#F2E9FF"]
OPACIDADES = [0.55, 0.62, 0.7, 0.78, 0.85, 0.92, 0.96, 1]


def pct(fraccion: float) -> str:
    return num(fraccion * 100, 2) + "%"


def keyframes_figura(nombre, fase, dx, dy, rot, esc_):
    a0, a1, v1, s1 = fase
    lejos = f"translate({num(dx)}px,{num(dy)}px) rotate({num(rot)}deg) scale({num(esc_)})"

    def parcial(t):
        return (f"translate({num(dx * t)}px,{num(dy * t)}px) rotate({num(rot * t)}deg) "
                f"scale({num(1 + (esc_ - 1) * t)})")

    c = []
    if a0 > 0:
        c.append(f"0%,{pct(a0)}{{transform:{lejos};opacity:0}}")
    else:
        c.append(f"0%{{transform:{lejos};opacity:.35}}")  # la nube aparece antes de cerrar el ciclo
    c.append(f"{pct((a0 + a1) / 2)}{{transform:{parcial(0.32)};opacity:.8}}")
    c.append(f"{pct(a1)},{pct(v1)}{{transform:none;opacity:1}}")
    c.append(f"{pct((v1 + s1) / 2)}{{transform:{parcial(0.42)};opacity:.65}}")
    if a0 > 0:
        c.append(f"{pct(s1)},100%{{transform:{lejos};opacity:0}}")
    else:
        c.append(f"{pct(s1)},{pct(0.93)}{{transform:{lejos};opacity:0}}100%{{transform:{lejos};opacity:.35}}")
    return f"@keyframes {nombre}{{{''.join(c)}}}"


def ciudad(rnd: random.Random, x0: float, x1: float, base: float, centro: float):
    """Siluetas de edificios con ventanas encendidas. Devuelve (edificios, ventanas por grupo)."""
    edificios, ventanas = [], {0: [], 1: [], 2: [], 3: []}
    colores_ventana = ["#22D3EE", "#8B5CF6", "#F5B544", "#E14FD0"]
    x = x0
    while x < x1:
        w = rnd.randint(16, 40)
        distancia = abs(x + w / 2 - centro)
        alto_max = 34 + min(1.0, distancia / 260) * 96
        h = rnd.randint(int(alto_max * 0.45), int(alto_max))
        edificios.append((x, base - h, w, h))
        for vy in range(int(base - h + 6), int(base - 6), 9):
            for vx in range(int(x + 4), int(x + w - 4), 7):
                if rnd.random() < 0.32:
                    color = rnd.choices(range(4), weights=[5, 3, 2, 1])[0]
                    ventanas[rnd.randrange(4)].append((vx, vy, 2.6, 3.6, colores_ventana[color]))
        x += w + rnd.randint(1, 5)
    return edificios, ventanas


def hero(perfil: dict, particulas: dict) -> str:
    per = perfil["persona"]
    W, H = 1200, 580
    lz = Lienzo(
        W, H,
        f"{per['nombre']} {per['apellido']} — {' · '.join(per['enfoque'])}",
        "Cabecera animada estilo 2050: terminal con whoami, aurora de colores, ciudad iluminada y un "
        "retrato holográfico de partículas, tomado de una foto real, que se transforma en el monograma "
        "AC y en un escudo con candado antes de volver al rostro.",
    )
    rnd = random.Random(2050)
    mx, my, mw, mh = 700, 60, 448, 470          # zona del retrato (esquinas HUD)
    ox, oy = 724, 72                             # origen de las partículas (400×420)
    cx, cy = ox + 200, oy + 214
    horizonte = 488

    css = [
        ".pg{animation-duration:%ss;animation-iteration-count:infinite;"
        "animation-timing-function:cubic-bezier(.55,0,.25,1);animation-fill-mode:both;"
        "transform-box:view-box;transform-origin:%spx %spx}" % (LOOP, cx, cy),
        ".ac,.es{opacity:0}",
        ".tk{animation:tk .01s steps(1) both}@keyframes tk{from{opacity:0}to{opacity:1}}",
        ".cur{animation:parp 1.2s steps(2,start) infinite}@keyframes parp{to{opacity:.15}}",
        ".en{animation:en .9s cubic-bezier(.2,.7,.2,1) both}",
        "@keyframes en{from{opacity:0;transform:translateY(12px)}}",
        ".au{animation:au ease-in-out infinite alternate}",
        "@keyframes au{from{transform:translateX(-46px)}to{transform:translateX(46px)}}",
        ".tw{animation:tw ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}",
        ".scan{animation:scan %ss linear infinite}" % num(LOOP / 3, 3),
        "@keyframes scan{0%%{transform:translateY(0)}80%%,100%%{transform:translateY(%spx)}}" % (mh + 90),
        ".bar{transform-box:fill-box;transform-origin:left;animation:bar %ss linear infinite}" % LOOP,
        "@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}",
        ".fl{animation-timing-function:ease-out;animation-iteration-count:infinite;animation-fill-mode:both}",
        ".orb{transform-box:fill-box;transform-origin:center;animation:orb linear infinite}",
        "@keyframes orb{to{transform:rotate(360deg)}}",
        ".mer{transform-box:fill-box;transform-origin:center;animation:mer 6s linear infinite}",
        "@keyframes mer{0%{transform:scaleX(1)}50%{transform:scaleX(-1)}100%{transform:scaleX(1)}}",
        ".pi{animation:pi 3.2s cubic-bezier(.5,0,1,1) infinite}",
        "@keyframes pi{from{transform:translateY(0);opacity:.9}to{transform:translateY(92px);opacity:0}}",
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}.scan,.fl,.f2,.f3,.pi{display:none}}",
    ]

    # ── Fondo: cielo, estrellas, aurora y brillos ──────────────────────────────
    lz.defs.append(
        degradado("hf", ["#040714", "#070C26", "#120A30"], 1, 1)
        + degradado("ga", ["#22D3EE", "#3B82F6", "#8B5CF6", "#E14FD0", "#E14FD0"], 1, 0, [0, .9, .9, .7, 0])
        + brillo("g1", "#22D3EE", .30, .07) + brillo("g2", "#8B5CF6", .30, .06) + brillo("g3", "#E14FD0", .22)
        + brillo("gh", "#38E1FF", .55, .12)
        + f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + f'<clipPath id="mc"><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="10"/></clipPath>'
        + '<linearGradient id="gs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22D3EE" stop-opacity="0"/>'
          '<stop offset=".85" stop-color="#22D3EE" stop-opacity=".07"/><stop offset="1" stop-color="#9BF6FF" stop-opacity=".38"/></linearGradient>'
        + degradado("gb", ["#121B48", "#080D26"], 0, 1)
        + degradado("gp", ["#0B1238", "#04071A"], 0, 1)
        + '<linearGradient id="gpl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset=".25" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>'
        + f'<mask id="mp"><rect x="560" y="{horizonte}" width="{W - 560}" height="{H - horizonte}" fill="url(#gpl)"/></mask>'
    )
    estrellas, estrellas_tw = [], []
    for i in range(80):
        sx, sy = rnd.uniform(20, W - 20), rnd.uniform(52, 420)
        r = rnd.choice([.6, .8, 1, 1.2, 1.5])
        color = rnd.choice(["#FFFFFF", "#9BE7FF", "#C4B5FD", "#F9A8D4"])
        if i < 12:
            dur = rnd.uniform(2.5, 5)
            estrellas_tw.append(f'<circle class="tw" cx="{num(sx)}" cy="{num(sy)}" r="{r + .4}" fill="{color}" '
                                f'style="animation-duration:{num(dur)}s;animation-delay:-{num(rnd.uniform(0, dur))}s"/>')
        else:
            estrellas.append(f'<circle cx="{num(sx)}" cy="{num(sy)}" r="{r}" fill="{color}" opacity="{num(rnd.uniform(.25, .8))}"/>')
    auroras = [
        ("M260 170C470 70 640 240 830 130S1090 40 1300 120L1300 186C1090 116 990 226 830 206S500 140 260 250Z", .26, 19, 0),
        ("M380 96C580 26 760 160 950 70S1150 16 1320 64L1320 104C1150 70 1050 146 950 128S620 82 380 156Z", .2, 26, -7),
        ("M120 300C380 210 600 330 860 250S1120 200 1300 260L1300 292C1120 246 1000 306 860 300S420 262 120 340Z", .14, 31, -15),
    ]
    capa_aurora = "".join(
        f'<path class="au" d="{d}" fill="url(#ga)" opacity="{op}" style="animation-duration:{dur}s;animation-delay:{dl}s"/>'
        for d, op, dur, dl in auroras)
    lz.add(
        f'<g clip-path="url(#hc)"><rect width="{W}" height="{H}" fill="url(#hf)"/>',
        "".join(estrellas), "".join(estrellas_tw), capa_aurora,
        f'<circle cx="{cx}" cy="{cy - 10}" r="300" fill="url(#g1)"/>',
        f'<circle cx="140" cy="{H - 20}" r="330" fill="url(#g2)"/>',
        f'<circle cx="{W - 80}" cy="60" r="260" fill="url(#g3)"/>',
    )

    # ── Horizonte: piso en perspectiva y ciudad ───────────────────────────────
    vx = cx
    piso = [f'<rect x="560" y="{horizonte}" width="{W - 560}" height="{H - horizonte}" fill="url(#gp)"/>']
    lineas = []
    for i in range(-14, 15):
        xb = vx + i * 58
        lineas.append(f"M{num(vx + i * 4)} {horizonte}L{num(xb)} {H}")
    for d in (4, 10, 18, 29, 43, 61, 84):
        lineas.append(f"M560 {horizonte + d}H{W}")
    piso.append(f'<path d="{"".join(lineas)}" stroke="#3B82F6" stroke-opacity=".38" stroke-width="1" fill="none"/>')
    piso.append(f'<rect class="pi" x="560" y="{horizonte}" width="{W - 560}" height="1.6" fill="#7DF3FF"/>')
    lz.add(f'<g mask="url(#mp)">{"".join(piso)}</g>')
    lz.add(f'<ellipse cx="{cx}" cy="{horizonte}" rx="400" ry="70" fill="url(#gh)"/>')
    edificios, ventanas = ciudad(rnd, 600, W + 10, horizonte, cx)
    lz.add(f'<path d="{rectangulos(edificios)}" fill="url(#gb)"/>')
    techos = "".join(f"M{x} {num(y + .5)}h{w}" for x, y, w, h in edificios)
    lz.add(f'<path d="{techos}" stroke="#8B5CF6" stroke-opacity=".55" stroke-width="1"/>')
    for grupo, lista in ventanas.items():
        por_color: dict[str, list] = {}
        for vx_, vy_, vw, vh, color in lista:
            por_color.setdefault(color, []).append((vx_, vy_, vw, vh))
        trazos = "".join(f'<path d="{rectangulos(r)}" fill="{c}" fill-opacity=".85"/>' for c, r in por_color.items())
        if grupo == 0:
            lz.add(f"<g>{trazos}</g>")
        else:
            dur = 3 + grupo * 1.7
            lz.add(f'<g class="tw" style="animation-duration:{num(dur)}s;animation-delay:-{grupo}s">{trazos}</g>')
    lz.add(f'<path d="M560 {horizonte}.5H{W}" stroke="#7DF3FF" stroke-opacity=".55"/>', "</g>")

    # ── Marco general ─────────────────────────────────────────────────────────
    lz.defs.append(degradado("gm", ["#22D3EE", "#8B5CF6", "#E14FD0"], 1, 0))
    lz.add(
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#gm)" stroke-opacity=".55" stroke-width="1.5"/>',
        f'<circle cx="30" cy="24" r="5.5" fill="#F87171" fill-opacity=".9"/><circle cx="50" cy="24" r="5.5" fill="#FBBF24" fill-opacity=".9"/>'
        f'<circle cx="70" cy="24" r="5.5" fill="#34D399" fill-opacity=".9"/>',
        lz.texto("mono", f"{per['usuario']} / README.md", 94, 29, 13, P["tenue"])[0],
        lz.texto("mono", "SYS.2050 // EN LÍNEA", W - 28, 29, 12, P["cian"], 1.5, "end")[0],
        f'<path d="M1 47.5H{W - 1}" stroke="#1D2A55"/>',
    )

    # ── Texto: terminal, nombre y enfoque ─────────────────────────────────────
    x0 = 58
    s1, w1 = lz.texto("mono", "alfonso@systems", x0, 106, 19, P["verde"])
    s2, w2 = lz.texto("mono", ":~$", x0 + w1, 106, 19, P["suave"])
    s3, w3 = lz.texto("mono", " whoami", x0 + w1 + w2, 106, 19, P["texto"], tipeo=(0.55, 0.15))
    lz.add(s1, s2, s3, f'<rect class="cur" x="{num(x0 + w1 + w2 + w3 + 3)}" y="90" width="11" height="20" fill="{P["verde"]}"/>')

    t_nombre, _ = lz.texto("titulo", per["nombre"], x0 - 3, 196, 80, P["texto"])
    t_apellido, w_ap = lz.texto("titulo", per["apellido"], x0 - 3, 280, 80, "#fff")
    lz.defs.append(
        f'<linearGradient id="gn" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{num(x0 + w_ap)}" y2="0">'
        f'<stop offset="0" stop-color="#22D3EE"/><stop offset=".4" stop-color="#3B82F6"/>'
        f'<stop offset=".75" stop-color="#8B5CF6"/><stop offset="1" stop-color="#E14FD0"/></linearGradient>'
        f'<mask id="mn" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{t_apellido}</mask>'
        + brillo("gtx", "#3B82F6", .35)
    )
    lz.add(
        f'<ellipse cx="{num(x0 + w_ap / 2)}" cy="252" rx="{num(w_ap * .7)}" ry="70" fill="url(#gtx)"/>',
        f'<g class="en" style="animation-delay:1.45s">{t_nombre}</g>',
        f'<g class="en" style="animation-delay:1.6s"><rect x="{x0 - 6}" y="202" width="{num(w_ap + 12)}" '
        f'height="98" fill="url(#gn)" mask="url(#mn)"/></g>',
    )

    # Colores con intención: ciberseguridad esmeralda, sistemas y redes cian, administración ámbar
    colores_enfoque = [P["esmeralda"], P["cian"], P["ambar"]]
    enfoque = per["enfoque"]
    partes, x = [], x0
    for i, area in enumerate(enfoque[:2]):
        s, w = lz.texto("texto", area, x, 336, 27, colores_enfoque[i])
        partes.append(s)
        x += w
        if i == 0:
            s, w = lz.texto("texto", "  ·  ", x, 336, 27, P["tenue"])
            partes.append(s)
            x += w
    partes.append(lz.texto("texto", enfoque[2], x0, 372, 27, colores_enfoque[2])[0])
    lz.add(f'<g class="en" style="animation-delay:1.8s">{"".join(partes)}</g>')

    chips, x = [], x0
    for texto, color in zip(per["complementos"], [P["cian"], "#A78BFA", "#C084FC"]):
        ancho = Fuente.de("mono").ancho(texto, 13.5) + 26
        chips.append(f'<rect x="{num(x)}" y="392" width="{num(ancho)}" height="28" rx="14" fill="{color}" '
                     f'fill-opacity=".12" stroke="{color}" stroke-opacity=".7"/>')
        chips.append(lz.texto("mono", texto, x + 13, 410.5, 13.5, color)[0])
        x += ancho + 10
    lz.add(f'<g class="en" style="animation-delay:1.95s">{"".join(chips)}</g>')

    filas = [("rol", per["titulo"]), ("base", per["ubicacion"]), ("idiomas", per["idiomas"])]
    kv = [f'<path d="M{x0} 444.5H600" stroke="#1D2A55"/>']
    for i, (clave, valor) in enumerate(filas):
        yy = 472 + i * 24
        kv.append(lz.texto("mono", clave, x0, yy, 13.5, P["tenue"])[0])
        kv.append(lz.texto("mono", valor, x0 + 92, yy, 13.5, P["suave"])[0])
    lz.add(f'<g class="en" style="animation-delay:2.1s">{"".join(kv)}</g>')
    tag = "IDEAS  >  SISTEMAS  >  SEGURIDAD  >  SOLUCIONES"
    lz.add(lz.texto("mono", tag, x0, 560, 11.5, "#5EC8E6", 1.6)[0])

    # ── HUD del retrato: esquinas, globo, etiquetas, órbitas ──────────────────
    lz.add(esquinas(mx, my, mw, mh, 22, P["cian"], 2, .95))
    lz.add(lz.texto("mono", "HOLO.SCAN // retrato de partículas", mx + 18, my + 24, 11, "#7C8DBD")[0])
    gx, gy, gr = mx + mw - 54, my + 58, 34
    globo = [f'<circle cx="{gx}" cy="{gy}" r="{gr + 10}" fill="url(#g1)"/>',
             f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="#0A1A3A" fill-opacity=".6" stroke="#22D3EE" stroke-width="1.4"/>']
    for k in (-.55, 0, .55):
        ry = gr * math.sqrt(1 - k * k)
        globo.append(f'<ellipse cx="{gx}" cy="{num(gy + gr * k)}" rx="{num(ry)}" ry="{num(ry * .22)}" fill="none" stroke="#3B82F6" stroke-opacity=".8"/>')
    for i in range(3):
        globo.append(f'<ellipse class="mer" cx="{gx}" cy="{gy}" rx="{num(gr * .75)}" ry="{gr}" fill="none" '
                     f'stroke="#8B5CF6" stroke-opacity=".9" style="animation-delay:-{i * 2}s"/>')
    globo.append(f'<path d="M{gx - gr} {gy}h{gr * 2}" stroke="#22D3EE" stroke-opacity=".7"/>')
    lz.add("".join(globo))
    lz.defs.append(degradado("gor", ["#22D3EE", "#8B5CF6", "#E14FD0"], 1, 0))
    orbitas = []
    for rx, k, rot, dur, sentido in ((205, .26, -14, 24, 1), (178, .2, 16, 32, -1)):
        orbitas.append(
            f'<g transform="translate({cx} {cy - 18}) rotate({rot}) scale(1 {k})">'
            f'<circle r="{rx}" fill="none" stroke="url(#gor)" stroke-opacity=".35" stroke-width="{num(1.4 / k)}"/>'
            f'<circle class="orb" r="{rx}" fill="none" stroke="#7DF3FF" stroke-opacity=".75" stroke-width="{num(2.6 / k)}" '
            f'stroke-dasharray="60 {num(2 * math.pi * rx - 60)}" style="animation-duration:{dur}s;'
            f'animation-direction:{"normal" if sentido > 0 else "reverse"}"/>'
            f'<circle class="orb" r="{rx}" fill="none" stroke="#E14FD0" stroke-width="{num(2.4 / k)}" '
            f'stroke-dasharray="22 {num(2 * math.pi * rx - 22)}" stroke-dashoffset="{num(math.pi * rx)}" '
            f'style="animation-duration:{dur}s;animation-direction:{"normal" if sentido > 0 else "reverse"}"/></g>')
    lz.add("".join(orbitas))

    # Etiquetas de fase y barra de progreso
    nombres_fase = [("01 · ROSTRO", "rostro"), ("02 · IDENTIDAD AC", "ac"), ("03 · SEGURIDAD", "escudo")]
    for i, (texto, figura) in enumerate(nombres_fase, start=1):
        a0, a1, v1, s1_ = FASES[figura]
        ini, fin = (a0 + a1) / 2, (v1 + s1_) / 2
        if ini <= 0:
            c = f"0%,{pct(fin - .01)}{{opacity:1}}{pct(fin)},100%{{opacity:0}}"
        else:
            c = f"0%,{pct(ini - .01)}{{opacity:0}}{pct(ini)},{pct(fin - .01)}{{opacity:1}}{pct(fin)},100%{{opacity:0}}"
        css.append(f"@keyframes fa{i}{{{c}}}.f{i}{{animation:fa{i} {LOOP}s linear infinite}}")
        lz.add(f'<g class="f{i}">' + lz.texto("monob", texto, mx + 18, my + mh - 26, 11, P["cian"], 1)[0] + "</g>")
    pista_y = my + mh - 12
    lz.add(
        f'<path d="M{mx + 18} {pista_y}H{mx + mw - 18}" stroke="#1D2A55" stroke-width="2"/>',
        f'<rect class="bar" x="{mx + 18}" y="{pista_y - 1}" width="{mw - 36}" height="2" fill="url(#gor)"/>',
    )

    # ── Partículas ────────────────────────────────────────────────────────────
    clases = {"rostro": "ro", "ac": "ac", "escudo": "es"}
    capas = []
    for figura in ("rostro", "ac", "escudo"):
        puntos = particulas[figura]
        n_grupos = max(p[5] for p in puntos) + 1
        for g in range(n_grupos):
            colores = {"ac": COLORES_AC, "escudo": COLORES_ESCUDO}.get(
                figura, COLORES_ROSTRO_ROSA if g % 6 == 0 else COLORES_ROSTRO)
            ang = rnd.uniform(0, 2 * math.pi)
            dist = rnd.uniform(70, 200)
            dx, dy = math.cos(ang) * dist, math.sin(ang) * dist * 0.8
            rot = rnd.uniform(-28, 28)
            escala = rnd.uniform(0.55, 1.45)
            nombre = f"{clases[figura]}{g}"
            css.append(keyframes_figura(nombre, FASES[figura], dx, dy, rot, escala))
            retraso = -rnd.uniform(0, 0.55)
            trazos = []
            for c in range(8):
                pts = [(ox + p[0], oy + p[1], p[2]) for p in puntos if p[5] == g and p[3] == c]
                if pts:
                    trazos.append(f'<path fill="{colores[c]}" fill-opacity="{OPACIDADES[c]}" d="{cuadros(pts)}"/>')
            capas.append(f'<g class="pg {clases[figura]}" style="animation-name:{nombre};'
                         f'animation-delay:{num(retraso)}s">' + "".join(trazos) + "</g>")

    flotantes = []
    for i in range(46):
        fx = ox + rnd.uniform(220, 395)
        fy = oy + rnd.uniform(30, 330)
        s = rnd.choice([2.5, 3, 3.5, 4, 5, 6])
        color = rnd.choice(["#22D3EE", "#7DF3FF", "#3B82F6", "#8B5CF6", "#A78BFA", "#E14FD0", "#F472D0"])
        dur = rnd.uniform(4.5, 8)
        dx, dy = rnd.uniform(25, 80), rnd.uniform(-55, 10)
        nombre = f"fl{i}"
        css.append(f"@keyframes {nombre}{{0%{{transform:translate(0,0);opacity:0}}20%{{opacity:.95}}"
                   f"100%{{transform:translate({num(dx)}px,{num(dy)}px);opacity:0}}}}")
        flotantes.append(f'<rect class="fl" x="{num(fx, 1)}" y="{num(fy, 1)}" width="{s}" height="{s}" '
                         f'fill="{color}" style="animation-name:{nombre};animation-duration:{num(dur)}s;'
                         f'animation-delay:-{num(rnd.uniform(0, dur))}s"/>')
    lz.add(
        '<g clip-path="url(#mc)">',
        "".join(capas), "".join(flotantes),
        f'<rect class="scan" x="{mx}" y="{my - 90}" width="{mw}" height="90" fill="url(#gs)"/>',
        "</g>",
    )
    lz.estilos.append("".join(css))
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  SEÑAL (cuadrícula decorativa)
# ═════════════════════════════════════════════════════════════════════════════

def senal() -> str:
    W, H = 1200, 168
    lz = Lienzo(W, H, "Concepto de actividad (decorativo)",
                "Cuadrícula animada de colores con una onda luminosa. Es decorativa: no representa actividad real.")
    rnd = random.Random(7)
    cols, filas, celda, hueco = 62, 6, 13, 4
    x0, y0 = 40, 50
    gama = ["#22D3EE", "#3B82F6", "#8B5CF6", "#E14FD0"]
    lz.defs.append(
        f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        + degradado("sf", ["#060B22", "#0B0A2C"], 1, 1)
        + degradado("so", ["#22D3EE", "#3B82F6", "#8B5CF6", "#E14FD0"], 1, 0)
        + '<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    )
    base, encendidas, destellos = [], {}, []
    for c in range(cols):
        t = c / (cols - 1)
        tramo = min(len(gama) - 2, int(t * (len(gama) - 1)))
        color_col = mezclar(gama[tramo], gama[tramo + 1], t * (len(gama) - 1) - tramo)
        for f in range(filas):
            x, y = x0 + c * (celda + hueco), y0 + f * (celda + hueco)
            r = rnd.random()
            if r < 0.30:
                op = rnd.choice([.35, .55, .8, 1])
                encendidas.setdefault((color_col, op), []).append((x, y, celda, celda))
            else:
                base.append((x, y, celda, celda))
            if rnd.random() < 0.05:
                dur = rnd.uniform(2.6, 6)
                destellos.append(f'<rect class="tw" x="{x}" y="{y}" width="{celda}" height="{celda}" fill="{color_col}" '
                                 f'style="animation-duration:{num(dur)}s;animation-delay:-{num(rnd.uniform(0, dur))}s"/>')
    mascara = rectangulos(base + [r for lista in encendidas.values() for r in lista])
    lz.defs.append(f'<mask id="sm"><path d="{mascara}" fill="#fff"/></mask>')
    lz.add(
        f'<g clip-path="url(#sc)"><rect width="{W}" height="{H}" fill="url(#sf)"/>',
        f'<path d="{rectangulos(base)}" fill="#111B44"/>',
        "".join(f'<path d="{rectangulos(r)}" fill="{c}" fill-opacity="{o}"/>' for (c, o), r in encendidas.items()),
        "".join(destellos),
        f'<g mask="url(#sm)"><rect class="sw" x="-300" y="0" width="300" height="{H}" fill="url(#sw)"/></g>',
    )
    # onda luminosa
    puntos = []
    for i in range(0, 121):
        x = x0 + i * (cols * (celda + hueco) - hueco) / 120
        y = y0 + 50 + math.sin(i / 120 * math.pi * 4.2) * 26 + math.sin(i / 120 * math.pi * 11) * 6
        puntos.append(f"{num(x)} {num(y)}")
    onda = "M" + "L".join(puntos)
    lz.add(f'<path d="{onda}" fill="none" stroke="url(#so)" stroke-width="2.4" stroke-opacity=".9"/>',
           f'<path class="wv" d="{onda}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" '
           f'stroke-dasharray="60 1400" pathLength="1460"/>')
    lz.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="url(#so)" stroke-opacity=".5" stroke-width="1.5"/></g>')
    lz.add(lz.texto("monob", ">_ CONCEPTO DE ACTIVIDAD", 40, 32, 13, P["cian"], 1.5)[0],
           lz.texto("mono", "decorativo · sin datos reales", W - 40, 32, 12, P["tenue"], ancla="end")[0])
    lz.estilos.append(
        ".sw{animation:sw 7s cubic-bezier(.4,0,.2,1) infinite}"
        "@keyframes sw{0%{transform:translateX(0)}70%,100%{transform:translateX(1500px)}}"
        ".tw{animation-name:tw;animation-iteration-count:infinite;animation-timing-function:ease-in-out}"
        "@keyframes tw{0%,100%{opacity:0}50%{opacity:1}}"
        ".wv{animation:wv 5s linear infinite}@keyframes wv{from{stroke-dashoffset:0}to{stroke-dashoffset:-1460}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  PIEZAS COMUNES: pedestal holográfico, cubos flotantes y chip de estado
#  (todo lo que sigue es nuevo; la cabecera y la cuadrícula de arriba están protegidas)
# ═════════════════════════════════════════════════════════════════════════════

# Estado real de un proyecto → color del chip
ESTADOS = {
    "disponible": "esmeralda", "laboratorio": "cian", "beta": "violeta",
    "demo": "ambar", "desarrollo": "coral",
}

CSS_COMUN = (
    ".fz{animation:fz ease-in-out infinite alternate}@keyframes fz{from{transform:translateY(0)}to{transform:translateY(-8px)}}"
    ".edot{transform-box:fill-box;transform-origin:center;animation:edot 2.4s ease-in-out infinite}"
    "@keyframes edot{0%,100%{opacity:.55;transform:scale(.8)}50%{opacity:1;transform:scale(1.15)}}"
    ".pdr{animation:pdr 14s linear infinite}@keyframes pdr{to{stroke-dashoffset:-400}}"
)


def pedestal(lz: Lienzo, gid: str, cx: float, cy: float, rx: float, c1: str, c2: str) -> str:
    """Plataforma holográfica: anillos elípticos, brillo y un haz de luz hacia arriba."""
    ry = rx * 0.24
    lz.defs.append(
        brillo(f"{gid}g", c1, .5, .12)
        + f'<linearGradient id="{gid}h" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity=".22"/>'
          f'<stop offset="1" stop-color="{c1}" stop-opacity="0"/></linearGradient>'
    )
    return (
        f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx * 1.35)}" ry="{num(ry * 2)}" fill="url(#{gid}g)"/>'
        f'<path d="M{num(cx - rx * .62)} {num(cy)}L{num(cx - rx * .42)} {num(cy - 150)}H{num(cx + rx * .42)}L{num(cx + rx * .62)} {num(cy)}Z" fill="url(#{gid}h)"/>'
        f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx * 1.12)}" ry="{num(ry * 1.12)}" fill="none" stroke="{c1}" stroke-opacity=".3"/>'
        f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx)}" ry="{num(ry)}" fill="{c1}" fill-opacity=".08" stroke="{c1}" stroke-width="2"/>'
        f'<ellipse class="pdr" cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx * .74)}" ry="{num(ry * .74)}" fill="none" '
        f'stroke="{c2}" stroke-width="1.6" stroke-dasharray="10 8"/>'
    )


def cubo(x: float, y: float, s: float, c: str) -> str:
    """Cubo isométrico translúcido; (x, y) es el vértice superior."""
    k = s * 0.866
    arriba = f"M{num(x)} {num(y)}l{num(k)} {num(s / 2)}l{num(-k)} {num(s / 2)}l{num(-k)} {num(-s / 2)}Z"
    izq = f"M{num(x - k)} {num(y + s / 2)}l{num(k)} {num(s / 2)}v{num(s)}l{num(-k)} {num(-s / 2)}Z"
    der = f"M{num(x)} {num(y + s)}l{num(k)} {num(-s / 2)}v{num(s)}l{num(-k)} {num(s / 2)}Z"
    claro = mezclar(c, "#FFFFFF", .35)
    return (f'<path d="{arriba}" fill="{claro}" fill-opacity=".75" stroke="{claro}" stroke-width=".8"/>'
            f'<path d="{izq}" fill="{c}" fill-opacity=".45" stroke="{claro}" stroke-opacity=".6" stroke-width=".8"/>'
            f'<path d="{der}" fill="{c}" fill-opacity=".22" stroke="{claro}" stroke-opacity=".6" stroke-width=".8"/>')


def cubos_flotantes(rnd: random.Random, posiciones, colores) -> str:
    partes = []
    for (x, y, s), c in zip(posiciones, colores):
        dur = rnd.uniform(3.4, 5.8)
        partes.append(f'<g class="fz" style="animation-duration:{num(dur)}s;animation-delay:-{num(rnd.uniform(0, dur))}s">'
                      f'{cubo(x, y, s, c)}</g>')
    return "".join(partes)


def chip_estado(lz: Lienzo, estado: str, detalle: str, x_der: float, y: float, tam: float = 12) -> str:
    color = P[ESTADOS.get(estado, "cian")]
    texto = estado.upper() + (f"  ·  {detalle}" if detalle else "")
    ancho = Fuente.de("monob").ancho(texto, tam, .5)
    x = x_der - ancho - 42
    return (f'<rect x="{num(x)}" y="{y}" width="{num(ancho + 42)}" height="28" rx="14" fill="{color}" fill-opacity=".16" stroke="{color}"/>'
            f'<circle class="edot" cx="{num(x + 16)}" cy="{y + 14}" r="4.5" fill="{color}"/>'
            + lz.texto("monob", texto, x + 28, y + 18.5, tam, mezclar(color, "#FFFFFF", .35), .5)[0])


# ── Texto neón: copia desenfocada que pulsa suavemente + texto nítido en tono claro ──

NEON_FILTRO = ('<filter id="nb" x="-8%" y="-80%" width="116%" height="260%" color-interpolation-filters="sRGB">'
               '<feGaussianBlur in="SourceGraphic" stdDeviation="1.6" result="a"/>'
               '<feGaussianBlur in="SourceGraphic" stdDeviation="5" result="b"/>'
               '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="a"/></feMerge></filter>')
NEON_CSS = ".ng{animation:ng 3.8s ease-in-out infinite}@keyframes ng{0%,100%{opacity:.6}50%{opacity:1}}"


def tono(color: str, t: float = .55) -> str:
    """Versión clara del color (para letras sobre fondo oscuro)."""
    return mezclar(color, "#FFFFFF", t)


def neon(lz: Lienzo, clave: str, texto: str, x: float, y: float, tam: float, color: str,
         ancla: str = "start", espaciado: float = 0.0, retraso: float = 0.0, pulso: bool = True) -> tuple[str, float]:
    if NEON_FILTRO not in lz.defs:
        lz.defs.append(NEON_FILTRO)
        lz.estilos.append(NEON_CSS)
    brillo_, ancho = lz.texto(clave, texto, x, y, tam, color, espaciado, ancla)
    nitido, _ = lz.texto(clave, texto, x, y, tam, tono(color), espaciado, ancla)
    clase = f' class="ng" style="animation-delay:-{num(retraso)}s"' if pulso else ' opacity=".7"'
    return f'<g filter="url(#nb)"{clase}>{brillo_}</g>{nitido}', ancho


def envolver(texto: str, clave: str, tam: float, ancho: float) -> list[str]:
    """Parte un texto en líneas que caben en `ancho` píxeles."""
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if Fuente.de(clave).ancho(prueba, tam) <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


# ═════════════════════════════════════════════════════════════════════════════
#  ENCABEZADOS DE SECCIÓN
# ═════════════════════════════════════════════════════════════════════════════

def encabezado(titulo: str, nota: str, icono_nombre: str, acento: str, acento2: str, tema: str) -> tuple[str, int]:
    T = TEMAS[tema]
    c1, c2 = P[acento], P[acento2]
    tam, espaciado = 22, 2.4
    ancho_titulo = Fuente.de("titulo").ancho(titulo.upper(), tam, espaciado)
    largo = 150
    x_t = 58
    x1 = x_t + ancho_titulo + 18
    W, H = int(x1 + largo + 14), 52
    lz = Lienzo(W, H, titulo, nota)
    lz.defs.append(degradado("eb", [c1, c2], 1, 1) + degradado("el", [c1, c2], 1, 0)
                   + f'<clipPath id="ec"><rect x="{num(x1)}" y="20" width="{largo}" height="10"/></clipPath>')
    lz.add(
        f'<rect x="2" y="6" width="40" height="40" rx="11" fill="url(#eb)"/>',
        f'<rect x="2" y="6" width="40" height="40" rx="11" fill="none" stroke="#fff" stroke-opacity=".35"/>',
        icono(icono_nombre, 10, 14, 24, "#fff", 2.1),
        (neon(lz, "titulo", titulo.upper(), x_t, 34, tam, c1, espaciado=espaciado)[0] if tema == "oscuro"
         else lz.texto("titulo", titulo.upper(), x_t, 34, tam, T["texto"], espaciado=espaciado)[0]),
        f'<rect x="{num(x1)}" y="24" width="{largo}" height="3" rx="1.5" fill="url(#el)" fill-opacity=".45"/>',
        f'<g clip-path="url(#ec)"><rect class="mv" x="{num(x1 - 50)}" y="24" width="50" height="3" fill="#fff" fill-opacity=".9"/></g>',
        f'<rect x="{num(x1 + largo + 4)}" y="21.5" width="8" height="8" rx="2" fill="{c2}"/>',
    )
    lz.estilos.append(
        ".mv{animation:mv 5s cubic-bezier(.5,0,.3,1) infinite}"
        f"@keyframes mv{{0%{{transform:translateX(0)}}60%,100%{{transform:translateX({largo + 50}px)}}}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar(), W


# ═════════════════════════════════════════════════════════════════════════════
#  ÁREAS (cuatro tarjetas del mismo tamaño)
# ═════════════════════════════════════════════════════════════════════════════

def ilustracion_area(tipo: str, x: float, y: float, c1: str, c2: str) -> str:
    """Ilustración en una zona de unos 170×140 con esquina superior izquierda en (x, y)."""
    p = []
    if tipo == "escudo":
        for k in range(2):
            rx = x + 4 + k * 32
            p.append(f'<rect x="{rx}" y="{y + 44 + k * 6}" width="26" height="{88 - k * 6}" rx="3" fill="#0B1538" stroke="{c1}" stroke-opacity=".45"/>')
            for j in range(5):
                yy = y + 52 + k * 6 + j * 15
                p.append(f'<rect x="{rx + 4}" y="{yy}" width="18" height="3" rx="1.5" fill="{c1}" fill-opacity=".35"/>')
                p.append(f'<circle class="led" cx="{rx + 20}" cy="{yy + 8}" r="1.6" fill="{c1}" style="animation-delay:-{(j + k) * .4}s"/>')
        sx, sy = x + 118, y + 18
        p.append(f'<path d="M{sx} {sy}l42 17v35c0 31-19 50-42 60-23-10-42-29-42-60V{sy + 17}Z" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-width="2.6"/>')
        p.append(f'<rect x="{sx - 15}" y="{sy + 56}" width="30" height="24" rx="4" fill="{c1}"/>')
        p.append(f'<path d="M{sx - 9} {sy + 56}v-8a9 9 0 0 1 18 0v8" fill="none" stroke="{c1}" stroke-width="3.2"/>')
        p.append(f'<circle cx="{sx}" cy="{sy + 66}" r="3.2" fill="#0B1538"/>')
    elif tipo == "red":
        for k in range(2):
            rx = x + 6 + k * 36
            p.append(f'<rect x="{rx}" y="{y + 30}" width="30" height="104" rx="3" fill="#0B1538" stroke="{c1}" stroke-opacity=".5"/>')
            for j in range(7):
                yy = y + 38 + j * 13.5
                p.append(f'<rect x="{rx + 4}" y="{yy}" width="16" height="3" rx="1.5" fill="{c2}" fill-opacity=".6"/>')
                p.append(f'<circle class="led" cx="{rx + 24}" cy="{yy + 1.5}" r="1.6" fill="{c1}" style="animation-delay:-{(j * 3 + k) * .3}s"/>')
        nodos = [(x + 124, y + 28), (x + 98, y + 80), (x + 152, y + 84), (x + 126, y + 126)]
        lineas = "".join(f"M{a[0]} {a[1]}L{b[0]} {b[1]}" for a, b in
                         [(nodos[0], nodos[1]), (nodos[0], nodos[2]), (nodos[1], nodos[2]), (nodos[1], nodos[3]), (nodos[2], nodos[3])])
        p.append(f'<path d="{lineas}" stroke="{c1}" stroke-width="2" stroke-opacity=".8"/>')
        for nx, ny in nodos:
            p.append(f'<circle cx="{nx}" cy="{ny}" r="9" fill="#0B1538" stroke="{c1}" stroke-width="2.4"/><circle cx="{nx}" cy="{ny}" r="3.4" fill="{c2}"/>')
    elif tipo == "gestion":
        cxg, cyg = x + 50, y + 64
        dientes = []
        for k in range(8):
            a = math.radians(k * 45)
            dientes.append(f"M{num(cxg + 25 * math.cos(a))} {num(cyg + 25 * math.sin(a))}L{num(cxg + 36 * math.cos(a))} {num(cyg + 36 * math.sin(a))}")
        p.append(f'<g class="gir" style="transform-origin:{num(cxg)}px {num(cyg)}px">'
                 f'<circle cx="{cxg}" cy="{cyg}" r="26" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-width="3"/>'
                 f'<path d="{"".join(dientes)}" stroke="{c1}" stroke-width="8" stroke-linecap="round"/>'
                 f'<circle cx="{cxg}" cy="{cyg}" r="9" fill="none" stroke="{c1}" stroke-width="3"/></g>')
        for k, h in enumerate([28, 46, 64, 88]):
            bx = x + 100 + k * 16
            p.append(f'<rect class="bc" x="{bx}" y="{y + 134 - h}" width="11" height="{h}" rx="2" fill="{c1 if k == 3 else c2}" '
                     f'fill-opacity="{.95 if k == 3 else .6}" style="animation-delay:-{k * .5}s"/>')
        p.append(f'<path d="M{x + 94} {y + 134}h74" stroke="{c1}" stroke-opacity=".6" stroke-width="1.5"/>')
    else:  # código e IA
        p.append(f'<rect x="{x + 2}" y="{y + 26}" width="112" height="96" rx="9" fill="#0B1538" stroke="{c1}" stroke-opacity=".6"/>')
        p.append(f'<circle cx="{x + 14}" cy="{y + 38}" r="2.6" fill="#F87171"/><circle cx="{x + 23}" cy="{y + 38}" r="2.6" fill="#F5B544"/>'
                 f'<circle cx="{x + 32}" cy="{y + 38}" r="2.6" fill="#34D399"/>')
        for j, (dx, w, col) in enumerate([(0, 46, c1), (12, 58, c2), (12, 34, c1), (24, 50, c2), (12, 40, c1), (0, 26, c2)]):
            p.append(f'<rect x="{x + 12 + dx}" y="{y + 50 + j * 11}" width="{w}" height="5" rx="2.5" fill="{col}" fill-opacity=".75"/>')
        hx, hy = x + 140, y + 62
        p.append(f'<path d="{hexagono(hx, hy, 32)}" fill="{c1}" fill-opacity=".18" stroke="{c1}" stroke-width="2.4"/>')
        p.append(f'<path d="m{hx - 12} {hy - 10}-10 10 10 10M{hx + 12} {hy - 10}l10 10-10 10M{hx + 4} {hy - 15}l-8 30" '
                 f'fill="none" stroke="{c1}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
        for nx, ny in ((x + 124, y + 118), (x + 160, y + 112), (x + 142, y + 136)):
            p.append(f'<circle class="led" cx="{nx}" cy="{ny}" r="4" fill="{c2}" style="animation-delay:-{(nx % 7) * .3}s"/>')
        p.append(f'<path d="M{x + 124} {y + 118}L{x + 160} {y + 112}L{x + 142} {y + 136}Z" fill="none" stroke="{c2}" stroke-opacity=".7"/>')
    return "".join(p)


def areas(perfil: dict) -> str:
    lista = perfil["areas"]
    W, H = 1200, 300
    lz = Lienzo(W, H, "Áreas: " + ", ".join(a["titulo"] for a in lista),
                " · ".join(a["titulo"] + ": " + " ".join(a["lema"]) for a in lista))
    gap = 18
    ancho = (W - gap * (len(lista) - 1)) / len(lista)
    for i, area in enumerate(lista):
        x = i * (ancho + gap)
        c1 = P[area["acento"]]
        c2 = P[area.get("acento2", PAREJA[area["acento"]])]
        lz.defs.append(
            f'<linearGradient id="af{i}" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".30"/>'
            f'<stop offset=".55" stop-color="{c2}" stop-opacity=".08"/><stop offset="1" stop-color="#0A1026" stop-opacity="0"/></linearGradient>'
            + degradado(f"ab{i}", [c1, c2], 1, 1) + brillo(f"ag{i}", c1, .45)
            + f'<clipPath id="ac{i}"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" rx="18"/></clipPath>'
        )
        ix, iy = x + ancho - 184, 4
        lz.add(
            f'<g clip-path="url(#ac{i})"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="#0A1026"/>',
            f'<rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="url(#af{i})"/>',
            f'<circle cx="{num(x + ancho - 90)}" cy="86" r="130" fill="url(#ag{i})"/>',
            pedestal(lz, f"ap{i}", ix + 92, iy + 136, 62, c1, c2),
            ilustracion_area(area["icono"], ix, iy, c1, c2),
            f'<rect class="br" x="{num(x - 300)}" y="0" width="300" height="{H}" fill="url(#brl)" style="animation-delay:-{i * 2.3}s"/></g>',
            f'<rect x="{num(x + .75)}" y=".75" width="{num(ancho - 1.5)}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#ab{i})" stroke-width="1.6" stroke-opacity=".9"/>',
            f'<rect x="{num(x + 22)}" y="24" width="50" height="50" rx="14" fill="url(#ab{i})"/>',
            icono(area["icono"], x + 34, 36, 26, "#fff", 2.2),
            lz.texto("mono", f"0{i + 1}", x + 22, 102, 12, c1, 1)[0],
        )
        lineas = area.get("titulo_lineas", [area["titulo"]])
        tam = min(lz.ajustar("titulo", l, ancho - 44, 24) for l in lineas)
        for j, linea in enumerate(lineas):
            yy = 214 - (len(lineas) - 1 - j) * 28
            lz.add(neon(lz, "titulo", linea, x + 22, yy, tam, c1, retraso=i * 0.9)[0])
        for j, linea in enumerate(area["lema"]):
            lz.add(lz.texto("texto", linea, x + 22, 246 + j * 22, lz.ajustar("texto", linea, ancho - 44, 15), tono(c1, .68))[0])
        lz.add(f'<rect x="{num(x + 22)}" y="226" width="34" height="3" rx="1.5" fill="{c1}"/>')
    lz.defs.append('<linearGradient id="brl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                   '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    lz.estilos.append(
        ".br{animation:br 10s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes br{0%{transform:translateX(0)}50%,100%{transform:translateX(620px)}}"
        ".led{animation:led 2.4s steps(2,start) infinite}@keyframes led{to{opacity:.2}}"
        ".gir{animation:gir 14s linear infinite}@keyframes gir{to{transform:rotate(360deg)}}"
        ".bc{transform-box:fill-box;transform-origin:bottom;animation:bc 3s ease-in-out infinite alternate}"
        "@keyframes bc{from{transform:scaleY(.7)}to{transform:scaleY(1)}}"
        + CSS_COMUN + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  LO QUE SÉ: bandas de categoría e íconos genéricos propios
#  (los logotipos de cada tecnología se cargan desde skill-icons en el README)
# ═════════════════════════════════════════════════════════════════════════════

def banda_categoria(grupo: dict, indice: int) -> str:
    W, H = 1200, 88
    c1 = P[grupo["acento"]]
    c2 = P[grupo.get("acento2", PAREJA[grupo["acento"]])]
    n = len(grupo["items"])
    lz = Lienzo(W, H, grupo["grupo"], f"{grupo['grupo']}: {grupo['descripcion']}")
    lz.defs.append(
        f'<clipPath id="kc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
        + degradado("kf", ["#070C22", mezclar("#070C22", c1, .12), "#0B0F2C"], 1, 0)
        + degradado("kb", [c1, c2], 1, 0) + brillo("kg", c1, .45)
        + f'<linearGradient id="ks" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity="0"/>'
          f'<stop offset=".5" stop-color="{c1}" stop-opacity=".18"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></linearGradient>'
    )
    circuito = []
    rnd = random.Random(grupo["grupo"])
    for k in range(6):
        x = rnd.uniform(620, 960)
        y = rnd.choice([18, 30, 58, 70])
        circuito.append(f"M{num(x)} {y}h{rnd.randint(30, 90)}v{rnd.choice([-1, 1]) * rnd.randint(6, 14)}h{rnd.randint(10, 30)}")
    lz.add(
        f'<g clip-path="url(#kc)"><rect width="{W}" height="{H}" fill="url(#kf)"/>',
        f'<circle cx="56" cy="44" r="120" fill="url(#kg)"/>',
        f'<path d="{"".join(circuito)}" fill="none" stroke="{c1}" stroke-opacity=".25" stroke-width="1.3"/>',
        f'<rect class="ksw" x="-320" y="0" width="320" height="{H}" fill="url(#ks)" style="animation-delay:-{num(indice * 2.4)}s"/>',
        f'<rect width="6" height="{H}" fill="url(#kb)"/></g>',
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="url(#kb)" stroke-opacity=".6" stroke-width="1.5"/>',
        f'<path class="kp" d="{hexagono(58, 44, 34)}" fill="none" stroke="{c1}" stroke-opacity=".5" stroke-dasharray="5 5" '
        f'style="animation-delay:-{num(indice * 1.7)}s"/>',
        f'<path d="{hexagono(58, 44, 27)}" fill="{c1}" fill-opacity=".18" stroke="{c1}" stroke-width="2.2"/>',
        icono(grupo["icono"], 45, 31, 26, mezclar(c1, "#FFFFFF", .3), 2.1),
        neon(lz, "titulo", grupo["grupo"], 108, 41, 23, c1, retraso=indice * 1.1)[0],
        lz.texto("texto", grupo["descripcion"], 108, 66, 15, tono(c1, .66))[0],
    )
    etiqueta = f"{n} {'elemento' if n == 1 else 'elementos'}"
    ancho = Fuente.de("monob").ancho(etiqueta, 13, .5) + 30
    lz.add(f'<rect x="{num(W - 30 - ancho)}" y="30" width="{num(ancho)}" height="28" rx="14" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-opacity=".8"/>',
           lz.texto("monob", etiqueta, W - 30 - ancho / 2, 49, 13, mezclar(c1, "#FFFFFF", .35), .5, "middle")[0])
    lz.estilos.append(
        ".ksw{animation:ksw 10s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes ksw{0%{transform:translateX(0)}45%,100%{transform:translateX(1560px)}}"
        ".kp{transform-box:fill-box;transform-origin:center;animation:kp 4.5s ease-in-out infinite}"
        "@keyframes kp{0%,100%{opacity:.35;transform:scale(.94)}50%{opacity:1;transform:scale(1.06)}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar()


def icono_generico(nombre: str, icono_nombre: str, acento: str) -> str:
    """Ícono propio en el mismo formato de casilla que los íconos de tecnologías (256×256)."""
    c1 = P[acento]
    lz = Lienzo(256, 256, nombre)
    lz.defs.append(brillo("ig", c1, .32))
    lz.add('<rect width="256" height="256" rx="60" fill="#242938"/>',
           '<circle cx="128" cy="128" r="104" fill="url(#ig)"/>',
           icono(icono_nombre, 58, 58, 140, mezclar(c1, "#FFFFFF", .18), 2.6))
    return lz.armar()


def insignia(icono_nombre: str, acento: str, titulo: str) -> str:
    """Insignia hexagonal para la tabla de constancias (88×88)."""
    c1 = P[acento]
    lz = Lienzo(88, 88, titulo)
    lz.defs.append(brillo("ng", c1, .4))
    lz.add('<circle cx="44" cy="44" r="42" fill="url(#ng)"/>',
           f'<path d="{hexagono(44, 44, 38)}" fill="#0A1230" stroke="{c1}" stroke-width="2.6"/>',
           f'<path d="{hexagono(44, 44, 38)}" fill="{c1}" fill-opacity=".14"/>',
           icono(icono_nombre, 24, 24, 40, mezclar(c1, "#FFFFFF", .2), 2.2))
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  FORMACIÓN (tarjetas con acento propio y marco dorado)
# ═════════════════════════════════════════════════════════════════════════════

def formacion(tarjetas: list[dict]) -> str:
    W, H = 1200, 300
    lz = Lienzo(W, H, "Formación", " · ".join(" ".join(t["titulo"]) + " (" + t["detalle"] + ", " + t["periodo"] + ")" for t in tarjetas))
    n = len(tarjetas)
    gap = 18
    ancho = (W - gap * (n - 1)) / n
    oro = P["ambar"]
    rnd = random.Random(11)
    lz.defs.append('<linearGradient id="fsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF4DD" stop-opacity="0"/>'
                   '<stop offset=".5" stop-color="#FFF4DD" stop-opacity=".12"/><stop offset="1" stop-color="#FFF4DD" stop-opacity="0"/></linearGradient>')
    for i, t in enumerate(tarjetas):
        x = i * (ancho + gap)
        c1 = P[t.get("acento", "ambar")]
        lz.defs.append(
            f'<clipPath id="fc{i}"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" rx="16"/></clipPath>'
            + degradado(f"fo{i}", [c1, oro], 1, 1)
            + f'<linearGradient id="ff{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".30"/>'
              f'<stop offset=".5" stop-color="{c1}" stop-opacity=".07"/><stop offset="1" stop-color="#0A0E22" stop-opacity="0"/></linearGradient>'
            + brillo(f"fg{i}", c1, .5)
        )
        circuito = []
        for k in range(7):
            yy = rnd.randint(30, 170)
            xx = x + rnd.uniform(ancho * .45, ancho - 20)
            circuito.append(f"M{num(xx)} {yy}h{rnd.randint(30, 90)}v{rnd.choice([-1, 1]) * rnd.randint(10, 30)}")
        lz.add(
            f'<g clip-path="url(#fc{i})"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="#0B0F24"/>',
            f'<rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="url(#ff{i})"/>',
            f'<circle cx="{num(x + ancho * .72)}" cy="76" r="120" fill="url(#fg{i})"/>',
            f'<path d="{"".join(circuito)}" fill="none" stroke="{c1}" stroke-opacity=".28" stroke-width="1.4"/>',
            f'<rect class="fsw" x="{num(x - 260)}" y="0" width="260" height="{H}" fill="url(#fsw)" style="animation-delay:-{i * 2.4}s"/></g>',
            f'<rect x="{num(x + .75)}" y=".75" width="{num(ancho - 1.5)}" height="{H - 1.5}" rx="16" fill="none" stroke="url(#fo{i})" stroke-width="1.6"/>',
        )
        icx, icy = x + ancho * .72, 84
        lz.add(f'<path d="{hexagono(icx, icy, 46)}" fill="{c1}" fill-opacity=".14" stroke="url(#fo{i})" stroke-width="2.4"/>',
               f'<path class="fpu" d="{hexagono(icx, icy, 56)}" fill="none" stroke="{c1}" stroke-opacity=".5" stroke-dasharray="5 6" style="animation-delay:-{i * 4}s"/>',
               icono(t["icono"], icx - 22, icy - 22, 44, mezclar(c1, "#FFFFFF", .3), 2.2))
        lz.add(lz.texto("monob", f"0{i + 1}", x + 22, 42, 13, c1, 1.5)[0],
               f'<rect x="{num(x + 22)}" y="54" width="28" height="3" rx="1.5" fill="{c1}"/>')
        tam = min(lz.ajustar("titulo", linea, ancho - 40, 21) for linea in t["titulo"])
        for j, linea in enumerate(t["titulo"]):
            lz.add(neon(lz, "titulo", linea, x + 22, 182 + j * 26, tam, c1, retraso=i * 0.9)[0])
        lz.add(lz.texto("texto", t["detalle"], x + 22, 254, lz.ajustar("texto", t["detalle"], ancho - 40, 14.5), tono(c1, .66))[0],
               lz.texto("mono", t["periodo"], x + 22, 278, 12.5, mezclar(c1, "#FFFFFF", .2))[0])
    lz.estilos.append(
        ".fsw{animation:fsw 9s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes fsw{0%{transform:translateX(0)}55%,100%{transform:translateX(560px)}}"
        ".fpu{transform-box:fill-box;transform-origin:center;animation:fpu 24s linear infinite}"
        "@keyframes fpu{to{transform:rotate(360deg)}}" + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  TRAYECTORIA (misma estructura: línea, años arriba, empresa y puesto abajo)
# ═════════════════════════════════════════════════════════════════════════════

def trayectoria(experiencia: list[dict]) -> str:
    puntos = list(reversed(experiencia))  # de la más antigua a la más reciente
    W, H = 1200, 226
    lz = Lienzo(W, H, "Trayectoria", " → ".join(f"{e['anio']}: {e['puesto']} en {e['empresa_corta']}" for e in puntos))
    colores = [P[e.get("acento", "coral")] for e in puntos]
    x0, x1, yl = 110, W - 110, 100
    lz.defs.append(
        f'<clipPath id="yc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("yf", ["#060B22", "#0B0A2C", "#140A22"], 1, 1)
        + f'<linearGradient id="yl" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">'
        + "".join(f'<stop offset="{num(i / max(1, len(colores) - 1))}" stop-color="{c}"/>' for i, c in enumerate(colores))
        + "</linearGradient>"
        + degradado("ylb", [P["coral"], P["ambar"], P["violeta"]], 1, 0)
        + brillo("yb1", P["coral"], .16) + brillo("yb2", P["violeta"], .14)
    )
    lz.add(f'<g clip-path="url(#yc)"><rect width="{W}" height="{H}" fill="url(#yf)"/>',
           f'<circle cx="{W - 160}" cy="{H}" r="320" fill="url(#yb1)"/><circle cx="160" cy="0" r="300" fill="url(#yb2)"/>',
           f'<path d="M{x0} {yl}H{x1}" stroke="url(#yl)" stroke-width="3" stroke-linecap="round"/>',
           f'<path d="M{x0} {yl}H{x1}" stroke="url(#yl)" stroke-width="12" stroke-opacity=".15"/>',
           f'<circle class="yp" cx="{x0}" cy="{yl}" r="5" fill="#fff"/>')
    paso = (x1 - x0) / max(1, len(puntos) - 1)
    for i, e in enumerate(puntos):
        x = x0 + i * paso
        c = colores[i]
        lz.defs.append(brillo(f"yg{i}", c, .6))
        lz.add(f'<circle cx="{num(x)}" cy="{yl}" r="38" fill="url(#yg{i})"/>',
               f'<path class="yn" d="{hexagono(x, yl, 31)}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-dasharray="4 4" style="animation-delay:-{i * .7}s"/>',
               f'<path d="{hexagono(x, yl, 24)}" fill="#0A1230" stroke="{c}" stroke-width="2.6"/>',
               icono(e.get("icono", "maletin"), x - 11, yl - 11, 22, mezclar(c, "#FFFFFF", .25), 2),
               lz.texto("monob", e["anio"], x, yl - 44, 15, c, 1, "middle")[0])
        tam = lz.ajustar("titulo", e["empresa_corta"], paso - 24 if len(puntos) > 1 else 300, 19)
        lz.add(neon(lz, "titulo", e["empresa_corta"], x, yl + 60, tam, c, ancla="middle", retraso=i * 0.9)[0])
        puesto = e.get("puesto_corto", e["puesto"])
        tam_p = lz.ajustar("mono", puesto, paso - 20 if len(puntos) > 1 else 300, 12.5)
        lz.add(lz.texto("mono", puesto, x, yl + 84, tam_p, tono(c, .62), ancla="middle")[0])
    lz.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#ylb)" stroke-opacity=".55" stroke-width="1.5"/></g>')
    lz.estilos.append(
        f".yp{{animation:yp 6s ease-in-out infinite}}@keyframes yp{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}"
        f"90%{{opacity:1}}100%{{transform:translateX({x1 - x0}px);opacity:0}}}}"
        ".yn{transform-box:fill-box;transform-origin:center;animation:yn 3s ease-in-out infinite}"
        "@keyframes yn{0%,100%{transform:scale(.92);opacity:.4}50%{transform:scale(1.08);opacity:1}}" + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  PORTADAS DE PROYECTOS (ilustración holográfica, acento propio, estado real)
# ═════════════════════════════════════════════════════════════════════════════

def motivo(tipo: str, c1: str, c2: str, rnd: random.Random) -> str:
    """Ilustración de la portada en la zona derecha (x 340–620, y 50–270)."""
    def st(g=2.6, f="none", o=None):
        return (f'fill="{f}"' + (f' fill-opacity="{o}"' if o is not None else "")
                + f' stroke="{c1}" stroke-width="{g}" stroke-linecap="round" stroke-linejoin="round"')
    p = []
    if tipo == "escudo":  # ALBA: revisión de seguridad
        for i in range(6):
            y = 92 + i * 24
            marca = ["#F87171", "#F5B544", "#34D399", "#3B82F6"][i % 4]
            p.append(f'<circle cx="352" cy="{y}" r="4.5" fill="{marca}"/>')
            p.append(f'<rect x="364" y="{y - 4}" width="{rnd.randint(64, 120)}" height="8" rx="4" fill="{c2}" fill-opacity=".5"/>')
        p.append(f'<rect class="mscan" x="340" y="82" width="170" height="24" rx="6" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-opacity=".6"/>')
        cx, top = 548, 58
        p.append(f'<path d="M{cx} {top}L{cx + 62} {top + 25}V{top + 90}C{cx + 62} {top + 136} {cx + 31} {top + 163} {cx} {top + 178}'
                 f'C{cx - 31} {top + 163} {cx - 62} {top + 136} {cx - 62} {top + 90}V{top + 25}Z" {st(3, c1, ".16")}/>')
        p.append(f'<circle cx="{cx - 4}" cy="{top + 84}" r="25" {st(3.2, "#0A1230", ".75")}/><path d="M{cx + 13} {top + 102}L{cx + 34} {top + 123}" {st(5)}/>')
    elif tipo == "logs":  # Laboratorio: análisis de registros
        p.append(f'<rect x="346" y="56" width="270" height="190" rx="12" fill="#050A1E" stroke="{c1}" stroke-opacity=".7" stroke-width="1.5"/>')
        p.append('<circle cx="362" cy="72" r="4" fill="#F87171"/><circle cx="375" cy="72" r="4" fill="#F5B544"/><circle cx="388" cy="72" r="4" fill="#34D399"/>')
        for i in range(7):
            y = 92 + i * 18
            a, b = rnd.randint(28, 48), rnd.randint(40, 118)
            sosp = i in (3, 4)
            p.append(f'<rect x="360" y="{y}" width="{a}" height="7" rx="3" fill="{c2}" fill-opacity=".55"/>')
            p.append(f'<rect x="{366 + a}" y="{y}" width="{b}" height="7" rx="3" fill="{"#F87171" if sosp else c1}" fill-opacity="{.95 if sosp else .55}"/>')
        p.append(f'<path d="M354 144h-5v36h5M606 144h5v36h-5" {st(2.4, "none")}/>')
        for i, h in enumerate([10, 14, 9, 18, 34, 40, 14, 8]):
            p.append(f'<rect class="mbar" x="{528 + i * 9}" y="{234 - h}" width="6" height="{h}" fill="{"#F87171" if h > 30 else c1}" style="animation-delay:-{i * .3}s"/>')
        p.append(f'<rect class="mcur" x="360" y="222" width="9" height="12" fill="{c1}"/>')
    elif tipo == "ia":  # SOPHYA: núcleo de IA con voz
        cx, cy = 492, 150
        p.append(f'<circle cx="{cx}" cy="{cy}" r="94" fill="none" stroke="{c2}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="3 7"/>')
        p.append(f'<circle class="mgir" cx="{cx}" cy="{cy}" r="68" fill="none" stroke="{c1}" stroke-opacity=".85" stroke-width="2.4" stroke-dasharray="40 14"/>')
        p.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-width="2.4"/>')
        p.append(f'<circle class="mpul" cx="{cx}" cy="{cy}" r="21" fill="{c1}"/>')
        for ang, r, col in ((20, 94, c2), (140, 68, "#22D3EE"), (250, 94, c1), (320, 68, c2), (80, 94, "#22D3EE")):
            a = math.radians(ang)
            p.append(f'<rect x="{num(cx + math.cos(a) * r - 5)}" y="{num(cy + math.sin(a) * r - 5)}" width="10" height="10" rx="2" fill="{col}"/>')
        for i in range(9):
            h = [10, 22, 36, 18, 44, 26, 14, 30, 12][i]
            p.append(f'<rect class="mbar" x="{556 + i * 7}" y="{cy - h / 2}" width="4" height="{h}" rx="2" fill="#22D3EE" style="animation-delay:-{i * .2}s"/>')
    elif tipo == "voz":  # English Speaking Coach: micrófono, voz y corrección
        p.append(f'<rect x="372" y="70" width="48" height="96" rx="24" {st(3, c1, ".18")}/>')
        p.append(f'<path d="M356 132c0 40 80 40 80 0M396 172v24M376 198h40" {st(3)}/>')
        for i in range(16):
            h = 10 + abs(math.sin(i * 0.9)) * 62
            p.append(f'<rect class="mbar" x="{452 + i * 9.5}" y="{num(132 - h / 2)}" width="5.5" height="{num(h)}" rx="2.7" '
                     f'fill="{c1 if i % 2 else c2}" style="animation-delay:-{num(i * .17)}s"/>')
        p.append(f'<rect x="470" y="186" width="136" height="48" rx="12" fill="#050A1E" stroke="{c2}" stroke-opacity=".85"/>')
        p.append(f'<path d="M488 234l-6 12 18-12" fill="#050A1E" stroke="{c2}" stroke-opacity=".85"/>')
        p.append(f'<rect x="486" y="202" width="72" height="6" rx="3" fill="{c1}"/><rect x="486" y="214" width="46" height="6" rx="3" fill="{c2}" fill-opacity=".7"/>')
        p.append(f'<path d="m572 204 6 6 12-12" fill="none" stroke="#34D399" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    elif tipo == "tienda":  # Smucky's: ropa deportiva y casual
        p.append(f'<path d="M360 70H604M374 70v-10M590 70v-10" stroke="{c2}" stroke-width="3" stroke-linecap="round"/>')
        # playera
        p.append(f'<path d="M424 70v8M424 78c-8 0-8 6-4 8" fill="none" stroke="{c2}" stroke-width="2"/>')
        p.append(f'<path d="M402 92l17-10h12c0 6 10 6 10 0h12l17 10 13 18-14 9-7-6v62h-62v-62l-7 6-14-9z" {st(2.8, c1, ".22")}/>')
        p.append(f'<path d="M418 132h34" stroke="{c1}" stroke-opacity=".7" stroke-width="2"/>')
        # sudadera con capucha
        p.append(f'<path d="M534 70v8M534 78c-8 0-8 6-4 8" fill="none" stroke="{c2}" stroke-width="2"/>')
        p.append(f'<path d="M512 96c4-14 40-14 44 0l16 10 10 46-14 2-6-30v66h-56v-66l-6 30-14-2 10-46z" fill="{c2}" fill-opacity=".2" '
                 f'stroke="{c2}" stroke-width="2.8" stroke-linejoin="round"/>')
        p.append(f'<path d="M520 96c4 16 24 16 28 0M534 112v26M520 160h28" fill="none" stroke="{c2}" stroke-width="2.2" stroke-linecap="round"/>')
        # short deportivo
        p.append(f'<path d="M368 214h56l4 34h-24l-4-16-4 16h-24z" {st(2.4, c1, ".25")}/>')
        # etiqueta y bolsa
        p.append(f'<path d="M466 222h48l12 12-12 12h-48z" fill="{c1}" fill-opacity=".25" stroke="{c1}" stroke-width="2"/><circle cx="478" cy="234" r="3.5" fill="{c1}"/>')
        p.append(f'<rect class="mpul" x="550" y="204" width="44" height="40" rx="6" fill="{c2}" fill-opacity=".22" stroke="{c2}" stroke-width="2.4"/>')
        p.append(f'<path d="M562 210v-6a10 10 0 0 1 20 0v6" fill="none" stroke="{c2}" stroke-width="2.4"/>')
    elif tipo == "lealtad":  # Chavarín & Said: tarjeta de sellos y QR de mostrador
        p.append(f'<rect x="350" y="78" width="200" height="126" rx="16" fill="#050A1E" stroke="{c1}" stroke-width="2"/>')
        p.append(f'<rect x="368" y="96" width="74" height="8" rx="4" fill="{c2}" fill-opacity=".8"/>')
        for i in range(8):
            fx, fy = 380 + (i % 4) * 34, 134 + (i // 4) * 34
            lleno = i < 5
            clase = ' class="msel"' if lleno else ""
            p.append(f'<circle{clase} cx="{fx}" cy="{fy}" r="12" fill="{c1 if lleno else "none"}" stroke="{c1}" stroke-width="2.2" style="animation-delay:{i * .35}s"/>')
        qx, qy, qs = 526, 146, 86
        p.append(f'<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="9" fill="#EEF3FF"/>')
        m = qs / 12
        bloques = []
        for fy in range(1, 11):
            for fx in range(1, 11):
                esquina = (fx < 4 and fy < 4) or (fx > 7 and fy < 4) or (fx < 4 and fy > 7)
                if esquina:
                    if fx in (1, 3, 8, 10) or fy in (1, 3, 8, 10) or (fx, fy) in ((2, 2), (9, 2), (2, 9)):
                        bloques.append((fx, fy))
                elif rnd.random() < 0.45:
                    bloques.append((fx, fy))
        d = "".join(f"M{num(qx + fx * m)} {num(qy + fy * m)}h{num(m)}v{num(m)}h-{num(m)}z" for fx, fy in bloques)
        p.append(f'<path d="{d}" fill="#0A1230"/>')
    else:
        p.append(f'<rect x="350" y="66" width="260" height="180" rx="12" fill="#050A1E" stroke="{c1}" stroke-opacity=".6"/>')
        p.append(f'<rect x="370" y="114" width="100" height="12" rx="6" fill="{c1}"/>')
    return "".join(p)


def portada(proyecto: dict, indice: int) -> str:
    W, H = 640, 300
    acento = proyecto.get("acento", "cian")
    c1 = P[acento]
    c2 = P[proyecto.get("acento2", PAREJA[acento])]
    estado = proyecto.get("estado_tipo", "disponible")
    lz = Lienzo(W, H, f"Portada de {proyecto['nombre']}",
                f"{proyecto['categoria']} · estado: {estado} · {proyecto['estado']}")
    rnd = random.Random(proyecto["id"])
    lz.defs.append(
        f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("pf", ["#050816", mezclar("#050816", c2, .16), mezclar("#050816", c1, .28)], 1, 1)
        + brillo("pg1", c1, .5, .14) + brillo("pg2", c2, .38)
        + degradado("pb", [c1, c2], 1, 1) + degradado("pn", [c1, c2], 1, 0)
        + '<pattern id="pr" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>'
        + '<linearGradient id="psw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    )
    vx, yh = 480, 240
    lineas = "".join(f"M{vx + i * 3} {yh}L{vx + i * 44} {H}" for i in range(-8, 9))
    lineas += "".join(f"M300 {yh + d}H{W}" for d in (5, 13, 25, 42))
    cubos = cubos_flotantes(rnd, [(338, 58, 12), (618, 92, 10), (606, 214, 14), (334, 214, 9)], [c1, c2, c1, c2])
    lz.add(
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="url(#pf)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#pr)"/>',
        f'<circle cx="500" cy="150" r="230" fill="url(#pg1)"/><circle cx="60" cy="300" r="220" fill="url(#pg2)"/>',
        f'<path d="{lineas}" stroke="{c1}" stroke-opacity=".2" fill="none"/>',
        pedestal(lz, "pp", 480, 258, 118, c1, c2),
        motivo(proyecto.get("portada", "web"), c1, c2, rnd),
        cubos,
        f'<rect class="psw" x="-260" y="0" width="260" height="{H}" fill="url(#psw)"/></g>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#pb)" stroke-width="2"/>',
    )
    lz.add(lz.texto("mono", f"proyecto/{proyecto['id']}", 28, 41, 12.5, mezclar(c1, "#FFFFFF", .2))[0])
    numero, _ = lz.texto("titulo", f"{indice:02d}", 22, 148, 86, "#fff")
    lz.defs.append(f'<mask id="pm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{numero}</mask>')
    lz.add(f'<rect x="18" y="74" width="140" height="80" fill="url(#pn)" fill-opacity=".38" mask="url(#pm)"/>')
    lz.add(chip_estado(lz, estado, proyecto.get("etiqueta", ""), W - 24, 22))
    lz.add(lz.texto("monob", proyecto["categoria"].upper(), 28, 190, 12.5, mezclar(c1, "#FFFFFF", .2), 1.2)[0])
    nombre = proyecto["nombre"]
    tam = lz.ajustar("titulo", nombre, 300, 34)
    if tam < 27 and " — " in nombre:
        l1, l2 = nombre.split(" — ", 1)
        tam = min(lz.ajustar("titulo", l1, 300, 29), lz.ajustar("titulo", l2, 300, 29))
        lz.add(neon(lz, "titulo", l1, 26, 222, tam, c1)[0],
               lz.texto("titulo", l2, 26, 222 + tam * 1.08, tam, tono(c2, .4))[0])
    else:
        lz.add(neon(lz, "titulo", nombre, 26, 236, tam, c1)[0])
    tecnologias = "  ·  ".join(proyecto.get("tecnologias", []))
    if tecnologias:
        lz.add(lz.texto("mono", tecnologias, 28, 280, lz.ajustar("mono", tecnologias, 300, 12.5), "#C3CDEA")[0])
    lz.estilos.append(
        ".psw{animation:psw 9s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes psw{0%{transform:translateX(0)}55%,100%{transform:translateX(920px)}}"
        ".mscan{animation:mscan 4s ease-in-out infinite alternate}@keyframes mscan{to{transform:translateY(120px)}}"
        ".mbar{transform-box:fill-box;transform-origin:center bottom;animation:mbar 1.6s ease-in-out infinite alternate}"
        "@keyframes mbar{from{transform:scaleY(.45)}to{transform:scaleY(1)}}"
        ".mcur{animation:mcur 1.1s steps(2,start) infinite}@keyframes mcur{to{opacity:0}}"
        ".mgir{transform-box:fill-box;transform-origin:center;animation:mgir 12s linear infinite}@keyframes mgir{to{transform:rotate(360deg)}}"
        ".mpul{transform-box:fill-box;transform-origin:center;animation:mpul 2.8s ease-in-out infinite}"
        "@keyframes mpul{0%,100%{transform:scale(.92)}50%{transform:scale(1.06)}}"
        ".msel{animation:msel 5s ease-out infinite both}@keyframes msel{0%{opacity:.15}12%,85%{opacity:1}100%{opacity:.15}}"
        + CSS_COMUN + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  BOTONES DE CONTACTO
# ═════════════════════════════════════════════════════════════════════════════

def boton(texto: str, icono_nombre: str, acento: str) -> str:
    W, H = 264, 58
    c1, c2 = P[acento], P[PAREJA[acento]]
    lz = Lienzo(W, H, texto)
    lz.defs.append(degradado("bb", [c1, c2], 1, 1)
                   + f'<linearGradient id="bf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity=".22"/>'
                     f'<stop offset="1" stop-color="{c2}" stop-opacity=".1"/></linearGradient>')
    lz.add(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#0A1026"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#bf)" stroke="url(#bb)" stroke-width="2"/>',
        f'<rect x="12" y="11" width="36" height="36" rx="10" fill="url(#bb)"/>',
        icono(icono_nombre, 18, 17, 24, "#fff", 2),
        lz.texto("texto", texto, 62, 36, 18, "#EEF3FF")[0],
        f'<path d="M{W - 34} 36L{W - 24} 26M{W - 32} 26H{W - 24}V34" fill="none" stroke="{c1}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  TARJETAS NEÓN (experiencia, detalle de áreas y laboratorios)
#  Caja animada: borde con una luz que la recorre, título neón y texto en tono claro.
# ═════════════════════════════════════════════════════════════════════════════

def tarjeta_neon(titulo: str, subtitulo: str, puntos: list[str], acento: str, acento2: str, icono_nombre: str,
                 lado_titulo: str, lado_sub: str, chip: str = "", indice: int = 0) -> str:
    W = 1200
    c1, c2 = P[acento], P[acento2]
    izq = 250
    x_t = izq + 40
    ancho_t = W - x_t - 40
    tam_p, alto_linea = 17, 27
    bloques = [envolver(pt, "texto", tam_p, ancho_t - 26) for pt in puntos]
    y_sub = 92 if subtitulo else 62
    y0 = y_sub + 40
    H = max(210, int(y0 + sum(len(b) for b in bloques) * alto_linea + (len(bloques) - 1) * 8 + 26))
    lz = Lienzo(W, H, titulo, (subtitulo + ". " if subtitulo else "") + " ".join(puntos))
    lz.defs.append(
        f'<clipPath id="tc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("tf", ["#060A1E", mezclar("#060A1E", c1, .10), "#0A0B24"], 1, 1)
        + f'<linearGradient id="tl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".32"/>'
          f'<stop offset="1" stop-color="{c2}" stop-opacity=".08"/></linearGradient>'
        + degradado("tb", [c1, c2], 1, 1) + brillo("tg", c1, .5) + brillo("tg2", c2, .2)
    )
    cx, cy = izq / 2, H / 2 - 22
    lz.add(
        f'<g clip-path="url(#tc)"><rect width="{W}" height="{H}" fill="url(#tf)"/>',
        f'<rect width="{izq}" height="{H}" fill="url(#tl)"/>',
        f'<circle cx="{num(cx)}" cy="{num(cy)}" r="150" fill="url(#tg)"/>',
        f'<circle cx="{W - 120}" cy="0" r="260" fill="url(#tg2)"/>',
        f'<path d="M{izq} 0V{H}" stroke="{c1}" stroke-opacity=".45"/></g>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#tb)" stroke-opacity=".5" stroke-width="1.5"/>',
        f'<rect class="tr" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="{tono(c1, .25)}" '
        f'stroke-width="2.6" stroke-linecap="round" pathLength="1000" stroke-dasharray="110 890" style="animation-delay:-{num(indice * 1.7)}s"/>',
        f'<path class="tp" d="{hexagono(cx, cy, 46)}" fill="none" stroke="{c1}" stroke-opacity=".6" stroke-dasharray="5 6" style="animation-delay:-{num(indice)}s"/>',
        f'<path d="{hexagono(cx, cy, 36)}" fill="#0A1230" stroke="{c1}" stroke-width="2.6"/>',
        f'<path d="{hexagono(cx, cy, 36)}" fill="{c1}" fill-opacity=".16"/>',
        icono(icono_nombre, cx - 17, cy - 17, 34, tono(c1, .3), 2.2),
    )
    tam_l = lz.ajustar("titulo", lado_titulo, izq - 30, 20)
    lz.add(neon(lz, "titulo", lado_titulo, cx, cy + 78, tam_l, c1, ancla="middle", retraso=indice * 0.8)[0],
           lz.texto("monob", lado_sub, cx, cy + 104, 13.5, tono(c1, .3), 1, "middle")[0])
    tam_t = lz.ajustar("titulo", titulo, ancho_t - (170 if chip else 0), 27)
    lz.add(neon(lz, "titulo", titulo, x_t, 58, tam_t, c1, retraso=indice * 0.8 + .4)[0])
    if subtitulo:
        lz.add(lz.texto("texto", subtitulo, x_t, y_sub, lz.ajustar("texto", subtitulo, ancho_t, 17), tono(c2, .5))[0])
    if chip:
        ancho_c = Fuente.de("monob").ancho(chip, 13, .5) + 30
        lz.add(f'<rect x="{num(W - 36 - ancho_c)}" y="34" width="{num(ancho_c)}" height="30" rx="15" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-opacity=".85"/>',
               lz.texto("monob", chip, W - 36 - ancho_c / 2, 54, 13, tono(c1, .35), .5, "middle")[0])
    y = y0
    for bloque in bloques:
        lz.add(f'<path d="M{x_t} {y - 6}l5 -5 5 5 -5 5Z" fill="{c1}"/>')
        for linea in bloque:
            lz.add(lz.texto("texto", linea, x_t + 24, y, tam_p, tono(c1, .74))[0])
            y += alto_linea
        y += 8
    lz.estilos.append(
        ".tr{animation:tr 7s linear infinite}@keyframes tr{to{stroke-dashoffset:-1000}}"
        ".tp{transform-box:fill-box;transform-origin:center;animation:tp 4s ease-in-out infinite}"
        "@keyframes tp{0%,100%{opacity:.35;transform:scale(.94)}50%{opacity:1;transform:scale(1.06)}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar()


def tarjeta_constancia(curso: dict, acento: str, icono_nombre: str, indice: int) -> str:
    """Constancia destacada como tarjeta neón (590×150). Si tiene verificación, la imagen va enlazada."""
    W, H = 590, 150
    c1 = P[acento]
    c2 = P[PAREJA[acento]]
    lz = Lienzo(W, H, curso["nombre"], f"{curso['emisor']} · {curso['fecha']} · {curso['tipo']}")
    lz.defs.append(
        f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
        + degradado("cf", ["#060A1E", mezclar("#060A1E", c1, .14)], 1, 1) + degradado("cb", [c1, c2], 1, 1)
        + brillo("cg", c1, .5)
    )
    lz.add(f'<g clip-path="url(#cc)"><rect width="{W}" height="{H}" fill="url(#cf)"/>',
           f'<circle cx="62" cy="75" r="110" fill="url(#cg)"/></g>',
           f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" fill="none" stroke="url(#cb)" stroke-opacity=".55" stroke-width="1.5"/>',
           f'<rect class="tr" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" fill="none" stroke="{tono(c1, .25)}" '
           f'stroke-width="2.4" stroke-linecap="round" pathLength="1000" stroke-dasharray="120 880" style="animation-delay:-{num(indice * 1.3)}s"/>',
           f'<path d="{hexagono(62, 75, 36)}" fill="#0A1230" stroke="{c1}" stroke-width="2.6"/>',
           f'<path d="{hexagono(62, 75, 36)}" fill="{c1}" fill-opacity=".16"/>',
           icono(icono_nombre, 45, 58, 34, tono(c1, .3), 2.2))
    lineas = envolver(curso["nombre"], "titulo", 18, 330)[:2]
    for j, linea in enumerate(lineas):
        lz.add(neon(lz, "titulo", linea, 118, 44 + j * 24, 18, c1, retraso=indice * .7)[0])
    y = 44 + len(lineas) * 24 + 8
    lz.add(lz.texto("texto", f"{curso['emisor']} · {curso['fecha']}", 118, y,
                    lz.ajustar("texto", f"{curso['emisor']} · {curso['fecha']}", 440, 14.5), tono(c1, .7))[0],
           lz.texto("mono", curso["tipo"], 118, y + 22, lz.ajustar("mono", curso["tipo"], 330, 12), tono(c2, .45))[0])
    chip = "VERIFICAR" if curso.get("verificacion") else "CONSTANCIA PDF"
    ancho_c = Fuente.de("monob").ancho(chip, 11.5, .5) + 26
    lz.add(f'<rect x="{num(W - 22 - ancho_c)}" y="18" width="{num(ancho_c)}" height="26" rx="13" fill="{c1}" '
           f'fill-opacity="{.22 if curso.get("verificacion") else .08}" stroke="{c1}" stroke-opacity=".8"/>',
           lz.texto("monob", chip, W - 22 - ancho_c / 2, 35.5, 11.5, tono(c1, .35), .5, "middle")[0])
    lz.estilos.append(".tr{animation:tr 8s linear infinite}@keyframes tr{to{stroke-dashoffset:-1000}}" + SIN_MOVIMIENTO)
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  CAJAS DE TECNOLOGÍA (logo + nombre neón en el color de la tecnología)
#  Los logotipos vienen de skill-icons (MIT) y se incrustan desde scripts/iconos-skill/.
# ═════════════════════════════════════════════════════════════════════════════

ICONOS_SKILL = Path(__file__).resolve().parent / "iconos-skill"


def _logo_incrustado(nombre: str, x: float, y: float, lado: float) -> str:
    import re
    svg = (ICONOS_SKILL / f"{nombre}.svg").read_text(encoding="utf-8")
    interior = re.sub(r"^\s*<svg[^>]*>", "", svg.strip())
    interior = re.sub(r"</svg>\s*$", "", interior)
    xlink = ' xmlns:xlink="http://www.w3.org/1999/xlink"' if "xlink:" in interior else ""
    return (f'<svg x="{num(x)}" y="{num(y)}" width="{num(lado)}" height="{num(lado)}" viewBox="0 0 256 256" fill="none"{xlink}>'
            f'{interior}</svg>')


def caja_tecnologia(item: dict, color: str, indice: int, aprendiendo: bool = False) -> str:
    W, H = 168, 172
    c = color
    lz = Lienzo(W, H, item["nombre"], item.get("nota", ""))
    lz.defs.append(f'<clipPath id="zc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
                   + brillo("zg", c, .45)
                   + f'<linearGradient id="zf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mezclar("#070B1E", c, .16)}"/>'
                     f'<stop offset="1" stop-color="#070B1E"/></linearGradient>')
    lz.add(f'<g clip-path="url(#zc)"><rect width="{W}" height="{H}" fill="url(#zf)"/>',
           f'<circle cx="{W / 2}" cy="56" r="74" fill="url(#zg)"/></g>')
    borde = ' stroke-dasharray="7 5"' if aprendiendo else ""
    lz.add(f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16.5" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width="1.6"{borde}/>',
           f'<rect class="zr" x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16.5" fill="none" stroke="{tono(c, .3)}" stroke-width="2.4" '
           f'stroke-linecap="round" pathLength="1000" stroke-dasharray="90 910" style="animation-delay:-{num((indice * 1.37) % 9)}s"/>')
    lado = 70
    if item.get("skill"):
        logo = _logo_incrustado(item["skill"], W / 2 - lado / 2, 20, lado)
    else:
        k = lado / 256
        logo = (f'<g transform="translate({num(W / 2 - lado / 2)} 20)"><rect width="{lado}" height="{lado}" rx="{num(60 * k)}" fill="#242938"/>'
                + icono(item["generico"], 58 * k, 58 * k, 140 * k, tono(c, .15), 2.0) + "</g>")
    dur = 3.6 + (indice % 5) * 0.45
    lz.add(f'<g class="zf" style="animation-duration:{num(dur)}s;animation-delay:-{num((indice * .83) % dur)}s">{logo}</g>')
    nombre = item["nombre"]
    lineas = envolver(nombre, "titulo", 16, W - 18)
    if len(lineas) > 2:
        lineas = [nombre]
    tam = min(lz.ajustar("titulo", l, W - 16, 16) for l in lineas)
    y = 118 if len(lineas) == 1 else 112
    for j, linea in enumerate(lineas):
        lz.add(neon(lz, "titulo", linea, W / 2, y + j * 19, tam, c, ancla="middle", retraso=(indice * .61) % 3.8)[0])
    nota = item.get("nota") or ("aprendiendo" if aprendiendo else "")
    if nota:
        lz.add(lz.texto("mono", nota, W / 2, H - 16, lz.ajustar("mono", nota, W - 16, 11), tono(c, .45), ancla="middle")[0])
    lz.estilos.append(
        ".zr{animation:zr 9s linear infinite}@keyframes zr{to{stroke-dashoffset:-1000}}"
        ".zf{animation-name:zf;animation-iteration-count:infinite;animation-timing-function:ease-in-out;animation-direction:alternate}"
        "@keyframes zf{from{transform:translateY(0)}to{transform:translateY(-4px)}}" + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  EXPERIENCIA EN UNA SOLA PIEZA: línea de tiempo luminosa conectada a cajas animadas
# ═════════════════════════════════════════════════════════════════════════════

def experiencia_cajas(experiencia: list[dict]) -> str:
    puntos = list(reversed(experiencia))  # de la más antigua a la más reciente
    n = len(puntos)
    W, gap, mx = 1200, 18, 0
    ancho = (W - gap * (n - 1)) / n
    yl, top, H = 46, 96, 418
    lz = Lienzo(W, H, "Experiencia",
                " → ".join(f"{e['anio']}: {e['puesto']} en {e['empresa']}. " + " ".join(e.get("resumen", [])) for e in puntos))
    colores = [P[e.get("acento", "coral")] for e in puntos]
    centros = [i * (ancho + gap) + ancho / 2 for i in range(n)]
    lz.defs.append(
        f'<linearGradient id="xl" gradientUnits="userSpaceOnUse" x1="{num(centros[0])}" y1="0" x2="{num(centros[-1])}" y2="0">'
        + "".join(f'<stop offset="{num(i / max(1, n - 1))}" stop-color="{c}"/>' for i, c in enumerate(colores))
        + "</linearGradient>"
    )
    # línea de tiempo con pulso viajero
    lz.add(f'<path d="M{num(centros[0])} {yl}H{num(centros[-1])}" stroke="url(#xl)" stroke-width="12" stroke-opacity=".16" stroke-linecap="round"/>',
           f'<path d="M{num(centros[0])} {yl}H{num(centros[-1])}" stroke="url(#xl)" stroke-width="3" stroke-linecap="round"/>',
           f'<circle class="xp" cx="{num(centros[0])}" cy="{yl}" r="5" fill="#fff"/>')
    for i, e in enumerate(puntos):
        x = i * (ancho + gap)
        cx = centros[i]
        c1 = colores[i]
        c2 = P[PAREJA[e.get("acento", "coral")]]
        lz.defs.append(
            f'<clipPath id="xc{i}"><rect x="{num(x)}" y="{top}" width="{num(ancho)}" height="{H - top}" rx="16"/></clipPath>'
            + f'<linearGradient id="xf{i}" x1="0" y1="0" x2=".5" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".26"/>'
              f'<stop offset=".6" stop-color="{c2}" stop-opacity=".06"/><stop offset="1" stop-color="#070B1E" stop-opacity="0"/></linearGradient>'
            + brillo(f"xg{i}", c1, .55) + degradado(f"xb{i}", [c1, c2], 1, 1)
        )
        # nodo, año y conector
        lz.add(f'<circle cx="{num(cx)}" cy="{yl}" r="26" fill="url(#xg{i})"/>',
               f'<path class="yn" d="{hexagono(cx, yl, 21)}" fill="none" stroke="{c1}" stroke-opacity=".55" stroke-dasharray="4 4" style="animation-delay:-{i * .7}s"/>',
               f'<path d="{hexagono(cx, yl, 16)}" fill="#0A1230" stroke="{c1}" stroke-width="2.4"/>',
               f'<circle cx="{num(cx)}" cy="{yl}" r="4.5" fill="{c1}"/>',
               f'<path d="M{num(cx)} {yl + 18}V{top}" stroke="{c1}" stroke-width="2" stroke-dasharray="3 4" stroke-opacity=".8"/>',
               f'<circle class="xd" cx="{num(cx)}" cy="{yl + 18}" r="3" fill="{tono(c1, .3)}" style="animation-delay:-{num(i * .5)}s"/>')
        # caja
        lz.add(f'<g clip-path="url(#xc{i})"><rect x="{num(x)}" y="{top}" width="{num(ancho)}" height="{H - top}" fill="#080C22"/>',
               f'<rect x="{num(x)}" y="{top}" width="{num(ancho)}" height="{H - top}" fill="url(#xf{i})"/>',
               f'<circle cx="{num(x + ancho - 40)}" cy="{top + 40}" r="110" fill="url(#xg{i})" opacity=".55"/></g>',
               f'<rect x="{num(x + 1)}" y="{top + 1}" width="{num(ancho - 2)}" height="{H - top - 2}" rx="15" fill="none" stroke="url(#xb{i})" stroke-opacity=".6" stroke-width="1.6"/>',
               f'<rect class="tr" x="{num(x + 1)}" y="{top + 1}" width="{num(ancho - 2)}" height="{H - top - 2}" rx="15" fill="none" '
               f'stroke="{tono(c1, .25)}" stroke-width="2.6" stroke-linecap="round" pathLength="1000" stroke-dasharray="120 880" '
               f'style="animation-delay:-{num(i * 1.75)}s"/>')
        ix, iy = x + 22, top + 22
        lz.add(f'<path d="{hexagono(ix + 24, iy + 24, 25)}" fill="{c1}" fill-opacity=".18" stroke="{c1}" stroke-width="2.2"/>',
               icono(e.get("icono", "maletin"), ix + 11, iy + 11, 26, tono(c1, .3), 2.1))
        anio = e["anio"]
        ancho_a = Fuente.de("monob").ancho(anio, 13, .5) + 26
        lz.add(f'<rect x="{num(x + ancho - 20 - ancho_a)}" y="{top + 26}" width="{num(ancho_a)}" height="28" rx="14" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-opacity=".85"/>',
               lz.texto("monob", anio, x + ancho - 20 - ancho_a / 2, top + 44.5, 13, tono(c1, .35), .5, "middle")[0])
        empresa = e["empresa_corta"]
        tam = lz.ajustar("titulo", empresa, ancho - 44, 23)
        lz.add(neon(lz, "titulo", empresa, x + 22, top + 112, tam, c1, retraso=i * .9)[0])
        puesto = e.get("puesto_corto", e["puesto"])
        lz.add(lz.texto("mono", puesto, x + 22, top + 138, lz.ajustar("mono", puesto, ancho - 44, 13), tono(c2, .45))[0],
               f'<rect x="{num(x + 22)}" y="{top + 154}" width="34" height="3" rx="1.5" fill="{c1}"/>')
        y = top + 186
        for linea in e.get("resumen", []):
            for parte in envolver(linea, "texto", 15.5, ancho - 54):
                lz.add(lz.texto("texto", parte, x + 22, y, 15.5, tono(c1, .76))[0])
                y += 23
            y += 6
        lz.add(lz.texto("mono", e["lugar"].split(" · ")[0], x + 22, H - 20,
                        lz.ajustar("mono", e["lugar"].split(" · ")[0], ancho - 44, 11.5), tono(c1, .25))[0])
    lz.estilos.append(
        f".xp{{animation:xp 6s ease-in-out infinite}}@keyframes xp{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}"
        f"90%{{opacity:1}}100%{{transform:translateX({num(centros[-1] - centros[0])}px);opacity:0}}}}"
        f".xd{{animation:xd 2.2s ease-in infinite}}@keyframes xd{{from{{transform:translateY(0);opacity:1}}to{{transform:translateY({top - yl - 22}px);opacity:0}}}}"
        ".yn{transform-box:fill-box;transform-origin:center;animation:yn 3s ease-in-out infinite}"
        "@keyframes yn{0%,100%{transform:scale(.92);opacity:.4}50%{transform:scale(1.08);opacity:1}}"
        ".tr{animation:tr 8s linear infinite}@keyframes tr{to{stroke-dashoffset:-1000}}" + SIN_MOVIMIENTO
    )
    return lz.armar()
