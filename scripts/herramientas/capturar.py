"""Captura la cabecera animada: imagen estática (PNG) y, opcionalmente, un GIF o cuadros sueltos.

La versión estática sirve para LinkedIn, tu CV o cualquier lugar que no reproduzca
animaciones SVG. GitHub NO la necesita: el README usa directamente assets/hero.svg.

Requiere:  pip install playwright pillow   y luego   python -m playwright install chromium
Uso:
    python scripts/herramientas/capturar.py                  # assets/hero-estatico.png
    python scripts/herramientas/capturar.py --gif            # además assets/hero-vista.gif
    python scripts/herramientas/capturar.py --cuadros 1,6,9  # PNG en esos segundos (para revisar)
"""

import argparse
import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[2]
HERO = RAIZ / "assets" / "hero.svg"


def abrir(pagina, svg: Path):
    pagina.goto(svg.resolve().as_uri())
    pagina.wait_for_timeout(300)
    pagina.evaluate("document.getAnimations().forEach(a => a.pause())")


def en_segundo(pagina, segundo: float) -> bytes:
    pagina.evaluate(
        "t => document.getAnimations().forEach(a => { a.currentTime = t * 1000; })",
        segundo,
    )
    pagina.wait_for_timeout(30)
    return pagina.screenshot(omit_background=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gif", action="store_true")
    p.add_argument("--cuadros", default="")
    p.add_argument("--salida", default=str(RAIZ / "assets"))
    a = p.parse_args()
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pagina = nav.new_page(viewport={"width": 1200, "height": 540}, device_scale_factor=1)
        abrir(pagina, HERO)
        # Estática: rostro formado y textos visibles (segundo 4 del ciclo)
        Image.open(io.BytesIO(en_segundo(pagina, 4.0))).save(salida / "hero-estatico.png", optimize=True)
        print("->", salida / "hero-estatico.png")

        for s in [x for x in a.cuadros.split(",") if x.strip()]:
            ruta = salida / f"hero-t{float(s):05.2f}.png"
            Image.open(io.BytesIO(en_segundo(pagina, float(s)))).save(ruta)
            print("->", ruta)

        if a.gif:
            cuadros = []
            fps = 12
            for i in range(int(16 * fps)):
                img = Image.open(io.BytesIO(en_segundo(pagina, 2.2 + i / fps))).convert("RGBA")
                fondo = Image.new("RGBA", img.size, "#0d1117")
                img = Image.alpha_composite(fondo, img).convert("RGB")
                cuadros.append(img.resize((600, 270), Image.LANCZOS))
            ruta = salida / "hero-vista.gif"
            paleta = cuadros[len(cuadros) // 5].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
            convertidos = [c.quantize(palette=paleta, dither=Image.Dither.NONE) for c in cuadros]
            convertidos[0].save(ruta, save_all=True, append_images=convertidos[1:], duration=int(1000 / fps),
                                loop=0, optimize=True, disposal=1)
            print("->", ruta)
        nav.close()


if __name__ == "__main__":
    main()
