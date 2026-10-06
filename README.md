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

<p align="center"><img src="assets/tarjetas/area-ciberseguridad.svg" width="100%" alt="Ciberseguridad: Herramientas defensivas en Python: análisis de logs, detección de accesos repetidos y búsqueda de secretos expuestos (ALBA y Cybersecurity Python Lab). Seguridad de red vista en CCNAv7: mitigación de amenazas, listas de control de acceso (ACL) y acceso administrativo seguro. Aprendiendo: blue team y análisis de eventos de seguridad."></p>
<p align="center"><img src="assets/tarjetas/area-sistemas-y-redes.svg" width="100%" alt="Sistemas y redes: Diagnóstico de conectividad en más de 50 estaciones de trabajo y configuración de switches (Junta de Conciliación y Arbitraje). Diseño e instalación de cableado estructurado, ponchado y configuración de periféricos (SEDAGRO). Gestión de usuarios y credenciales en Linux (BBVA Technology)."></p>
<p align="center"><img src="assets/tarjetas/area-administracion-de-tecnologia.svg" width="100%" alt="Administración de tecnología: Posgrado en Administración de Tecnologías (UNINTER). Soporte técnico a clientes internacionales e implementación de autenticación biométrica (BBVA Technology). Bases de datos para el seguimiento de resultados de pruebas y respaldos de producción (Marelli)."></p>
<p align="center"><img src="assets/tarjetas/area-desarrollo-e-ia.svg" width="100%" alt="Desarrollo e IA: Aplicaciones con IA: SOPHYA (asistente en beta) y English Speaking Coach (tutor de inglés por voz, demo en línea). Desarrollo web: tienda en línea Smucky&#x27;s y plataforma de lealtad Chavarín &amp; Said (demo funcional). Diplomado en Inteligencia Artificial Generativa y Automatización (Top Learning)."></p>

<details><summary><b>Ver áreas como texto</b></summary>

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

</details>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/loquese-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/loquese-claro.svg"><img src="assets/secciones/loquese-oscuro.svg" width="364" alt="Lo que sé"></picture></h3>

<p align="center"><img src="assets/loquese/experiencia.svg" width="100%" alt="Experiencia laboral: Lo que he usado en mis empleos: BBVA Technology, Marelli y dependencias de gobierno"></p>

<p align="center">
<img src="assets/tecnologias/experiencia-soporte-tecnico.svg" width="128" alt="Soporte técnico (primer nivel e internacional)">
<img src="assets/tecnologias/experiencia-linux.svg" width="128" alt="Linux (usuarios y credenciales)">
<img src="assets/tecnologias/experiencia-switches-y-redes.svg" width="128" alt="Switches y redes (configuración)">
<img src="assets/tecnologias/experiencia-cableado-estructurado.svg" width="128" alt="Cableado estructurado">
<img src="assets/tecnologias/experiencia-tcp-ip.svg" width="128" alt="TCP/IP">
<img src="assets/tecnologias/experiencia-autenticacion-biometrica.svg" width="128" alt="Autenticación biométrica (Face ID y huella)">
<img src="assets/tecnologias/experiencia-bases-de-datos.svg" width="128" alt="Bases de datos (seguimiento de pruebas)">
<img src="assets/tecnologias/experiencia-respaldos.svg" width="128" alt="Respaldos (datos de producción)">
<img src="assets/tecnologias/experiencia-java.svg" width="128" alt="Java (asistente digital)">
<img src="assets/tecnologias/experiencia-aws.svg" width="128" alt="AWS (soporte de infraestructura)">
</p>

<p align="center"><img src="assets/loquese/proyectos.svg" width="100%" alt="Tecnologías en mis proyectos: Lenguajes, frameworks y bases de datos que uso en mis proyectos y estudios"></p>

<p align="center">
<img src="assets/tecnologias/proyectos-html5.svg" width="128" alt="HTML5">
<img src="assets/tecnologias/proyectos-css3.svg" width="128" alt="CSS3">
<img src="assets/tecnologias/proyectos-javascript.svg" width="128" alt="JavaScript">
<img src="assets/tecnologias/proyectos-typescript.svg" width="128" alt="TypeScript">
<img src="assets/tecnologias/proyectos-python.svg" width="128" alt="Python">
<img src="assets/tecnologias/proyectos-pytest.svg" width="128" alt="pytest (pruebas automáticas)">
<img src="assets/tecnologias/proyectos-node-js.svg" width="128" alt="Node.js">
<img src="assets/tecnologias/proyectos-fastapi.svg" width="128" alt="FastAPI">
<img src="assets/tecnologias/proyectos-postgresql.svg" width="128" alt="PostgreSQL">
<img src="assets/tecnologias/proyectos-firebase.svg" width="128" alt="Firebase">
<img src="assets/tecnologias/proyectos-java.svg" width="128" alt="Java (ejercicios)">
<img src="assets/tecnologias/proyectos-c.svg" width="128" alt="C# (escuela)">
<img src="assets/tecnologias/proyectos-net.svg" width="128" alt=".NET (ASP.NET · escuela)">
<img src="assets/tecnologias/proyectos-c.svg" width="128" alt="C++">
<img src="assets/tecnologias/proyectos-php.svg" width="128" alt="PHP">
</p>

<p align="center"><img src="assets/loquese/herramientas.svg" width="100%" alt="Herramientas: Para programar, versionar, diseñar, simular redes y desplegar"></p>

<p align="center">
<img src="assets/tecnologias/herramientas-git.svg" width="128" alt="Git">
<img src="assets/tecnologias/herramientas-github.svg" width="128" alt="GitHub">
<img src="assets/tecnologias/herramientas-vs-code.svg" width="128" alt="VS Code">
<img src="assets/tecnologias/herramientas-figma.svg" width="128" alt="Figma">
<img src="assets/tecnologias/herramientas-arduino.svg" width="128" alt="Arduino">
<img src="assets/tecnologias/herramientas-microsoft-office.svg" width="128" alt="Microsoft Office">
<img src="assets/tecnologias/herramientas-cisco-packet-tracer.svg" width="128" alt="Cisco Packet Tracer (simulación de redes)">
<img src="assets/tecnologias/herramientas-vercel.svg" width="128" alt="Vercel">
<img src="assets/tecnologias/herramientas-render.svg" width="128" alt="Render (despliegue)">
<img src="assets/tecnologias/herramientas-scripts-bat.svg" width="128" alt="Scripts .bat (automatización en Windows)">
</p>

<p align="center"><img src="assets/loquese/aprendiendo.svg" width="100%" alt="Actualmente aprendiendo: Lo que estoy estudiando ahora"></p>

<p align="center">
<img src="assets/tecnologias/aprendiendo-react.svg" width="128" alt="React">
<img src="assets/tecnologias/aprendiendo-next-js.svg" width="128" alt="Next.js">
<img src="assets/tecnologias/aprendiendo-tailwind-css.svg" width="128" alt="Tailwind CSS">
<img src="assets/tecnologias/aprendiendo-docker.svg" width="128" alt="Docker">
<img src="assets/tecnologias/aprendiendo-azure.svg" width="128" alt="Azure">
<img src="assets/tecnologias/aprendiendo-blue-team.svg" width="128" alt="Blue team (eventos de seguridad)">
</p>

<details><summary><b>Ver «Lo que sé» como texto</b></summary>

- **Experiencia laboral:** Soporte técnico (primer nivel e internacional), Linux (usuarios y credenciales), Switches y redes (configuración), Cableado estructurado, TCP/IP, Autenticación biométrica (Face ID y huella), Bases de datos (seguimiento de pruebas), Respaldos (datos de producción), Java (asistente digital), AWS (soporte de infraestructura)
- **Tecnologías en mis proyectos:** HTML5, CSS3, JavaScript, TypeScript, Python, pytest (pruebas automáticas), Node.js, FastAPI, PostgreSQL, Firebase, Java (ejercicios), C# (escuela), .NET (ASP.NET · escuela), C++, PHP
- **Herramientas:** Git, GitHub, VS Code, Figma, Arduino, Microsoft Office, Cisco Packet Tracer (simulación de redes), Vercel, Render (despliegue), Scripts .bat (automatización en Windows)
- **Actualmente aprendiendo:** React, Next.js, Tailwind CSS, Docker, Azure, Blue team (eventos de seguridad)

</details>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/formacion-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/formacion-claro.svg"><img src="assets/secciones/formacion-oscuro.svg" width="587" alt="Formación y constancias"></picture></h3>

<p align="center"><img src="assets/formacion.svg" width="100%" alt="Formación: Ingeniería en Sistemas Computacionales; Posgrado en Administración de Tecnologías; Redes empresariales, seguridad y automatización; IA generativa y automatización"></p>

<p align="center"><img src="assets/tarjetas/constancia-ccnav7-redes-empresariales-seguridad-y-automatizacion.svg" width="49%" alt="CCNAv7: Redes empresariales, Seguridad y Automatización — Cisco Networking Academy · academia UNINTER, dic 2023"> <img src="assets/tarjetas/constancia-cisco-redes-empresariales-avanzadas.svg" width="49%" alt="CISCO: Redes Empresariales Avanzadas — UNINTER, nov 2024"></p>
<p align="center"><a href="https://coursera.org/verify/D66JI5C6CMUL"><img src="assets/tarjetas/constancia-opensuse-linux-os-fundamentals.svg" width="49%" alt="OpenSUSE Linux OS Fundamentals — EDUCBA · Coursera, sep 2025"></a> <img src="assets/tarjetas/constancia-diplomado-en-inteligencia-artificial-generativa-y-automatizacion.svg" width="49%" alt="Diplomado en Inteligencia Artificial Generativa y Automatización — Top Learning Online, sep 2025"></p>
<p align="center"><a href="https://coursera.org/verify/85AUMO3S7G8Y"><img src="assets/tarjetas/constancia-introduction-to-git-and-github.svg" width="49%" alt="Introduction to Git and GitHub — Google · Coursera, abr 2025"></a> <a href="https://coursera.org/verify/L4123WTS5IIU"><img src="assets/tarjetas/constancia-scrum-master-certification-scrum-methodologies.svg" width="49%" alt="Scrum Master Certification: Scrum Methodologies — LearnQuest · Coursera, jun 2025"></a></p>

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

<p align="center"><img src="assets/tarjetas/exp-marelli.svg" width="100%" alt="Técnico de Pruebas en Marelli (2026, Tepotzotlán, Estado de México): Pruebas funcionales a tarjetas electrónicas en varias etapas: manufactura, antes de la entrega al cliente y verificación posterior. Desarrollo y administración de bases de datos para el seguimiento de resultados y de materiales reparados. Respaldo de la información de las máquinas de prueba."></p>
<p align="center"><img src="assets/tarjetas/exp-bbva-technology.svg" width="100%" alt="Técnico de Soporte e Implementación TI en BBVA Technology America (2025, Ciudad de México · clientes en Colombia, Venezuela y España): Soporte técnico a clientes internacionales en un equipo de dos personas. Implementación de autenticación biométrica (Face ID y huella digital) para usuarios bancarios. Gestión y actualización de credenciales de usuario en Linux. Apoyo en el desarrollo en Java del asistente digital de la aplicación bancaria y en servicios de AWS para soporte de infraestructura."></p>
<p align="center"><img src="assets/tarjetas/exp-junta-de-conciliacion.svg" width="100%" alt="Técnico en TI (servicio social) en Junta de Conciliación y Arbitraje (2023 – 2024, Cuernavaca, Morelos): Diagnóstico y solución de problemas de conectividad en más de 50 estaciones de trabajo. Configuración y gestión de switches; mantenimiento preventivo y correctivo de equipos. Soporte técnico de primer nivel en hardware y software."></p>
<p align="center"><img src="assets/tarjetas/exp-sedagro.svg" width="100%" alt="Practicante en TI en Secretaría de Desarrollo Agropecuario (SEDAGRO) (2021, Cuernavaca, Morelos): Diseño e instalación de cableado estructurado hacia switches de red; ponchado de cables. Diagnóstico de fallas de conectividad y configuración de impresoras y periféricos."></p>

<details><summary><b>Ver experiencia como texto</b></summary>

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

</details>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/laboratorios-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/laboratorios-claro.svg"><img src="assets/secciones/laboratorios-oscuro.svg" width="632" alt="Laboratorios en desarrollo"></picture></h3>

<p align="center"><a href="https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad"><img src="assets/tarjetas/lab-cybersecurity-python-lab-siguientes-entregas.svg" width="100%" alt="Cybersecurity Python Lab · siguientes entregas (pendiente): Laboratorio de códigos 2FA (TOTP), analizador de correos con indicadores de phishing, verificador de archivos sospechosos, checklist de seguridad y seis herramientas más."></a></p>
<p align="center"><a href="https://github.com/AlfonsoCha1/Herramientas_cyberseguridad"><img src="assets/tarjetas/lab-alba-etapa-2.svg" width="100%" alt="ALBA · etapa 2 (pendiente): Diagnóstico de sistemas en modo de solo lectura, flujo de BitLocker y recuperación de memorias USB."></a></p>

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
