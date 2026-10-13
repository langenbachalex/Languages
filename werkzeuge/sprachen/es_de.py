"""Sprachpaket Spanisch (Ziel, Spanien) – Deutsch (Hilfe). Konzept: docs/es-de/konzept.md
TSV-Felder wie in allen Paketen: fr = Zielsprache, de = Hilfssprache. Zeitmaschine: hoy (presente) – ayer (pretérito indefinido) – mañana (ir a + infinitivo)."""
import os

PAAR = "es-de"
NAME = "Mi español"
KURZ = "ES"
HILFE_KURZ = "DE"
FLAGGE = "🇪🇸"
LANG = "es"
LANG_HILFE = "de"
SPRACHAUSGABE = "es-ES"
THEME = {"blau": "#8a1c1c", "rot": "#e0a800"}   # Rot und Gold

# Themen in Lernreihenfolge – werden Thema für Thema ergänzt (jeweils nach Absegnung)
THEMEN = [
    {"id": "profes", "name": "Entre profes", "de": "Unter Lehrern – mit Diego", "symbol": "🧑‍🏫", "datei": "entre_profes.tsv"},
    {"id": "sentimientos", "name": "Sentimientos y ambientes", "de": "Gefühle und Stimmungen", "symbol": "🎭", "datei": "sentimientos.tsv"},
    {"id": "gatos", "name": "Los gatos", "de": "Die Katzen", "symbol": "🐈", "datei": "gatos.tsv"},
    {"id": "musica", "name": "Música y lengua", "de": "Musik und Sprache", "symbol": "🎵", "datei": "musica.tsv"},
    {"id": "historias", "name": "Historias y fantasía", "de": "Geschichten und Fantasy", "symbol": "🐉", "datei": "historias.tsv"},
    {"id": "deporte", "name": "Deporte y kung-fu", "de": "Sport und Kung-Fu", "symbol": "🥋", "datei": "deporte.tsv"},
    {"id": "comer", "name": "Comer y vivir bien", "de": "Essen und gut leben", "symbol": "🥘", "datei": "comer.tsv"},
    {"id": "ninos", "name": "Niños y bebés", "de": "Kinder und Babys", "symbol": "👶", "datei": "ninos.tsv"},
    {"id": "falsos_amigos", "name": "Falsos amigos", "de": "Falsche Freunde Englisch/Französisch–Spanisch (Bonus)", "symbol": "⚡", "datei": "falsos_amigos.tsv"},
]

# Titel – Tapas-Leiter
TITEL = [(0, "Aceituna", "🫒"), (300, "Tortilla", "🥔"), (900, "Gambas", "🍤"), (1800, "Paella", "🥘"),
         (3000, "Jamón", "🍖"), (4500, "Manchego", "🧀"), (6500, "Gran chef", "✨")]
TITEL_ANSAGE = "¡Enhorabuena! ¡Ahora eres {name}!"
SPIEL_TEXTE = {
    "feuer": "¡Estás en racha! ¡Tres días seguidos!",
    "woche": "¡Semana perfecta! Has trabajado todos los días de clase. ¡Olé!",
    "monat": "¡Cuatro semanas perfectas seguidas! ¡Qué campeón!",
    "fini": "Se acabó por hoy. ¡Hasta mañana!",
}

# Dialoge: A = Alex (Mr. Alex' Stimme), B = Diego (Carmelo)
ROLLEN = {"A": "Alex", "B": "Diego"}
DIALOGE_TITEL = ["Diálogos con Diego", "Dialoge mit Diego"]

GESCHICHTE = {"titel": "", "unter": "", "sammlung": ["", ""]}   # später, optional

# Aussprache « Los sonidos difíciles » – Daten kommen später (sonidos.tsv vorerst leer)
AUSSPRACHE = None  # kein Aussprachemodul im Spanischen (Mr. Alex, 13.10.2026)

# Karte: Spanien mit Provinzen – kommt später (vorerst keine Orte)
KARTE = {"name": "España", "einheit": "provincias", "lieux": "lugares", "start": "Sevilla",
         "quelle": "", "badge": "Vuelta a España",
         "hinweis": ["Cada sesión terminada y cada parte terminada desbloquean un lugar, empezando por Sevilla. ¡Toca un lugar!",
                     "Jede fertige Sesión und jeder fertige Teil schalten einen Ort frei, Start in Sevilla. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    """Noch keine Karte: leere Gebiete; Orte-Datei ist leer."""
    return {}, (lambda lon, lat: None), (lambda lon, lat: (0, 0))


# Stimmen: Mr. Alex' Klon auf Spanisch (Hörproben 13.10. freigegeben, Dentale geprüft), Diego = „Carmelo – Mature, Mysterious and Clear“
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "es", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "5egO01tkUjEzu7xSSE8M", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
AUSSPRACHE_KORREKTUR = {}

UI = {
    "app": "Language Learning",
    "gruss": ["¡Buenos días! ¿Vamos?", "¡Hola! ¿Nos ponemos?", "¡Buenas noches! ¿Una sesión corta?"],
    "motto": ["Diez minutos al día: la sesión, y luego lo que quieras.", "Zehn Minuten am Tag: die Sesión, danach was du willst."],
    "seance": "▶ Mi sesión de hoy", "seance_fertig": "✓ Sesión de hoy terminada",
    "seance_stand": "{neu} nuevas · {wdh} para repasar · {fertig} / {gesamt} hechas",
    "seance_leer": "Nada que repasar hoy – ¡explora los temas!",
    "themen": ["Los temas", "Die Themen"], "expressions": "expresiones", "parties": "partes",
    "bonus": ["Pronunciación e historia", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} capítulos · uno nuevo por semana perfecta",
    "stand": ["{n} expresiones en tu caja · {fest} bien asentadas · {orte} / {alle} lugares visitados",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Inicio", "zurueck_accueil": "← Inicio", "zurueck_thema": "← Tema", "suivant": "Siguiente ➜", "retour": "◀ Atrás",
    "encore_hoeren": "🔊 Otra vez", "solution": "Solución", "hoeren": "🔊 Escuchar", "stop": "■ Stop",
    "jetzt_du": "¡Te toca! Repite.", "jetzt_du_dialog": "¡Te toca! Di tu frase.",
    "poli": "usted · formal", "poli_titel": "Höflichkeitsform", "trou": "hueco", "hilfe_zeigen": "Deutsch anzeigen",
    "seance_titel": "Mi sesión de hoy", "nouvelle": "nueva", "revision": "repaso · nivel {s}",
    "neu_ansage": ["¡Expresión nueva! Escucha y repite.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Ejemplo", "ziel_sprache": "Español", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["¿Cómo se dice en español? Dilo en voz alta y luego « Solución ».", "Wie sagt man das auf Spanisch? Sag es laut, dann „Solución“."],
    "je_savais": "😊 Lo sabía", "encore": "🔁 Otra vez", "pas_grave": "¡No pasa nada! Vuelve dentro de un rato.",
    "fini": "¡Se acabó por hoy!", "pause": "¡Pausa!",
    "fini_text": ["Tu caja está al día. Mañana, las expresiones vuelven en el momento justo. Si quieres seguir, explora los temas – sin presión.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["Puedes retomar la sesión cuando quieras – lo hecho, hecho está.", "Du kannst die Sesión jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 Mi colección",
    "etape": "Paso {n}", "zeitmaschine": "⏳ Máquina del tiempo", "trouve": "🔎 Encuentra la expresión",
    "thema_ansage": ["Elige una parte. Cada parte: escuchar y repetir en tres pasos, la máquina del tiempo, y luego encontrar las expresiones.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "Parte {n}",
    "dialog_hoeren": "👂 Escuchar", "repeter": "Repetir", "tu_es": "🎭 Eres {rolle}", "role": "Papel", "repliques": "frases",
    "dialog_start": "▶ Empezar el diálogo", "dialog_hoeren_knopf": "▶ Escuchar el diálogo",
    "dialog_ok_rolle": "Cambia de papel – ¡o repítelo!", "dialog_ok": "¡Ahora te toca hablar a ti!",
    "dialog_ansage_rolle": ["Eres {ich}. Di tus frases cuando te toque – la app habla por {andere}.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. Escucha el diálogo.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Más fácil: mostrar mis frases", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Capítulo {n}", "kapitel_ansage": ["Escucha el capítulo o léelo en voz alta. Toca un párrafo para el alemán.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Escuchar todo el capítulo", "kapitel_weiter": "Capítulo siguiente ➜",
    "kapitel_naechste": ["El próximo capítulo se desbloquea con tu próxima semana perfecta.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["La continuación se está escribiendo.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Todavía no desbloqueado", "semaine_parfaite": "Semana perfecta",
    "mot": "Palabra {n} / {alle}", "paire": "Par {n} / {alle}", "lentement": "🐢 Despacio", "normal": "🔊 Normal",
    "lr_label": "Escuchar y repetir", "parties_label": "Partes – acceso directo",
    "trop_vite": "⏱️ ¡Demasiado rápido!", "trop_vite_text": ["Di las frases de verdad, en voz alta. Entonces hay puntos. ¡Otra vez!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Otra vez ➜", "termine": "{name}: ¡terminado!", "presque": ["¡Casi! Todavía falta:", "Fast! Es fehlt noch:"],
    "thema_fertig": "Todo el tema « {name} » está terminado. ¡Chapó!", "autres_parties": "Otras partes",
    "stufen": [["¡Escucha y repite! La frase alemana te ayuda.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["¿Qué palabra falta? Di toda la frase y luego « Solución ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Solución“."],
               ["Di la frase en español y luego « Solución ».", "Sag den Satz auf Spanisch, dann „Solución“."]],
    "dis_phrase": "¡Di toda la frase en español!", "phrase": "Frase {n} / {alle}",
    "tipp_buchstabe": ["Más fácil: la primera letra", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Más fácil: la frase con hueco", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Hoy", "presente"], "pc": ["Ayer", "pretérito indefinido", "¿Y ayer?"], "fp": ["Mañana", "ir a + infinitivo", "¿Y mañana?"]},
    "solution_zeit": "Solución: {zeit}",
    "zeit_ansage": ["Escucha la frase de hoy. Luego dila en pasado y en futuro – en voz alta. Después « Solución ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Solución“."],
    "expression": "Expresión {n} / {alle}",
    "bonus_weekend": "🏖️ Bonus de fin de semana +{p}", "en_feu": "¡Estás en racha! {n} días seguidos", "en_feu_text": "{n} días de clase seguidos – ¡+{p} puntos!",
    "semaine_parfaite_titel": "¡Semana perfecta!", "semaine_parfaite_text": "Has trabajado todos los días de clase – +{p} puntos.",
    "nouveau_chapitre": " Nuevo capítulo: « {titel} »", "suite_bientot": "",
    "mois_parfait": "¡Mes perfecto!", "mois_parfait_text": "{n} semanas perfectas seguidas – ¡+{p} puntos y un marco dorado!",
    "nouveau_titre": "¡Nuevo título: {name}!", "points": "puntos", "jours_suite": "Días de clase seguidos",
    "visite": "visitado ✓",
    "ton_titre": "Tu título", "encore_points": "Faltan {n} puntos para « {name} » {symbol}",
    "cette_semaine": "Esta semana", "tage": ["Lun", "Mar", "Mié", "Jue", "Vie"],
    "serie_text": ["🔥 {n} días de clase seguidos · ⭐ {w} semanas perfectas. Las vacaciones y los festivos no cuentan – tu racha se mantiene.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 Mi caja ({n} expresiones)", "boite_text": ["Nivel 0 = nueva u olvidada · a partir del nivel 3, la expresión está bien asentada.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "d", "badges": "Insignias",
    "badge_liste": ["En racha", "Semana perfecta", "5 × perfecta", "Mes perfecto", "Héroe del fin de semana", "100 expresiones", "50 bien asentadas"],
    "offline": "📥 Sin conexión", "offline_text": ["Descarga los audios de este idioma para practicar sin conexión.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} archivos de audio sin conexión", "offline_laden": "📥 Descargar para usar sin conexión", "offline_fertig": "✓ Disponible sin conexión",
    "bald": "en preparación",
    "offline_laeuft": "Descargando… {n} / {alle}",
}
