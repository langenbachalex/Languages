"""Sprachpaket Arabisch (Ziel) – Deutsch (Hilfe). Studie und Entscheidungen: docs/ar/studie.md
Hocharabisch (gebildetes gesprochenes Standardarabisch, Pausalformen) mit saudischer Stimme; syrische Abweichungen als fester Bestandteil
(Zeile « Syrisch » je Wendung mit Knopf « Şām », Zeile « in Syrien » je Laut, Kasten je Grammatiklektion).
Anzeige dreizeilig: Schrift mit Taschkīl, Umschrift, Deutsch. Vor den Themen: Schriftmodul (Buchstaben) und drei Lautmodule.
TSV-Felder wie in allen Paketen: fr = Zielsprache, de = Hilfssprache; zusätzlich umschrift(_w), wurzel, syrisch, syrisch_u."""
import os

PAAR = "ar-de"
NAME = "عربيّتي"
KURZ = "AR"
HILFE_KURZ = "DE"
FLAGGE = "🇸🇦"
LANG = "ar"
LANG_HILFE = "de"
SPRACHAUSGABE = "ar-SA"
TEMPO = 0.7
# Grün und Gold; hell und dunkel wie bei den anderen Sprachen
THEME = {"blau": "#1b6b45", "rot": "#b8860b", "rot_text": "#ffffff", "dunkel": {"blau": "#7fd4a6", "blau_text": "#07180f", "rot": "#e6c15a", "rot_text": "#1a1200"}}

# Themen folgen nach Schrift- und Lautmodulen (Thema 9 = « Arabische Wörter, die du schon kennst »)
THEMEN = []

# Titel – von der Dattel bis zur Kunāfa
TITEL = [(0, "تَمْر", "🌴"), (300, "قَهْوَة", "☕"), (900, "فَتُّوش", "🥗"), (1800, "شَاوَرْمَا", "🌯"),
         (3000, "كِبَّة", "🥘"), (4500, "بَقْلاوَة", "🍯"), (6500, "كُنَافَة", "👑")]
TITEL_ANSAGE = "مَبْرُوك! أَنْتَ الآنَ {name}!"
SPIEL_TEXTE = {  # gesprochen vom Erzähler (audio/spiel/<id>.mp3)
    "feuer": "اِشْتَعَلْتَ! ثَلاثَةُ أَيَّامٍ مُتَتَالِيَة!",
    "woche": "أُسْبُوعٌ كَامِل! دَرَسْتَ كُلَّ يَوْمِ مَدْرَسَة. أَحْسَنْت!",
    "monat": "أَرْبَعَةُ أَسَابِيعَ كَامِلَةٍ مُتَتَالِيَة! بَطَلٌ حَقِيقِيّ!",
    "fini": "هَذَا كُلُّ شَيْءٍ لِلْيَوْم. إِلَى الغَد!",
}

# Dialoge: Rolle A = Alex (Mr. Alex' Klon auf Arabisch), Rolle B = Khalid (Stimme « Ali – calm & deep Saudi »)
ROLLEN = {"A": "Alex", "B": "خالد"}
DIALOGE_TITEL = ["حِوَارَات مَعَ خَالِد", "Dialoge mit Khalid"]
ERZAEHLER = "b"      # Khalids Stimme erzählt (Sätze, Geschichte, Orte); Mr. Alex spricht nur seine Dialogseite
LOB_STIMME = "b"

# Geschichte in Damaskus
GESCHICHTE = {"titel": "سِرُّ الجَامِعِ الأُمَوِيّ",
              "unter": "مُعَلِّمٌ فِي دِمَشْق، تَذْكِرَةٌ قَدِيمَة، وَقِطٌّ يَعْرِفُ كُلَّ شَيْء.",
              "sammlung": ["كُلُّ أُسْبُوعٍ كَامِلٍ يَفْتَحُ فَصْلاً: مُعَلِّمٌ فِي دِمَشْق وَسِرُّ الجَامِعِ الأُمَوِيّ.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: ein Lehrer in Damaskus und das Geheimnis der Umayyaden-Moschee."]}

# Schriftmodul: 29 Buchstaben (28 + Hamza) in sechs Formgruppen, vor den Lautmodulen
SCHRIFT = {"datei": "huruf.tsv", "symbol": "✍️", "titel": "الحُرُوف", "de": "Die Buchstaben",
           "gruppen": [("g1", "ا ب ت ث ن ي", "Alif und die Zahnbuchstaben"), ("g2", "ج ح خ", "Die Kehlgruppe"), ("g3", "د ذ ر ز و", "Die Nicht-Verbinder"),
                       ("g4", "س ش ص ض", "Sīn und die Emphatischen"), ("g5", "ط ظ ع غ", "Tiefe Laute"), ("g6", "ف ق ك ل م ه ء", "Der Rest und Hamza")]}

# Lautmodule (folgen): neue Konsonanten · Länge und Verdopplung · Hamza und Wortenden
TRAEGERSATZ = "اِسْمَعْ جَيِّدًا: {wort}."
AUSSPRACHE = []

# Karte: Syrien und Saudi-Arabien (folgt), Start Damaskus, Einschub Damaskus-Altstadt
KARTE = {"name": "سُورِيَا وَالسُّعُودِيَّة", "einheit": "مُحَافَظَة", "lieux": "مَكَان", "start": "دِمَشْق",
         "quelle": "Karte: Natural Earth (gemeinfrei).",
         "badge": "رِحْلَة الشَّام",
         "hinweis": ["كُلُّ جَلْسَةٍ وَكُلُّ جُزْءٍ يَفْتَحُ مَكَانًا، اِبْتِدَاءً مِنْ دِمَشْق. اِلْمِسْ مَكَانًا!",
                     "Jede fertige Sitzung und jeder fertige Teil schalten einen Ort frei, Start in Damaskus. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import arabien_karte
    return arabien_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen (ElevenLabs, Hörproben 18.10.): Mr. Alex' Klon auf Arabisch; Khalid = « Ali – calm & Deep Arabic Saudi Narrator »; Şām = « Yazan Syrian »
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "ar", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "MI88rOZjXbH22N8KHXUo", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_S = {"id": "pIPrJAPlpTZzoh1Pzjgr", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
AUSSPRACHE_KORREKTUR = {}

# Oberflächentexte: [Zielsprache, Hilfe] oder nur Zielsprache; kurze Knöpfe mit Umschrift, solange die Schrift neu ist
UI = {
    "app": "Language Learning",
    "gruss": ["أَهْلاً! نَبْدَأ؟", "مَرْحَبًا! هَيَّا بِنَا!", "مَسَاءَ الخَيْر! جَلْسَةٌ قَصِيرَة؟"],
    "motto": ["عَشْرُ دَقَائِقَ فِي اليَوْم: الجَلْسَةُ أَوَّلاً، ثُمَّ مَا تَشَاء.", "Zehn Minuten am Tag: die Sitzung zuerst, danach was du willst."],
    "seance": "▶ هَيَّا نَبْدَأ · hayyā nabdaʾ", "seance_fertig": "✓ تَمَّ اليَوْم",
    "seance_stand": "{neu} جَدِيد · {wdh} مُرَاجَعَة · {fertig} / {gesamt} تَمّ",
    "seance_leer": "لا مُرَاجَعَةَ اليَوْم – اِكْتَشِفِ المَوَاضِيع!",
    "themen": ["المَوَاضِيع", "Die Themen"], "expressions": "عِبَارَة", "parties": "جُزْء",
    "bonus": ["النُّطْق وَالقِصَّة", "Aussprache und Geschichte"],
    "schrift": ["الحُرُوف", "Die Buchstaben"], "schrift_ansage": ["اُنْظُرْ، اِسْمَعْ، كَرِّر. كُلُّ حَرْفٍ لَهُ ثَلاثَةُ أَشْكَال.", "Schau, hör, sprich nach. Jeder Buchstabe hat drei Gestalten."],
    "harf_karte": "الحَرْف", "harf_hoeren": "اِسْمَعْ وَاخْتَر", "harf_finden": "اِبْحَثْ عَنِ الحَرْف", "harf_n": "حَرْف {n} / {alle}",
    "formen": ["مُنْفَصِل", "فِي البِدَايَة", "فِي الوَسَط", "فِي النِّهَايَة"], "formen_de": ["allein", "am Anfang", "in der Mitte", "am Ende"],
    "harf_hoeren_ansage": ["اِسْمَعِ اسْمَ الحَرْف. أَيُّ حَرْفٍ هُوَ؟", "Hör den Namen des Buchstabens. Welcher ist es?"],
    "harf_finden_ansage": ["اِسْمَعِ الكَلِمَة. أَيُّ حَرْفٍ يُعْطِي الصَّوْتَ {laut}؟", "Hör das Wort. Welcher Buchstabe macht den Laut {laut}?"],
    "nicht_verbinder": "لا يَتَّصِلُ بِمَا بَعْدَه – verbindet nicht nach links",
    "grammatik": ["القَوَاعِد", "Grammatik"], "grammatik_thema": "قَوَاعِدُ هَذَا المَوْضُوع", "grammatik_ansage": ["القَاعِدَة، الأَمْثِلَة، ثُمَّ أَنْت.", "Die Regel, die Beispiele, dann du."],
    "regel": ["القَاعِدَة", "Die Regel"], "beispiele": ["أَمْثِلَة – سَمِعْتَهَا كُلَّهَا", "Beispiele – alle schon gehört"], "kontrast": ["قَارِن", "Vergleich"],
    "bilde": ["كَوِّنِ الصِّيغَة", "Bilde die Form"], "bilde_ansage": ["اِقْرَأِ الصِّيغَة وَاخْتَرِ الشَّكْلَ الصَّحِيح.", "Lies die Formel, wähl die richtige Form."],
    "hoer": ["اِسْمَعْ وَقَرِّر", "Hör und entscheide"], "richtig": "صَحِيح!", "falsch": "لا – حَاوِلْ مَرَّةً أُخْرَى.", "satz_n": "الجُمْلَة {n}",
    "syrisch": "سُورِي · Syrisch", "sham": "شَام", "wurzel_titel": "Wurzel",
    "kapitel_zahl": "{frei} / {alle} فَصْل · فَصْلٌ جَدِيدٌ كُلَّ أُسْبُوعٍ كَامِل",
    "stand": ["{n} عِبَارَة فِي صُنْدُوقِك · {fest} رَاسِخَة · {orte} / {alle} مَكَان",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "الرَّئِيسِيَّة", "zurueck_accueil": "← الرَّئِيسِيَّة", "zurueck_thema": "← المَوْضُوع", "suivant": "التَّالِي ➜", "retour": "◀ رُجُوع",
    "encore_hoeren": "🔊 مَرَّةً أُخْرَى", "solution": "الحَلّ · al-ḥall", "hoeren": "🔊 اِسْمَع", "stop": "■ قِف",
    "jetzt_du": "دَوْرُك! كَرِّر.", "jetzt_du_dialog": "دَوْرُك! قُلْ جُمْلَتَك.",
    "poli": "حَضْرَتُك · رَسْمِيّ", "poli_titel": "Höflichkeitsform", "trou": "فَرَاغ", "hilfe_zeigen": "أَظْهِرِ الأَلْمَانِيَّة",
    "seance_titel": "صَالَةُ الكَلِمَات", "nouvelle": "جَدِيد", "revision": "مُرَاجَعَة · مُسْتَوَى {s}",
    "neu_ansage": ["عِبَارَةٌ جَدِيدَة! اِسْمَعْ وَكَرِّر.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "مِثَال", "ziel_sprache": "العَرَبِيَّة", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["كَيْفَ تَقُولُهَا بِالعَرَبِيَّة؟ قُلْهَا بِصَوْتٍ عَالٍ، ثُمَّ « الحَلّ ».", "Wie sagt man das auf Arabisch? Sag es laut, dann „al-ḥall“."],
    "je_savais": "😊 عَرَفْتُهَا", "encore": "🔁 مَرَّةً أُخْرَى", "pas_grave": "لا بَأْس! سَتَعُودُ قَرِيبًا.",
    "fini": "هَذَا كُلُّ شَيْءٍ لِلْيَوْم!", "pause": "اِسْتِرَاحَة!",
    "fini_text": ["صُنْدُوقُكَ مُحَدَّث. غَدًا تَعُودُ العِبَارَاتُ فِي وَقْتِهَا. إِنْ أَرَدْتَ المُتَابَعَة: المَوَاضِيع، بِلا ضَغْط.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["يُمْكِنُكَ مُتَابَعَةُ الجَلْسَةِ مَتَى شِئْت – مَا تَمَّ قَدْ تَمّ.", "Du kannst die Sitzung jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 مَجْمُوعَتِي",
    "etape": "خُطْوَة {n}", "zeitmaschine": "⏳ آلَةُ الزَّمَن", "trouve": "🔎 اِبْحَثْ عَنِ العِبَارَة",
    "thema_ansage": ["اِخْتَرْ جُزْءًا. كُلُّ جُزْء: اِسْمَعْ وَكَرِّرْ فِي ثَلاثِ خُطُوَات، آلَةُ الزَّمَن، ثُمَّ اِبْحَثْ عَنِ العِبَارَات.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "جُزْء {n}",
    "dialog_hoeren": "👂 اِسْمَع", "repeter": "كَرِّر", "tu_es": "🎭 أَنْتَ {rolle}", "role": "دَوْر", "repliques": "جُمْلَة",
    "dialog_start": "▶ اِبْدَأِ الحِوَار", "dialog_hoeren_knopf": "▶ اِسْمَعِ الحِوَار",
    "dialog_ok_rolle": "بَدِّلِ الدَّوْر – أَوْ مَرَّةً أُخْرَى!", "dialog_ok": "الآنَ دَوْرُكَ فِي الكَلام!",
    "dialog_ansage_rolle": ["أَنْتَ {ich}. قُلْ جُمَلَكَ عِنْدَمَا يَأْتِي دَوْرُك – التَّطْبِيقُ يَتَكَلَّمُ عَنْ {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. اِسْمَعِ الحِوَار.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["أَسْهَل: أَظْهِرْ جُمَلِي", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "الفَصْل {n}", "kapitel_ansage": ["اِسْمَعِ الفَصْلَ أَوِ اقْرَأْهُ بِصَوْتٍ عَالٍ. اِلْمِسْ فِقْرَةً لِلأَلْمَانِيَّة.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ اِسْمَعِ الفَصْلَ كُلَّه", "kapitel_weiter": "الفَصْلُ التَّالِي ➜",
    "kapitel_naechste": ["الفَصْلُ التَّالِي يُفْتَحُ مَعَ أُسْبُوعِكَ الكَامِلِ القَادِم.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["التَّتِمَّةُ تُكْتَبُ الآن.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "لَمْ يُفْتَحْ بَعْد", "semaine_parfaite": "أُسْبُوعٌ كَامِل",
    "mot": "كَلِمَة {n} / {alle}", "paire": "زَوْج {n} / {alle}", "lentement": "🐢 بِبُطْء", "normal": "🔊 عَادِي",
    "lr_label": "اِسْمَعْ وَكَرِّر", "parties_label": "الأَجْزَاء – وُصُولٌ مُبَاشِر",
    "trop_vite": "⏱️ بِسُرْعَةٍ زَائِدَة!", "trop_vite_text": ["قُلِ الجُمَلَ بِصَوْتٍ عَالٍ حَقًّا. عِنْدَهَا تُوجَدُ نِقَاطٌ أَيْضًا. مَرَّةً أُخْرَى!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "مَرَّةً أُخْرَى ➜", "termine": "{name}: تَمّ!", "presque": ["تَقْرِيبًا! بَقِيَ:", "Fast! Es fehlt noch:"],
    "thema_fertig": "مَوْضُوعُ « {name} » تَمَّ كُلُّه. مَا شَاءَ الله!", "autres_parties": "الأَجْزَاءُ الأُخْرَى",
    "stufen": [["اِسْمَعْ وَكَرِّر! الجُمْلَةُ الأَلْمَانِيَّةُ تُسَاعِدُك.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["أَيُّ كَلِمَةٍ نَاقِصَة؟ قُلِ الجُمْلَةَ كُلَّهَا، ثُمَّ « الحَلّ ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „al-ḥall“."],
               ["قُلِ الجُمْلَةَ بِالعَرَبِيَّة، ثُمَّ « الحَلّ ».", "Sag den Satz auf Arabisch, dann „al-ḥall“."]],
    "dis_phrase": "قُلِ الجُمْلَةَ كُلَّهَا بِالعَرَبِيَّة!", "phrase": "جُمْلَة {n} / {alle}",
    "tipp_buchstabe": ["أَسْهَل: الحَرْفُ الأَوَّل", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["أَسْهَل: جُمْلَةٌ بِفَرَاغ", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["اليَوْم", "المُضَارِع"], "pc": ["أَمْس", "المَاضِي", "وَأَمْس؟"], "fp": ["غَدًا", "المُسْتَقْبَل (سَـ)", "وَغَدًا؟"]},
    "solution_zeit": "الحَلّ: {zeit}",
    "zeit_ansage": ["اِسْمَعْ جُمْلَةَ اليَوْم. ثُمَّ قُلْهَا فِي المَاضِي وَفِي المُسْتَقْبَل – بِصَوْتٍ عَالٍ. ثُمَّ « الحَلّ ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „al-ḥall“."],
    "expression": "عِبَارَة {n} / {alle}",
    "bonus_weekend": "🏖️ مُكَافَأَةُ نِهَايَةِ الأُسْبُوع +{p}", "en_feu": "اِشْتَعَلْت! {n} أَيَّام مُتَتَالِيَة", "en_feu_text": "{n} أَيَّام مَدْرَسَة مُتَتَالِيَة – +{p} نُقْطَة!",
    "semaine_parfaite_titel": "أُسْبُوعٌ كَامِل!", "semaine_parfaite_text": "دَرَسْتَ كُلَّ يَوْمِ مَدْرَسَة – +{p} نُقْطَة.",
    "nouveau_chapitre": " فَصْلٌ جَدِيد: « {titel} »!", "suite_bientot": " تَتِمَّةُ القِصَّةِ قَرِيبًا.",
    "mois_parfait": "شَهْرٌ كَامِل!", "mois_parfait_text": "{n} أَسَابِيع كَامِلَة مُتَتَالِيَة – +{p} نُقْطَة وَإِطَارٌ ذَهَبِيّ!",
    "nouveau_titre": "لَقَبٌ جَدِيد: {name}!", "points": "نُقْطَة", "jours_suite": "أَيَّام مَدْرَسَة مُتَتَالِيَة",
    "visite": "تَمَّتِ الزِّيَارَة ✓",
    "ton_titre": "لَقَبُك", "encore_points": "{n} نُقْطَة أُخْرَى لِـ« {name} » {symbol}",
    "cette_semaine": "هَذَا الأُسْبُوع", "tage": ["اثن", "ثلا", "أرب", "خمي", "جمع"],
    "serie_text": ["🔥 {n} أَيَّام مَدْرَسَة مُتَتَالِيَة · ⭐ {w} أُسْبُوع كَامِل. العُطَلُ لا تُحْسَب – سِلْسِلَتُكَ تَبْقَى.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 صُنْدُوقِي ({n} عِبَارَة)", "boite_text": ["المُسْتَوَى 0 = جَدِيد أَوْ مَنْسِيّ · مِنَ المُسْتَوَى 3 تَكُونُ العِبَارَةُ رَاسِخَة.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "ي", "badges": "الشَّارَات",
    "badge_liste": ["اِشْتَعَلْت", "أُسْبُوعٌ كَامِل", "5 × كَامِل", "شَهْرٌ كَامِل", "بَطَلُ نِهَايَةِ الأُسْبُوع", "100 عِبَارَة", "50 رَاسِخَة"],
    "offline": "📥 بِدُونِ اتِّصَال", "offline_text": ["حَمِّلْ أَصْوَاتَ هَذِهِ اللُّغَةِ لِلتَّدْرِيبِ بِدُونِ اتِّصَال.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} مِلَفّ صَوْتِيّ بِدُونِ اتِّصَال", "offline_laden": "📥 حَمِّلْ لِلاسْتِخْدَامِ بِدُونِ اتِّصَال", "offline_fertig": "✓ مُتَاحٌ بِدُونِ اتِّصَال",
    "bald": "قَرِيبًا",
    "offline_laeuft": "جَارِي التَّحْمِيل… {n} / {alle}",
}
