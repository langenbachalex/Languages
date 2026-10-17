"""Sprachpaket Französisch (Ziel) – Deutsch (Hilfe). Konzept: docs/fr-de/konzept.md
Alles, was die App über diese Sprache wissen muss: Themen, Oberflächentexte, Titel, Aussprache-Teil, Dialogrollen,
Geschichte, Karte, Stimmen. Die TSV-Felder heißen in allen Paketen gleich (fr = Zielsprache, de = Hilfssprache)."""
import os

PAAR = "fr-de"
NAME = "Mon français"          # Name der Sprache in der App
KURZ = "FR"                    # Umschalter
HILFE_KURZ = "DE"
FLAGGE = "🇫🇷"
LANG = "fr"                    # HTML lang / Sprachausgabe des Geräts
LANG_HILFE = "de"
SPRACHAUSGABE = "fr-FR"
THEME = {"blau": "#1b3f8f", "rot": "#c8102e", "rot_text": "#ffffff", "dunkel": {"blau": "#9db9ff", "blau_text": "#0f1522", "rot": "#ff7b88", "rot_text": "#1a0608"},
         "icon_buchstabe": "F", "icon_farben": [(0, 85, 164), (255, 255, 255), (239, 65, 53)]}

# Themen in Lernreihenfolge (die tägliche Séance nimmt neue Wendungen in dieser Reihenfolge)
THEMEN = [
    {"id": "profs", "name": "Entre profs", "de": "Unter Lehrern – mit Aurélien", "symbol": "🧑‍🏫", "datei": "entre_profs.tsv"},
    {"id": "sentiments", "name": "Sentiments et ambiances", "de": "Gefühle und Stimmungen", "symbol": "🎭", "datei": "sentiments.tsv"},
    {"id": "chats", "name": "Les chats", "de": "Die Katzen", "symbol": "🐈", "datei": "chats.tsv"},
    {"id": "musique", "name": "Musique et langue", "de": "Musik und Sprache", "symbol": "🎵", "datei": "musique.tsv"},
    {"id": "histoires", "name": "Histoires et fantasy", "de": "Geschichten und Fantasy", "symbol": "🐉", "datei": "histoires.tsv"},
    {"id": "sport", "name": "Sport et kung-fu", "de": "Sport und Kung-Fu", "symbol": "🥋", "datei": "sport.tsv"},
    {"id": "manger", "name": "Manger et bien vivre", "de": "Essen und gut leben", "symbol": "🥖", "datei": "manger.tsv"},
    {"id": "enfants", "name": "Enfants et bébés", "de": "Kinder und Babys", "symbol": "👶", "datei": "enfants.tsv"},
    {"id": "faux_amis", "name": "Faux amis", "de": "Falsche Freunde Englisch–Französisch (Bonus)", "symbol": "⚡", "datei": "faux_amis.tsv"},
]

# Titel – französische Delikatessen, vom kleinen Éclair bis zum Kaviar
TITEL = [(0, "Petit éclair", "🍮"), (300, "Croissant", "🥐"), (900, "Baguette", "🥖"), (1800, "Crêpe", "🥞"),
         (3000, "Fromage", "🧀"), (4500, "Huîtres", "🦪"), (6500, "Caviar", "✨")]
TITEL_ANSAGE = "Félicitations ! Tu es maintenant {name} !"
SPIEL_TEXTE = {  # gesprochen von Mr. Alex (audio/spiel/<id>.mp3)
    "feuer": "Tu es en feu ! Trois jours de suite !",
    "woche": "Semaine parfaite ! Tu as travaillé chaque jour d'école. Bravo !",
    "monat": "Quatre semaines parfaites de suite ! Quel champion !",
    "fini": "C'est fini pour aujourd'hui. À demain !",
}

# Dialoge: Rolle A = Alex (Mr. Alex' Stimme), Rolle B = Aurélien (zweite Stimme)
ROLLEN = {"A": "Alex", "B": "Aurélien"}
DIALOGE_TITEL = ["Dialogues avec Aurélien", "Dialoge mit Aurélien"]

# Geschichte « Le secret du Louvre »
GESCHICHTE = {"titel": "Le secret du Louvre",
              "unter": "Julien Lefèvre, professeur à Metz – un billet, une salle qui n'existe pas, un chat qui sait.",
              "sammlung": ["Chaque semaine parfaite débloque un chapitre : Julien Lefèvre, professeur à Metz, et le mystère du Louvre.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: Julien Lefèvre, Lehrer aus Metz, und das Geheimnis des Louvre."]}

# Aussprache: les nasales – Laute (Schild, Schreibweisen, Tipp Ziel, Tipp Hilfe), Minimalpaar-Gruppen
# Einzelwörter des Aussprache-Moduls werden in diesem Satz gesprochen und danach geschnitten (audio.py)
TRAEGERSATZ = "Écoute bien : {wort}."
AUSSPRACHE = {
    "id": "nasale", "symbol": "👃", "titel": "Les nasales",
    "unter": "[ɑ̃] en · [ɔ̃] on · [ɛ̃] in · [œ̃] un – écouter, distinguer, les deux dans un mot",
    "datei": "nasale.tsv",
    "klaenge": {"an": ["[ɑ̃]", "en · an · em · am", "bouche ouverte, langue en bas", "Mund offen, Zunge unten (wie in « enfant »)"],
                "on": ["[ɔ̃]", "on · om", "lèvres arrondies, bouche presque fermée", "Lippen rund, Mund fast zu (wie in « bon »)"],
                "in": ["[ɛ̃]", "in · ain · ein · aim", "bouche étirée, comme un « ä » nasal", "Mund breit, wie ein nasales „ä“ (wie in « vin »)"],
                "un": ["[œ̃]", "un · um", "comme [ɛ̃], mais lèvres légèrement arrondies", "wie [ɛ̃], aber Lippen leicht gerundet (wie in « brun »)"]},
    "reihe": ["an", "on", "in", "un"],
    "paare": [["p1", "en ou on ?"], ["p2", "in ou en ?"], ["p3", "in ou on ?"]],
    "beide_name": "👑 Les deux",
    "texte": {
        "beide": ["Deux nasales dans un mot. Écoute lentement, puis à vitesse normale – et répète en soignant chaque voyelle.",
                  "Zwei Nasale in einem Wort. Hör langsam, dann normal – und sprich nach, jede Nasale sauber."],
        "klang": ["{laut} – {tipp}. Écoute lentement, puis normalement. Répète !", "{laut} – {tipp}. Hör langsam, dann normal. Sprich nach!"],
        "paar": ["Écoute le mot. Lequel est-ce ? Touche le bon.", "Hör das Wort. Welches ist es? Tipp auf das richtige."],
        "hilfe": ["Je t'aide : {a}. Écoute encore !", "Ich helfe dir: {a}. Hör noch mal!"],
        "beide_hoeren": ["Plus facile : écouter les deux", "Noch einfacher: beide hören"],
    },
}

# Karte: Frankreich mit Départements (IGN Admin Express via france-geojson, Licence ouverte)
KARTE = {"name": "La France", "einheit": "départements", "lieux": "lieux", "start": "Metz",
         "quelle": "Carte : IGN Admin Express via france-geojson (Licence ouverte).",
         "badge": "Tour de France",
         "hinweis": ["Chaque séance terminée et chaque partie terminée débloquent un lieu, en partant de Metz. Touche un lieu !",
                     "Jede fertige Séance und jeder fertige Teil schalten einen Ort frei, Start in Metz. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import frankreich_karte
    return frankreich_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen (ElevenLabs): Mr. Alex' Klon auf Französisch (Hörprobe 13.10. freigegeben), Aurélien = „Julien – Professional“
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "fr", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "eOwAMwUJEGkP44SKOXIH", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
# Schreibweise nur fürs Vorlesen (ganze Wörter): die Stimme las einzelne Wörter englisch oder mit Endkonsonant.
AUSSPRACHE_KORREKTUR = {"Metz": "Mess", "Nancy": "Nanci", "temps": "tant", "Paris": "Pari", "‿": ""}

# Oberflächentexte: [Zielsprache, Hilfe] oder nur Zielsprache
UI = {
    "app": "Language Learning",
    "gruss": ["Bonjour ! On y va ?", "Salut ! On s'y met ?", "Bonsoir ! Une petite séance ?"],
    "motto": ["Dix minutes par jour : la séance, puis ce que tu veux.", "Zehn Minuten am Tag: die Séance, danach was du willst."],
    "seance": "▶ C'est parti !", "seance_fertig": "✓ Terminé pour aujourd'hui",
    "seance_stand": "{neu} nouvelles · {wdh} à réviser · {fertig} / {gesamt} faites",
    "seance_leer": "Rien à réviser aujourd'hui – explore les thèmes !",
    "themen": ["Les thèmes", "Die Themen"], "expressions": "expressions", "parties": "parties",
    "bonus": ["Prononciation et histoire", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} chapitres · un nouveau par semaine parfaite",
    "stand": ["{n} expressions dans ta boîte · {fest} bien ancrées · {orte} / {alle} lieux visités",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Accueil", "zurueck_accueil": "← Accueil", "zurueck_thema": "← Thème", "suivant": "Suivant ➜", "retour": "◀ Retour",
    "encore_hoeren": "🔊 Encore", "solution": "Solution", "hoeren": "🔊 Écouter", "stop": "■ Stop",
    "jetzt_du": "À toi ! Répète.", "jetzt_du_dialog": "À toi ! Dis ta réplique.",
    "poli": "vous · poli", "poli_titel": "Höflichkeitsform", "trou": "trou", "hilfe_zeigen": "Deutsch anzeigen",
    "seance_titel": "Muscu des mots", "nouvelle": "nouvelle", "revision": "révision · niveau {s}",
    "neu_ansage": ["Nouvelle expression ! Écoute et répète.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Exemple", "ziel_sprache": "Français", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["Comment dit-on en français ? Dis-le à voix haute, puis « Solution ».", "Wie sagt man das auf Französisch? Sag es laut, dann „Solution“."],
    "je_savais": "😊 Je savais", "encore": "🔁 Encore", "pas_grave": "Pas grave ! Elle revient tout à l'heure.",
    "fini": "C'est fini pour aujourd'hui !", "pause": "Pause !",
    "fini_text": ["Ta boîte est à jour. Demain, les expressions reviennent au bon moment. Si tu veux continuer, explore les thèmes – sans pression.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["Tu peux reprendre la séance quand tu veux – ce qui est fait reste fait.", "Du kannst die Séance jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 Ma collection",
    "etape": "Étape {n}", "zeitmaschine": "⏳ Machine à remonter le temps", "trouve": "🔎 Trouve l'expression",
    "thema_ansage": ["Choisis une partie. Chaque partie : écouter et répéter en trois étapes, la machine à remonter le temps, puis retrouver les expressions.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "Partie {n}",
    "dialog_hoeren": "👂 Écouter", "repeter": "Répéter", "tu_es": "🎭 Tu es {rolle}", "role": "Rôle", "repliques": "répliques",
    "dialog_start": "▶ Commencer le dialogue", "dialog_hoeren_knopf": "▶ Écouter le dialogue",
    "dialog_ok_rolle": "Change de rôle – ou encore une fois !", "dialog_ok": "Maintenant, à toi de parler !",
    "dialog_ansage_rolle": ["Tu es {ich}. Dis tes répliques quand c'est ton tour – l'appli parle pour {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. Écoute le dialogue.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Plus facile : montrer mes répliques", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Chapitre {n}", "kapitel_ansage": ["Écoute le chapitre, ou lis-le à voix haute. Touche un paragraphe pour l'allemand.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Écouter tout le chapitre", "kapitel_weiter": "Chapitre suivant ➜",
    "kapitel_naechste": ["Le chapitre suivant se débloque avec ta prochaine semaine parfaite.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["La suite est en cours d'écriture.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Pas encore débloqué", "semaine_parfaite": "Semaine parfaite",
    "mot": "Mot {n} / {alle}", "paire": "Paire {n} / {alle}", "lentement": "🐢 Lentement", "normal": "🔊 Normal",
    "lr_label": "Écouter et répéter", "parties_label": "Parties – accès direct",
    "trop_vite": "⏱️ Trop vite !", "trop_vite_text": ["Dis vraiment les phrases à voix haute. Ensuite, il y a des points. Encore une fois !", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Encore une fois ➜", "termine": "{name} : terminé !", "presque": ["Presque ! Il manque encore :", "Fast! Es fehlt noch:"],
    "thema_fertig": "Tout le thème « {name} » est terminé. Chapeau !", "autres_parties": "Autres parties",
    "stufen": [["Écoute et répète ! La phrase allemande t'aide.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["Quel mot manque ? Dis toute la phrase, puis « Solution ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Solution“."],
               ["Dis la phrase en français, puis « Solution ».", "Sag den Satz auf Französisch, dann „Solution“."]],
    "dis_phrase": "Dis toute la phrase en français !", "phrase": "Phrase {n} / {alle}",
    "tipp_buchstabe": ["Plus facile : la première lettre", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Plus facile : la phrase à trou", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Aujourd'hui", "présent"], "pc": ["Hier", "passé composé", "Et hier ?"], "fp": ["Demain", "futur proche", "Et demain ?"]},
    "solution_zeit": "Solution : {zeit}",
    "zeit_ansage": ["Écoute la phrase d'aujourd'hui. Puis dis-la au passé, et au futur – à voix haute. Ensuite « Solution ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Solution“."],
    "expression": "Expression {n} / {alle}",
    "bonus_weekend": "🏖️ Bonus week-end +{p}", "en_feu": "Tu es en feu ! {n} jours de suite", "en_feu_text": "{n} jours d'école de suite – +{p} points !",
    "semaine_parfaite_titel": "Semaine parfaite !", "semaine_parfaite_text": "Tu as travaillé chaque jour d'école – +{p} points.",
    "nouveau_chapitre": " Nouveau chapitre : « {titel} » !", "suite_bientot": " La suite de l'histoire arrive bientôt.",
    "mois_parfait": "Mois parfait !", "mois_parfait_text": "{n} semaines parfaites de suite – +{p} points et un cadre doré !",
    "nouveau_titre": "Nouveau titre : {name} !", "points": "points", "jours_suite": "Jours d'école de suite",
    "visite": "visité ✓",
    "ton_titre": "Ton titre", "encore_points": "Encore {n} points jusqu'à « {name} » {symbol}",
    "cette_semaine": "Cette semaine", "tage": ["Lun", "Mar", "Mer", "Jeu", "Ven"],
    "serie_text": ["🔥 {n} jours d'école de suite · ⭐ {w} semaines parfaites. Vacances et jours fériés ne comptent pas – ta série reste.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 Ma boîte ({n} expressions)", "boite_text": ["Niveau 0 = nouvelle ou oubliée · à partir du niveau 3, l'expression est bien ancrée.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "j", "badges": "Badges",
    "badge_liste": ["En feu", "Semaine parfaite", "5 × parfaite", "Mois parfait", "Héros du week-end", "100 expressions", "50 bien ancrées"],
    "offline": "📥 Hors-ligne", "offline_text": ["Télécharge les audios de cette langue pour travailler sans connexion.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} fichiers audio hors-ligne", "offline_laden": "📥 Télécharger pour hors-ligne", "offline_fertig": "✓ Disponible hors-ligne",
    "bald": "en préparation",
    "offline_laeuft": "Téléchargement… {n} / {alle}",
}
