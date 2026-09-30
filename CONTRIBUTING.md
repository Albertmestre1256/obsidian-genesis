# Contribuir

Probá los cambios en una copia de la bóveda. Conservá la separación entre fuentes, síntesis y entregables, los créditos y la compatibilidad con Python 3.8 o posterior.

Para ejecutar las pruebas:

```sh
python -m pip install "pytest<9"
python -m pytest -q
python 00_CORE/schemas/validate.py
```

Las pruebas del instalador usan carpetas temporales y comprueban que no reemplace notas ni ajustes. Si cambiás rutas, revisá README, guías, skills y enlaces. Para cambios de interfaz, comprobá también una bóveda limpia en Obsidian.

En una propuesta de cambio, explicá el problema, qué cambia y cómo lo probaste. No incluyas datos de tu bóveda personal. Para informar un error, usá la plantilla de issue y un ejemplo ficticio mínimo.

Antes de publicar, completá la [lista de publicación](DOCS/publicacion.md).
