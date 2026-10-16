"""Karte von Beleriand (The Silmarillion) für die englische App – selbst gezeichnet aus den Ortsnamen des Buches.
Erwartet inhalte/en-de/karte/beleriand.geojson: Polygone (Regionen) mit properties {code, nom, region} in einem eigenen
Koordinatensystem (x nach Osten, y nach Norden, Einheit frei; wird auf 0..600 × 0..600 abgebildet).
Fehlt die Datei (Gerüst-Stand), liefert laden() eine leere Karte – die App blendet die Karte dann aus.
Ergebnis wie bei den anderen Karten: ({Code: {"d": Pfad, "nom": Name, "region": Region}}, gebiet(lon, lat), proj(lon, lat))."""
import json, os

BREITE = 600


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


def _enthaelt(geom, x, y):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return any(_in_ring(x, y, poly[0]) and not any(_in_ring(x, y, loch) for loch in poly[1:]) for poly in polys)


def laden(ordner):
    pfad = os.path.join(ordner, "beleriand.geojson")
    if not os.path.exists(pfad):
        return {}, (lambda x, y: None), (lambda x, y: (0, 0))
    with open(pfad, encoding="utf-8") as f:
        features = json.load(f)["features"]
    xs = [p[0] for ft in features for r in _ringe(ft["geometry"]) for p in r]
    ys = [p[1] for ft in features for r in _ringe(ft["geometry"]) for p in r]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    skala = BREITE / max(x1 - x0, y1 - y0)
    dx, dy = (BREITE - (x1 - x0) * skala) / 2, (BREITE - (y1 - y0) * skala) / 2

    def proj(x, y):
        return round((x - x0) * skala + dx, 1), round((y1 - y) * skala + dy, 1)

    karte = {}
    for ft in features:
        p = ft["properties"]
        d = ""
        for ring in _ringe(ft["geometry"]):
            pts = [proj(x, y) for x, y in ring]
            d += "M" + " L".join(f"{x} {y}" for x, y in pts) + " Z "
        karte[p["code"]] = {"d": d.strip(), "nom": p["nom"], "region": p.get("region", "")}

    def gebiet(x, y):
        for ft in features:
            if _enthaelt(ft["geometry"], x, y):
                return ft["properties"]["code"]
        raise ValueError(f"Ort ({x}, {y}) liegt in keiner Region")

    return karte, gebiet, proj
