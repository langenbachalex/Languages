"""Gleicht die Lautheit aller Audios an (EBU R128, zwei Durchgänge mit ffmpeg loudnorm, lineare Verstärkung wo möglich).
Ziel: −18 LUFS, Spitzen höchstens −1,5 dBTP. Dateien, die schon innerhalb ±1 LU liegen, bleiben unverändert.
Aufruf:  python3 werkzeuge/lautstaerke.py [paar …]       (ohne Angabe: alle Sprachen)
         python3 werkzeuge/lautstaerke.py --messen [paar]   (nur messen)
audio.py ruft angleichen() für jede neu erzeugte Datei auf."""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ZIEL_I, ZIEL_TP, TOLERANZ = -18.0, -1.5, 1.0
APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")


def _json(text):
    return json.loads(text[text.rindex("{"):text.rindex("}") + 1])


def messen(pfad):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pfad, "-af",
                          f"loudnorm=I={ZIEL_I}:TP={ZIEL_TP}:LRA=20:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return _json(out)


def angleichen(pfad):
    """Gibt (alt, neu) in LUFS zurück, oder None, wenn nichts zu tun war."""
    if not shutil.which("ffmpeg"):
        return None
    m = messen(pfad)
    i = float(m["input_i"])
    if i == float("-inf") or i < -70 or abs(i - ZIEL_I) <= TOLERANZ:
        return None
    filt = (f"loudnorm=I={ZIEL_I}:TP={ZIEL_TP}:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    tmp = pfad + ".tmp.mp3"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", pfad, "-af", filt,
                    "-ar", "44100", "-ac", "1", "-b:a", "128k", tmp], check=True)
    os.replace(tmp, pfad)
    neu = float(messen(pfad)["input_i"])
    if neu < ZIEL_I - TOLERANZ:
        # Linear ging nicht weiter, weil die Spitzen die Grenze erreichen (typisch für Bibliotheksstimmen):
        # zweiter Durchgang mit Spitzenbegrenzung, danach sanft angehoben.
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", pfad, "-af",
                        f"alimiter=limit=0.7:level=false,loudnorm=I={ZIEL_I}:TP={ZIEL_TP}:LRA=20",
                        "-ar", "44100", "-ac", "1", "-b:a", "128k", tmp], check=True)
        os.replace(tmp, pfad)
        neu = float(messen(pfad)["input_i"])
    return i, neu


def dateien(paare):
    for paar in paare:
        for wurzel, _, namen in os.walk(os.path.join(APP, "audio", paar)):
            for n in sorted(namen):
                if n.endswith(".mp3"):
                    yield os.path.join(wurzel, n)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    paare = args or sorted(os.listdir(os.path.join(APP, "audio")))
    liste = list(dateien(paare))
    if "--messen" in sys.argv:
        werte = {}
        for p in liste:
            teil = os.path.relpath(p, os.path.join(APP, "audio")).split(os.sep)
            werte.setdefault(f"{teil[0]}/{teil[1]}", []).append(float(messen(p)["input_i"]))
        for k, v in sorted(werte.items()):
            v = [x for x in v if x > -70]
            print(f"{k:22} {len(v):4} Dateien · Mittel {sum(v)/len(v):6.1f} · min {min(v):6.1f} · max {max(v):6.1f} LUFS")
        return
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        ergebnisse = list(pool.map(angleichen, liste))
    geaendert = [e for e in ergebnisse if e]
    print(f"{len(liste)} Dateien geprüft, {len(geaendert)} angeglichen, {len(liste) - len(geaendert)} lagen schon im Ziel.")


if __name__ == "__main__":
    main()
