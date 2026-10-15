# Beta-Test: gesammelte Fehler und Wünsche

Sammeldatei (angelegt 15.10.2026 auf Wunsch von Mr. Alex). Hier landet jede Rückmeldung; umgesetzt wird gebündelt, Veröffentlichung nur nach Freigabe („pushen?“).
Status: ☐ offen · ◐ umgesetzt, noch nicht veröffentlicht · ☑ veröffentlicht.

## Aussprache (Audio)

| Status | Sprache | Stelle | Beobachtung | Lösung |
|---|---|---|---|---|
| ☑ | fr | Lob « Bravo ! », « Canon ! » und 10 weitere Einzelwörter | englisch gelesen | französischer Kontext (« Bravo, très bien ! », « C'est canon ! »), neue Dateinamen, 14.10. |
| ☑ | fr | Ort Nancy | englisch gelesen | Vorlese-Schreibung « Nanci », 15.10. |
| ☑ | fr | Nasale « temps » | s hörbar | Vorlese-Schreibung « tant », 15.10. |
| ☑ | es | Wendung « dar clase » | englisch gelesen | Vorlese-Fassung « ¡Dar clase! » (WENDUNG_KORREKTUR), 15.10. |
| ☐ | es | Orte Sevilla, Córdoba: « mezquita » | Seseo statt Distinción | vier Varianten zum Hören geschickt (neu erzeugt / Stabilität 0,85 / Regieanweisung / « methquita »); Entscheidung offen. Analyse: Sprachcode « es » hat keine Region, Modell wählt Varietät aus Textkontext (andalusische Namen) und Zufall. |
| ☐ | fr, de | Julien (Aurélien) leiser als Mr. Alex | 7 dB | alle Audios auf −18 LUFS angeglichen, 14.10. (☑) |

## Oberfläche

| Status | Betrifft | Beobachtung | Lösung |
|---|---|---|---|
| ☑ | alle Sprachen | Sprachfarbe (fr: dunkles Blau) zu dunkel; Hervorhebungen heben sich nicht ab. Analyse: app.js setzt die Sprachfarben fest, dadurch gelten im Dunkelmodus die hellen Farben weiter (Kontrast 1,3–2,8 : 1). Spanisch-Gold mit weißer Schrift auch im Hellmodus zu schwach (2,1 : 1). | Vorschlag mit Farbprobe am 15.10.; je Sprache eigene Hell- und Dunkelfarben, Schriftfarbe auf Gold dunkel. Umgesetzt und veröffentlicht 15.10. (Freigabe Mr. Alex). |
| ☑ | alle Karten | freigeschaltete Gebiete nicht unterscheidbar (gleiche Farbe, schwacher Rand); gewählter Ort nicht erkennbar | weiße Trennlinien zwischen freigeschalteten Gebieten, gewähltes Gebiet mit rotem Rahmen und hellgelber Füllung, Punkt größer Veröffentlicht 15.10. |

## Noch nicht zugeordnet

(leer)
| ☐ | alle Sprachen | Lob nur gehört bzw. nur in der Zielsprache gelesen; Übersetzung fehlt | Übersetzungsspalte `de` in allen vier `lob.tsv` (fr/es/it → Deutsch, de → Französisch); in der Séance erscheint das Lob jetzt als Pop-up (Zielsprache groß, Übersetzung darunter, 3 s); auf Abschluss-Seiten, im Dialog und im Aussprache-Modul steht die Übersetzung unter dem Lob. Gebaut 15.10., wartet auf Freigabe zum Veröffentlichen. |
