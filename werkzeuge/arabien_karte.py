"""Karte Syrien + Saudi-Arabien (folgt: Natural Earth 10m admin-1). Fehlt inhalte/ar-de/karte/*.geojson, liefert laden() eine leere Karte –
die App blendet die Karte dann aus (wie beleriand_karte vor dem Zeichnen)."""
import os


def laden(ordner):
    if not os.path.exists(os.path.join(ordner, "gebiete.geojson")):
        return {}, (lambda lon, lat: None), (lambda lon, lat: (0, 0))
    raise NotImplementedError("Karte Syrien/Saudi-Arabien noch nicht gebaut")
