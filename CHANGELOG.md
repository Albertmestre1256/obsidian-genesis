> [!info]- Índice de esta nota (líneas)
> - Líneas 1–13: Este índice
> - Líneas 15–16: Cambios
> - Líneas 17–20: 16/10/2026 — README en cuatro idiomas
> - Líneas 21–24: 16/10/2026 — sin carpetas __pycache__ en la bóveda
> - Líneas 25–28: 15/10/2026 — próximo paso solo en la ficha
> - Líneas 29–32: 15/10/2026 — destino visible al comprobar el cierre
> - Líneas 33–36: 15/10/2026 — conservar cambios posteriores al plan
> - Líneas 37–40: 15/10/2026 — cierre coherente con el proyecto inicial
> - Líneas 41–44: 14/10/2026 — operación visible coherente con el registro
> - Líneas 45–48: 14/10/2026 — inventario de perfil plegable
> - Líneas 49–52: 13/10/2026 — índices de proyectos con nombres propios
> - Líneas 53–74: Sin publicar — candidata a v0.1.0

# Cambios

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
