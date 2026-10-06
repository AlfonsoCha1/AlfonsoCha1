<!--
  ESTE ARCHIVO SE GENERA AUTOMÁTICAMENTE con scripts/generar.py a partir de perfil.toml.
  Para cambiar el contenido, edita perfil.toml (guía: docs/MANTENIMIENTO.md).
-->

<p align="center"><img src="assets/hero.svg" width="100%" alt="Alfonso Chavarín — Ciberseguridad, Sistemas y redes, Administración de tecnología. Retrato holográfico animado de partículas que se transforma en el monograma AC y en un escudo."></p>

<p align="center">
  <b>Ingeniero en Sistemas Computacionales</b> · Posgrado en Administración de Tecnologías<br>
  Cuernavaca, Morelos, México · Español nativo · Inglés B2
</p>
<p align="center">
  <a href="https://www.linkedin.com/in/alfonso-chavarin/">LinkedIn</a> · <a href="mailto:alfonso.chavarin@hotmail.com">alfonso.chavarin@hotmail.com</a> · <a href="https://portafolio-original-tau.vercel.app/">Portafolio</a> · <a href="https://github.com/AlfonsoCha1?tab=repositories">Repositorios</a>
</p>

Soy Ingeniero en Sistemas Computacionales con posgrado en Administración de Tecnologías. Mi experiencia está en soporte e implementación de TI, redes y bases de datos: di soporte a clientes internacionales en BBVA Technology, resolví problemas de conectividad y configuré switches en dependencias de gobierno, y en manufactura desarrollé y administré bases de datos de resultados de pruebas. Hoy enfoco mis proyectos en la ciberseguridad defensiva, con herramientas en Python para revisar la seguridad de proyectos y analizar registros.

**Construyendo ahora:** ALBA, un kit local para revisar la seguridad de proyectos, y nuevas herramientas para mi laboratorio de ciberseguridad en Python.

<details><summary><b>English summary</b></summary>

Computer Systems Engineer (UNINTER) with a postgraduate degree in Technology Management. Hands-on experience in IT support and implementation (BBVA Technology, international clients), networking (government agencies) and production test databases (Marelli). I am currently building defensive security tools in Python: ALBA, a local project security reviewer, and a cybersecurity lab focused on log analysis. Spanish (native) · English (B2).

</details>

<p align="center"><img src="assets/senal.svg" width="100%" alt="Cuadrícula decorativa animada (no representa actividad real)"></p>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/proyectos-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/proyectos-claro.svg"><img src="assets/secciones/proyectos-oscuro.svg" width="552" alt="Proyectos destacados"></picture></h3>

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Herramientas_cyberseguridad"><img src="assets/proyectos/alba.svg" width="100%" alt="Portada de ALBA — Mi Kit Técnico"></a>
<p><b>ALBA — Mi Kit Técnico</b><br><sub>CIBERSEGURIDAD · <b>Disponible</b> · v0.1.0 · primer módulo operativo</sub></p>
<p>Aplicación local en español para revisar la seguridad de proyectos web y Node.js y aprender mientras lo haces. Funciona sin internet y solo usa la biblioteca estándar de Python.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Eliges una carpeta (o el proyecto ficticio del laboratorio) y antes de empezar ves el alcance: qué va a leer, siempre en modo de solo lectura.</li><li>Busca secretos expuestos (16 reglas específicas + 1 genérica), configuraciones peligrosas (CORS, TLS, eval/exec, cookies, Docker) y dependencias con avisos conocidos. Si tienes Gitleaks, lo usa como segundo detector.</li><li>Cada hallazgo separa hechos, indicios e hipótesis. Los secretos nunca se muestran completos: prefijo, longitud y huella HMAC.</li><li>Propone correcciones acotadas con vista previa, aprobación ligada al cambio exacto, respaldo, verificación y reversión.</li><li>Exporta informes en HTML, Markdown y JSON.</li></ul>
<p><sub>Probado en Ubuntu 24.04 (base de Linux Mint 22). Windows y macOS: prototipo. El resto del kit está diseñado y marcado como pendiente.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Herramientas_cyberseguridad"><b>Repositorio</b></a></p>
<p><code>Python (stdlib)</code> <code>Linux</code> <code>Gitleaks</code> <code>HTML/CSS/JS</code></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad"><img src="assets/proyectos/cyber-lab.svg" width="100%" alt="Portada de Cybersecurity Python Lab"></a>
<p><b>Cybersecurity Python Lab</b><br><sub>CIBERSEGURIDAD · LABORATORIO · <b>Laboratorio</b> · 4 de 14 herramientas disponibles</sub></p>
<p>Laboratorio de ciberseguridad defensiva en Python: herramientas pequeñas e independientes, cada una con código, datos sintéticos, pruebas automáticas y guía. Son herramientas de aprendizaje, no productos para producción.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>08 · Generador de reportes: convierte eventos JSON, JSON Lines o CSV en reportes Markdown y HTML, y lista las filas que no pudo usar.</li><li>09 · Contador de intentos de login: cuenta accesos exitosos y fallidos por usuario e IP en registros de OpenSSH y otros formatos.</li><li>11 · Buscador en logs: busca palabras, IPs, rangos de red (CIDR) y fechas con líneas de contexto, sin cargar el archivo completo.</li><li>12 · Detector de múltiples accesos: alerta cuando una cuenta o IP acumula demasiados fallos en una ventana de tiempo, con evidencia.</li><li>Un menú (python menu.py) ejecuta las demostraciones y las pruebas de cada herramienta.</li></ul>
<p><sub>Las otras 10 herramientas se publican por entregas.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad"><b>Repositorio</b></a></p>
<p><code>Python</code> <code>pytest</code> <code>Análisis de logs</code> <code>Regex</code></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://ia-sophya.vercel.app/"><img src="assets/proyectos/sophya.svg" width="100%" alt="Portada de SOPHYA — Asistente de IA"></a>
<p><b>SOPHYA — Asistente de IA</b><br><sub>IA APLICADA · <b>Beta</b> · Beta gratuita · requiere cuenta</sub></p>
<p>Asistente de inteligencia artificial en español, en beta gratuita. Ayuda a investigar, redactar, analizar datos y pensar ideas de negocio.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Chat con memoria dentro de la conversación y entre sesiones; la memoria se puede exportar.</li><li>Voz: dictado y respuestas habladas.</li><li>Investigación web y modo de trabajo autónomo.</li><li>Herramientas de correo y agenda, y búsqueda de empleo.</li></ul>
<p><sub>Código privado: el enlace lleva a la aplicación.</sub></p>
</details>
<p><a href="https://ia-sophya.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
<p><code>Python</code> <code>FastAPI</code> <code>JavaScript</code></p>
</td>
<td width="50%" valign="top">
<a href="https://english-speaking-coach-nine.vercel.app/"><img src="assets/proyectos/english-coach.svg" width="100%" alt="Portada de English Speaking Coach"></a>
<p><b>English Speaking Coach</b><br><sub>IA APLICADA · VOZ · <b>Demo</b> · Demo en línea · entrevista de trabajo completa</sub></p>
<p>Practica inglés hablando con un coach de IA: te escucha, te corrige y te hace repetir las palabras difíciles.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Eliges un escenario: entrevista de trabajo, conversación cotidiana, viajes, reuniones, presentaciones o negocios.</li><li>Ajustas el nivel (A2 a C1), el estilo de corrección (Profesor o Conversación fluida) y la duración (Corta o Completa).</li><li>Toda la práctica es por voz, sin escribir; al final recibes tus 3 errores principales con ejercicios.</li><li>Un agente de IA decide cada turno; el código funciona con Groq, OpenAI o Anthropic usando una clave propia.</li></ul>
<p><sub>Código privado: el enlace lleva a la aplicación.</sub></p>
</details>
<p><a href="https://english-speaking-coach-nine.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
<p><code>TypeScript</code> <code>Next.js</code> <code>Web Speech API</code> <code>IA generativa</code></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://smuckys-bychavamon.vercel.app/"><img src="assets/proyectos/smuckys.svg" width="100%" alt="Portada de Smucky&#x27;s by Chavamon"></a>
<p><b>Smucky&#x27;s by Chavamon</b><br><sub>E-COMMERCE · <b>Disponible</b> · Tienda en línea</sub></p>
<p>Tienda en línea de mi marca de ropa deportiva y casual: playeras, blusas, playeras sin mangas y shorts deportivos.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Catálogo por categorías con carrito de compras y favoritos.</li><li>Cuenta de cliente con pedidos, entregas y devoluciones.</li><li>Pago con tarjeta de crédito o débito y Mercado Pago; pago con Stripe.</li></ul>
<p><sub>Código privado: el enlace lleva a la tienda.</sub></p>
</details>
<p><a href="https://smuckys-bychavamon.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
<p><code>HTML</code> <code>CSS</code> <code>JavaScript</code> <code>Firebase</code> <code>FastAPI</code></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Chavarin_-_Said"><img src="assets/proyectos/lealtad.svg" width="100%" alt="Portada de Chavarín &amp; Said — Lealtad"></a>
<p><b>Chavarín &amp; Said — Lealtad</b><br><sub>FULL STACK · <b>Demo</b> · Demostración funcional · base para pilotos</sub></p>
<p>Plataforma de tarjetas de puntos o sellos para pequeños negocios de comida, tiendas y servicios (nombre provisional). Todavía no está lista para negocios reales.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Directorio de negocios con categorías y búsqueda.</li><li>Registro de clientes con un QR de mostrador por sucursal; tarjeta web e impresa.</li><li>Paneles para cliente, empleado, dueño y administración; los tickets repetidos se rechazan.</li><li>La demo usa negocios y personas ficticios.</li></ul>
<p><sub>La demo está en un servidor gratuito: puede tardar alrededor de un minuto en despertar.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Chavarin_-_Said"><b>Repositorio</b></a> · <a href="https://chavarin-said-lealtad.onrender.com/"><b>Ver demo</b></a></p>
<p><code>TypeScript</code> <code>Node.js</code> <code>PostgreSQL</code> <code>Docker</code></p>
</td>
</tr>
</table>

<details><summary><b>Más proyectos, prácticas y ejercicios</b> (8)</summary>

<table>
<tr><th align="left">Proyecto</th><th align="left">Qué es</th><th align="left">Enlaces</th></tr>
<tr><td><b>Portafolio web</b><br><sub>Web</sub></td><td>Mi sitio personal con experiencia, proyectos y CV descargable.</td><td><a href="https://github.com/AlfonsoCha1/portafolio-original"><b>Repositorio</b></a> · <a href="https://portafolio-original-tau.vercel.app/"><b>Ver demo</b></a></td></tr>
<tr><td><b>Restaurante Smucky&#x27;s</b><br><sub>Práctica web</sub></td><td>Sitio de restaurante con menú por categorías, pedidos y reservaciones.</td><td><a href="https://github.com/AlfonsoCha1/PROYECTO-INTERLIGENCIA-ARTIFICIAL"><b>Repositorio</b></a> · <a href="https://proyecto-interligencia-artificial.vercel.app/"><b>Ver demo</b></a></td></tr>
<tr><td><b>Tipos-bash</b><br><sub>Automatización</sub></td><td>Scripts .bat para Windows: limpieza automática de archivos temporales y organizador de archivos de producción.</td><td><a href="https://github.com/AlfonsoCha1/Tipos-bash"><b>Repositorio</b></a></td></tr>
<tr><td><b>Java</b><br><sub>Ejercicios</sub></td><td>Ejercicios de Java: condicionales, bucles, juego de adivinar el número y sistema de descuentos.</td><td><a href="https://github.com/AlfonsoCha1/Java"><b>Repositorio</b></a></td></tr>
<tr><td><b>ESCUELA</b><br><sub>Ejercicios</sub></td><td>Prácticas escolares en C# y ASP.NET Web Forms.</td><td><a href="https://github.com/AlfonsoCha1/ESCUELA"><b>Repositorio</b></a></td></tr>
<tr><td><b>SUMA</b><br><sub>Ejercicios</sub></td><td>Ejercicio básico en C# y ASP.NET.</td><td><a href="https://github.com/AlfonsoCha1/SUMA"><b>Repositorio</b></a></td></tr>
<tr><td><b>PROYECTOS</b><br><sub>Ejercicios</sub></td><td>Ejercicios de HTML, CSS y JavaScript.</td><td><a href="https://github.com/AlfonsoCha1/PROYECTOS"><b>Repositorio</b></a></td></tr>
<tr><td><b>Versiones anteriores del portafolio</b><br><sub>Web</sub></td><td>portafolio-alfonso, Portafolio y Portafolio_Original: versiones previas de mi sitio personal.</td><td><a href="https://github.com/AlfonsoCha1/portafolio-alfonso"><b>Repositorio</b></a></td></tr>
</table>

</details>

<p>→ <a href="https://github.com/AlfonsoCha1?tab=repositories"><b>Ver todos mis repositorios públicos</b></a></p>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/areas-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/areas-claro.svg"><img src="assets/secciones/areas-oscuro.svg" width="316" alt="Áreas"></picture></h3>

<p align="center"><img src="assets/areas.svg" width="100%" alt="Áreas: Ciberseguridad, Sistemas y redes, Administración de tecnología, Desarrollo e IA"></p>

**Ciberseguridad**

- Herramientas defensivas en Python: análisis de logs, detección de accesos repetidos y búsqueda de secretos expuestos (ALBA y Cybersecurity Python Lab).
- Seguridad de red vista en CCNAv7: mitigación de amenazas, listas de control de acceso (ACL) y acceso administrativo seguro.
- Aprendiendo: blue team y análisis de eventos de seguridad.

**Sistemas y redes**

- Diagnóstico de conectividad en más de 50 estaciones de trabajo y configuración de switches (Junta de Conciliación y Arbitraje).
- Diseño e instalación de cableado estructurado, ponchado y configuración de periféricos (SEDAGRO).
- Gestión de usuarios y credenciales en Linux (BBVA Technology).

**Administración de tecnología**

- Posgrado en Administración de Tecnologías (UNINTER).
- Soporte técnico a clientes internacionales e implementación de autenticación biométrica (BBVA Technology).
- Bases de datos para el seguimiento de resultados de pruebas y respaldos de producción (Marelli).

**Desarrollo e IA**

- Aplicaciones con IA: SOPHYA (asistente en beta) y English Speaking Coach (tutor de inglés por voz, demo en línea).
- Desarrollo web: tienda en línea Smucky's y plataforma de lealtad Chavarín & Said (demo funcional).
- Diplomado en Inteligencia Artificial Generativa y Automatización (Top Learning).

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/loquese-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/loquese-claro.svg"><img src="assets/secciones/loquese-oscuro.svg" width="364" alt="Lo que sé"></picture></h3>

<p align="center"><img src="assets/loquese/experiencia.svg" width="100%" alt="Experiencia laboral: Lo que he usado en mis empleos: BBVA Technology, Marelli y dependencias de gobierno"></p>

<table align="center">
<tr>
<td align="center" width="20%"><img src="assets/iconos/soporte-tecnico.svg" width="48" height="48" alt=""><br><b>Soporte técnico</b><br><sub>primer nivel e internacional</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Linux-Dark.svg" width="48" height="48" alt=""><br><b>Linux</b><br><sub>usuarios y credenciales</sub></td>
<td align="center" width="20%"><img src="assets/iconos/switches-y-redes.svg" width="48" height="48" alt=""><br><b>Switches y redes</b><br><sub>configuración</sub></td>
<td align="center" width="20%"><img src="assets/iconos/cableado-estructurado.svg" width="48" height="48" alt=""><br><b>Cableado estructurado</b></td>
<td align="center" width="20%"><img src="assets/iconos/tcp-ip.svg" width="48" height="48" alt=""><br><b>TCP/IP</b></td>
</tr>
<tr>
<td align="center" width="20%"><img src="assets/iconos/autenticacion-biometrica.svg" width="48" height="48" alt=""><br><b>Autenticación biométrica</b><br><sub>Face ID y huella</sub></td>
<td align="center" width="20%"><img src="assets/iconos/bases-de-datos.svg" width="48" height="48" alt=""><br><b>Bases de datos</b><br><sub>seguimiento de pruebas</sub></td>
<td align="center" width="20%"><img src="assets/iconos/respaldos.svg" width="48" height="48" alt=""><br><b>Respaldos</b><br><sub>datos de producción</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Java-Dark.svg" width="48" height="48" alt=""><br><b>Java</b><br><sub>asistente digital</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/AWS-Dark.svg" width="48" height="48" alt=""><br><b>AWS</b><br><sub>soporte de infraestructura</sub></td>
</tr>
</table>

<p align="center"><img src="assets/loquese/proyectos.svg" width="100%" alt="Tecnologías en mis proyectos: Lenguajes, frameworks y bases de datos que uso en mis proyectos y estudios"></p>

<table align="center">
<tr>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/HTML.svg" width="48" height="48" alt=""><br><b>HTML5</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/CSS.svg" width="48" height="48" alt=""><br><b>CSS3</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/JavaScript.svg" width="48" height="48" alt=""><br><b>JavaScript</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/TypeScript.svg" width="48" height="48" alt=""><br><b>TypeScript</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Python-Dark.svg" width="48" height="48" alt=""><br><b>Python</b></td>
</tr>
<tr>
<td align="center" width="20%"><img src="assets/iconos/pytest.svg" width="48" height="48" alt=""><br><b>pytest</b><br><sub>pruebas automáticas</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/NodeJS-Dark.svg" width="48" height="48" alt=""><br><b>Node.js</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/FastAPI.svg" width="48" height="48" alt=""><br><b>FastAPI</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/PostgreSQL-Dark.svg" width="48" height="48" alt=""><br><b>PostgreSQL</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Firebase-Dark.svg" width="48" height="48" alt=""><br><b>Firebase</b></td>
</tr>
<tr>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Java-Dark.svg" width="48" height="48" alt=""><br><b>Java</b><br><sub>ejercicios</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/CS.svg" width="48" height="48" alt=""><br><b>C#</b><br><sub>escuela</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/DotNet.svg" width="48" height="48" alt=""><br><b>.NET</b><br><sub>ASP.NET · escuela</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/CPP.svg" width="48" height="48" alt=""><br><b>C++</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/PHP-Dark.svg" width="48" height="48" alt=""><br><b>PHP</b></td>
</tr>
</table>

<p align="center"><img src="assets/loquese/herramientas.svg" width="100%" alt="Herramientas: Para programar, versionar, diseñar, simular redes y desplegar"></p>

<table align="center">
<tr>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Git.svg" width="48" height="48" alt=""><br><b>Git</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Github-Dark.svg" width="48" height="48" alt=""><br><b>GitHub</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/VSCode-Dark.svg" width="48" height="48" alt=""><br><b>VS Code</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Figma-Dark.svg" width="48" height="48" alt=""><br><b>Figma</b></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Arduino.svg" width="48" height="48" alt=""><br><b>Arduino</b></td>
</tr>
<tr>
<td align="center" width="20%"><img src="assets/iconos/microsoft-office.svg" width="48" height="48" alt=""><br><b>Microsoft Office</b></td>
<td align="center" width="20%"><img src="assets/iconos/cisco-packet-tracer.svg" width="48" height="48" alt=""><br><b>Cisco Packet Tracer</b><br><sub>simulación de redes</sub></td>
<td align="center" width="20%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Vercel-Dark.svg" width="48" height="48" alt=""><br><b>Vercel</b></td>
<td align="center" width="20%"><img src="assets/iconos/render.svg" width="48" height="48" alt=""><br><b>Render</b><br><sub>despliegue</sub></td>
<td align="center" width="20%"><img src="assets/iconos/scripts-bat.svg" width="48" height="48" alt=""><br><b>Scripts .bat</b><br><sub>automatización en Windows</sub></td>
</tr>
</table>

<p align="center"><img src="assets/loquese/aprendiendo.svg" width="100%" alt="Actualmente aprendiendo: Lo que estoy estudiando ahora"></p>

<table align="center">
<tr>
<td align="center" width="16%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/React-Dark.svg" width="48" height="48" alt=""><br><b>React</b></td>
<td align="center" width="16%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/NextJS-Dark.svg" width="48" height="48" alt=""><br><b>Next.js</b></td>
<td align="center" width="16%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/TailwindCSS-Dark.svg" width="48" height="48" alt=""><br><b>Tailwind CSS</b></td>
<td align="center" width="16%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Docker.svg" width="48" height="48" alt=""><br><b>Docker</b></td>
<td align="center" width="16%"><img src="https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/Azure-Dark.svg" width="48" height="48" alt=""><br><b>Azure</b></td>
<td align="center" width="16%"><img src="assets/iconos/blue-team.svg" width="48" height="48" alt=""><br><b>Blue team</b><br><sub>eventos de seguridad</sub></td>
</tr>
</table>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/formacion-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/formacion-claro.svg"><img src="assets/secciones/formacion-oscuro.svg" width="587" alt="Formación y constancias"></picture></h3>

<p align="center"><img src="assets/formacion.svg" width="100%" alt="Formación: Ingeniería en Sistemas Computacionales; Posgrado en Administración de Tecnologías; Redes empresariales, seguridad y automatización; IA generativa y automatización"></p>

<table>
<tr><th></th><th align="left">Constancia destacada</th><th align="left">Emisor · fecha</th><th align="left">Verificación</th></tr>
<tr><td align="center" width="56"><img src="assets/insignias/redes.svg" width="44" height="44" alt=""></td><td><b>CCNAv7: Redes empresariales, Seguridad y Automatización</b><br><sub>certificado de finalización de curso</sub></td><td>Cisco Networking Academy · academia UNINTER<br><sub>dic 2023</sub></td><td><sub>constancia en PDF</sub></td></tr>
<tr><td align="center" width="56"><img src="assets/insignias/redes.svg" width="44" height="44" alt=""></td><td><b>CISCO: Redes Empresariales Avanzadas</b><br><sub>certificado · 81 horas</sub></td><td>UNINTER<br><sub>nov 2024</sub></td><td><sub>constancia en PDF</sub></td></tr>
<tr><td align="center" width="56"><img src="assets/insignias/linux.svg" width="44" height="44" alt=""></td><td><b>OpenSUSE Linux OS Fundamentals</b><br><sub>curso en línea</sub></td><td>EDUCBA · Coursera<br><sub>sep 2025</sub></td><td><a href="https://coursera.org/verify/D66JI5C6CMUL"><b>verificar</b></a></td></tr>
<tr><td align="center" width="56"><img src="assets/insignias/ia.svg" width="44" height="44" alt=""></td><td><b>Diplomado en Inteligencia Artificial Generativa y Automatización</b><br><sub>diplomado · 112 horas</sub></td><td>Top Learning Online<br><sub>sep 2025</sub></td><td><sub>constancia en PDF</sub></td></tr>
<tr><td align="center" width="56"><img src="assets/insignias/desarrollo.svg" width="44" height="44" alt=""></td><td><b>Introduction to Git and GitHub</b><br><sub>curso en línea</sub></td><td>Google · Coursera<br><sub>abr 2025</sub></td><td><a href="https://coursera.org/verify/85AUMO3S7G8Y"><b>verificar</b></a></td></tr>
<tr><td align="center" width="56"><img src="assets/insignias/gestion.svg" width="44" height="44" alt=""></td><td><b>Scrum Master Certification: Scrum Methodologies</b><br><sub>curso en línea</sub></td><td>LearnQuest · Coursera<br><sub>jun 2025</sub></td><td><a href="https://coursera.org/verify/L4123WTS5IIU"><b>verificar</b></a></td></tr>
</table>

<details><summary><b>Ver todos mis estudios, cursos y constancias</b> — nombre exacto, emisor, fecha y enlace de verificación (18)</summary>

**Formación académica**

- **Posgrado en Administración de Tecnologías** — Universidad Internacional (UNINTER) · 2025 – 2026 · En línea
- **Ingeniería en Sistemas Computacionales** — Universidad Internacional (UNINTER) · 2020 – 2024 · Cuernavaca, Morelos

**Redes y sistemas**

- **CCNAv7: Redes empresariales, Seguridad y Automatización** — Cisco Networking Academy · academia UNINTER · dic 2023 · certificado de finalización de curso
- **CCNAv7: Introducción a Redes** — Cisco Networking Academy · academia UNINTER · ene 2023 · certificado de finalización de curso
- **CISCO: Redes Empresariales Avanzadas** — UNINTER · nov 2024 · certificado · 81 horas
- **CISCO: Redes Empresariales, Seguridad y Automatización** — UNINTER · oct 2024 · certificado · 81 horas
- **OpenSUSE Linux OS Fundamentals** — EDUCBA · Coursera · sep 2025 · curso en línea · [verificar](https://coursera.org/verify/D66JI5C6CMUL)

**Desarrollo e inteligencia artificial**

- **Diplomado en Inteligencia Artificial Generativa y Automatización** — Top Learning Online · sep 2025 · diplomado · 112 horas
- **Introduction to Git and GitHub** — Google · Coursera · abr 2025 · curso en línea · [verificar](https://coursera.org/verify/85AUMO3S7G8Y)
- **Java (nivel 3)** — TR Network · feb 2026 · constancia
- **Curso de programación en Python** — Asociación de Robótica Aplicada y Ciencias de la Tecnología · ene 2022 · reconocimiento · 16 horas
- **Curso de Robótica Aplicada, nivel avanzado** — Asociación de Robótica Aplicada y Ciencias de la Tecnología · jun – oct 2021 · reconocimiento · 60 horas

**Gestión y metodologías ágiles**

- **Scrum Master Certification: Scrum Methodologies** — LearnQuest · Coursera · jun 2025 · curso en línea · [verificar](https://coursera.org/verify/L4123WTS5IIU)
- **Introduction to Scrum Master Training** — LearnQuest · Coursera · jul 2025 · curso en línea · [verificar](https://coursera.org/verify/J2GU682X9PGQ)

**Otras constancias**

- **Comunicación Digital con Medios Enriquecidos** — UNINTER · oct 2023 · certificado · 54 horas
- **Comunicación Web Interactiva** — UNINTER · nov 2022 · certificado · 54 horas
- **Ofimática** — UNINTER · dic 2021 · certificado · 81 horas
- **3.ª Presentación de Proyectos** — UNINTER · ESCAT · may 2024 · reconocimiento por participación

</details>

<sub>Las constancias de Coursera son cursos en línea sin créditos académicos; cada enlace de verificación viene de su certificado. Los cursos de Cisco Networking Academy son certificados de finalización de curso, no la certificación CCNA.</sub>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/experiencia-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/experiencia-claro.svg"><img src="assets/secciones/experiencia-oscuro.svg" width="396" alt="Experiencia"></picture></h3>

<p align="center"><img src="assets/trayectoria.svg" width="100%" alt="Trayectoria: 2021 SEDAGRO → 2023 – 2024 Junta de Conciliación → 2025 BBVA Technology → 2026 Marelli"></p>

**Técnico de Pruebas** · Marelli  
<sub>2026 · Tepotzotlán, Estado de México</sub>

- Pruebas funcionales a tarjetas electrónicas en varias etapas: manufactura, antes de la entrega al cliente y verificación posterior.
- Desarrollo y administración de bases de datos para el seguimiento de resultados y de materiales reparados.
- Respaldo de la información de las máquinas de prueba.

**Técnico de Soporte e Implementación TI** · BBVA Technology America  
<sub>2025 · Ciudad de México · clientes en Colombia, Venezuela y España</sub>

- Soporte técnico a clientes internacionales en un equipo de dos personas.
- Implementación de autenticación biométrica (Face ID y huella digital) para usuarios bancarios.
- Gestión y actualización de credenciales de usuario en Linux.
- Apoyo en el desarrollo en Java del asistente digital de la aplicación bancaria y en servicios de AWS para soporte de infraestructura.

**Técnico en TI (servicio social)** · Junta de Conciliación y Arbitraje  
<sub>2023 – 2024 · Cuernavaca, Morelos</sub>

- Diagnóstico y solución de problemas de conectividad en más de 50 estaciones de trabajo.
- Configuración y gestión de switches; mantenimiento preventivo y correctivo de equipos.
- Soporte técnico de primer nivel en hardware y software.

**Practicante en TI** · Secretaría de Desarrollo Agropecuario (SEDAGRO)  
<sub>2021 · Cuernavaca, Morelos</sub>

- Diseño e instalación de cableado estructurado hacia switches de red; ponchado de cables.
- Diagnóstico de fallas de conectividad y configuración de impresoras y periféricos.

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/laboratorios-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/laboratorios-claro.svg"><img src="assets/secciones/laboratorios-oscuro.svg" width="632" alt="Laboratorios en desarrollo"></picture></h3>

- **[Cybersecurity Python Lab · siguientes entregas](https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad)** <sub>`pendiente`</sub> — Laboratorio de códigos 2FA (TOTP), analizador de correos con indicadores de phishing, verificador de archivos sospechosos, checklist de seguridad y seis herramientas más.
- **[ALBA · etapa 2](https://github.com/AlfonsoCha1/Herramientas_cyberseguridad)** <sub>`pendiente`</sub> — Diagnóstico de sistemas en modo de solo lectura, flujo de BitLocker y recuperación de memorias USB.

<sub>Mi actividad real es la gráfica de contribuciones que GitHub muestra debajo de este README; las cuadrículas animadas de esta página son decorativas.</sub>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/contacto-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/contacto-claro.svg"><img src="assets/secciones/contacto-oscuro.svg" width="369" alt="Contacto"></picture></h3>

<p align="center">
  <a href="https://www.linkedin.com/in/alfonso-chavarin/"><img src="assets/botones/linkedin.svg" width="200" alt="LinkedIn"></a>
  <a href="mailto:alfonso.chavarin@hotmail.com"><img src="assets/botones/correo.svg" width="200" alt="Correo"></a>
  <a href="https://portafolio-original-tau.vercel.app/"><img src="assets/botones/portafolio.svg" width="200" alt="Portafolio"></a>
  <a href="https://github.com/AlfonsoCha1?tab=repositories"><img src="assets/botones/repositorios.svg" width="200" alt="Repositorios"></a>
</p>

<!-- MANUAL:INICIO -->
<!-- Lo que escribas entre estas dos marcas se conserva cada vez que se regenera el README. -->
<!-- MANUAL:FIN -->

<p align="center"><i>“Technology is not only about building things, but about solving real problems with useful solutions.”</i></p>
