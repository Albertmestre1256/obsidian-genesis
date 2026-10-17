> **Besonderer Dank an [davidkimai](https://github.com/davidkimai):** Dieses Kit basiert auf dessen Arbeit [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis passt diese Arbeit an, um Obsidian-Vaults mit Hilfe einer KI einzurichten und zu organisieren.
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–16: Este índice
> - Líneas 18–19: Introducción
> - Líneas 20–27: Obsidian Genesis: dein Vault, eingerichtet von einer KI
> - Líneas 28–51: Projektstand — 16. Oktober 2026
> - Líneas 52–72: In drei Schritten starten
> - Líneas 73–78: Anhänge oder ein bestehender Vault
> - Líneas 79–86: Fortsetzen
> - Líneas 87–101: Was es enthält
> - Líneas 102–112: Optionale Hilfe
> - Líneas 113–116: Datenschutz
> - Líneas 117–120: Lizenz
> - Líneas 121–124: Community und Hilfe
> - Líneas 125–127: Über die Entwicklung

**Sprache:** [Español](README.md) · [English](README.en.md) · Deutsch · [中文](README.zh.md)

# Obsidian Genesis: dein Vault, eingerichtet von einer KI

Lade das Kit herunter, gib den Ordner einer KI und beantworte ihre Fragen. Der Assistent bereitet deine Notizen und dein erstes Projekt nach den Regeln des Kits vor. Du musst weder programmieren noch Obsidian kennen.

Ein **Vault** ist ein Ordner mit Notizen, den du mit [Obsidian](https://obsidian.md) öffnest. Das Kit ist auf Spanisch und eignet sich für Studium, Arbeit oder jedes persönliche Projekt. Du kannst dem Assistenten in deiner eigenen Sprache schreiben; die Notizen und Anleitungen des Kits bleiben vorerst auf Spanisch.

Die Einstiegsnotiz [Leer primero](LEER_PRIMERO.md) („Zuerst lesen“) verbindet das Panel und den allgemeinen Index. In einem neuen Vault aktiviert das Kit die **Graphansicht** von Obsidian: Öffne sie über ihr Symbol in der Seitenleiste, um die verbundenen Notizen zu erkunden, oder nutze den lokalen Graphen im Index eines Projekts.

## Projektstand — 16. Oktober 2026

**Lokaler Kandidat in Prüfung; noch keine stabile Version.** Der Schwerpunkt bleibt, einen Vault mit einfachen Fragen zu starten, ohne dass die Person programmieren oder die Indizes pflegen muss.

| Bereits umgesetzt | Was es ermöglicht |
|---|---|
| Einrichtung im Gespräch | Antworten vor dem ersten Projekt speichern und Offenes später fortsetzen. |
| Optionales, fortsetzbares Profil | Ein einziges einklappbares Inventar führen; ausgelassene Angaben bewahren und nur das ergänzen, was die Person wählt. |
| Verbundene Knoten und Indizes | Jede Sammlung verlinkt ihre übergeordnete Sammlung, ihre Unterknoten und Notizen; allgemeine Knoten verlinken die Übersichtskarte und Leer primero. Neue Projekte erhalten Indizes mit eigenem Namen. |
| Pflege und Abschluss | Den Assistenten identifizieren, Änderungen mit erhaltener Historie protokollieren und Projektkarten, Panel, Profil, Übersichtskarten, Zeilenbereiche und die Stimmigkeit des ersten Projekts prüfen. |
| Zugang für verschiedene KIs | Anleitungen für Claude Code, OpenCode, ChatGPT und andere Assistenten mit Dateiwerkzeugen; eine manuelle Alternative ist verfügbar. |

Der Projektersteller prüft den Zustand erneut, bevor er ein Projekt speichert, und unterscheidet blockierende Bedingungen von Teilfehlern; jede Datei wird angelegt, ohne eine vorhandene zu ersetzen.

Die Abschlussprüfung zeigt, welchen Ordner sie geprüft hat; die Anleitung verwendet dessen ausdrücklichen Pfad, um die heruntergeladene Kopie von deinem Vault zu unterscheiden.

Die jüngsten Codeänderungen wurden unter Windows gezielt geprüft: **129 bestandene Fälle für Profilinventar und Indizes sowie 25 bestandene und 1 übersprungener Fall für die Installation, jeweils unter Python 3.8 und 3.13**. Diese Ergebnisse gelten für konkrete Änderungen; die vollständige Testsammlung wurde für diese Version nicht erneut ausgeführt.

In zwei Testgesprächen mit Claude Code und fiktiven Personen richtete die KI den Vault ein, bestand die geprüfte Abschlusskontrolle und setzte beim Fortsetzen ohne wiederholte Fragen fort; in einem der beiden geschah das aus einem neuen Gespräch heraus. Aus diesen Tests entstanden zwei Anpassungen, die noch nicht in einem Gespräch getestet wurden: Das Panel speichert keine feste Kopie des nächsten Schritts mehr (er bleibt in der Projektkarte), und die Skripte hinterlassen keine technischen `__pycache__`-Ordner mehr im Vault. Das sind keine Tests mit echten Einsteigenden.

Es fehlen noch vollständige Gespräche in OpenCode und ChatGPT, Tests mit Einsteigenden und die restlichen visuellen Prüfungen in Obsidian. Einige Interaktionen wurden bereits in früheren Kopien beobachtet; das bestätigt nicht die Darstellung aller aktuellen Änderungen. Die lokalen Änderungen und die entfernte GitHub-Actions-Matrix warten noch auf eine autorisierte Veröffentlichung.

Die Community-Diskussionen sind verfügbar; Sponsoring ist noch offen. README und Dokumentenwegweiser sind auf Spanisch, Englisch, Deutsch und Chinesisch verfügbar; die gemeinsamen Anleitungen bleiben auf Spanisch. Bestehende Vaults anzupassen und zu optimieren ist eine spätere Phase. [Änderungsprotokoll](CHANGELOG.md) · [Mitwirken](CONTRIBUTING.md) (beide auf Spanisch).

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

## Anhänge oder ein bestehender Vault

Ein angehängtes ZIP gibt keinen Zugriff auf deinen Computer. Wenn der Chat Dateien erzeugen kann, kann er dir eine eingerichtete Kopie zum Herunterladen zurückgeben. Wenn er nur mit Text antwortet, bleibt das Speichern offen. Die [Zugangsanleitung](DOCS/QUICKSTART.md) erklärt die Möglichkeiten.

Wenn du bereits einen Vault hast, ist die aktuelle Integration zurückhaltend: Die KI liest seine Regeln, vergleicht Konflikte und bewahrt Notizen und Einstellungen. Einen ganzen bestehenden Vault automatisch umzuorganisieren oder zu optimieren ist noch nicht umgesetzt; das ist die oben erwähnte spätere Phase.

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
- [Das Kit ohne Python einbinden](DOCS/instalacion-manual.md).
- [Vorlagen und Panel](DOCS/obsidian.md).
- [Fehlerbehebung](DOCS/TROUBLESHOOTING.md).

Python 3.8 oder neuer automatisiert Installation, Erstellung, Prüfung und Index mit der Standardbibliothek. Die KI kann die Einrichtung auch mit ihren Dateiwerkzeugen vornehmen. Zum Mitwirken: [CONTRIBUTING](CONTRIBUTING.md).

## Datenschutz

Das Kit speichert lokale Dateien und installiert keine Synchronisierung. Die KI verarbeitet das Geteilte gemäß ihrem Dienst und ihren Einstellungen: Gib ihr nur den nötigen Kontext.

## Lizenz

[MIT](LICENSE), mit Nennung von davidkimai und Albert Mestre. Unabhängige Adaption von Context Engineering, ohne Verbindung zum ursprünglichen Projekt.

## Community und Hilfe

Für Fragen, Ideen und Erfahrungen gibt es die [Community-Diskussionen](https://github.com/Albertmestre1256/obsidian-genesis/discussions). Wenn etwas nicht funktioniert, erstelle einen [Fehlerbericht](https://github.com/Albertmestre1256/obsidian-genesis/issues) mit der Vorlage „No me funciona“ und einem kleinen Beispiel mit fiktiven Daten. [Mitwirken](CONTRIBUTING.md) (auf Spanisch).

## Über die Entwicklung

Albert Mestre entwickelt diese Adaption mit wesentlichen Beiträgen von **OpenCode, Claude und Codex (OpenAI)**. Diese KI-Werkzeuge halfen, einen wichtigen Teil des Codes zu erstellen, und unterstützten Dokumentation und Tests; sie werden hier als Mitwirkende gewürdigt. Vorschläge werden geprüft und Ergebnisse vor der Integration verifiziert; der Einsatz von KI ersetzt keine Tests mit Menschen und belegt für sich allein nicht, dass das Kit einfach zu benutzen ist.
