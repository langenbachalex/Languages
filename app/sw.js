// Automatisch erzeugt von werkzeuge/bauen.py – Offline-Speicher von Language Learning.
// Kern (Code, Daten, Icons) wird bei jeder Version neu geladen; Audio bleibt im eigenen Speicher (ll-audio), gefüllt beim Abspielen oder über „Hors-ligne“.
const VERSION = "ll-kern-1ff8c1002670";
const AUDIO = "ll-audio";
const DATEIEN = ["./", "LIESMICH.md", "app.css", "app.js", "basis.css", "daten_es-de.js", "daten_fr-de.js", "index.html", "manifest.webmanifest", "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((alle) => Promise.all(alle.filter((k) => k.startsWith("ll-kern-") && k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const istAudio = e.request.url.includes("/audio/");
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then((r) => r || fetch(e.request).then((antwort) => {
    if (istAudio && antwort.ok) { const kopie = antwort.clone(); caches.open(AUDIO).then((c) => c.put(e.request, kopie)); }
    return antwort;
  })));
});
