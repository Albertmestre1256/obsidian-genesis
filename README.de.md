> **Besonderer Dank an [davidkimai](https://github.com/davidkimai):** Dieses Kit basiert auf dessen Arbeit [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis passt diese Arbeit an, um Obsidian-Vaults mit Hilfe einer KI einzurichten und zu organisieren.

> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 3–18: Este índice
> - Líneas 20–21: Introducción
> - Líneas 22–29: Obsidian Genesis: dein Vault, eingerichtet von einer KI
> - Líneas 30–53: Projektstand — 20. Oktober 2026
> - Líneas 54–74: In drei Schritten starten
> - Líneas 75–80: Anhänge und vorhandene Notizen
> - Líneas 81–88: Fortsetzen
> - Líneas 89–103: Was es enthält
> - Líneas 104–113: Optionale Hilfe
> - Líneas 114–117: Datenschutz
> - Líneas 118–121: Lizenz
> - Líneas 122–125: Community und Hilfe
> - Líneas 126–129: Projekt unterstützen
> - Líneas 130–132: Über die Entwicklung

**Sprache:** [Español](README.md) · [English](README.en.md) · Deutsch · [中文](README.zh.md)

# Obsidian Genesis: dein Vault, eingerichtet von einer KI

Lade das Kit herunter, gib den Ordner einer KI und beantworte ihre Fragen. Der Assistent bereitet deine Notizen und dein erstes Projekt nach den Regeln des Kits vor. Du musst weder programmieren noch Obsidian kennen.

Ein **Vault** ist ein Ordner mit Notizen, den du mit [Obsidian](https://obsidian.md) öffnest. Das Kit ist auf Spanisch und eignet sich für Studium, Arbeit oder jedes persönliche Projekt. Du kannst dem Assistenten in deiner eigenen Sprache schreiben; die Notizen und Anleitungen des Kits bleiben vorerst auf Spanisch.

Die Einstiegsnotiz [Leer primero](LEER_PRIMERO.md) („Zuerst lesen“) verbindet das Panel und den allgemeinen Index. In einem neuen Vault aktiviert das Kit die **Graphansicht** von Obsidian: Öffne sie über ihr Symbol in der Seitenleiste, um die verbundenen Notizen zu erkunden, oder nutze den lokalen Graphen im Index eines Projekts.

## Projektstand — 20. Oktober 2026

**Code in `main` veröffentlicht (`c69c38a`); noch keine stabile Version.** Der Schwerpunkt bleibt, einen Vault mit einfachen Fragen zu starten, ohne dass die Person programmieren oder die Indizes pflegen muss.

| Bereits umgesetzt | Was es ermöglicht |
|---|---|
| Einrichtung im Gespräch | Antworten vor dem ersten Projekt speichern und Offenes später fortsetzen. |
| Optionales, fortsetzbares Profil | Ein einziges einklappbares Inventar führen; ausgelassene Angaben bewahren und nur das ergänzen, was die Person wählt. |
| Verbundene Knoten und Indizes | Jede Sammlung verlinkt ihre übergeordnete Sammlung, ihre Unterknoten und Notizen; allgemeine Knoten verlinken die Übersichtskarte und Leer primero. Neue Projekte erhalten Indizes mit eigenem Namen. |
| Pflege und Abschluss | Den Assistenten identifizieren, Änderungen mit erhaltener Historie protokollieren und Projektkarten, Panel, Profil, Übersichtskarten, Zeilenbereiche und die Stimmigkeit des ersten Projekts prüfen. |
| Zugang für verschiedene KIs | Anleitungen für Claude Code, OpenCode, ChatGPT und andere Assistenten mit Dateiwerkzeugen; eine manuelle Alternative ist verfügbar. |

Der Projektersteller prüft den Zustand erneut, bevor er ein Projekt speichert, und unterscheidet blockierende Bedingungen von Teilfehlern; jede Datei wird angelegt, ohne eine vorhandene zu ersetzen.

Die einfache Ansicht reduziert die sichtbaren Hilfsdateien im Datei-Explorer und im Graphen der neuen Vaults, die das Kit vorbereitet.

Die [entfernte Testmatrix für den Code-Commit `c69c38a`](https://github.com/Albertmestre1256/obsidian-genesis/actions/runs/39375866749) endete **6/6 erfolgreich** unter Windows, macOS und Ubuntu mit Python 3.8 und 3.13. Das sind technische Ergebnisse; sie belegen keine einfache Bedienung.

Einrichtung und Fortsetzung wurden mit Claude Code geprüft. Der manuelle Versuch mit OpenCode/Big Pickle zeigte fortgesetzte Nutzung innerhalb derselben Sitzung, aber keine unabhängig geprüfte Fortsetzung. Ein neuer Codex-Chat setzte eine frühere Kopie fort und bewahrte ausgelassene Angaben, mit externem Kontext und externen Werkzeugen. Das sind keine Tests mit echten Einsteigenden; sie bestätigen nicht die Oberfläche aller aktuellen Änderungen.

Noch offen sind die unabhängige Fortsetzung in OpenCode, die gesonderte Prüfung von ChatGPT im Web, ein Test mit fünf Einsteigenden (mindestens vier ohne Hilfe) und die abschließende formale Sichtprüfung in Obsidian.

Die Community-Diskussionen sind verfügbar, und du kannst das Projekt auf [Patreon](https://www.patreon.com/obsidiangenesis) unterstützen. README und Dokumentenwegweiser sind auf Spanisch, Englisch, Deutsch und Chinesisch verfügbar; die gemeinsamen Anleitungen bleiben auf Spanisch. Bestehende Vaults anzupassen oder zu optimieren gehört nicht zu diesem Kit: Dafür wird es ein separates Repository geben. [Änderungsprotokoll](CHANGELOG.md) · [Mitwirken](CONTRIBUTING.md) (beide auf Spanisch).

## In drei Schritten starten

1. **Lade das Repository herunter und entpacke es:** Code → Download ZIP.
2. **Öffne den Ordner in einer KI, die Dateien lesen und schreiben kann.** Wähle den Ordner, der dieses README und `AI-INSTRUCTIONS.md` enthält.
3. **Füge diese Nachricht ein und beantworte die Fragen:**

   > Ich möchte, dass du meinen Obsidian-Vault mit diesem Kit einrichtest. Lies zuerst `INDICE.md`, dann `00_CORE/atoms/00_vault-rules.md` und `AI-INSTRUCTIONS.md`. Ich kenne Obsidian nicht: Führe mich mit einfachen Fragen, ein oder zwei auf einmal, und kümmere dich anhand meiner Antworten um die Dateien. Erkläre mir vor dem Schreiben, wo du alles speicherst und was du anlegst. Halte den Hauptindex aktuell. Wenn du keinen Zugriff dafür hast, sag es mir.

| Du nutzt | So öffnest du das Kit |
|---|---|
| OpenCode | Öffne den Ordner und nutze die Nachricht oben oder `/configurar`. [Anleitung](DOCS/opencode.md). |
| ChatGPT | Lokaler Ordner mit Dateiwerkzeugen oder eine angehängte Kopie. [Anleitung](DOCS/chatgpt.md). |
| Claude Code | Öffne den Ordner und nutze die Nachricht oben oder `/configurar`. |
| Eine andere KI | Gib ihr Zugriff auf den Ordner und nutze dieselbe Nachricht. |

Die KI fragt, was du organisieren möchtest, welche Notizen du behalten willst und was das Ziel ist. Du kannst „weiß ich noch nicht“ oder „ich habe keine Frist“ antworten; die erste Aufgabe kann später gewählt werden.

Sie führt außerdem ein **Personalisierungsinventar**: was du beantwortet hast, was offen ist und was du übersprungen hast. In neuen Notizen ist es unter dem Projekt und seinem Fortschritt eingeklappt; du kannst es aufklappen, wenn du es ansehen möchtest. Vorstellung, Lebenslauf, Ausbildung, Routine und Nutzungsdauer des Vaults sind optional. Du kannst mit dem Nötigsten beginnen und später **„was fehlt noch, um meinen Vault zu personalisieren“** oder **„lass uns mein Profil vervollständigen“** sagen. [So funktioniert es](00_CORE/protocols/personalizar-vault.md).

**Du erhältst:** einen vorbereiteten Ordner, die Projektkarte, ein Panel für den Zugriff und eine Erklärung, wie du ihn in Obsidian öffnest. Die KI prüft die Dateien; die visuelle Prüfung erfolgt in Obsidian. Falls du es noch nicht hast, installiere es von [obsidian.md](https://obsidian.md), öffne den vorbereiteten Ordner als Vault und gehe zu `Panel.md`.

## Anhänge und vorhandene Notizen

Ein angehängtes ZIP gibt keinen Zugriff auf deinen Computer. Wenn der Chat Dateien erzeugen kann, kann er dir eine eingerichtete Kopie zum Herunterladen zurückgeben. Wenn er nur mit Text antwortet, bleibt das Speichern offen. Die [Zugangsanleitung](DOCS/QUICKSTART.md) erklärt die Möglichkeiten.

Wenn du bereits einen Vault hast, passt dieses Kit ihn nicht an: Verwende es in einem neuen Ordner. Bestehende Vaults anzupassen oder zu optimieren wird ein separates Repository, das noch nicht verfügbar ist.

## Fortsetzen

Sag **„Mach weiter mit [Projekt]“**. Die KI liest zuerst den Index, dann die Regeln und die aktuelle Projektkarte und setzt das Offene fort. Du kannst um ein weiteres Projekt, einen Entwurf, eine Überprüfung oder das Speichern des Abschlusses bitten: [Alltägliche Anfragen](DOCS/usar-con-otras-ias.md).

Um mehr Inhalte zu organisieren, bitte **„Füge einen Knoten für Zusammenfassungen meiner Kurse hinzu“**. Jeder Knoten hat einen Index mit Links und Zusammenfassungen; die allgemeine Übersichtskarte verbindet alle Knoten, und die KI pflegt sie beim Hinzufügen von Notizen. Vorhandene Indizes bleiben erhalten; sie umzubenennen oder Notizen umzuorganisieren erfordert einen vereinbarten Umfang. [Anleitung](DOCS/indice-principal.md).

Claude Code und OpenCode enthalten `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` und `/cerrar`. In Claude werden das Anlegen eines weiteren Projekts und der Abschluss manuell aufgerufen. Die Berechtigungen hängen vom Assistenten ab. Teile bei Anhängen immer die aktuellen Notizen: Sie werden nicht synchronisiert.

## Was es enthält

Was die einzelnen Dateien tun und wann sie hilfreich sind, erklärt der [Wegweiser zu Dokumenten und Werkzeugen](DOCS/README.de.md).

| Ort | Zweck |
|---|---|
| `INDICE.md` | Erste Lektüre: vollständiger Katalog der Dateien und Projekte |
| `LEER_PRIMERO.md` | Einstiegsnotiz für die Person und zentrale Verbindung der allgemeinen Knoten |
| `Panel.md` | Zugriff auf Projekte und Aufgaben |
| `00_CORE/` | Regeln, Projektkarten, Anleitungen und Werkzeuge |
| `PROJECT_TEMPLATE/` | Ordner für Quellen, Entwürfe, Ergebnisse und Verlauf |
| `DOCS/` | Optionale Hilfe |

Das Beispiel `aprender-python` ist fiktiv und von deinen eigenen Projekten getrennt. Deine Daten werden aus deinen Antworten ergänzt; Abschnitte ohne Angaben können leer bleiben.

## Optionale Hilfe

Diese Anleitungen sind auf Spanisch:

- [Ein Projekt von Hand anlegen](DOCS/primer-proyecto.md).
- [Vorlagen und Panel](DOCS/obsidian.md).
- [Fehlerbehebung](DOCS/TROUBLESHOOTING.md).

Python 3.8 oder neuer automatisiert Erstellung, Prüfung und Index mit der Standardbibliothek. Die KI kann die Einrichtung auch mit ihren Dateiwerkzeugen vornehmen. Zum Mitwirken: [CONTRIBUTING](CONTRIBUTING.md).

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
