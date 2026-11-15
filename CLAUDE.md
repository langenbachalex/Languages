# Hinweise für Claude (Projekt Languages, Mr. Alex)

## Agent Skills
Agent Skills nutzen (Plugin `agent-skills` von Addy Osmani, eingetragen in `.claude/settings.json`), aber die Regeln von Mr. Alex haben Vorrang.

## Regeln von Mr. Alex
- **Erst Vorschlag, dann OK, dann Bau:** Inhalte und größere Änderungen zuerst im Chat vorschlagen; gebaut, aufgenommen und veröffentlicht wird nach seinem OK.
- **Veröffentlichen:** auf Branch `bugfix` arbeiten, dann `bugfix` in `main` mergen und beide pushen (GitHub Pages liest `main`). Commits mit `-c user.name="Alex Langenbach" -c user.email="langenbachalex@gmail.com"`.
- **Audio kostet Credits:** Aufnahmen (`werkzeuge/audio.py`) nur nach ausdrücklichem OK.
- **Fehler sammeln:** neue Fehler nur in `docs/beta-fehler.md` eintragen; ab 5 offenen behebbaren Einträgen fragen, ob sie gebündelt behoben werden.
- **Antworten kurz**, Ergebnis zuerst; vor dem Pushen bauen (`python3 werkzeuge/bauen.py`) und die betroffenen Teile im Browser prüfen.

## Aufbau
App in `app/` (wird von `werkzeuge/bauen.py` erzeugt), Sprachpakete in `werkzeuge/sprachen/<paar>.py`, Inhalte in `inhalte/<paar>/`, Konzepte in `docs/`.
