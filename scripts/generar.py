#!/usr/bin/env python3
"""Genera el README del perfil y todas sus imágenes a partir de perfil.toml.

Uso
    python scripts/generar.py              genera README.md y assets/
    python scripts/generar.py --verificar  solo revisa que todo esté al día (no escribe)

Requisitos: Python 3.11 o superior. Solo usa la biblioteca estándar: no necesita
paquetes, fuentes instaladas ni internet. El texto de las imágenes se dibuja como
trazos (scripts/fuentes/*.json), así se ve igual en cualquier equipo.

El resultado es reproducible: con el mismo perfil.toml siempre sale lo mismo.

Archivos:
    scripts/muro_svg.py       paleta, texto como trazos e íconos
    scripts/muro_graficos.py  cada imagen (cabecera, portadas, «Lo que sé», etc.)
    scripts/generar.py        este archivo: arma el README y guarda todo
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parent))

import muro_graficos as g  # noqa: E402
from muro_svg import FALTANTES, TEMAS, esc  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "perfil.toml"
README = RAIZ / "README.md"
ASSETS = RAIZ / "assets"
PARTICULAS = ASSETS / "fuente" / "particulas.json"

MANUAL_INI = "<!-- MANUAL:INICIO -->"
MANUAL_FIN = "<!-- MANUAL:FIN -->"

# clave: (título, descripción, ícono, acento)
SECCIONES = {
    "proyectos": ("Proyectos destacados", "Proyectos con enlaces reales", "carpeta", "cian"),
    "areas": ("Áreas", "Ciberseguridad, sistemas y administración de tecnología", "objetivo", "violeta"),
    "loquese": ("Lo que sé", "Tecnologías que uso y que estoy aprendiendo", "chip", "azul"),
    "formacion": ("Formación y constancias", "Estudios, cursos y constancias", "birrete", "ambar"),
    "experiencia": ("Experiencia", "Trayectoria profesional", "maletin", "verde"),
    "laboratorios": ("Laboratorios en desarrollo", "Lo que sigue", "matraz", "magenta"),
    "contacto": ("Contacto", "Enlaces de contacto", "antena", "cian"),
}

# clave, texto, ícono, acento
BOTONES = [
    ("linkedin", "LinkedIn", "perfil", "azul"),
    ("correo", "Correo", "correo", "cian"),
    ("portafolio", "Portafolio", "web", "violeta"),
    ("repositorios", "Repositorios", "repos", "verde"),
]

ANCHOS_ENCABEZADO: dict[str, int] = {}


# ─────────────────────────────────────────────────────────────────────────────
#  Piezas del README
# ─────────────────────────────────────────────────────────────────────────────

def imagen_tema(base: str, alt: str, ancho: str = "100%") -> str:
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}-oscuro.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="{base}-claro.svg">'
            f'<img src="{base}-oscuro.svg" width="{ancho}" alt="{esc(alt)}"></picture>')


def imagen(ruta: str, alt: str, ancho: str = "100%") -> str:
    return f'<img src="{ruta}" width="{ancho}" alt="{esc(alt)}">'


def titulo_seccion(clave: str) -> str:
    titulo = SECCIONES[clave][0]
    return f'<h3>{imagen_tema(f"assets/secciones/{clave}", titulo, str(ANCHOS_ENCABEZADO.get(clave, 400)))}</h3>'


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
        "linkedin": con["linkedin"], "correo": f"mailto:{con['correo']}",
        "portafolio": con["portafolio"], "repositorios": repos_url,
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
    a(f'<p align="center">{imagen("assets/hero.svg", alt_hero)}</p>\n')
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
    a(f'<p align="center">{imagen("assets/senal.svg", "Cuadrícula decorativa animada (no representa actividad real)")}</p>\n')

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
        a('<tr><th align="left">Proyecto</th><th align="left">Qué es</th><th align="left">Enlaces</th></tr>')
        for p in otros:
            a(f"<tr><td><b>{esc(p['nombre'])}</b><br><sub>{esc(p['categoria'])}</sub></td>"
              f"<td>{esc(p['descripcion'])}</td><td>{enlaces_proyecto(p)}</td></tr>")
        a("</table>\n")
        a("</details>\n")
    a(f'<p>→ <a href="{repos_url}"><b>Ver todos mis repositorios públicos</b></a></p>\n')

    # Áreas
    a(titulo_seccion("areas") + "\n")
    nombres_areas = ", ".join(x["titulo"] for x in perfil["areas"])
    a(f'<p align="center">{imagen("assets/areas.svg", "Áreas: " + nombres_areas)}</p>\n')
    for area in perfil["areas"]:
        a(f"**{area['titulo']}**\n")
        for punto in area["puntos"]:
            a(f"- {punto}")
        a("")

    # Lo que sé
    grupos = perfil["lo_que_se"]
    a(titulo_seccion("loquese") + "\n")
    todos = ", ".join(it["nombre"] for gr in grupos for it in gr["items"])
    a(f'<p align="center">{imagen("assets/lo-que-se.svg", "Lo que sé: " + todos)}</p>\n')
    c = perfil["conocimientos"]
    a("<details><summary><b>Ver como texto, separado por dónde lo he usado</b></summary>\n")
    a("| Dónde | Conocimientos |")
    a("|:--|:--|")
    a(f"| **En el trabajo** | {chips(c['trabajo'])} |")
    a(f"| **En mis proyectos** | {chips(c['proyectos'])} |")
    a(f"| **Aprendiendo** | {chips(c['aprendiendo'])} |")
    a(f"| **Herramientas** | {chips(c['herramientas'])} |")
    a("\n</details>\n")

    # Formación y constancias
    a(titulo_seccion("formacion") + "\n")
    tarjetas = perfil["formacion_tarjetas"]
    alt_f = "Formación: " + "; ".join(" ".join(t["titulo"]) for t in tarjetas)
    a(f'<p align="center">{imagen("assets/formacion.svg", alt_f)}</p>\n')
    cursos = [x for x in perfil["cursos"] if x.get("publicar", True)]
    a(f"<details><summary><b>Ver estudios, cursos y constancias</b> — nombre exacto, emisor, fecha y "
      f"enlace de verificación ({len(perfil['formacion']) + len(cursos)})</summary>\n")
    a("**Formación académica**\n")
    for f in perfil["formacion"]:
        a(f"- **{f['programa']}** — {f['institucion']} · {f['periodo']} · {f['modalidad']}")
    a("")
    grupos_c: dict[str, list] = {}
    for curso in cursos:
        if not curso.get("otros"):
            grupos_c.setdefault(curso["grupo"], []).append(curso)

    def linea_curso(x):
        texto = f"- **{x['nombre']}** — {x['emisor']} · {x['fecha']} · {x['tipo']}"
        if x.get("verificacion"):
            texto += f" · [verificar]({x['verificacion']})"
        return texto

    for grupo, lista in grupos_c.items():
        a(f"**{grupo}**\n")
        for x in lista:
            a(linea_curso(x))
        a("")
    adicionales = [x for x in cursos if x.get("otros")]
    if adicionales:
        a("**Otras constancias**\n")
        for x in adicionales:
            a(linea_curso(x))
        a("")
    a("</details>\n")
    a("<sub>Las constancias de Coursera son cursos en línea sin créditos académicos; cada enlace de verificación "
      "viene de su certificado. Los cursos de Cisco Networking Academy son certificados de finalización de curso, "
      "no la certificación CCNA.</sub>\n")

    # Experiencia
    experiencia = visibles(perfil["experiencia"])
    a(titulo_seccion("experiencia") + "\n")
    alt_t = "Trayectoria: " + " → ".join(f"{e['anio']} {e['empresa_corta']}" for e in reversed(experiencia))
    a(f'<p align="center">{imagen("assets/trayectoria.svg", alt_t)}</p>\n')
    for e in experiencia:
        a(f"**{e['puesto']}** · {e['empresa']}  ")
        a(f"<sub>{esc(e['periodo'])} · {esc(e['lugar'])}</sub>\n")
        for punto in e["puntos"]:
            a(f"- {punto}")
        a("")

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
        a(f'  <a href="{esc(enlaces_contacto[clave])}">{imagen(f"assets/botones/{clave}.svg", texto, "200")}</a>')
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
    salida[ASSETS / "hero.svg"] = g.hero(perfil, particulas)
    salida[ASSETS / "senal.svg"] = g.senal()
    salida[ASSETS / "areas.svg"] = g.areas(perfil)
    salida[ASSETS / "lo-que-se.svg"] = g.lo_que_se(perfil["lo_que_se"])
    salida[ASSETS / "formacion.svg"] = g.formacion(perfil["formacion_tarjetas"])
    salida[ASSETS / "trayectoria.svg"] = g.trayectoria(visibles(perfil["experiencia"]))
    for tema in TEMAS:
        for clave, (titulo, nota, icono_nombre, acento) in SECCIONES.items():
            svg, ancho = g.encabezado(titulo, nota, icono_nombre, acento, tema)
            ANCHOS_ENCABEZADO[clave] = ancho
            salida[ASSETS / "secciones" / f"{clave}-{tema}.svg"] = svg
    for clave, texto, icono_nombre, acento in BOTONES:
        salida[ASSETS / "botones" / f"{clave}.svg"] = g.boton(texto, icono_nombre, acento)
    destacados = [p for p in visibles(perfil["proyectos"]) if p.get("destacado")]
    for i, p in enumerate(destacados, start=1):
        salida[ASSETS / "proyectos" / f"{p['id']}.svg"] = g.portada(p, i)
    for ruta, contenido in salida.items():
        try:
            ElementTree.fromstring(contenido)
        except ElementTree.ParseError as error:
            raise SystemExit(f"SVG inválido en {ruta.name}: {error}")
    salida[README] = construir_readme(perfil, readme_actual)
    return salida


CARPETAS_GENERADAS = ["proyectos", "secciones", "botones"]  # lo que sobre ahí se borra


def sobrantes(salida: dict[Path, str]) -> list[Path]:
    resultado = []
    for carpeta in CARPETAS_GENERADAS:
        d = ASSETS / carpeta
        if d.exists():
            resultado += [r for r in d.glob("*.svg") if r not in salida]
    resultado += [r for r in ASSETS.glob("*.svg") if r not in salida]  # SVG sueltos de versiones anteriores
    return resultado


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
    sobra = sobrantes(salida)

    if FALTANTES:
        print("Aviso: estos caracteres no existen en la tipografía y salen como «?» en las imágenes: "
              + " ".join(sorted(FALTANTES)), file=sys.stderr)

    relativas = [str(r.relative_to(RAIZ)) for r in desactualizados]
    if args.verificar:
        if relativas or sobra:
            print("Hay archivos desactualizados. Corre: python scripts/generar.py")
            for r in relativas:
                print("  -", r)
            for r in sobra:
                print("  - sobra:", r.relative_to(RAIZ))
            return 1
        print("Todo al día.")
        return 0
    for r in sobra:
        r.unlink()
    print(f"Listo: {len(relativas)} archivo(s) actualizados, {len(sobra)} sobrante(s) eliminados.")
    for r in relativas:
        print("  -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
