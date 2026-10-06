<!--
  ESTE ARCHIVO SE GENERA AUTOMÁTICAMENTE con scripts/generar.py a partir de perfil.toml.
  Para cambiar el contenido, edita perfil.toml (guía: docs/MANTENIMIENTO.md).
-->

<p align="center"><img src="assets/hero.svg" width="100%" alt="Alfonso Chavarín — Ciberseguridad, Sistemas y redes, Administración de tecnología. Retrato holográfico animado de partículas que se transforma en el monograma AC y en un escudo."></p>

Ingeniero en Sistemas Computacionales con posgrado en Administración de Tecnologías. Trabajo en soporte e implementación de TI, redes y bases de datos, y hoy enfoco mis proyectos en la ciberseguridad defensiva con Python.

**Construyendo ahora:** ALBA, un kit local para revisar la seguridad de proyectos, y nuevas herramientas para mi laboratorio de ciberseguridad en Python.

<details><summary><b>English summary</b></summary>

Computer Systems Engineer (UNINTER) with a postgraduate degree in Technology Management. Hands-on experience in IT support and implementation (BBVA Technology, international clients), networking (government agencies) and production test databases (Marelli). I am currently building defensive security tools in Python: ALBA, a local project security reviewer, and a cybersecurity lab focused on log analysis. Spanish (native) · English (B2).

</details>

<p align="center"><img src="assets/senal.svg" width="100%" alt="Cuadrícula decorativa animada (no representa actividad real)"></p>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/proyectos-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/proyectos-claro.svg"><img src="assets/secciones/proyectos-oscuro.svg" width="552" alt="Proyectos destacados"></picture></h3>

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Herramientas_cyberseguridad"><img src="assets/proyectos/alba.svg" width="100%" alt="ALBA — Mi Kit Técnico — Disponible: v0.1.0 · primer módulo operativo. Python (stdlib), Linux, Gitleaks, HTML/CSS/JS"></a>
<p>Aplicación local en español para revisar la seguridad de proyectos web y Node.js y aprender mientras lo haces. Funciona sin internet y solo usa la biblioteca estándar de Python.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Eliges una carpeta (o el proyecto ficticio del laboratorio) y antes de empezar ves el alcance: qué va a leer, siempre en modo de solo lectura.</li><li>Busca secretos expuestos (16 reglas específicas + 1 genérica), configuraciones peligrosas (CORS, TLS, eval/exec, cookies, Docker) y dependencias con avisos conocidos. Si tienes Gitleaks, lo usa como segundo detector.</li><li>Cada hallazgo separa hechos, indicios e hipótesis. Los secretos nunca se muestran completos: prefijo, longitud y huella HMAC.</li><li>Propone correcciones acotadas con vista previa, aprobación ligada al cambio exacto, respaldo, verificación y reversión.</li><li>Exporta informes en HTML, Markdown y JSON.</li></ul>
<p><sub>Probado en Ubuntu 24.04 (base de Linux Mint 22). Windows y macOS: prototipo. El resto del kit está diseñado y marcado como pendiente.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Herramientas_cyberseguridad"><b>Repositorio</b></a></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad"><img src="assets/proyectos/cyber-lab.svg" width="100%" alt="Cybersecurity Python Lab — Laboratorio: 4 de 14 herramientas disponibles. Python, pytest, Análisis de logs, Regex"></a>
<p>Laboratorio de ciberseguridad defensiva en Python: herramientas pequeñas e independientes, cada una con código, datos sintéticos, pruebas automáticas y guía. Son herramientas de aprendizaje, no productos para producción.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>08 · Generador de reportes: convierte eventos JSON, JSON Lines o CSV en reportes Markdown y HTML, y lista las filas que no pudo usar.</li><li>09 · Contador de intentos de login: cuenta accesos exitosos y fallidos por usuario e IP en registros de OpenSSH y otros formatos.</li><li>11 · Buscador en logs: busca palabras, IPs, rangos de red (CIDR) y fechas con líneas de contexto, sin cargar el archivo completo.</li><li>12 · Detector de múltiples accesos: alerta cuando una cuenta o IP acumula demasiados fallos en una ventana de tiempo, con evidencia.</li><li>Un menú (python menu.py) ejecuta las demostraciones y las pruebas de cada herramienta.</li></ul>
<p><sub>Las otras 10 herramientas se publican por entregas.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Tipos-de-Proyectos/tree/main/ciberseguridad"><b>Repositorio</b></a></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://ia-sophya.vercel.app/"><img src="assets/proyectos/sophya.svg" width="100%" alt="SOPHYA — Asistente de IA — Beta: Beta gratuita · requiere cuenta. Python, FastAPI, JavaScript"></a>
<p>Asistente de inteligencia artificial en español, en beta gratuita. Ayuda a investigar, redactar, analizar datos y pensar ideas de negocio.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Chat con memoria dentro de la conversación y entre sesiones; la memoria se puede exportar.</li><li>Voz: dictado y respuestas habladas.</li><li>Investigación web y modo de trabajo autónomo.</li><li>Herramientas de correo y agenda, y búsqueda de empleo.</li></ul>
<p><sub>Código privado: el enlace lleva a la aplicación.</sub></p>
</details>
<p><a href="https://ia-sophya.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
</td>
<td width="50%" valign="top">
<a href="https://english-speaking-coach-nine.vercel.app/"><img src="assets/proyectos/english-coach.svg" width="100%" alt="English Speaking Coach — Demo: Demo en línea · entrevista de trabajo completa. TypeScript, Next.js, Web Speech API, IA generativa"></a>
<p>Practica inglés hablando con un coach de IA: te escucha, te corrige y te hace repetir las palabras difíciles.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Eliges un escenario: entrevista de trabajo, conversación cotidiana, viajes, reuniones, presentaciones o negocios.</li><li>Ajustas el nivel (A2 a C1), el estilo de corrección (Profesor o Conversación fluida) y la duración (Corta o Completa).</li><li>Toda la práctica es por voz, sin escribir; al final recibes tus 3 errores principales con ejercicios.</li><li>Un agente de IA decide cada turno; el código funciona con Groq, OpenAI o Anthropic usando una clave propia.</li></ul>
<p><sub>Código privado: el enlace lleva a la aplicación.</sub></p>
</details>
<p><a href="https://english-speaking-coach-nine.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://smuckys-bychavamon.vercel.app/"><img src="assets/proyectos/smuckys.svg" width="100%" alt="Smucky&#x27;s by Chavamon — Disponible: Tienda en línea. HTML, CSS, JavaScript, Firebase, FastAPI"></a>
<p>Tienda en línea de mi marca de ropa deportiva y casual: playeras, blusas, playeras sin mangas y shorts deportivos.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Catálogo por categorías con carrito de compras y favoritos.</li><li>Cuenta de cliente con pedidos, entregas y devoluciones.</li><li>Pago con tarjeta de crédito o débito y Mercado Pago; pago con Stripe.</li></ul>
<p><sub>Código privado: el enlace lleva a la tienda.</sub></p>
</details>
<p><a href="https://smuckys-bychavamon.vercel.app/"><b>Visitar sitio</b></a> · <sub>código privado</sub></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/AlfonsoCha1/Chavarin_-_Said"><img src="assets/proyectos/lealtad.svg" width="100%" alt="Chavarín &amp; Said — Lealtad — Demo: Demostración funcional · base para pilotos. TypeScript, Node.js, PostgreSQL, Docker"></a>
<p>Plataforma de tarjetas de puntos o sellos para pequeños negocios de comida, tiendas y servicios (nombre provisional). Todavía no está lista para negocios reales.</p>
<details><summary><b>Cómo funciona</b></summary>
<ul><li>Directorio de negocios con categorías y búsqueda.</li><li>Registro de clientes con un QR de mostrador por sucursal; tarjeta web e impresa.</li><li>Paneles para cliente, empleado, dueño y administración; los tickets repetidos se rechazan.</li><li>La demo usa negocios y personas ficticios.</li></ul>
<p><sub>La demo está en un servidor gratuito: puede tardar alrededor de un minuto en despertar.</sub></p>
</details>
<p><a href="https://github.com/AlfonsoCha1/Chavarin_-_Said"><b>Repositorio</b></a> · <a href="https://chavarin-said-lealtad.onrender.com/"><b>Ver demo</b></a></p>
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

<p align="center"><img src="assets/areas.svg" width="100%" alt="Áreas: Ciberseguridad: Defensa, análisis de registros y revisión segura de proyectos; Sistemas y redes: Conectividad, switches, cableado estructurado y Linux; Administración de tecnología: Soporte TI, datos y gestión de proyectos tecnológicos; Desarrollo e IA: Aplicaciones web y asistentes con inteligencia artificial"></p>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/loquese-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/loquese-claro.svg"><img src="assets/secciones/loquese-oscuro.svg" width="364" alt="Lo que sé"></picture></h3>

<p align="center"><img src="assets/loquese/lenguajes.svg" width="100%" alt="Lenguajes y frameworks: Lo que uso para programar mis proyectos"></p>

<p align="center">
<img src="assets/tecnologias/lenguajes-python.svg" width="128" alt="Python">
<img src="assets/tecnologias/lenguajes-javascript.svg" width="128" alt="JavaScript">
<img src="assets/tecnologias/lenguajes-typescript.svg" width="128" alt="TypeScript">
<img src="assets/tecnologias/lenguajes-html5.svg" width="128" alt="HTML5">
<img src="assets/tecnologias/lenguajes-css3.svg" width="128" alt="CSS3">
<img src="assets/tecnologias/lenguajes-java.svg" width="128" alt="Java">
<img src="assets/tecnologias/lenguajes-c.svg" width="128" alt="C#">
<img src="assets/tecnologias/lenguajes-net.svg" width="128" alt=".NET">
<img src="assets/tecnologias/lenguajes-c.svg" width="128" alt="C++">
<img src="assets/tecnologias/lenguajes-php.svg" width="128" alt="PHP">
<img src="assets/tecnologias/lenguajes-node-js.svg" width="128" alt="Node.js">
<img src="assets/tecnologias/lenguajes-fastapi.svg" width="128" alt="FastAPI">
<img src="assets/tecnologias/lenguajes-postgresql.svg" width="128" alt="PostgreSQL">
<img src="assets/tecnologias/lenguajes-firebase.svg" width="128" alt="Firebase">
<img src="assets/tecnologias/lenguajes-pytest.svg" width="128" alt="pytest">
</p>

<p align="center"><img src="assets/loquese/sistemas.svg" width="100%" alt="Sistemas, redes y herramientas: Infraestructura, redes, versiones y despliegue"></p>

<p align="center">
<img src="assets/tecnologias/sistemas-linux.svg" width="128" alt="Linux">
<img src="assets/tecnologias/sistemas-redes.svg" width="128" alt="Redes (switches · TCP/IP)">
<img src="assets/tecnologias/sistemas-cisco-packet-tracer.svg" width="128" alt="Cisco Packet Tracer">
<img src="assets/tecnologias/sistemas-aws.svg" width="128" alt="AWS">
<img src="assets/tecnologias/sistemas-git.svg" width="128" alt="Git">
<img src="assets/tecnologias/sistemas-github.svg" width="128" alt="GitHub">
<img src="assets/tecnologias/sistemas-vs-code.svg" width="128" alt="VS Code">
<img src="assets/tecnologias/sistemas-vercel.svg" width="128" alt="Vercel">
<img src="assets/tecnologias/sistemas-render.svg" width="128" alt="Render">
<img src="assets/tecnologias/sistemas-figma.svg" width="128" alt="Figma">
<img src="assets/tecnologias/sistemas-arduino.svg" width="128" alt="Arduino">
<img src="assets/tecnologias/sistemas-microsoft-office.svg" width="128" alt="Microsoft Office">
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

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/formacion-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/formacion-claro.svg"><img src="assets/secciones/formacion-oscuro.svg" width="587" alt="Formación y constancias"></picture></h3>

<p align="center"><img src="assets/formacion.svg" width="100%" alt="Formación: Ingeniería en Sistemas Computacionales; Posgrado en Administración de Tecnologías; Redes empresariales, seguridad y automatización; IA generativa y automatización"></p>

<details><summary><b>Cursos y constancias</b> — con enlaces de verificación (16)</summary>

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

<sub>Los cursos de Coursera son cursos en línea sin créditos académicos. Los cursos de Cisco Networking Academy son certificados de finalización de curso, no la certificación CCNA.</sub>

</details>

<h3><picture><source media="(prefers-color-scheme: dark)" srcset="assets/secciones/experiencia-oscuro.svg"><source media="(prefers-color-scheme: light)" srcset="assets/secciones/experiencia-claro.svg"><img src="assets/secciones/experiencia-oscuro.svg" width="396" alt="Experiencia"></picture></h3>

<p align="center"><img src="assets/experiencia.svg" width="100%" alt="Experiencia: 2021 Practicante en TI en Secretaría de Desarrollo Agropecuario (SEDAGRO) → 2023 – 2024 Técnico en TI (servicio social) en Junta de Conciliación y Arbitraje → 2025 Técnico de Soporte e Implementación TI en BBVA Technology America → 2026 Técnico de Pruebas en Marelli"></p>

<details><summary><b>Funciones de cada puesto</b></summary>

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
