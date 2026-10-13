"""Spanische Provinzen (click_that_hood / Code for America, MIT; Daten der CartoDB-Grenzen) als einfache SVG-Pfade.
Ergebnis wie frankreich_karte.laden: {Code: {"d": Pfad, "nom": Name, "region": Autonome Gemeinschaft}}, 0..600 × 0..600.
Die Kanaren werden wie auf spanischen Karten als Einschub nach Südosten verschoben."""
import json, math, os

BREITE = 600
LON0, LON1, LAT0, LAT1 = -9.6, 4.6, 33.4, 44.0
K = math.cos(math.radians((LAT0 + LAT1) / 2))
KANAREN = (16.6, 6.3)   # Verschiebung (lon, lat) für den Einschub

REGION = {"01": "Andalucía", "02": "Aragón", "03": "Islas Baleares", "04": "Canarias", "05": "Cantabria", "06": "Castilla-La Mancha",
          "07": "Castilla y León", "08": "Cataluña", "09": "Ceuta", "10": "Extremadura", "11": "Galicia", "12": "La Rioja", "13": "Madrid",
          "14": "Melilla", "15": "Murcia", "16": "Navarra", "17": "País Vasco", "18": "Asturias", "19": "Comunidad Valenciana"}
NAME = {"01": "Álava", "03": "Alicante", "07": "Islas Baleares", "12": "Castellón", "20": "Guipúzcoa", "38": "Santa Cruz de Tenerife",
        "46": "Valencia", "48": "Vizcaya"}


def _verschoben(lon, lat):
    return (lon + KANAREN[0], lat + KANAREN[1]) if lon < -11 else (lon, lat)


def projektion():
    w, h = (LON1 - LON0) * K, LAT1 - LAT0
    skala = BREITE / max(w, h)
    dx, dy = (BREITE - w * skala) / 2, (BREITE - h * skala) / 2

    def p(lon, lat):
        lon, lat = _verschoben(lon, lat)
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
    provs = json.load(open(os.path.join(ordner, "provincias.geojson"), encoding="utf-8"))["features"]
    p = projektion()
    karte = {}
    for f in provs:
        code = f["properties"]["cod_prov"]
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
        karte[code] = {"d": "".join(teile), "nom": NAME.get(code, f["properties"]["name"]), "region": REGION[f["properties"]["cod_ccaa"]]}

    def provinz(lon, lat):
        for f in provs:
            if _enthaelt(f["geometry"], lon, lat):
                return f["properties"]["cod_prov"]
        naechst = min(provs, key=lambda f: min((pt[0] - lon) ** 2 + (pt[1] - lat) ** 2 for r in _ringe(f["geometry"]) for pt in r))
        return naechst["properties"]["cod_prov"]
    return karte, provinz, p
