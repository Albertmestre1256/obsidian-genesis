> [!info]- Índice de esta nota (líneas)
> - Líneas 1–42: Este índice
> - Líneas 44–45: Cambios
> - Líneas 46–49: 21/10/2026 — entrega de una copia como ZIP
> - Líneas 50–53: 21/10/2026 — README más claro con guías enlazadas
> - Líneas 54–57: 21/10/2026 — material heredado fuera de Genesis
> - Líneas 58–61: 21/10/2026 — skills opcionales en Markdown, sin instalador
> - Líneas 62–65: 21/10/2026 — creador: porcentajes, identificador y plantilla
> - Líneas 66–69: 21/10/2026 — bloqueos huérfanos con guía de recuperación
> - Líneas 70–73: 21/10/2026 — ayuda de IA al final de los README
> - Líneas 74–77: 20/10/2026 — registro inviolable y enlaces solo dentro de la bóveda
> - Líneas 78–81: 20/10/2026 — robustez de registro, rangos y Panel
> - Líneas 82–85: 20/10/2026 — vista simple con las skills portables
> - Líneas 86–89: 20/10/2026 — cinco skills portables
> - Líneas 90–93: 20/10/2026 — alcance: bóvedas nuevas
> - Líneas 94–97: 20/10/2026 — decisión explícita sobre el retiro al configurar
> - Líneas 98–101: 20/10/2026 — retiro opcional del material del kit
> - Líneas 102–105: 20/10/2026 — estado del proyecto y financiación en GitHub
> - Líneas 106–109: 20/10/2026 — apoyo opcional en Patreon
> - Líneas 110–113: 20/10/2026 — comprobaciones mecánicas con herramientas
> - Líneas 114–117: 20/10/2026 — comentarios YAML en el catálogo
> - Líneas 118–121: 18/10/2026 — vista simple opcional en bóvedas existentes
> - Líneas 122–125: 17/10/2026 — menos repetición al validar el inventario
> - Líneas 126–129: 17/10/2026 — inicio y acceso en una sola guía
> - Líneas 130–133: 17/10/2026 — entradas de IA más concisas
> - Líneas 134–137: 17/10/2026 — vista simple inicial de bóvedas nuevas
> - Líneas 138–141: 17/10/2026 — originales conservados y mantenimiento acotado
> - Líneas 142–145: 16/10/2026 — guía de los documentos en cuatro idiomas
> - Líneas 146–149: 16/10/2026 — simplificación de herramientas Python
> - Líneas 150–153: 16/10/2026 — comunidad y soporte accesibles desde los README
> - Líneas 154–157: 16/10/2026 — abrir la bóveda en Obsidian no desactualiza el índice
> - Líneas 158–161: 16/10/2026 — instalar desde un kit abierto con OpenCode
> - Líneas 162–165: 16/10/2026 — README en cuatro idiomas
> - Líneas 166–169: 16/10/2026 — sin carpetas __pycache__ en la bóveda
> - Líneas 170–173: 15/10/2026 — próximo paso solo en la ficha
> - Líneas 174–177: 15/10/2026 — destino visible al comprobar el cierre
> - Líneas 178–181: 15/10/2026 — conservar cambios posteriores al plan
> - Líneas 182–185: 15/10/2026 — cierre coherente con el proyecto inicial
> - Líneas 186–189: 14/10/2026 — operación visible coherente con el registro
> - Líneas 190–193: 14/10/2026 — inventario de perfil plegable
> - Líneas 194–197: 13/10/2026 — índices de proyectos con nombres propios
> - Líneas 198–219: Sin publicar — candidata a v0.1.0

# Cambios

## 21/10/2026 — entrega de una copia como ZIP

Antes de ofrecer una copia para descargar, la IA pregunta el primer paso (puede quedar pendiente), completa el cierre y solo marca la configuración como lista con «CIERRE VERIFICADO». Arma el ZIP con nombres UTF-8 y lo comprueba descomprimiéndolo y repitiendo el cierre sobre esa copia. La guía de ChatGPT y Solución de problemas explican qué hacer si los nombres aparecen como «├ìndice». Surgió de una prueba con ChatGPT web.

## 21/10/2026 — README más claro con guías enlazadas

Los README en español, inglés, alemán y chino explican primero qué es el kit y suman un glosario corto (bóveda, ficha, Panel, índice general y nodo), qué recibís, el uso diario y una sección «Guías» que enlaza cada documento según lo que necesites. El estado del proyecto queda breve y sin datos de desarrollo. En los cuatro README, una línea en blanco separa la atribución del índice de líneas para que GitHub no los muestre como una sola cita.

## 21/10/2026 — material heredado fuera de Genesis

Genesis crea bóvedas nuevas. Se retiran el instalador para bóvedas existentes (`instalar.py`), su guía de instalación manual y sus pruebas, incluida la de vista simple en una bóveda existente; quedan respaldados para el futuro repositorio de adaptación. Las guías conservan el aviso de alcance: si ya tenés una bóveda, usá el kit en una carpeta nueva.

## 21/10/2026 — skills opcionales en Markdown, sin instalador

Las cinco skills de `skills/` quedan como notas Markdown opcionales: la configuración ya no las instala y la bóveda funciona sin ellas. Al entregar, la IA avisa que existen y las copia a la carpeta del asistente solo si la persona lo pide. Se retiran `instalar_skills.py` y sus pruebas; la guía de skills explica la copia con herramientas de archivos. Para retomar se recomienda `empezar`; `inicio` queda como alternativa portable.

## 21/10/2026 — creador: porcentajes, identificador y plantilla

El creador escapa `%` en el texto que escribe, como el catálogo, para que `%%` no abra un comentario de Obsidian y oculte el resto. Si el nombre no tiene letras latinas ni números, pide acordar un identificador en lugar de informar que falta el id. Al copiar la plantilla omite lo mismo que el catálogo (archivos del sistema como `.DS_Store` o `Thumbs.db`, ocultos y nombres habituales de credenciales) y además temporales (`~$*`, `*.tmp`, `*~`), y reconoce su índice aunque el nombre llegue en otra forma Unicode, como en macOS. La revisión de fichas acepta una fuente con paréntesis, como «(fuente: Plan (versión 2026))», sin avisar que falta.

## 21/10/2026 — bloqueos huérfanos con guía de recuperación

Si una escritura encuentra un bloqueo, el mensaje indica su ruta y antigüedad. Ante uno reciente pide esperar; a partir de los 10 minutos, o si no puede medir la antigüedad, explica cómo recuperarse si quedó de una operación interrumpida y pide que una IA lo confirme con la persona antes de borrarlo. Los bloqueos del kit registran el proceso y la hora de inicio. El kit sigue sin retirarlos por su cuenta; la guía está en «Aparece un bloqueo» de Solución de problemas.

## 21/10/2026 — ayuda de IA al final de los README

En los cuatro README, la sección sobre el desarrollo con ayuda de IA pasa a ser la última, después de «Apoyar el proyecto»; el crédito a davidkimai sigue en la primera línea. No cambia el texto de ninguna sección.

## 20/10/2026 — registro inviolable y enlaces solo dentro de la bóveda

Un resumen del registro ya no puede imitar ni cortar una entrada: el signo de porcentaje se escribe como entidad en el texto y escapado en el comentario de datos. La raíz de la bóveda se reconoce por `INDICE.md` y las reglas: las herramientas rechazan enlaces y junctions desde cada ruta hasta esa raíz, inclusive, pero ya no en las carpetas que la contienen; sin esas marcas revisan la ruta completa como antes. Los originales, históricos y archivos protegidos se miden desde esa raíz, también al revisar notas sueltas desde una subcarpeta. Solo las etiquetas de Windows que redirigen rutas cuentan como enlace: archivos en la nube, deduplicados o comprimidos, no. Vale también para el actualizador, el creador y la instalación de skills; el actualizador no crea ni reescribe índices si se le indica una carpeta protegida. Una prueba de temporales revisa el prefijo real.

## 20/10/2026 — robustez de registro, rangos y Panel

El registro rechaza con un error controlado una acción que no sea texto y no informa un fallo si otro proceso retiró su bloqueo después de guardar. Los rangos cuentan solo los saltos de línea reales, como Obsidian, y una bóveda del kit (con `INDICE.md` y reglas) dentro de una carpeta llamada `_archivo`, `01_FUENTES` u otra protegida ya no queda bloqueada, salvo dentro de otra bóveda del kit; una copia en `.claude/worktrees` cuenta como bóveda propia. Las notas reescritas conservan sus permisos. El acceso del Panel por nombre corto ignora carpetas ocultas, dependencias, enlaces y junctions. El inventario mezclado explica la mezcla, y el instalador heredado ya no remite a una sección retirada.

## 20/10/2026 — vista simple con las skills portables

La vista simple también oculta la carpeta `skills/` e `instalar_skills.py` en el explorador y el gráfico; los archivos siguen disponibles para la IA.

## 20/10/2026 — cinco skills portables

Fuentes editables de inicio, volcar, reorganización, coherencia y eficiencia de contexto en `skills/`, sin rutas ni reglas personales del mantenedor. La configuración incluye su instalación local para el asistente actual; `instalar_skills.py` consulta antes de copiar y conserva personalizaciones. Guía y alternativa sin Python en `DOCS/skills-portables.md`. Catálogo y mantenimiento reconocen las integraciones de Codex sin reescribir su formato.

## 20/10/2026 — alcance: bóvedas nuevas

Las entradas, el protocolo de configuración y las guías ya no ofrecen adaptar bóvedas existentes: Genesis prepara bóvedas nuevas y esa adaptación será un repositorio separado. El instalador y su guía sin Python se marcan como material heredado; ambos y sus pruebas se conservan, pendientes de una decisión de retiro o separación. No cambia código.

## 20/10/2026 — decisión explícita sobre el retiro al configurar

El cierre de configuración exige revisar el material sobrante y presentar cada archivo propuesto para eliminar, su función, motivo, respaldo y lo que se conserva. La persona autoriza la lista con la orden explícita de retiro o indica exclusiones, conservación o postergación; sin respuesta queda pendiente y no se borra. Este paso sustituye la mención opcional anterior, sin añadir scripts ni eliminar archivos del kit.

## 20/10/2026 — retiro opcional del material del kit

`DOCS/obsidian.md` describe cómo la IA puede retirar, a pedido, material del kit que ya no se usa en una bóveda lista: lista exacta de archivos autorizada, respaldo fuera de la bóveda, retiro archivo por archivo con nueva comprobación justo antes, referencias comprobadas y registro. Sin ese pedido se conserva todo. `configurar-vault.md` lo ofrece una vez al entregar y `AI-INSTRUCTIONS.md` lo enruta.

## 20/10/2026 — estado del proyecto y financiación en GitHub

Los README citan el código publicado en main y su matriz remota en lugar de una versión anterior de Pruebas. `.github/FUNDING.yml` usa el nombre de la página de Patreon y el índice general lo cataloga.

## 20/10/2026 — apoyo opcional en Patreon

Los cuatro README terminan con una sección para apoyar el proyecto en Patreon y ya no presentan el patrocinio como pendiente. Los aportes son opcionales y el kit sigue siendo público.

## 20/10/2026 — comprobaciones mecánicas con herramientas

La entrada para asistentes indica decidir rangos, fichas, mapas y hashes con la salida de las herramientas del kit, consultar primero sin escribir e informar solo estado, archivos y errores. Sin Python se conserva la comprobación por lectura.

## 20/10/2026 — comentarios YAML en el catálogo

El indexador reconoce valores entre comillas con comentarios al final, igual que el validador. Las fichas y los nodos conservan su identidad en el mapa; el texto con # y los apóstrofos entre comillas se conserva.

## 18/10/2026 — vista simple opcional en bóvedas existentes

El instalador ofrece --vista-simple con simulación y confirmación. Conserva notas, estilos y preferencias, informa el filtro pendiente si hay búsqueda propia y respalda solo los ajustes modificados sin reemplazar respaldos anteriores. Repetir sin cambios no escribe; la guía explica cómo revertir según los archivos creados y respaldados.

## 17/10/2026 — menos repetición al validar el inventario

El validador devuelve directamente los errores de estructura y usa la lista de filas para detectar un inventario sin datos, sin una bandera paralela. Conserva los mensajes y los controles de formato, estados, alcances y duplicados; no añade funciones, dependencias ni archivos.

## 17/10/2026 — inicio y acceso en una sola guía

QUICKSTART reúne el pedido inicial, el acceso local o por copia, la integración de notas existentes y la reanudación. Se retira empezar-con-ia.md y se actualizan sus enlaces en Panel, README y ayudas; las guías específicas de cada cliente permanecen disponibles.

## 17/10/2026 — entradas de IA más concisas

Las entradas remiten a los recorridos existentes sin repetir sus procedimientos. Se conservan el índice completo de inicio, las reglas, la configuración parcial, el inventario y el mantenimiento identificado. La documentación específica se consulta según el pedido; no se añaden archivos al kit ni se cambia el código de las herramientas.

## 17/10/2026 — vista simple inicial de bóvedas nuevas

La carpeta nueva lleva activado un fragmento CSS para despejar el explorador y un filtro del gráfico que prioriza proyectos, fichas y notas frente al soporte técnico. Los archivos siguen accesibles y no cambian sus rutas. La IA conserva los ajustes preparados en la entrega, sin pedir pasos técnicos al principiante. Se reutiliza la vista confirmada por Albert en una copia local; no se acredita una revisión visual formal de este candidato. El instalador de bóvedas existentes conserva sus preferencias y no aplica todavía esta vista.

## 17/10/2026 — originales conservados y mantenimiento acotado

La guía de personalización explicita conservar el documento original antes de resumirlo y enlazarlo desde el inventario y el contexto; mantiene su origen y carácter ficticio cuando corresponda. El cierre recomienda índices de líneas solo sobre notas afectadas, sin imponer un barrido de la bóveda. Las exportaciones de conversaciones conservan su formato y requieren un destino acordado; si un original fuera de las carpetas protegidas impide el cierre, se informa sin reescribirlo. Es una aclaración de las instrucciones: no cambia el validador, no migra documentos existentes ni acredita una nueva prueba conversacional.

## 16/10/2026 — guía de los documentos en cuatro idiomas

DOCS/README.md y sus versiones en inglés, alemán y chino explican la función de los documentos, integraciones, ajustes, scripts y pruebas. Incluyen un índice de secciones y enlaces a los cuatro README principales y entre sus idiomas. Cada README principal enlaza su guía. Los archivos creados durante el uso se distinguen de los distribuidos; no se duplican las instrucciones comunes ni se cambian las reglas de inicio. Al instalar en otra bóveda, las cuatro guías del repositorio permanecen en el kit fuente para evitar enlaces a README y pruebas ausentes; la copia manual sigue el mismo criterio. La ayuda de uso remite a un inicio rápido disponible también en la bóveda instalada, sin depender del README del repositorio. Los cuatro README distinguen los resultados focales recientes de una suite completa que no se volvió a ejecutar sobre esta versión. La declaración final reconoce a OpenCode, Claude y Codex (OpenAI) por su aporte sustancial al código, sin alterar los créditos originales. Las rutas de archivos futuros se muestran como plantillas con identificador reemplazable, sin confundirlas con archivos distribuidos.

## 16/10/2026 — simplificación de herramientas Python

El lector de filas del inventario mantiene barras escapadas y columnas vacías con menos código. El actualizador reutiliza la jerarquía de nodos ya calculada, sin cambiar el contenido de los índices. Se quitaron cinco importaciones repetidas de las pruebas y se añadieron cuatro casos de escapes. Se conservan las seis herramientas, los formatos y los controles de conservación y concurrencia.

## 16/10/2026 — comunidad y soporte accesibles desde los README

Los cuatro README enlazan las discusiones de la comunidad ya habilitadas y los reportes de errores. CONTRIBUTING distingue dudas, propuestas y fallos, reutiliza la plantilla existente y pide comprobaciones proporcionales al cambio. El patrocinio sigue pendiente; no se habilitaron servicios ni se añadieron enlaces de cobro.

## 16/10/2026 — abrir la bóveda en Obsidian no desactualiza el índice

Al abrir la bóveda, Obsidian crea ajustes propios en `.obsidian/` (apariencia, atajos, marcadores, plugins, temas). El índice principal ahora cataloga solo los cuatro ajustes que trae el kit, así un cierre verificado no pasa a «Mapas desactualizados» solo por abrir la bóveda o cambiar su aspecto. Las notas, adjuntos y carpetas `.obsidian` dentro de subcarpetas siguen controlados. Observado en la prueba con ChatGPT.

## 16/10/2026 — instalar desde un kit abierto con OpenCode

Al abrir la carpeta del kit, OpenCode instala sus dependencias dentro de `.opencode/`. El instalador ya no las copia a la bóveda: omite `node_modules` y los archivos que OpenCode genera en esa carpeta, de modo que una bóveda con su propio `.opencode/package.json` no queda bloqueada por un conflicto. La guía de personalización aclara que un pedido puntual ya atendido, como un mail, se marca hecho en las acciones de la ficha y no cuenta como el primer paso elegido por el usuario.

## 16/10/2026 — README en cuatro idiomas

El README tiene versiones completas en inglés, alemán y chino, con un selector de idioma al comienzo de cada una; se quitó el resumen en inglés que estaba al final del README en español. Las guías, reglas e instrucciones para asistentes siguen en español. El índice de líneas reconoce la atribución inicial traducida y la mantiene como primera línea.

## 16/10/2026 — sin carpetas __pycache__ en la bóveda

Los scripts del kit ya no dejan carpetas `__pycache__` dentro de la bóveda al cargar sus módulos internos, como ocurría al validar o cerrar una sesión. Una prueba nueva lo comprueba ejecutando validación, cierre, catálogo, registro e instalación en una copia. Si una IA importa un script desde otro programa o usa `python -m`, ese módulo todavía puede dejar su propia caché.

## 15/10/2026 — próximo paso solo en la ficha

Al configurar, el Panel ya no copia el próximo paso como texto fijo: muestra la bienvenida y el acceso al proyecto y al inventario, y remite a «Acciones pendientes», que lee las tareas de las fichas y se actualiza sola. Así el Panel no queda desfasado cuando cambian las tareas. Las bóvedas ya configuradas conservan su línea anterior; el cierre no la edita.

## 15/10/2026 — destino visible al comprobar el cierre

El cierre muestra la ruta absoluta de la bóveda revisada antes de informar el resultado. Las guías usan una raíz explícita y explican que, sin ella, se revisa la bóveda donde está el script, no la carpeta actual. Se conserva esa selección y la API diaria; mover una copia no exige recrear sus notas.

## 15/10/2026 — conservar cambios posteriores al plan

Los planes del creador vuelven a comprobar reglas, fichas, índices y nombres ocupados antes de la primera escritura. Conservan los datos y el origen con los que se prepararon, evitan duplicar una ficha aparecida después y mantienen la creación exclusiva por archivo. La salida distingue una guardia que bloqueó de una fase de escritura iniciada que exige releer el estado; admite recuperación con un plan nuevo sin reemplazar archivos idénticos. No agrega transacciones globales ni deshace cambios automáticamente.

## 15/10/2026 — cierre coherente con el proyecto inicial

En la sección canónica de configuración, el cierre contrasta el identificador con una ficha propia incluida en la revisión diaria y un índice del mismo proyecto. Detecta identidades repetidas, coincidencias con ejemplos y referencias ausentes, ambiguas o externas en los formatos admitidos. Conserva nombres propios, proyectos adicionales, la configuración parcial sin archivos todavía y el formato anterior sin esa sección. No exige completar el perfil ni repara datos automáticamente; la guía de mantenimiento detalla el alcance.

## 14/10/2026 — operación visible coherente con el registro

El cierre detecta una etiqueta «Última operación de mantenimiento» antigua, duplicada o ambigua en sus formatos admitidos, sin modificar la configuración. Reconoce tildes equivalentes, énfasis y listas numeradas; distingue el código en citas y los comentarios dentro de código inline. Conserva compatibilidad con configuraciones sin etiqueta o con valor vacío; excluye ejemplos en código y comentarios. Las guías indican actualizar el ID antes de registrar la huella de la configuración, manteniendo IDs distintos para operaciones reales distintas.

## 14/10/2026 — inventario de perfil plegable

Las notas de configuración nuevas muestran proyecto y avance antes de la tabla opcional de respuestas. El inventario mantiene las seis columnas y puede plegarse; las tablas anteriores se conservan. El lector valida todos los datos y rechaza formatos mezclados o inventarios múltiples, sin contar ejemplos dentro de código o comentarios.

## 13/10/2026 — índices de proyectos con nombres propios

Los proyectos nuevos usan un nombre de índice ligado a su identificador para distinguirlos en el gráfico. El creador conserva nombres anteriores y propios, evita proponer un segundo índice al reintentar y rechaza ambigüedades o referencias incompatibles antes de escribir. No migra bóvedas existentes.

## Sin publicar — candidata a v0.1.0

- Configuración conversacional: entregar carpeta, responder preguntas y recibir una bóveda preparada, sin exigir Python ni edición de plantillas.
- Protocolo único para bóvedas nuevas, existentes o copias descargables; guarda configuración parcial antes del proyecto y permite retomar fichas editadas.
- Objetivo acordado, nombres derivados de las respuestas y fecha, fuentes y primera tarea opcionales. Enlaces portables en copias descargables.
- Inventario persistente de personalización: perfil, formación, materiales, alcance, vida útil y preferencias; distingue pendientes, omisiones y propuestas por bóveda y proyecto, sin exigir CV ni reiniciar la configuración.
- `INDICE.md` como primera lectura completa: catálogo con etiquetas breves, proyectos propios y ejemplos separados. Actualización después de guardar y comprobación al iniciar.
- Actualizador conserva comentarios y saltos LF/CRLF, evita enlaces y junctions y se integra con instalación y creación.
- Mapa vinculante de nodos con índices locales, resúmenes, padre e hijos. El mismo actualizador mantiene los bloques locales y el general; conserva índices manuales y fuentes originales.
- Identificación de IA y registro renovable a los cinco días, con historial íntegro y reintentos incluso si las notas cambian después. Zona horaria local, validación de registros dañados y recuperación de escrituras interrumpidas.
- Índices por líneas en notas editables y mapas nuevos, conservación de comentarios y exclusión de originales, históricos e integraciones del reindexado. Comprobación de rangos en CI; mantenimiento común sin exigir Python al usuario.
- Índice de líneas plegable en lectura, conservando los rangos y admitiendo el formato anterior. Plantillas agrupadas en `00_CORE/templates/`, separadas de las fichas existentes.
- Guía común de trabajo diario y revisión manual; accesos de Claude Code y OpenCode remiten a ella, conservando sus metadatos y permisos.
- Guías de OpenCode y ChatGPT para carpeta local o adjuntos; seis comandos para configurar, retomar, crear, redactar, validar y cerrar.
- Instalador conservador con simulación y detección de conflictos, sin reemplazar notas, instrucciones propias ni ajustes de Obsidian.
- Creador opcional comprueba nombres y coincidencias por propiedades, usa las plantillas y conserva archivos completos al reintentar.
- Panel y Bases reconocen fichas renombradas por propiedades y excluyen plantillas y ejemplos ficticios.
- Validador sin dependencias: propiedades planas, textos entre comillas y listas simples; explica errores de formato y avisos sin acreditar veracidad.
- Guías de escritura proporcionales a la tarea, alternativa manual para principiantes y recursos opcionales con atribución a davidkimai.
- Pruebas de conservación, reanudación, rutas y catálogo. CI en Windows/macOS/Linux con Python 3.8 y 3.13, acciones v7 y comprobación del índice.

Pendiente: completar los recorridos nativos en Claude Code, OpenCode y ChatGPT, probar con usuarios, comprobar al final la interfaz de Obsidian y publicar la release autorizada. La fecha y el tag v0.1.0 se fijan al publicar.
