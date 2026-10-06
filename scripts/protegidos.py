"""Protección de los elementos animados que no deben cambiar.

Protegidos:
  - assets/hero.svg: rostro holográfico de partículas, monograma AC, escudo, cuadro HUD,
    escaneo, órbitas, aurora, ciudad, terminal y nombre. Lo único que se puede cambiar
    son los colores de las palabras de enfoque y de las etiquetas («chips») debajo de ellas.
  - assets/senal.svg: la cuadrícula de cuadritos (byte por byte).
  - assets/fuente/particulas.json: los puntos del retrato (byte por byte).

Las huellas SHA-256 esperadas están en assets/fuente/protegidos.json. generar.py las
comprueba antes de escribir: si algo protegido cambiaría, se detiene sin tocar nada.

Uso directo (comprueba los archivos que ya están en el repositorio):
    python scripts/protegidos.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from xml.etree import ElementTree

RAIZ = Path(__file__).resolve().parents[1]
REGISTRO = RAIZ / "assets" / "fuente" / "protegidos.json"
SVG_NS = "{http://www.w3.org/2000/svg}"

# Grupos de la cabecera que sí se pueden editar (solo colores de texto)
GRUPOS_EDITABLES = {"animation-delay:1.8s", "animation-delay:1.95s"}


def _sha(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def huella_cabecera(svg: str) -> str:
    """Huella de hero.svg sin los grupos editables (textos de enfoque y etiquetas)."""
    ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    raiz = ElementTree.fromstring(svg)
    padres = {hijo: padre for padre in raiz.iter() for hijo in padre}
    quitados = 0
    for g in list(raiz.iter(f"{SVG_NS}g")):
        if g.get("class") == "en" and g.get("style") in GRUPOS_EDITABLES:
            padres[g].remove(g)
            quitados += 1
    if quitados != len(GRUPOS_EDITABLES):
        raise ValueError(f"Se esperaban {len(GRUPOS_EDITABLES)} grupos editables en hero.svg y hay {quitados}")
    return _sha(ElementTree.tostring(raiz, encoding="utf-8"))


def huellas(hero_svg: str, senal_svg: str, particulas: bytes) -> dict[str, str]:
    return {
        "hero.svg (sin textos de enfoque)": huella_cabecera(hero_svg),
        "senal.svg": _sha(senal_svg.encode("utf-8")),
        "fuente/particulas.json": _sha(particulas),
    }


def comprobar(hero_svg: str, senal_svg: str, particulas: bytes) -> list[str]:
    """Devuelve la lista de elementos protegidos que cambiaron (vacía si todo está igual)."""
    esperadas = json.loads(REGISTRO.read_text(encoding="utf-8"))["huellas"]
    actuales = huellas(hero_svg, senal_svg, particulas)
    return [nombre for nombre, valor in actuales.items() if esperadas.get(nombre) != valor]


def main() -> int:
    assets = RAIZ / "assets"
    cambios = comprobar((assets / "hero.svg").read_text(encoding="utf-8"),
                        (assets / "senal.svg").read_text(encoding="utf-8"),
                        (assets / "fuente" / "particulas.json").read_bytes())
    if cambios:
        print("Cambiaron elementos protegidos:", ", ".join(cambios))
        return 1
    print("Elementos protegidos intactos: rostro holográfico, monograma AC, partículas, cuadro HUD y cuadrícula.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
