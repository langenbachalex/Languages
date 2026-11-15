# System-Tabelle: welches System steckt in welcher App

Stand: 15.11.2026 (angelegt mit Mr. Alex). Zweck: Was Mr. Alex in einer App systematisch baut, soll in die anderen wandern, ohne dass er jeden Schritt mehrmals erklären muss oder den Überblick verliert.

- **Apps:** `EN6` Englisch 6 (`School/app/`), `EN9` Englisch 9 (`School/app/klasse9/`), `FR` Französisch 5/6 (`School/app/franz/`), `LANG` Language Learning (dieses Repository, alle Sprachen).
- **Zeichen:** ✅ gebaut (Commit) · ◐ teilweise · ☐ offen, passt · — passt nicht · ? noch prüfen.
- **Pflege:** Jeder Bau-Chat, der ein System baut oder ändert, trägt seine Zeile hier ein. Die wöchentliche Aufgabe « Systeme School → Languages » (freitags) liest die neuen School-Commits seit dem Stand unten, ergänzt die Tabelle und fragt Mr. Alex, was übernommen werden soll. Übernommen wird nur nach seinem OK.
- **Stand School:** zuletzt gelesen bis Commit `b0d845a` (15.11.2026, Branch `claude/awesome-dijkstra-dy57ir`).
- **Lernkern (Stufe 2, begonnen 15.11.):** `app/lernkern.js` in diesem Repository ist der Master (Version 1.0.0, 39 Tests in `werkzeuge/lernkern_test.js`). LANG nutzt ihn seit 15.11. Er enthält: Antwort-Regel (nur fällige steigen, « Gewusst » bis Stufe 3, falsch = zwei zurück), Stolperstein/sicher, Wiederholungen mit Auffüllen, Power Up (Fristen, Aufladen, Tempo), Tippen vergleichen. Tagesplan-Zusammenstellung und Aussehen bleiben in jeder App.
- **Übernahme in School (nach den GLN, je App ein Bau-Chat: EN9, dann EN6, dann FR):** Datei aus `langenbachalex/Languages` (`main`, `app/lernkern.js`) nach `School/app/lernkern.js` kopieren, die Bauskripte kopieren sie wie die anderen gemeinsamen Dateien in `klasse9/` und `franz/`, Skript-Tag vor `app.js`. Die Spielstände passen schon: `stand.gym.karten[id] = { s, f, x }` und `stand.teile[key] = { am, s }` haben dasselbe Format. `merke(id, richtig, art)` wird zu `karten[id] = Lernkern.antwort(karten[id], { richtig, geprueft: art !== "s", heute })`; Power Up über `Lernkern.teilFaellig/teilErledigt/tempo`. Danach zeigt die Tabelle je App die Kern-Version; die wöchentliche Aufgabe meldet, wenn eine App eine ältere Version hat.

| System | EN6 | EN9 | FR | LANG |
|---|---|---|---|---|
| Word Gym: Kasten Stufe 0–7, Intervalle 1·3·7·14·30·60·120, Tagesplan | ✅ | ✅ | ✅ 8292614 (« Muscu des mots ») | ✅ |
| Pensum einstellbar (neu und Wiederholungen) | ✅ | ✅ | ✅ 8292614 | ✅ fda0ed4, 19e54b9 |
| Antworten füttern den Kasten, Fehler = zwei Stufen zurück, nur fällige steigen | ✅ 74e4f05 | ✅ d9df4b4 | ✅ 8292614 | ✅ 763f60a |
| « Gewusst » höchstens bis Stufe 3, darüber nur geprüfte Antworten | ✅ 74e4f05 | ✅ d9df4b4 | ✅ 8292614 | ✅ 6b188d9 |
| Abrufform wächst mit der Stufe (wählen, tippen, Lücke) | ◐ ab 3 wählen/tippen | ◐ ab 3 wählen, E-Kurs tippen | ◐ ab 3 aus vier wählen | ✅ 6b188d9 (2–3 wählen, 4–5 tippen, 6–7 Lücke) |
| Satz-Karten (2 pro Tag), neu nur aus Geübtem oder mit bekanntem Wort | ✅ 74e4f05 | ✅ d9df4b4 | ✅ 8292614 | ✅ 8901ea5 |
| Wiederholungen aufgefüllt mit den als Nächstes fälligen | ? | ? | ✅ 8292614 | ✅ 8901ea5 |
| Schluss-Treffer, Fehler vor dem Schluss noch einmal | ✅ 010b7d6 | ✅ d9df4b4 | ✅ 8292614 | ✅ 8901ea5 |
| Tricky words / Stolpersteine (3 Fehler, bis Stufe 5), Liste | ✅ 74e4f05 | ✅ d9df4b4 | ✅ 8292614 | ✅ 763f60a, 8901ea5 |
| « N sicher » ab Stufe 5 mit Balken | ✅ 74e4f05 | ✅ d9df4b4 | ✅ 8292614 | ✅ 8901ea5 |
| Satz zuerst: neue Wendung erst nach Schritt 1 im Thema | ? | ◐ Beispielsatz erst nach dem Wort | ? | ✅ 763f60a |
| Memory nach dem Tagespensum (+10 einmal am Tag) | ✅ 948b925 | ✅ | ? | ✅ 5755f64 |
| Combo-Belohnungen (Zähler, Flitzer) | ✅ | ✅ | ? | ✅ 5755f64 |
| Eintippen mit Fehlertoleranz | ✅ | ✅ E-Kurs | ☐ | ✅ 6b188d9 |
| ⚡ Power Up: erledigte Teile nach 30/60/120 Tagen gelb, kürzere Sperrzeiten | ✅ (29.10.) | ✅ (29.10.) | ☐ | ✅ 8901ea5 |
| Belohnungen der Reihe nach (Lob, Stempel, Pop-up schneiden sich nicht) | ✅ (24.10.) | ✅ (24.10.) | ? | ✅ f1c92da |
| GLN-Kopplung (vor dem GLN wird alles fällig) | ✅ | ✅ | ? | — keine GLN |
| Lehrer-Bereich: schwere Wörter, Sync Stufe A (QR) | ✅ | ✅ | ✅ | — Selbstlerner |
| Lernkern `lernkern.js` (Version) | ☐ nach GLN | ☐ nach GLN | ☐ nach GLN | ✅ 1.0.0 |
| Festes Testprogramm im Repo | ✅ `werkzeuge/testprogramm.js` (15.11.) | ✅ | ✅ | ✅ `werkzeuge/testprogramm.js` (15.11.) |
