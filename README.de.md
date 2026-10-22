> **Besonderer Dank an [davidkimai](https://github.com/davidkimai):** Dieses Kit basiert auf dessen Arbeit [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis passt diese Arbeit an, um Obsidian-Vaults mit Hilfe einer KI einzurichten und zu organisieren.

> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 3–19: Este índice
> - Líneas 21–22: Introducción
> - Líneas 23–28: Obsidian Genesis: dein Vault, eingerichtet von einer KI
> - Líneas 29–40: Was die Begriffe bedeuten
> - Líneas 41–59: In drei Schritten starten
> - Líneas 60–68: Was du erhältst
> - Líneas 69–76: Im Alltag
> - Líneas 77–97: Anleitungen
> - Líneas 98–113: Was im Ordner liegt
> - Líneas 114–119: Projektstand
> - Líneas 120–123: Datenschutz
> - Líneas 124–127: Lizenz
> - Líneas 128–131: Community und Hilfe
> - Líneas 132–135: Projekt unterstützen
> - Líneas 136–138: Über die Entwicklung

**Sprache:** [Español](README.md) · [English](README.en.md) · Deutsch · [中文](README.zh.md)

# Obsidian Genesis: dein Vault, eingerichtet von einer KI

Obsidian Genesis ist ein kostenloses Kit, mit dem du [Obsidian](https://obsidian.md) nutzen kannst, ohne zu wissen, wie es funktioniert. Du gibst diesen Ordner einer KI, die Dateien lesen und schreiben kann, beantwortest ein paar einfache Fragen, und die KI richtet deinen Vault ein: dein erstes Projekt, ein Panel als Einstieg und einen Index, den sie aktuell hält. Du musst nicht programmieren.

Es eignet sich für Studium, Arbeit oder jedes persönliche Projekt. Das Kit ist auf Spanisch: Du kannst dem Assistenten in deiner eigenen Sprache schreiben, aber die Notizen und Anleitungen des Kits bleiben vorerst auf Spanisch. Dieses README und den Dokumentenwegweiser gibt es auch auf Spanisch, Englisch und Chinesisch.

## Was die Begriffe bedeuten

| Begriff | Bedeutung |
|---|---|
| Vault | Der Ordner mit Notizen, den du mit Obsidian öffnest. |
| Projektkarte | Eine Notiz mit Ziel, geprüften Fakten und nächsten Schritten eines Projekts. |
| Panel | Die Startseite: deine Projekte und offenen Aufgaben. |
| Allgemeiner Index | `INDICE.md`, die Übersicht aller Dateien. Die KI liest ihn zuerst und hält ihn aktuell. |
| Knoten | Ein Themenordner mit eigenem Index, zum Beispiel „Zusammenfassungen meiner Kurse“. |

Die KI arbeitet mit den Regeln und Anleitungen des Kits: Sie fragt, bevor sie schreibt, erklärt, wo sie was speichert, und prüft die Dateien am Ende.

## In drei Schritten starten

1. **Lade das Repository herunter und entpacke es:** Code → Download ZIP.
2. **Öffne den Ordner in einer KI, die Dateien lesen und schreiben kann.** Wähle den Ordner, der dieses README und `AI-INSTRUCTIONS.md` enthält.
3. **Füge diese Nachricht ein und beantworte die Fragen:**

   > Ich möchte, dass du meinen Obsidian-Vault mit diesem Kit einrichtest. Lies zuerst `INDICE.md`, dann `00_CORE/atoms/00_vault-rules.md` und `AI-INSTRUCTIONS.md`. Ich kenne Obsidian nicht: Führe mich mit einfachen Fragen, ein oder zwei auf einmal, und kümmere dich anhand meiner Antworten um die Dateien. Erkläre mir vor dem Schreiben, wo du alles speicherst und was du anlegst. Halte den Hauptindex aktuell. Wenn du keinen Zugriff dafür hast, sag es mir.

| Du nutzt | So öffnest du das Kit |
|---|---|
| Claude Code | Öffne den Ordner und nutze die Nachricht oben oder `/configurar`. |
| OpenCode | Öffne den Ordner und nutze die Nachricht oben oder `/configurar`. [Anleitung](DOCS/opencode.md). |
| ChatGPT | Lokaler Ordner mit Dateiwerkzeugen oder eine angehängte Kopie. [Anleitung](DOCS/chatgpt.md). |
| Eine andere KI | Gib ihr Zugriff auf den Ordner und nutze dieselbe Nachricht. |

Die KI fragt, was du organisieren möchtest, welche Notizen du behalten willst und was das Ziel ist. Du kannst „weiß ich noch nicht“ oder „ich habe keine Frist“ antworten: Die erste Aufgabe kann später gewählt werden. Wenn du ein ZIP anhängst, statt Zugriff auf den Ordner zu geben, erklärt der [Schnellstart](DOCS/QUICKSTART.md), was du zurückbekommen kannst.

Wenn du bereits einen Vault hast, passt das Kit ihn nicht an: Verwende es in einem neuen Ordner. Bestehende Vaults anzupassen wird ein separates Repository, das noch nicht verfügbar ist.

## Was du erhältst

- Einen Ordner, den du als Vault öffnen kannst, mit deinem ersten Projekt und seiner Projektkarte.
- Das **Panel** (`Panel.md`) für den Zugriff auf Projekte und Aufgaben und **Leer primero** (`LEER_PRIMERO.md`, „Zuerst lesen“), das das Panel mit dem allgemeinen Index verbindet.
- Eine einfache Ansicht: Der Datei-Explorer zeigt deine Notizen und blendet die technischen Dateien des Kits aus. Die **Graphansicht** von Obsidian, über ihr Symbol in der Seitenleiste, zeigt, wie sie verbunden sind.
- Ein optionales, eingeklapptes **Personalisierungsinventar**: was du beantwortet hast, was offen ist und was du übersprungen hast. Du kannst es jederzeit mit **„was fehlt noch, um meinen Vault zu personalisieren“** vervollständigen. [So funktioniert es](00_CORE/protocols/personalizar-vault.md).

Zum Öffnen installierst du Obsidian von [obsidian.md](https://obsidian.md), öffnest den vorbereiteten Ordner als Vault und gehst zu `Panel.md`. Die KI prüft die Dateien; wie es in Obsidian aussieht, prüfst du selbst.

## Im Alltag

- **Fortsetzen:** Sag **„Mach weiter mit [Projekt]“** oder nutze `/empezar`. Die KI liest den Index, die Regeln und die Projektkarte und setzt das Offene fort.
- **Weitere Anfragen:** ein weiteres Projekt, ein Entwurf, eine Überprüfung oder das Speichern des Tagesabschlusses. [Anfragen zum Kopieren](DOCS/usar-con-otras-ias.md).
- **Mehr Inhalte organisieren:** Bitte **„Füge einen Knoten für Zusammenfassungen meiner Kurse hinzu“**. Die KI legt seinen Index an und verbindet ihn mit der allgemeinen Übersichtskarte. [So funktionieren Knoten](DOCS/indice-principal.md).

Claude Code und OpenCode enthalten `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` und `/cerrar`; in Claude werden das Anlegen eines weiteren Projekts und der Abschluss manuell aufgerufen. Die Berechtigungen hängen vom Assistenten ab. Wenn du mit Anhängen arbeitest, teile immer die aktuellen Notizen: Sie werden nicht von selbst synchronisiert.

## Anleitungen

Die Anleitungen sind auf Spanisch, außer dem Dokumentenwegweiser.

| Wenn du … möchtest | Lies |
|---|---|
| die Wege kennen, einer KI den Ordner zu geben | [Schnellstart](DOCS/QUICKSTART.md) |
| ChatGPT nutzen | [Erste Schritte mit ChatGPT](DOCS/chatgpt.md) |
| OpenCode nutzen | [Erste Schritte mit OpenCode](DOCS/opencode.md) |
| die Verbindung von Claude mit Obsidian (MCP) reparieren | [Wenn Claude keine Verbindung zum MCP herstellt](DOCS/mcp-claude.md) |
| die alltäglichen Anfragen kennen | [Mit einer KI arbeiten](DOCS/usar-con-otras-ias.md) |
| ein Projekt ohne KI anlegen | [Dein erstes Projekt von Hand](DOCS/primer-proyecto.md) |
| Panel, Vorlagen und einfache Ansicht verstehen | [Vorlagen und Panel](DOCS/obsidian.md) |
| Knoten hinzufügen und die Übersichtskarte verstehen | [Übersichtskarte und Knotenindizes](DOCS/indice-principal.md) |
| wissen, wie Änderungen protokolliert und geprüft werden | [Pflege](DOCS/mantenimiento.md) |
| die fünf optionalen Skills nutzen | [Optionale Skills](DOCS/skills-portables.md) |
| ein Problem lösen | [Fehlerbehebung](DOCS/TROUBLESHOOTING.md) |
| sehen, was jede Datei des Kits tut | [Wegweiser zu Dokumenten und Werkzeugen](DOCS/README.de.md) |

**Für Assistenten und die Entwicklung des Kits:** [Einstieg für die KI](AI-INSTRUCTIONS.md) · [Regeln des Vaults](00_CORE/atoms/00_vault-rules.md) · [Einrichtungsprotokoll](00_CORE/protocols/configurar-vault.md) · [Projektersteller](DOCS/creacion-para-asistentes.md) · [Mitwirken](CONTRIBUTING.md) · [Test mit Nutzenden](DOCS/prueba-con-usuarios.md) · [Veröffentlichung](DOCS/publicacion.md) · [Änderungsprotokoll](CHANGELOG.md).

## Was im Ordner liegt

| Ort | Wofür |
|---|---|
| `Panel.md` | Zugriff auf Projekte und Aufgaben |
| `LEER_PRIMERO.md` | Einstiegsnotiz für die Person und Verbindung der allgemeinen Knoten |
| `INDICE.md` | Katalog der Dateien und Projekte; erste Lektüre der KI |
| `00_CORE/` | Regeln, Projektkarten, Vorlagen und Werkzeuge |
| `PROJECT_TEMPLATE/` | Ordner eines Projekts: Quellen, Entwürfe, Ergebnisse und Archiv |
| `skills/` | Fünf optionale Skills |
| `DOCS/` | Anleitungen |

Das Beispiel `aprender-python` ist fiktiv und von deinen Projekten getrennt. Deine Daten stammen aus deinen Antworten; was du nicht weißt, kann leer bleiben.

Python 3.8 oder neuer automatisiert Erstellung, Prüfung und Index mit der Standardbibliothek. Ohne Python nutzt die KI ihre Dateiwerkzeuge.

## Projektstand

Version 1.0, die erste veröffentlichbare Version. Die Einrichtung im Gespräch mit fortsetzbarem Profil, der Projektersteller, verbundene Knoten und Indizes, das Änderungsprotokoll und die Prüfung funktionieren. Die automatischen Tests laufen unter Windows, macOS und Ubuntu mit Python 3.8 und 3.13 erfolgreich; das belegt nicht, dass das Kit einfach zu benutzen ist.

Einrichtung und Fortsetzung wurden mit Claude Code geprüft, die Einrichtung auch mit ChatGPT im Web. Noch offen sind die Fortsetzung in ChatGPT im Web und in OpenCode, ein Test mit fünf Einsteigenden und die abschließende Sichtprüfung in Obsidian. Details stehen im [Änderungsprotokoll](CHANGELOG.md) (auf Spanisch).

## Datenschutz

Das Kit speichert lokale Dateien und installiert keine Synchronisierung. Die KI verarbeitet das Geteilte gemäß ihrem Dienst und ihren Einstellungen: Gib ihr nur den nötigen Kontext.

## Lizenz

[MIT](LICENSE), mit Nennung von davidkimai und Albert Mestre. Unabhängige Adaption von Context Engineering, ohne Verbindung zum ursprünglichen Projekt.

## Community und Hilfe

Für Fragen, Ideen und Erfahrungen gibt es die [Community-Diskussionen](https://github.com/Albertmestre1256/obsidian-genesis/discussions). Wenn etwas nicht funktioniert, erstelle einen [Fehlerbericht](https://github.com/Albertmestre1256/obsidian-genesis/issues) mit der Vorlage „No me funciona“ und einem kleinen Beispiel mit fiktiven Daten. [Mitwirken](CONTRIBUTING.md) (auf Spanisch).

## Projekt unterstützen

Obsidian Genesis ist kostenlos und bleibt es auch. Wenn dir das Kit hilft, kannst du es auf [Patreon](https://www.patreon.com/obsidiangenesis) unterstützen. Beiträge schaffen Zeit für Anleitungen für Einsteigende, Tests mit echten Menschen, Übersetzungen und Hilfe. Sie sind freiwillig: Sie schalten keine Funktionen frei, und das gesamte Kit bleibt öffentlich.

## Über die Entwicklung

Albert Mestre entwickelt diese Adaption mit wesentlichen Beiträgen von **OpenCode, Claude und Codex (OpenAI)**. Diese KI-Werkzeuge halfen, einen wichtigen Teil des Codes zu erstellen, und unterstützten Dokumentation und Tests; sie werden hier als Mitwirkende gewürdigt. Vorschläge werden geprüft und Ergebnisse vor der Integration verifiziert; der Einsatz von KI ersetzt keine Tests mit Menschen und belegt für sich allein nicht, dass das Kit einfach zu benutzen ist.
