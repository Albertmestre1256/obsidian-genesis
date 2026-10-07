# Solución de problemas

## No veo las carpetas `.claude` ni `.obsidian`
→ En Mac, usá `Cmd + Shift + .` en Finder. En Windows, el punto no las oculta por sí solo; si tienen el atributo oculto, activá Ver → Mostrar → Elementos ocultos. Para una bóveda nueva alcanza con abrir la carpeta completa.

## "python no se reconoce como un comando" (o "command not found: python")
→ Python no está instalado o no está en el PATH. Probá con `python3` o, en Windows, con `py`. Si ninguno funciona, instalá Python desde python.org (en Windows, marcá "Add Python to PATH" durante la instalación). Python hace falta para el validador automático y `instalar.py`. Podés usar revisión manual y copiar solo archivos ausentes siguiendo la [instalación manual](instalacion-manual.md).

---

## Mensajes del revisor de células (`/validar`)

### "Todavía no hay células para revisar"
→ En `00_CORE/cells/`, duplicá `TEMPLATE_cell.md` y renombrala `<tu-proyecto>-context.md`. El nombre tiene que terminar en `-context.md`.

### "No encuentro las propiedades"
→ La célula tiene que empezar con una línea `---`, después las propiedades, y otra línea `---`. Copiá ese comienzo de `TEMPLATE_cell.md`. En Obsidian, las propiedades se ven como un recuadro arriba de la nota.

### "La línea N de las propiedades no tiene el formato 'nombre: valor'"
→ Cada propiedad ocupa una línea con el formato `nombre: valor` (el nombre, dos puntos, un espacio y el valor). Lo más fácil es editarlas desde el recuadro de propiedades de Obsidian, no en el texto.

### Comillas, dos puntos o propiedades vacías
→ Si un texto contiene dos puntos seguidos de un espacio, encerralo completo entre comillas: `descripcion: "Meta: automatizar planillas"`. Cerrá siempre las comillas. `proyecto` y `descripcion` necesitan texto: `null` y `[]` no son nombres ni descripciones.

El revisor admite propiedades en una línea y listas simples. No es un lector de todo YAML: si informa una estructura no admitida, escribí ese valor como texto en una línea. Evitá repetir la misma propiedad.

### "Falta la propiedad 'X'" o "Falta la sección '## X'"
→ Copiala desde `TEMPLATE_cell.md` a tu célula y completala. Las secciones obligatorias son `## Hechos clave` y `## Próximas acciones`.

### "'contexto' vale '...'"
→ Poné una sola letra: A (técnico), B (narrativo), C (persuasivo) o D (operativo).

### "'actualizado' está vacío" o "tiene que ser una fecha"
→ Poné la fecha de la última actualización con el formato AAAA-MM-DD, por ejemplo `2026-01-31`. En el recuadro de propiedades de Obsidian podés elegirla en un calendario.

### "La acción '...' tiene que empezar con '- [ ] '"
→ Cada acción es una tarea: `- [ ] algo pendiente` o `- [x] algo hecho`. Si está en curso, agregá `(en curso)` al final.

### aviso: "El hecho '...' no tiene fuente"
→ No es un error. Agregá al final del hecho de dónde sale el dato, por ejemplo `(fuente: contrato firmado, 01_FUENTES/contrato.pdf)`. Mientras tanto, tratalo como algo no comprobado.

### aviso: "La decisión '...' no empieza con una fecha"
→ Formato: `- 2026-01-31: qué se decidió — porque razón`.

### aviso: "Quedan textos [completar: ...] sin reemplazar"
→ Reemplazá esos textos por tus datos reales.

### aviso: "La célula ocupa ~N tokens"
→ Está demasiado larga para darle a la IA. Resumí, o mové lo viejo a la carpeta `_archivo` del proyecto.

---

## Comandos e IA

### Claude Code no reconoce `/empezar` (u otro comando)
→ Abrí Claude Code en la raíz de la bóveda. Cada comando está en `.claude/skills/nombre/SKILL.md`. Reiniciá esa sesión si acabás de agregar las skills. Si una instalación previa tiene comandos del mismo nombre, revisá esas copias antes de migrar; el instalador no borra archivos antiguos.

### Claude me pide permiso para modificar archivos
→ Revisá lo que propone. Los permisos efectivos dependen de tu configuración de Claude Code. La skill validar declara permiso solo para el comando del validador durante su uso; el kit no concede permisos generales de escritura.

### Uso otra IA, no Claude Code
→ Usá los prompts sin variables de [Usar con otras IAs](usar-con-otras-ias.md). Adjuntá reglas y ficha. Si el chat no puede editar tu carpeta, copiá vos el resultado a Obsidian.


## El instalador informa conflictos

No copió nada. Hay archivos con el mismo nombre y distinto contenido. Comparalos antes de decidir una actualización. Conservá tu versión si tiene notas o reglas propias; repetir el instalador no la reemplaza. `--dry-run` permite ver el plan sin escribir.

## El instalador agregó archivos pero la revisión dio errores

Los archivos nuevos están copiados y las notas previas se conservaron. Revisá las células mencionadas por el validador. Si hubo un error de permisos o de disco durante la copia, el registro muestra hasta dónde llegó. El instalador intenta retirar únicamente el archivo incompleto que acababa de crear; si no puede, lo informa. Un reintento omite archivos ya idénticos.

## No aparece el panel o la fecha automática

Seguí [Configurar Obsidian](obsidian.md). Bases requiere Obsidian 1.9.10 o posterior. En una bóveda existente el instalador no cambia los plugins habilitados. Al copiar una plantilla a mano, reemplazá el marcador de fecha por una fecha real.
