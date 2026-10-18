"""Karte Portugal (Natural Earth 10m admin-1, gemeinfrei): 18 Distrikte des Festlands als SVG-Pfade im Koordinatensystem 0..600 × 0..600,
dazu die Autonomen Regionen Açores und Madeira als gerahmte Einschübe im Atlantik links (wie auf portugiesischen Schulkarten).
Ergebnis wie arabien_karte: ({Code: {"d", "nom", "region"[, "rahmen"]}}, gebiet(lon, lat), proj(lon, lat))."""
import json, math, os

# Festland rechts: Ausschnitt (Grad) → Pixel
FESTLAND = {"lon": (-9.6, -6.1), "lat": (36.9, 42.2), "x": (300, 592), "y": (8, 592)}
# Einschübe links: Ausschnitt (Grad) → Rahmen (Pixel); Madeira ohne die Ilhas Selvagens
EINSCHUEBE = {
    "PT-20": {"lon": (-31.4, -24.9), "lat": (36.8, 40.0), "x": (8, 284), "y": (40, 230), "nom": "Açores"},
    "PT-30": {"lon": (-17.35, -16.15), "lat": (32.55, 33.2), "x": (8, 284), "y": (262, 432), "nom": "Madeira"},
}
REGION = {"PT-16": "Norte", "PT-03": "Norte", "PT-13": "Norte", "PT-17": "Norte", "PT-04": "Norte",
          "PT-01": "Centro", "PT-18": "Centro", "PT-09": "Centro", "PT-06": "Centro", "PT-05": "Centro", "PT-10": "Centro",
          "PT-11": "Lisboa e Vale do Tejo", "PT-14": "Lisboa e Vale do Tejo", "PT-15": "Lisboa e Vale do Tejo",
          "PT-12": "Alentejo", "PT-07": "Alentejo", "PT-02": "Alentejo", "PT-08": "Algarve",
          "PT-20": "Região Autónoma", "PT-30": "Região Autónoma"}


def _box(b):
    """Projektion eines Ausschnitts in einen Pixelrahmen, winkeltreu (cos-Breite), zentriert."""
    k = math.cos(math.radians(sum(b["lat"]) / 2))
    w, h = (b["lon"][1] - b["lon"][0]) * k, b["lat"][1] - b["lat"][0]
    bw, bh = b["x"][1] - b["x"][0] - 16, b["y"][1] - b["y"][0] - 16
    s = min(bw / w, bh / h)
    dx, dy = b["x"][0] + 8 + (bw - w * s) / 2, b["y"][0] + 8 + (bh - h * s) / 2

    def p(lon, lat):
        return round((lon - b["lon"][0]) * k * s + dx, 1), round((b["lat"][1] - lat) * s + dy, 1)
    return p


def _ringe(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


def _in_ring(x, y, ring):
    drin = False
    for i in range(len(ring)):
        x1, y1 = ring[i - 1][:2]; x2, y2 = ring[i][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            drin = not drin
    return drin


def _enthaelt(geom, lon, lat):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return any(_in_ring(lon, lat, poly[0]) and not any(_in_ring(lon, lat, loch) for loch in poly[1:]) for poly in polys)


def _einschub(lon):
    return "PT-20" if lon < -20 else "PT-30" if lon < -13 else None


def laden(ordner):
    gebiete = json.load(open(os.path.join(ordner, "distritos.geojson"), encoding="utf-8"))["features"]
    proj_fest = _box(FESTLAND)
    proj_ein = {c: _box(b) for c, b in EINSCHUEBE.items()}

    def proj(lon, lat):
        c = _einschub(lon)
        return proj_ein[c](lon, lat) if c else proj_fest(lon, lat)

    karte = {}
    for f in gebiete:
        code = f["properties"]["code"]
        b = EINSCHUEBE.get(code)
        p = proj_ein[code] if b else proj_fest
        teile = []
        for ring in _ringe(f["geometry"]):
            if b and not all(b["lon"][0] <= lo <= b["lon"][1] and b["lat"][0] <= la <= b["lat"][1] for lo, la in ring):
                continue   # Ilhas Selvagens liegen außerhalb des Madeira-Rahmens
            pts, letzter = [], None
            for punkt in ring:
                xy = p(punkt[0], punkt[1])
                if letzter and abs(xy[0] - letzter[0]) < 0.6 and abs(xy[1] - letzter[1]) < 0.6:
                    continue
                pts.append(xy); letzter = xy
            if len(pts) >= 3:
                teile.append("M" + " ".join(f"{x} {y}" for x, y in pts) + "Z")
        eintrag = {"d": "".join(teile), "nom": b["nom"] if b else f["properties"]["name"], "region": REGION[code]}
        if b:
            eintrag["rahmen"] = [b["x"][0], b["y"][0], b["x"][1] - b["x"][0], b["y"][1] - b["y"][0]]
        karte[code] = eintrag

    def gebiet(lon, lat):
        c = _einschub(lon)
        if c:
            return c
        for f in gebiete:
            if _enthaelt(f["geometry"], lon, lat):
                return f["properties"]["code"]
        fest = [f for f in gebiete if f["properties"]["code"] not in EINSCHUEBE]
        naechst = min(fest, key=lambda f: min((pt[0] - lon) ** 2 + (pt[1] - lat) ** 2 for r in _ringe(f["geometry"]) for pt in r))
        return naechst["properties"]["code"]
    return karte, gebiet, proj
