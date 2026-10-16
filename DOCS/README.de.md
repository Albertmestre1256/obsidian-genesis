---
tipo: guia-documentos
descripcion: "Inhalt und Zweck der Kit-Dokumente und wann sie hilfreich sind."
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–4: Propiedades
> - Líneas 5–17: Este índice
> - Líneas 19–26: Wegweiser zu den Dokumenten und Werkzeugen des Kits
> - Líneas 27–37: Inhaltsverzeichnis
> - Líneas 38–47: Einstieg
> - Líneas 48–65: Regeln und Projekte
> - Líneas 66–85: Hilfe
> - Líneas 86–99: Integrationen und Einstellungen
> - Líneas 100–113: Python und Tests
> - Líneas 114–124: Repository und Credits
> - Líneas 125–133: Optionale Ressourcen
> - Líneas 134–146: Beim Verwenden erzeugte Dateien

# Wegweiser zu den Dokumenten und Werkzeugen des Kits

**Haupt-README und seine Sprachen:** [Español](../README.md) · [English](../README.en.md) · [Deutsch](../README.de.md) · [中文](../README.zh.md)

**Dieser Wegweiser in anderen Sprachen:** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

Du musst zum Start nicht alles lesen: Folge dem Haupt-README und beantworte die Fragen deiner KI. Dieser Wegweiser erklärt die Dateien und hilft bei der Suche nach Unterstützung. Die Dateipfade bleiben in allen Sprachen gleich; die gemeinsamen Anweisungen des Kits sind weiterhin auf Spanisch. Dieser Wegweiser beschreibt das vollständige Repository und wird im heruntergeladenen Kit-Ordner gelesen. Beim Integrieren in einen anderen Vault bleibt er hier bei Tests und Entwicklungsdokumentation; die Nutzungshilfen werden kopiert.

## Inhaltsverzeichnis

- [Einstieg](#einstieg)
- [Regeln und Projekte](#regeln-und-projekte)
- [Hilfe](#hilfe)
- [Integrationen und Einstellungen](#integrationen-und-einstellungen)
- [Python und Tests](#python-und-tests)
- [Repository und Credits](#repository-und-credits)
- [Optionale Ressourcen](#optionale-ressourcen)
- [Beim Verwenden erzeugte Dateien](#beim-verwenden-erzeugte-dateien)

## Einstieg

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`README.md`](../README.md) · [`README.en.md`](../README.en.md) · [`README.de.md`](../README.de.md) · [`README.zh.md`](../README.zh.md) | Einstieg, Projektstand und Startnachricht für die KI. |
| [`LEER_PRIMERO.md`](../LEER_PRIMERO.md) | Einstiegsnotiz mit Verbindungen zu Panel, Übersicht und Regeln. |
| [`Panel.md`](../Panel.md) | Täglicher Zugang zu Projekten und Aufgaben. |
| [`INDICE.md`](../INDICE.md) | Tatsächlicher Gesamtkatalog des Vaults; erste Lektüre der KI. |
| [`AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md) · [`AGENTS.md`](../AGENTS.md) · [`CLAUDE.md`](../CLAUDE.md) | Die Assistentenanleitung bestimmt den Ablauf; AGENTS und CLAUDE verweisen darauf. |

## Regeln und Projekte

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`00_CORE/atoms/00_vault-rules.md`](../00_CORE/atoms/00_vault-rules.md) | Gemeinsame Regeln für Kontext, Erhalt, Verknüpfungen und Urheberschaft. |
| [`00_CORE/protocols/configurar-vault.md`](../00_CORE/protocols/configurar-vault.md) | Einrichtungsgespräch und Vault-Erstellung mit unvollständigen Angaben. |
| [`00_CORE/protocols/personalizar-vault.md`](../00_CORE/protocols/personalizar-vault.md) | Inventar der Antworten, Auslassungen und später ergänzbaren Angaben. |
| [`00_CORE/protocols/context-injection.md`](../00_CORE/protocols/context-injection.md) | Passenden Kontext laden, ohne den gesamten Vault zu lesen. |
| [`00_CORE/protocols/ai-write-protocol.md`](../00_CORE/protocols/ai-write-protocol.md) | Texte mit ausreichendem Kontext vorbereiten, verfassen und prüfen. |
| [`00_CORE/molecules/marco-comunicacion-general.md`](../00_CORE/molecules/marco-comunicacion-general.md) | Zweck, Zielgruppe und Art der Kommunikation bestimmen. |
| [`00_CORE/cognitive-tools/redaccion-tecnica.md`](../00_CORE/cognitive-tools/redaccion-tecnica.md) · [`00_CORE/cognitive-tools/redaccion-narrativa.md`](../00_CORE/cognitive-tools/redaccion-narrativa.md) · [`00_CORE/cognitive-tools/redaccion-operativa.md`](../00_CORE/cognitive-tools/redaccion-operativa.md) · [`00_CORE/cognitive-tools/redaccion-persuasiva.md`](../00_CORE/cognitive-tools/redaccion-persuasiva.md) | Schreibhilfen für technische, erzählende, operative und überzeugende Texte. |
| [`00_CORE/cells/ejemplo-context.md`](../00_CORE/cells/ejemplo-context.md) | Fiktives Beispiel einer Kontextnotiz; keine persönlichen Angaben von dir. |
| [`00_CORE/templates/TEMPLATE_cell.md`](../00_CORE/templates/TEMPLATE_cell.md) | Vorlage für eine Projekt-Kontextnotiz. |
| [`00_CORE/templates/TEMPLATE_configuracion.md`](../00_CORE/templates/TEMPLATE_configuracion.md) | Vorlage für Einrichtung und optionales, später ergänzbares Profil. |
| [`00_CORE/templates/TEMPLATE_nodo.md`](../00_CORE/templates/TEMPLATE_nodo.md) | Indexvorlage für eine Notizensammlung. |
| [`PROJECT_TEMPLATE/00 - Índice y Contexto.md`](../PROJECT_TEMPLATE/00%20-%20%C3%8Dndice%20y%20Contexto.md) | Grundlage des verknüpften Indexes für neue Projekte. |
| [`PROJECT_TEMPLATE/01_FUENTES/README.md`](../PROJECT_TEMPLATE/01_FUENTES/README.md) · [`PROJECT_TEMPLATE/02_SINTESIS/README.md`](../PROJECT_TEMPLATE/02_SINTESIS/README.md) · [`PROJECT_TEMPLATE/03_ENTREGABLES/README.md`](../PROJECT_TEMPLATE/03_ENTREGABLES/README.md) · [`PROJECT_TEMPLATE/_archivo/README.md`](../PROJECT_TEMPLATE/_archivo/README.md) | Erklären die Ablage von Originalen, Arbeit, Ergebnissen und Historie. |

## Hilfe

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`DOCS/QUICKSTART.md`](../DOCS/QUICKSTART.md) | Kurzverweis auf Einstieg und Zugriffshilfen. |
| [`DOCS/empezar-con-ia.md`](../DOCS/empezar-con-ia.md) | Echten Ordnerzugriff geben oder mit einer angehängten Kopie arbeiten. |
| [`DOCS/opencode.md`](../DOCS/opencode.md) | Kit öffnen und Befehle in OpenCode nutzen. |
| [`DOCS/chatgpt.md`](../DOCS/chatgpt.md) | ChatGPT-Abläufe mit Ordner oder Anhängen. |
| [`DOCS/usar-con-otras-ias.md`](../DOCS/usar-con-otras-ias.md) | Alltägliche Anfragen zum Fortsetzen, Schreiben oder Speichern von Fortschritten. |
| [`DOCS/primer-proyecto.md`](../DOCS/primer-proyecto.md) | Ein Projekt alternativ von Hand anlegen. |
| [`DOCS/instalacion-manual.md`](../DOCS/instalacion-manual.md) | Kit ohne Ausführen von Python integrieren. |
| [`DOCS/creacion-para-asistentes.md`](../DOCS/creacion-para-asistentes.md) | Technische Referenz für die KI beim Erstellen von Projektdateien. |
| [`DOCS/indice-principal.md`](../DOCS/indice-principal.md) | Übersicht, lokale Indizes und skalierbare Verknüpfungen pflegen. |
| [`DOCS/mantenimiento.md`](../DOCS/mantenimiento.md) | Zeilenbereiche, Übersichten und Protokoll aktualisieren; Abschluss prüfen. |
| [`DOCS/obsidian.md`](../DOCS/obsidian.md) | Vorlagen, Panel, Bases und Graph in Obsidian. |
| [`DOCS/TROUBLESHOOTING.md`](../DOCS/TROUBLESHOOTING.md) | Häufige Fehler und Diagnose eines blockierten Schritts. |
| [`DOCS/mcp-claude.md`](../DOCS/mcp-claude.md) | MCP-Verbindungen und Schemas in Claude diagnostizieren. |
| [`DOCS/prueba-con-usuarios.md`](../DOCS/prueba-con-usuarios.md) | Ablauf und Kriterien für Tests mit echten Einsteigenden. |
| [`DOCS/publicacion.md`](../DOCS/publicacion.md) | Prüfungen vor der Veröffentlichung einer Version. |

## Integrationen und Einstellungen

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`.claude/skills/configurar/SKILL.md`](../.claude/skills/configurar/SKILL.md) · [`.opencode/commands/configurar.md`](../.opencode/commands/configurar.md) | /configurar: Gespräch starten oder unvollständige Einrichtung fortsetzen. |
| [`.claude/skills/empezar/SKILL.md`](../.claude/skills/empezar/SKILL.md) · [`.opencode/commands/empezar.md`](../.opencode/commands/empezar.md) | /empezar: Projektkontext laden und fortfahren. |
| [`.claude/skills/nuevo-proyecto/SKILL.md`](../.claude/skills/nuevo-proyecto/SKILL.md) · [`.opencode/commands/nuevo-proyecto.md`](../.opencode/commands/nuevo-proyecto.md) | /nuevo-proyecto: weiteres Projekt vereinbaren und hinzufügen. |
| [`.claude/skills/redactar/SKILL.md`](../.claude/skills/redactar/SKILL.md) · [`.opencode/commands/redactar.md`](../.opencode/commands/redactar.md) | /redactar: mit vorhandenem Kontext und Fakten schreiben. |
| [`.claude/skills/validar/SKILL.md`](../.claude/skills/validar/SKILL.md) · [`.opencode/commands/validar.md`](../.opencode/commands/validar.md) | /validar: Kontextnotizen prüfen und Fehler oder Hinweise erklären. |
| [`.claude/skills/cerrar/SKILL.md`](../.claude/skills/cerrar/SKILL.md) · [`.opencode/commands/cerrar.md`](../.opencode/commands/cerrar.md) | /cerrar: Speichern von Änderungen vorschlagen und Freigegebenes prüfen. |
| [`.claude/skills/vault-manager/SKILL.md`](../.claude/skills/vault-manager/SKILL.md) · [`.claude/settings.json`](../.claude/settings.json) | Orientierung zur Vault-Nutzung und Einstellungen der Claude-Integration. |
| [`.obsidian/app.json`](../.obsidian/app.json) · [`.obsidian/core-plugins.json`](../.obsidian/core-plugins.json) · [`.obsidian/graph.json`](../.obsidian/graph.json) · [`.obsidian/templates.json`](../.obsidian/templates.json) | Grundeinstellungen für neue Vaults; eigene Einstellungen beim Integrieren erhalten. |
| [`Proyectos.base`](../Proyectos.base) | Projekttabelle des Panels; weder Notiz noch Skript. |

## Python und Tests

Python automatisiert Aufgaben. Mit einer KI, die Dateien verwalten kann, brauchst du zum Verwenden des Kits nicht zu programmieren. Tests dienen der Entwicklung des Kits; der Installer kopiert sie nicht in einen eingerichteten Vault.

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`instalar.py`](../instalar.py) | Kit zu einem anderen Vault hinzufügen, ohne vorhandene Dateien zu ersetzen. |
| [`crear_proyecto.py`](../crear_proyecto.py) | Kontextnotiz und Ordner eines vereinbarten Projekts erstellen. |
| [`actualizar_indice.py`](../actualizar_indice.py) | Allgemeinen Index und Knotenindizes erzeugen oder prüfen. |
| [`00_CORE/schemas/validate.py`](../00_CORE/schemas/validate.py) | Kontextnotizen und Einrichtung prüfen; mit --cierre einen Vorgang abgleichen. |
| [`00_CORE/schemas/note_index.py`](../00_CORE/schemas/note_index.py) | Zeilenbereiche bearbeitbarer Notizen berechnen und prüfen. |
| [`00_CORE/schemas/registrar_cambios.py`](../00_CORE/schemas/registrar_cambios.py) | Urheberschaft und geänderte Dateien mit erhaltener Historie protokollieren. |
| [`tests/conftest.py`](../tests/conftest.py) · [`tests/test_crear_proyecto.py`](../tests/test_crear_proyecto.py) · [`tests/test_indice.py`](../tests/test_indice.py) · [`tests/test_instalar.py`](../tests/test_instalar.py) · [`tests/test_kit.py`](../tests/test_kit.py) · [`tests/test_mantenimiento.py`](../tests/test_mantenimiento.py) · [`tests/test_nodos.py`](../tests/test_nodos.py) · [`tests/test_validate.py`](../tests/test_validate.py) | Gemeinsame Testvorbereitung sowie Tests für Erstellung, Indizes, Installation, Paket, Pflege, Knoten und Validierung. |

## Repository und Credits

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`LICENSE`](../LICENSE) | MIT-Lizenz und Namensnennung von davidkimai und Albert Mestre. |
| [`CHANGELOG.md`](../CHANGELOG.md) | Änderungen des Kits nach Version oder Datum. |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Mitwirken, Hilfe suchen und Änderungen prüfen. |
| [`.github/ISSUE_TEMPLATE/no-me-funciona.md`](../.github/ISSUE_TEMPLATE/no-me-funciona.md) | Kurze Vorlage für Fehlerberichte mit fiktivem Beispiel. |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | Definition der Remote-Tests in GitHub Actions. |
| [`.gitignore`](../.gitignore) | Lokale Dateien, die Git ignorieren soll. |

## Optionale Ressourcen

| Dokument oder Werkzeug | Zweck |
|---|---|
| [`00_CORE/davidkimai-resources/README.md`](../00_CORE/davidkimai-resources/README.md) | Einstieg in angepasste Ressourcen des Originalprojekts; optional. |
| [`00_CORE/davidkimai-resources/protocols/01_extract_information.md`](../00_CORE/davidkimai-resources/protocols/01_extract_information.md) | Informationen aus Quellen entnehmen, ohne Fehlendes zu erfinden. |
| [`00_CORE/davidkimai-resources/evaluation/token_budgeting.md`](../00_CORE/davidkimai-resources/evaluation/token_budgeting.md) | Ausreichenden Kontext auswählen, ohne irrelevantes Material zu laden. |
| [`00_CORE/davidkimai-resources/field-theory/field_dynamics.md`](../00_CORE/davidkimai-resources/field-theory/field_dynamics.md) | Optionales Denkmodell zum Verknüpfen und Pflegen von Kontext. |

## Beim Verwenden erzeugte Dateien

Diese Dateien entstehen erst aus deinen Antworten und liegen dem Kit nicht als persönliche Dateien bei. Die Projektnamen unten sind Beispielpfade; du musst diese Dateien nicht von Hand anlegen. In Beispielpfaden steht `{ID}` oder `ID` für die gewählte Projektkennung; es ist kein wörtlicher Name.

| Dokument oder Werkzeug | Zweck |
|---|---|
| `00_CORE/configuracion.md` | Antworten, übersprungene Angaben und Einrichtungsstand; ermöglicht Fortsetzen ohne erneute Befragung. |
| `00_CORE/cells/{ID}-context.md` | Kontextnotiz je Projekt mit Ziel, Fakten, Entscheidungen und nächsten Aufgaben. |
| `ID/00 - Índice - ID.md` | Eigener Projektindex mit Verbindungen zu Notizen und Unterknoten. Auch ein unabhängiger Knoten hat einen Index. |
| `ID/01_FUENTES/ · ID/02_SINTESIS/ · ID/03_ENTREGABLES/ · ID/_archivo/` | Originalmaterial, laufende Arbeit, Ergebnisse und Historie im vereinbarten Umfang. |
| `00_CORE/logs/registro-cambios.md · 00_CORE/logs/historial/` | Änderungsprotokoll mit Urheberschaft; bei Erneuerung nach fünf Tagen bleibt das vorherige archiviert. |

Der allgemeine Index enthält das tatsächliche Inventar. Dieser Wegweiser erklärt die Aufgaben der Dateien; er ersetzt keine Regeln und verlangt nicht, alle Dokumente in jedes Gespräch zu laden.
