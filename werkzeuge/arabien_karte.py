"""Karte Syrien + Saudi-Arabien (Natural Earth 10m admin-1, gemeinfrei): 13 syrische Gouvernements und 13 saudische Provinzen als SVG-Pfade
im Koordinatensystem 0..600 × 0..600. Damaskus bekommt einen Einschub (Altstadt, acht Stationen) oben rechts über dem leeren Irak;
das Gouvernement auf der Landeskarte heißt "SY-DIm", der Einschub trägt den Code "SY-DI" (Mechanik wie tuerkei_karte).
Ergebnis: ({Code: {"d", "nom", "region"}}, gebiet(lon, lat), proj(lon, lat))."""
import json, math, os

BREITE = 600
LON0, LON1, LAT0, LAT1 = 34.3, 56.0, 16.0, 37.5
K = math.cos(math.radians((LAT0 + LAT1) / 2))
EINSCHUB = {"lon": (36.27, 36.34), "lat": (33.495, 33.56), "x": (345, 585), "y": (15, 238)}   # Ausschnitt (Grad) → Lage (Pixel)
NAME_AR = {"SY-DI": "دِمَشْق"}


def projektion():
    w, h = (LON1 - LON0) * K, LAT1 - LAT0
    skala = BREITE / max(w, h)
    dx, dy = (BREITE - w * skala) / 2, (BREITE - h * skala) / 2

    def p(lon, lat):
        return round((lon - LON0) * K * skala + dx, 1), round((LAT1 - lat) * skala + dy, 1)
    return p


def im_einschub(lon, lat):
    e = EINSCHUB
    return e["lon"][0] <= lon <= e["lon"][1] and e["lat"][0] <= lat <= e["lat"][1]


def einschub_proj(lon, lat):
    e = EINSCHUB
    sx = (e["x"][1] - e["x"][0]) / (e["lon"][1] - e["lon"][0]); sy = (e["y"][1] - e["y"][0]) / (e["lat"][1] - e["lat"][0])
    return round(e["x"][0] + (lon - e["lon"][0]) * sx, 1), round(e["y"][0] + (e["lat"][1] - lat) * sy, 1)


def _ringe(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


def _in_ring(x, y, ring):
    drin = False
    for i in range(len(ring)):
        x1, y1 = ring[i - 1]; x2, y2 = ring[i]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            drin = not drin
    return drin


def _enthaelt(geom, lon, lat):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return any(_in_ring(lon, lat, poly[0]) and not any(_in_ring(lon, lat, loch) for loch in poly[1:]) for poly in polys)


def _schnitt(a, b, achse, wert):
    t = (wert - a[achse]) / (b[achse] - a[achse])
    return [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]


def _zuschneiden(ring):
    e = EINSCHUB
    kanten = [(0, e["lon"][0], True), (0, e["lon"][1], False), (1, e["lat"][0], True), (1, e["lat"][1], False)]
    pts = list(ring)
    for achse, wert, groesser in kanten:
        drin = (lambda q: q[achse] >= wert) if groesser else (lambda q: q[achse] <= wert)
        neu = []
        for i, b in enumerate(pts):
            a = pts[i - 1]
            if drin(b):
                if not drin(a):
                    neu.append(_schnitt(a, b, achse, wert))
                neu.append(b)
            elif drin(a):
                neu.append(_schnitt(a, b, achse, wert))
        pts = neu
        if not pts:
            break
    return pts


def _name(p):
    n = p.get("name_ar") or p["name"]
    for praefix in ("محافظة ", "منطقة "):
        if n.startswith(praefix):
            n = n[len(praefix):]
    return NAME_AR.get(p["code"], n)


def laden(ordner):
    pfad = os.path.join(ordner, "gebiete.geojson")
    if not os.path.exists(pfad):
        return {}, (lambda lon, lat: None), (lambda lon, lat: (0, 0))
    gebiete = [f for f in json.load(open(pfad, encoding="utf-8"))["features"] if "~" not in f["properties"]["code"]]   # UNDOF-Zone weg
    p = projektion()
    karte, damaskus = {}, None
    for f in gebiete:
        teile = []
        for ring in _ringe(f["geometry"]):
            pts, letzter = [], None
            for lon, lat in ring:
                xy = p(lon, lat)
                if letzter and abs(xy[0] - letzter[0]) < 0.6 and abs(xy[1] - letzter[1]) < 0.6:
                    continue
                pts.append(xy); letzter = xy
            if len(pts) >= 3:
                teile.append("M" + " ".join(f"{x} {y}" for x, y in pts) + "Z")
        code = f["properties"]["code"]
        region = "سُورِيَا" if f["properties"]["land"] == "SYR" else "السُّعُودِيَّة"
        if code == "SY-DI":
            damaskus = f; code = "SY-DIm"
        karte[code] = {"d": "".join(teile), "nom": _name(f["properties"]), "region": region}
    # Einschub Damaskus: Gouvernement zugeschnitten auf die Altstadt (füllt den Rahmen), Stationen als Punkte
    teile = []
    for ring in _ringe(damaskus["geometry"]):
        pts = [einschub_proj(lon, lat) for lon, lat in _zuschneiden(ring)]
        if len(pts) >= 3:
            teile.append("M" + " ".join(f"{x} {y}" for x, y in pts) + "Z")
    e = EINSCHUB
    karte["SY-DI"] = {"d": "".join(teile), "nom": NAME_AR["SY-DI"], "region": "سُورِيَا",
                      "rahmen": [e["x"][0], e["y"][0], e["x"][1] - e["x"][0], e["y"][1] - e["y"][0]], "auch": "SY-DIm",
                      "von": p((e["lon"][0] + e["lon"][1]) / 2, (e["lat"][0] + e["lat"][1]) / 2)}

    def gebiet(lon, lat):
        if im_einschub(lon, lat):
            return "SY-DI"
        for f in gebiete:
            if _enthaelt(f["geometry"], lon, lat):
                return f["properties"]["code"].replace("SY-DI", "SY-DIm")
        naechst = min(gebiete, key=lambda f: min((pt[0] - lon) ** 2 + (pt[1] - lat) ** 2 for r in _ringe(f["geometry"]) for pt in r))
        return naechst["properties"]["code"].replace("SY-DI", "SY-DIm")

    def proj(lon, lat):
        return einschub_proj(lon, lat) if im_einschub(lon, lat) else p(lon, lat)
    return karte, gebiet, proj
