> [!info]- Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–10: Cambios
> - Líneas 11–14: 14/10/2026 — operación visible coherente con el registro
> - Líneas 15–18: 14/10/2026 — inventario de perfil plegable
> - Líneas 19–22: 13/10/2026 — índices de proyectos con nombres propios
> - Líneas 23–44: Sin publicar — candidata a v0.1.0

# Cambios

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
