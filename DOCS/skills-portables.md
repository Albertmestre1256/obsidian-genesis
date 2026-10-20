> [!info]- Índice de esta nota (líneas)
> - Líneas 1–6: Este índice
> - Líneas 8–21: Cinco skills para tu bóveda
> - Líneas 22–47: Instalar durante la configuración
> - Líneas 48–55: Personalizar y mantener
> - Líneas 56–58: Referencias de compatibilidad

# Cinco skills para tu bóveda

El kit incluye cinco habilidades editables en `skills/`. La IA las instala junto con la configuración de una bóveda nueva, en la carpeta local del asistente utilizado. También puede leer el archivo directamente si su aplicación no carga skills. Instalar instrucciones no concede acceso a notas ni instala Obsidian o un conector.

| Skill | Para qué sirve | Qué decide la persona |
|---|---|---|
| `inicio` | Leer reglas y estado para retomar | Qué proyecto trabajar; solo lectura |
| `volcar` | Guardar lo valioso de la conversación | Destinos y contenido del plan |
| `vault-reorganizer` | Mover, renombrar o archivar | Objetos y destinos concretos |
| `vault-coherence-auditor` | Encontrar referencias rotas o contradictorias | Qué correcciones aplicar |
| `vault-token-optimizer` | Leer con menos contexto y proponer mejoras | Cambios de estructura o contenido |

Las skills descubren la raíz y reglas de la bóveda conectada. No traen rutas de una computadora, proyectos del autor ni políticas personales de purga. Se pueden copiar a otra computadora con la bóveda, conservando los archivos ocultos; una conexión MCP o permiso de acceso se configura en el equipo nuevo si hace falta.

## Instalar durante la configuración

Esta tarea la hace la IA, dentro del alcance de configuración acordado. Usá el asistente actual si se conoce; preguntá cuál solo si eso cambia el destino y no está claro. Prepará primero el kit completo en la carpeta nueva, como indica el protocolo de configuración.

| Asistente | Destino dentro de la bóveda |
|---|---|
| Claude Code | `.claude/skills/NOMBRE/` |
| Codex | `.agents/skills/NOMBRE/` |
| OpenCode | `.opencode/skills/NOMBRE/` |
| Otra IA con acceso a archivos | Lectura directa de `skills/NOMBRE/SKILL.md`; usar su instalación nativa solo tras comprobarla |

Con Python, desde la raíz del kit copiado (ejemplo: Claude Code):

```sh
python instalar_skills.py "." --asistente claude --dry-run
python instalar_skills.py "." --asistente claude --yes
```

`destino` puede ser otra raíz explícita; `--asistente` acepta `claude`, `codex` u `opencode`. La consulta es el modo predeterminado. Se copian las cinco carpetas completas, incluidos recursos futuros; las copias idénticas se conservan y un archivo diferente impide todo el lote antes de copiar. No hay modo de forzar reemplazos. Ante un fallo de escritura concurrente, puede quedar una operación parcial: releé lo creado antes de reintentar y completá el registro. El script no configura la bóveda ni actualiza mapas o registros por sí solo.

Sin Python, copiá con herramientas de archivos cada carpeta desde `skills/` al destino local de la tabla: compará primero todo el lote, conservá archivos distintos y verificá el contenido al terminar. No uses enlaces hacia la computadora de origen. Si el usuario omite la instalación, conservá las fuentes y dejá disponible la lectura directa.

No copies a carpetas globales de la cuenta ni instales para todos los asistentes por defecto. Si el usuario cambia de asistente, acordá ese destino y comprobá duplicados: OpenCode también descubre `.claude/skills` y `.agents/skills`, por lo que puede reutilizar una instalación ya presente en lugar de crear otra con el mismo nombre. Si una skill global con el mismo nombre tiene prioridad, indicá cuál está cargando la aplicación y usá la ruta local explícita sin modificar la global.

Verificá los cinco `SKILL.md`, sus nombres y su igualdad con la fuente recién instalada. Esa comprobación acredita archivos, no una conversación real en cada cliente. La recarga depende de la aplicación; si no aparecen, consultá su mecanismo de recarga o abrí una sesión nueva. Los comandos slash no son universales: también podés pedir «usá inicio para retomar mi proyecto».

## Personalizar y mantener

Pedile a tu IA, por ejemplo: «Adaptá la skill volcar de esta bóveda a mi forma de guardar notas». La copia instalada pertenece a esa bóveda: conservá un respaldo o diff, editá esa copia, verificá sus rutas y descripción y registrá qué cambió. La fuente de `skills/` sirve como referencia; no sincronices encima de una personalización. Reinstalar detecta la diferencia y la conserva para una conciliación explícita.

Las cinco skills son independientes: el resumen de `volcar` no necesita una sexta skill de compactación. La IA adapta rutas, idioma y herramientas a tu entorno sin cambiar por eso las reglas compartidas ni ejecutar limpiezas futuras. No agregues credenciales ni datos privados innecesarios a una skill compartida.

Después de instalar o modificar, seguí [mantenimiento](mantenimiento.md): autoría, fecha con zona, archivos realmente afectados, mapas y comprobaciones. Los `SKILL.md` conservan frontmatter estándar y cuerpo Markdown; el índice de líneas de las fuentes ya está incluido. Las integraciones instaladas conservan su formato. Conservá `skills/`, las copias instaladas, esta guía y `instalar_skills.py` al retirar material de desarrollo del kit.

## Referencias de compatibilidad

Rutas comprobadas en la documentación oficial al preparar esta integración (20/10/2026): [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://learn.chatgpt.com/docs/build-skills) y [OpenCode](https://opencode.ai/docs/skills/). Otras interfaces, incluidas las aplicaciones web, pueden exigir subir un paquete o conectar archivos: no se afirma instalación automática en esas interfaces.
