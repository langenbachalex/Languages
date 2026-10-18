"""Sprachpaket Portugiesisch (Ziel, Portugal) – Deutsch (Hilfe). Konzept: docs/pt-de/konzept.md
TSV-Felder wie in allen Paketen: fr = Zielsprache, de = Hilfssprache. Zeitmaschine: hoje (presente) – ontem (pretérito perfeito simples) – amanhã (ir + infinitivo).
Gebaut ohne Audio (Mr. Alex, 18.10.: Credits erst ab 13.11.); bis dahin spricht die Sprachausgabe des Geräts (pt-PT)."""
import os

PAAR = "pt-de"
NAME = "O meu português"
KURZ = "PT"
HILFE_KURZ = "DE"
FLAGGE = "🇵🇹"
LANG = "pt"
LANG_HILFE = "de"
SPRACHAUSGABE = "pt-PT"
THEME = {"blau": "#00603a", "rot": "#c8102e", "rot_text": "#ffffff", "dunkel": {"blau": "#6fd6a4", "blau_text": "#03200f", "rot": "#ff8a96", "rot_text": "#2a0408"}}   # Grün und Rot

# Themen in Lernreihenfolge
THEMEN = [
    {"id": "colegas", "name": "Entre colegas", "de": "Unter Lehrern – mit Tiago", "symbol": "🧑‍🏫", "datei": "entre_colegas.tsv"},
    {"id": "sentimentos", "name": "Sentimentos e ambientes", "de": "Gefühle und Stimmungen", "symbol": "🎭", "datei": "sentimentos.tsv"},
    {"id": "gatos", "name": "Os gatos", "de": "Die Katzen", "symbol": "🐈", "datei": "gatos.tsv"},
    {"id": "musica", "name": "Música e língua", "de": "Musik und Sprache", "symbol": "🎵", "datei": "musica.tsv"},
    {"id": "historias", "name": "Histórias e fantasia", "de": "Geschichten und Fantasy", "symbol": "🐉", "datei": "historias.tsv"},
    {"id": "desporto", "name": "Desporto e kung fu", "de": "Sport und Kung-Fu", "symbol": "🥋", "datei": "desporto.tsv"},
    {"id": "comer", "name": "Comer e viver bem", "de": "Essen und gut leben", "symbol": "🐟", "datei": "comer.tsv"},
    {"id": "criancas", "name": "Crianças e bebés", "de": "Kinder und Babys", "symbol": "👶", "datei": "criancas.tsv"},
    {"id": "falsos_amigos", "name": "Falsos amigos", "de": "Falsche Freunde Englisch/Französisch/Spanisch–Portugiesisch (Bonus)", "symbol": "⚡", "datei": "falsos_amigos.tsv"},
]

# Titel – Leiter der Leckereien
TITEL = [(0, "Bica", "☕"), (300, "Pastel de nata", "🥧"), (900, "Sardinha", "🐟"), (1800, "Bacalhau", "🎣"),
         (3000, "Francesinha", "🥪"), (4500, "Vinho do Porto", "🍷"), (6500, "Grande chef", "✨")]
TITEL_ANSAGE = "Parabéns! Agora és {name}!"
SPIEL_TEXTE = {
    "feuer": "Estás em série! Três dias seguidos!",
    "woche": "Semana perfeita! Trabalhaste todos os dias de aulas. Boa!",
    "monat": "Quatro semanas perfeitas seguidas! És um campeão!",
    "fini": "Por hoje, chega. Até amanhã!",
}

# Dialoge: A = Alex (Mr. Alex' Stimme), B = Tiago (Stimme nach Wahl am 13.11.)
ROLLEN = {"A": "Alex", "B": "Tiago"}
DIALOGE_TITEL = ["Diálogos com o Tiago", "Dialoge mit Tiago"]

GESCHICHTE = {"titel": "O segredo da Regaleira",
              "unter": "Rita Carvalho, professora em Lisboa – um bilhete, uma porta que não existe, um gato que sabe.",
              "sammlung": ["Cada semana perfeita desbloqueia um capítulo: Rita Carvalho, professora em Lisboa, e o mistério da Regaleira.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: Rita Carvalho, Lehrerin in Lissabon, und das Geheimnis der Regaleira."]}

# Aussprache « Os sons nasais »: nasal gegen oral – das hörbare Herz des europäischen Portugiesisch
TRAEGERSATZ = "Ouve bem… {wort}."   # Einzelwörter im Trägersatz, die Pause dient dem Schnitt (audio.py)
AUSSPRACHE = {
    "id": "sons", "symbol": "👃", "titel": "Os sons nasais", "unter": "nasal [ɐ̃w̃ ɐ̃ õ ĩ] ou oral – ouvir, distinguir, os dois numa palavra",
    "datei": "sons.tsv",
    "klaenge": {"nasal": ["[ɐ̃w̃] [ɐ̃]", "ão · ã · m/n depois da vogal", "o ar sai também pelo nariz", "Luft auch durch die Nase (pão, mãe, sim)"],
                "oral": ["[aw] [a]", "au · á · vogal sem til", "o ar sai só pela boca", "Luft nur durch den Mund (pau, lá, vi)"]},
    "reihe": ["nasal", "oral"],
    "paare": [["p1", "Nasal ou oral?"]],
    "beide_name": "👑 Os dois",
    "texte": {
        "beide": ["Nasal e oral na mesma palavra. Ouve devagar, depois à velocidade normal – e repete com cuidado.",
                  "Nasal und oral in einem Wort. Hör langsam, dann normal – und sprich sorgfältig nach."],
        "klang": ["{laut} – {tipp}. Ouve devagar, depois normal. Repete!", "{laut} – {tipp}. Hör langsam, dann normal. Sprich nach!"],
        "paar": ["Ouve a palavra. Qual é? Toca na certa.", "Hör das Wort. Welches ist es? Tipp auf das richtige."],
        "hilfe": ["Eu ajudo: {a}. Ouve outra vez!", "Ich helfe dir: {a}. Hör noch mal!"],
        "beide_hoeren": ["Mais fácil: ouvir as duas", "Noch einfacher: beide hören"],
    },
}

# Karte: Portugal mit 18 Distrikten, Açores und Madeira als Einschübe (Natural Earth, gemeinfrei)
KARTE = {"name": "Portugal", "einheit": "distritos", "lieux": "lugares", "start": "Lisboa",
         "quelle": "Mapa: distritos e regiões autónomas de Portugal via Natural Earth (domínio público).", "badge": "Volta a Portugal",
         "hinweis": ["Cada sessão terminada e cada parte terminada desbloqueiam um lugar, a começar por Lisboa. Toca num lugar!",
                     "Jede fertige Sessão und jeder fertige Teil schalten einen Ort frei, Start in Lissabon. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import portugal_karte
    return portugal_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen: Mr. Alex' Klon auf Portugiesisch (eleven_v4 kennt nur « pt », kein « pt-PT » – europäische Schreibung im Text verankert den Akzent).
# Tiago: Wahl am 13.11. aus docs/pt-de/hoerprobe (Rui, Diogo, Lourenço, Afonso, Duarte), gleich mit eleven_v4. Bis dahin None = keine Aufnahme.
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "pt", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = None

UI = {
    "app": "Language Learning",
    "gruss": ["Bom dia! Vamos?", "Olá! Começamos?", "Boa noite! Uma sessão curta?"],
    "motto": ["Dez minutos por dia: a sessão, e depois o que quiseres.", "Zehn Minuten am Tag: die Sessão, danach was du willst."],
    "seance": "▶ Vamos!", "seance_fertig": "✓ Feito por hoje",
    "seance_stand": "{neu} novas · {wdh} para rever · {fertig} / {gesamt} feitas",
    "seance_leer": "Nada para rever hoje – explora os temas!",
    "themen": ["Os temas", "Die Themen"], "expressions": "expressões", "parties": "partes",
    "bonus": ["Pronúncia e história", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} capítulos · um novo por semana perfeita",
    "stand": ["{n} expressões na tua caixa · {fest} bem assentes · {orte} / {alle} lugares visitados",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Início", "zurueck_accueil": "← Início", "zurueck_thema": "← Tema", "suivant": "Seguinte ➜", "retour": "◀ Voltar",
    "encore_hoeren": "🔊 Outra vez", "solution": "Solução", "hoeren": "🔊 Ouvir", "stop": "■ Parar",
    "jetzt_du": "É a tua vez! Repete.", "jetzt_du_dialog": "É a tua vez! Diz a tua frase.",
    "poli": "você / o senhor · formal", "poli_titel": "Höflichkeitsform", "trou": "espaço", "hilfe_zeigen": "Deutsch anzeigen",
    "seance_titel": "Ginásio de palavras", "nouvelle": "nova", "revision": "revisão · nível {s}",
    "neu_ansage": ["Expressão nova! Ouve e repete.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Exemplo", "ziel_sprache": "Português", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["Como se diz em português? Diz em voz alta e depois « Solução ».", "Wie sagt man das auf Portugiesisch? Sag es laut, dann „Solução“."],
    "je_savais": "😊 Eu sabia", "encore": "🔁 Outra vez", "pas_grave": "Não faz mal! Volta daqui a pouco.",
    "fini": "Por hoje, chega!", "pause": "Pausa!",
    "fini_text": ["A tua caixa está em dia. Amanhã, as expressões voltam no momento certo. Se quiseres continuar, explora os temas – sem pressão.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["Podes retomar a sessão quando quiseres – o que está feito, está feito.", "Du kannst die Sessão jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 A minha coleção",
    "etape": "Passo {n}", "zeitmaschine": "⏳ Máquina do tempo", "trouve": "🔎 Encontra a expressão",
    "thema_ansage": ["Escolhe uma parte. Cada parte: ouvir e repetir em três passos, a máquina do tempo, e depois encontrar as expressões.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "Parte {n}",
    "dialog_hoeren": "👂 Ouvir", "repeter": "Repetir", "tu_es": "🎭 És o {rolle}", "role": "Papel", "repliques": "falas",
    "dialog_start": "▶ Começar o diálogo", "dialog_hoeren_knopf": "▶ Ouvir o diálogo",
    "dialog_ok_rolle": "Troca de papel – ou repete!", "dialog_ok": "Agora és tu a falar!",
    "dialog_ansage_rolle": ["És o {ich}. Diz as tuas falas quando for a tua vez – a app fala pelo {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. Ouve o diálogo.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Mais fácil: mostrar as minhas falas", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Capítulo {n}", "kapitel_ansage": ["Ouve o capítulo ou lê-o em voz alta. Toca num parágrafo para o alemão.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Ouvir o capítulo todo", "kapitel_weiter": "Capítulo seguinte ➜",
    "kapitel_naechste": ["O próximo capítulo desbloqueia com a tua próxima semana perfeita.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["A continuação está a ser escrita.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Ainda não desbloqueado", "semaine_parfaite": "Semana perfeita",
    "mot": "Palavra {n} / {alle}", "paire": "Par {n} / {alle}", "lentement": "🐢 Devagar", "normal": "🔊 Normal",
    "lr_label": "Ouvir e repetir", "parties_label": "Partes – acesso direto",
    "trop_vite": "⏱️ Demasiado rápido!", "trop_vite_text": ["Diz as frases a sério, em voz alta. Assim há pontos. Outra vez!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Outra vez ➜", "termine": "{name}: terminado!", "presque": ["Quase! Ainda falta:", "Fast! Es fehlt noch:"],
    "thema_fertig": "O tema « {name} » está todo terminado. Bravo!", "autres_parties": "Outras partes",
    "stufen": [["Ouve e repete! A frase alemã ajuda-te.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["Que palavra falta? Diz a frase toda e depois « Solução ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Solução“."],
               ["Diz a frase em português e depois « Solução ».", "Sag den Satz auf Portugiesisch, dann „Solução“."]],
    "dis_phrase": "Diz a frase toda em português!", "phrase": "Frase {n} / {alle}",
    "tipp_buchstabe": ["Mais fácil: a primeira letra", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Mais fácil: a frase com espaço", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Hoje", "presente"], "pc": ["Ontem", "pretérito perfeito", "E ontem?"], "fp": ["Amanhã", "ir + infinitivo", "E amanhã?"]},
    "solution_zeit": "Solução: {zeit}",
    "zeit_ansage": ["Ouve a frase de hoje. Depois diz no passado e no futuro – em voz alta. A seguir « Solução ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Solução“."],
    "expression": "Expressão {n} / {alle}",
    "bonus_weekend": "🏖️ Bónus de fim de semana +{p}", "en_feu": "Estás em série! {n} dias seguidos", "en_feu_text": "{n} dias de aulas seguidos – +{p} pontos!",
    "semaine_parfaite_titel": "Semana perfeita!", "semaine_parfaite_text": "Trabalhaste todos os dias de aulas – +{p} pontos.",
    "nouveau_chapitre": " Capítulo novo: « {titel} »", "suite_bientot": "",
    "mois_parfait": "Mês perfeito!", "mois_parfait_text": "{n} semanas perfeitas seguidas – +{p} pontos e uma moldura dourada!",
    "nouveau_titre": "Título novo: {name}!", "points": "pontos", "jours_suite": "Dias de aulas seguidos",
    "visite": "visitado ✓",
    "ton_titre": "O teu título", "encore_points": "Faltam {n} pontos para « {name} » {symbol}",
    "cette_semaine": "Esta semana", "tage": ["Seg", "Ter", "Qua", "Qui", "Sex"],
    "serie_text": ["🔥 {n} dias de aulas seguidos · ⭐ {w} semanas perfeitas. As férias e os feriados não contam – a tua série mantém-se.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 A minha caixa ({n} expressões)", "boite_text": ["Nível 0 = nova ou esquecida · a partir do nível 3, a expressão está bem assente.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "d", "badges": "Medalhas",
    "badge_liste": ["Em série", "Semana perfeita", "5 × perfeita", "Mês perfeito", "Herói do fim de semana", "100 expressões", "50 bem assentes"],
    "offline": "📥 Sem ligação", "offline_text": ["Descarrega os áudios desta língua para praticar sem ligação.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} ficheiros de áudio sem ligação", "offline_laden": "📥 Descarregar para usar sem ligação", "offline_fertig": "✓ Disponível sem ligação",
    "bald": "em preparação",
    "offline_laeuft": "A descarregar… {n} / {alle}",
}
