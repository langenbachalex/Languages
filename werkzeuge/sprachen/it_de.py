"""Sprachpaket Italienisch (Ziel) – Deutsch (Hilfe). Konzept: docs/it-de/konzept.md
TSV-Felder wie in allen Paketen: fr = Zielsprache, de = Hilfssprache. Zeitmaschine: oggi (presente) – ieri (passato prossimo) – domani (futuro semplice)."""
import os

PAAR = "it-de"
NAME = "Il mio italiano"
KURZ = "IT"
HILFE_KURZ = "DE"
FLAGGE = "🇮🇹"
LANG = "it"
LANG_HILFE = "de"
SPRACHAUSGABE = "it-IT"
THEME = {"blau": "#1e6b3a", "rot": "#c8102e", "rot_text": "#ffffff", "dunkel": {"blau": "#7ad9a5", "blau_text": "#07200f", "rot": "#ff7b88", "rot_text": "#1a0608"}}   # Grün und Rot

# Themen in Lernreihenfolge – werden Thema für Thema ergänzt (jeweils nach Absegnung)
THEMEN = [
    {"id": "colleghi", "name": "Tra colleghi", "de": "Unter Lehrern – mit Giovanni", "symbol": "🧑‍🏫", "datei": "tra_colleghi.tsv"},
    {"id": "sentimenti", "name": "Sentimenti e atmosfere", "de": "Gefühle und Stimmungen", "symbol": "🎭", "datei": "sentimenti.tsv"},
    {"id": "gatti", "name": "I gatti", "de": "Die Katzen", "symbol": "🐈", "datei": "gatti.tsv"},
    {"id": "musica", "name": "Musica e lingua", "de": "Musik und Sprache", "symbol": "🎵", "datei": "musica.tsv"},
    {"id": "storie", "name": "Storie e fantasia", "de": "Geschichten und Fantasy", "symbol": "🐉", "datei": "storie.tsv"},
    {"id": "sport", "name": "Sport e kung fu", "de": "Sport und Kung-Fu", "symbol": "🥋", "datei": "sport.tsv"},
    {"id": "mangiare", "name": "Mangiare e vivere bene", "de": "Essen und gut leben", "symbol": "🍝", "datei": "mangiare.tsv"},
    {"id": "bambini", "name": "Bambini e neonati", "de": "Kinder und Babys", "symbol": "👶", "datei": "bambini.tsv"},
    {"id": "falsi_amici", "name": "Falsi amici", "de": "Falsche Freunde Deutsch/Englisch/Französisch/Spanisch–Italienisch (Bonus)", "symbol": "⚡", "datei": "falsi_amici.tsv"},
]

# Titel – Leiter der Leckereien
TITEL = [(0, "Oliva", "🫒"), (300, "Pizza", "🍕"), (900, "Pasta al ragù", "🍝"), (1800, "Parmigiano", "🧀"),
         (3000, "Chianti", "🍷"), (4500, "Gelato", "🍨"), (6500, "Gran chef", "✨")]
TITEL_ANSAGE = "Complimenti! Adesso sei {name}!"
SPIEL_TEXTE = {
    "feuer": "Sei in serie! Tre giorni di fila!",
    "woche": "Settimana perfetta! Hai lavorato tutti i giorni di scuola. Bravissimo!",
    "monat": "Quattro settimane perfette di fila! Che campione!",
    "fini": "Finito per oggi. A domani!",
}

# Dialoge: A = Alex (Mr. Alex' Stimme), B = Giovanni (Andy)
ROLLEN = {"A": "Alex", "B": "Giovanni"}
DIALOGE_TITEL = ["Dialoghi con Giovanni", "Dialoge mit Giovanni"]

GESCHICHTE = {"titel": "Il segreto della Torre",
              "unter": "Chiara Rossi, professoressa a Bologna – un biglietto, una porta che non esiste, un gatto che sa.",
              "sammlung": ["Ogni settimana perfetta sblocca un capitolo: Chiara Rossi, professoressa a Bologna, e il mistero della Torre.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: Chiara Rossi, Lehrerin in Bologna, und das Geheimnis des Turms."]}

TRAEGERSATZ = "Ascolta bene… {wort}."   # Einzelwörter/Wendungen im Trägersatz, Auslassungspunkte erzeugen die Pause für den Schnitt
AUSSPRACHE = None   # später, optional: « Le doppie »

# Karte: Italien mit Provinzen (ISTAT via openpolis/geojson-italy, CC BY 4.0)
KARTE = {"name": "Italia", "einheit": "province", "lieux": "luoghi", "start": "Bologna",
         "quelle": "Mappa: province d'Italia, dati ISTAT via openpolis/geojson-italy (CC BY 4.0).", "badge": "Giro d'Italia",
         "hinweis": ["Ogni sessione finita e ogni parte finita sbloccano un luogo, partendo da Bologna. Tocca un luogo!",
                     "Jede fertige Sessione und jeder fertige Teil schalten einen Ort frei, Start in Bologna. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import italien_karte
    return italien_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen: Mr. Alex' Klon auf Italienisch (Hörprobe 13.10. freigegeben), Giovanni = „Andy – Warm, Nuanced and Mature“ (Bibliothek)
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "it", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "DLMxnwJE0a28JQLTMJPJ", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
# Vorlese-Schreibung (ganze Wörter/Phrasen): Lob « Hai orecchio » mit hörbarem H; Ort « I portici » mit englischem I (Artikel am Anfang weggelassen)
AUSSPRACHE_KORREKTUR = {"Hai": "Ai", "I portici di Bologna": "Portici di Bologna"}
# Wendungen, die allein gelesen ins Englische kippen: im Trägersatz sprechen und schneiden (audio.py)
WENDUNG_IM_TRAEGERSATZ = {"fare fatica a", "fare fatica ad addormentarsi"}

UI = {
    "app": "Language Learning",
    "gruss": ["Buongiorno! Andiamo?", "Ciao! Ci mettiamo?", "Buonasera! Una sessione breve?"],
    "motto": ["Dieci minuti al giorno: la sessione, e poi quello che vuoi.", "Zehn Minuten am Tag: die Sessione, danach was du willst."],
    "seance": "▶ Si parte!", "seance_fertig": "✓ Fatto per oggi",
    "seance_stand": "{neu} nuove · {wdh} da ripassare · {fertig} / {gesamt} fatte",
    "seance_leer": "Niente da ripassare oggi – esplora i temi!",
    "themen": ["I temi", "Die Themen"], "expressions": "espressioni", "parties": "parti",
    "bonus": ["Pronuncia e storia", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} capitoli · uno nuovo per ogni settimana perfetta",
    "stand": ["{n} espressioni nella tua scatola · {fest} ben radicate · {orte} / {alle} luoghi visitati",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Home", "zurueck_accueil": "← Home", "zurueck_thema": "← Tema", "suivant": "Avanti ➜", "retour": "◀ Indietro",
    "encore_hoeren": "🔊 Ancora", "solution": "Soluzione", "hoeren": "🔊 Ascolta", "stop": "■ Stop",
    "jetzt_du": "Tocca a te! Ripeti.", "jetzt_du_dialog": "Tocca a te! Di' la tua battuta.",
    "poli": "Lei · formale", "poli_titel": "Höflichkeitsform", "trou": "buco", "hilfe_zeigen": "Deutsch anzeigen",
    "seance_titel": "Palestra delle parole", "nouvelle": "nuova", "revision": "ripasso · livello {s}",
    "neu_ansage": ["Espressione nuova! Ascolta e ripeti.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Esempio", "ziel_sprache": "Italiano", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["Come si dice in italiano? Dillo ad alta voce e poi « Soluzione ».", "Wie sagt man das auf Italienisch? Sag es laut, dann „Soluzione“."],
    "je_savais": "😊 Lo sapevo", "encore": "🔁 Ancora", "pas_grave": "Non fa niente! Torna tra un po'.",
    "fini": "Finito per oggi!", "pause": "Pausa!",
    "fini_text": ["La tua scatola è aggiornata. Domani le espressioni tornano al momento giusto. Se vuoi continuare, esplora i temi – senza fretta.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["Puoi riprendere la sessione quando vuoi – quello che è fatto, è fatto.", "Du kannst die Sessione jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 La mia collezione",
    "etape": "Passo {n}", "zeitmaschine": "⏳ Macchina del tempo", "trouve": "🔎 Trova l'espressione",
    "thema_ansage": ["Scegli una parte. Ogni parte: ascoltare e ripetere in tre passi, la macchina del tempo, e poi ritrovare le espressioni.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "Parte {n}",
    "dialog_hoeren": "👂 Ascolta", "repeter": "Ripeti", "tu_es": "🎭 Sei {rolle}", "role": "Ruolo", "repliques": "battute",
    "dialog_start": "▶ Inizia il dialogo", "dialog_hoeren_knopf": "▶ Ascolta il dialogo",
    "dialog_ok_rolle": "Cambia ruolo – o rifallo!", "dialog_ok": "Adesso tocca a te parlare!",
    "dialog_ansage_rolle": ["Sei {ich}. Di' le tue battute quando tocca a te – l'app parla per {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. Ascolta il dialogo.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Più facile: mostra le mie battute", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Capitolo {n}", "kapitel_ansage": ["Ascolta il capitolo o leggilo ad alta voce. Tocca un paragrafo per il tedesco.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Ascolta tutto il capitolo", "kapitel_weiter": "Capitolo seguente ➜",
    "kapitel_naechste": ["Il prossimo capitolo si sblocca con la tua prossima settimana perfetta.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["Il seguito è in scrittura.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Non ancora sbloccato", "semaine_parfaite": "Settimana perfetta",
    "mot": "Parola {n} / {alle}", "paire": "Coppia {n} / {alle}", "lentement": "🐢 Lentamente", "normal": "🔊 Normale",
    "lr_label": "Ascolta e ripeti", "parties_label": "Parti – accesso diretto",
    "trop_vite": "⏱️ Troppo veloce!", "trop_vite_text": ["Di' le frasi davvero, ad alta voce. Allora ci sono anche i punti. Ancora!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Ancora ➜", "termine": "{name}: finito!", "presque": ["Quasi! Manca ancora:", "Fast! Es fehlt noch:"],
    "thema_fertig": "Tutto il tema « {name} » è finito. Chapeau!", "autres_parties": "Altre parti",
    "stufen": [["Ascolta e ripeti! La frase tedesca ti aiuta.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["Quale parola manca? Di' tutta la frase e poi « Soluzione ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Soluzione“."],
               ["Di' la frase in italiano e poi « Soluzione ».", "Sag den Satz auf Italienisch, dann „Soluzione“."]],
    "dis_phrase": "Di' tutta la frase in italiano!", "phrase": "Frase {n} / {alle}",
    "tipp_buchstabe": ["Più facile: la prima lettera", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Più facile: la frase con il buco", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Oggi", "presente"], "pc": ["Ieri", "passato prossimo", "E ieri?"], "fp": ["Domani", "futuro semplice", "E domani?"]},
    "solution_zeit": "Soluzione: {zeit}",
    "zeit_ansage": ["Ascolta la frase di oggi. Poi dilla al passato e al futuro – ad alta voce. Dopo « Soluzione ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Soluzione“."],
    "expression": "Espressione {n} / {alle}",
    "bonus_weekend": "🏖️ Bonus del weekend +{p}", "en_feu": "Sei in serie! {n} giorni di fila", "en_feu_text": "{n} giorni di scuola di fila – +{p} punti!",
    "semaine_parfaite_titel": "Settimana perfetta!", "semaine_parfaite_text": "Hai lavorato tutti i giorni di scuola – +{p} punti.",
    "nouveau_chapitre": " Nuovo capitolo: « {titel} »", "suite_bientot": "",
    "mois_parfait": "Mese perfetto!", "mois_parfait_text": "{n} settimane perfette di fila – +{p} punti e una cornice d'oro!",
    "nouveau_titre": "Nuovo titolo: {name}!", "points": "punti", "jours_suite": "Giorni di scuola di fila",
    "visite": "visitato ✓",
    "ton_titre": "Il tuo titolo", "encore_points": "Mancano {n} punti per « {name} » {symbol}",
    "cette_semaine": "Questa settimana", "tage": ["Lun", "Mar", "Mer", "Gio", "Ven"],
    "serie_text": ["🔥 {n} giorni di scuola di fila · ⭐ {w} settimane perfette. Le vacanze e i giorni festivi non contano – la tua serie resta.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 La mia scatola ({n} espressioni)", "boite_text": ["Livello 0 = nuova o dimenticata · dal livello 3 l'espressione è ben radicata.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "g", "badges": "Distintivi",
    "badge_liste": ["In serie", "Settimana perfetta", "5 × perfetta", "Mese perfetto", "Eroe del weekend", "100 espressioni", "50 ben radicate"],
    "offline": "📥 Offline", "offline_text": ["Scarica gli audio di questa lingua per esercitarti senza connessione.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} file audio offline", "offline_laden": "📥 Scarica per usare offline", "offline_fertig": "✓ Disponibile offline",
    "bald": "in preparazione",
    "offline_laeuft": "Scaricamento… {n} / {alle}",
}
