# Studie: Arabisch (syrisch / levantinisch) – Stimmen und Machbarkeit

Stand: 17.10.2026. Auftrag Mr. Alex: prüfen, ob es auf ElevenLabs genug hochwertige Stimmen für syrisches Arabisch gibt. Nichts gebaut.

## Stimmen in der ElevenLabs-Bibliothek (Abfrage 17.10.)
- Arabisch insgesamt: über 100 Stimmen; die meisten ägyptisch (57), saudisch (56), Golf (16), levantinisch (22), **syrisch 6**.
- Syrisch (Label « syrian »): Ghaida (w, jung, zwei Varianten, sehr oft geklont), Mr. FF (m, mittleres Alter), **Yazan Syrian** (m, « Damascene (Shami) dialect »), Marwan (m, levantinisch), Shami (m, Erzählung).
- Levantinisch: Fadi (Lebanese Conversational, m), Hadi N (m), Salma, Laloosh (w).
- Modelle: `eleven_multilingual_v2` und `eleven_v4` sprechen Arabisch; Mr. Alex' Klon über `language_code: ar`.

## Kernfrage Dialekt
Die Modelle kennen keinen Dialekt-Schalter. Was der Text in arabischer Schrift hergibt (شو، عم، بدي، رايح), liest die Stimme als Dialekt; eine syrische Stimme färbt die Aussprache (qāf als Hamza, Imāla, Betonung). MSA-Text bleibt MSA. Das heißt: **die Inhalte müssen durchgehend in syrischem Dialekt geschrieben sein**, Hilfssprache Deutsch, Umschrift als Zusatzzeile sinnvoll.

## Hörproben 17.10. (an Mr. Alex)
Klon, Yazan, Mr. FF, Fadi – derselbe Shami-Satz. Entscheidung offen.

## Offene Fragen vor dem Bau
1. Partnerstimme (Yazan / Mr. FF / Fadi / andere).
2. Schrift: arabische Schrift mit Umschrift darunter? (Empfehlung: ja, beides.)
3. Aussprache-Modul: emphatische Konsonanten, ʿayn / ḥāʾ / qāf-als-Hamza, kurze/lange Vokale – gut geeignet für Minimalpaare.
4. Karte: Syrien (Gouvernements, freie Daten: Natural Earth / HDX, OCHA) ab Damaskus; Geschichte in Damaskus.
