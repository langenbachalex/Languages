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
| ☑ | alle Sprachen | Lob nur gehört bzw. nur in der Zielsprache gelesen; Übersetzung fehlt | Übersetzungsspalte `de` in allen vier `lob.tsv` (fr/es/it → Deutsch, de → Französisch); in der Séance erscheint das Lob jetzt als Pop-up (Zielsprache groß, Übersetzung darunter, 3 s); auf Abschluss-Seiten, im Dialog und im Aussprache-Modul steht die Übersetzung unter dem Lob. Veröffentlicht 15.10. |
| ☑ | fr | Nasale (Aussprache-Modul): Einzelwörter kippen ins Englische/Deutsche (« vin » wie „win“, « temps » als „tem“) | Ursache: nackte Einzelwörter ohne Satzkontext, 38 der 86 Wörter sind auch englische/deutsche Wörter. Lösung: jedes Wort wird im Trägersatz « Écoute bien : … » gesprochen, danach schneidet audio.py den Vorspann an der Pause ab (TRAEGERSATZ je Paket, Stimme „w“). Alle 86 Nasale neu, 15.10. |
| ☑ | es | Geschichte Kap. 1, Absatz 4: « Entre » am Satzanfang als „ontre“ (französisch) | zwei Neuaufnahmen kippten ebenfalls; Vorlese-Schreibung « Éntre » (AUSSPRACHE_KORREKTUR), neu aufgenommen 15.10. |
| ☑ | it | Wendung « fare fatica »: « fare » wird englisch gelesen (wie „fair“) | beide Wendungen im Trägersatz « Ascolta bene… » gesprochen und geschnitten (WENDUNG_IM_TRAEGERSATZ), 17.10. |
| ☑ | it | Lob « Hai orecchio! »: das H wird hörbar gesprochen | Vorlese-Schreibung « Ai » (ganzes Wort), neu aufgenommen 17.10.; kein weiterer Lob-Eintrag mit hai/ho. |
| ☑ | alle Karten | Ortstexte auf der Karte erscheinen unübersetzt (Deutsch war nur per Tipp auf den Text oder mit « + DE » sichtbar) | deutsche Fassung steht jetzt immer sichtbar unter dem Ortstext (alle fünf Sprachen). Veröffentlicht 16.10. |
| ☑ | it | « I portici » (Karte Bologna): der Artikel « I » wird englisch gelesen | Vorlese-Fassung « Portici di Bologna » (Artikel am Anfang weggelassen), neu aufgenommen 17.10. |
| ☑ | fr | « Paris »: das S wird gesprochen | Vorlese-Schreibung « Pari », 9 Aufnahmen neu (3 Orte, 3 Absätze, Satz se_19 mit Zeiten), 17.10. |
| ☑ | fr | « une réunion » (Entre profs, Wendung und Beispielsatz; auch Satz in Faux amis): « une » klingt wie « un » | drei Aufnahmen neu erzeugt 17.10.; Wendung und Faux-amis-Satz gut, Beispielsatz « On a une réunion » kippt weiter nach « a ». Drei Vorlese-Varianten geschickt (Pause nach « On a » / « eune » / Komma vor « à seize heures »); keine Variante überzeugend; Satz geändert zu « J'ai une réunion à seize heures, tu viens ? » (Mr. Alex, 17.10., Variante d), neu aufgenommen. ☑ |
| ☐ | fr | Lob « Bingo, c'est ça ! »: « Bingo » englisch gesprochen | 17.10.: zwei Vorlese-Varianten geschickt (« Baingo » / « Bin-go »); Eintrag ersetzt durch « Gagné ! » (17.10.), Bingo-Aufnahme entfernt. ☑ |
| ☑ | es | « Hoy » am Satzanfang mit hörbarem H | Vorlese-Schreibung « Oy » (ganzes Wort), drei Sätze neu (pr_15, co_22, de_22), 17.10. |
| ☑ | tr | « saat »: langes a klingt dumpf | Vorlese-Schreibung « sa-at » (alle Formen), 24 Satzaufnahmen in 8 Einträgen neu, 17.10. (Hörprobe an Mr. Alex) |
