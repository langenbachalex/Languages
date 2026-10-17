# Studie: Türkisch – Stimmen und Machbarkeit

Stand: 17.10.2026. Auftrag Mr. Alex: « proper Turkish ». Nichts gebaut.

## Stimmen in der ElevenLabs-Bibliothek (Abfrage 17.10.)
- Türkisch: über 100 Stimmen, Labels « istanbul », « standard », « anatolian ». Reiche Auswahl, viele professionelle Sprecher.
- Männlich, Erzählung: **Hasan Yasin** (warm, conversational), Emrullah Tuna (tief), Onur Buyu, Mustafa Silici (Schauspieler), **Can** (jung, klar), Murat Albayrak.
- Weiblich: Füsun Tuncer, Aysegül Cakır, Elvan, Meloxia.
- Modelle: `eleven_multilingual_v2` und `eleven_v4`; Mr. Alex' Klon über `language_code: tr`.

## Besonderheiten
- Standardsprache ist eindeutig (Istanbul-Türkisch), kein Dialektproblem.
- Vokalharmonie und Agglutination: Einzelwörter sind weniger gefährdet als im Romanischen, aber Trägersatz-Mechanismus trotzdem nutzen.
- Aussprache-Modul: ı / i, ö / ü, weiches ğ, Betonung – ergiebige Minimalpaare.
- Karte: Türkei mit 81 İl (freie Daten: GADM / Natural Earth) ab Istanbul oder Izmir; Geschichte entsprechend.

## Entscheidungen Mr. Alex, 17.10.
- **Türkisch zuerst** (vor Arabisch).
- Partnerstimme: **Can** (`SacdY6cqu2yrF7ExGIOe`, eleven_multilingual_v2).
- Karte: Türkei mit İl, **Istanbul als 5–10 Stationen** (Sultanahmet, Galata, Kadıköy, Üsküdar, Beşiktaş, Eyüp, Bosporus, Prinzeninseln …), Start Istanbul.
- Partnerfigur **Cem**; Lernender Mr. Alex als Lehrer; Titel-Leiter Çay … Baklava; Geschichte in Istanbul; Istanbul-Stationen Sultanahmet, Kapalıçarşı, Galata, Beyoğlu, Beşiktaş, Kadıköy, Üsküdar, Adalar, danach Edirne, Bursa, İzmir, Ankara und das Land.
- **Gerüst gebaut 17.10.:** Paket `tr_de.py` (türkische Oberfläche, Lob mit Übersetzung, Titel, Farben Türkis/Rot, Cem = Stimme Can), Karte 81 İl (Natural Earth, `tuerkei_karte.py`), fünftes Paket in der Haupt-App (🇹🇷). Noch keine Themen, Audios, Orte, Geschichte. Thema 1 « Öğretmenler arasında » gebaut und aufgenommen 17.10. (24 Wendungen, Zeitmaschine -di/-ecek, 181 Audios). Veröffentlicht 17.10. Nächster Schritt: Thema 2 zur Freigabe.
