# Hinweise für Claude (Projekt Languages, Mr. Alex)

## Agent Skills
Agent Skills nutzen (Plugin `agent-skills` von Addy Osmani, eingetragen in `.claude/settings.json`), aber die Regeln von Mr. Alex haben Vorrang.

## Regeln von Mr. Alex
- **Erst Vorschlag, dann OK, dann Bau:** Inhalte und größere Änderungen zuerst im Chat vorschlagen; gebaut, aufgenommen und veröffentlicht wird nach seinem OK.
- **Veröffentlichen:** auf Branch `bugfix` arbeiten, dann `bugfix` in `main` mergen und beide pushen (GitHub Pages liest `main`). Commits mit `-c user.name="Alex Langenbach" -c user.email="langenbachalex@gmail.com"`.
- **Audio kostet Credits:** Aufnahmen (`werkzeuge/audio.py`) nur nach ausdrücklichem OK.
- **Fehler sammeln:** neue Fehler nur in `docs/beta-fehler.md` eintragen; ab 5 offenen behebbaren Einträgen fragen, ob sie gebündelt behoben werden.
- **Antworten kurz**, Ergebnis zuerst; vor dem Pushen bauen (`python3 werkzeuge/bauen.py`) und die betroffenen Teile im Browser prüfen.

## Testprogramm
`node werkzeuge/testprogramm.js` (vorher `python3 werkzeuge/bauen.py`): Lernkern-Tests, Offline-Liste, alle Sprachen laden ohne Fehler, Hauptwege (Séance, Memory, Thema-Teil, Dialog, Sammlung/Karte, Power Up), drei Formate (Laptop 1366×768, Handy 360×740, iPad 820×1180, nur Chromium), English-Ausgabe. Schalter: `--nur=fr-de`, `--format=handy`, `--schnell`. Ausgabe „ALLES OK“ oder Fehlerliste.
1. **Fehler → zuerst ein Test:** erst eine Prüfung ins Testprogramm, die den Fehler zeigt (rot), dann reparieren (grün).
2. **Fertig heißt grün:** fertig erst bei „ALLES OK“; sonst mit der Ausgabe melden.
3. **Nach jedem Bau läuft es** (bei kleinen Änderungen nur der betroffene Teil).

## Lernkern
`app/lernkern.js` ist der gemeinsame Kern für alle Apps (Kasten, Prüfregeln, Wiederholungen, Power Up, Tippen vergleichen). Master ist hier; Regeländerungen nur dort, mit Test in `werkzeuge/lernkern_test.js`, Version erhöhen, Zeile in `docs/systeme.md`.

## Systeme über alle Apps
`docs/systeme.md` zeigt, welches System (Word Gym, Power Up, …) in welcher App steckt (EN6, EN9, FR in `langenbachalex/School`, LANG hier). Wer ein System baut oder ändert, trägt es dort ein. Die wöchentliche Aufgabe « Systeme School → Languages » liest neue School-Commits und fragt, was übernommen wird.

## Aufbau
App in `app/` (wird von `werkzeuge/bauen.py` erzeugt), Sprachpakete in `werkzeuge/sprachen/<paar>.py`, Inhalte in `inhalte/<paar>/`, Konzepte in `docs/`.
