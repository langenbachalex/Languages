"""Italienische Provinzen (ISTAT via openpolis/geojson-italy, CC BY 4.0; vereinfacht auf 3 Dezimalstellen) als SVG-Pfade.
Ergebnis wie frankreich_karte.laden: {Code: {"d": Pfad, "nom": Name, "region": Region}}, 0..600 × 0..600."""
import json, math, os

BREITE = 600
LON0, LON1, LAT0, LAT1 = 6.5, 18.6, 35.4, 47.2
K = math.cos(math.radians((LAT0 + LAT1) / 2))


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
        x1, y1 = ring[i - 1][:2]; x2, y2 = ring[i][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            drin = not drin
    return drin


def _enthaelt(geom, lon, lat):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return any(_in_ring(lon, lat, poly[0]) and not any(_in_ring(lon, lat, loch) for loch in poly[1:]) for poly in polys)


def laden(ordner):
    provs = json.load(open(os.path.join(ordner, "province.geojson"), encoding="utf-8"))["features"]
    p = projektion()
    karte = {}
    for f in provs:
        code = f["properties"]["code"]
        teile = []
        for ring in _ringe(f["geometry"]):
            pts, letzter = [], None
            for punkt in ring:
                xy = p(punkt[0], punkt[1])
                if letzter and abs(xy[0] - letzter[0]) < 0.6 and abs(xy[1] - letzter[1]) < 0.6:
                    continue
                pts.append(xy); letzter = xy
            if len(pts) >= 3:
                teile.append("M" + " ".join(f"{x} {y}" for x, y in pts) + "Z")
        karte[code] = {"d": "".join(teile), "nom": f["properties"]["name"], "region": f["properties"]["regione"]}

    def provinz(lon, lat):
        for f in provs:
            if _enthaelt(f["geometry"], lon, lat):
                return f["properties"]["code"]
        naechst = min(provs, key=lambda f: min((pt[0] - lon) ** 2 + (pt[1] - lat) ** 2 for r in _ringe(f["geometry"]) for pt in r))
        return naechst["properties"]["code"]
    return karte, provinz, p
