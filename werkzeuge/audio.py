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
            t = re.sub(rf"(?<![\w'’]){re.escape(a)}(?!\w)", b, t)   # Genitiv-Apostroph danach erlaubt („Sauron's“)
        else:
            t = t.replace(a, b)
    return t


def auftraege(P):
    """(Pfad relativ zu app/, Text, Stimme) – Stimme „a“ = Mr. Alex, „b“ = Gesprächspartner."""
    inhalte, paar, liste = os.path.join(bauen.BASIS, "inhalte", P.PAAR), P.PAAR, []
    s = lambda t: sprechtext(P, t)
    # Erzähler: alles außer Dialogen („a“ = Mr. Alex, „b“ = zweite Stimme). Englisch: Simon erzählt, Mr. Alex spricht nur Barangollach im Dialog.
    n = getattr(P, "ERZAEHLER", "a")
    lob = getattr(P, "LOB_STIMME", n)
    for t in P.THEMEN:
        for z in bauen.tsv(inhalte, t["datei"]):
            wid = z["id"]
            im_traeger = z["wendung"] in getattr(P, "WENDUNG_IM_TRAEGERSATZ", set())   # kippt allein in eine andere Sprache
            liste.append((f"audio/{paar}/wendungen/{wid}.mp3", s(getattr(P, "WENDUNG_KORREKTUR", {}).get(z["wendung"], z["wendung"])), ("w" + n) if im_traeger else n))
            liste.append((f"audio/{paar}/saetze/{wid}.mp3", s(getattr(P, "SATZ_KORREKTUR", {}).get(z["satz_fr"], z["satz_fr"])), n))
            if z["passe_compose"]:
                liste.append((f"audio/{paar}/saetze/{wid}_pc.mp3", s(z["passe_compose"]), n))
                liste.append((f"audio/{paar}/saetze/{wid}_fp.mp3", s(z["futur_proche"]), n))
            if (z.get("syrisch") or "").strip():   # Arabisch: syrische Variante, Stimme „s“ (STIMME_S)
                liste.append((f"audio/{paar}/syrisch/{wid}.mp3", z["syrisch"], "s"))
    for z in bauen.tsv(inhalte, "dialoge.tsv"):
        liste.append((f"audio/{paar}/dialoge/{z['id']}.mp3", s(z["fr"]), "a" if z["rolle"] == "A" else "b"))
    for A in bauen.aussprache_module(P):
        for z in bauen.tsv(inhalte, A["datei"]):
            liste.append((f"audio/{paar}/{A['id']}/{z['id']}.mp3", s(bauen.rein(z["wort"])), "w" + n))
    SCH = getattr(P, "SCHRIFT", None)
    for z in (bauen.tsv(inhalte, SCH["datei"]) if SCH else []):   # Arabisch: Buchstabenname und Beispielwort, je im Trägersatz
        liste.append((f"audio/{paar}/huruf/{z['id']}.mp3", s(z["name"]), "w" + n))
        liste.append((f"audio/{paar}/huruf/{z['id']}_w.mp3", s(z["beispiel"]), "w" + n))
    for z in bauen.tsv(inhalte, "geschichte.tsv"):
        liste.append((f"audio/{paar}/geschichte/k{int(z['kapitel']):02d}_{int(z['nr']):02d}.mp3", s(z["fr"].replace("**", "")), n))
    AN = getattr(P, "ANEKDOTEN", None)
    for z in (bauen.tsv(inhalte, AN["datei"]) if AN else []):
        liste.append((f"audio/{paar}/anekdoten/a{int(z['nr']):02d}_{int(z['satz']):02d}.mp3", s(z["fr"].replace("**", "")), n))
        if (z.get("syrisch") or "").strip():
            liste.append((f"audio/{paar}/anekdoten/a{int(z['nr']):02d}_{int(z['satz']):02d}_s.mp3", z["syrisch"], "s"))
    for z in bauen.tsv(inhalte, "orte.tsv"):
        liste.append((f"audio/{paar}/orte/{z['id']}.mp3", s(f"{z['name']}. {z['fakt_fr']}"), n))
    for z in bauen.tsv(inhalte, "lob.tsv"):
        liste.append((f"audio/{paar}/lob/{z['id']}.mp3", s(z["text"]), lob))
    for k, t in P.SPIEL_TEXTE.items():
        liste.append((f"audio/{paar}/spiel/{k}.mp3", s(t), n))
    for i, (_, name, _) in enumerate(P.TITEL):
        if i:
            liste.append((f"audio/{paar}/spiel/titel_{i}.mp3", s(P.TITEL_ANSAGE.format(name=name)), n))
    return liste


def vorspann_schneiden(pfad):
    """Trägersatz entfernen: Schnitt an der letzten Pause vor dem Wort (ffmpeg silencedetect). Gibt die Schnittstelle zurück."""
    import re, shutil, subprocess
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg fehlt – Einzelwörter brauchen den Schnitt")
    out = subprocess.run(["ffmpeg", "-i", pfad, "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    dauer = 60 * float(m.group(2)) + float(m.group(3))
    # Alle Pausen im Fenster der letzten 2,8 s; Schnitt an der längsten (die Pause am Doppelpunkt des Trägersatzes),
    # nicht an der letzten: Verschlusslaute im Wort (« qalb », Mr. Alex 18.10.) sind kurze Stillen und wurden als Schnittstelle genommen.
    pausen = [(float(e), float(d)) for e, d in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", out) if float(e) < dauer - 0.25]
    im_fenster = [p for p in pausen if dauer - p[0] <= 2.8]
    if not im_fenster:   # Einzelwort oder kurze Wendung nach der Pause
        raise RuntimeError(f"keine Pause vor dem Wort gefunden: {pfad} ({pausen}, {dauer:.2f}s)")
    ab = max(max(im_fenster, key=lambda p: p[1])[0] - 0.06, 0)
    tmp = pfad + ".schnitt.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", pfad, "-ss", f"{ab:.3f}", "-af", "afade=t=in:d=0.02", "-c:a", "libmp3lame", "-b:a", "128k", tmp], check=True)
    os.replace(tmp, pfad)
    return ab


def erzeugen(P, pfad, text, stimme):
    """stimme: „a“ Mr. Alex, „b“ zweite Stimme, „wa“/„wb“ Einzelwort – im Trägersatz gesprochen, danach geschnitten,
    damit die Stimme bei nackten Wörtern nicht in eine andere Sprache kippt."""
    st = P.STIMME_B if stimme.endswith("b") else getattr(P, "STIMME_S", None) if stimme.endswith("s") else P.STIMME
    if not st:
        return None
    wort = stimme.startswith("w")
    if wort:
        text = getattr(P, "TRAEGERSATZ", "{wort}.").format(wort=text)
    body = {"text": text, "model_id": st["modell"], "voice_settings": st["einstellungen"]}
    if st.get("language_code"):
        body["language_code"] = st["language_code"]
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{st['id']}?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        daten = r.read()
    ziel = os.path.join(bauen.wurzel(P), pfad)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "wb") as f:
        f.write(daten)
    if wort:
        vorspann_schneiden(ziel)
    import lautstaerke
    lautstaerke.angleichen(ziel)   # gleiche Lautheit für alle Stimmen (−18 LUFS)
    return ziel


def main():
    nur = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name in [n for a in bauen.AUSGABEN for n in a["pakete"]]:
        P = bauen.paket(name)
        if nur and P.PAAR not in nur:
            continue
        offen = [a for a in auftraege(P) if not os.path.exists(os.path.join(bauen.wurzel(P), a[0]))]
        offen = [a for a in offen if not a[2].endswith("b") or P.STIMME_B]
        offen = [a for a in offen if not a[2].endswith("s") or getattr(P, "STIMME_S", None)]
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
