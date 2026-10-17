"""Türkei: 81 İl (Natural Earth 10m admin-1, gemeinfrei) als SVG-Pfade im Koordinatensystem 0..600 × 0..600.
Ergebnis wie bei den anderen Karten: ({Code: {"d", "nom", "region"}}, gebiet(lon, lat), proj(lon, lat)).
İstanbul bekommt einen Einschub (Mr. Alex, 16.10.: die acht Stationen lagen auf der Landeskarte in einem Punkt): das Stadtzentrum
wird vergrößert unten links ins Mittelmeer gesetzt (Code "34", Rahmen in "rahmen"); das İl auf der Landeskarte heißt "34m"."""
import json, math, os

BREITE = 600
LON0, LON1, LAT0, LAT1 = 25.5, 45.0, 35.7, 42.3
K = math.cos(math.radians((LAT0 + LAT1) / 2))
EINSCHUB = {"lon": (28.90, 29.18), "lat": (40.86, 41.065), "x": (20, 280), "y": (405, 595)}   # Ausschnitt (Grad) → Lage (Pixel)
# Küste im Einschub von Hand (Natural Earth ist hier zu grob: kein Goldenes Horn, Bosporus ein Strich). Ringe in (lon, lat).
ISTANBUL = [
    # Europäische Seite: Marmaraküste → Sarayburnu → Goldenes Horn → Karaköy → Beşiktaş → Ortaköy → Bosporus
    [(28.90, 40.975), (28.93, 40.982), (28.95, 40.996), (28.97, 40.999), (28.98, 41.005), (28.987, 41.013), (28.985, 41.019),
     (28.975, 41.02), (28.962, 41.024), (28.95, 41.03), (28.936, 41.044), (28.925, 41.056), (28.945, 41.051), (28.958, 41.041),
     (28.966, 41.032), (28.974, 41.021), (28.983, 41.025), (28.99, 41.033), (29.0, 41.04), (29.008, 41.041), (29.02, 41.046),
     (29.03, 41.05), (29.04, 41.062), (29.044, 41.065), (28.90, 41.065)],
    # Asiatische Seite: Bosporus → Üsküdar → Haydarpaşa → Kadıköy → Moda → Bostancı → Maltepe
    [(29.057, 41.065), (29.053, 41.052), (29.043, 41.04), (29.03, 41.032), (29.018, 41.028), (29.006, 41.018), (29.004, 41.012),
     (29.008, 41.006), (29.016, 41.0), (29.024, 40.993), (29.03, 40.985), (29.026, 40.978), (29.04, 40.97), (29.06, 40.962),
     (29.09, 40.955), (29.13, 40.92), (29.18, 40.90), (29.18, 41.065)],
    # Prinzeninseln: Kınalıada, Burgazada, Heybeliada, Büyükada
    [(29.045, 40.915), (29.055, 40.918), (29.058, 40.908), (29.048, 40.905)],
    [(29.06, 40.888), (29.072, 40.892), (29.075, 40.878), (29.063, 40.875)],
    [(29.083, 40.885), (29.098, 40.882), (29.1, 40.868), (29.086, 40.866)],
    [(29.108, 40.882), (29.128, 40.88), (29.138, 40.86), (29.105, 40.86)],
]


def im_einschub(lon, lat):
    e = EINSCHUB
    return e["lon"][0] <= lon <= e["lon"][1] and e["lat"][0] <= lat <= e["lat"][1]


def einschub_proj(lon, lat):
    e = EINSCHUB
    sx = (e["x"][1] - e["x"][0]) / (e["lon"][1] - e["lon"][0]); sy = (e["y"][1] - e["y"][0]) / (e["lat"][1] - e["lat"][0])
    return round(e["x"][0] + (lon - e["lon"][0]) * sx, 1), round(e["y"][0] + (e["lat"][1] - lat) * sy, 1)


def _zuschneiden(ring):
    """Sutherland–Hodgman: Ring auf das Rechteck des Einschubs beschränken."""
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


def _schnitt(a, b, achse, wert):
    t = (wert - a[achse]) / (b[achse] - a[achse])
    return [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]


def projektion():
    w, h = (LON1 - LON0) * K, LAT1 - LAT0
    skala = BREITE / max(w, h)
    dx, dy = (BREITE - w * skala) / 2, (BREITE - h * skala) / 2

    def p(lon, lat):
        return round((lon - LON0) * K * skala + dx, 1), round((LAT1 - lat) * skala + dy, 1)
    return p


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


def laden(ordner):
    iller = json.load(open(os.path.join(ordner, "iller.geojson"), encoding="utf-8"))["features"]
    p = projektion()
    karte = {}
    for f in iller:
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
        if code == "34":
            einschub = f
            code = "34m"
        karte[code] = {"d": "".join(teile), "nom": f["properties"]["name"], "region": f["properties"]["region"]}
    # Einschub İstanbul: Zentrum vergrößert, zugeschnitten auf den Ausschnitt
    teile = []
    for ring in ISTANBUL:
        pts = [einschub_proj(lon, lat) for lon, lat in _zuschneiden(ring)]
        if len(pts) >= 3:
            teile.append("M" + " ".join(f"{x} {y}" for x, y in pts) + "Z")
    e = EINSCHUB
    karte["34"] = {"d": "".join(teile), "nom": einschub["properties"]["name"], "region": einschub["properties"]["region"],
                   "rahmen": [e["x"][0], e["y"][0], e["x"][1] - e["x"][0], e["y"][1] - e["y"][0]], "auch": "34m",
                   "von": p((e["lon"][0] + e["lon"][1]) / 2, (e["lat"][0] + e["lat"][1]) / 2)}

    def il(lon, lat):
        if im_einschub(lon, lat):
            return "34"
        for f in iller:
            if _enthaelt(f["geometry"], lon, lat):
                return f["properties"]["code"]
        naechst = min(iller, key=lambda f: min((pt[0] - lon) ** 2 + (pt[1] - lat) ** 2 for r in _ringe(f["geometry"]) for pt in r))
        return naechst["properties"]["code"].replace("34", "34m")

    def proj(lon, lat):
        return einschub_proj(lon, lat) if im_einschub(lon, lat) else p(lon, lat)
    return karte, il, proj
