# Konzept: „Language Learning“ – eine App, mehrere Sprachen

Stand: 13.10.2026. **Schritt 1 (Umbau) gebaut und veröffentlicht am 13.10.:** Sprachpakete, Umschalter, Pensum 3 + 8, Offline pro Sprache, App an der Wurzel, Name „Language Learning“, alter Stand wird automatisch übernommen. Figuren: Diego (Spanisch), Giovanni (Italienisch), Aurélien lernt Deutsch (Vorschlag). Grundlage: Brainstorming mit Mr. Alex (13.10.).
Grundsatz wie bisher: vor jedem Bauschritt fragen.

## 1. Festgelegt (Mr. Alex, 13.10.)

- **Eine App, ein Umschalter** für die Sprachen; keine App pro Sprache. Neue Sprachen sollen sich bequem ergänzen lassen.
- **Sprachen:** zuerst Umbau mit Französisch, dann **Spanisch**, dann **Italienisch**, außerdem **Deutsch umgedreht** (Ziel Deutsch, Hilfe Französisch) mit **eigenen deutschen Redewendungen**, nicht aus den französischen Daten gespiegelt.
- **Pensum:** **Wiederholungen einstellbar 4/6/8/10/12 pro Sprache, Voreinstellung 8 (Mr. Alex, 14.11.); neue einstellbar 1–5 pro Sprache, Voreinstellung 1** (Mr. Alex, 29.10.; vorher fest 3 neue, bestätigt 13.10.). Auswahl unter dem Séance-Knopf.
- **Séance nach Word Gym 2.0 (Mr. Alex, 14.11., Vorlage School-App « Deine 5 Minuten »):** 1. **Satz zuerst:** eine Wendung wird erst neue Karte, wenn Schritt 1 ihres Teils im Thema fertig ist; sonst nur Wiederholungen und ein Hinweis auf der Startkarte. 2. **Stolpersteine:** dreimal verfehlt und unter Stufe 3 = 🧩, kommt in der Séance zuerst, zeigt den Satz mit Lücke, Liste in « Meine Sammlung ». 3. **Antworten füttern den Kasten:** « Encore » in Séance und « Trouve l'expression » = zwei Stufen zurück, morgen fällig, Fehler gezählt; « Je savais » im Thema hebt nur fällige Karten. 4. **Abrufform wächst mit der Stufe (14.11.):** Stufe 0–1 sagen und selbst einschätzen · 2–3 Auswahl aus drei (Ablenker aus demselben Thema) · 4–5 Wendung tippen · 6–7 Satzlücke tippen; Arabisch und Wendungen mit « … » wählen statt tippen; « 💡 Leichter » wechselt zur Auswahl. Tippen: Groß/Klein, Satzzeichen, Apostroph egal, « / » = Varianten, « (e) » optional; nur Akzente falsch oder 1–2 Tippfehler = « Presque » (zählt richtig, Schreibweise wird gezeigt). Geprüft richtig = eine Stufe hoch, falsch = zwei zurück. **Ab Stufe 3 hebt nur eine geprüfte Antwort** – « Je savais » (Séance Stufe 0–1, Thema) wirkt nur bis Stufe 3.
5. **Combo und Memory (14.11., Vorlage School-App):** Combo-Zähler 🔥 im Séance-Kopf ab 2 richtigen in Folge; bei 3 🛴, bei 5 🚗 mit Spur, bei jedem Zehner 🚀 mit Konfetti, Klang aus Web Audio (keine Aufnahme); Fehler setzt zurück. Memory 🎲 nach fertiger Séance (Endseite und Startkarte): 6 Paare Wendung ↔ kurze Übersetzung (ohne Klammern), zuerst aus den Wendungen von heute, aufgefüllt aus dem Kasten; aufgedeckte Wendung wird vorgelesen; +10 Punkte für das erste gewonnene Spiel des Tages (`S.memoryTag`).
6. **Aus School übernommen (15.11., Vorlage « Muscu des mots » FR und Power Up EN6/EN9):** **Satz-Karten** – zwei pro Tag aus Dialogzeilen, Geschichte (freie Kapitel), Anekdoten (freie) sowie Beispiel- und Zeitmaschinen-Sätzen anderer Wendungen, Lücke = die Wendung; eigener Kasten `S.saetze`; neu nur, wenn die Wendung schon im Kasten ist oder der Dialog gemacht wurde; Stufe 0–1 selbst, 2–5 wählen, ab 6 tippen. **Tagesplan:** Wiederholungen aufgefüllt mit den als Nächstes fälligen, nur fällige steigen; zum Schluss ein sicherer Treffer (« !id », Auswahl); Fehler kommen vor dem Schluss noch einmal. **« 💪 N sicher »** ab Stufe 5 (Startkarte, Sammlung mit Balken); Stolpersteine bis Stufe 5. **⚡ Power Up:** `S.teile[key] = { am, s }`, fällig nach 30/60/120 Tagen, Kachel/Gruppe/Sprung gelb mit ⚡, Startseite « ⚡ N Teile fast leer » mit Knopf, Wiederholung = Stufe +1 und « Aufgeladen! », Sperrzeiten 50/35/25 % bei bekannten Teilen; alte `true`-Einträge gelten als heute erledigt.
- **Inhalte pro Sprache neu finden, nicht übersetzen:** gleiche Themen (Lebenswelt), aber in jeder Sprache die dort wirklich gebräuchlichen Redewendungen. Alles andere (Übungen, Séance, Leitner, Spiel) bleibt gleich.
- **Name:** App „Language Learning“. Repository bleibt `Languages` → Adresse bleibt `https://langenbachalex.github.io/Languages/`.

## 2. Architektur

- **Sprache = Paar aus Zielsprache und Hilfssprache**, z. B. `fr-de` (Französisch, Hilfe Deutsch), `es-de`, `it-de`, `de-fr` (Deutsch, Hilfe Französisch).
- **Dateien je Paar:** `inhalte/<paar>/` (TSVs wie bisher), `app/daten_<paar>.js`, `app/audio/<paar>/…`, `docs/<paar>/konzept.md`. Bauskript: ein Eintrag je Paar in einer Liste.
- **Ein Code:** `app/index.html`, `app/app.js` an der Wurzel. Alle Oberflächentexte (Ansagen, Knöpfe, Lob, Titel, Ansprache) kommen aus der Sprachdatei, nicht aus dem Code. Die Übungstypen bleiben: Séance, Écouter et répéter (3 Stufen), Zeitmaschine, Trouve l'expression, Dialoge mit Rollen, Aussprache, Karte, Geschichte.
- **Umschalter** oben in der Leiste: Flaggen/Kürzel der verfügbaren Paare. Die gewählte Sprache bleibt gespeichert.
- **Fortschritt getrennt pro Paar:** Leitner-Kasten, Teile, Karte, Geschichte, Titel. **Gemeinsam:** Serien (Schultage), Punkte als ein Konto, Wochen-Kalender. Für die Serie zählt der Tag, sobald in irgendeiner Sprache ein Teil oder eine Séance fertig ist.
- **Offline:** Vorab geladen werden nur Code und die zuletzt genutzte Sprache. Pro Sprache ein Knopf „Hors-ligne / Sin conexión / Offline“ mit Anzeige des Stands; Audio anderer Sprachen wird erst beim Umschalten geladen. (Französisch allein: 46 MB.)
- **Adresse:** App an der Wurzel `…/Languages/`; `…/Languages/francais/` leitet weiter. Fortschritt im Browser bleibt (gleiche Domain).

## 3. Inhalte je Sprache

| | Französisch (fertig) | Spanisch (fertig) | Italienisch (fertig) | Deutsch, Hilfe FR (fertig) |
|---|---|---|---|---|
| Themen | 9 × 24 Wendungen | gleiche 9 Themen, eigene Wendungen | gleiche 9 Themen, eigene Wendungen | gleiche Themen, **deutsche** Redewendungen (fix und fertig sein, die Nase voll haben …) |
| Gesprächspartner | Aurélien | [offen: z. B. eine Kollegin aus Sevilla] | [offen: z. B. ein Freund aus Bologna] | [offen: Alex selbst als Lehrer? Aurélien lernt Deutsch?] |
| Aussprache | Nasale | r/rr, b/v, j/g, ll/y | Doppelkonsonanten (pala/palla), offene/geschlossene e/o, gli/gn | ch/sch, ü/ö, h, Endungen -e/-er |
| Faux amis | gegen Englisch | gegen Englisch **und** Französisch (*constipado, embarazada, burro*) | gegen Englisch und Französisch/Spanisch (*burro, camera, caldo*) | gegen Französisch (*Gymnasium, Rente, Figur*) |
| Karte | Frankreich, 96 Départements, 50 Orte | Spanien, Provinzen, 50 Orte | Italien, Provinzen/Regionen, 50 Orte | Deutschland (oder deutschsprachiger Raum), 50 Orte |
| Titel | Delikatessen (Éclair → Caviar) | Tapas-Reihe | Pasta-/Dolci-Reihe | [offen] |
| Geschichte | Le secret du Louvre | optional, später | optional, später | optional |
| Stimme | Mr. Alex (Klon, fr) + Julien für Aurélien | **Hörprobe zuerst** (Klon mit `language_code: es`); sonst Bibliotheksstimme für Sätze, Klon fürs Lob | **Hörprobe zuerst** (`it`) | Mr. Alex' Klon auf Deutsch (natürliche Muttersprache) |

Jedes Thema wie bisher: Vorschlag → Mr. Alex liest → OK → Audio → veröffentlichen.

## 4. Bauplan (jeder Schritt einzeln abzusegnen)

1. **Umbau** der App auf Sprachpaare mit Französisch als einzigem Paar, Pensum 3 + 8, Umschalter (noch mit einer Sprache), Offline pro Sprache, Adresse an der Wurzel, Name „Language Learning“. Danach Probe durch Mr. Alex.
2. **Spanisch:** fertig (13.10.): 9 Themen mit Notizen, 2 Dialoge mit Diego, Aussprache nur r/rr, Karte mit 52 Provinzen ab Sevilla, Geschichte « El secreto del Alcázar » Kapitel 1–3. Konzept: `docs/es-de/konzept.md`.
3. **Italienisch:** fertig (13.10.): 9 Themen mit Notizen, 2 Dialoge mit Giovanni (Andy), kein Aussprache-Teil, Karte mit 110 Provinzen ab Bologna, Geschichte « Il segreto della Torre » Kapitel 1–3. Konzept: `docs/it-de/konzept.md`.
4. **Deutsch (Hilfe FR):** fertig (13.10.): Oberfläche Französisch (Entscheidung Mr. Alex), 9 Themen mit eigenen deutschen Wendungen und französischen Notizen, Lob auf Deutsch, 2 Dialoge Alex/Aurélien (Julien spricht Deutsch), Karte mit 434 Kreisen ab Saarbrücken, Geschichte « Das Geheimnis der Völklinger Hütte » Kapitel 1–3, Aussprache « Die schweren Laute » (h, ich, ach, ei, ie). Konzept: `docs/de-fr/konzept.md`.
5. **Portugiesisch (Portugal):** gebaut ohne Audio (18.10.): 9 Themen mit Notizen, 2 Dialoge mit Tiago, Aussprache « Os sons nasais » (nasal gegen oral), Karte mit 18 Distrikten ab Lissabon, Açores und Madeira als Einschübe, Geschichte « O segredo da Regaleira » Kapitel 1–3. Audio nach dem 13.11. (Credits). Konzept: `docs/pt-de/konzept.md`.

## 5. Offen

- Punkte und Titel pro Sprache, Serie gemeinsam (so gebaut, 13.10.).
- Für Deutsch: Aurélien als Lernender – noch zu bestätigen.

## 6. Englisch (aufgeschoben)

Brainstorming und Rahmenfakten in `docs/en/brainstorming.md` (Kasten oben). Aufgeschoben am 15.10.2026; Beta-Fehler werden in `docs/beta-fehler.md` gesammelt.
