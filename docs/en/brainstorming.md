# Brainstorming: Englisch (britisch) – « Mastery » statt Grundwortschatz

> **WIEDER AUFGENOMMEN (Mr. Alex, 16.10.2026).** Vor jedem Bauschritt fragen. Simons Stimme ist im Konto: « Simon T », ID `idD5c2qhqB8tWCuqP5sv` (geklont, Received Pronunciation). Mr. Alex' Klon ist jetzt als britisches Englisch gekennzeichnet.
>
> **Rahmenfakten (Stand 16.10.):** Britisches Englisch, Niveau nahe oder über Muttersprachler, Ziel nuancierter und pointierter Ausdruck in Umgangs-, akademischem und literarischem Register, volle Beherrschung fortgeschrittenen Vokabulars. **Bilingual:** Deutsch bleibt fester Bestandteil (Entsprechung neben jedem Wort und Satz), englische Gloss zusätzlich. **Stimmen:** Mr. Alex' Klon auf britischem Englisch (gerolltes r ggf. per Schreibung forcieren) plus **Simon**, ein Freund (ID oben); Lautstärke wird automatisch angeglichen. **Pensum** 3 + 8. **Karte und Geschichte ja**; Geschichte als eigene Erzählung in der Welt des Buchs. **Buch:** « The Dragonbone Chair » (Tad Williams), sonst « The Lord of the Rings » / « The Silmarillion »; geschützt, Text nur über Ladeweg auf dem Gerät, nicht ins Repository; archive.org von hier nicht erreichbar, Text muss Mr. Alex liefern. **Buch zuerst:** « The Silmarillion » (Mr. Alex hat den Text am 16.10. als Markdown hochgeladen, 154.000 Wörter, Seitenzahlen als Überschriften; liegt nur in der Sitzung, nie ins Repository). **Karte: Beleriand** (bestätigt 16.10.), selbst gezeichnet aus den Ortsnamen des Buches, ca. 25–30 Regionen und 50 Orte, Start **Menegroth**. **Stimmen:** Hörprobe vom 16.10. bestanden (Klon und Simon). **Erste Achse: Precision pairs.** **Geschichte:** Erzähler ist einer der Noldor mit dem Namen **Barangollach**, eigene Erzählung in Beleriand. **Ort der App:** eigene Web-App unter `app/english/` im selben Repository (Option 3, Mr. Alex 16.10.): gleicher Motor, gleiche Werkzeuge, eigener Speicher `english-v1`, eigener Offline-Speicher `en-…`, Adresse https://langenbachalex.github.io/Languages/english/. **Gebaut 16.10.:** Gerüst (Paket `en_de.py`, Oberfläche, Lob mit Übersetzung, Titel-Leiter, Farben, Simon als Partner), dazu Lob/Titel/Gruß im Ton des Silmarillion (Voranstellung, gehobenes Vokabular), Titel-Leiter Wanderer … High King of the Noldor … Named in Song, Geschichte Kapitel 1 « The Noldolantë, as Barangollach tells it » (10 Absätze, Audio), Karte Beleriand (24 Regionen, 50 Orte mit Fakten und Audio, Start Menegroth), 155 Audios. Veröffentlicht 16.10. **Lektion 1 « In the Council » gebaut 16.10.:** 24 Wendungen aus den Reden der Elben in « The Council of Elrond » (Buch II, Kap. 2), Zitate im Original (Freigabe Mr. Alex: Buchtext darf ins Repository), Registermaschine statt Zeitmaschine (im Rat / unter Freunden / schlicht), zwei Dialoge Barangollach–**Ninuivor** (Simon), Lob-Schicht im Ton des Rats; **alles Lob spricht ausschließlich Simon** (LOB_STIMME = b). Buchtext liegt in der Sitzung (Scratchpad), Kapitel 7145–7708 der Markdown-Datei. Nächste Lektionen: weitere Kapitel oder Precision pairs. **Nichts gebaut, keine Audios in der App.**

Stand: 14.10.2026. **Nur Machbarkeit und Überblick, nichts gebaut, keine Audios.** Grundlage: Vorgaben Mr. Alex (14.10.): eigene Stimme plus Simon (noch einzupflegen, Lautstärke angeglichen), Niveau nahe oder über Muttersprachler, Ziel: nuancierter, pointierter Ausdruck im Umgangs-, akademischen und literarischen Register; vollständige Beherrschung fortgeschrittenen Vokabulars; optional Literaturbegleitung (Buch als Markdown, Vokabeln Kapitel für Kapitel).

## 1. Was anders ist als bei den vier bisherigen Sprachen

| | Bisher (fr, es, it, de) | Englisch |
|---|---|---|
| Ziel | Alltagsphrasen, Idiome, Grundtempora | Präzision, Register, Konnotation, seltene und literarische Wörter |
| Einheit | die Wendung (3 Wörter) mit einem Beispielsatz | das **Wort oder die Wendung im Kontrast**: Bedeutung, Register, Kollokationen, nahe Synonyme und ihr Unterschied |
| Hilfssprache | Deutsch (Tipp-Text) | **Englisch selbst** (Definition, Beispiel, Synonymfeld); Deutsch höchstens als letzte Stufe hinter einem zweiten Tipp |
| Übungstyp | hören, nachsprechen, Lücke, Zeitmaschine | **wählen, formulieren, umformulieren**: Welches Wort passt hier (und warum nicht das andere)? Sag denselben Gedanken in drei Registern. |
| Humor | Assimil-Ton in den Sätzen | bleibt, aber die Sätze sind länger und tragen das Wort im Kontext (ein Satz, der das Wort braucht) |
| Partner | Aurélien, Diego, Giovanni | **Simon** (Brite); Rolle noch offen: Kollege, Autor, Dozent? |
| Oberfläche | Zielsprache mit Tipp | Englisch, ohne Tipp-Ebene; die Hilfe ist eine zweite englische Ebene (Definition statt Übersetzung) |

Der Kern der App (Leitner-Kasten, Séance, Punkte, Serie, Karte, Geschichte, Offline, Audio-Erzeugung) bleibt nutzbar. Neu sind **Übungsformen**, die das bestehende Sprachpaket-Format nicht hergibt. Das ist der eigentliche Bauaufwand.

## 2. Machbarkeit: was die bestehende App kann und was neu wäre

**Direkt wiederverwendbar (kein Code):**
- Sprachpaket `en` mit eigener Oberfläche, Lob (britisch: « Spot on. », « Quite. », « Bang on. », « Nicely put. »), Titel-Leiter, Farben, Umschalter 🇬🇧.
- Leitner mit 3 + 8 pro Tag; Intervalle; Punkte; Serie; Offline.
- Audio-Erzeugung: Klon mit `language_code: en` (britisches Englisch braucht eine Hörprobe: der v4-Klon folgt eher dem Text als dem Akzent; das muss getestet werden), Simon als zweite Stimme, Lautstärke-Angleich ist jetzt automatisch.
- Dialoge mit Rollen (für Register-Kontraste gut geeignet: dieselbe Szene einmal casual, einmal formal).
- Karte (Großbritannien, Counties; freie Daten gibt es: ONS Open Geography, OGL-Lizenz) und Geschichte (Kapitel pro perfekte Woche) als Belohnung.

**Anpassung mit wenig Code:**
- **Zweite englische Ebene statt Übersetzung:** Das Feld `satz_de` wird zur Definition oder Paraphrase, `deutsch` zur Kurzdefinition. Der Tipp-Knopf heißt « Gloss » statt « Deutsch anzeigen ». Die Notiz (bisher Grammatik-Hinweis) wird zum **Usage note**: Register, Kollokationen, häufige Fehler, Etymologie, wenn sie beim Behalten hilft.
- **Zeitmaschine → Registermaschine:** Die drei Zeitstufen (heute / gestern / morgen) werden zu drei Registern: *casual / neutral / formal* oder *spoken / written / literary*. Derselbe Mechanismus, andere Beschriftung, andere Spalten. Beispiel: « He's a bit of a plonker » → « He's not the sharpest » → « He is somewhat lacking in judgement ».
- **Lückensatz → Wortwahl:** Statt eines Lückenworts wird zwischen zwei nahen Synonymen gewählt (*persuade / convince*, *imply / infer*, *disinterested / uninterested*). Das ist technisch das Minimalpaar aus dem Aussprachemodul, auf Wörter übertragen.

**Neu zu bauen (eigene Übungsform):**
- **Formulierungsübung:** Ein Gedanke auf Deutsch oder als neutrale englische Paraphrase, Aufgabe: pointiert englisch sagen, dann Musterlösung hören (deine Stimme) und zwei Alternativen in anderen Registern (Simon). Kein Rechts/Falsch, sondern Selbstbewertung wie bei « Je savais / Encore ».
- **Literaturbegleitung** (Abschnitt 4).

## 3. Mögliche Inhaltsachsen (Vorschlag, zur Auswahl)

1. **Precision pairs** – nahe Synonyme mit Unterschied: *historic / historical, continual / continuous, flaunt / flout, discreet / discrete, enervate / energise, fortuitous / fortunate, nauseous / nauseated, comprise / compose, less / fewer, who / whom, which / that*. 24 Paare pro Teil.
2. **Register ladders** – ein Gedanke in drei bis vier Stufen: *knackered → shattered → exhausted → spent*; *skint → broke → hard up → impecunious*; *chuffed → pleased → gratified*. Hier liegt der britische Ton.
3. **Literary and learned vocabulary** – Wörter, die man liest, aber selten hört, mit sicherer Aussprache: *lugubrious, perspicacious, obsequious, recondite, sanguine, mellifluous, insouciant, lachrymose, pellucid, ineffable, apotheosis, quotidian, verisimilitude, sententious, bathos, liminal, palimpsest*. Aussprache ist hier der eigentliche Nutzen deiner Stimme.
4. **Academic prowess** – Hedging, Stance, Argumentstruktur: *it would appear that, arguably, by no means, to the extent that, notwithstanding, this is not to say, it is worth noting, I would venture*; Konnektoren mit Nuance (*albeit, whereas, insofar as, inasmuch as, hence, thereby*); Latinismen in Maßen (*a fortiori, pace, sic, viz., cf., ibid., prima facie, ceteris paribus*).
5. **Casual command** – britischer Alltag, Understatement, Ironie: *not half, I don't mind if I do, fair enough, can't be arsed, taking the mickey, Bob's your uncle, it's not rocket science, bless, cheers, ta, sorted, dodgy, faff, knackered, gutted, chuffed, skint, peckish, miffed*. Mit Hinweis, was in welchem Milieu geht.
6. **Idioms with history** – Wendungen, deren Bild man kennen sollte: *the whole nine yards, by and large, hoist with his own petard, a dead ringer, the bee's knees, to go the whole hog, cold turkey, red herring*. Mit Herkunft als Notiz (das ist dein Assimil-Humor-Platz).
7. **Phrasal verbs, die man nicht aus dem Lehrbuch hat** – *to tide over, to wing it, to fob off, to hold forth, to bear out, to pan out, to own up, to while away, to mull over*.
8. **Pronunciation for the near-native** – was Deutsche noch verrät: *th* ist kein Problem mehr, aber **Wortbetonung** (*CONtroversy / conTROversy*, *harASS / HARass*), **stumme Buchstaben** (*subtle, indict, victuals, Worcester, Leicester, Marylebone, quay, colonel*), **Vokalqualität** (*bath / trap, cot / caught, pull / pool*), **Intonation** von Understatement und Ironie. Als Aussprachemodul nach dem bestehenden Muster: Minimalpaare und « beide in einem Wort » funktionieren hier eins zu eins.
9. **False friends for the advanced** – nicht *become / bekommen*, sondern *eventually / eventuell, sensible, actual, brave, chef, gift, pathetic, sympathetic, sensible, genial, fabric, billion* und die britisch-amerikanischen Fallen (*pants, chips, first floor, quite, table a motion*).

Alle Achsen passen in das bestehende Format « 24 Einträge pro Thema, 3 Teile à 8 », mit den oben genannten Anpassungen.

## 4. Literaturbegleitung: Machbarkeit

**Idee:** Ein Buch als Markdown in `inhalte/en/buecher/<titel>.md`; pro Kapitel werden Vokabeln ausgewählt und als Thema in den Leitner-Kasten übernommen; der Kapiteltext selbst ist in der App lesbar, mit Tipp auf ein Wort für Gloss und Audio.

**Was gut geht:**
- Markdown einlesen, Kapitel erkennen, Text in der App anzeigen: das ist dieselbe Mechanik wie die Geschichte (Absätze mit Audio). Ohne Audio für den ganzen Text ist es trivial; mit Audio für ganze Kapitel wird es teuer (ein Roman mit 100.000 Wörtern sind rund 600.000 Zeichen, bei ElevenLabs etwa 60 Kapitel à 10.000 Zeichen).
- **Vokabelauswahl pro Kapitel:** halbautomatisch. Ich ziehe aus dem Kapitel die seltenen Wörter (Häufigkeitsliste, etwa die 20.000 häufigsten englischen Wörter als Filter), du streichst und ergänzt; ich schreibe Gloss, Register-Hinweis und den Beispielsatz **aus dem Buch selbst** (das ist der Gewinn: das Wort im Originalkontext). Daraus wird ein normales Thema mit 24 Einträgen, Audio nur für Wort und Satz.
- **Fortschritt:** Kapitel freischalten wie die Geschichte, aber nicht nach perfekter Woche, sondern wenn das Kapitel-Vokabular im Kasten ist. Lesen und Lernen laufen dann parallel.

**Was zu klären ist:**
- **Urheberrecht:** Gemeinfreie Bücher (Austen, Dickens, Conrad, Woolf bis 1941, Orwell ab 2021 in der EU) sind unproblematisch und für dein Ziel ohnehin ergiebig (Wodehouse für den Ton, Woolf für den Satz, Conrad für das Vokabular). Ein aktuelles Buch dürfte nur privat, nicht veröffentlicht auf GitHub Pages liegen; dafür bräuchte es einen Ladeweg, der den Text im Browser behält (Datei auf dem Gerät öffnen, nicht ins Repository). Das ist machbar, aber ein eigener Schritt.
- **Größe:** Ein Roman als Text sind 500 KB bis 1 MB; als Datei im Repository kein Problem, im Offline-Speicher auch nicht.
- **Vokabelmenge:** Bei einem anspruchsvollen Roman kommen pro Kapitel leicht 30 bis 60 seltene Wörter zusammen. Mit 3 neuen pro Tag ist das ein Kapitel pro zwei Wochen. Entweder höheres Pensum für Englisch (du bist hier nicht Anfänger: 8 + 15?) oder strengere Auswahl (nur Wörter, die du behalten willst, nicht alle unbekannten).

**Empfehlung:** Mit einem gemeinfreien Buch anfangen, Kapitel 1 als Probe: Markdown einlesen, Vokabelliste automatisch ziehen, du wählst, ich baue das Thema. Wenn das Format sitzt, der Rest.

## 5. Festgelegt (Mr. Alex, 14.10.)

- **Bilingual bleibt.** Deutsch ist fester Bestandteil, nicht nur Notfallebene: Die deutsche Entsprechung steht neben jedem englischen Wort und jeder Wendung, weil es ums Denken in beiden Sprachen geht. Die englische Gloss (Definition, Synonymfeld) kommt dazu, ersetzt das Deutsche aber nicht. Praktisch: `deutsch` = deutsche Entsprechung(en), `satz_de` = deutsche Fassung des Satzes, Notiz = Usage note auf Englisch mit deutschem Vergleich, wo er hilft (« das Deutsche hat dafür zwei Wörter / kein Wort »).
- **Stimme:** der Klon hat britisches Englisch eingesprochen; `language_code: en`, Hörprobe trotzdem, weil der Klon im Test stellenweise ein gerolltes oder rhotisches r gesprochen hat. Falls nötig, wird britische Aussprache über die Schreibung im Audiotext forciert (wie « Mess » für Metz): AUSSPRACHE_KORREKTUR im Sprachpaket.
- **Simon ist ein Freund** (kein Kollege, kein Dozent).
- **Karte und Geschichte: ja.** Geschichte **auf dem Buch aufbauend**, das auch die Literaturbegleitung trägt.
- **Buch:** « The Dragonbone Chair » (Tad Williams, 1988, Memory, Sorrow and Thorn 1), Link auf archive.org (Leihbibliothek, nur mit Konto ausleihbar, DRM). Aus dieser Umgebung nicht lesbar (archive.org ist gesperrt); der Text müsste von Mr. Alex selbst bereitgestellt werden. Urheberrechtlich geschützt: Der Buchtext darf **nicht** ins öffentliche Repository, nur über einen Ladeweg, der ihn auf dem Gerät behält. Die Geschichte in der App muss eine **eigene Erzählung in der Welt und im Ton des Buches** sein, keine Nacherzählung.
- **Alternativ:** « The Lord of the Rings » und « The Silmarillion » (Tolkien). Urheberrechtlich dieselbe Lage: geschützt (in EU und UK bis 2044), Text nur über den Ladeweg auf dem Gerät, nicht ins Repository; Geschichte in der App als eigene Erzählung in der Welt, keine Nacherzählung.
- **Pensum bleibt** 3 neue + 8 alte pro Tag.
- **Noch nichts bauen.** Weitere Entscheidungen folgen.

## 6. Offene Entscheidungen (vor jedem Bauschritt)

1. **Zweite Stimme:** Simon ist noch nicht im Konto. Sobald du ihn eingepflegt hast, brauche ich die Stimmen-ID; dann Hörprobe deiner Stimme auf britischem Englisch und Simon im Vergleich.
2. ~~Pensum~~ entschieden: 3 + 8 wie bisher.
3. ~~Hilfsebene~~ entschieden: Deutsch bleibt fester Bestandteil, englische Gloss zusätzlich.
4. **Welche Achsen zuerst?** Mein Vorschlag für den Start: *Precision pairs* (passt in das bestehende Format fast ohne Code), dann *Register ladders* (braucht die umgebaute Zeitmaschine), dann *Literary vocabulary* mit Aussprache.
5. ~~Simons Rolle~~ entschieden: ein Freund.
6. ~~Buch~~ entschieden: The Dragonbone Chair, sonst The Lord of the Rings / The Silmarillion; offen: wie der Text in die Arbeit kommt (Datei von Mr. Alex).
7. ~~Karte und Geschichte~~ entschieden: beides ja, Geschichte in der Welt des Buches (eigene Erzählung).

## 7. Aufwand (grob)

| Schritt | Aufwand |
|---|---|
| Sprachpaket `en`, Oberfläche, Lob, Titel, Umschalter | ein Thema-Schritt wie bisher |
| Hilfsebene umbauen (Gloss statt Übersetzung) | klein, im Code |
| Registermaschine (Zeitmaschine umbeschriften) | klein, im Code und in den Daten |
| Wortwahl-Übung (zwei Synonyme) | mittel, neue Übungsform auf Basis der Minimalpaare |
| Formulierungsübung mit Selbstbewertung | mittel |
| Literaturbegleitung: Markdown einlesen, Kapitel anzeigen, Vokabeln ziehen | mittel bis groß, in Stufen |
| Inhalte pro Achse | wie bisher: Vorschlag → OK → Audio → veröffentlichen |
