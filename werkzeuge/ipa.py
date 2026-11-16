"""Lautschrift (IPA) für Wendungen und Beispielsätze erzeugen (Mr. Alex, 15./16.11.2026).
Aufruf:  python3 werkzeuge/ipa.py es-de            füllt leere Spalten ipa_w / ipa in den Themen-TSV
         python3 werkzeuge/ipa.py es-de --zeigen   nur anzeigen, nichts schreiben
         python3 werkzeuge/ipa.py es-de --neu      alles neu erzeugen (überschreibt)
Ablauf: espeak-ng (apt-get install espeak-ng) → Sprachregeln unten → Korrekturen aus inhalte/<paar>/ipa_korrekturen.tsv
(Spalten: id, feld [w = Wendung, s = Satz], alt, neu – „alt“ muss in der erzeugten Fassung vorkommen). Danach durchsehen."""
import csv, importlib, os, re, subprocess, sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASIS, "werkzeuge", "sprachen"))
STIMME = {"fr": "fr", "es": "es", "it": "it"}
VOKALE = "aeiouɛɔəøœyɑɐɪʊɨæʌɒɜɞ"
# Silbenanlaut: diese Konsonantenfolgen bleiben vor dem Betonungsstrich zusammen (Spanisch/Italienisch)
ANLAUT = {"pr", "br", "tr", "dr", "kr", "ɡr", "fr", "pɾ", "bɾ", "tɾ", "dɾ", "kɾ", "ɡɾ", "fɾ", "βɾ", "ðɾ", "ɣɾ", "pl", "bl", "kl", "ɡl", "fl", "βl", "ɣl"}
EINHEIT = ["tʃ", "dʒ", "ts", "dz", "ʎ", "ɲ"]


def espeak(text, sprache):
    if " / " in text:   # Varianten « bien / mal »: einzeln sprechen, mit « / » verbinden (sonst liest espeak « barra »)
        teile = text.split(" / ")
        return " / ".join(re.sub(r"\s+", " ", espeak(t, sprache)).strip() for t in teile)
    t = text.replace("…", ",").replace("‿", " ")
    return subprocess.run(["espeak-ng", "-v", STIMME[sprache], "-q", "--ipa", t], capture_output=True, text=True).stdout


def betonung_vor_silbe(wort, sprache):
    """espeak setzt ˈ vor den Vokal; IPA verlangt ihn vor die Silbe: tˈaɾðe → ˈtaɾðe, korˈixo → koˈrixo."""
    while True:
        i = wort.find("ˈ")
        if i <= 0 or wort[i - 1] in VOKALE or wort[i - 1] in "ːˈ":
            return wort if i <= 0 or wort[i - 1] not in "ː" else wort
        # Konsonanten unmittelbar davor einsammeln (Digraphe als Einheit)
        j, teile = i, []
        while j > 0 and wort[j - 1] not in VOKALE and wort[j - 1] not in "ˈːˌ ̃":
            two = wort[j - 2:j] if j >= 2 else ""
            if two in EINHEIT: teile.insert(0, two); j -= 2
            else: teile.insert(0, wort[j - 1]); j -= 1
        if not teile:
            return wort
        k = 0
        while k < len(teile) and teile[-1 - k] in ("j", "w"): k += 1   # Gleitlaute gehören zur Silbe: kwˈanto → ˈkwanto
        rest = teile[:len(teile) - k]
        m = 2 if len(rest) >= 2 and (rest[-2] + rest[-1]) in ANLAUT else (1 if rest else 0)
        n = k + m
        if sprache == "it" and len(teile) > n and teile[-n - 1] in ("s", "z") and teile[-n - 1] != teile[-n]: n += 1   # s/z + Konsonant gehört zur nächsten Silbe: faˈstidjo, ˈzɡwardo
        start = i - len("".join(teile[-n:]))
        wort = wort[:start] + "ˈ" + wort[start:i] + wort[i + 1:]
        if wort.count("ˈ") and wort.find("ˈ") == start:   # nur der erste Strich je Wort wird verschoben
            return wort


def regeln(roh, sprache):
    t = re.sub(r"\s+", " ", roh.replace("\n", " ")).strip()
    t = t.replace("ˌ", "")
    if sprache == "fr":
        t = t.replace("ˈ", "").replace("ː", "").replace("-", "")
        t = re.sub(r"(?<![bpkɡtdfv][ʁl])y(?=[iɛeaøɑo])", "ɥ", t)
        t = t.replace("kœ̃ɡfy", "kuŋfu")
        return t
    t = t.replace("-", "")
    if sprache == "es":
        t = re.sub(r"(?<=[bdfɡklmnprstxθβðɣɾ])iˈ(?=[aeouɛɔ])", "jˈ", t)   # abrió: aβɾiˈo → aβɾjˈo
        t = re.sub(r"(?<=[bdfɡklmnprstxθβðɣɾ])uˈ(?=[aeioɛɔ])", "wˈ", t)   # luego, prueba
        t = re.sub(r"(?<=[bdfɡklmnprstxθβðɣɾ])u(?=[aeoɛɔ])", "w", t)        # croissant: kɾuaˈsan → kɾwaˈsan
        t = t.replace("ː", "").replace("oɪ", "oi").replace("aɪ", "ai").replace("eɪ", "ei").replace("aʊ", "au").replace("ɪ", "i").replace("ʊ", "u")
    if sprache == "it":
        t = t.replace("ɪ", "i").replace("ʊ", "u").replace("rɾ", "rr").replace("ɾ", "r")
        for lang, doppelt in (("tʃː", "ttʃ"), ("dʒː", "ddʒ"), ("tsː", "tts"), ("dzː", "ddz")): t = t.replace(lang, doppelt)
        t = re.sub(r"([bcdfɡklmnprstvzʃʎɲ])ː", r"\1\1", t)   # Doppelkonsonant: tː → tt
        t = t.replace("ː", "")
        t = re.sub(r"(?<=[bcdfɡklmnprstvzʃʎɲ])iˈ(?=[aeiouɛɔ])", "jˈ", t)   # lezione: tsiˈone → tsjˈone
        t = re.sub(r"(?<=[bcdfɡklmnprstvzʃʎɲ])uˈ(?=[aeiouɛɔ])", "wˈ", t)   # cuore: kuˈɔre → kwˈɔre
        t = re.sub(r"(?<=[bcdfɡklmnprstvz])u(?=[oɔ])", "w", t)   # buongiorno, suonare
    if sprache == "es":
        t = t.replace("ɛ", "e").replace("ɔ", "o")
    woerter = []
    for w in t.split(" "):
        w = betonung_vor_silbe(w, sprache)
        if sprache in ("it", "es") and len(w) >= 5:
            m = re.search(r"([bcdfɡklmnprstvzʃʎɲɾβðɣθx])i([aeoɛɔ])$", w)
            if m and not w[:m.start()].endswith("ˈ") and "ˈ" + m.group(1) + "i" not in w: w = w[:m.start()] + m.group(1) + "j" + m.group(2)
        gruppen = re.findall(f"[{VOKALE}]+", w.replace("ˈ", ""))
        hiatus = len(gruppen) == 1 and len(gruppen[0]) >= 2 and gruppen[0][0] in "iu" and ("ˈ" + gruppen[0]) in w   # frío, día: zweisilbig
        if len(gruppen) <= 1 and not hiatus: w = w.replace("ˈ", "")   # Einsilber ohne Betonungsstrich
        woerter.append(w)
    t = " ".join(woerter)
    if sprache == "it":
        t = t.replace("lɔop", "lup").replace("ˈfantazi", "ˈfɛntazi").replace("bwonˈdʒɔrno", "bwɔnˈdʒorno")
        t = t.replace("sta ˈsera", "staˈsera").replace("sta matˈtina", "stamatˈtina").replace("kuŋɡ fu", "kuŋ fu")
    if sprache == "es":
        t = t.replace("ˈkuŋfˈu", "ˈkuŋfu").replace("kuŋfˈu", "ˈkuŋfu")
        t = re.sub(r"(\S*?)ˈ(\S*?)mˈente", r"\1ˌ\2ˈmente", t)
        t = re.sub(r"(?<=\s)rie(?=\s|$)", "ˈrie", t)   # ríe   # actualmente: Nebenbetonung + Hauptbetonung auf -mente
    return t


def main():
    paar = sys.argv[1]
    zeigen, neu = "--zeigen" in sys.argv, "--neu" in sys.argv
    P = importlib.import_module(paar.replace("-", "_"))
    sprache = P.LANG
    korr = {}
    kp = os.path.join(BASIS, "inhalte", paar, "ipa_korrekturen.tsv")
    if os.path.exists(kp):
        for z in csv.DictReader(open(kp, encoding="utf-8"), delimiter="\t"):
            korr.setdefault((z["id"], z["feld"]), []).append((z["alt"], z["neu"]))
    n = 0
    for th in P.THEMEN:
        p = os.path.join(BASIS, "inhalte", paar, th["datei"])
        zeilen = list(csv.reader(open(p, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
        kopf = zeilen[0]
        if "ipa_w" not in kopf: kopf += ["ipa_w", "ipa"]
        iw, ip, iwend, isatz = kopf.index("ipa_w"), kopf.index("ipa"), kopf.index("wendung"), kopf.index("satz_fr")
        for z in zeilen[1:]:
            while len(z) < len(kopf): z.append("")
            for idx, quelle, feld in ((iw, iwend, "w"), (ip, isatz, "s")):
                if z[idx] and not neu: continue
                t = regeln(espeak(z[quelle], sprache), sprache)
                for alt, ersatz in korr.get((z[0], feld), []):
                    if alt not in t: sys.exit(f"Korrektur passt nicht: {z[0]} {feld}: « {alt} » nicht in « {t} »")
                    t = t.replace(alt, ersatz)
                z[idx] = t; n += 1
            if zeigen: print(z[0], z[iwend], "→", z[iw], "|", z[isatz], "→", z[ip])
        if not zeigen:
            with open(p, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\").writerows(zeilen)
    print(f"{paar}: {n} Felder {'angezeigt' if zeigen else 'geschrieben'}")


if __name__ == "__main__":
    main()
