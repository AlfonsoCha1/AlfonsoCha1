"""Extrae los contornos de las letras de una fuente a un JSON pequeño.

Solo hace falta correrlo si quieres cambiar de tipografía. El generador
(`scripts/generar.py`) usa los JSON resultantes y así no depende de fuentes
instaladas ni de internet: el texto de las imágenes se dibuja como trazos SVG,
que GitHub muestra igual en cualquier equipo.

Requiere:  pip install fonttools
Uso:       python scripts/herramientas/extraer_glifos.py fuente.woff salida.json
"""

import json
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

CARACTERES = (
    "".join(chr(c) for c in range(32, 127))
    + "¡¿áéíóúÁÉÍÓÚñÑüÜ·•—–…°ºª×→←↗"
)


def redondear_ruta(d: str) -> str:
    salida = []
    for token in d.replace(",", " ").split():
        try:
            valor = float(token)
            salida.append(str(int(round(valor))))
        except ValueError:
            salida.append(token)
    return " ".join(salida)


def main(origen: str, destino: str) -> None:
    fuente = TTFont(origen)
    cmap = fuente.getBestCmap()
    glifos = fuente.getGlyphSet()
    hmtx = fuente["hmtx"]
    datos = {
        "unidades": fuente["head"].unitsPerEm,
        "ascendente": fuente["hhea"].ascent,
        "descendente": fuente["hhea"].descent,
        "glifos": {},
    }
    for caracter in CARACTERES:
        nombre = cmap.get(ord(caracter))
        if nombre is None:
            continue
        pluma = SVGPathPen(glifos)
        glifos[nombre].draw(pluma)
        datos["glifos"][caracter] = {
            "d": redondear_ruta(pluma.getCommands()),
            "w": hmtx[nombre][0],
        }
    with open(destino, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, separators=(",", ":"))
    print(f"{destino}: {len(datos['glifos'])} glifos")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
