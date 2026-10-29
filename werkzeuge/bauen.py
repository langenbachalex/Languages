"""Baut die App „Language Learning“ in app/: je Sprachpaar eine Datendatei (daten_<paar>.js), dazu index.html, Manifest, Icons, sw.js.
Sprachpakete: werkzeuge/sprachen/<paar>.py (Themen, Oberflächentexte, Titel …), Inhalte: inhalte/<paar>/*.tsv, Audio: app/audio/<paar>/.
Aufruf: python3 werkzeuge/bauen.py        Konzept: docs/konzept-mehrsprachig.md
TSV-Felder heißen in allen Paketen gleich: fr = Zielsprache, de = Hilfssprache (historisch aus dem ersten Paar fr-de)."""
import csv, hashlib, importlib, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprachen"))
BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(BASIS, "app")
SCHRIFT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAKETE = ["fr_de", "es_de", "it_de", "pt_de", "de_fr", "tr_de", "ar_de"]   # Reihenfolge = Reihenfolge im Umschalter
# Ausgaben: je eine eigenständige Web-App (eigener Ordner, Speicher, Offline-Speicher). Englisch läuft getrennt unter app/english/,
# teilt aber Code, Werkzeuge und Audio-Pipeline (Entscheidung Mr. Alex 16.10., docs/en/brainstorming.md).
AUSGABEN = [
    {"ordner": "", "pakete": PAKETE, "name": "Language Learning", "kurz": "Languages", "speicher": "languages-v1", "alt": "francais-v1",
     "praefix": "ll", "lang": "fr", "farbe": "#0a2a6b", "hintergrund": "#f4f6fb", "icon": ("LL", (10, 42, 107))},
    {"ordner": "english", "pakete": ["en_de"], "name": "English – Word Gym", "kurz": "English", "speicher": "english-v1", "alt": None,
     "praefix": "en", "lang": "en", "farbe": "#1f4e3d", "hintergrund": "#f4f6fb", "icon": ("EN", (31, 78, 61))},
]
AUDIO_STAND = 2   # erhöhen, wenn vorhandene Audiodateien ersetzt wurden (Browser verwirft dann den Audio-Speicher)
# Tagespensum: höchstens 8 Wiederholungen; neue Wendungen pro Sprache einstellbar 1–5, Voreinstellung 1 (Mr. Alex, 29.10.; vorher fest 3)
PENSUM = {"neu": 1, "neu_max": 5, "wiederholung": 8}
# Leitner-Stufen: nach so vielen Tagen kommt eine Wendung wieder (Stufe 0 = neu / vergessen)
INTERVALLE = [1, 3, 7, 14, 30, 60, 120]


def paket(name):
    return importlib.import_module(name)


def ausgabe_von(P):
    """Die Ausgabe (Web-App), zu der ein Sprachpaket gehört."""
    name = P.__name__.rsplit(".", 1)[-1]
    return next(a for a in AUSGABEN if name in a["pakete"])


def wurzel(P):
    """Ordner der Web-App, in der dieses Paket liegt (Daten, Audio, Icons)."""
    return os.path.join(APP, ausgabe_von(P)["ordner"])


def tsv(inhalte, name):
    with open(os.path.join(inhalte, name), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def rein(markup):
    """comm{an|en}ç{on|on}s → commençons"""
    return re.sub(r"\{[^|{}]+\|([^}]*)\}", r"\1", markup)


def audio_pruefer(P):
    """Pfad relativ zur Web-App, nur wenn die Datei existiert (sonst Sprachausgabe des Geräts)."""
    paar, basis = P.PAAR, wurzel(P)
    def audio(rel):
        pfad = f"audio/{paar}/{rel}"
        voll = os.path.join(basis, pfad)
        if not os.path.exists(voll):
            return None
        with open(voll, "rb") as f:
            pruef = hashlib.md5(f.read()).hexdigest()[:8]
        return f"{pfad}?v={pruef}"   # ersetzte Datei = neue Adresse = der Browser lädt sie neu (sw.js vergleicht Audio mit Suchteil)
    return audio


def aussprache_module(P):
    """P.AUSSPRACHE: None, ein Modul (dict) oder eine Liste von Modulen."""
    A = getattr(P, "AUSSPRACHE", None)
    return [] if not A else (A if isinstance(A, list) else [A])


def daten_fuer(P):
    paar, inhalte, audio = P.PAAR, os.path.join(BASIS, "inhalte", P.PAAR), audio_pruefer(P)
    wendungen, themen = [], []
    for t in P.THEMEN:
        ids = []
        for z in tsv(inhalte, t["datei"]):
            wid = z["id"]
            assert wid not in [w["id"] for w in wendungen], f"{paar} doppelte ID {wid}"
            assert z["luecke"] in z["satz_fr"], f"{paar} {wid}: Lücke „{z['luecke']}“ steht nicht im Satz"
            assert bool(z["passe_compose"]) == bool(z["futur_proche"]), f"{paar} {wid}: Zeitmaschine braucht beide Zeiten"
            leer = lambda k: (z.get(k) or "").strip() or None
            w = {"id": wid, "thema": t["id"], "fr": z["wendung"], "de": z["deutsch"], "register": z["register"] or "tu",
                 "anker": z["anker"], "notiz": leer("notiz"), "audio": audio(f"wendungen/{wid}.mp3"),
                 "gloss": leer("gloss_w"),   # Interlinear-Glosse der Wendung (Türkisch, Arabisch)
                 "umschrift": leer("umschrift_w"), "wurzel": leer("wurzel"),   # Arabisch: Umschrift und Wurzel (ك-ت-ب)
                 "satz": {"fr": z["satz_fr"], "de": z["satz_de"], "luecke": z["luecke"], "gloss": leer("gloss"), "umschrift": leer("umschrift"), "audio": audio(f"saetze/{wid}.mp3")},
                 "zeit": None, "syrisch": None}
            if leer("syrisch"):   # Arabisch: die syrische Variante der Wendung (Knopf « Şām », syrische Stimme)
                w["syrisch"] = {"fr": z["syrisch"], "umschrift": leer("syrisch_u"), "audio": audio(f"syrisch/{wid}.mp3")}
            if z["passe_compose"]:
                w["zeit"] = {"pc": {"fr": z["passe_compose"], "umschrift": leer("umschrift_pc"), "audio": audio(f"saetze/{wid}_pc.mp3")},
                             "fp": {"fr": z["futur_proche"], "umschrift": leer("umschrift_fp"), "audio": audio(f"saetze/{wid}_fp.mp3")}}
            wendungen.append(w)
            ids.append(wid)
        themen.append({"id": t["id"], "name": t["name"], "de": t["de"], "symbol": t["symbol"], "wendungen": ids})
    dialoge = []
    for z in tsv(inhalte, "dialoge.tsv"):
        if not dialoge or dialoge[-1]["id"] != z["dialog"]:
            dialoge.append({"id": z["dialog"], "titel": z["titel"], "ort": z["ort"], "zeilen": []})
        dialoge[-1]["zeilen"].append({"id": z["id"], "rolle": z["rolle"], "fr": z["fr"], "de": z["de"], "umschrift": (z.get("umschrift") or "").strip() or None, "audio": audio(f"dialoge/{z['id']}.mp3")})
    # Aussprache: ein Modul (Französisch, Spanisch) oder mehrere (Arabisch) – Laute, Minimalpaare, beide Laute in einem Wort (Markup {laut|buchstaben})
    aussprachen = []
    for A in aussprache_module(P):
        modul = {"id": A["id"], "symbol": A["symbol"], "titel": A["titel"], "unter": A["unter"], "info": A["klaenge"], "reihe": A["reihe"],
                 "paare_gruppen": A["paare"], "beide_name": A["beide_name"], "texte": A["texte"], "klaenge": {}, "paare": [], "beide": []}
        zeilen = tsv(inhalte, A["datei"])
        def wort(z):
            return {"id": z["id"], "wort": rein(z["wort"]), "de": z["de"], "klang": z["klang"], "umschrift": (z.get("umschrift") or "").strip() or None,
                    "syrien": (z.get("syrien") or "").strip() or None, "audio": audio(f"{A['id']}/{z['id']}.mp3")}
        for z in zeilen:
            eintrag = wort(z)
            if z["teil"] == "klang":
                modul["klaenge"].setdefault(z["klang"], []).append(eintrag)
            elif z["teil"] == "paar" and z["id"].endswith("a"):
                b = next(x for x in zeilen if x["id"] == z["partner"])
                eintrag["gruppe"] = z["id"].split("_")[0]
                eintrag["b"] = wort(b)
                modul["paare"].append(eintrag)
            elif z["teil"] == "beide":
                eintrag["markup"] = z["wort"]; eintrag["klaenge"] = z["klang"].split(",")
                modul["beide"].append(eintrag)
        aussprachen.append(modul)
    aussprache = aussprachen[0] if aussprachen else {"id": "", "symbol": "", "titel": "", "unter": "", "info": {}, "reihe": [], "paare_gruppen": [], "beide_name": "", "texte": {}, "klaenge": {}, "paare": [], "beide": []}
    geschichte = []
    for z in tsv(inhalte, "geschichte.tsv"):
        if not geschichte or geschichte[-1]["nr"] != int(z["kapitel"]):
            geschichte.append({"nr": int(z["kapitel"]), "titel": z["titel"], "absaetze": []})
        aid = f"k{int(z['kapitel']):02d}_{int(z['nr']):02d}"
        geschichte[-1]["absaetze"].append({"id": aid, "fr": z["fr"], "de": z["de"], "umschrift": (z.get("umschrift") or "").strip() or None, "audio": audio(f"geschichte/{aid}.mp3")})
    # Anekdoten (Nasreddin Hoca, Dschuha): kurze Texte wie Kapitel, frei je fertigem Thema
    anekdoten, AN = [], getattr(P, "ANEKDOTEN", None)
    for z in (tsv(inhalte, AN["datei"]) if AN else []):
        if not anekdoten or anekdoten[-1]["nr"] != int(z["nr"]):
            anekdoten.append({"nr": int(z["nr"]), "titel": z["titel"], "absaetze": []})
        aid = f"a{int(z['nr']):02d}_{int(z['satz']):02d}"
        absatz = {"id": aid, "fr": z["fr"], "de": z["de"], "umschrift": (z.get("umschrift") or "").strip() or None, "audio": audio(f"anekdoten/{aid}.mp3")}
        if (z.get("syrisch") or "").strip():   # Pointe auf Syrisch (Knopf « Şām », Mr. Alex 18.10.)
            absatz["syrisch"] = {"fr": z["syrisch"], "umschrift": (z.get("syrisch_u") or "").strip() or None, "audio": audio(f"anekdoten/{aid}_s.mp3")}
        anekdoten[-1]["absaetze"].append(absatz)
    # Grammatik-Lektionen (Türkisch): eine pro Thema, Beispiele sind bereits aufgenommene Sätze (Wendung, Dialogzeile oder Absatz der Geschichte)
    def quelle(qid):
        w = next((w for w in wendungen if w["id"] == qid), None)
        if w:
            return {"fr": w["satz"]["fr"], "de": w["satz"]["de"], "gloss": w["satz"]["gloss"], "umschrift": w["satz"]["umschrift"], "audio": w["satz"]["audio"]}
        for d in dialoge:
            for z in d["zeilen"]:
                if z["id"] == qid:
                    return {"fr": z["fr"], "de": z["de"], "gloss": None, "umschrift": z["umschrift"], "audio": z["audio"]}
        for k in geschichte + anekdoten:
            for a in k["absaetze"]:
                if a["id"] == qid:
                    return {"fr": a["fr"].replace("**", ""), "de": a["de"], "gloss": None, "umschrift": a["umschrift"], "audio": a["audio"]}
        raise KeyError(f"{paar} Grammatik: Satz {qid} unbekannt")
    grammatik = []
    gdatei = getattr(P, "GRAMMATIK_DATEI", "dilbilgisi.tsv")
    for z in (tsv(inhalte, gdatei) if os.path.exists(os.path.join(inhalte, gdatei)) else []):
        assert any(t["id"] == z["thema"] for t in themen), f"{paar} Grammatik {z['id']}: Thema {z['thema']} fehlt"
        # Beispiele: « id=Hinweis;id=Hinweis » – ein Semikolon im Hinweis zählt nicht als Trenner, wenn danach keine id folgt
        import re as _re
        beispiele = [dict(quelle(e.split("=", 1)[0].strip()), hinweis=e.split("=", 1)[1].strip()) for e in _re.split(r";(?=\s*[a-z]+_\d+=|\s*k\d+_\d+=|\s*d\w+_\d+=)", z["beispiele"]) if e.strip()]
        kontrast = [dict(zip(["a", "b", "text"], k.split("|"))) for k in z["kontrast"].split(";") if k]
        chips = []
        for c in z["chips"].split(";"):
            if not c: continue
            formel, antworten = c.split("=")
            chips.append({"formel": formel, "antworten": antworten.split("|")})   # erste Antwort ist richtig
        hoeren = []
        for h in z["hoeren"].split(";"):
            if not h: continue
            paarung, richtig = h.split("=")
            hoeren.append({"saetze": [quelle(q) for q in paarung.split(":")], "richtig": int(richtig) - 1})
        grammatik.append({"id": z["id"], "thema": z["thema"], "titel": z["titel"], "de": z["de"], "regel": z["regel"].split("||"),
                          "morphem": [m for m in z["morphem"].split(",") if m], "beispiele": beispiele, "kontrast": kontrast,
                          "chips": chips, "hoeren_frage": z["hoeren_frage"], "hoeren": hoeren})
    # Schriftmodul (Arabisch): Buchstaben in Formgruppen, Name und Beispielwort aufgenommen
    schrift = None
    SCH = getattr(P, "SCHRIFT", None)
    if SCH:
        buchstaben = list(tsv(inhalte, SCH["datei"]))
        schrift = {"symbol": SCH["symbol"], "titel": SCH["titel"], "de": SCH["de"], "gruppen": []}
        for gid, name, de in SCH["gruppen"]:
            schrift["gruppen"].append({"id": gid, "name": name, "de": de, "buchstaben": [
                {"id": z["id"], "harf": z["harf"], "name": z["name"], "name_u": z["name_u"], "laut": z["laut"], "verbindet": z["verbindet"] == "1",
                 "beispiel": z["beispiel"], "beispiel_u": z["beispiel_u"], "beispiel_de": z["beispiel_de"], "syrien": z["syrien"] or None,
                 "audio": audio(f"huruf/{z['id']}.mp3"), "audio_wort": audio(f"huruf/{z['id']}_w.mp3")} for z in buchstaben if z["gruppe"] == gid]})
        assert sum(len(g["buchstaben"]) for g in schrift["gruppen"]) == len(buchstaben), f"{paar}: Buchstaben ohne Gruppe"
    lob = {}
    for z in tsv(inhalte, "lob.tsv"):
        lob.setdefault(z["art"], []).append({"text": z["text"], "de": z.get("de", ""), "audio": audio(f"lob/{z['id']}.mp3"), "gruppe": [g for g in z["gruppe"].split(",") if g]})
    # Karte und Orte
    karte, gebiet, proj = P.karte_laden(inhalte)
    orte = []
    for z in tsv(inhalte, "orte.tsv"):
        lon, lat = float(z["lon"]), float(z["lat"])
        x, y = proj(lon, lat)
        dep = gebiet(lon, lat)
        orte.append({"id": z["id"], "name": z["name"], "region": z["region"], "dep": dep, "dep_name": karte[dep]["nom"],
                     "x": x, "y": y, "fakt": z["fakt_fr"], "fakt_de": z["fakt_de"], "audio": audio(f"orte/{z['id']}.mp3")})
    import frei_saarland
    spiel = {"orte": orte, "karte": karte, "karte_info": P.KARTE,
             "titel": [{"ab": ab, "name": n, "symbol": s, "audio": audio(f"spiel/titel_{i}.mp3")} for i, (ab, n, s) in enumerate(P.TITEL)],
             "texte": {k: {"text": t, "audio": audio(f"spiel/{k}.mp3")} for k, t in P.SPIEL_TEXTE.items()},
             "frei": frei_saarland.als_daten()}
    return {"paar": paar, "name": P.NAME, "kurz": P.KURZ, "hilfe_kurz": P.HILFE_KURZ, "flagge": P.FLAGGE, "lang": P.LANG, "lang_hilfe": P.LANG_HILFE,
            "sprachausgabe": P.SPRACHAUSGABE, "tempo": getattr(P, "TEMPO", None), "audio_speicher": f"{ausgabe_von(P)['praefix']}-audio-{AUDIO_STAND}", "theme": {k: v for k, v in P.THEME.items() if not k.startswith("icon")},
            "ui": P.UI, "themen": themen, "wendungen": wendungen, "dialoge": dialoge, "rollen": P.ROLLEN, "dialoge_titel": P.DIALOGE_TITEL,
            "aussprache": aussprache, "aussprachen": aussprachen, "schrift": schrift, "geschichte": geschichte, "grammatik": grammatik,
            "anekdoten": anekdoten, "anekdoten_info": {k: v for k, v in (AN or {}).items() if k != "datei"}, "geschichte_info": P.GESCHICHTE, "lob": lob,
            "pensum": PENSUM, "intervalle": INTERVALLE, "spiel": spiel}


def audio_dateien(obj, menge):
    """Alle Audio-Pfade in einem Datenpaket (für den Offline-Download)."""
    if isinstance(obj, dict):
        for v in obj.values(): audio_dateien(v, menge)
    elif isinstance(obj, list):
        for v in obj: audio_dateien(v, menge)
    elif isinstance(obj, str) and obj.startswith("audio/"):
        menge.add(obj)


GETEILT = ["app.js", "basis.css", "app.css"]   # gemeinsamer Code, wird in jede weitere Ausgabe kopiert


def main():
    for ausgabe in AUSGABEN:
        ordner = os.path.join(APP, ausgabe["ordner"])
        os.makedirs(ordner, exist_ok=True)
        if ausgabe["ordner"]:
            for n in GETEILT:
                with open(os.path.join(APP, n), "rb") as q, open(os.path.join(ordner, n), "wb") as z:
                    z.write(q.read())
        paare = []
        for name in ausgabe["pakete"]:
            P = paket(name)
            daten = daten_fuer(P)
            menge = set(); audio_dateien(daten, menge)
            daten["audio_liste"] = sorted(menge)
            with open(os.path.join(ordner, f"daten_{P.PAAR}.js"), "w", encoding="utf-8") as f:
                f.write(f"// Automatisch erzeugt von werkzeuge/bauen.py aus werkzeuge/sprachen/{name}.py – bitte nicht von Hand ändern.\n")
                f.write("window.SPRACHEN = window.SPRACHEN || {};\n")
                f.write(f"window.SPRACHEN[{json.dumps(P.PAAR)}] = " + json.dumps(daten, ensure_ascii=False, indent=1) + ";\n")
            paare.append(P.PAAR)
            print(f"{P.PAAR}: {len(daten['themen'])} Themen, {len(daten['wendungen'])} Wendungen, "
                  f"{sum(1 for w in daten['wendungen'] if w['satz']['audio'])} Sätze mit Audio, {len(menge)} Audiodateien")
        webapp(ausgabe, paare)


def webapp(A, paare):
    ordner = os.path.join(APP, A["ordner"])
    andere = [a["ordner"] + "/" for a in AUSGABEN if a["ordner"] and a is not A]   # Unterordner anderer Ausgaben
    konfig = {"speicher": A["speicher"], "alt": A["alt"], "name": A["name"]}
    with open(os.path.join(ordner, "index.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html>
<html lang="{A['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{A['name']}</title>
<meta name="theme-color" content="{A['farbe']}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{A['kurz']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<link rel="stylesheet" href="basis.css">
<link rel="stylesheet" href="app.css">
</head>
<body>
<div class="niveau-leiste">
  <div class="sprachen" role="group" aria-label="Langue"></div>
  <div class="niveau" role="group" aria-label="Aide">
    <button type="button" data-de="0" aria-pressed="true">FR</button>
    <button type="button" data-de="1" aria-pressed="false">FR + DE</button>
  </div>
</div>
<main id="app" aria-live="polite"></main>
<script>window.APP_KONFIG = {json.dumps(konfig, ensure_ascii=False)};</script>
{"".join(f'<script src="daten_{p}.js"></script>' + chr(10) for p in paare)}<script src="app.js"></script>
</body>
</html>
""")
    os.makedirs(os.path.join(ordner, "icons"), exist_ok=True)
    text, farbe = A["icon"]
    for g in (180, 192, 512):
        ziel = os.path.join(ordner, "icons", f"icon-{g}.png")
        if os.path.exists(ziel):
            continue
        img = Image.new("RGB", (g, g), farbe)
        d = ImageDraw.Draw(img)
        d.ellipse([g * 0.14, g * 0.14, g * 0.86, g * 0.86], fill=(255, 255, 255))
        d.text((g / 2, g * 0.5), text, font=ImageFont.truetype(SCHRIFT, int(g * 0.34)), fill=farbe, anchor="mm")
        img.save(ziel)
    manifest = {"name": A["name"], "short_name": A["kurz"], "lang": A["lang"],
                "start_url": "./", "scope": "./", "display": "standalone",
                "background_color": A["hintergrund"], "theme_color": A["farbe"],
                "icons": [{"src": f"icons/icon-{g}.png", "sizes": f"{g}x{g}", "type": "image/png", "purpose": "any maskable"} for g in (192, 512)]}
    with open(os.path.join(ordner, "manifest.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    # Offline: Kern (Code, Daten, Icons) wird vorab geladen; Audio landet beim Abspielen oder über „Hors-ligne“ im Audio-Speicher
    dateien, h = ["./"], hashlib.sha1()
    for wurzel_, _, namen in sorted(os.walk(ordner)):
        if "/audio" in wurzel_.replace(os.sep, "/"):
            continue
        for n in sorted(namen):
            pfad = os.path.join(wurzel_, n)
            rel = os.path.relpath(pfad, ordner).replace(os.sep, "/")
            if rel in ("sw.js",) or rel.startswith("francais/") or any(rel.startswith(x) for x in andere):
                continue
            dateien.append(rel)
            with open(pfad, "rb") as f:
                h.update(rel.encode() + f.read())
    version = h.hexdigest()[:12]
    audio_version = f"{A['praefix']}-audio-{AUDIO_STAND}"
    with open(os.path.join(ordner, "sw.js"), "w", encoding="utf-8") as f:
        f.write(f"""// Automatisch erzeugt von werkzeuge/bauen.py – Offline-Speicher von {A['name']}.
// Kern (Code, Daten, Icons) wird bei jeder Version neu geladen; Audio bleibt im eigenen Speicher ({audio_version}), gefüllt beim Abspielen oder über „Hors-ligne“.
// Wird AUDIO_STAND in bauen.py erhöht (nach Neuaufnahmen oder Lautstärke-Angleich), verwirft der Browser alle alten Audios.
const VERSION = "{A['praefix']}-kern-{version}";
const AUDIO = "{audio_version}";
const DATEIEN = {json.dumps(dateien)};
self.addEventListener("install", (e) => {{
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
}});
self.addEventListener("activate", (e) => {{
  e.waitUntil(caches.keys().then((alle) => Promise.all(alle.filter((k) => (k.startsWith("{A['praefix']}-kern-") && k !== VERSION) || (k.startsWith("{A['praefix']}-audio") && k !== AUDIO)).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
}});
self.addEventListener("fetch", (e) => {{
  if (e.request.method !== "GET") return;
  const istAudio = e.request.url.includes("/audio/");
  e.respondWith(caches.match(e.request, {{ ignoreSearch: !istAudio }}).then((r) => r || fetch(e.request).then((antwort) => {{
    if (istAudio && antwort.ok) {{ const kopie = antwort.clone(); caches.open(AUDIO).then((c) => c.put(e.request, kopie)); }}
    return antwort;
  }})));
}});
""")
    print(f"Web-App {A['name']} ({A['ordner'] or 'Wurzel'}):", len(dateien), "Kern-Dateien, Version", version)


if __name__ == "__main__":
    main()
