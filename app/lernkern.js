/* Lernkern – gemeinsame Lernlogik für alle Apps von Mr. Alex (Stufe 2, begonnen 15.11.2026).
   Master: langenbachalex/Languages, Datei app/lernkern.js. Tests: node werkzeuge/lernkern_test.js. Übersicht: docs/systeme.md.
   Reine Funktionen: kein DOM, kein Speicher, Datum kommt als „JJJJ-MM-TT“ herein. Jede App behält ihr eigenes Aussehen und ihren Spielstand
   und ruft nur diese Regeln auf – eine Regel ändern heißt: hier ändern, Tests laufen lassen, Datei in die Apps kopieren.
   Regeln (Entscheidungen Mr. Alex 29.10., 10.11., 14.11.):
   - Kasten Stufe 0–7, fällig nach 1·3·7·14·30·60·120 Tagen.
   - Richtig hebt nur fällige Karten (kein Hochjagen am selben Tag); « Gewusst » ohne Prüfung höchstens bis Stufe 3.
   - Falsch = zwei Stufen zurück, morgen fällig, Fehler zählen (x). Stolperstein: x ≥ 3 und Stufe < 5. Sicher: Stufe ≥ 5.
   - Wiederholungen: fällige zuerst (Stolpersteine vorn), aufgefüllt mit den als Nächstes fälligen.
   - Power Up: erledigter Teil { am, s } wird nach 30/60/120 Tagen fällig; erneut erledigt = Stufe +1; Sperrzeiten 50/35/25 %.
   - Tippen: Groß/Klein, Satzzeichen, Apostroph egal; « a / b » = Varianten; « (e) » optional; nur Akzente oder wenige Tippfehler = fast richtig. */
(function (wurzel) {
  "use strict";
  const K = {
    VERSION: "1.0.0",
    INTERVALLE: [1, 3, 7, 14, 30, 60, 120],
    DECKEL: 3, SICHER: 5, TRICKY: 3,
    POWER_TAGE: [30, 60, 120], POWER_TEMPO: [0.5, 0.35, 0.25],
  };

  // ---------- Datum ----------
  K.plusTage = (iso, n) => {
    const d = new Date(iso + "T12:00:00Z");
    d.setUTCDate(d.getUTCDate() + n);
    return d.toISOString().slice(0, 10);
  };
  K.faelligAb = (stufe, heute) => K.plusTage(heute, K.INTERVALLE[Math.min(Math.max(stufe, 0), K.INTERVALLE.length - 1)]);

  // ---------- Kasten ----------
  // Neue Karte zurückgeben (die alte bleibt unverändert). karte = { s, f, x? } oder null für eine noch unbekannte Karte.
  K.antwort = (karte, { richtig, geprueft = false, heute }) => {
    const k = karte ? { ...karte } : { s: 0, f: heute };
    if (richtig) {
      if (k.f > heute) return k;
      if (geprueft || k.s < K.DECKEL) k.s = Math.min(k.s + 1, K.INTERVALLE.length);
      k.f = K.faelligAb(k.s, heute);
    } else {
      k.s = Math.max(0, k.s - 2); k.f = K.faelligAb(0, heute); k.x = (k.x || 0) + 1;
    }
    return k;
  };
  K.istTricky = (k) => !!k && (k.x || 0) >= K.TRICKY && k.s < K.SICHER;
  K.istSicher = (k) => !!k && k.s >= K.SICHER;
  // karten = { id: { s, f, x } }; reihenfolge(id) = Platz in der App (Buch/Themen); Ergebnis: Liste der Ids für heute
  K.wiederholungen = (karten, { heute, anzahl, reihenfolge = () => 0, auffuellen = true, nur = () => true }) => {
    const reihe = (a, b) => (K.istTricky(b[1]) - K.istTricky(a[1])) || (a[1].f < b[1].f ? -1 : a[1].f > b[1].f ? 1 : reihenfolge(a[0]) - reihenfolge(b[0]));
    const alle = Object.entries(karten).filter(([id]) => nur(id));
    const faellig = alle.filter(([, k]) => k.f <= heute).sort(reihe);
    const spaeter = auffuellen ? alle.filter(([, k]) => k.f > heute).sort(reihe) : [];
    return [...faellig, ...spaeter].map(([id]) => id).slice(0, anzahl);
  };

  // ---------- Power Up (erledigte Teile) ----------
  K.teilFaellig = (e, heute) => !!e && e !== true && e.s < K.POWER_TAGE.length && heute >= K.plusTage(e.am, K.POWER_TAGE[e.s]);
  // Ein Teil wurde (wieder) durchgemacht: neuer Eintrag und ob er aufgeladen wurde
  K.teilErledigt = (e, heute) => {
    if (!e || e === true) return { eintrag: e === true ? { am: heute, s: 0 } : { am: heute, s: 0 }, aufgeladen: false };
    if (K.teilFaellig(e, heute)) return { eintrag: { am: heute, s: e.s + 1 }, aufgeladen: true };
    return { eintrag: e, aufgeladen: false };
  };
  // Sperrzeiten-Faktor: wer einen Teil schon kennt, darf zügiger durch
  K.tempo = (e) => (!e ? 1 : K.POWER_TEMPO[Math.min(e === true ? 0 : e.s, K.POWER_TEMPO.length - 1)]);

  // ---------- Tippen vergleichen ----------
  K.normal = (x) => String(x).normalize("NFC").toLowerCase().replace(/[’`']/g, " ").replace(/[«»"“”„¡!¿?.,;:…()\[\]]/g, " ").replace(/\s+/g, " ").trim();
  K.ohneAkzent = (x) => x.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ı/g, "i");
  K.abstand = (a, b) => {
    const d = Array.from({ length: b.length + 1 }, (_, j) => j);
    for (let i = 1; i <= a.length; i++) {
      let vor = d[0]; d[0] = i;
      for (let j = 1; j <= b.length; j++) { const tmp = d[j]; d[j] = Math.min(d[j] + 1, d[j - 1] + 1, vor + (a[i - 1] === b[j - 1] ? 0 : 1)); vor = tmp; }
    }
    return d[b.length];
  };
  K.varianten = (ziel) => {
    const v = new Set();
    const ohneKl = ziel.replace(/\((\w+)\)/g, ""), mitKl = ziel.replace(/\((\w+)\)/g, "$1");
    for (const z of [ziel, ohneKl, mitKl]) {
      v.add(z);
      const m = z.match(/^(.*\s)(\S+) \/ (\S+)(.*)$/);
      if (m) { v.add(m[1] + m[2] + m[4]); v.add(m[1] + m[3] + m[4]); }
    }
    return [...v].map(K.normal);
  };
  K.vergleiche = (eingabe, ziel) => {
    const e = K.normal(eingabe), vs = K.varianten(ziel);
    if (vs.includes(e)) return "richtig";
    if (vs.some((z) => K.ohneAkzent(z) === K.ohneAkzent(e))) return "fast";
    if (vs.some((z) => K.abstand(K.ohneAkzent(e), K.ohneAkzent(z)) <= (z.length < 6 ? 0 : z.length < 14 ? 1 : 2))) return "fast";
    return "falsch";
  };

  if (typeof module !== "undefined" && module.exports) module.exports = K;
  else wurzel.Lernkern = K;
})(typeof window !== "undefined" ? window : globalThis);
