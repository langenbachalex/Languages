// Automatisch erzeugt von werkzeuge/bauen.py – Offline-Speicher von English – Word Gym.
// Kern (Code, Daten, Icons) wird bei jeder Version neu geladen; Audio bleibt im eigenen Speicher (en-audio-2), gefüllt beim Abspielen oder über „Hors-ligne“.
// Wird AUDIO_STAND in bauen.py erhöht (nach Neuaufnahmen oder Lautstärke-Angleich), verwirft der Browser alle alten Audios.
const VERSION = "en-kern-13bb221397ce";
const AUDIO = "en-audio-2";
const DATEIEN = ["./", "app.css", "app.js", "basis.css", "daten_en-de.js", "index.html", "manifest.webmanifest", "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((alle) => Promise.all(alle.filter((k) => (k.startsWith("en-kern-") && k !== VERSION) || (k.startsWith("en-audio") && k !== AUDIO)).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const istAudio = e.request.url.includes("/audio/");
  e.respondWith(caches.match(e.request, { ignoreSearch: !istAudio }).then((r) => r || fetch(e.request).then((antwort) => {
    if (istAudio && antwort.ok) { const kopie = antwort.clone(); caches.open(AUDIO).then((c) => c.put(e.request, kopie)); }
    return antwort;
  })));
});
