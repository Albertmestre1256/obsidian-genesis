# Obsidian + IA: kit de arranque con Context Engineering

Guardá el contexto de cada proyecto en una ficha corta y retomá el trabajo con tu IA sin explicar todo de nuevo. Podés usar el kit con Claude, ChatGPT, Gemini o un asistente con acceso a tus archivos.

Para empezar solo necesitás [Obsidian](https://obsidian.md) y la IA que ya usás. Python es opcional para revisar fichas o instalar el kit en una bóveda existente.

## Una bóveda nueva, en tres pasos

1. **Descargá y descomprimí** el ZIP del repositorio (Code → Download ZIP) o el paquete de una release cuando esté publicada.
2. En Obsidian, elegí **Abrir carpeta como bóveda** y seleccioná la carpeta descomprimida que contiene este README. Ya incluye la configuración necesaria.
3. Abrí **[Panel](Panel.md)**. Para probar con una IA, adjuntá las [reglas](00_CORE/atoms/00_vault-rules.md) y la [ficha de ejemplo](00_CORE/cells/ejemplo-context.md) y pegá:

   > Leé primero las reglas y después la ficha adjunta del proyecto aprender-python. Es un ejemplo ficticio. Resumí el objetivo, las acciones pendientes y el próximo paso. No modifiques archivos.

Con **Claude Code**, abrilo en la carpeta de la bóveda y usá `/empezar aprender-python`. La skill encuentra la ficha por su propiedad `proyecto`, aunque el archivo se llame `ejemplo-context.md`.

El objetivo es que el arranque sea breve; el tiempo de instalación todavía debe medirse con usuarios nuevos.

## Si ya tenés una bóveda

El instalador agrega archivos nuevos y conserva los existentes, incluidos los ajustes de `.obsidian`. Si encuentra un archivo del kit con contenido distinto, muestra todos los conflictos y termina antes de copiar.

Con Python 3.8 o superior, desde la carpeta descargada:

```powershell
python instalar.py "C:/ruta/de/tu/boveda"
```

En macOS o Linux usá `python3 instalar.py "/ruta/de/tu/boveda"`. En Windows también podés abrir `instalar.py` con doble clic si Python está asociado a los archivos `.py`; la ventana pide la ruta y espera al terminar.

Para ver qué agregaría sin escribir: `python instalar.py "C:/ruta/de/tu/boveda" --dry-run`.

Sin Python, copiá `00_CORE/`, `PROJECT_TEMPLATE/`, `DOCS/`, `.claude/`, `Panel.md`, `Proyectos.base` y `AI-INSTRUCTIONS.md` a la raíz de tu bóveda, **omitiendo cualquier archivo que ya exista**. No copies `.obsidian/` sobre una bóveda existente. Después revisá [los ajustes opcionales de Obsidian](DOCS/obsidian.md).

## Tu primer proyecto

Con Claude Code, escribí `/nuevo-proyecto Mi proyecto`. Te pide los datos que falten y crea la carpeta y la ficha.

Con ChatGPT, Claude o Gemini en un chat, seguí [Usar con otras IAs](DOCS/usar-con-otras-ias.md): incluye los cinco prompts y explica cómo guardar sus respuestas en Obsidian.

A mano: duplicá `PROJECT_TEMPLATE/`, nombrá la copia y creá una nota en `00_CORE/cells/` cuyo nombre termine en `-context.md`. Insertá `TEMPLATE_cell` con el plugin Plantillas, completá los campos y actualizá el enlace a esa ficha en el índice del proyecto. También podés copiar la plantilla y poner la fecha a mano.

## Uso diario

| Tarea | Claude Code | Cualquier chat con IA |
|---|---|---|
| Retomar | `/empezar nombre-corto` | Adjuntar reglas y ficha, pedir próximos pasos |
| Redactar | `/redactar nombre-corto qué necesitás` | Adjuntar contexto y usar el prompt de redacción |
| Guardar avances | `/cerrar nombre-corto` | Revisar los cambios propuestos y actualizar la ficha |
| Crear proyecto | `/nuevo-proyecto Nombre del proyecto` | Usar el prompt de creación |
| Revisar fichas | `/validar` | Pedir una revisión manual |

`/cerrar` y `/nuevo-proyecto` se invocan manualmente en Claude Code. Las escrituras y permisos dependen de tu asistente y su configuración. El kit pide revisar un plan antes de guardar el cierre o redactar un entregable; no garantiza que el cliente muestre un permiso por cada archivo.

## Qué guarda cada carpeta

| Lugar | Para qué sirve |
|---|---|
| `00_CORE/atoms/` | Reglas compartidas por todos los proyectos |
| `00_CORE/cells/` | Una ficha o **célula** por proyecto: hechos, decisiones y acciones |
| `00_CORE/cognitive-tools/` | Guías para textos técnicos, narrativos, persuasivos y operativos |
| `PROJECT_TEMPLATE/` | Modelo con fuentes originales, síntesis, entregables y archivo |
| `.claude/skills/` | Instrucciones que Claude Code carga cuando las necesitás |
| `.obsidian/` | Ajustes para la bóveda nueva: Plantillas, Bases y búsqueda |
| `DOCS/` | Guía rápida, solución de problemas y uso con otras IAs |

Una **bóveda** es una carpeta que Obsidian abre como colección de notas. Una **célula** es una nota corta de proyecto con propiedades arriba. Los contextos **A/B/C/D** indican el tipo de comunicación: técnica, narrativa, persuasiva u operativa.

Las carpetas con punto pueden estar ocultas en macOS/Linux. En Finder se muestran con `Cmd + Shift + .`. En Windows, el punto por sí solo no las oculta; si tienen el atributo oculto, activá Ver → Mostrar → Elementos ocultos. Para abrir el ZIP como bóveda no necesitás manipularlas.

## Revisar el kit

```sh
python 00_CORE/schemas/validate.py
```

El revisor usa solo Python estándar. Comprueba formato y campos, **no la veracidad de las fuentes**. Los datos de la ficha de ejemplo son ficticios.

Para contribuir: [CONTRIBUTING](CONTRIBUTING.md). Para problemas de uso: [TROUBLESHOOTING](DOCS/TROUBLESHOOTING.md).

## Privacidad

El kit guarda archivos locales y no instala servicios de sincronización. Cuando adjuntás notas a una IA o le das acceso a la carpeta, ese servicio puede procesarlas según su configuración. Compartí solo el contexto que necesite la tarea.

## English

A starter Obsidian vault for working with AI assistants. Unzip it, open the folder as a vault, then open **Panel.md**. Keep a short context note for each project and share only the relevant rules and notes with your assistant. Claude Code skills and copy-and-paste prompts for other assistants are included. Documentation and templates are currently in Spanish. The optional installer adds missing files to an existing vault and stops on conflicts without overwriting notes or Obsidian settings.

## Licencia y créditos

[MIT](LICENSE). Trabajo derivado e independiente del repositorio [Context Engineering](https://github.com/davidkimai/Context-Engineering) de **davidkimai** (© 2025 davidkimai). El término context engineering fue popularizado por Andrej Karpathy. Este kit no está afiliado ni respaldado por ellos.
