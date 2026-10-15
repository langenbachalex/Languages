"""Audios für alle Sprachpaare (ElevenLabs). Stimmen stehen im Sprachpaket (werkzeuge/sprachen/<paar>.py).
Vorhandene Dateien bleiben erhalten (eigene Aufnahmen auch).
Aufruf:  python3 werkzeuge/audio.py --zaehlen          (nur Zeichen zählen, keine Credits)
         python3 werkzeuge/audio.py [paar]             (erzeugen, danach bauen.py)
"""
import json, os, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bauen


def sprechtext(P, t):
    """Schreibweise nur fürs Vorlesen anpassen (ganze Wörter, Groß-/Kleinschreibung bleibt beim Ersatz wie angegeben)."""
    import re
    for a, b in P.AUSSPRACHE_KORREKTUR.items():
        if a.isalnum() or " " in a:
            t = re.sub(rf"(?<![\w'’]){re.escape(a)}(?![\w'’])", b, t)
        else:
            t = t.replace(a, b)
    return t


def auftraege(P):
    """(Pfad relativ zu app/, Text, Stimme) – Stimme „a“ = Mr. Alex, „b“ = Gesprächspartner."""
    inhalte, paar, liste = os.path.join(bauen.BASIS, "inhalte", P.PAAR), P.PAAR, []
    s = lambda t: sprechtext(P, t)
    for t in P.THEMEN:
        for z in bauen.tsv(inhalte, t["datei"]):
            wid = z["id"]
            liste.append((f"audio/{paar}/wendungen/{wid}.mp3", s(z["wendung"]), "a"))
            liste.append((f"audio/{paar}/saetze/{wid}.mp3", s(z["satz_fr"]), "a"))
            if z["passe_compose"]:
                liste.append((f"audio/{paar}/saetze/{wid}_pc.mp3", s(z["passe_compose"]), "a"))
                liste.append((f"audio/{paar}/saetze/{wid}_fp.mp3", s(z["futur_proche"]), "a"))
    for z in bauen.tsv(inhalte, "dialoge.tsv"):
        liste.append((f"audio/{paar}/dialoge/{z['id']}.mp3", s(z["fr"]), "a" if z["rolle"] == "A" else "b"))
    for z in (bauen.tsv(inhalte, P.AUSSPRACHE["datei"]) if P.AUSSPRACHE else []):
        liste.append((f"audio/{paar}/{P.AUSSPRACHE['id']}/{z['id']}.mp3", s(bauen.rein(z["wort"])), "a"))
    for z in bauen.tsv(inhalte, "geschichte.tsv"):
        liste.append((f"audio/{paar}/geschichte/k{int(z['kapitel']):02d}_{int(z['nr']):02d}.mp3", s(z["fr"].replace("**", "")), "a"))
    for z in bauen.tsv(inhalte, "orte.tsv"):
        liste.append((f"audio/{paar}/orte/{z['id']}.mp3", s(f"{z['name']}. {z['fakt_fr']}"), "a"))
    for z in bauen.tsv(inhalte, "lob.tsv"):
        liste.append((f"audio/{paar}/lob/{z['id']}.mp3", z["text"], "a"))
    for k, t in P.SPIEL_TEXTE.items():
        liste.append((f"audio/{paar}/spiel/{k}.mp3", t, "a"))
    for i, (_, name, _) in enumerate(P.TITEL):
        if i:
            liste.append((f"audio/{paar}/spiel/titel_{i}.mp3", P.TITEL_ANSAGE.format(name=name), "a"))
    return liste


def erzeugen(P, pfad, text, stimme):
    st = P.STIMME if stimme == "a" else P.STIMME_B
    if not st:
        return None
    body = {"text": text, "model_id": st["modell"], "voice_settings": st["einstellungen"]}
    if st.get("language_code"):
        body["language_code"] = st["language_code"]
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{st['id']}?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        daten = r.read()
    ziel = os.path.join(bauen.APP, pfad)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "wb") as f:
        f.write(daten)
    import lautstaerke
    lautstaerke.angleichen(ziel)   # gleiche Lautheit für alle Stimmen (−18 LUFS)
    return ziel


def main():
    nur = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name in bauen.PAKETE:
        P = bauen.paket(name)
        if nur and P.PAAR not in nur:
            continue
        offen = [a for a in auftraege(P) if not os.path.exists(os.path.join(bauen.APP, a[0]))]
        offen = [a for a in offen if a[2] == "a" or P.STIMME_B]
        print(P.PAAR + ":", len(offen), "Audios fehlen,", sum(len(a[1]) for a in offen), "Zeichen")
        if "--zaehlen" in sys.argv:
            continue
        neu = fehler = 0
        for pfad, text, stimme in offen:
            try:
                erzeugen(P, pfad, text, stimme); neu += 1
            except urllib.error.HTTPError as e:
                fehler += 1
                print("FEHLER:", pfad, e.code, e.read()[:200])
                if e.code in (401, 402, 429):
                    break
        print(P.PAAR + ":", neu, "neu,", fehler, "Fehler")


if __name__ == "__main__":
    main()
