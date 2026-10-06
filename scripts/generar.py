#!/usr/bin/env python3
"""Genera el README del perfil y todas sus imágenes a partir de perfil.toml.

Uso
    python scripts/generar.py              genera README.md y assets/
    python scripts/generar.py --verificar  solo revisa que todo esté al día (no escribe)

Requisitos: Python 3.11 o superior. Solo usa la biblioteca estándar: no necesita
paquetes, fuentes instaladas ni internet. El texto de las imágenes se dibuja como
trazos (scripts/fuentes/*.json), así se ve igual en cualquier equipo.

El resultado es reproducible: con el mismo perfil.toml siempre sale lo mismo.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import random
import sys
import tomllib
from pathlib import Path
from xml.etree import ElementTree

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "perfil.toml"
README = RAIZ / "README.md"
ASSETS = RAIZ / "assets"
FUENTES = Path(__file__).resolve().parent / "fuentes"
PARTICULAS = ASSETS / "fuente" / "particulas.json"

MANUAL_INI = "<!-- MANUAL:INICIO -->"
MANUAL_FIN = "<!-- MANUAL:FIN -->"

# ─────────────────────────────────────────────────────────────────────────────
#  Paleta
# ─────────────────────────────────────────────────────────────────────────────

OSCURO = {
    "fondo": "#070B14", "panel": "#0B1220", "panel2": "#0F1A2E",
    "linea": "#1B2943", "linea2": "#2A3B5F", "rejilla": "#101B30",
    "texto": "#E6EDF7", "suave": "#9AA9C2", "tenue": "#5E6F8C",
    "cian": "#22D3EE", "violeta": "#8B5CF6", "azul": "#3B82F6",
    "verde": "#34D399", "ambar": "#F5B544", "rojo": "#F87171",
}
CLARO = {
    "fondo": "#FFFFFF", "panel": "#F6F8FB", "panel2": "#EEF2F7",
    "linea": "#D5DDE8", "linea2": "#B8C4D6", "rejilla": "#E9EEF5",
    "texto": "#0B1220", "suave": "#3E4C63", "tenue": "#66758E",
    "cian": "#0E7490", "violeta": "#6D28D9", "azul": "#1D4ED8",
    "verde": "#047857", "ambar": "#B45309", "rojo": "#B91C1C",
}
TEMAS = {"oscuro": OSCURO, "claro": CLARO}

# Colores de las partículas por figura (de oscuro a brillante)
PARTICULAS_COLORES = {
    "rostro": ["#5B3FD6", "#6D4CF2", "#5A6CF6", "#3B82F6", "#2BA3F2", "#22C3EA", "#5EE6F0", "#D2FAFF"],
    "ac": ["#1E6F8F", "#1F8FA8", "#22B3C4", "#22D3EE", "#2EE6C8", "#34D399", "#7CF0C2", "#D8FFF0"],
    "escudo": ["#3D2FA8", "#4B3DCC", "#5B5BF0", "#6C7BFA", "#4F9DF7", "#3BC3F2", "#7FDBFA", "#E0F2FF"],
}
OPACIDADES = [0.55, 0.62, 0.7, 0.78, 0.85, 0.92, 0.96, 1]

SIN_MOVIMIENTO = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def num(valor: float, decimales: int = 2) -> str:
    texto = f"{valor:.{decimales}f}".rstrip("0").rstrip(".")
    return "0" if texto in ("-0", "") else texto


def esc(texto: str) -> str:
    return html.escape(str(texto), quote=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Texto dibujado como trazos SVG
# ─────────────────────────────────────────────────────────────────────────────

FALTANTES: set[str] = set()  # caracteres que la tipografía no trae (se dibujan como «?»)


class Fuente:
    ARCHIVOS = {
        "titulo": ("t", "space-grotesk-700.json"),
        "texto": ("s", "space-grotesk-500.json"),
        "mono": ("m", "jetbrains-mono-400.json"),
        "monob": ("b", "jetbrains-mono-700.json"),
    }
    _cache: dict[str, "Fuente"] = {}

    def __init__(self, clave: str):
        prefijo, archivo = self.ARCHIVOS[clave]
        datos = json.loads((FUENTES / archivo).read_text(encoding="utf-8"))
        self.prefijo = prefijo
        self.unidades = datos["unidades"]
        self.glifos = datos["glifos"]

    @classmethod
    def de(cls, clave: str) -> "Fuente":
        if clave not in cls._cache:
            cls._cache[clave] = cls(clave)
        return cls._cache[clave]

    def glifo(self, caracter: str) -> dict:
        if caracter not in self.glifos:
            FALTANTES.add(caracter)
            return self.glifos["?"]
        return self.glifos[caracter]

    def ancho(self, texto: str, tam: float, espaciado: float = 0) -> float:
        total = sum(self.glifo(c)["w"] for c in texto) * tam / self.unidades
        return total + espaciado * max(0, len(texto) - 1)


class Lienzo:
    """Documento SVG con glifos reutilizables (<use>) y estilos propios."""

    def __init__(self, ancho: int, alto: int, titulo: str, descripcion: str = ""):
        self.ancho, self.alto = ancho, alto
        self.titulo, self.descripcion = titulo, descripcion
        self.glifos: dict[str, str] = {}
        self.defs: list[str] = []
        self.estilos: list[str] = []
        self.cuerpo: list[str] = []

    def add(self, *partes: str) -> None:
        self.cuerpo.extend(partes)

    def texto(self, clave, texto, x, y, tam, color, espaciado=0.0, ancla="start", tipeo=None):
        """Devuelve (svg, ancho). `tipeo=(inicio, paso)` hace aparecer letra por letra."""
        f = Fuente.de(clave)
        ancho = f.ancho(texto, tam, espaciado)
        if ancla == "middle":
            x -= ancho / 2
        elif ancla == "end":
            x -= ancho
        k = tam / f.unidades
        avance_extra = espaciado / k
        cursor = 0.0
        usos = []
        for i, c in enumerate(texto):
            g = f.glifo(c)
            if g["d"]:
                gid = f"{f.prefijo}{ord(c):x}"
                self.glifos[gid] = g["d"]
                atributos = f' x="{num(cursor, 1)}"' if cursor else ""
                if tipeo:
                    atributos += f' class="tk" style="animation-delay:{tipeo[0] + i * tipeo[1]:.2f}s"'
                usos.append(f'<use href="#{gid}"{atributos}/>')
            cursor += g["w"] + avance_extra
        svg = (f'<g transform="translate({num(x)} {num(y)}) scale({num(k, 5)} {num(-k, 5)})" '
               f'fill="{color}">' + "".join(usos) + "</g>")
        return svg, ancho

    def ajustar(self, clave, texto, ancho_max, tam_max, espaciado=0.0):
        """Tamaño de letra más grande que cabe en `ancho_max`."""
        f = Fuente.de(clave)
        tam = tam_max
        while tam > 8 and f.ancho(texto, tam, espaciado) > ancho_max:
            tam -= 0.5
        return tam

    def armar(self) -> str:
        defs = "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in sorted(self.glifos.items()))
        defs += "".join(self.defs)
        estilo = "".join(self.estilos)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.ancho} {self.alto}" '
            f'width="{self.ancho}" height="{self.alto}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(self.titulo)}</title><desc id="d">{esc(self.descripcion)}</desc>'
            + (f"<style>{estilo}</style>" if estilo else "")
            + f"<defs>{defs}</defs>"
            + "".join(self.cuerpo)
            + "</svg>\n"
        )


def cuadros(puntos) -> str:
    """Une muchos cuadritos en un solo trazo (mucho más ligero que un <rect> por punto)."""
    partes = []
    for x, y, s in puntos:
        partes.append(f"M{num(x - s / 2, 1)} {num(y - s / 2, 1)}h{num(s, 1)}v{num(s, 1)}h-{num(s, 1)}z")
    return "".join(partes)


def esquinas(x, y, w, h, largo, color, grosor=2, opacidad=1.0) -> str:
    d = (f"M{x} {y + largo}V{y}H{x + largo}"
         f"M{x + w - largo} {y}H{x + w}V{y + largo}"
         f"M{x + w} {y + h - largo}V{y + h}H{x + w - largo}"
         f"M{x + largo} {y + h}H{x}V{y + h - largo}")
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-opacity="{opacidad}" stroke-linecap="square"/>')


# ─────────────────────────────────────────────────────────────────────────────
#  Cabecera holográfica animada
# ─────────────────────────────────────────────────────────────────────────────

LOOP = 16  # segundos de la secuencia completa del retrato
FASES = {  # figura: (empieza a formarse, formada, empieza a irse, ya se fue) en fracción del ciclo
    "rostro": (0.00, 0.09, 0.35, 0.44),
    "ac": (0.38, 0.47, 0.61, 0.70),
    "escudo": (0.64, 0.73, 0.87, 0.96),
}


def pct(fraccion: float) -> str:
    return num(fraccion * 100, 2) + "%"


def keyframes_figura(nombre, fase, dx, dy, rot, esc_):
    a0, a1, v1, s1 = fase
    lejos = f"translate({num(dx)}px,{num(dy)}px) rotate({num(rot)}deg) scale({num(esc_)})"

    def parcial(t):
        return (f"translate({num(dx * t)}px,{num(dy * t)}px) rotate({num(rot * t)}deg) "
                f"scale({num(1 + (esc_ - 1) * t)})")

    cuadros_ = []
    if a0 > 0:
        cuadros_.append(f"0%,{pct(a0)}{{transform:{lejos};opacity:0}}")
    else:
        # La primera figura aparece como nube al final del ciclo anterior, sin huecos
        cuadros_.append(f"0%{{transform:{lejos};opacity:.35}}")
    cuadros_.append(f"{pct((a0 + a1) / 2)}{{transform:{parcial(0.32)};opacity:.8}}")
    cuadros_.append(f"{pct(a1)},{pct(v1)}{{transform:none;opacity:1}}")
    cuadros_.append(f"{pct((v1 + s1) / 2)}{{transform:{parcial(0.42)};opacity:.65}}")
    if a0 > 0:
        cuadros_.append(f"{pct(s1)},100%{{transform:{lejos};opacity:0}}")
    else:
        cuadros_.append(f"{pct(s1)},{pct(0.93)}{{transform:{lejos};opacity:0}}100%{{transform:{lejos};opacity:.35}}")
    return f"@keyframes {nombre}{{{''.join(cuadros_)}}}"


def hero(perfil: dict, particulas: dict) -> str:
    P = OSCURO
    per = perfil["persona"]
    W, H = 1200, 540
    nombre_completo = f"{per['nombre']} {per['apellido']}"
    lz = Lienzo(
        W, H,
        f"{nombre_completo} — {' · '.join(per['enfoque'])}",
        "Cabecera animada: terminal con whoami y un retrato holográfico hecho de partículas, "
        "tomado de una foto real, que se dispersa y se transforma en el monograma AC y en un escudo "
        "con candado antes de volver al rostro.",
    )
    rnd = random.Random(2050)

    # Marco del retrato
    mx, my, mw, mh = 704, 66, 440, 446
    ox, oy = mx + 20, my + 10  # origen de las coordenadas de partículas (400×420)
    cx, cy = ox + 200, oy + 214

    css = [
        ".pg{animation-duration:%ss;animation-iteration-count:infinite;"
        "animation-timing-function:cubic-bezier(.55,0,.25,1);animation-fill-mode:both;"
        "transform-box:view-box;transform-origin:%spx %spx}" % (LOOP, cx, cy),
        ".ac,.es{opacity:0}",
        ".tk{animation:tk .01s steps(1) both}@keyframes tk{from{opacity:0}to{opacity:1}}",
        ".cur{animation:curm .9s steps(6,end) .55s both,parp 1.2s steps(2,start) 1.6s infinite}",
        "@keyframes parp{to{opacity:.15}}",
        ".en{animation:en .9s cubic-bezier(.2,.7,.2,1) both}",
        "@keyframes en{from{opacity:0;transform:translateY(12px)}}",
        ".scan{animation:scan %ss linear infinite}" % num(LOOP / 3, 3),
        "@keyframes scan{0%%{transform:translateY(0)}80%%,100%%{transform:translateY(%spx)}}" % (mh + 90),
        ".bar{transform-box:fill-box;transform-origin:left;animation:bar %ss linear infinite}" % LOOP,
        "@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}",
        ".fl{animation-timing-function:ease-out;animation-iteration-count:infinite;animation-fill-mode:both}",
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}.scan,.fl,.f2,.f3{display:none}}",
    ]

    # Fondo, rejilla y brillos
    lz.defs.append(
        '<linearGradient id="hf" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{P["fondo"]}"/><stop offset="1" stop-color="#0A1324"/></linearGradient>'
        '<pattern id="rej" width="28" height="28" patternUnits="userSpaceOnUse">'
        f'<path d="M28 0H0V28" fill="none" stroke="{P["rejilla"]}" stroke-width="1"/></pattern>'
        '<radialGradient id="g1"><stop offset="0" stop-color="#22D3EE" stop-opacity=".16"/>'
        '<stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="g2"><stop offset="0" stop-color="#8B5CF6" stop-opacity=".13"/>'
        '<stop offset=".55" stop-color="#8B5CF6" stop-opacity=".04"/>'
        '<stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="hc"><rect x="0" y="0" width="{W}" height="{H}" rx="18"/></clipPath>'
        f'<clipPath id="mc"><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="12"/></clipPath>'
        '<linearGradient id="gs" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#22D3EE" stop-opacity="0"/>'
        '<stop offset=".85" stop-color="#22D3EE" stop-opacity=".07"/>'
        '<stop offset="1" stop-color="#7FF3FF" stop-opacity=".32"/></linearGradient>'
    )
    lz.add(
        f'<g clip-path="url(#hc)"><rect width="{W}" height="{H}" fill="url(#hf)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#rej)" opacity=".55"/>'
        f'<circle cx="{cx}" cy="{cy}" r="330" fill="url(#g1)"/>'
        f'<circle cx="150" cy="{H - 40}" r="300" fill="url(#g2)"/></g>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{P["linea"]}"/>',
        f'<path d="M18 .5H150" stroke="{P["cian"]}" stroke-width="2"/>',
        f'<path d="M{W - 150} {H - .5}H{W - 18}" stroke="{P["violeta"]}" stroke-width="2"/>',
    )

    # Barra de ventana
    lz.add(
        f'<circle cx="30" cy="23" r="5.5" fill="#F87171" fill-opacity=".85"/>'
        f'<circle cx="50" cy="23" r="5.5" fill="#FBBF24" fill-opacity=".85"/>'
        f'<circle cx="70" cy="23" r="5.5" fill="#34D399" fill-opacity=".85"/>',
        lz.texto("mono", f"{per['usuario']} / README.md", 94, 28, 13, P["tenue"])[0],
        f'<path d="M1 46.5H{W - 1}" stroke="{P["linea"]}"/>',
    )

    # Bloque izquierdo: terminal + identidad
    x0 = 58
    s1, w1 = lz.texto("mono", "alfonso@systems", x0, 104, 19, P["verde"])
    s2, w2 = lz.texto("mono", ":~$", x0 + w1, 104, 19, P["suave"])
    comando = " whoami"
    s3, w3 = lz.texto("mono", comando, x0 + w1 + w2, 104, 19, P["texto"], tipeo=(0.55, 0.15))
    ancho_letra = Fuente.de("mono").ancho("a", 19)
    cursor_x = x0 + w1 + w2 + w3 + 3
    css.append("@keyframes curm{from{transform:translateX(-%spx)}to{transform:translateX(0)}}" % num(ancho_letra * 6))
    lz.add(s1, s2, s3, f'<rect class="cur" x="{num(cursor_x)}" y="88" width="11" height="20" fill="{P["verde"]}"/>')

    t_nombre, _ = lz.texto("titulo", per["nombre"], x0 - 3, 192, 80, P["texto"])
    t_apellido, w_ap = lz.texto("titulo", per["apellido"], x0 - 3, 276, 80, "#fff")
    # Degradado continuo en el apellido: el texto funciona como máscara de un rectángulo
    lz.defs.append(
        f'<linearGradient id="gn" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{num(x0 + w_ap)}" y2="0">'
        f'<stop offset="0" stop-color="{P["cian"]}"/><stop offset=".55" stop-color="{P["azul"]}"/>'
        f'<stop offset="1" stop-color="{P["violeta"]}"/></linearGradient>'
        f'<mask id="mn" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{t_apellido}</mask>'
    )
    lz.add(f'<g class="en" style="animation-delay:1.45s">{t_nombre}</g>',
           f'<g class="en" style="animation-delay:1.6s"><rect x="{x0 - 6}" y="200" width="{num(w_ap + 12)}" '
           f'height="96" fill="url(#gn)" mask="url(#mn)"/></g>')

    colores_enfoque = [P["cian"], P["violeta"], P["ambar"]]
    enfoque = per["enfoque"]
    linea1 = []
    x = x0
    for i, area in enumerate(enfoque[:2]):
        s, w = lz.texto("texto", area, x, 330, 27, colores_enfoque[i])
        linea1.append(s)
        x += w
        if i == 0:
            s, w = lz.texto("texto", "  ·  ", x, 330, 27, P["tenue"])
            linea1.append(s)
            x += w
    s_l2, _ = lz.texto("texto", enfoque[2], x0, 366, 27, colores_enfoque[2])
    s_comp, _ = lz.texto("mono", "  ·  ".join(per["complementos"]), x0, 408, 15, P["suave"])
    lz.add(f'<g class="en" style="animation-delay:1.8s">{"".join(linea1)}{s_l2}</g>',
           f'<g class="en" style="animation-delay:1.95s">{s_comp}</g>')

    filas = [("rol", per["titulo"]), ("base", per["ubicacion"]), ("idiomas", per["idiomas"])]
    kv = [f'<path d="M{x0} 436.5H620" stroke="{P["linea"]}"/>']
    for i, (clave, valor) in enumerate(filas):
        yy = 466 + i * 24
        kv.append(lz.texto("mono", clave, x0, yy, 13.5, P["tenue"])[0])
        kv.append(lz.texto("mono", valor, x0 + 92, yy, 13.5, P["suave"])[0])
    lz.add(f'<g class="en" style="animation-delay:2.1s">{"".join(kv)}</g>')

    # Marco del retrato
    lz.add(
        f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="12" fill="{P["panel"]}" '
        f'fill-opacity=".55" stroke="{P["linea"]}"/>',
        esquinas(mx - 6, my - 6, mw + 12, mh + 12, 20, P["cian"], 2, 0.9),
        lz.texto("mono", "VISUAL.MAP // retrato de partículas", mx + 16, my + 24, 11, P["tenue"])[0],
    )
    marcas = "".join(f"M{mx + mw - 10} {my + 40 + i * 12}h{6 if i % 4 == 0 else 3}" for i in range(31))
    lz.add(f'<path d="{marcas}" stroke="{P["linea2"]}" stroke-width="1"/>')

    # Etiquetas de fase (cambian junto con la figura)
    etiquetas = [("01 · ROSTRO", "rostro"), ("02 · IDENTIDAD AC", "ac"), ("03 · SEGURIDAD", "escudo")]
    for i, (texto, figura) in enumerate(etiquetas, start=1):
        a0, a1, v1, s1_ = FASES[figura]
        ini, fin = (a0 + a1) / 2, (v1 + s1_) / 2
        if ini <= 0:
            cuadros_ = f"0%,{pct(fin - .01)}{{opacity:1}}{pct(fin)},100%{{opacity:0}}"
        else:
            cuadros_ = (f"0%,{pct(ini - .01)}{{opacity:0}}{pct(ini)},{pct(fin - .01)}{{opacity:1}}"
                        f"{pct(fin)},100%{{opacity:0}}")
        css.append(f"@keyframes fa{i}{{{cuadros_}}}.f{i}{{animation:fa{i} {LOOP}s linear infinite}}")
        lz.add(f'<g class="f{i}">' + lz.texto("monob", texto, mx + mw - 18, my + 24, 11, P["cian"], 1, "end")[0] + "</g>")

    # Barra de progreso del ciclo
    pista_y = my + mh - 16
    marcas_fase = "".join(f"M{num(mx + 16 + (mw - 32) * FASES[f][0])} {pista_y - 4}v8" for f in FASES)
    lz.add(
        f'<path d="M{mx + 16} {pista_y}H{mx + mw - 16}" stroke="{P["linea"]}" stroke-width="2"/>',
        f'<path d="{marcas_fase}" stroke="{P["linea2"]}"/>',
        f'<rect class="bar" x="{mx + 16}" y="{pista_y - 1}" width="{mw - 32}" height="2" fill="{P["cian"]}" fill-opacity=".8"/>',
    )

    # Partículas: cada figura se divide en grupos que viajan en direcciones distintas
    clases = {"rostro": "ro", "ac": "ac", "escudo": "es"}
    capas = []
    for figura, puntos in (("rostro", particulas["rostro"]), ("ac", particulas["ac"]), ("escudo", particulas["escudo"])):
        n_grupos = max(p[5] for p in puntos) + 1
        colores = PARTICULAS_COLORES[figura]
        for g in range(n_grupos):
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

    # Datos que se desprenden del rostro
    flotantes = []
    for i in range(34):
        fx = ox + rnd.uniform(230, 390)
        fy = oy + rnd.uniform(40, 300)
        s = rnd.choice([2.5, 3, 3.5, 4, 5])
        color = rnd.choice(PARTICULAS_COLORES["rostro"][3:])
        dur = rnd.uniform(4.5, 8)
        dx, dy = rnd.uniform(25, 70), rnd.uniform(-50, 10)
        nombre = f"fl{i}"
        css.append(f"@keyframes {nombre}{{0%{{transform:translate(0,0);opacity:0}}20%{{opacity:.9}}"
                   f"100%{{transform:translate({num(dx)}px,{num(dy)}px);opacity:0}}}}")
        flotantes.append(f'<rect class="fl" x="{num(fx, 1)}" y="{num(fy, 1)}" width="{s}" height="{s}" '
                         f'fill="{color}" style="animation-name:{nombre};animation-duration:{num(dur)}s;'
                         f'animation-delay:-{num(rnd.uniform(0, dur))}s"/>')

    lz.add(
        f'<g clip-path="url(#mc)">',
        f'<ellipse cx="{cx}" cy="{cy - 20}" rx="150" ry="170" fill="url(#g1)"/>',
        "".join(capas),
        "".join(flotantes),
        f'<rect class="scan" x="{mx}" y="{my - 90}" width="{mw}" height="90" fill="url(#gs)"/>',
        "</g>",
    )

    lz.estilos.append("".join(css))
    return lz.armar()


# ─────────────────────────────────────────────────────────────────────────────
#  Señal decorativa (cuadritos que se iluminan y recorren la cuadrícula)
# ─────────────────────────────────────────────────────────────────────────────

def senal(tema: str) -> str:
    P = TEMAS[tema]
    W, H = 1200, 86
    lz = Lienzo(W, H, "Señal decorativa", "Cuadrícula animada de cuadritos que se iluminan. Es decorativa: no representa actividad real.")
    rnd = random.Random(7)
    cols, filas, celda, hueco = 80, 4, 11, 4
    x0, y0 = 2, 6
    base = []
    posiciones = []
    for c in range(cols):
        for f in range(filas):
            x = x0 + c * (celda + hueco)
            y = y0 + f * (celda + hueco)
            posiciones.append((x, y))
            base.append(f"M{x} {y}h{celda}v{celda}h-{celda}z")
    d = "".join(base)
    paleta = [P["cian"], P["azul"], P["violeta"], P["verde"]]
    base_color = P["linea"] if tema == "oscuro" else "#E3E9F2"
    lz.defs.append(
        f'<mask id="mk"><path d="{d}" fill="#fff"/></mask>'
        '<linearGradient id="gw" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{P["cian"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{P["cian"]}" stop-opacity=".95"/>'
        f'<stop offset=".8" stop-color="{P["violeta"]}" stop-opacity=".8"/>'
        f'<stop offset="1" stop-color="{P["violeta"]}" stop-opacity="0"/></linearGradient>'
    )
    lz.add(f'<path d="{d}" fill="{base_color}"/>')
    lz.add(f'<g mask="url(#mk)"><rect class="sw" x="-260" y="0" width="260" height="70" fill="url(#gw)"/></g>')
    destellos = []
    for i in range(46):
        x, y = rnd.choice(posiciones)
        color = rnd.choice(paleta)
        dur = rnd.uniform(2.8, 6.5)
        destellos.append(f'<rect class="tw" x="{x}" y="{y}" width="{celda}" height="{celda}" fill="{color}" '
                         f'style="animation-duration:{num(dur)}s;animation-delay:-{num(rnd.uniform(0, dur))}s"/>')
    lz.add("".join(destellos))
    lz.add(lz.texto("mono", "decorativo · sin datos reales", W - 4, 82, 11, P["tenue"], ancla="end")[0])
    lz.estilos.append(
        ".sw{animation:sw 7s cubic-bezier(.4,0,.2,1) infinite}"
        "@keyframes sw{0%{transform:translateX(0)}70%,100%{transform:translateX(1480px)}}"
        ".tw{opacity:.7;animation-name:tw;animation-iteration-count:infinite;animation-timing-function:ease-in-out}"
        "@keyframes tw{0%,100%{opacity:0}50%{opacity:.95}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar()


# ─────────────────────────────────────────────────────────────────────────────
#  Encabezados de sección
# ─────────────────────────────────────────────────────────────────────────────

def encabezado(titulo: str, nota: str, acento: str, tema: str) -> tuple[str, int]:
    """Encabezado compacto (su ancho depende del título) para que se lea bien también en celular."""
    P = TEMAS[tema]
    color = P[acento]
    tam, espaciado = 22, 2.4
    ancho_titulo = Fuente.de("titulo").ancho(titulo.upper(), tam, espaciado)
    largo = 120
    x1 = 42 + ancho_titulo + 18
    W = int(x1 + largo + 12)
    H = 44
    lz = Lienzo(W, H, titulo, nota)
    lz.add(lz.texto("monob", ">_", 2, 30, 20, color)[0])
    lz.add(lz.texto("titulo", titulo.upper(), 42, 30, tam, P["texto"], espaciado=espaciado)[0])
    lz.defs.append(
        '<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{color}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{color}"/></linearGradient>'
        f'<clipPath id="lc"><rect x="{num(x1)}" y="18" width="{largo}" height="9"/></clipPath>'
    )
    lz.add(
        f'<path d="M{num(x1)} 22.5H{num(x1 + largo)}" stroke="{P["linea"]}" stroke-width="1.5"/>',
        f'<g clip-path="url(#lc)"><rect class="mv" x="{num(x1 - 60)}" y="21.25" width="60" height="2.5" fill="url(#gl)"/></g>',
        f'<rect x="{num(x1 + largo + 2)}" y="19.5" width="6" height="6" fill="{color}"/>',
    )
    lz.estilos.append(
        ".mv{animation:mv 6s cubic-bezier(.5,0,.3,1) infinite}"
        f"@keyframes mv{{0%{{transform:translateX(0)}}60%,100%{{transform:translateX({largo + 60}px)}}}}"
        + SIN_MOVIMIENTO
    )
    return lz.armar(), W


# ─────────────────────────────────────────────────────────────────────────────
#  Íconos vectoriales simples (sin logotipos de terceros)
# ─────────────────────────────────────────────────────────────────────────────

def icono(nombre: str, x: float, y: float, s: float, color: str, grosor: float = 2.2) -> str:
    """Dibuja un ícono de lado `s` con esquina superior izquierda en (x, y)."""
    def p(px, py):
        return f"{num(x + px * s, 1)} {num(y + py * s, 1)}"

    st = f'fill="none" stroke="{color}" stroke-width="{grosor}" stroke-linecap="round" stroke-linejoin="round"'
    if nombre == "escudo":
        return (f'<path d="M{p(.5, .04)}L{p(.9, .2)}V{p(.9, .5)[0:0]}{num(y + .5 * s, 1)}C{p(.9, .76)} {p(.72, .9)} {p(.5, .98)}'
                f'C{p(.28, .9)} {p(.1, .76)} {p(.1, .5)}V{num(y + .2 * s, 1)}Z" {st}/>'
                f'<rect x="{num(x + .36 * s, 1)}" y="{num(y + .46 * s, 1)}" width="{num(.28 * s, 1)}" height="{num(.22 * s, 1)}" rx="2" {st}/>'
                f'<path d="M{p(.41, .46)}V{num(y + .38 * s, 1)}A{num(.09 * s, 1)} {num(.09 * s, 1)} 0 0 1 {p(.59, .38)}V{num(y + .46 * s, 1)}" {st}/>')
    if nombre == "red":
        nodos = [(.5, .16), (.16, .72), (.84, .72), (.5, .52)]
        lineas = f'<path d="M{p(.5, .16)}L{p(.5, .52)}L{p(.16, .72)}M{p(.5, .52)}L{p(.84, .72)}M{p(.16, .72)}L{p(.84, .72)}" {st}/>'
        circulos = "".join(f'<circle cx="{num(x + a * s, 1)}" cy="{num(y + b * s, 1)}" r="{num(.09 * s, 1)}" {st}/>' for a, b in nodos)
        return lineas + circulos
    if nombre == "gestion":
        dientes = "".join(
            f'<path d="M{p(.38 + .16 * math.cos(a), .4 + .16 * math.sin(a))}L{p(.38 + .27 * math.cos(a), .4 + .27 * math.sin(a))}" {st}/>'
            for a in [i * math.pi / 4 for i in range(8)])
        return (f'<circle cx="{num(x + .38 * s, 1)}" cy="{num(y + .4 * s, 1)}" r="{num(.17 * s, 1)}" {st}/>'
                f'<circle cx="{num(x + .38 * s, 1)}" cy="{num(y + .4 * s, 1)}" r="{num(.06 * s, 1)}" {st}/>' + dientes
                + f'<path d="M{p(.66, .95)}V{num(y + .78 * s, 1)}M{p(.8, .95)}V{num(y + .66 * s, 1)}M{p(.94, .95)}V{num(y + .54 * s, 1)}" {st}/>')
    if nombre == "linkedin":
        return (f'<rect x="{num(x, 1)}" y="{num(y, 1)}" width="{num(s, 1)}" height="{num(s, 1)}" rx="{num(s * .2, 1)}" {st}/>'
                f'<path d="M{p(.3, .45)}V{num(y + .74 * s, 1)}M{p(.47, .74)}V{num(y + .45 * s, 1)}M{p(.47, .56)}C{p(.5, .44)} {p(.72, .4)} {p(.72, .58)}V{num(y + .74 * s, 1)}" {st}/>'
                f'<circle cx="{num(x + .3 * s, 1)}" cy="{num(y + .29 * s, 1)}" r="1.4" fill="{color}"/>')
    if nombre == "correo":
        return (f'<rect x="{num(x, 1)}" y="{num(y + .16 * s, 1)}" width="{num(s, 1)}" height="{num(.68 * s, 1)}" rx="3" {st}/>'
                f'<path d="M{p(.04, .22)}L{p(.5, .56)}L{p(.96, .22)}" {st}/>')
    if nombre == "web":
        return (f'<circle cx="{num(x + s / 2, 1)}" cy="{num(y + s / 2, 1)}" r="{num(s * .46, 1)}" {st}/>'
                f'<ellipse cx="{num(x + s / 2, 1)}" cy="{num(y + s / 2, 1)}" rx="{num(s * .2, 1)}" ry="{num(s * .46, 1)}" {st}/>'
                f'<path d="M{p(.05, .5)}H{num(x + .95 * s, 1)}M{p(.12, .28)}H{num(x + .88 * s, 1)}M{p(.12, .72)}H{num(x + .88 * s, 1)}" {st}/>')
    if nombre == "repos":
        return (f'<path d="M{p(.04, .2)}H{num(x + .38 * s, 1)}L{p(.48, .3)}H{num(x + .96 * s, 1)}V{num(y + .86 * s, 1)}H{num(x + .04 * s, 1)}Z" {st}/>'
                f'<path d="M{p(.36, .5)}L{p(.26, .6)}L{p(.36, .7)}M{p(.64, .5)}L{p(.74, .6)}L{p(.64, .7)}" {st}/>')
    return ""


# ─────────────────────────────────────────────────────────────────────────────
#  Tarjetas de áreas
# ─────────────────────────────────────────────────────────────────────────────

def areas(perfil: dict) -> str:
    P = OSCURO
    lista = perfil["areas"]
    W, H = 1200, 252
    lz = Lienzo(W, H, "Áreas: " + ", ".join(a["titulo"] for a in lista),
                " · ".join(a["titulo"] + ": " + " ".join(a["lema"]) for a in lista))
    ancho = (W - 24 * (len(lista) - 1)) / len(lista)
    css = [".pu{transform-box:fill-box;transform-origin:center;animation:pu 4.5s ease-in-out infinite}"
           "@keyframes pu{0%,100%{transform:scale(.86);opacity:.5}50%{transform:scale(1.08);opacity:1}}",
           ".br{animation:br 9s cubic-bezier(.5,0,.3,1) infinite}"
           f"@keyframes br{{0%{{transform:translateX(0)}}55%,100%{{transform:translateX({W + 400}px)}}}}",
           SIN_MOVIMIENTO]
    lz.defs.append(
        f'<clipPath id="ac"><rect x="0" y="0" width="{W}" height="{H}" rx="16"/></clipPath>'
        '<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    )
    for i, area in enumerate(lista):
        x = i * (ancho + 24)
        color = P[area["acento"]]
        lz.defs.append(f'<radialGradient id="ga{i}"><stop offset="0" stop-color="{color}" stop-opacity=".28"/>'
                       f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        lz.add(
            f'<rect x="{num(x + .5)}" y=".5" width="{num(ancho - 1)}" height="{H - 1}" rx="16" fill="{P["panel"]}" stroke="{P["linea"]}"/>',
            f'<path d="M{num(x + 24)} 1.5H{num(x + 110)}" stroke="{color}" stroke-width="3"/>',
            f'<circle class="pu" cx="{num(x + 62)}" cy="70" r="40" fill="url(#ga{i})" style="animation-delay:-{i * 1.5}s"/>',
            icono(area["icono"], x + 34, 42, 56, color, 2.4),
            lz.texto("mono", f"0{i + 1}", x + ancho - 26, 46, 13, P["tenue"], ancla="end")[0],
        )
        tam = lz.ajustar("titulo", area["titulo"], ancho - 52, 27)
        lz.add(lz.texto("titulo", area["titulo"], x + 26, 160, tam, P["texto"])[0])
        for j, linea in enumerate(area["lema"]):
            lz.add(lz.texto("texto", linea, x + 26, 194 + j * 24, 16, P["suave"])[0])
    lz.add(f'<g clip-path="url(#ac)"><rect class="br" x="-400" y="0" width="400" height="{H}" fill="url(#gb)"/></g>')
    lz.estilos.append("".join(css))
    return lz.armar()


# ─────────────────────────────────────────────────────────────────────────────
#  Portadas de proyectos
# ─────────────────────────────────────────────────────────────────────────────

def motivo(tipo: str, P: dict, color: str, rnd: random.Random) -> str:
    """Ilustración vectorial de la portada, en la zona derecha (x 350–616, y 56–272)."""
    def trazo(grosor=2.5, relleno="none", opacidad=None):
        extra = f' fill-opacity="{opacidad}"' if opacidad is not None else ""
        return (f'fill="{relleno}"{extra} stroke="{color}" stroke-width="{grosor}" '
                'stroke-linecap="round" stroke-linejoin="round"')

    st = trazo()
    tenue = P["linea2"]
    partes = []
    if tipo == "escudo":
        for i in range(7):
            y = 84 + i * 24
            largo = rnd.randint(70, 150)
            marca = [P["rojo"], P["ambar"], P["verde"], tenue][i % 4]
            partes.append(f'<circle cx="364" cy="{y}" r="4" fill="{marca}"/>')
            partes.append(f'<rect x="376" y="{y - 4}" width="{largo}" height="8" rx="4" fill="{tenue}" fill-opacity=".8"/>')
        partes.append('<rect x="352" y="128" width="190" height="28" rx="6" fill="#22D3EE" fill-opacity=".08" stroke="#22D3EE" stroke-opacity=".35"/>')
        cx, top = 548, 70
        partes.append(f'<path d="M{cx} {top}L{cx + 62} {top + 26}V{top + 92}C{cx + 62} {top + 138} {cx + 30} {top + 166} {cx} {top + 182}'
                      f'C{cx - 30} {top + 166} {cx - 62} {top + 138} {cx - 62} {top + 92}V{top + 26}Z" {trazo(2.5, color, ".08")}/>')
        partes.append(f'<circle cx="{cx - 4}" cy="{top + 86}" r="24" {st}/><path d="M{cx + 13} {top + 103}L{cx + 32} {top + 122}" {trazo(4)}/>')
    elif tipo == "logs":
        partes.append(f'<rect x="352" y="60" width="264" height="200" rx="10" fill="{P["fondo"]}" stroke="{tenue}"/>')
        partes.append(f'<circle cx="368" cy="76" r="3.5" fill="{P["rojo"]}"/><circle cx="380" cy="76" r="3.5" fill="{P["ambar"]}"/><circle cx="392" cy="76" r="3.5" fill="{P["verde"]}"/>')
        for i in range(8):
            y = 98 + i * 18
            a = rnd.randint(30, 50)
            b = rnd.randint(40, 120)
            sospechoso = i in (3, 4, 5)
            partes.append(f'<rect x="366" y="{y}" width="{a}" height="7" rx="3" fill="{tenue}"/>')
            partes.append(f'<rect x="{372 + a}" y="{y}" width="{b}" height="7" rx="3" fill="{P["rojo"] if sospechoso else tenue}" fill-opacity="{.9 if sospechoso else .55}"/>')
        partes.append(f'<path d="M360 148h-4v52h4M604 148h4v52h-4" {st}/>')
        alturas = [10, 14, 9, 16, 34, 40, 12, 8]
        for i, h in enumerate(alturas):
            partes.append(f'<rect x="{530 + i * 9}" y="{248 - h}" width="6" height="{h}" fill="{P["rojo"] if h > 30 else color}" fill-opacity=".85"/>')
    elif tipo == "ia":
        cx, cy = 500, 160
        for r, dash in ((92, "3 7"), (66, "10 6"), (40, "")):
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-opacity="{.4 if dash else .9}" stroke-width="2"{extra}/>')
        partes.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{color}" fill-opacity=".85"/>')
        for ang in (20, 140, 250, 320):
            a = math.radians(ang)
            r = 66 if ang % 2 else 92
            partes.append(f'<rect x="{num(cx + math.cos(a) * r - 4)}" y="{num(cy + math.sin(a) * r - 4)}" width="8" height="8" fill="{P["cian"]}"/>')
        for i in range(9):
            h = [10, 22, 36, 18, 44, 26, 14, 30, 12][i]
            partes.append(f'<rect x="{560 + i * 7}" y="{160 - h / 2}" width="4" height="{h}" rx="2" fill="{P["cian"]}" fill-opacity=".8"/>')
    elif tipo == "voz":
        partes.append(f'<rect x="376" y="84" width="44" height="88" rx="22" {trazo(2.5, color, ".1")}/>')
        partes.append(f'<path d="M362 140c0 36 72 36 72 0M398 176v26M380 204h36" {st}/>')
        for i in range(16):
            h = 8 + abs(math.sin(i * 0.9)) * 52
            partes.append(f'<rect x="{454 + i * 9}" y="{num(146 - h / 2)}" width="5" height="{num(h)}" rx="2.5" fill="{color}" fill-opacity="{.45 + .5 * (i % 3 == 0)}"/>')
        partes.append(f'<rect x="470" y="196" width="122" height="44" rx="12" fill="{P["fondo"]}" stroke="{tenue}"/>')
        partes.append(f'<path d="M490 240l-6 12 18-12" fill="{P["fondo"]}" stroke="{tenue}"/>')
    elif tipo == "tienda":
        partes.append(f'<rect x="372" y="66" width="168" height="196" rx="12" fill="{P["fondo"]}" stroke="{tenue}"/>')
        partes.append(f'<path d="M420 104l22-14h28l22 14 18 22-18 12-8-8v72h-68v-72l-8 8-18-12z" {trazo(2.5, color, ".12")}/>')
        partes.append(f'<rect x="390" y="226" width="80" height="8" rx="4" fill="{tenue}"/><rect x="390" y="242" width="44" height="8" rx="4" fill="{color}"/>')
        partes.append(f'<circle cx="572" cy="110" r="30" {trazo(2.5, color, ".1")}/>')
        partes.append(f'<path d="M556 100h6l6 18h16l5-12h-24M570 124a2 2 0 1 0 0.1 0M582 124a2 2 0 1 0 0.1 0" {trazo(2)}/>')
    elif tipo == "lealtad":
        partes.append(f'<rect x="356" y="86" width="196" height="122" rx="14" fill="{P["fondo"]}" stroke="{color}" stroke-width="2"/>')
        partes.append(f'<rect x="374" y="104" width="70" height="8" rx="4" fill="{tenue}"/>')
        for i in range(8):
            fx = 384 + (i % 4) * 34
            fy = 142 + (i // 4) * 34
            lleno = i < 5
            partes.append(f'<circle cx="{fx}" cy="{fy}" r="12" fill="{color if lleno else "none"}" fill-opacity="{.85 if lleno else 0}" stroke="{color}" stroke-width="2"/>')
        qx, qy, qs = 528, 150, 84
        partes.append(f'<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="8" fill="#E6EDF7"/>')
        modulo = qs / 12
        bloques = []
        for fy in range(1, 11):
            for fx in range(1, 11):
                en_esquina = (fx < 4 and fy < 4) or (fx > 7 and fy < 4) or (fx < 4 and fy > 7)
                if en_esquina:
                    borde = fx in (1, 3, 8, 10) or fy in (1, 3, 8, 10)
                    centro = (fx, fy) in ((2, 2), (9, 2), (2, 9))
                    if borde or centro:
                        bloques.append((fx, fy))
                elif rnd.random() < 0.45:
                    bloques.append((fx, fy))
        d = "".join(f"M{num(qx + fx * modulo)} {num(qy + fy * modulo)}h{num(modulo)}v{num(modulo)}h-{num(modulo)}z" for fx, fy in bloques)
        partes.append(f'<path d="{d}" fill="#0B1220"/>')
    elif tipo == "menu":
        partes.append(f'<rect x="380" y="64" width="190" height="200" rx="12" fill="{P["fondo"]}" stroke="{tenue}"/>')
        for i in range(5):
            y = 100 + i * 32
            partes.append(f'<rect x="400" y="{y}" width="{rnd.randint(70, 110)}" height="8" rx="4" fill="{tenue}"/>')
            partes.append(f'<rect x="526" y="{y}" width="26" height="8" rx="4" fill="{color}"/>')
    else:  # web / terminal
        partes.append(f'<rect x="356" y="66" width="256" height="190" rx="12" fill="{P["fondo"]}" stroke="{tenue}"/>')
        partes.append(f'<path d="M356 94H612" stroke="{tenue}"/><rect x="376" y="114" width="100" height="12" rx="6" fill="{color}"/>')
        for i in range(4):
            partes.append(f'<rect x="376" y="{142 + i * 18}" width="{rnd.randint(90, 200)}" height="8" rx="4" fill="{tenue}"/>')
        partes.append(f'<rect x="500" y="114" width="92" height="66" rx="8" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".5"/>')
    return "".join(partes)


def portada(proyecto: dict, indice: int) -> str:
    P = OSCURO
    W, H = 640, 300
    color = P[proyecto.get("acento", "cian")]
    lz = Lienzo(W, H, f"Portada de {proyecto['nombre']}", f"{proyecto['categoria']} · {proyecto['estado']}")
    rnd = random.Random(proyecto["id"])
    lz.defs.append(
        f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
        '<pattern id="pr" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M24 0H0V24" fill="none" stroke="{P["rejilla"]}"/></pattern>'
        f'<radialGradient id="pg"><stop offset="0" stop-color="{color}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
    )
    lz.add(
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="{P["panel"]}"/>'
        f'<rect width="{W}" height="{H}" fill="url(#pr)" opacity=".7"/>'
        f'<circle cx="490" cy="160" r="230" fill="url(#pg)"/></g>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{P["linea"]}"/>',
        f'<path d="M20 .5H120" stroke="{color}" stroke-width="3"/>',
    )
    lz.add(lz.texto("mono", f"proyecto/{indice:02d}", 28, 40, 12.5, P["tenue"])[0])
    lz.add(lz.texto("titulo", f"{indice:02d}", 24, 150, 96, P["linea2"])[0])
    etiqueta = proyecto.get("etiqueta", proyecto["estado"])
    ancho_et = Fuente.de("monob").ancho(etiqueta, 12, 0.5)
    lz.add(f'<rect x="{num(W - 28 - ancho_et - 24)}" y="22" width="{num(ancho_et + 24)}" height="26" rx="13" '
           f'fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".7"/>')
    lz.add(lz.texto("monob", etiqueta, W - 40, 39.5, 12, color, 0.5, "end")[0])
    lz.add(motivo(proyecto.get("portada", "web"), P, color, rnd))

    lz.add(lz.texto("mono", proyecto["categoria"].upper(), 28, 186, 12.5, color, 1)[0])
    nombre = proyecto["nombre"]
    ancho_max = 318
    tam = lz.ajustar("titulo", nombre, ancho_max, 34)
    if tam < 27 and " — " in nombre:
        l1, l2 = nombre.split(" — ", 1)
        tam = min(lz.ajustar("titulo", l1, ancho_max, 32), lz.ajustar("titulo", l2, ancho_max, 32))
        lz.add(lz.texto("titulo", l1, 26, 222, tam, P["texto"])[0])
        lz.add(lz.texto("titulo", l2, 26, 222 + tam * 1.1, tam, P["suave"])[0])
    else:
        lz.add(lz.texto("titulo", nombre, 26, 232, tam, P["texto"])[0])
    tecnologias = "  ·  ".join(proyecto.get("tecnologias", []))
    if tecnologias:
        tam_t = lz.ajustar("mono", tecnologias, 330, 12.5)
        lz.add(lz.texto("mono", tecnologias, 28, 278, tam_t, P["suave"])[0])
    return lz.armar()


# ─────────────────────────────────────────────────────────────────────────────
#  Botones de contacto
# ─────────────────────────────────────────────────────────────────────────────

def boton(texto: str, icono_nombre: str, acento: str, tema: str) -> str:
    P = TEMAS[tema]
    W, H = 264, 54
    color = P[acento]
    lz = Lienzo(W, H, texto)
    fondo = P["panel"]
    lz.add(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{fondo}" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>',
        icono(icono_nombre, 20, 15, 24, color, 2),
        lz.texto("texto", texto, 60, 34, 18, P["texto"])[0],
        f'<path d="M{W - 34} 34L{W - 24} 24M{W - 32} 24H{W - 24}V32" fill="none" stroke="{P["tenue"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    )
    return lz.armar()


# ─────────────────────────────────────────────────────────────────────────────
#  README
# ─────────────────────────────────────────────────────────────────────────────

SECCIONES = {
    "proyectos": ("Proyectos destacados", "enlaces reales · estado actual", "cian"),
    "areas": ("Áreas", "ciberseguridad · sistemas · gestión", "violeta"),
    "experiencia": ("Experiencia", "lo más relevante", "verde"),
    "conocimientos": ("Conocimientos", "experiencia vs. aprendizaje", "azul"),
    "formacion": ("Formación y constancias", "nombres y emisores exactos", "ambar"),
    "laboratorios": ("Laboratorios en desarrollo", "lo que sigue", "verde"),
    "contacto": ("Contacto", "", "cian"),
}

BOTONES = [
    ("linkedin", "LinkedIn", "linkedin", "azul"),
    ("correo", "Correo", "correo", "cian"),
    ("portafolio", "Portafolio", "web", "violeta"),
    ("repositorios", "Repositorios", "repos", "verde"),
]


def imagen_tema(base: str, alt: str, ancho: str = "100%") -> str:
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}-oscuro.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="{base}-claro.svg">'
            f'<img src="{base}-oscuro.svg" width="{ancho}" alt="{esc(alt)}"></picture>')


ANCHOS_ENCABEZADO: dict[str, int] = {}


def titulo_seccion(clave: str) -> str:
    titulo, _, _ = SECCIONES[clave]
    ancho = str(ANCHOS_ENCABEZADO.get(clave, 400))
    return f'<h3>{imagen_tema(f"assets/secciones/{clave}", titulo, ancho)}</h3>'


def visibles(lista):
    return sorted((x for x in lista if x.get("publicar", True)), key=lambda x: x.get("orden", 0))


def chips(lista) -> str:
    return " ".join(f"<code>{esc(t)}</code>" for t in lista)


def enlaces_proyecto(p: dict) -> str:
    partes = []
    if p["visibilidad"] == "publico" and p.get("repo"):
        partes.append(f'<a href="{esc(p["repo"])}"><b>Repositorio</b></a>')
    if p.get("demo"):
        etiqueta = "Ver demo" if p["visibilidad"] == "publico" else "Visitar sitio"
        partes.append(f'<a href="{esc(p["demo"])}"><b>{etiqueta}</b></a>')
    if p["visibilidad"] == "privado":
        partes.append("<sub>código privado</sub>")
    return " · ".join(partes)


def celda_proyecto(p: dict) -> str:
    destino = p["repo"] if p["visibilidad"] == "publico" and p.get("repo") else p.get("demo") or p.get("repo")
    lineas = [
        '<td width="50%" valign="top">',
        f'<a href="{esc(destino)}"><img src="assets/proyectos/{p["id"]}.svg" width="100%" alt="Portada de {esc(p["nombre"])}"></a>',
        f'<p><b>{esc(p["nombre"])}</b><br><sub>{esc(p["categoria"].upper())} · {esc(p["estado"])}</sub></p>',
        f'<p>{esc(p["descripcion"])}</p>',
    ]
    if p.get("funcionamiento"):
        lineas.append("<details><summary><b>Cómo funciona</b></summary>")
        lineas.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in p["funcionamiento"]) + "</ul>")
        if p.get("nota"):
            lineas.append(f'<p><sub>{esc(p["nota"])}</sub></p>')
        lineas.append("</details>")
    lineas.append(f"<p>{enlaces_proyecto(p)}</p>")
    if p.get("tecnologias"):
        lineas.append(f"<p>{chips(p['tecnologias'])}</p>")
    lineas.append("</td>")
    return "\n".join(lineas)


def bloque_manual(readme_actual: str) -> str:
    if MANUAL_INI in readme_actual and MANUAL_FIN in readme_actual:
        inicio = readme_actual.index(MANUAL_INI)
        fin = readme_actual.index(MANUAL_FIN) + len(MANUAL_FIN)
        return readme_actual[inicio:fin]
    return (f"{MANUAL_INI}\n<!-- Lo que escribas entre estas dos marcas se conserva cada vez que "
            f"se regenera el README. -->\n{MANUAL_FIN}")


def construir_readme(perfil: dict, readme_actual: str) -> str:
    per = perfil["persona"]
    con = perfil["contacto"]
    usuario = per["usuario"]
    repos_url = f"https://github.com/{usuario}?tab=repositories"
    enlaces_contacto = {
        "linkedin": con["linkedin"],
        "correo": f"mailto:{con['correo']}",
        "portafolio": con["portafolio"],
        "repositorios": repos_url,
    }
    proyectos = visibles(perfil["proyectos"])
    destacados = [p for p in proyectos if p.get("destacado")]
    otros = [p for p in proyectos if not p.get("destacado")]
    alt_hero = (f"{per['nombre']} {per['apellido']} — {', '.join(per['enfoque'])}. "
                "Retrato holográfico animado de partículas que se transforma en el monograma AC y en un escudo.")

    L: list[str] = []
    a = L.append
    a("<!--\n  ESTE ARCHIVO SE GENERA AUTOMÁTICAMENTE con scripts/generar.py a partir de perfil.toml.\n"
      "  Para cambiar el contenido, edita perfil.toml (guía: docs/MANTENIMIENTO.md).\n-->\n")
    a(f'<p align="center"><img src="assets/hero.svg" width="100%" alt="{esc(alt_hero)}"></p>\n')
    a('<p align="center">')
    a(f"  <b>{esc(per['titulo'])}</b> · {esc(per['posgrado'])}<br>")
    a(f"  {esc(per['ubicacion'])} · {esc(per['idiomas'])}")
    a("</p>")
    a('<p align="center">')
    a("  " + " · ".join([
        f'<a href="{esc(con["linkedin"])}">LinkedIn</a>',
        f'<a href="mailto:{esc(con["correo"])}">{esc(con["correo"])}</a>',
        f'<a href="{esc(con["portafolio"])}">Portafolio</a>',
        f'<a href="{repos_url}">Repositorios</a>',
    ]))
    a("</p>\n")
    a(per["presentacion"].strip() + "\n")
    a(f"**Construyendo ahora:** {per['construyendo']}\n")
    a("<details><summary><b>English summary</b></summary>\n")
    a(per["resumen_ingles"].strip() + "\n")
    a("</details>\n")
    a(f'<p align="center">{imagen_tema("assets/senal", "Cuadrícula decorativa animada (no representa actividad real)")}</p>\n')

    # Proyectos
    a(titulo_seccion("proyectos") + "\n")
    a("<table>")
    for i in range(0, len(destacados), 2):
        a("<tr>")
        for p in destacados[i:i + 2]:
            a(celda_proyecto(p))
        if len(destacados[i:i + 2]) == 1:
            a('<td width="50%"></td>')
        a("</tr>")
    a("</table>\n")
    if otros:
        a(f"<details><summary><b>Más proyectos, prácticas y ejercicios</b> ({len(otros)})</summary>\n")
        a("<table>")
        a("<tr><th align=\"left\">Proyecto</th><th align=\"left\">Qué es</th><th align=\"left\">Enlaces</th></tr>")
        for p in otros:
            a(f"<tr><td><b>{esc(p['nombre'])}</b><br><sub>{esc(p['categoria'])}</sub></td>"
              f"<td>{esc(p['descripcion'])}</td><td>{enlaces_proyecto(p)}</td></tr>")
        a("</table>\n")
        a("</details>\n")
    a(f'<p>→ <a href="{repos_url}"><b>Ver todos mis repositorios públicos</b></a></p>\n')

    # Áreas
    a(titulo_seccion("areas") + "\n")
    nombres_areas = ", ".join(x["titulo"] for x in perfil["areas"])
    a(f'<p align="center"><img src="assets/areas.svg" width="100%" alt="Áreas: {esc(nombres_areas)}"></p>\n')
    for area in perfil["areas"]:
        a(f"**{area['titulo']}**\n")
        for punto in area["puntos"]:
            a(f"- {punto}")
        a("")

    # Experiencia
    a(titulo_seccion("experiencia") + "\n")
    for e in visibles(perfil["experiencia"]):
        a(f"**{e['puesto']}** · {e['empresa']}  ")
        a(f"<sub>{esc(e['periodo'])} · {esc(e['lugar'])}</sub>\n")
        for punto in e["puntos"]:
            a(f"- {punto}")
        a("")

    # Conocimientos
    c = perfil["conocimientos"]
    a(titulo_seccion("conocimientos") + "\n")
    a("| Dónde | Conocimientos |")
    a("|:--|:--|")
    a(f"| **En el trabajo** | {chips(c['trabajo'])} |")
    a(f"| **En mis proyectos** | {chips(c['proyectos'])} |")
    a(f"| **Aprendiendo** | {chips(c['aprendiendo'])} |")
    a(f"| **Herramientas** | {chips(c['herramientas'])} |")
    a("")

    # Formación y constancias
    a(titulo_seccion("formacion") + "\n")
    a("**Formación académica**\n")
    for f in perfil["formacion"]:
        a(f"- **{f['programa']}** — {f['institucion']} · {f['periodo']} · {f['modalidad']}")
    a("")
    cursos = [x for x in perfil["cursos"] if x.get("publicar", True)]
    grupos: dict[str, list] = {}
    for curso in cursos:
        if not curso.get("otros"):
            grupos.setdefault(curso["grupo"], []).append(curso)

    def linea_curso(x):
        texto = f"- **{x['nombre']}** — {x['emisor']} · {x['fecha']} · {x['tipo']}"
        if x.get("verificacion"):
            texto += f" · [verificar]({x['verificacion']})"
        return texto

    for grupo, lista in grupos.items():
        a(f"**{grupo}**\n")
        for x in lista:
            a(linea_curso(x))
        a("")
    adicionales = [x for x in cursos if x.get("otros")]
    if adicionales:
        a(f"<details><summary><b>Otras constancias</b> ({len(adicionales)})</summary>\n")
        for x in adicionales:
            a(linea_curso(x))
        a("\n</details>\n")
    a("<sub>Las constancias de Coursera son cursos en línea sin créditos académicos; cada enlace de verificación "
      "viene de su certificado. Los cursos de Cisco Networking Academy son certificados de finalización de curso, "
      "no la certificación CCNA.</sub>\n")

    # Laboratorios
    if perfil.get("laboratorios"):
        a(titulo_seccion("laboratorios") + "\n")
        for lab in perfil["laboratorios"]:
            nombre = f"[{lab['nombre']}]({lab['enlace']})" if lab.get("enlace") else lab["nombre"]
            a(f"- **{nombre}** <sub>`{lab['estado']}`</sub> — {lab['detalle']}")
        a("")
        a("<sub>Mi actividad real es la gráfica de contribuciones que GitHub muestra debajo de este README; "
          "las cuadrículas animadas de esta página son decorativas.</sub>\n")

    # Contacto
    a(titulo_seccion("contacto") + "\n")
    a('<p align="center">')
    for clave, texto, _, _ in BOTONES:
        a(f'  <a href="{esc(enlaces_contacto[clave])}">{imagen_tema(f"assets/botones/{clave}", texto, "196")}</a>')
    a("</p>\n")
    a(bloque_manual(readme_actual) + "\n")
    a(f'<p align="center"><i>“{esc(per["frase"])}”</i></p>')
    return "\n".join(L) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
#  Orquestación
# ─────────────────────────────────────────────────────────────────────────────

def archivos_generados(perfil: dict, readme_actual: str) -> dict[Path, str]:
    particulas = json.loads(PARTICULAS.read_text(encoding="utf-8"))
    salida: dict[Path, str] = {}
    salida[ASSETS / "hero.svg"] = hero(perfil, particulas)
    salida[ASSETS / "areas.svg"] = areas(perfil)
    for tema in TEMAS:
        salida[ASSETS / f"senal-{tema}.svg"] = senal(tema)
        for clave, (titulo, nota, acento) in SECCIONES.items():
            svg, ancho = encabezado(titulo, nota, acento, tema)
            ANCHOS_ENCABEZADO[clave] = ancho
            salida[ASSETS / "secciones" / f"{clave}-{tema}.svg"] = svg
        for clave, texto, icono_nombre, acento in BOTONES:
            salida[ASSETS / "botones" / f"{clave}-{tema}.svg"] = boton(texto, icono_nombre, acento, tema)
    destacados = [p for p in visibles(perfil["proyectos"]) if p.get("destacado")]
    for i, p in enumerate(destacados, start=1):
        salida[ASSETS / "proyectos" / f"{p['id']}.svg"] = portada(p, i)
    for ruta, contenido in salida.items():
        try:
            ElementTree.fromstring(contenido)
        except ElementTree.ParseError as error:
            raise SystemExit(f"SVG inválido en {ruta.name}: {error}")
    salida[README] = construir_readme(perfil, readme_actual)
    return salida


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera el README del perfil y sus imágenes.")
    parser.add_argument("--verificar", action="store_true", help="no escribe; falla si algo no está al día")
    args = parser.parse_args()

    if sys.version_info < (3, 11):
        print("Necesitas Python 3.11 o superior.", file=sys.stderr)
        return 2
    perfil = tomllib.loads(DATOS.read_text(encoding="utf-8"))
    readme_actual = README.read_text(encoding="utf-8") if README.exists() else ""
    salida = archivos_generados(perfil, readme_actual)

    desactualizados = []
    for ruta, contenido in salida.items():
        actual = ruta.read_text(encoding="utf-8") if ruta.exists() else None
        if actual != contenido:
            desactualizados.append(ruta)
            if not args.verificar:
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_text(contenido, encoding="utf-8", newline="\n")

    # Portadas que ya no corresponden a ningún proyecto destacado
    esperadas = {r for r in salida if r.parent == ASSETS / "proyectos"}
    sobrantes = [r for r in (ASSETS / "proyectos").glob("*.svg") if r not in esperadas] if (ASSETS / "proyectos").exists() else []

    if FALTANTES:
        print("Aviso: estos caracteres no existen en la tipografía y salen como «?» en las imágenes: "
              + " ".join(sorted(FALTANTES)), file=sys.stderr)

    relativas = [str(r.relative_to(RAIZ)) for r in desactualizados]
    if args.verificar:
        if relativas or sobrantes:
            print("Hay archivos desactualizados. Corre: python scripts/generar.py")
            for r in relativas:
                print("  -", r)
            for r in sobrantes:
                print("  - sobra:", r.relative_to(RAIZ))
            return 1
        print("Todo al día.")
        return 0
    for r in sobrantes:
        r.unlink()
    print(f"Listo: {len(relativas)} archivo(s) actualizados, {len(sobrantes)} portada(s) sobrantes eliminadas.")
    for r in relativas:
        print("  -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
