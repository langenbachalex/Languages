"""Sprachpaket Englisch (britisch, Ziel) – Deutsch (Hilfe). Konzept: docs/en/brainstorming.md
Eigene Web-App unter app/english/ (bauen.py AUSGABEN), gleicher Motor wie die vier anderen Sprachen.
Niveau nahe oder über Muttersprachler: Precision pairs, Register, literarisches Vokabular; Partner Simon (ein Freund);
Karte Beleriand, Geschichte erzählt von Barangollach, einem der Noldor (eigene Erzählung in der Welt von « The Silmarillion »).
Die TSV-Felder heißen in allen Paketen gleich (fr = Zielsprache, de = Hilfssprache)."""
import os

PAAR = "en-de"
NAME = "My English"
KURZ = "EN"
HILFE_KURZ = "DE"
FLAGGE = "🇬🇧"
LANG = "en"
LANG_HILFE = "de"
SPRACHAUSGABE = "en-GB"
# Tiefes Grün und Burgunderrot (Beleriand, nicht Union Jack); hell und dunkel geprüft wie bei den anderen Sprachen
THEME = {"blau": "#1f4e3d", "rot": "#8b1e2d", "rot_text": "#ffffff", "dunkel": {"blau": "#7fd1a8", "blau_text": "#0f1522", "rot": "#ff8a94", "rot_text": "#1a0608"},
         "icon_buchstabe": "E", "icon_farben": [(31, 78, 61), (255, 255, 255), (139, 30, 45)]}

# Themen in Lernreihenfolge – erste Achse: Precision pairs (Inhalt folgt, Freigabe je Thema)
THEMEN = []

# Titel – Rang und Ruhm unter den Eldar: vom Wanderer bis zu dem, der in den Liedern genannt wird (Mr. Alex, 16.10.)
TITEL = [(0, "Wanderer", "🚶"), (300, "Herald", "📯"), (900, "Marchwarden", "🏹"), (1800, "Captain of the Noldor", "⚔️"),
         (3000, "Loremaster of Tirion", "📜"), (4500, "Lord of the Golden Flower", "🌼"), (6500, "Prince of the Noldor", "💎"),
         (9000, "High King of the Noldor", "👑"), (12000, "Named in Song", "🎵")]
TITEL_ANSAGE = "Hail! Wanderer no longer: you are now {name}."
# Ton des Buches: Voranstellung des gewichtigen Adjektivs („Grey is the shadow“), gehobenes Vokabular
SPIEL_TEXTE = {  # gesprochen von Mr. Alex (audio/spiel/<id>.mp3)
    "feuer": "Bright burns your flame! Three days unbroken!",
    "woche": "Perfect is this week: every school day kept. Hail!",
    "monat": "Four perfect weeks, unbroken! Of such deeds are songs made.",
    "fini": "Ended is the labour of this day. Rest, and return tomorrow.",
}

# Dialoge: Rolle A = Alex (Mr. Alex' Stimme), Rolle B = Simon (ein Freund, geklonte Stimme)
ROLLEN = {"A": "Alex", "B": "Simon"}
DIALOGE_TITEL = ["Dialogues with Simon", "Dialoge mit Simon"]

# Geschichte: Barangollach, einer der Noldor, erzählt – eigene Erzählung in Beleriand (Titel und Kapitel folgen)
GESCHICHTE = {"titel": "The Chronicle of Barangollach",
              "unter": "One of the Noldor, a long memory, and a road through Beleriand that the histories never mention.",
              "sammlung": ["Every perfect week unlocks a chapter: Barangollach, one of the Noldor, and his own road through Beleriand.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: Barangollach, einer der Noldor, und sein eigener Weg durch Beleriand."]}

# Aussprache-Modul: später (Wortbetonung, stumme Buchstaben, Vokalqualität); Einzelwörter im Trägersatz
TRAEGERSATZ = "Listen carefully: {wort}."
AUSSPRACHE = None

# Karte: Beleriand, selbst gezeichnet aus den Ortsnamen des Buches (keine fremden Kartendaten)
KARTE = {"name": "Beleriand", "einheit": "regions", "lieux": "places", "start": "Menegroth",
         "quelle": "Map drawn for this app from the place names of The Silmarillion; no map artwork was copied.",
         "badge": "Across Beleriand",
         "hinweis": ["Every finished Word Gym and every finished part unlocks a place, starting at Menegroth. Tap a place!",
                     "Jedes fertige Word Gym und jeder fertige Teil schalten einen Ort frei, Start in Menegroth. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import beleriand_karte
    return beleriand_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen (ElevenLabs): Mr. Alex' Klon auf britischem Englisch, Simon T (geklont, Received Pronunciation) – Hörprobe 16.10. bestanden
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "en", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "idD5c2qhqB8tWCuqP5sv", "modell": "eleven_v4", "language_code": "en", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
AUSSPRACHE_KORREKTUR = {}

# Oberflächentexte: [Zielsprache, Hilfe] oder nur Zielsprache
UI = {
    "app": "English – Word Gym",
    "gruss": ["Hail and well met!", "Well met! Young is the day.", "Late is the hour. A word or two?"],
    "motto": ["Ten minutes a day: the Word Gym, then yours is the road.", "Zehn Minuten am Tag: das Word Gym, danach gehört der Weg dir."],
    "seance": "▶ Let's go", "seance_fertig": "✓ Done for today",
    "seance_stand": "{neu} new · {wdh} to revise · {fertig} / {gesamt} done",
    "seance_leer": "Nothing to revise today – explore the themes!",
    "themen": ["Themes", "Die Themen"], "expressions": "items", "parties": "parts",
    "bonus": ["Pronunciation and story", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} chapters · a new one for every perfect week",
    "stand": ["{n} items in your box · {fest} firmly anchored · {orte} / {alle} places visited",
              "{n} Einträge in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Home", "zurueck_accueil": "← Home", "zurueck_thema": "← Theme", "suivant": "Next ➜", "retour": "◀ Back",
    "encore_hoeren": "🔊 Again", "solution": "Solution", "hoeren": "🔊 Listen", "stop": "■ Stop",
    "jetzt_du": "Your turn! Repeat.", "jetzt_du_dialog": "Your turn! Say your line.",
    "poli": "formal", "poli_titel": "Formal register", "trou": "gap", "hilfe_zeigen": "Show German",
    "seance_titel": "Word Gym", "nouvelle": "new", "revision": "revision · level {s}",
    "neu_ansage": ["New item! Listen and repeat.", "Neuer Eintrag! Hör zu und sprich nach."],
    "exemple": "Example", "ziel_sprache": "English", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["How do you say it in English? Say it out loud, then “Solution”.", "Wie sagt man das auf Englisch? Sag es laut, dann „Solution“."],
    "je_savais": "😊 I knew it", "encore": "🔁 Again", "pas_grave": "No matter – it comes back in a moment.",
    "fini": "Ended is the day's labour!", "pause": "A rest!",
    "fini_text": ["Your box is up to date. Tomorrow the items come back at the right moment. If you want more, explore the themes – no pressure.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Einträge zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["You can pick the Word Gym up whenever you like – what's done stays done.", "Du kannst das Word Gym jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 My collection",
    "etape": "Step {n}", "zeitmaschine": "⏳ Time machine", "trouve": "🔎 Find the item",
    "thema_ansage": ["Choose a part. Each part: listen and repeat in three steps, the time machine, then find the items again.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Einträge wiederfinden."],
    "partie": "Part {n}",
    "dialog_hoeren": "👂 Listen", "repeter": "Repeat", "tu_es": "🎭 You are {rolle}", "role": "Role", "repliques": "lines",
    "dialog_start": "▶ Start the dialogue", "dialog_hoeren_knopf": "▶ Listen to the dialogue",
    "dialog_ok_rolle": "Swap roles – or once more!", "dialog_ok": "Now it's your turn to speak!",
    "dialog_ansage_rolle": ["You are {ich}. Say your lines when it's your turn – the app speaks for {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["“{titel}” – {ort}. Listen to the dialogue.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Easier: show my lines", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Chapter {n}", "kapitel_ansage": ["Listen to the chapter, or read it aloud. Tap a paragraph for German.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Listen to the whole chapter", "kapitel_weiter": "Next chapter ➜",
    "kapitel_naechste": ["The next chapter unlocks with your next perfect week.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["The sequel is being written.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Not unlocked yet", "semaine_parfaite": "Perfect week",
    "mot": "Word {n} / {alle}", "paire": "Pair {n} / {alle}", "lentement": "🐢 Slowly", "normal": "🔊 Normal",
    "lr_label": "Listen and repeat", "parties_label": "Parts – direct access",
    "trop_vite": "⏱️ Too fast!", "trop_vite_text": ["Really say the sentences out loud. Then there are points. Once more!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Once more ➜", "termine": "{name}: done!", "presque": ["Nearly there! Still missing:", "Fast! Es fehlt noch:"],
    "thema_fertig": "Whole is the theme “{name}”. Hail!", "autres_parties": "Other parts",
    "stufen": [["Listen and repeat! The German sentence helps you.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["Which word is missing? Say the whole sentence, then “Solution”.", "Welches Wort fehlt? Sag den ganzen Satz, dann „Solution“."],
               ["Say the sentence in English, then “Solution”.", "Sag den Satz auf Englisch, dann „Solution“."]],
    "dis_phrase": "Say the whole sentence in English!", "phrase": "Sentence {n} / {alle}",
    "tipp_buchstabe": ["Easier: the first letter", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Easier: the sentence with a gap", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Today", "present"], "pc": ["Yesterday", "past", "And yesterday?"], "fp": ["Tomorrow", "future", "And tomorrow?"]},
    "solution_zeit": "Solution: {zeit}",
    "zeit_ansage": ["Listen to today's sentence. Then say it in the past, and in the future – out loud. Then “Solution”.",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Solution“."],
    "expression": "Item {n} / {alle}",
    "bonus_weekend": "🏖️ Weekend bonus +{p}", "en_feu": "Bright burns your flame! {n} days unbroken", "en_feu_text": "{n} school days unbroken – +{p} points!",
    "semaine_parfaite_titel": "Perfect is this week!", "semaine_parfaite_text": "Every school day kept – +{p} points.",
    "nouveau_chapitre": " New chapter: “{titel}”!", "suite_bientot": " The next part of the story is on its way.",
    "mois_parfait": "Perfect is this month!", "mois_parfait_text": "{n} perfect weeks unbroken – +{p} points and a golden frame!",
    "nouveau_titre": "Hail, {name}!", "points": "points", "jours_suite": "School days in a row",
    "visite": "visited ✓",
    "ton_titre": "Your title", "encore_points": "{n} more points to “{name}” {symbol}",
    "cette_semaine": "This week", "tage": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "serie_text": ["🔥 {n} school days in a row · ⭐ {w} perfect weeks. Holidays and bank holidays don't count – your streak stays.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 My box ({n} items)", "boite_text": ["Level 0 = new or forgotten · from level 3 the item is firmly anchored.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt der Eintrag."],
    "jours": "d", "badges": "Badges",
    "badge_liste": ["On fire", "Perfect week", "5 × perfect", "Perfect month", "Weekend hero", "100 items", "50 firmly anchored"],
    "offline": "📥 Offline", "offline_text": ["Download the audio for this language to practise without a connection.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} audio files offline", "offline_laden": "📥 Download for offline use", "offline_fertig": "✓ Available offline",
    "bald": "in preparation",
    "offline_laeuft": "Downloading… {n} / {alle}",
}
