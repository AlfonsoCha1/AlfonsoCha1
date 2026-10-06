"""Todas las imágenes del muro (SVG animados con CSS, sin JavaScript).

Cada función recibe datos de perfil.toml y devuelve el texto de un SVG.
"""

from __future__ import annotations

import math
import random

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

    colores_enfoque = [P["cian"], "#A78BFA", P["ambar"]]
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
    for texto, color in zip(per["complementos"], [P["cian"], "#A78BFA", "#F472D0"]):
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
#  ENCABEZADOS DE SECCIÓN
# ═════════════════════════════════════════════════════════════════════════════

def encabezado(titulo: str, nota: str, icono_nombre: str, acento: str, tema: str) -> tuple[str, int]:
    T = TEMAS[tema]
    c1, c2 = P[acento], P[PAREJA[acento]]
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
        lz.texto("titulo", titulo.upper(), x_t, 34, tam, T["texto"], espaciado=espaciado)[0],
        f'<rect x="{num(x1)}" y="24" width="{largo}" height="3" rx="1.5" fill="url(#el)" fill-opacity=".35"/>',
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
#  ÁREAS
# ═════════════════════════════════════════════════════════════════════════════

def ilustracion_area(tipo: str, x: float, y: float, c1: str, c2: str, i: int) -> str:
    """Ilustración en la parte superior derecha de cada tarjeta (x, y = esquina de la zona 170×140)."""
    p = []
    if tipo == "escudo":
        for k in range(3):  # racks de servidores
            rx = x + 6 + k * 34
            p.append(f'<rect x="{rx}" y="{y + 40 + k * 6}" width="28" height="{96 - k * 6}" rx="3" fill="#0B1538" stroke="{c1}" stroke-opacity=".45"/>')
            for j in range(5):
                yy = y + 50 + k * 6 + j * 15
                p.append(f'<rect x="{rx + 4}" y="{yy}" width="20" height="3" rx="1.5" fill="{c1}" fill-opacity=".35"/>')
                p.append(f'<circle class="led" cx="{rx + 22}" cy="{yy + 8}" r="1.6" fill="{c1}" style="animation-delay:-{(j + k) * .4}s"/>')
        sx, sy = x + 132, y + 22
        p.append(f'<path d="M{sx} {sy}l40 16v34c0 30-18 48-40 58-22-10-40-28-40-58V{sy + 16}Z" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-width="2.4"/>')
        p.append(f'<rect x="{sx - 15}" y="{sy + 54}" width="30" height="24" rx="4" fill="{c1}"/>')
        p.append(f'<path d="M{sx - 9} {sy + 54}v-8a9 9 0 0 1 18 0v8" fill="none" stroke="{c1}" stroke-width="3.2"/>')
        p.append(f'<circle cx="{sx}" cy="{sy + 64}" r="3.2" fill="#0B1538"/>')
    elif tipo == "red":
        for k in range(2):
            rx = x + 8 + k * 40
            p.append(f'<rect x="{rx}" y="{y + 28}" width="32" height="108" rx="3" fill="#0B1538" stroke="{c1}" stroke-opacity=".5"/>')
            for j in range(7):
                yy = y + 36 + j * 14
                p.append(f'<rect x="{rx + 4}" y="{yy}" width="18" height="3" rx="1.5" fill="{c2}" fill-opacity=".5"/>')
                p.append(f'<circle class="led" cx="{rx + 26}" cy="{yy + 1.5}" r="1.6" fill="{c1}" style="animation-delay:-{(j * 3 + k) * .3}s"/>')
        nodos = [(x + 128, y + 30), (x + 104, y + 82), (x + 156, y + 86), (x + 130, y + 128)]
        lineas = "".join(f"M{a[0]} {a[1]}L{b[0]} {b[1]}" for a, b in
                         [(nodos[0], nodos[1]), (nodos[0], nodos[2]), (nodos[1], nodos[2]), (nodos[1], nodos[3]), (nodos[2], nodos[3])])
        p.append(f'<path d="{lineas}" stroke="{c1}" stroke-width="2" stroke-opacity=".8"/>')
        for nx, ny in nodos:
            p.append(f'<circle cx="{nx}" cy="{ny}" r="9" fill="#0B1538" stroke="{c1}" stroke-width="2.4"/><circle cx="{nx}" cy="{ny}" r="3.4" fill="{c2}"/>')
    else:  # gestión
        cxg, cyg = x + 54, y + 62
        dientes = []
        for k in range(8):
            a = math.radians(k * 45)
            dientes.append(f"M{num(cxg + 26 * math.cos(a))} {num(cyg + 26 * math.sin(a))}L{num(cxg + 38 * math.cos(a))} {num(cyg + 38 * math.sin(a))}")
        p.append(f'<g class="gir" style="transform-origin:{num(cxg)}px {num(cyg)}px">'
                 f'<circle cx="{cxg}" cy="{cyg}" r="27" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-width="3"/>'
                 f'<path d="{"".join(dientes)}" stroke="{c1}" stroke-width="8" stroke-linecap="round"/>'
                 f'<circle cx="{cxg}" cy="{cyg}" r="9" fill="none" stroke="{c1}" stroke-width="3"/></g>')
        for k, h in enumerate([28, 46, 64, 88]):
            bx = x + 104 + k * 16
            p.append(f'<rect class="bc" x="{bx}" y="{y + 136 - h}" width="11" height="{h}" rx="2" fill="{c1 if k == 3 else c2}" '
                     f'fill-opacity="{.95 if k == 3 else .6}" style="animation-delay:-{k * .5}s"/>')
        p.append(f'<path d="M{x + 98} {y + 136}h74" stroke="{c1}" stroke-opacity=".6" stroke-width="1.5"/>')
    return "".join(p)


def areas(perfil: dict) -> str:
    lista = perfil["areas"]
    W, H = 1200, 300
    lz = Lienzo(W, H, "Áreas: " + ", ".join(a["titulo"] for a in lista),
                " · ".join(a["titulo"] + ": " + " ".join(a["lema"]) for a in lista))
    gap = 24
    ancho = (W - gap * (len(lista) - 1)) / len(lista)
    for i, area in enumerate(lista):
        x = i * (ancho + gap)
        c1, c2 = P[area["acento"]], P[PAREJA[area["acento"]]]
        lz.defs.append(
            f'<linearGradient id="af{i}" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".30"/>'
            f'<stop offset=".55" stop-color="{c2}" stop-opacity=".08"/><stop offset="1" stop-color="#0A1026" stop-opacity="0"/></linearGradient>'
            + degradado(f"ab{i}", [c1, c2], 1, 1) + brillo(f"ag{i}", c1, .45)
            + f'<clipPath id="ac{i}"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" rx="18"/></clipPath>'
        )
        lz.add(
            f'<g clip-path="url(#ac{i})"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="#0A1026"/>',
            f'<rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="url(#af{i})"/>',
            f'<circle cx="{num(x + ancho - 90)}" cy="90" r="130" fill="url(#ag{i})"/>',
            ilustracion_area(area["icono"], x + ancho - 196, 18, c1, c2, i),
            f'<rect class="br" x="{num(x - 300)}" y="0" width="300" height="{H}" fill="url(#brl)" style="animation-delay:-{i * 3}s"/></g>',
            f'<rect x="{num(x + .75)}" y=".75" width="{num(ancho - 1.5)}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#ab{i})" stroke-width="1.5" stroke-opacity=".85"/>',
            f'<rect x="{num(x + 24)}" y="26" width="52" height="52" rx="14" fill="url(#ab{i})"/>',
            icono(area["icono"], x + 36, 38, 28, "#fff", 2.2),
            lz.texto("mono", f"0{i + 1}", x + 24, 108, 12, c1, 1)[0],
        )
        tam = lz.ajustar("titulo", area["titulo"], ancho - 48, 28)
        lz.add(lz.texto("titulo", area["titulo"], x + 24, 210, tam, P["texto"])[0])
        for j, linea in enumerate(area["lema"]):
            lz.add(lz.texto("texto", linea, x + 24, 244 + j * 24, 16, P["suave"])[0])
    lz.defs.append('<linearGradient id="brl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                   '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    lz.estilos.append(
        ".br{animation:br 9s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes br{0%{transform:translateX(0)}55%,100%{transform:translateX(760px)}}"
        ".led{animation:led 2.4s steps(2,start) infinite}@keyframes led{to{opacity:.2}}"
        ".gir{animation:gir 14s linear infinite}@keyframes gir{to{transform:rotate(360deg)}}"
        ".bc{transform-box:fill-box;transform-origin:bottom;animation:bc 3s ease-in-out infinite alternate}"
        "@keyframes bc{from{transform:scaleY(.7)}to{transform:scaleY(1)}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  LO QUE SÉ (tecnologías)
# ═════════════════════════════════════════════════════════════════════════════

def lo_que_se(grupos: list[dict]) -> str:
    W = 1200
    pad, gap, cols = 30, 12, 9
    tw = (W - 2 * pad - gap * (cols - 1)) / cols
    th = 128
    filas = sorted({g["fila"] for g in grupos})
    alto_fila = 26 + th
    H = 62 + len(filas) * alto_fila + (len(filas) - 1) * 24 + 26
    todos = [it["nombre"] for g in grupos for it in g["items"]]
    lz = Lienzo(W, H, "Lo que sé", "Tecnologías: " + ", ".join(todos))
    rnd = random.Random(3)
    lz.defs.append(
        f'<clipPath id="lc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("lf", ["#060B22", "#0A0D2E", "#120A30"], 1, 1)
        + degradado("lb", ["#22D3EE", "#3B82F6", "#8B5CF6", "#E14FD0"], 1, 0)
        + '<pattern id="lr" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#0F1A40"/></pattern>'
        + '<linearGradient id="lsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7DF3FF" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="#7DF3FF" stop-opacity=".16"/><stop offset="1" stop-color="#7DF3FF" stop-opacity="0"/></linearGradient>'
        + brillo("lg1", "#3B82F6", .22) + brillo("lg2", "#E14FD0", .16)
    )
    lz.add(
        f'<g clip-path="url(#lc)"><rect width="{W}" height="{H}" fill="url(#lf)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#lr)" opacity=".8"/>',
        f'<circle cx="180" cy="{H}" r="420" fill="url(#lg1)"/><circle cx="{W - 120}" cy="40" r="360" fill="url(#lg2)"/>',
    )
    lz.add(lz.texto("monob", "STACK.SYS", pad, 38, 13, P["cian"], 1.5)[0],
           lz.texto("mono", "// tecnologías que uso y que estoy aprendiendo", pad + 92, 38, 12.5, P["tenue"])[0])
    # leyenda
    lx = W - pad
    s, w = lz.texto("mono", "aprendiendo", lx, 38, 12, P["suave"], ancla="end")
    lz.add(s, f'<rect x="{num(lx - w - 22)}" y="27" width="13" height="13" rx="3" fill="none" stroke="{P["verde"]}" stroke-dasharray="3 2"/>')
    lx2 = lx - w - 40
    s, w2 = lz.texto("mono", "experiencia", lx2, 38, 12, P["suave"], ancla="end")
    lz.add(s, f'<rect x="{num(lx2 - w2 - 22)}" y="27" width="13" height="13" rx="3" fill="{P["cian"]}" fill-opacity=".25" stroke="{P["cian"]}"/>')

    css = []
    y_fila = 62
    indice = 0
    for fila in filas:
        col = 0
        for g in [g for g in grupos if g["fila"] == fila]:
            acento = P[g["acento"]]
            n = len(g["items"])
            gx = pad + col * (tw + gap)
            gw = n * tw + (n - 1) * gap
            etiqueta = g["grupo"].upper()
            lz.add(f'<rect x="{num(gx)}" y="{y_fila + 4}" width="8" height="8" rx="2" fill="{acento}"/>',
                   lz.texto("monob", etiqueta, gx + 16, y_fila + 13, 11.5, acento, 1.4)[0])
            ancho_eti = Fuente.de("monob").ancho(etiqueta, 11.5, 1.4)
            lz.add(f'<path d="M{num(gx + 26 + ancho_eti)} {y_fila + 8.5}H{num(gx + gw)}" stroke="{acento}" stroke-opacity=".35"/>')
            for it in g["items"]:
                tx = pad + col * (tw + gap)
                ty = y_fila + 26
                color = it["color"]
                aprende = g.get("aprendiendo", False)
                gid = f"t{indice}"
                lz.defs.append(
                    f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity=".26"/>'
                    f'<stop offset=".6" stop-color="{color}" stop-opacity=".05"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
                    + brillo(f"h{indice}", color, .55)
                )
                borde = (f'stroke="{color}" stroke-opacity=".8" stroke-dasharray="5 4"' if aprende
                         else f'stroke="{color}" stroke-opacity=".6"')
                lz.add(f'<rect x="{num(tx)}" y="{ty}" width="{num(tw)}" height="{th}" rx="14" fill="#0A1230"/>',
                       f'<rect x="{num(tx)}" y="{ty}" width="{num(tw)}" height="{th}" rx="14" fill="url(#{gid})" {borde} stroke-width="1.3"/>')
                hcx, hcy = tx + tw / 2, ty + 48
                dur = rnd.uniform(3.5, 6)
                lz.add(f'<circle class="hl" cx="{num(hcx)}" cy="{hcy}" r="40" fill="url(#h{indice})" '
                       f'style="animation-duration:{num(dur)}s;animation-delay:-{num(rnd.uniform(0, dur))}s"/>',
                       f'<path d="{hexagono(hcx, hcy, 30)}" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-width="2"/>',
                       f'<path d="{hexagono(hcx, hcy, 36)}" fill="none" stroke="{color}" stroke-opacity=".3" stroke-dasharray="4 5"/>')
                glifo = it["glifo"]
                tam_g = lz.ajustar("titulo", glifo, 40, 22)
                color_glifo = it.get("color_glifo", mezclar(color, "#FFFFFF", .25))
                lz.add(lz.texto("titulo", glifo, hcx, hcy + tam_g * .36, tam_g, color_glifo, ancla="middle")[0])
                tam_n = lz.ajustar("texto", it["nombre"], tw - 14, 15)
                lz.add(lz.texto("texto", it["nombre"], hcx, ty + 104, tam_n, P["texto"], ancla="middle")[0])
                if aprende:
                    lz.add(lz.texto("mono", "aprendiendo", hcx, ty + 120, 10, P["verde"], ancla="middle")[0])
                else:
                    lz.add(f'<rect x="{num(hcx - 14)}" y="{ty + 114}" width="28" height="3" rx="1.5" fill="{color}" fill-opacity=".9"/>')
                col += 1
                indice += 1
        # haz de luz que recorre la fila
        dur = 6 + fila
        lz.add(f'<rect class="lsw" x="-240" y="{y_fila + 26}" width="240" height="{th}" fill="url(#lsw)" '
               f'style="animation-duration:{dur}s;animation-delay:-{fila * 1.6}s"/>')
        y_fila += alto_fila + 24
    lz.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#lb)" stroke-opacity=".55" stroke-width="1.5"/></g>')
    css.append(".hl{animation-name:hl;animation-iteration-count:infinite;animation-timing-function:ease-in-out}"
               "@keyframes hl{0%,100%{opacity:.25}50%{opacity:1}}"
               ".lsw{animation-name:lsw;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.5,0,.3,1)}"
               f"@keyframes lsw{{0%{{transform:translateX(0)}}70%,100%{{transform:translateX({W + 480}px)}}}}" + SIN_MOVIMIENTO)
    lz.estilos.append("".join(css))
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  FORMACIÓN (tarjetas doradas)
# ═════════════════════════════════════════════════════════════════════════════

def formacion(tarjetas: list[dict]) -> str:
    W, H = 1200, 300
    lz = Lienzo(W, H, "Formación", " · ".join(" ".join(t["titulo"]) + " (" + t["detalle"] + ", " + t["periodo"] + ")" for t in tarjetas))
    n = len(tarjetas)
    gap = 20
    ancho = (W - gap * (n - 1)) / n
    oro, oro2, cobre = "#F5B544", "#FFD98A", "#E07B39"
    rnd = random.Random(11)
    lz.defs.append(
        degradado("fo", [oro2, oro, cobre], 1, 1)
        + '<linearGradient id="ff" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5B544" stop-opacity=".30"/>'
          '<stop offset=".5" stop-color="#E07B39" stop-opacity=".08"/><stop offset="1" stop-color="#0A0E22" stop-opacity="0"/></linearGradient>'
        + brillo("fg", oro, .5)
        + '<linearGradient id="fsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE7B0" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="#FFE7B0" stop-opacity=".16"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></linearGradient>'
    )
    for i, t in enumerate(tarjetas):
        x = i * (ancho + gap)
        lz.defs.append(f'<clipPath id="fc{i}"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" rx="16"/></clipPath>')
        # circuitos de fondo
        circuito = []
        for k in range(7):
            yy = rnd.randint(30, 170)
            xx = x + rnd.uniform(ancho * .45, ancho - 20)
            largo = rnd.randint(30, 90)
            circuito.append(f"M{num(xx)} {yy}h{largo}v{rnd.choice([-1, 1]) * rnd.randint(10, 30)}")
        lz.add(
            f'<g clip-path="url(#fc{i})"><rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="#0B0F24"/>',
            f'<rect x="{num(x)}" y="0" width="{num(ancho)}" height="{H}" fill="url(#ff)"/>',
            f'<circle cx="{num(x + ancho * .72)}" cy="70" r="120" fill="url(#fg)"/>',
            f'<path d="{"".join(circuito)}" fill="none" stroke="{oro}" stroke-opacity=".28" stroke-width="1.4"/>',
            f'<rect class="fsw" x="{num(x - 260)}" y="0" width="260" height="{H}" fill="url(#fsw)" style="animation-delay:-{i * 2.2}s"/></g>',
            f'<rect x="{num(x + .75)}" y=".75" width="{num(ancho - 1.5)}" height="{H - 1.5}" rx="16" fill="none" stroke="url(#fo)" stroke-width="1.5" stroke-opacity=".9"/>',
        )
        icx, icy = x + ancho * .72, 84
        lz.add(f'<path d="{hexagono(icx, icy, 46)}" fill="{oro}" fill-opacity=".14" stroke="url(#fo)" stroke-width="2.2"/>',
               f'<path class="fpu" d="{hexagono(icx, icy, 56)}" fill="none" stroke="{oro}" stroke-opacity=".5" stroke-dasharray="5 6" style="animation-delay:-{i}s"/>',
               icono(t["icono"], icx - 22, icy - 22, 44, oro2, 2.2))
        lz.add(lz.texto("monob", f"0{i + 1}", x + 22, 42, 13, oro, 1.5)[0])
        y_t = 182
        tam = min(lz.ajustar("titulo", linea, ancho - 40, 21) for linea in t["titulo"])
        for j, linea in enumerate(t["titulo"]):
            lz.add(lz.texto("titulo", linea, x + 22, y_t + j * 26, tam, "#FFF4DD")[0])
        lz.add(lz.texto("texto", t["detalle"], x + 22, 254, lz.ajustar("texto", t["detalle"], ancho - 40, 14.5), "#E8CFA0")[0],
               lz.texto("mono", t["periodo"], x + 22, 278, 12.5, oro)[0])
    lz.estilos.append(
        ".fsw{animation:fsw 8s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes fsw{0%{transform:translateX(0)}60%,100%{transform:translateX(560px)}}"
        ".fpu{transform-box:fill-box;transform-origin:center;animation:fpu 20s linear infinite}"
        "@keyframes fpu{to{transform:rotate(360deg)}}" + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  TRAYECTORIA (línea de tiempo de experiencia)
# ═════════════════════════════════════════════════════════════════════════════

def trayectoria(experiencia: list[dict]) -> str:
    puntos = list(reversed(experiencia))  # de la más antigua a la más reciente
    W, H = 1200, 210
    lz = Lienzo(W, H, "Trayectoria", " → ".join(f"{e['anio']}: {e['puesto']} en {e['empresa_corta']}" for e in puntos))
    colores = [P["cian"], P["azul"], P["violeta"], P["magenta"], P["ambar"]]
    x0, x1, yl = 110, W - 110, 92
    lz.defs.append(
        f'<clipPath id="yc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("yf", ["#060B22", "#0B0A2C"], 1, 1)
        + f'<linearGradient id="yl" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">'
        + "".join(f'<stop offset="{num(i / max(1, len(puntos) - 1))}" stop-color="{c}"/>'
                  for i, c in enumerate(colores[:max(2, len(puntos))]))
        + "</linearGradient>"
        + degradado("ylb", [colores[0], colores[min(len(puntos), len(colores)) - 1]], 1, 0)
        + brillo("yb1", "#3B82F6", .18) + brillo("yb2", "#E14FD0", .14)
    )
    lz.add(f'<g clip-path="url(#yc)"><rect width="{W}" height="{H}" fill="url(#yf)"/>',
           f'<circle cx="200" cy="{H}" r="300" fill="url(#yb1)"/><circle cx="{W - 200}" cy="0" r="300" fill="url(#yb2)"/>',
           f'<path d="M{x0} {yl}H{x1}" stroke="url(#yl)" stroke-width="3" stroke-linecap="round"/>',
           f'<path d="M{x0} {yl}H{x1}" stroke="url(#yl)" stroke-width="12" stroke-opacity=".15"/>',
           f'<circle class="yp" cx="{x0}" cy="{yl}" r="5" fill="#fff"/>')
    paso = (x1 - x0) / max(1, len(puntos) - 1)
    for i, e in enumerate(puntos):
        x = x0 + i * paso
        c = colores[i % len(colores)]
        lz.defs.append(brillo(f"yg{i}", c, .6))
        lz.add(f'<circle cx="{num(x)}" cy="{yl}" r="30" fill="url(#yg{i})"/>',
               f'<circle cx="{num(x)}" cy="{yl}" r="12" fill="#0A1230" stroke="{c}" stroke-width="3"/>',
               f'<circle class="yn" cx="{num(x)}" cy="{yl}" r="5" fill="{c}" style="animation-delay:-{i * .6}s"/>',
               lz.texto("monob", e["anio"], x, yl - 34, 15, c, 1, "middle")[0])
        tam = lz.ajustar("titulo", e["empresa_corta"], paso - 24 if len(puntos) > 1 else 300, 19)
        lz.add(lz.texto("titulo", e["empresa_corta"], x, yl + 52, tam, P["texto"], ancla="middle")[0])
        puesto = e.get("puesto_corto", e["puesto"])
        tam_p = lz.ajustar("mono", puesto, paso - 20 if len(puntos) > 1 else 300, 12.5)
        lz.add(lz.texto("mono", puesto, x, yl + 76, tam_p, P["suave"], ancla="middle")[0])
    lz.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="url(#ylb)" stroke-opacity=".5" stroke-width="1.5"/></g>')
    lz.estilos.append(
        f".yp{{animation:yp 6s ease-in-out infinite}}@keyframes yp{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}"
        f"90%{{opacity:1}}100%{{transform:translateX({x1 - x0}px);opacity:0}}}}"
        ".yn{transform-box:fill-box;transform-origin:center;animation:yn 2.4s ease-in-out infinite}"
        "@keyframes yn{0%,100%{transform:scale(.7)}50%{transform:scale(1.25)}}" + SIN_MOVIMIENTO
    )
    return lz.armar()


# ═════════════════════════════════════════════════════════════════════════════
#  PORTADAS DE PROYECTOS
# ═════════════════════════════════════════════════════════════════════════════

def motivo(tipo: str, c1: str, c2: str, rnd: random.Random) -> str:
    """Ilustración de la portada en la zona derecha (x 340–620, y 50–280)."""
    st = (lambda g=2.6, f="none", o=None:
          f'fill="{f}"' + (f' fill-opacity="{o}"' if o is not None else "")
          + f' stroke="{c1}" stroke-width="{g}" stroke-linecap="round" stroke-linejoin="round"')
    p = []
    if tipo == "escudo":
        for i in range(7):
            y = 88 + i * 24
            marca = ["#F87171", "#F5B544", "#34D399", "#3B82F6"][i % 4]
            p.append(f'<circle cx="356" cy="{y}" r="4.5" fill="{marca}"/>')
            p.append(f'<rect x="368" y="{y - 4}" width="{rnd.randint(70, 140)}" height="8" rx="4" fill="{c2}" fill-opacity=".45"/>')
        p.append('<rect class="mscan" x="344" y="80" width="200" height="26" rx="6" fill="#22D3EE" fill-opacity=".14" stroke="#22D3EE" stroke-opacity=".5"/>')
        cx, top = 552, 62
        p.append(f'<path d="M{cx} {top}L{cx + 64} {top + 26}V{top + 94}C{cx + 64} {top + 142} {cx + 32} {top + 170} {cx} {top + 186}'
                 f'C{cx - 32} {top + 170} {cx - 64} {top + 142} {cx - 64} {top + 94}V{top + 26}Z" {st(3, c1, ".16")}/>')
        p.append(f'<circle cx="{cx - 4}" cy="{top + 88}" r="26" {st(3.2, "#0A1230", ".7")}/><path d="M{cx + 14} {top + 106}L{cx + 36} {top + 128}" {st(5)}/>')
    elif tipo == "logs":
        p.append(f'<rect x="346" y="58" width="270" height="206" rx="12" fill="#050A1E" stroke="{c1}" stroke-opacity=".6" stroke-width="1.5"/>')
        p.append('<circle cx="362" cy="74" r="4" fill="#F87171"/><circle cx="375" cy="74" r="4" fill="#F5B544"/><circle cx="388" cy="74" r="4" fill="#34D399"/>')
        for i in range(8):
            y = 96 + i * 18
            a, b = rnd.randint(28, 48), rnd.randint(40, 118)
            sosp = i in (3, 4, 5)
            p.append(f'<rect x="360" y="{y}" width="{a}" height="7" rx="3" fill="{c2}" fill-opacity=".5"/>')
            p.append(f'<rect x="{366 + a}" y="{y}" width="{b}" height="7" rx="3" fill="{"#F87171" if sosp else c1}" fill-opacity="{.95 if sosp else .55}"/>')
        p.append(f'<path d="M354 146h-5v54h5M606 146h5v54h-5" {st(2.4, "none")}/>')
        for i, h in enumerate([10, 14, 9, 18, 36, 44, 14, 8]):
            p.append(f'<rect class="mbar" x="{528 + i * 9}" y="{248 - h}" width="6" height="{h}" fill="{"#F87171" if h > 30 else c1}" style="animation-delay:-{i * .3}s"/>')
        p.append(f'<rect class="mcur" x="360" y="240" width="9" height="12" fill="{c1}"/>')
    elif tipo == "ia":
        cx, cy = 500, 160
        p.append(f'<circle cx="{cx}" cy="{cy}" r="98" fill="none" stroke="{c2}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 7"/>')
        p.append(f'<circle class="mgir" cx="{cx}" cy="{cy}" r="70" fill="none" stroke="{c1}" stroke-opacity=".8" stroke-width="2.4" stroke-dasharray="40 14"/>')
        p.append(f'<circle cx="{cx}" cy="{cy}" r="42" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-width="2.4"/>')
        p.append(f'<circle class="mpul" cx="{cx}" cy="{cy}" r="22" fill="{c1}"/>')
        for ang, r, col in ((20, 98, c2), (140, 70, "#22D3EE"), (250, 98, c1), (320, 70, c2), (80, 98, "#22D3EE")):
            a = math.radians(ang)
            p.append(f'<rect x="{num(cx + math.cos(a) * r - 5)}" y="{num(cy + math.sin(a) * r - 5)}" width="10" height="10" rx="2" fill="{col}"/>')
        for i in range(9):
            h = [10, 22, 36, 18, 44, 26, 14, 30, 12][i]
            p.append(f'<rect class="mbar" x="{562 + i * 7}" y="{160 - h / 2}" width="4" height="{h}" rx="2" fill="#22D3EE" style="animation-delay:-{i * .2}s"/>')
    elif tipo == "voz":
        p.append(f'<rect x="372" y="78" width="48" height="96" rx="24" {st(3, c1, ".18")}/>')
        p.append(f'<path d="M356 140c0 40 80 40 80 0M396 180v26M376 208h40" {st(3)}/>')
        for i in range(17):
            h = 10 + abs(math.sin(i * 0.9)) * 64
            p.append(f'<rect class="mbar" x="{452 + i * 9.5}" y="{num(144 - h / 2)}" width="5.5" height="{num(h)}" rx="2.7" '
                     f'fill="{c1 if i % 2 else c2}" style="animation-delay:-{num(i * .17)}s"/>')
        p.append(f'<rect x="466" y="202" width="132" height="46" rx="12" fill="#050A1E" stroke="{c2}" stroke-opacity=".8"/>')
        p.append(f'<rect x="482" y="218" width="70" height="6" rx="3" fill="{c1}"/><rect x="482" y="230" width="44" height="6" rx="3" fill="{c2}" fill-opacity=".6"/>')
    elif tipo == "tienda":
        p.append(f'<rect x="360" y="60" width="180" height="204" rx="14" fill="#0A0A22" stroke="{c1}" stroke-opacity=".6"/>')
        p.append(f'<path d="M410 102l24-15h30l24 15 20 24-20 13-9-9v76h-80v-76l-9 9-20-13z" {st(3, c1, ".2")}/>')
        p.append(f'<rect x="380" y="228" width="84" height="9" rx="4.5" fill="{c2}" fill-opacity=".7"/><rect x="380" y="244" width="46" height="9" rx="4.5" fill="{c1}"/>')
        p.append(f'<circle class="mpul" cx="576" cy="108" r="32" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-width="2.6"/>')
        p.append(f'<path d="M558 98h7l7 19h18l6-13h-27M572 126a2.4 2.4 0 1 0 .1 0M586 126a2.4 2.4 0 1 0 .1 0" {st(2.4)}/>')
        p.append(f'<path d="M552 184h52l12 12-12 12h-52z" fill="{c2}" fill-opacity=".25" stroke="{c2}" stroke-width="2"/><circle cx="564" cy="196" r="3.5" fill="{c2}"/>')
    elif tipo == "lealtad":
        p.append(f'<rect x="350" y="82" width="200" height="126" rx="16" fill="#050A1E" stroke="{c1}" stroke-width="2"/>')
        p.append(f'<rect x="368" y="100" width="74" height="8" rx="4" fill="{c2}" fill-opacity=".7"/>')
        for i in range(8):
            fx, fy = 380 + (i % 4) * 34, 138 + (i // 4) * 34
            lleno = i < 5
            clase = ' class="msel"' if lleno else ""
            p.append(f'<circle{clase} cx="{fx}" cy="{fy}" r="12" fill="{c1 if lleno else "none"}" stroke="{c1}" stroke-width="2.2" style="animation-delay:{i * .35}s"/>')
        qx, qy, qs = 526, 150, 86
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
        p.append(f'<rect x="350" y="66" width="260" height="190" rx="12" fill="#050A1E" stroke="{c1}" stroke-opacity=".6"/>')
        p.append(f'<rect x="370" y="114" width="100" height="12" rx="6" fill="{c1}"/>')
    return "".join(p)


def portada(proyecto: dict, indice: int) -> str:
    W, H = 640, 300
    acento = proyecto.get("acento", "cian")
    c1 = P[acento]
    c2 = P[proyecto.get("acento2", PAREJA[acento])]
    lz = Lienzo(W, H, f"Portada de {proyecto['nombre']}", f"{proyecto['categoria']} · {proyecto['estado']}")
    rnd = random.Random(proyecto["id"])
    lz.defs.append(
        f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + degradado("pf", ["#050816", mezclar("#050816", c2, .18), mezclar("#050816", c1, .28)], 1, 1)
        + brillo("pg1", c1, .55, .15) + brillo("pg2", c2, .4)
        + degradado("pb", [c1, c2], 1, 1) + degradado("pn", [c1, c2], 1, 0)
        + '<pattern id="pr" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>'
        + '<linearGradient id="psw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    )
    # piso en perspectiva bajo la ilustración
    vx, yh = 480, 236
    lineas = "".join(f"M{vx + i * 3} {yh}L{vx + i * 44} {H}" for i in range(-8, 9))
    lineas += "".join(f"M300 {yh + d}H{W}" for d in (5, 13, 25, 42, 64))
    lz.add(
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="url(#pf)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#pr)"/>',
        f'<circle cx="500" cy="150" r="230" fill="url(#pg1)"/><circle cx="60" cy="300" r="220" fill="url(#pg2)"/>',
        f'<path d="{lineas}" stroke="{c1}" stroke-opacity=".22" fill="none"/>',
        motivo(proyecto.get("portada", "web"), c1, c2, rnd),
        f'<rect class="psw" x="-260" y="0" width="260" height="{H}" fill="url(#psw)"/></g>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#pb)" stroke-width="2"/>',
    )
    lz.add(lz.texto("mono", f"proyecto/{indice:02d}", 28, 42, 12.5, mezclar(c1, "#FFFFFF", .3))[0])
    numero, _ = lz.texto("titulo", f"{indice:02d}", 24, 150, 96, "#fff")
    lz.defs.append(f'<mask id="pm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{numero}</mask>')
    lz.add(f'<rect x="20" y="70" width="150" height="90" fill="url(#pn)" fill-opacity=".55" mask="url(#pm)"/>')
    etiqueta = proyecto.get("etiqueta", proyecto["estado"])
    ancho_et = Fuente.de("monob").ancho(etiqueta, 12, 0.5)
    lz.add(f'<rect x="{num(W - 28 - ancho_et - 26)}" y="22" width="{num(ancho_et + 26)}" height="28" rx="14" '
           f'fill="{c1}" fill-opacity=".18" stroke="{c1}"/>',
           lz.texto("monob", etiqueta, W - 41, 40.5, 12, mezclar(c1, "#FFFFFF", .35), 0.5, "end")[0])
    lz.add(lz.texto("monob", proyecto["categoria"].upper(), 28, 190, 12.5, mezclar(c1, "#FFFFFF", .2), 1.2)[0])
    nombre = proyecto["nombre"]
    tam = lz.ajustar("titulo", nombre, 310, 34)
    if tam < 27 and " — " in nombre:
        l1, l2 = nombre.split(" — ", 1)
        tam = min(lz.ajustar("titulo", l1, 310, 29), lz.ajustar("titulo", l2, 310, 29))
        lz.add(lz.texto("titulo", l1, 26, 222, tam, "#FFFFFF")[0],
               lz.texto("titulo", l2, 26, 222 + tam * 1.08, tam, mezclar(c1, "#FFFFFF", .45))[0])
    else:
        lz.add(lz.texto("titulo", nombre, 26, 236, tam, "#FFFFFF")[0])
    tecnologias = "  ·  ".join(proyecto.get("tecnologias", []))
    if tecnologias:
        lz.add(lz.texto("mono", tecnologias, 28, 280, lz.ajustar("mono", tecnologias, 300, 12.5), "#B9C5E6")[0])
    lz.estilos.append(
        ".psw{animation:psw 8s cubic-bezier(.5,0,.3,1) infinite}"
        "@keyframes psw{0%{transform:translateX(0)}60%,100%{transform:translateX(920px)}}"
        ".mscan{animation:mscan 4s ease-in-out infinite alternate}@keyframes mscan{to{transform:translateY(144px)}}"
        ".mbar{transform-box:fill-box;transform-origin:center bottom;animation:mbar 1.6s ease-in-out infinite alternate}"
        "@keyframes mbar{from{transform:scaleY(.45)}to{transform:scaleY(1)}}"
        ".mcur{animation:mcur 1.1s steps(2,start) infinite}@keyframes mcur{to{opacity:0}}"
        ".mgir{transform-box:fill-box;transform-origin:center;animation:mgir 12s linear infinite}@keyframes mgir{to{transform:rotate(360deg)}}"
        ".mpul{transform-box:fill-box;transform-origin:center;animation:mpul 2.6s ease-in-out infinite}"
        "@keyframes mpul{0%,100%{transform:scale(.85)}50%{transform:scale(1.08)}}"
        ".msel{animation:msel 5s ease-out infinite both}@keyframes msel{0%{opacity:.15}12%,85%{opacity:1}100%{opacity:.15}}"
        + SIN_MOVIMIENTO
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
