# Konzept: „Language Learning“ – eine App, mehrere Sprachen

Stand: 13.10.2026. **Schritt 1 (Umbau) gebaut und veröffentlicht am 13.10.:** Sprachpakete, Umschalter, Pensum 3 + 8, Offline pro Sprache, App an der Wurzel, Name „Language Learning“, alter Stand wird automatisch übernommen. Figuren: Diego (Spanisch), Giovanni (Italienisch), Aurélien lernt Deutsch (Vorschlag). Grundlage: Brainstorming mit Mr. Alex (13.10.).
Grundsatz wie bisher: vor jedem Bauschritt fragen.

## 1. Festgelegt (Mr. Alex, 13.10.)

- **Eine App, ein Umschalter** für die Sprachen; keine App pro Sprache. Neue Sprachen sollen sich bequem ergänzen lassen.
- **Sprachen:** zuerst Umbau mit Französisch, dann **Spanisch**, dann **Italienisch**, außerdem **Deutsch umgedreht** (Ziel Deutsch, Hilfe Französisch) mit **eigenen deutschen Redewendungen**, nicht aus den französischen Daten gespiegelt.
- **Pensum:** **3 neue + 8 alte pro Tag, pro Sprache** (bestätigt 13.10.).
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

| | Französisch (fertig) | Spanisch (fertig) | Italienisch (fertig) | Deutsch (Hilfe FR) |
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
4. **Deutsch (Hilfe FR):** eigene Wendungen, Oberfläche und Lob auf Deutsch mit französischer Hilfe.

## 5. Offen

- Punkte und Titel pro Sprache, Serie gemeinsam (so gebaut, 13.10.).
- Für Deutsch: Aurélien als Lernender – noch zu bestätigen.
