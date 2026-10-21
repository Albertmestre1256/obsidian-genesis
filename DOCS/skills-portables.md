> [!info]- Índice de esta nota (líneas)
> - Líneas 1–6: Este índice
> - Líneas 8–23: Cinco skills opcionales para tu bóveda
> - Líneas 24–38: Usarlas como skills de tu asistente
> - Líneas 39–46: Personalizar y mantener
> - Líneas 47–49: Referencias de compatibilidad

# Cinco skills opcionales para tu bóveda

El kit incluye cinco habilidades editables en `skills/`, escritas en Markdown. Son opcionales: la configuración no las instala y la bóveda funciona sin ellas. Cualquier IA con acceso a archivos puede leer `skills/NOMBRE/SKILL.md` y seguirlo. Copiar instrucciones no concede acceso a notas ni instala Obsidian o un conector.

| Skill | Para qué sirve | Qué decide la persona |
|---|---|---|
| `inicio` | Leer reglas y estado para retomar en un asistente sin las skills del kit | Qué proyecto trabajar; solo lectura |
| `volcar` | Guardar lo valioso de la conversación | Destinos y contenido del plan |
| `vault-reorganizer` | Mover, renombrar o archivar | Objetos y destinos concretos |
| `vault-coherence-auditor` | Encontrar referencias rotas o contradictorias | Qué correcciones aplicar |
| `vault-token-optimizer` | Leer con menos contexto y proponer mejoras | Cambios de estructura o contenido |

Para retomar un proyecto, la entrada recomendada es `empezar`, que ya viene con el kit: `/empezar` en Claude Code y OpenCode, o el pedido «seguí con [proyecto]» en cualquier IA. `inicio` queda como alternativa portable para otros asistentes.

Las skills descubren la raíz y reglas de la bóveda conectada. No traen rutas de una computadora, proyectos del autor ni políticas personales de purga. Se pueden copiar a otra computadora con la bóveda, conservando los archivos ocultos; una conexión MCP o permiso de acceso se configura en el equipo nuevo si hace falta.

## Usarlas como skills de tu asistente

Si querés invocarlas por su nombre, pedile a tu IA que copie cada skill que elijas desde `skills/` a la carpeta local de tu asistente, dentro de la bóveda:

| Asistente | Destino dentro de la bóveda |
|---|---|
| Claude Code | `.claude/skills/NOMBRE/` |
| Codex | `.agents/skills/NOMBRE/` |
| OpenCode | `.opencode/skills/NOMBRE/` |
| Otra IA con acceso a archivos | Lectura directa de `skills/NOMBRE/SKILL.md` |

La IA copia la carpeta completa con sus herramientas de archivos, sin Python ni enlaces hacia otra computadora, y verifica el contenido al terminar. Si el destino ya tiene una carpeta con ese nombre y es distinta, la conserva y te consulta: puede ser tu personalización. No copia a carpetas globales de la cuenta ni para todos los asistentes. OpenCode también descubre `.claude/skills` y `.agents/skills`, así que puede reutilizar una copia presente en lugar de crear otra con el mismo nombre. Si una skill global con el mismo nombre tiene prioridad, la IA indica cuál carga la aplicación y usa la ruta local explícita sin modificar la global.

La recarga depende de la aplicación: si no aparecen, abrí una sesión nueva. Una copia acredita archivos, no una conversación real en cada cliente. Los comandos slash no son universales: también podés pedir «usá volcar para guardar esta conversación».

## Personalizar y mantener

Pedile a tu IA, por ejemplo: «Adaptá la skill volcar de esta bóveda a mi forma de guardar notas». La copia pertenece a esa bóveda: conservá un respaldo o diff, editá esa copia, verificá sus rutas y descripción y registrá qué cambió. La fuente de `skills/` sirve como referencia; no la copies encima de una personalización: al volver a copiar, la IA compara y conserva tu versión para una conciliación explícita.

Las cinco skills son independientes: el resumen de `volcar` no necesita una sexta skill de compactación. La IA adapta rutas, idioma y herramientas a tu entorno sin cambiar por eso las reglas compartidas ni ejecutar limpiezas futuras. No agregues credenciales ni datos privados innecesarios a una skill compartida.

Después de copiar o modificar, seguí [mantenimiento](mantenimiento.md): autoría, fecha con zona, archivos realmente afectados, mapas y comprobaciones. Los `SKILL.md` conservan frontmatter estándar y cuerpo Markdown; el índice de líneas de las fuentes ya está incluido. Conservá `skills/`, las copias y esta guía al retirar material de desarrollo del kit.

## Referencias de compatibilidad

Rutas comprobadas en la documentación oficial al preparar esta integración (20/10/2026): [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://learn.chatgpt.com/docs/build-skills) y [OpenCode](https://opencode.ai/docs/skills/). Otras interfaces, incluidas las aplicaciones web, pueden exigir subir un paquete o conectar archivos: no se afirma instalación automática en esas interfaces.
