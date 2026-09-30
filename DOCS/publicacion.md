# Preparar la primera publicación

Usá esta lista sobre la versión final del kit:

- [ ] Probar el Panel, Plantillas y enlaces en Obsidian limpio.
- [ ] Probar las cinco skills en Claude Code real.
- [ ] Completar y registrar la prueba con usuarios.
- [ ] Ejecutar `python -m pytest -q` y el validador.
- [ ] Confirmar nombre de repositorio, cuenta y visibilidad con la persona responsable.
- [ ] Confirmar el contacto previsto con el autor del material de origen.
- [ ] Revisar archivos y ZIP para excluir notas personales, credenciales y estado local.
- [ ] Crear primero el repositorio privado, si se mantiene ese plan, y revisar allí el contenido.
- [ ] Confirmar publicación pública, tag `v0.1.0` y release con ZIP.

El ZIP debe incluir `.claude/`, `.obsidian/` y `.github/`, además de las notas y scripts. Excluir `.git/`, cachés de Python, `.obsidian/workspace*.json` y archivos personales. Extraerlo en una carpeta nueva y volver a ejecutar pruebas antes de subirlo.

No marcar los casilleros por haber escrito el procedimiento: se completan con resultados reales.
