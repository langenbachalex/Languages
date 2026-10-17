"""Sprachpaket Türkisch (Ziel) – Deutsch (Hilfe). Studie: docs/tr/studie.md
Fünftes Paket in der Haupt-App (Entscheidung Mr. Alex 17.10.: konsistent mit den anderen Paketen). Partner Cem (Stimme « Can »).
TSV-Felder wie in allen Paketen: fr = Zielsprache, de = Hilfssprache. Zeitmaschine: bugün – dün (-di) – yarın (-ecek)."""
import os

PAAR = "tr-de"
NAME = "Benim Türkçem"
KURZ = "TR"
HILFE_KURZ = "DE"
FLAGGE = "🇹🇷"
LANG = "tr"
LANG_HILFE = "de"
SPRACHAUSGABE = "tr-TR"
TEMPO = 0.7   # Voreinstellung langsam (Mr. Alex, 17.10.); Schalter 🐢 0,7× / 1× in der Leiste
# Türkis und Rot (türkis = « turquoise », das Wort stammt von « Türkei »); hell und dunkel wie bei den anderen Sprachen
THEME = {"blau": "#1a6f7a", "rot": "#c8102e", "rot_text": "#ffffff", "dunkel": {"blau": "#6fd3de", "blau_text": "#07191c", "rot": "#ff7b88", "rot_text": "#1a0608"}}

# Themen in Lernreihenfolge – werden Thema für Thema ergänzt (jeweils nach Absegnung)
THEMEN = [
    {"id": "ogretmenler", "name": "Öğretmenler arasında", "de": "Unter Lehrern – mit Cem", "symbol": "🧑‍🏫", "datei": "ogretmenler.tsv"},
    {"id": "duygular", "name": "Duygular ve haller", "de": "Gefühle und Stimmungen", "symbol": "🎭", "datei": "duygular.tsv"},
    {"id": "kediler", "name": "Kediler", "de": "Die Katzen", "symbol": "🐈", "datei": "kediler.tsv"},
    {"id": "muzik", "name": "Müzik ve dil", "de": "Musik und Sprache", "symbol": "🎵", "datei": "muzik.tsv"},
]

# Titel – vom Çay bis zum Baklava
TITEL = [(0, "Çay", "🍵"), (300, "Simit", "🥯"), (900, "Börek", "🥐"), (1800, "Lahmacun", "🫓"),
         (3000, "Kebap", "🍢"), (4500, "Künefe", "🍮"), (6500, "Baklava", "👑")]
TITEL_ANSAGE = "Tebrikler! Artık sen {name}sin!"
SPIEL_TEXTE = {  # gesprochen von Mr. Alex (audio/spiel/<id>.mp3)
    "feuer": "Alev aldın! Üst üste üç gün!",
    "woche": "Mükemmel bir hafta! Her okul günü çalıştın. Aferin!",
    "monat": "Üst üste dört mükemmel hafta! Tam bir şampiyon!",
    "fini": "Bugünlük bu kadar. Yarın görüşürüz!",
}

# Dialoge: Rolle A = Alex (Mr. Alex' Stimme), Rolle B = Cem (Stimme « Can »)
ROLLEN = {"A": "Alex", "B": "Cem"}
DIALOGE_TITEL = ["Cem'le diyaloglar", "Dialoge mit Cem"]

# Geschichte in Istanbul (Titel und Kapitel folgen)
GESCHICHTE = {"titel": "Boğaz'ın sırrı",
              "unter": "İstanbul'da bir öğretmen, bir vapur bileti ve her şeyi bilen bir kedi.",
              "sammlung": ["Her mükemmel hafta bir bölüm açar: İstanbul'da bir öğretmen ve Boğaz'ın sırrı.",
                           "Jede perfekte Woche schaltet ein Kapitel frei: ein Lehrer in Istanbul und das Geheimnis des Bosporus."]}

# Aussprache-Modul: später (ı / i, ö / ü, weiches ğ, Betonung); Einzelwörter im Trägersatz
TRAEGERSATZ = "İyi dinle: {wort}."
AUSSPRACHE = None

# Karte: Türkei mit 81 İl (Natural Earth, gemeinfrei), Istanbul als mehrere Stationen, Start Istanbul
KARTE = {"name": "Türkiye", "einheit": "il", "lieux": "yer", "start": "İstanbul",
         "quelle": "Harita: Natural Earth (kamu malı), 81 il.",
         "badge": "Türkiye turu",
         "hinweis": ["Her biten seans ve her biten bölüm bir yer açar, İstanbul'dan başlayarak. Bir yere dokun!",
                     "Jede fertige Seans und jeder fertige Teil schalten einen Ort frei, Start in Istanbul. Tipp auf einen Ort!"]}


def karte_laden(inhalte):
    import tuerkei_karte
    return tuerkei_karte.laden(os.path.join(inhalte, "karte"))


# Stimmen (ElevenLabs): Mr. Alex' Klon auf Türkisch (Hörprobe 17.10.), Cem = « Can – Deep, Confident Turkish »
STIMME = {"id": "AK2WYGe96RmMwFKM5KEz", "modell": "eleven_v4", "language_code": "tr", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
STIMME_B = {"id": "SacdY6cqu2yrF7ExGIOe", "modell": "eleven_multilingual_v2", "einstellungen": {"stability": 0.5, "similarity_boost": 0.75}}
# « saat » (Doppelvokal) klang dumpf: Vorlese-Schreibung mit Silbentrennung, alle Formen
AUSSPRACHE_KORREKTUR = {"saat": "sa-at", "saatte": "sa-atte", "saate": "sa-ate", "saatten": "sa-atten", "saati": "sa-ati", "Saat": "Sa-at"}

# Oberflächentexte: [Zielsprache, Hilfe] oder nur Zielsprache
UI = {
    "app": "Language Learning",
    "gruss": ["Merhaba! Başlayalım mı?", "Selam! Hadi bakalım!", "İyi akşamlar! Kısa bir seans?"],
    "motto": ["Günde on dakika: önce seans, sonra ne istersen.", "Zehn Minuten am Tag: die Seans, danach was du willst."],
    "seance": "▶ Hadi başlayalım!", "seance_fertig": "✓ Bugünlük tamam",
    "seance_stand": "{neu} yeni · {wdh} tekrar · {fertig} / {gesamt} bitti",
    "seance_leer": "Bugün tekrar yok – konuları keşfet!",
    "themen": ["Konular", "Die Themen"], "expressions": "ifade", "parties": "bölüm",
    "bonus": ["Telaffuz ve hikâye", "Aussprache und Geschichte"],
    "kapitel_zahl": "{frei} / {alle} bölüm · her mükemmel haftada bir yenisi",
    "stand": ["Kutunda {n} ifade · {fest} iyice yerleşti · {orte} / {alle} yer gezildi",
              "{n} Wendungen in deinem Kasten · {fest} fest verankert (ab Stufe 3) · {orte} / {alle} Orte besucht"],
    "accueil": "Ana sayfa", "zurueck_accueil": "← Ana sayfa", "zurueck_thema": "← Konu", "suivant": "Sonraki ➜", "retour": "◀ Geri",
    "encore_hoeren": "🔊 Tekrar", "solution": "Çözüm", "hoeren": "🔊 Dinle", "stop": "■ Dur",
    "jetzt_du": "Sıra sende! Tekrarla.", "jetzt_du_dialog": "Sıra sende! Repliğini söyle.",
    "poli": "siz · kibar", "poli_titel": "Höflichkeitsform", "trou": "boşluk", "hilfe_zeigen": "Almancasını göster",
    "seance_titel": "Kelime Salonu", "nouvelle": "yeni", "revision": "tekrar · seviye {s}",
    "neu_ansage": ["Yeni ifade! Dinle ve tekrarla.", "Neue Wendung! Hör zu und sprich nach."],
    "exemple": "Örnek", "ziel_sprache": "Türkçe", "hilfe_sprache": "Deutsch",
    "wie_sagt_man": ["Türkçesi ne? Yüksek sesle söyle, sonra « Çözüm ».", "Wie sagt man das auf Türkisch? Sag es laut, dann „Çözüm“."],
    "je_savais": "😊 Biliyordum", "encore": "🔁 Tekrar", "pas_grave": "Sorun değil! Birazdan yine gelir.",
    "fini": "Bugünlük bu kadar!", "pause": "Mola!",
    "fini_text": ["Kutun güncel. Yarın ifadeler tam zamanında geri gelir. Devam etmek istersen konulara bak – baskı yok.",
                  "Dein Kasten ist auf dem neuesten Stand. Morgen kommen die Wendungen zum richtigen Zeitpunkt zurück. Wenn du weitermachen willst: die Themen, ohne Druck."],
    "pause_text": ["Seansa istediğin zaman devam edebilirsin – yapılan yapılmış sayılır.", "Du kannst die Seans jederzeit fortsetzen – was gemacht ist, bleibt gemacht."],
    "sammlung": "🏆 Koleksiyonum",
    "etape": "Adım {n}", "zeitmaschine": "⏳ Zaman makinesi", "trouve": "🔎 İfadeyi bul",
    "thema_ansage": ["Bir bölüm seç. Her bölüm: üç adımda dinle ve tekrarla, zaman makinesi, sonra ifadeleri yeniden bul.",
                     "Wähl einen Teil. Jeder Teil: hören und nachsprechen in drei Stufen, Zeitmaschine, dann die Wendungen wiederfinden."],
    "partie": "Bölüm {n}",
    "dialog_hoeren": "👂 Dinle", "repeter": "Tekrarla", "tu_es": "🎭 Sen {rolle}sin", "role": "Rol", "repliques": "replik",
    "dialog_start": "▶ Diyaloğu başlat", "dialog_hoeren_knopf": "▶ Diyaloğu dinle",
    "dialog_ok_rolle": "Rol değiştir – ya da bir kez daha!", "dialog_ok": "Şimdi konuşma sırası sende!",
    "dialog_ansage_rolle": ["Sen {ich}sin. Sıra sana gelince repliklerini söyle – uygulama {andere} için konuşur.",
                            "Du bist {ich}. Sprich deine Zeilen, wenn du dran bist – die App spricht {andere}."],
    "dialog_ansage": ["« {titel} » – {ort}. Diyaloğu dinle.", "„{titel}“ – {ort}. Hör dir den Dialog an."],
    "dialog_tipp": ["Daha kolay: repliklerimi göster", "Noch einfacher: meine Zeilen zeigen"],
    "chapitre": "Bölüm {n}", "kapitel_ansage": ["Bölümü dinle ya da yüksek sesle oku. Almancası için bir paragrafa dokun.", "Hör das Kapitel, oder lies es laut. Tipp auf einen Absatz für Deutsch."],
    "kapitel_alles": "▶ Bütün bölümü dinle", "kapitel_weiter": "Sonraki bölüm ➜",
    "kapitel_naechste": ["Sonraki bölüm, bir sonraki mükemmel haftanla açılır.", "Das nächste Kapitel kommt mit deiner nächsten perfekten Woche."],
    "kapitel_ende": ["Devamı yazılıyor.", "Die Fortsetzung wird gerade geschrieben."],
    "pas_debloque": "Henüz açılmadı", "semaine_parfaite": "Mükemmel hafta",
    "mot": "Kelime {n} / {alle}", "paire": "Çift {n} / {alle}", "lentement": "🐢 Yavaş", "normal": "🔊 Normal",
    "lr_label": "Dinle ve tekrarla", "parties_label": "Bölümler – doğrudan erişim",
    "trop_vite": "⏱️ Çok hızlı!", "trop_vite_text": ["Cümleleri gerçekten yüksek sesle söyle. O zaman puan da var. Bir kez daha!", "Sprich die Sätze wirklich laut. Dann gibt es auch Punkte. Noch mal!"],
    "encore_fois": "Bir kez daha ➜", "termine": "{name}: bitti!", "presque": ["Az kaldı! Eksik olan:", "Fast! Es fehlt noch:"],
    "thema_fertig": "« {name} » konusunun tamamı bitti. Helal olsun!", "autres_parties": "Diğer bölümler",
    "stufen": [["Dinle ve tekrarla! Almanca cümle sana yardım eder.", "Hör zu und sprich nach! Der deutsche Satz hilft dir."],
               ["Hangi kelime eksik? Bütün cümleyi söyle, sonra « Çözüm ».", "Welches Wort fehlt? Sag den ganzen Satz, dann „Çözüm“."],
               ["Cümleyi Türkçe söyle, sonra « Çözüm ».", "Sag den Satz auf Türkisch, dann „Çözüm“."]],
    "dis_phrase": "Bütün cümleyi Türkçe söyle!", "phrase": "Cümle {n} / {alle}",
    "tipp_buchstabe": ["Daha kolay: ilk harf", "Noch einfacher: erster Buchstabe"],
    "tipp_luecke": ["Daha kolay: boşluklu cümle", "Noch einfacher: Satz mit Lücke"],
    "zeiten": {"jetzt": ["Bugün", "şimdiki zaman"], "pc": ["Dün", "geçmiş zaman (-di)", "Ya dün?"], "fp": ["Yarın", "gelecek zaman (-ecek)", "Ya yarın?"]},
    "solution_zeit": "Çözüm: {zeit}",
    "zeit_ansage": ["Bugünün cümlesini dinle. Sonra dünü ve yarını söyle – yüksek sesle. Ardından « Çözüm ».",
                    "Hör den Satz von heute. Dann sag ihn in der Vergangenheit und in der Zukunft – laut. Danach „Çözüm“."],
    "expression": "İfade {n} / {alle}",
    "bonus_weekend": "🏖️ Hafta sonu bonusu +{p}", "en_feu": "Alev aldın! Üst üste {n} gün", "en_feu_text": "Üst üste {n} okul günü – +{p} puan!",
    "semaine_parfaite_titel": "Mükemmel hafta!", "semaine_parfaite_text": "Her okul günü çalıştın – +{p} puan.",
    "nouveau_chapitre": " Yeni bölüm: « {titel} »!", "suite_bientot": " Hikâyenin devamı yakında.",
    "mois_parfait": "Mükemmel ay!", "mois_parfait_text": "Üst üste {n} mükemmel hafta – +{p} puan ve altın çerçeve!",
    "nouveau_titre": "Yeni unvan: {name}!", "points": "puan", "jours_suite": "Üst üste okul günü",
    "visite": "gezildi ✓",
    "ton_titre": "Unvanın", "encore_points": "« {name} » {symbol} için {n} puan daha",
    "cette_semaine": "Bu hafta", "tage": ["Pzt", "Sal", "Çar", "Per", "Cum"],
    "serie_text": ["🔥 üst üste {n} okul günü · ⭐ {w} mükemmel hafta. Tatiller ve bayramlar sayılmaz – serin devam eder.",
                   "🔥 {n} Schultage am Stück · ⭐ {w} perfekte Wochen. Ferien und Feiertage zählen nicht – deine Serie bleibt."],
    "boite": "📦 Kutum ({n} ifade)", "boite_text": ["Seviye 0 = yeni ya da unutulmuş · seviye 3'ten itibaren ifade iyice yerleşmiştir.", "Stufe 0 = neu oder vergessen · ab Stufe 3 sitzt die Wendung."],
    "jours": "g", "badges": "Rozetler",
    "badge_liste": ["Alev aldın", "Mükemmel hafta", "5 × mükemmel", "Mükemmel ay", "Hafta sonu kahramanı", "100 ifade", "50 iyice yerleşmiş"],
    "offline": "📥 Çevrimdışı", "offline_text": ["Bağlantısız çalışmak için bu dilin seslerini indir.", "Lade die Audios dieser Sprache, um ohne Verbindung zu üben."],
    "offline_stand": "{n} / {alle} ses dosyası çevrimdışı", "offline_laden": "📥 Çevrimdışı için indir", "offline_fertig": "✓ Çevrimdışı kullanılabilir",
    "bald": "hazırlanıyor",
    "offline_laeuft": "İndiriliyor… {n} / {alle}",
}
