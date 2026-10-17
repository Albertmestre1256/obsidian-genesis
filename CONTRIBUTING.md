> [!info]- Índice de esta nota (líneas)
> - Líneas 1–5: Este índice
> - Líneas 7–10: Contribuir
> - Líneas 11–14: Dónde pedir ayuda
> - Líneas 15–34: Comprobar cambios

# Contribuir

Probá los cambios en una copia de la bóveda. Conservá la separación entre fuentes, síntesis y entregables, los créditos y la compatibilidad con Python 3.8 o posterior.

## Dónde pedir ayuda

Usá [Discussions](https://github.com/Albertmestre1256/obsidian-genesis/discussions) para preguntar cómo empezar, compartir experiencias o proponer mejoras. Para un fallo reproducible, abrí una [issue](https://github.com/Albertmestre1256/obsidian-genesis/issues) con la plantilla «No me funciona»: explicá en qué paso ocurrió y usá un ejemplo ficticio pequeño. No hace falta compartir tu bóveda personal. También podés contribuir probando el inicio o mejorando las traducciones.

## Comprobar cambios

Para documentación, revisá el contenido, los enlaces y los índices de los archivos modificados. Para código, ejecutá los casos afectados; reservá la suite completa para cambios transversales o una entrega.

Para ejecutar las pruebas:

```sh
python -m pip install "pytest<9"
python -m pytest -q
python 00_CORE/schemas/validate.py
python actualizar_indice.py --comprobar
```

Las pruebas del instalador usan carpetas temporales y comprueban que no reemplace notas ni ajustes. Si cambiás rutas, revisá README, guías, skills y enlaces. Para cambios de interfaz, comprobá también una bóveda limpia en Obsidian.

Tras cambiar archivos o descripciones, actualizá `INDICE.md` con `python actualizar_indice.py` y volvé a comprobarlo. En OpenCode, verificá que los comandos se carguen y después probá su recorrido con un proveedor disponible. Una carga correcta no acredita la respuesta del modelo. Conservá las pruebas y sus datos ficticios fuera del kit distribuido.

En una propuesta de cambio, explicá el problema, qué cambia y cómo lo probaste. No incluyas datos de tu bóveda personal. Para informar un error, usá la plantilla de issue y un ejemplo ficticio mínimo.

Antes de publicar, completá la [lista de publicación](DOCS/publicacion.md).
