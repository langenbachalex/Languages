# Studie: Arabisch (syrisch / levantinisch) – Stimmen und Machbarkeit

Stand: 17.10.2026. Auftrag Mr. Alex: prüfen, ob es auf ElevenLabs genug hochwertige Stimmen für syrisches Arabisch gibt. Nichts gebaut.

## Stimmen in der ElevenLabs-Bibliothek (Abfrage 17.10.)
- Arabisch insgesamt: über 100 Stimmen; die meisten ägyptisch (57), saudisch (56), Golf (16), levantinisch (22), **syrisch 6**.
- Syrisch (Label « syrian »): Ghaida (w, jung, zwei Varianten, sehr oft geklont), Mr. FF (m, mittleres Alter), **Yazan Syrian** (m, « Damascene (Shami) dialect »), Marwan (m, levantinisch), Shami (m, Erzählung).
- Levantinisch: Fadi (Lebanese Conversational, m), Hadi N (m), Salma, Laloosh (w).
- Modelle: `eleven_multilingual_v2` und `eleven_v4` sprechen Arabisch; Mr. Alex' Klon über `language_code: ar`.

## Kernfrage Dialekt
Die Modelle kennen keinen Dialekt-Schalter. Was der Text in arabischer Schrift hergibt (شو، عم، بدي، رايح), liest die Stimme als Dialekt; eine syrische Stimme färbt die Aussprache (qāf als Hamza, Imāla, Betonung). MSA-Text bleibt MSA. Das heißt: **die Inhalte müssen durchgehend in syrischem Dialekt geschrieben sein**, Hilfssprache Deutsch, Umschrift als Zusatzzeile sinnvoll.

## Entscheidung Mr. Alex, 17.10.
- **Standard-Arabisch mit saudischer Stimme** (universell verständlich), nicht syrischer Dialekt als Grundlage.
- **Hinweise auf syrische Abweichungen bleiben in der App** (Notiz-Feld je Wendung: « in Syrien sagt man … »).
- Reihenfolge: Türkisch zuerst, Arabisch danach. Nichts gebaut.

## Offene Fragen vor dem Bau
1. Partnerstimme (Yazan / Mr. FF / Fadi / andere).
2. Schrift: arabische Schrift mit Umschrift darunter? (Empfehlung: ja, beides.)
3. Aussprache-Modul: emphatische Konsonanten, ʿayn / ḥāʾ / qāf-als-Hamza, kurze/lange Vokale – gut geeignet für Minimalpaare.
4. Karte: Syrien (Gouvernements, freie Daten: Natural Earth / HDX, OCHA) ab Damaskus; Geschichte in Damaskus.

## Entscheidungen Mr. Alex, 18.10. (Konzept bestätigt)
- Hocharabisch als Basis, **syrische Abweichungen als fester Bestandteil**: Zeile « Syrisch » je Wendung, Zeile « in Syrien » je Laut im Aussprachemodul, Kasten « Syrisch » je Grammatiklektion.
- **Schriftmodul: ja** (28 Buchstaben in sechs Formgruppen, vor den Lautmodulen).
- **Pausalformen: ja** (gebildetes gesprochenes Hocharabisch, Kasusvokale am Satzende fallen).
- **Karte: Syrien und Saudi-Arabien** auf einer Karte (Levante + Halbinsel), Start Damaskus, Einschub Damaskus-Altstadt.
- **Partner: Khalid** (saudische Männerstimme). Erzähler ebenfalls saudisch; Mr. Alex' Klon mit `language_code: ar` für seine Dialogseite (Test offen).
- **Syrisch-Knopf « 🔊 Şām »: ja** – die syrische Variante der Wendung, gelesen von einer syrischen Stimme (Yazan, Damaszener Dialekt).
- Aussprache vor den Themen: drei Module (neue Konsonanten · Länge und Verdopplung · Hamza und Wortenden), Anzeige dreizeilig (Schrift mit Taschkīl, Umschrift, Deutsch), Tempo 0,7×.
- Thema 9 wird « Arabische Wörter, die du schon kennst » (Lehnwörter im Deutschen, Türkischen, Spanischen).
- Geschichte « سرّ الجامع الأموي », Titel als Speisen (Tamr … Kunāfa).
- Reihenfolge: Stimmtests → Code (mehrere Lautmodule je Paket, Umschriftzeile, Wurzel in der Glosse, Şām-Knopf) → Schriftmodul → Lautmodule → Thema 1 + Lektion 1.
