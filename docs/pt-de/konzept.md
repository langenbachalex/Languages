# Konzeptblatt Portugiesisch (Paar `pt-de`) – „O meu português“

Stand: 18.10.2026. **Gebaut und veröffentlicht, noch ohne Audio** (Mr. Alex, 18.10.: Credits erst ab 13.11.). Bis dahin liest die Sprachausgabe des Geräts (pt-PT). Rahmen: `docs/konzept-mehrsprachig.md`. Alles wie bei Französisch, Spanisch und Italienisch, mit portugiesischen Inhalten.

## 1. Rahmen

- **Zielsprache:** europäisches Portugiesisch (Portugal): *tu* unter Freunden, formell *o senhor / a senhora* mit 3. Person, Verlaufsform *estar a* + Infinitiv, Pronomen nach dem Verb (*custa-me*), europäische Wörter (*autocarro, comboio, pequeno-almoço, bica, miúdos, giro, fixe*). Hilfe: Deutsch.
- **Gesprächspartner:** **Tiago**, Lehrer in Lissabon, Kollege wie Diego und Giovanni. Trockener Humor, sagt oft *« Pronto… »*.
- **Stimmen:** Mr. Alex' Klon mit `eleven_v4`, `language_code: pt` (das Modell kennt kein `pt-PT`; die europäische Schreibung im Text verankert den Akzent). Tiago: Wahl am 13.11. aus den Hörproben in `docs/pt-de/hoerprobe/` (Rui, Diogo, Lourenço, Afonso, Duarte; alle Portugal), gleich mit `eleven_v4`. Bis dahin `STIMME_B = None`.
- **Warum manche Partnerstimmen flach klingen (18.10.):** Sie laufen auf `eleven_multilingual_v2` und sind als ruhige Erzählerstimmen gewählt; der Klon läuft auf `eleven_v4`, das den Sinn spielt. Umstellung aller Partnerstimmen auf v4 ist für den 13.11. vorgemerkt (Erinnerung), erst mit Hörprobe je Paket.

## 2. Themen (je 24 Wendungen, mit Zeitmaschine hoje – ontem – amanhã)

| # | Thema | Beispiele |
|---|---|---|
| 1 | **Entre colegas** – mit Tiago | *corrigir testes, estar de rastos, como é que correu?, dar aulas, o intervalo, custa-me, valer a pena, desenrascar-se, estar a mil, pronto, podia repetir? (formell)* |
| 2 | **Sentimentos e ambientes** | *toca-me, estar em baixo, ter saudades de, parte-me o coração, pele de galinha, estar bem-disposto, uma tristeza bonita (Fado), os meus sentimentos (formell)* |
| 3 | **Os gatos** | *ronronar, fazer festas, pedir mimos, dormir a sesta, um gato vadio, fazer asneiras, estar-se nas tintas, a senhora tem gato? (formell)* |
| 4 | **Música e língua** | *cantar afinado, o refrão, ter ouvido, o sotaque, engolir as vogais, tocar guitarra (portuguesa), saber de cor, podia falar mais devagar? (formell)* |
| 5 | **Histórias e fantasia** | *era uma vez, a demanda, um feitiço, numa manhã de nevoeiro (D. Sebastião), o vilão, diz-se que, com o coração nas mãos, podia recomendar-me um livro? (formell)* |
| 6 | **Desporto e kung fu** | *treinar, um pontapé, aquecer, estar todo dorido, aguentar a posição, a faixa, recuperar o fôlego, posso inscrever-me? (formell)* |
| 7 | **Comer e viver bem** | *matar a fome, comer à grande, petiscar, a pastelaria, fresco como uma alface, apanhar ar, provar, queria um pastel de nata (formell)* |
| 8 | **Crianças e bebés** | *dormir a noite toda, fazer uma birra, pegar ao colo, os miúdos, a chucha, um beijinho, rir às gargalhadas, que idade tem o seu filho? (formell)* |
| ⚡ | **Falsos amigos** – gegen Englisch, Französisch, Spanisch | *esquisito, puxar, constipado, embaraçado, polvo, borracha, largo, propina, pasta, oficina, escritório, assistir a, pretender, atualmente, livraria, esperto, camisola, presunto, fábrica, balcão, novela* |

## 3. Aussprache « Os sons nasais »

Nasal gegen oral, das hörbare Herz des europäischen Portugiesisch: je 8 Wörter nasal (*pão, mão, mãe, irmã, bom, sim, cão, limão*) und oral (*pau, mau, pai, lá, avó, vi, céu, café*), 8 Minimalpaare (*pão/pau, mão/mau, lã/lá, vim/vi, som/só, mundo/mudo, lindo/lido, manta/mata*), 8 Wörter mit beiden (*avião, coração, alemão, feijão, balcão …*). Codes `nasal`, `oral`.

## 4. Spiel, Dialoge, Geschichte

- **Titel:** ☕ Bica → 🥧 Pastel de nata → 🐟 Sardinha → 🎣 Bacalhau → 🥪 Francesinha → 🍷 Vinho do Porto → ✨ **Grande chef**
- **Karte:** 18 Distrikte (Natural Earth admin-1, gemeinfrei; `inhalte/pt-de/karte/distritos.geojson`, Lader `werkzeuge/portugal_karte.py`), Açores und Madeira als gerahmte Einschübe im Atlantik links (Madeira ohne Ilhas Selvagens). Start in **Lisboa**, 50 Orte mit *curiosidades* (`orte.tsv`), Abzeichen « Volta a Portugal ».
- **Lob:** 83 Sprüche wie bei Spanisch (*Boa! · Fixe! · Na mouche! · Tiro-te o chapéu! · Pareces um lisboeta! …*).
- **Dialoge:** « Sexta-feira à tarde » (Lehrerzimmer) und « O gato melancólico » (Kaffeemaschine; Alex hat « Uma casa portuguesa » gesungen).
- **Geschichte « O segredo da Regaleira »:** Rita Carvalho, Lehrerin in Lissabon, findet in Duartes Arbeit eine Zugfahrkarte Rossio–Sintra. Kapitel 1 « O bilhete », 2 « O poço » (der Initiationsbrunnen der Quinta da Regaleira), 3 « A porta que não existe » (Raum mit Katzen-Azulejos, der Gärtner seit 1910). Gleiche Beats wie Alcázar, Torre, Bosporus, Umayyaden-Moschee.

## 5. Offen

- Audio nach dem 13.11.: Tiagos Stimme wählen, dann `python3 werkzeuge/audio.py pt-de` (Klon für Wendungen, Sätze, Zeiten, Geschichte, Orte, Lob, Aussprache; Tiago für seine Dialogzeilen).
- Vorlese-Korrekturen (`AUSSPRACHE_KORREKTUR`) erst nach der ersten Hörprobe.
