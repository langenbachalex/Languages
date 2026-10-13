# Languages – persönliche Sprach-Apps von Mr. Alex

Privat, getrennt von den Schul-Apps (Repository `School`). Weitere Sprachen folgen nach demselben Muster.

| Sprache | App | Inhalte | Skripte | Konzept |
|---|---|---|---|---|
| Französisch · „Mon français“ | `app/francais/` → https://langenbachalex.github.io/Languages/francais/ | `inhalte/francais/` | `werkzeuge/francais_bauen.py`, `werkzeuge/francais_audio.py` | `docs/francais/konzept.md` |

**Bauen:** `python3 werkzeuge/francais_bauen.py` (daten.js, Icons, Manifest, sw.js). **Audio:** `python3 werkzeuge/francais_audio.py --zaehlen` zählt, ohne `--zaehlen` erzeugt es fehlende Dateien (ElevenLabs, nur nach Absprache).
**Veröffentlichen:** Jeder Push auf `main`, der `app/` ändert, veröffentlicht über `.github/workflows/pages.yml`.
**Grundsatz:** Vor jedem Bauschritt wird Mr. Alex gefragt. Startnotiz: `docs/francais/start.md`.
