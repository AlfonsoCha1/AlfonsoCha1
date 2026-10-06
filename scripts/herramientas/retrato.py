"""Convierte una foto en las partículas del retrato holográfico de la cabecera.

Genera `assets/fuente/particulas.json` con tres figuras:
  - rostro: puntos tomados de la foto (conserva tus rasgos reales)
  - ac:     monograma AC con cursor de terminal
  - escudo: escudo con cerradura (ciberseguridad)

Después corre `python scripts/generar.py` para reconstruir `assets/hero.svg`.

Requiere (solo para este script, no para el generador):
    pip install pillow numpy opencv-python-headless "rembg[cpu]"

Uso:
    python scripts/herramientas/retrato.py ruta/a/tu_foto.jpg
    python scripts/herramientas/retrato.py foto.jpg --mascara mascara.png   # si ya tienes el recorte

Ajustes del encuadre (fracciones del ancho/alto de la foto):
    --recorte 0.20,0.00,0.80,0.47   izquierda, arriba, derecha, abajo
    --excluir 0.58,0.42,1,1         zona que se ignora (por ejemplo, el celular en una selfie)

La foto original NO se guarda en el repositorio; solo los puntos resultantes.
"""

import argparse
import json
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "assets" / "fuente" / "particulas.json"
FUENTE_AC = Path(__file__).resolve().parent / "SpaceGrotesk-Bold.woff"

ANCHO, ALTO = 400, 420  # área del marco donde viven las partículas
CELDA = 5
CELDA_ROSTRO = 4
GRUPOS = {"rostro": 40, "ac": 24, "escudo": 24}


def mascara_persona(foto: Image.Image) -> Image.Image:
    from rembg import new_session, remove

    sesion = new_session("u2net_human_seg")
    return remove(foto, session=sesion, only_mask=True)


def puntos_rostro(foto, mascara, recorte, excluir, rnd):
    w, h = foto.size
    caja = (int(w * recorte[0]), int(h * recorte[1]), int(w * recorte[2]), int(h * recorte[3]))
    gris = np.asarray(foto.convert("L"), dtype=np.uint8)
    alfa = np.asarray(mascara.convert("L"), dtype=np.float32) / 255.0

    ex = (int(w * excluir[0]), int(h * excluir[1]), int(w * excluir[2]), int(h * excluir[3]))
    alfa[ex[1]:ex[3], ex[0]:ex[2]] = 0

    gris = gris[caja[1]:caja[3], caja[0]:caja[2]]
    alfa = alfa[caja[1]:caja[3], caja[0]:caja[2]]
    ch, cw = gris.shape

    escala = min((ANCHO - 30) / cw, (ALTO - 10) / ch)
    ow, oh = int(cw * escala), int(ch * escala)
    ox, oy = (ANCHO - ow) / 2, (ALTO - oh) / 2 + 6

    # Luminosidad por celda a la resolución final
    lum = cv2.resize(gris, (ow, oh), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    msk = cv2.resize(alfa, (ow, oh), interpolation=cv2.INTER_AREA)
    dentro = msk > 0.5

    # Corrige la luz desigual de la foto: mezcla la luminosidad global con la
    # local (dividida entre su versión muy desenfocada) para que ojos, cejas,
    # nariz y boca se lean igual en los dos lados de la cara.
    relleno = lum.copy()
    relleno[~dentro] = lum[dentro].mean()
    local = lum / (cv2.GaussianBlur(relleno, (0, 0), 18) + 1e-3)

    def normalizar(x):
        bajo, alto = np.percentile(x[dentro], [5, 97])
        return np.clip((x - bajo) / max(1e-3, alto - bajo), 0, 1)

    valor = (0.4 * normalizar(lum) + 0.6 * normalizar(local)) ** 1.1
    distancia = cv2.distanceTransform(dentro.astype(np.uint8), cv2.DIST_L2, 5)
    # La parte baja (cuello y hombros) se disuelve en datos sueltos
    desvanecer = np.clip((1.0 - np.linspace(0, 1, oh)) / 0.24, 0, 1)

    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
    c = CELDA_ROSTRO
    puntos = []
    for fy, y in enumerate(range(c // 2, oh, c)):
        for fx, x in enumerate(range(c // 2, ow, c)):
            if msk[y, x] < 0.4:
                continue
            celda = valor[max(0, y - c // 2): y + c // 2 + 1, max(0, x - c // 2): x + c // 2 + 1]
            v = float(celda.mean())
            contorno = distancia[y, x] < c * 1.2 and y < oh - 2 * c
            if v > 0.10 + 0.80 * bayer[fy % 4, fx % 4] or contorno:
                if contorno:
                    v = max(v, 0.5)
                f = desvanecer[y]
                if f < 1 and rnd.random() > f:
                    continue
                puntos.append((ox + x, oy + y, v * (0.55 + 0.45 * f)))
    return puntos


def puntos_de_figura(imagen_mascara, rnd, relleno=0.42):
    m = np.asarray(imagen_mascara, dtype=np.uint8)
    dist = cv2.distanceTransform((m > 127).astype(np.uint8), cv2.DIST_L2, 5)
    puntos = []
    for y in range(CELDA // 2, ALTO, CELDA):
        for x in range(CELDA // 2, ANCHO, CELDA):
            if m[y, x] > 127:
                borde = dist[y, x] < CELDA * 1.4
                if borde or rnd.random() < relleno:
                    v = 0.62 + rnd.random() * 0.3 if borde else 0.25 + rnd.random() * 0.3
                    puntos.append((x + (rnd.random() - 0.5) * 1.2, y + (rnd.random() - 0.5) * 1.2, v))
    return puntos


def figura_ac():
    img = Image.new("L", (ANCHO, ALTO), 0)
    d = ImageDraw.Draw(img)
    fuente = ImageFont.truetype(str(FUENTE_AC), 230)
    texto = "AC"
    caja = d.textbbox((0, 0), texto, font=fuente)
    tw, th = caja[2] - caja[0], caja[3] - caja[1]
    x = (ANCHO - tw) / 2 - caja[0] - 46
    y = (ALTO - th) / 2 - caja[1] - 6
    d.text((x, y), texto, font=fuente, fill=255)
    # cursor de terminal tipo guion bajo: «AC_»
    cx = x + caja[2] + 12
    d.rectangle([cx, y + caja[3] - 18, cx + 58, y + caja[3]], fill=255)
    return img


def figura_escudo():
    img = Image.new("L", (ANCHO, ALTO), 0)
    d = ImageDraw.Draw(img)
    cx, top = ANCHO / 2, 44
    ancho, alto = 280, 330
    contorno = [
        (cx, top), (cx + ancho / 2, top + 52), (cx + ancho / 2, top + alto * 0.48),
        (cx + ancho * 0.33, top + alto * 0.78), (cx, top + alto),
        (cx - ancho * 0.33, top + alto * 0.78), (cx - ancho / 2, top + alto * 0.48),
        (cx - ancho / 2, top + 52),
    ]
    d.polygon(contorno, fill=255)
    interior = [(cx + (px - cx) * 0.84, top + 26 + (py - top) * 0.84) for px, py in contorno]
    d.polygon(interior, fill=0)
    # candado
    d.rounded_rectangle([cx - 58, top + 148, cx + 58, top + 236], radius=12, fill=255)
    d.arc([cx - 40, top + 92, cx + 40, top + 184], 180, 360, fill=255, width=14)
    d.ellipse([cx - 11, top + 172, cx + 11, top + 194], fill=0)
    d.rectangle([cx - 5, top + 186, cx + 5, top + 214], fill=0)
    return img


def empaquetar(puntos, grupos, rnd, celda):
    salida = []
    for x, y, v in puntos:
        x, y, v = float(x), float(y), float(v)
        tam = round((0.55 + 0.30 * v) * celda * 2) / 2
        color = min(7, int(v * 8))
        opac = int(40 + 60 * v)
        salida.append([round(x * 2) / 2, round(y * 2) / 2, tam, color, opac, rnd.randrange(grupos)])
    return salida


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("foto")
    p.add_argument("--mascara")
    p.add_argument("--recorte", default="0.20,0.00,0.80,0.47")
    p.add_argument("--excluir", default="0.58,0.42,1,1")
    p.add_argument("--semilla", type=int, default=2050)
    a = p.parse_args()

    rnd = random.Random(a.semilla)
    foto = Image.open(a.foto).convert("RGB")
    mascara = Image.open(a.mascara).convert("L") if a.mascara else mascara_persona(foto)
    recorte = [float(v) for v in a.recorte.split(",")]
    excluir = [float(v) for v in a.excluir.split(",")]

    datos = {
        "marco": [ANCHO, ALTO],
        "rostro": empaquetar(puntos_rostro(foto, mascara, recorte, excluir, rnd), GRUPOS["rostro"], rnd, CELDA_ROSTRO),
        "ac": empaquetar(puntos_de_figura(figura_ac(), rnd, 0.40), GRUPOS["ac"], rnd, CELDA),
        "escudo": empaquetar(puntos_de_figura(figura_escudo(), rnd, 0.30), GRUPOS["escudo"], rnd, CELDA),
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, separators=(",", ":")), encoding="utf-8")
    print({k: len(v) for k, v in datos.items() if k != "marco"}, "->", SALIDA)


if __name__ == "__main__":
    main()
