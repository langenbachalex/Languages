"""Sprachpaket Deutsch (Ziel) – Französisch (Hilfe), für Aurélien. Konzept: docs/de-fr/konzept.md
Oberfläche Französisch (wie fr-de, mit deutschem Tipp-Text), Wendungen und Lob auf Deutsch, Notizen auf Französisch.
TSV-Felder wie in allen Paketen: fr = Zielsprache (hier Deutsch), de = Hilfssprache (hier Französisch).
Zeitmaschine: heute (Präsens) – gestern (Perfekt) – morgen (Futur I)."""
import os

PAAR = "de-fr"
NAME = "Mon allemand"
KURZ = "DE"
HILFE_KURZ = "FR"
FLAGGE = "🇩🇪"
LANG = "de"
LANG_HILFE = "fr"
SPRACHAUSGABE = "de-DE"
THEME = {"blau": "#2b2b2b", "rot": "#c80000", "rot_text": "#ffffff", "dunkel": {"blau": "#d9dde6", "blau_text": "#15181f", "rot": "#ff7070", "rot_text": "#2a0000"}}   # Schwarz und Rot (Gold im Icon)

# Themen in Lernreihenfolge – werden Thema für Thema ergänzt (jeweils nach Absegnung)
THEMEN = [
    {"id": "lehrer", "name": "Unter Lehrern", "de": "Entre profs – avec Alex", "symbol": "🧑‍🏫", "datei": "unter_lehrern.tsv"},
    {"id": "gefuehle", "name": "Gefühle und Stimmungen", "de": "Sentiments et ambiances", "symbol": "🎭", "datei": "gefuehle.tsv"},
    {"id": "katzen", "name": "Die Katzen", "de": "Les chats", "symbol": "🐈", "datei": "katzen.tsv"},
    {"id": "musik", "name": "Musik und Sprache", "de": "Musique et langue", "symbol": "🎵", "datei": "musik.tsv"},
    {"id": "geschichten", "name": "Geschichten und Fantasy", "de": "Histoires et fantasy", "symbol": "🐉", "datei": "geschichten.tsv"},
    {"id": "sport", "name": "Sport und Kung-Fu", "de": "Sport et kung-fu", "symbol": "🥋", "datei": "sport.tsv"},
    {"id": "essen", "name": "Essen und gut leben", "de": "Manger et bien vivre", "symbol": "🥨", "datei": "essen.tsv"},
    {"id": "kinder", "name": "Kinder und Babys", "de": "Enfants et bébés", "symbol": "👶", "datei": "kinder.tsv"},
    {"id": "falsche_freunde", "name": "Falsche Freunde", "de": "Faux amis français–allemand (bonus)", "symbol": "⚡", "datei": "falsche_freunde.tsv"},
]

# Titel – deutsche Leckereien
TITEL = [(0, "Brezel", "🥨"), (300, "Bratwurst", "🌭"), (900, "Kartoffelsalat", "🥔"), (1800, "Schnitzel", "🍽️"),
         (3000, "Sauerbraten", "🍖"), (4500, "Schwarzwälder Kirschtorte", "🍰"), (6500, "Chefkoch", "✨")]
TITEL_ANSAGE = "Glückwunsch! Jetzt bist du {name}!"
SPIEL_TEXTE = {
    "feuer": "Du bist in Serie! Drei Tage am Stück!",
    "woche": "Perfekte Woche! Du hast an jedem Schultag gearbeitet. Bravo!",
    "monat": "Vier perfekte Wochen am Stück! Was für ein Champion!",
    "fini": "Schluss für heute. Bis morgen!",
}

# Dialoge: A = Alex (Mr. Alex' Stimme, Deutsch), B = Aurélien (Julien, spricht Deutsch mit französischem Akzent)
ROLLEN = {"A": "Alex", "B": "Aurélien"}
DIALOGE_TITEL = ["Dialogues avec Alex", "Dialoge mit Alex"]

GESCHICHTE = {"titel": "Das Geheimnis der Völklinger Hütte",
              "unter": "Lena Becker, Lehrerin in Saarbrücken – eine Eintrittskarte, eine Tür, die es nicht gibt, eine Katze, die Bescheid weiß.",
              "sammlung": ["Chaque semaine parfaite débloque un chapitre : Lena Becker, professeure à Sarrebruck, et le mystère de l'usine de Völklingen.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: Lena Becker, Lehrerin in Saarbrücken, und das Geheimnis der Völklinger Hütte."]}

# Aussprache « Die schweren Laute » – für Französischsprachige: h, ich-Laut, ach-Laut, ei/ie, Vokallänge
# Einzelwörter des Aussprache-Moduls werden in diesem Satz gesprochen und danach geschnitten (audio.py)
TRAEGERSATZ = "Hör gut zu: {wort}."
AUSSPRACHE = {
    "id": "laute", "symbol": "👄", "titel": "Die schweren Laute",
    "unter": "h · ich · ach · ei · ie – écouter, distinguer, plusieurs dans un mot",
    "datei": "laute.tsv",
    "klaenge": {"h": ["[h]", "h", "un souffle, comme pour embuer un miroir – jamais muet", "ein Hauch, nie stumm (Hund, Haus)"],
                "ich": ["[ç]", "ch après i, e, ä, ö, ü, l, n, r", "comme le « ch » de « ich » : la langue près du palais, un chuchotement", "der ich-Laut: Zunge am Gaumen (ich, Milch)"],
                "ach": ["[x]", "ch après a, o, u, au", "comme la « jota » espagnole, au fond de la gorge", "der ach-Laut: hinten im Rachen (Nacht, Buch)"],
                "ei": ["[aɪ]", "ei · ai", "se prononce « aïe » – jamais « è »", "wie „ai“ (Zeit, mein)"],
                "ie": ["[iː]", "ie", "un « i » long – jamais « ié »", "ein langes i (Liebe, vier)"],
                "kein": ["[–]", "sans h", "pas de souffle au début", "ohne h (und, aus)"],
                "kurz": ["[ˑ]", "voyelle brève", "voyelle courte, souvent devant deux consonnes", "kurzer Vokal (Stadt, Mitte)"],
                "lang": ["[ː]", "voyelle longue", "voyelle longue, souvent devant une consonne ou avec h", "langer Vokal (Staat, Miete)"]},
    "reihe": ["h", "ich", "ach", "ei", "ie"],
    "paare": [["p1", "h ou pas h ?"], ["p2", "ie ou ei ?"], ["p3", "brève ou longue ?"]],
    "beide_name": "👑 Plusieurs à la fois",
    "texte": {
        "beide": ["Plusieurs sons difficiles dans un mot. Écoute lentement, puis à vitesse normale – et répète en soignant chaque son.",
                  "Mehrere schwere Laute in einem Wort. Hör langsam, dann normal – und sprich jeden Laut sauber nach."],
        "klang": ["{laut} – {tipp}. Écoute lentement, puis normal. Répète !", "{laut} – {tipp}. Hör langsam, dann normal. Sprich nach!"],
        "paar": ["Écoute le mot. Lequel est-ce ? Touche le bon.", "Hör das Wort. Welches ist es? Tipp auf das richtige."],
        "hilfe": ["Je t'aide : {a}. Écoute encore !", "Ich helfe dir: {a}. Hör noch mal!"],
        "beide_hoeren": ["Plus facile : écouter les deux", "Noch einfacher: beide hören"],
    },
}

# Karte: Deutschland mit Landkreisen (deutschlandGeoJSON / DIVA-GIS, nicht-kommerziell, Stand etwa 2010)
KARTE = {"name": "L'Allemagne", "einheit": "Landkreise", "lieux": "lieux", "start": "Saarbrücken",
         "quelle": "Carte : Landkreise d'Allemagne via deutschlandGeoJSON (données DIVA-GIS, usage non commercial).", "badge": "Deutschlandtour",
         "hinweis": ["Chaque séance terminée et chaque partie terminée débloquent un lieu, en partant de Sarrebruck. Touche un lieu !",
                     "Jede fertige Séance und jeder fertige Teil schalten einen Ort frei, Start in Saarbrücken. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import deutschland_karte
    return deutschland_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen: Mr. Alex' Klon auf Deutsch, Aurélien = Julien (multilingual, Deutsch)
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "de", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "eOwAMwUJEGkP44SKOXIH", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
AUSSPRACHE_KORREKTUR = {}

# Oberflächentexte: [Französisch für den Lerner, Deutsch zum Antippen]
UI = {
    "app": "Language Learning",
    "gruss": ["Bonjour ! On y va ?", "Salut ! On s'y met ?", "Bonsoir ! Une petite séance ?"],
    "motto": ["Dix minutes par jour : la séance, puis ce que tu veux.", "Zehn Minuten am Tag: die Séance, danach was du willst."],
    "seance": "▶ Ma séance du jour", "seance_fertig": "✓ Séance du jour terminée",
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
    "poli": "Sie · poli", "poli_titel": "Forme de politesse", "trou": "trou", "hilfe_zeigen": "Afficher le français",
    "seance_titel": "Ma séance du jour", "nouvelle": "nouvelle", "revision": "révision · niveau {s}",
    "neu_ansage": ["Nouvelle expression ! Écoute et répète.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Exemple", "ziel_sprache": "Deutsch", "hilfe_sprache": "Français",
    "wie_sagt_man": ["Comment dit-on en allemand ? Dis-le à voix haute, puis « Solution ».", "Wie sagt man das auf Deutsch? Sag es laut, dann „Solution“."],
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
    "chapitre": "Chapitre {n}", "kapitel_ansage": ["Écoute le chapitre, ou lis-le à voix haute. Touche un paragraphe pour le français.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Französisch."],
    "kapitel_alles": "▶ Écouter tout le chapitre", "kapitel_weiter": "Chapitre suivant ➜",
    "kapitel_naechste": ["Le chapitre suivant se débloque avec ta prochaine semaine parfaite.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["La suite est en cours d'écriture.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Pas encore débloqué", "semaine_parfaite": "Semaine parfaite",
    "mot": "Mot {n} / {alle}", "paire": "Paire {n} / {alle}", "lentement": "🐢 Lentement", "normal": "🔊 Normal",
    "lr_label": "Écouter et répéter", "parties_label": "Parties – accès direct",
    "trop_vite": "⏱️ Trop vite !", "trop_vite_text": ["Dis vraiment les phrases à voix haute. Ensuite, il y a des points. Encore une fois !", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Encore une fois ➜", "termine": "{name} : terminé !", "presque": ["Presque ! Il manque encore :", "Fast! Es fehlt noch:"],
    "thema_fertig": "Tout le thème « {name} » est terminé. Chapeau !", "autres_parties": "Autres parties",
    "stufen": [["Écoute et répète ! La phrase française t'aide.", "Hör zu und sprich nach! Der französische Satz hilft dir."],
               ["Quel mot manque ? Dis toute la phrase, puis « Solution ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Solution“."],
               ["Dis la phrase en allemand, puis « Solution ».", "Sag den Satz auf Deutsch, dann „Solution“."]],
    "dis_phrase": "Dis toute la phrase en allemand !", "phrase": "Phrase {n} / {alle}",
    "tipp_buchstabe": ["Plus facile : la première lettre", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Plus facile : la phrase à trou", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Aujourd'hui", "Präsens"], "pc": ["Hier", "Perfekt", "Et hier ?"], "fp": ["Demain", "Futur I", "Et demain ?"]},
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
