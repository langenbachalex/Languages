# Languages – „Language Learning“, die persönliche Sprach-App von Mr. Alex

Eine App, mehrere Sprachpaare (Zielsprache + Hilfssprache), Umschalter oben. Privat, getrennt von den Schul-Apps (Repository `School`).
**App:** https://langenbachalex.github.io/Languages/ · **Konzept:** `docs/konzept-mehrsprachig.md` · **Grundsatz:** vor jedem Bauschritt wird Mr. Alex gefragt.

| Paar | Sprache | Sprachpaket | Inhalte | Audio | Konzept |
|---|---|---|---|---|---|
| `fr-de` | Französisch, Hilfe Deutsch – „Mon français“ | `werkzeuge/sprachen/fr_de.py` | `inhalte/fr-de/` | `app/audio/fr-de/` | `docs/fr-de/konzept.md` |
| `es-de` | Spanisch (geplant, Partner: Diego) | | | | |
| `it-de` | Italienisch (geplant, Partner: Giovanni) | | | | |
| `de-fr` | Deutsch, Hilfe Französisch (geplant, eigene deutsche Redewendungen) | | | | |

**Neue Sprache:** Sprachpaket `werkzeuge/sprachen/<paar>.py` (Themen, Oberflächentexte, Titel, optionaler Aussprache-Teil (`AUSSPRACHE = None` zum Weglassen), Rollen, Karte, Stimmen), Ordner `inhalte/<paar>/` mit denselben TSV-Dateien wie `fr-de`, Eintrag in `PAKETE` in `werkzeuge/bauen.py`.
**Bauen:** `python3 werkzeuge/bauen.py` (je Paar `app/daten_<paar>.js`, dazu `index.html`, Manifest, Icons, `sw.js`).
**Audio:** `python3 werkzeuge/audio.py --zaehlen` zählt, `python3 werkzeuge/audio.py [paar]` erzeugt fehlende Dateien (ElevenLabs, nur nach Absprache).
**Veröffentlichen:** Jeder Push auf `main`, der `app/` ändert, veröffentlicht über `.github/workflows/pages.yml`.
**Offline:** Code und Daten werden vorab geladen; Audio pro Sprache über „Hors-ligne“ in der Sammlung (oder nach und nach beim Abspielen).
**Fortschritt:** nur im Browser des Geräts (`localStorage`, Schlüssel `languages-v1`); pro Sprache Kasten, Teile, Punkte, Titel – gemeinsam die Serie.
