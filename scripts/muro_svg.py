"""Base para dibujar el muro: paleta, texto como trazos, lienzo SVG e íconos propios.

Solo usa la biblioteca estándar de Python. Lo importan muro_graficos.py y generar.py.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

FUENTES = Path(__file__).resolve().parent / "fuentes"

# ─────────────────────────────────────────────────────────────────────────────
#  Paleta «Aurora 2050»: azul profundo con cian, azul, violeta y magenta;
#  ámbar para formación y gestión.
# ─────────────────────────────────────────────────────────────────────────────

OSCURO = {
    "fondo": "#050816", "panel": "#0A1026", "panel2": "#0E1636",
    "linea": "#1D2A55", "linea2": "#2E3F78", "rejilla": "#0E1838",
    "texto": "#EEF3FF", "suave": "#A9B6D8", "tenue": "#6B7BA8",
    "cian": "#22D3EE", "azul": "#3B82F6", "violeta": "#8B5CF6",
    "magenta": "#E14FD0", "verde": "#34D399", "ambar": "#F5B544",
    "rojo": "#F87171",
}
CLARO = {
    "fondo": "#FFFFFF", "panel": "#F6F8FB", "panel2": "#EEF2F7",
    "linea": "#D5DDE8", "linea2": "#B8C4D6", "rejilla": "#E9EEF5",
    "texto": "#0B1220", "suave": "#3E4C63", "tenue": "#66758E",
    "cian": "#0E7490", "azul": "#1D4ED8", "violeta": "#6D28D9",
    "magenta": "#A21CAF", "verde": "#047857", "ambar": "#B45309",
    "rojo": "#B91C1C",
}
TEMAS = {"oscuro": OSCURO, "claro": CLARO}

# Segundo color de cada acento, para degradados (acento → acento2)
PAREJA = {
    "cian": "azul", "azul": "violeta", "violeta": "magenta",
    "magenta": "ambar", "verde": "cian", "ambar": "magenta",
}

SIN_MOVIMIENTO = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def num(valor: float, decimales: int = 2) -> str:
    texto = f"{valor:.{decimales}f}".rstrip("0").rstrip(".")
    return "0" if texto in ("-0", "") else texto


def esc(texto: str) -> str:
    return html.escape(str(texto), quote=True)


def mezclar(c1: str, c2: str, t: float) -> str:
    """Color intermedio entre dos colores hex (t=0 → c1, t=1 → c2)."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


# ─────────────────────────────────────────────────────────────────────────────
#  Texto dibujado como trazos SVG (así no depende de fuentes instaladas)
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

    def texto(self, clave, texto, x, y, tam, color, espaciado=0.0, ancla="start", tipeo=None, extra=""):
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
               f'fill="{color}"{extra}>' + "".join(usos) + "</g>")
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


# ─────────────────────────────────────────────────────────────────────────────
#  Utilidades de dibujo
# ─────────────────────────────────────────────────────────────────────────────

def cuadros(puntos) -> str:
    """Une muchos cuadritos (x, y, lado) en un solo trazo."""
    partes = []
    for x, y, s in puntos:
        partes.append(f"M{num(x - s / 2, 1)} {num(y - s / 2, 1)}h{num(s, 1)}v{num(s, 1)}h-{num(s, 1)}z")
    return "".join(partes)


def rectangulos(rects) -> str:
    """Une rectángulos (x, y, ancho, alto) en un solo trazo."""
    return "".join(f"M{num(x, 1)} {num(y, 1)}h{num(w, 1)}v{num(h, 1)}h-{num(w, 1)}z" for x, y, w, h in rects)


def esquinas(x, y, w, h, largo, color, grosor=2, opacidad=1.0) -> str:
    d = (f"M{x} {y + largo}V{y}H{x + largo}"
         f"M{x + w - largo} {y}H{x + w}V{y + largo}"
         f"M{x + w} {y + h - largo}V{y + h}H{x + w - largo}"
         f"M{x + largo} {y + h}H{x}V{y + h - largo}")
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-opacity="{opacidad}" stroke-linecap="square"/>')


def brillo(gid: str, color: str, opacidad: float, medio: float = 0.0) -> str:
    """Degradado radial de un color a transparente (para halos y brillos)."""
    centro = f'<stop offset="0" stop-color="{color}" stop-opacity="{num(opacidad)}"/>'
    intermedio = (f'<stop offset=".5" stop-color="{color}" stop-opacity="{num(medio)}"/>' if medio else "")
    return (f'<radialGradient id="{gid}">{centro}{intermedio}'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def degradado(gid: str, colores, x2: float = 1, y2: float = 0, opacidades=None) -> str:
    paradas = []
    n = len(colores)
    for i, c in enumerate(colores):
        op = f' stop-opacity="{num(opacidades[i])}"' if opacidades else ""
        paradas.append(f'<stop offset="{num(i / (n - 1) if n > 1 else 0)}" stop-color="{c}"{op}/>')
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{"".join(paradas)}</linearGradient>'


def hexagono(cx, cy, r) -> str:
    import math
    puntos = [(cx + r * math.cos(math.radians(90 + 60 * i)), cy + r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    return "M" + "L".join(f"{num(px)} {num(py)}" for px, py in puntos) + "Z"


# ─────────────────────────────────────────────────────────────────────────────
#  Íconos propios (trazos en una cuadrícula de 24×24; ninguno es logotipo de marca)
# ─────────────────────────────────────────────────────────────────────────────

ICONOS = {
    "escudo": '<path d="M12 2.5 20 5.5V11c0 5-3.4 8.8-8 10.5C7.4 19.8 4 16 4 11V5.5Z"/>'
              '<rect x="9" y="11" width="6" height="5" rx="1"/><path d="M10 11V9.5a2 2 0 0 1 4 0V11"/>',
    "red": '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/>'
           '<circle cx="12" cy="12.5" r="2"/><path d="M12 7v3.5M10.4 13.8 6.6 16.7M13.6 13.8l3.8 2.9M7 18h10"/>',
    "gestion": '<circle cx="9.5" cy="9.5" r="3"/><path d="M9.5 3v2M9.5 14v2M3 9.5h2M14 9.5h2M5 5l1.4 1.4'
               'M12.6 12.6 14 14M5 14l1.4-1.4M12.6 6.4 14 5"/><path d="M16 21v-4M19 21v-7M22 21V11"/>',
    "carpeta": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
               '<path d="m10 11-2 2 2 2M14 11l2 2-2 2"/>',
    "objetivo": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>'
                '<path d="M12 1v3M12 20v3M1 12h3M20 12h3"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx=".8"/>'
            '<path d="M9 2v4M12 2v4M15 2v4M9 18v4M12 18v4M15 18v4M2 9h4M2 12h4M2 15h4M18 9h4M18 12h4M18 15h4"/>',
    "birrete": '<path d="M2 9 12 4l10 5-10 5Z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>',
    "maletin": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 12.5h18M11 12.5v2h2v-2"/>',
    "matraz": '<path d="M9 3h6M10 3v6L4.5 18.5A1.6 1.6 0 0 0 6 21h12a1.6 1.6 0 0 0 1.5-2.5L14 9V3"/><path d="M7.5 15h9"/>',
    "antena": '<circle cx="12" cy="9" r="2"/><path d="M8.2 5.2a5.4 5.4 0 0 0 0 7.6M15.8 5.2a5.4 5.4 0 0 1 0 7.6'
              'M5.4 2.5a9.2 9.2 0 0 0 0 13M18.6 2.5a9.2 9.2 0 0 1 0 13M12 11v10M9 21h6"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20M9 9l-2 2 2 2M15 9l2 2-2 2"/>',
    "grafica": '<path d="M3 3v18h18"/><path d="M7 16v-4M11 16V9M15 16v-6M19 16V6"/>',
    "ia": '<circle cx="12" cy="12" r="3"/><circle cx="4.5" cy="5" r="1.6"/><circle cx="19.5" cy="5" r="1.6"/>'
          '<circle cx="4.5" cy="19" r="1.6"/><circle cx="19.5" cy="19" r="1.6"/>'
          '<path d="m5.8 6.2 4 3.8M18.2 6.2l-4 3.8M5.8 17.8l4-3.8M18.2 17.8l-4-3.8M12 3v6M12 15v6"/>',
    "perfil": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.2-4 4.3-6 8-6s6.8 2 8 6"/>',
    "correo": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="m3 6.5 9 6.5 9-6.5"/>',
    "web": '<circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4" ry="9.5"/><path d="M2.5 12h19M4 7h16M4 17h16"/>',
    "repos": '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
             '<path d="m10 11-2 2 2 2M14 11l2 2-2 2"/>',
    "servidor": '<rect x="4" y="3" width="16" height="6" rx="1.5"/><rect x="4" y="10" width="16" height="6" rx="1.5"/>'
                '<path d="M8 6h.01M8 13h.01M12 20h8M4 20h4M8 16v4"/>',
}


def icono(nombre: str, x: float, y: float, lado: float, color: str, grosor: float = 2.0) -> str:
    """Ícono de `lado` píxeles con su esquina superior izquierda en (x, y)."""
    k = lado / 24
    return (f'<g transform="translate({num(x)} {num(y)}) scale({num(k, 4)})" fill="none" stroke="{color}" '
            f'stroke-width="{num(grosor / k, 2)}" stroke-linecap="round" stroke-linejoin="round">'
            f'{ICONOS.get(nombre, "")}</g>')
