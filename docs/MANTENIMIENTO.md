# Cómo mantener tu muro de GitHub

Tu muro (el README de github.com/AlfonsoCha1) **se genera** a partir de un solo archivo: `perfil.toml`.
No edites `README.md` a mano (se sobrescribe). Edita `perfil.toml` y regenera.

## Estructura del repositorio

```
perfil.toml                     ← TODOS tus datos (proyectos, tecnologías, experiencia, cursos, contacto)
README.md                       ← generado (no editar, salvo el bloque MANUAL)
assets/
  hero.svg                      ← cabecera animada: aurora, ciudad, órbitas y retrato de partículas
  hero-estatico.png             ← versión estática para LinkedIn, CV, etc.
  senal.svg                     ← cuadrícula decorativa de colores con onda luminosa
  areas.svg                     ← 4 tarjetas: Ciberseguridad / Sistemas y redes / Administración / Desarrollo e IA
  loquese/*.svg                 ← bandas animadas de cada categoría de «Lo que sé»
  tecnologias/*.svg             ← una caja neón por tecnología (logo + nombre en su color)
  tarjetas/*.svg                ← cajas neón animadas: áreas, experiencia, constancias destacadas y laboratorios
  insignias/*.svg               ← insignias hexagonales
  formacion.svg                 ← tarjetas de formación (cada una con su color)
  trayectoria.svg               ← línea de tiempo de experiencia
  secciones/*.svg               ← encabezados de sección (tema oscuro y claro)
  proyectos/*.svg               ← portadas de los proyectos destacados
  botones/*.svg                 ← botones de contacto
  fuente/particulas.json        ← puntos del retrato (sale de tu foto) · PROTEGIDO
  fuente/protegidos.json        ← huellas de los elementos protegidos
scripts/
  generar.py                    ← arma el README y guarda todo (solo Python, sin instalar nada)
  muro_graficos.py              ← dibujo de cada imagen
  muro_svg.py                   ← paleta de colores, letras e íconos
  protegidos.py                 ← comprueba que la cabecera y la cuadrícula no cambien
  fuentes/                      ← letras Space Grotesk y JetBrains Mono como trazos (licencia OFL)
  iconos-skill/                 ← logotipos de tecnologías de skill-icons (licencia MIT, ver LICENSE-skill-icons.txt)
  herramientas/retrato.py       ← convierte una foto en partículas (opcional)
  herramientas/capturar.py      ← crea la imagen estática y un GIF de vista previa (opcional)
.github/workflows/generar-perfil.yml ← regenera solo cuando cambias perfil.toml en GitHub
docs/README-anterior.md         ← tu README original, por si quieres volver a él
```

**Colores con intención** (`acento` en perfil.toml): ciberseguridad `esmeralda`; sistemas y redes `cian`/`azul`;
desarrollo e IA `violeta`; administración de tecnología y formación `ambar`/`dorado`; experiencia `coral`.
También existen `magenta` y `verde`.
Los valores exactos están al inicio de `scripts/muro_svg.py` (diccionario `OSCURO`).

## Dos formas de actualizar

**A. Desde github.com (también desde el celular)**
1. Abre `perfil.toml` en tu repositorio `AlfonsoCha1` → ícono del lápiz.
2. Haz el cambio y pulsa *Commit changes*.
3. La acción **Generar perfil** (pestaña *Actions*) regenera el README y las imágenes en 1–2 minutos.
   Solo guarda algo si de verdad cambió: no crea commits vacíos.

**B. Desde tu computadora (Windows)**
```powershell
git pull
py scripts\generar.py          # o: python scripts/generar.py
git add -A
git commit -m "Actualiza perfil"
git push
```
Necesitas Python 3.11 o superior. No hay que instalar paquetes.
Para revisar sin escribir nada: `py scripts\generar.py --verificar`.

## Proyectos

Cada proyecto es un bloque `[[proyectos]]` en `perfil.toml`.

**Agregar uno:** copia un bloque existente, pégalo debajo y cambia los datos. El `id` debe ser único, en
minúsculas y sin espacios (se usa para el nombre de la portada: `assets/proyectos/<id>.svg`).

| Campo | Para qué sirve |
|---|---|
| `nombre`, `categoria`, `estado` | Título, área y estado real (por ejemplo «Beta», «Demo funcional», «En línea»). |
| `visibilidad` | `"publico"` muestra el botón **Repositorio**; `"privado"` no enlaza el código y muestra **Visitar sitio**. |
| `repo`, `demo` | Enlaces. En privados deja `repo = ""` y pon la página en `demo`. |
| `descripcion` | Una o dos frases. |
| `funcionamiento` | Lista de pasos que aparece en «Cómo funciona». Describe lo que realmente hace. |
| `nota` | Aclaración opcional (servidor gratuito, plataformas probadas, etc.). |
| `tecnologias` | Lista corta; aparece en la portada y como etiquetas. |
| `portada` | Ilustración: `escudo`, `logs`, `ia`, `voz`, `tienda`, `lealtad` (o `web` genérica). |
| `acento`, `acento2` | Colores del degradado de la portada (ver «Colores con intención»). |
| `estado_tipo` | Estado real: `disponible`, `laboratorio`, `beta`, `demo` o `desarrollo` (chip de color en la portada). |
| `etiqueta` | Detalle corto junto al estado (por ejemplo `v0.1`, `4/14`). |
| `destacado` | `true` = sale con portada en la sección principal (se ve mejor en número par). `false` = va a la lista desplegable «Más proyectos». |
| `orden` | Número menor aparece primero. |
| `publicar` | `false` lo oculta sin borrarlo. |

**Ordenar:** cambia los números de `orden`. **Ocultar:** `publicar = false`.
**Quitar la portada:** `destacado = false` (el generador borra la portada que sobra).

## Elementos protegidos

La cabecera (`assets/hero.svg`: rostro de partículas, monograma AC, escudo, cuadro HUD, órbitas, aurora, ciudad),
la cuadrícula (`assets/senal.svg`) y las partículas (`assets/fuente/particulas.json`) están protegidas.
`python scripts/protegidos.py` comprueba sus huellas; `generar.py` se detiene sin escribir nada si un cambio
las alteraría. En la cabecera solo pueden cambiar los colores de las palabras de enfoque y de las etiquetas.
Si algún día cambias tu foto a propósito, actualiza las huellas en `assets/fuente/protegidos.json`.

## «Lo que sé»

Cuatro categorías `[[lo_que_se]]`: experiencia laboral, tecnologías en proyectos, herramientas y aprendiendo.
Cada una tiene su banda animada y una **caja neón por tecnología** (`assets/tecnologias/`), con el logo y el
nombre brillando en el color de esa tecnología. Debajo hay un desplegable con todo como texto.

```toml
{ nombre = "Python", skill = "Python-Dark", color = "#FFD43B" }                  # logotipo oficial
{ nombre = "Cisco Packet Tracer", generico = "simulador", color = "#2EE6A0" }    # ícono propio
```

- `skill`: archivo de `scripts/iconos-skill/` (sin `.svg`). Para agregar uno nuevo, copia el SVG desde
  github.com/tandpfun/skill-icons/tree/main/icons a esa carpeta (licencia MIT).
- `generico`: ícono propio (`auriculares`, `switch`, `cable`, `capas`, `huella`, `basedatos`, `respaldo`, `prueba`,
  `simulador`, `documento`, `nube`, `terminal`, `escudo`, `red`...).
- `color`: color neón de la caja. Si lo omites, usa el color de la categoría. `nota`: texto pequeño opcional.

## Cajas neón

Áreas, experiencia, constancias destacadas y laboratorios se dibujan como cajas animadas (una luz recorre el borde
y el título brilla en el color de cada elemento). Salen de los mismos datos de `perfil.toml`; el texto completo
también queda en los desplegables «Ver … como texto» para que se pueda leer y copiar.

## Experiencia, cursos y áreas

- `[[experiencia]]`: puesto, empresa, periodo, lugar y puntos. `publicar = false` la oculta.
  Para la línea de tiempo usa `anio`, `empresa_corta`, `puesto_corto`, `acento` e `icono` (hoja, balanza, banco, fabrica...).
- `[[formacion]]`: estudios académicos (lista detallada).
- `[[formacion_tarjetas]]`: las 4 tarjetas (`icono`, `acento`, `titulo` en dos líneas, `detalle`, `periodo`).
- `[[cursos]]`: usa el **nombre exacto** del certificado, el emisor y la fecha. Pon el enlace en `verificacion`
  solo si es una verificación oficial (por ejemplo `coursera.org/verify/...`). `otros = true` lo manda al bloque
  «Otras constancias». `destacado = true` + `insignia` la muestra en la tabla visible de constancias destacadas. Un curso o constancia **no** es una certificación profesional: el campo `tipo`
  lo deja claro.
- `[[areas]]`: las cuatro tarjetas (`titulo_lineas` parte el título en dos líneas). `lema` son las dos líneas cortas de la tarjeta; `puntos`, el detalle debajo.
- `[[laboratorios]]`: lo que estás construyendo o lo que viene.

## Texto propio que no quieres que se borre

Escribe entre `<!-- MANUAL:INICIO -->` y `<!-- MANUAL:FIN -->` en `README.md`. Ese bloque se conserva al regenerar.

## Cambiar la foto del retrato holográfico

El retrato sale de la foto de tu portafolio (`imagenes_yo/Yo_uno.jpg`). Para usar otra:

```powershell
py -m pip install pillow numpy opencv-python-headless "rembg[cpu]"
py scripts\herramientas\retrato.py C:\ruta\a\tu_foto.jpg
py scripts\generar.py
```

- Funciona mejor con una foto de frente, bien iluminada, con la cara y los hombros.
- Si sale algo que no quieres (por ejemplo el celular en una selfie), ajusta `--excluir` y `--recorte`
  (fracciones del ancho y alto de la foto). Ejemplo: `--recorte 0.20,0.00,0.80,0.47`.
- La foto **no** se guarda en el repositorio, solo los puntos (`assets/fuente/particulas.json`).
- La primera vez, `rembg` descarga un modelo de unos 170 MB para recortar el fondo.

## Imagen estática y GIF

GitHub no los necesita (usa `hero.svg`), pero sirven para LinkedIn o tu CV:

```powershell
py -m pip install playwright pillow
py -m playwright install chromium
py scripts\herramientas\capturar.py          # assets/hero-estatico.png
py scripts\herramientas\capturar.py --gif    # además assets/hero-vista.gif
```

## Qué puede y qué no puede hacer un README de GitHub

- GitHub **elimina** `<script>`, `<style>`, `<iframe>`, `class`, `id` y estilos en línea del README. Por eso todo
  el diseño está dentro de las imágenes SVG, y el texto importante está como texto real con enlaces reales.
- Las animaciones son **CSS dentro de los SVG**, que GitHub muestra con `<img>`. No usan JavaScript, canvas ni
  WebGL, y no cargan fuentes ni archivos externos.
- No se puede cambiar la barra lateral, la navegación, los botones ni los repositorios fijados de GitHub: eso no
  es parte del README.
- Los encabezados de sección cambian entre tema claro y oscuro con `<picture>` (función oficial de GitHub).
  La cabecera, los paneles, las tarjetas y las portadas son oscuros en ambos temas, a propósito.
- En celulares la tabla de proyectos se ve en dos columnas más angostas.

### Accesibilidad y reproducción automática

- Cada imagen tiene texto alternativo y los SVG traen `<title>` y `<desc>`.
- Si la persona activó «reducir movimiento» en su sistema, las animaciones se detienen y se ve el rostro fijo.
  Esto depende de que su navegador lo respete dentro de imágenes SVG (Chrome, Edge, Firefox y Safari actuales sí).
- GitHub no ofrece un botón de pausa para animaciones dentro de imágenes: no se puede agregar desde el README.
  Por eso los efectos son lentos, sin destellos fuertes, y el ciclo principal dura 16 segundos.
- La aplicación móvil de GitHub y algunos lectores de RSS pueden mostrar los SVG sin animación.
- GitHub guarda en caché las imágenes: después de un cambio, a veces tarda unos minutos en verse.

### Sobre los datos

- Las cuadrículas de cuadritos son **decorativas** y lo dicen en la imagen. Tu actividad real es la gráfica de
  contribuciones que GitHub pone debajo del README.
- No hay contadores de visitas, estadísticas de terceros ni servicios externos: nada puede quedar como panel vacío.

## Volver al README anterior

Copia el contenido de `docs/README-anterior.md` sobre `README.md` y haz commit. Si quieres quedarte con el
anterior de forma permanente, desactiva la acción en *Actions → Generar perfil → Disable workflow*.
