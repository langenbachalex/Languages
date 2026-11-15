// Tests für den Lernkern (app/lernkern.js). Aufruf: node werkzeuge/lernkern_test.js – Ausgabe „ALLES OK“ oder Fehlerliste, Rückgabewert 1 bei Fehlern.
// Die Regeln stammen aus den Entscheidungen von Mr. Alex (School 10.11. und 29.10., Languages 14.11.); docs/systeme.md.
const K = require("../app/lernkern.js");
const fehler = [];
let n = 0;
const gleich = (name, ist, soll) => {
  n++;
  const a = JSON.stringify(ist), b = JSON.stringify(soll);
  if (a !== b) fehler.push(`${name}: erwartet ${b}, bekommen ${a}`);
};

const H = "2026-11-15";
// Datum
gleich("plusTage", K.plusTage(H, 1), "2026-11-16");
gleich("plusTage Monatswechsel", K.plusTage("2026-11-30", 3), "2026-12-03");
gleich("faelligAb Stufe 0 = morgen", K.faelligAb(0, H), "2026-11-16");
gleich("faelligAb Stufe 7 = 120 Tage", K.faelligAb(7, H), K.plusTage(H, 120));
gleich("faelligAb über Stufe 7 bleibt 120", K.faelligAb(9, H), K.plusTage(H, 120));

// Antwort: richtig + fällig → eine Stufe hoch
gleich("richtig fällig", K.antwort({ s: 2, f: H }, { richtig: true, geprueft: true, heute: H }), { s: 3, f: K.faelligAb(3, H) });
// richtig, aber nicht fällig → nichts (kein Hochjagen am selben Tag)
gleich("richtig nicht fällig", K.antwort({ s: 2, f: "2026-11-20" }, { richtig: true, geprueft: true, heute: H }), { s: 2, f: "2026-11-20" });
// « Gewusst » (nicht geprüft) höchstens bis Stufe 3; darüber nur neu einplanen
gleich("Gewusst 2 → 3", K.antwort({ s: 2, f: H }, { richtig: true, heute: H }), { s: 3, f: K.faelligAb(3, H) });
gleich("Gewusst gedeckelt bei 3", K.antwort({ s: 3, f: H }, { richtig: true, heute: H }), { s: 3, f: K.faelligAb(3, H) });
gleich("geprüft über 3", K.antwort({ s: 3, f: H }, { richtig: true, geprueft: true, heute: H }), { s: 4, f: K.faelligAb(4, H) });
gleich("Stufe höchstens 7", K.antwort({ s: 7, f: H }, { richtig: true, geprueft: true, heute: H }).s, 7);
// falsch → zwei Stufen zurück, morgen fällig, Fehler zählen
gleich("falsch", K.antwort({ s: 5, f: "2026-12-01", x: 1 }, { richtig: false, heute: H }), { s: 3, f: "2026-11-16", x: 2 });
gleich("falsch nicht unter 0", K.antwort({ s: 1, f: H }, { richtig: false, heute: H }), { s: 0, f: "2026-11-16", x: 1 });
// neue Karte
gleich("neue Karte falsch", K.antwort(null, { richtig: false, heute: H }), { s: 0, f: "2026-11-16", x: 1 });
// Eingabe bleibt unverändert
const alt = { s: 2, f: H }; K.antwort(alt, { richtig: true, heute: H }); gleich("keine Nebenwirkung", alt, { s: 2, f: H });

// Stolpersteine und sicher
gleich("tricky", K.istTricky({ s: 4, x: 3 }), true);
gleich("tricky endet bei 5", K.istTricky({ s: 5, x: 3 }), false);
gleich("nicht tricky unter 3 Fehlern", K.istTricky({ s: 0, x: 2 }), false);
gleich("sicher ab 5", [K.istSicher({ s: 4 }), K.istSicher({ s: 5 })], [false, true]);

// Wiederholungen: fällige zuerst (Stolpersteine vorn), aufgefüllt mit den als Nächstes fälligen
const karten = { a: { s: 1, f: "2026-11-10" }, b: { s: 1, f: "2026-11-12", x: 3 }, c: { s: 2, f: "2026-11-18" }, d: { s: 2, f: "2026-11-16" }, e: { s: 1, f: "2026-11-14" } };
const reihe = { a: 0, b: 1, c: 2, d: 3, e: 4 };
gleich("Wiederholungen", K.wiederholungen(karten, { heute: H, anzahl: 4, reihenfolge: (id) => reihe[id] }), ["b", "a", "e", "d"]);
gleich("Wiederholungen ohne Auffüllen", K.wiederholungen(karten, { heute: H, anzahl: 4, auffuellen: false, reihenfolge: (id) => reihe[id] }), ["b", "a", "e"]);

// Power Up
gleich("Teil neu erledigt", K.teilErledigt(undefined, H), { eintrag: { am: H, s: 0 }, aufgeladen: false });
gleich("Teil noch frisch", K.teilFaellig({ am: "2026-10-20", s: 0 }, H), false);
gleich("Teil nach 30 Tagen fällig", K.teilFaellig({ am: "2026-10-16", s: 0 }, H), true);
gleich("Stufe 1 erst nach 60", K.teilFaellig({ am: "2026-10-01", s: 1 }, H), false);
gleich("ab Stufe 3 nie fällig", K.teilFaellig({ am: "2020-01-01", s: 3 }, H), false);
gleich("alter Eintrag true nie fällig", K.teilFaellig(true, H), false);
gleich("fälliger Teil wird aufgeladen", K.teilErledigt({ am: "2026-10-01", s: 0 }, H), { eintrag: { am: H, s: 1 }, aufgeladen: true });
gleich("nicht fälliger Teil bleibt", K.teilErledigt({ am: "2026-11-10", s: 0 }, H), { eintrag: { am: "2026-11-10", s: 0 }, aufgeladen: false });
gleich("Tempo", [K.tempo(undefined), K.tempo({ s: 0 }), K.tempo({ s: 1 }), K.tempo({ s: 4 }), K.tempo(true)], [1, 0.5, 0.35, 0.25, 0.5]);

// Tippen vergleichen
gleich("genau", K.vergleiche("se sentir mal", "se sentir bien / mal"), "richtig");
gleich("Groß/Klein, Satzzeichen", K.vergleiche("Wie ist es gelaufen", "Wie ist es gelaufen?"), "richtig");
gleich("(e) optional", [K.vergleiche("je suis désolée", "je suis désolé(e)"), K.vergleiche("je suis désolé", "je suis désolé(e)")], ["richtig", "richtig"]);
gleich("Apostroph wie Leerzeichen", K.vergleiche("ça s’est bien passé", "ça s'est bien passé ?"), "richtig");
gleich("nur Akzente", K.vergleiche("avoir hate de", "avoir hâte de"), "fast");
gleich("Tippfehler", K.vergleiche("ca s est bien pase", "ça s'est bien passé ?"), "fast");
gleich("türkisch ı", K.vergleiche("Geldiginiz icin tesekkurler", "Geldiğiniz için teşekkürler"), "fast");
gleich("falsch", K.vergleiche("avoir faim", "avoir hâte de"), "falsch");
gleich("kurz muss genau sein", K.vergleiche("oui", "non"), "falsch");

console.log(`Lernkern ${K.VERSION}: ${n} Prüfungen`);
if (fehler.length) { fehler.forEach((f) => console.log("FEHLER " + f)); process.exit(1); }
console.log("ALLES OK");
