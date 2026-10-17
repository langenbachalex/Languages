/* Language Learning – persönliche Sprach-App für Mr. Alex (docs/konzept-mehrsprachig.md)
   Eine App, mehrere Sprachpaare (Ziel + Hilfe), Umschalter oben. Jedes Paar bringt seine Daten und Oberflächentexte mit
   (werkzeuge/sprachen/<paar>.py → daten_<paar>.js). Kein Konto; Fortschritt bleibt nur auf diesem Gerät (localStorage):
   pro Sprache Kartenstapel, Teile, Punkte und Titel – gemeinsam die Serie (Schultage, perfekte Wochen).
   Kern: die tägliche Séance – 3 neue Wendungen + höchstens 8 Wiederholungen (Leitner) pro Sprache, danach ist Schluss.
   Datenfelder heißen in allen Paaren gleich: fr = Zielsprache, de = Hilfssprache. */
(function () {
  "use strict";

  const PAKETE = window.SPRACHEN || {};
  const PAARE = Object.keys(PAKETE);
  const app = document.getElementById("app");
  // Speicherschlüssel je Web-App (index.html setzt window.APP_KONFIG; Englisch läuft getrennt unter english/)
  const KONFIG = window.APP_KONFIG || {};
  const SPEICHER = KONFIG.speicher || "languages-v1", ALT = KONFIG.alt === undefined ? "francais-v1" : KONFIG.alt;
  const GRUPPE = 8; // Wendungen je Teil eines Themas
  const PUNKTE = { teil: 10, wiederholung: 5, seance: 30, einheit: 50, feuer: 30, wochenende: 20, woche: 100, monat: 200 };

  /* ---------- Speicher (nur lokal) ---------- */
  const leer = () => ({ paar: PAARE[0], de: false, serie: { tage: {}, wochen: [], feuer: [], wochenende: [], abzeichen: [] }, sprachen: {} });
  function laden() {
    let s;
    try { s = JSON.parse(localStorage.getItem(SPEICHER) || "null"); } catch (e) { s = null; }
    if (!s) {
      s = leer();
      try { // Umzug aus „Mon français“: alter Stand wird zur Sprache fr-de, die Serie wird gemeinsam
        const alt = ALT ? JSON.parse(localStorage.getItem(ALT) || "null") : null;
        if (alt) {
          const sp = alt.spiel || {};
          s.de = !!alt.de;
          s.serie = { tage: sp.tage || {}, wochen: sp.wochen || [], feuer: sp.feuer || [], wochenende: sp.wochenende || [], abzeichen: sp.abzeichen || [] };
          s.sprachen["fr-de"] = { teile: alt.teile || {}, karten: alt.karten || {}, tag: alt.tag || null, gruppen: alt.gruppen || {},
            spiel: { punkte: sp.punkte || 0, titel: sp.titel || 0, seances: sp.seances || 0 } };
        }
      } catch (e) { /* kein alter Stand */ }
    }
    if (!PAKETE[s.paar]) s.paar = PAARE[0];
    s.tempo = s.tempo || {};   // je Sprache: true = normales Tempo trotz langsamer Voreinstellung (Türkisch 0,7×)
    return s;
  }
  function speichern() {
    try { localStorage.setItem(SPEICHER, JSON.stringify(stand)); } catch (e) { /* ohne Speicher geht es trotzdem */ }
  }
  const stand = laden();
  function sprachStand(paar) {
    if (!stand.sprachen[paar]) stand.sprachen[paar] = { teile: {}, karten: {}, tag: null, gruppen: {}, spiel: { punkte: 0, titel: 0, seances: 0 } };
    return stand.sprachen[paar];
  }

  /* ---------- Sprachpaar ---------- */
  let D, U, SP, S, WENDUNG, REIHENFOLGE, A, PENSUM, INTERVALLE;
  // Platzhalter {name} füllen; Texte sind String oder [Ziel, Hilfe]
  const f = (t, v) => String(t).replace(/\{(\w+)\}/g, (_, k) => (v && k in v ? v[k] : `{${k}}`));
  const uf = (key, v) => frde(f(U[key][0], v), f(U[key][1], v));
  const ufp = (key, v) => frde(f(U[key][0], v), f(U[key][1], v), "p");
  function setzeSprache(paar, start = true) {
    D = PAKETE[paar]; U = D.ui; SP = D.spiel; S = sprachStand(paar); A = D.aussprache;
    PENSUM = D.pensum; INTERVALLE = D.intervalle;
    WENDUNG = Object.fromEntries(D.wendungen.map((w) => [w.id, w]));
    REIHENFOLGE = Object.fromEntries(D.wendungen.map((w, i) => [w.id, i]));
    stand.paar = paar; speichern();
    document.documentElement.lang = D.lang;
    // Sprachfarben als Regeln für hell und dunkel (nicht als feste Inline-Werte: die überschrieben den Dunkelmodus, Kontrast 1,3–2,8 : 1)
    const T = D.theme, Td = T.dunkel || T;
    let st = document.getElementById("sprachfarben");
    if (!st) { st = document.createElement("style"); st.id = "sprachfarben"; document.head.append(st); }
    const hell = `--blau:${T.blau};--rot:${T.rot};--rot-text:${T.rot_text || "#ffffff"};--blau-text:${T.blau_text || "#ffffff"}`;
    const dunkel = `--blau:${Td.blau};--rot:${Td.rot};--rot-text:${Td.rot_text || "#0f1522"};--blau-text:${Td.blau_text || "#0f1522"}`;
    st.textContent = `:root{${hell}} @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){${dunkel}}} :root[data-theme="dark"]{${dunkel}}`;
    document.title = `${U.app} · ${D.name}`;
    const n = document.querySelectorAll(".niveau button");
    n[0].textContent = D.kurz; n[1].textContent = `+ ${D.hilfe_kurz}`;   // kurz, damit zwei Sprachreihen und der Schalter auf ein Handy passen
    tempoKnopf.hidden = !D.tempo; tempoAnzeige();
    document.querySelectorAll(".sprachen button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.paar === paar)));
    if (start) { lage = null; seance = null; startseite(); }
  }
  // Tempo: Sprachen mit langsamer Voreinstellung (D.tempo, z. B. Türkisch 0,7×) bekommen einen Schalter 🐢 0,7× / 1× (Mr. Alex, 17.10.)
  const tempoAktuell = () => (D.tempo && !stand.tempo[stand.paar] ? D.tempo : 1);
  const tempoKnopf = el("button", { type: "button", class: "tempo", hidden: true, title: "Tempo", onclick: () => { stand.tempo[stand.paar] = !stand.tempo[stand.paar]; speichern(); tempoAnzeige(); } });
  function tempoAnzeige() { const t = tempoAktuell(); tempoKnopf.textContent = t < 1 ? `🐢 ${String(t).replace(".", ",")}×` : "🔊 1×"; tempoKnopf.setAttribute("aria-pressed", String(t < 1)); }
  // rechte Spalte der Leiste: Hilfe-Schalter oben, Tempo darunter (passt zu den zwei Sprachreihen)
  const rechts = el("div", { class: "rechts" });
  const niveauEl = document.querySelector(".niveau");
  niveauEl.replaceWith(rechts); rechts.append(niveauEl, tempoKnopf);
  const sprachLeiste = document.querySelector(".sprachen");
  PAARE.forEach((p) => sprachLeiste.append(el("button", { type: "button", "data-paar": p, "aria-pressed": "false", title: PAKETE[p].name,
    onclick: () => { if (p !== stand.paar) setzeSprache(p); } }, PAKETE[p].flagge + " " + PAKETE[p].kurz)));
  if (PAARE.length < 2) sprachLeiste.classList.add("eine");

  /* ---------- Ziel / Ziel + Hilfe ---------- */
  let ansicht = null;  // aktuelle Seite – wird beim Umschalten neu gezeichnet
  let leise = false;   // beim Neuzeichnen nichts abspielen
  function setzeDe(an) {
    stand.de = an; speichern();
    document.querySelectorAll(".niveau button").forEach((b) => b.setAttribute("aria-pressed", String((b.dataset.de === "1") === an)));
    if (ansicht) { leise = true; try { ansicht(); } finally { leise = false; } }
  }
  document.querySelectorAll(".niveau button").forEach((b) => b.addEventListener("click", () => setzeDe(b.dataset.de === "1")));
  // Text in der Zielsprache mit Hilfe: antippen zeigt die Hilfssprache darunter; bei „+ DE“ immer sichtbar
  function frde(fr, de, tag = "span") {
    if (!de) return el(tag, { lang: D.lang }, fr);
    const hilfe = el("span", { class: "frde-de", lang: D.lang_hilfe, hidden: !stand.de }, de);
    return el(tag, { class: "frde", lang: D.lang, role: "button", tabindex: "0", title: U.hilfe_zeigen,
      onclick: () => { hilfe.hidden = !hilfe.hidden; },
      onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hilfe.hidden = !hilfe.hidden; } } }, fr, hilfe);
  }
  const ansage = (fr, de) => el("div", { class: "ansage" }, frde(fr, de, "p"));
  const ansageU = (key, v) => el("div", { class: "ansage" }, ufp(key, v));

  /* ---------- Lob (Mr. Alex' Stimme, solange keine Datei da ist: Stimme des Geräts) ---------- */
  const verlauf = [];
  function waehleRuf(art) {
    const liste = (D.lob || {})[art] || [];
    if (!liste.length) return null;
    const gleicheArt = verlauf.filter((v) => v.art === art).slice(-10).map((v) => v.r);
    const nahGruppen = new Set(verlauf.slice(-3).flatMap((v) => v.r.gruppe || []));
    const frisch = (r) => !gleicheArt.includes(r);
    const andereGruppe = (r) => !(r.gruppe || []).some((g) => nahGruppen.has(g));
    const pool = [liste.filter((r) => frisch(r) && andereGruppe(r)), liste.filter(frisch),
      liste.filter((r) => r !== (verlauf[verlauf.length - 1] || {}).r), liste].find((p) => p.length);
    const r = pool[Math.floor(Math.random() * pool.length)];
    verlauf.push({ art, r }); if (verlauf.length > 40) verlauf.shift();
    return r;
  }
  let vorLob = null, richtigSerie = 0, letzterRuf = null;
  const tonLob = (r) => r.audio || { text: r.text };
  function ruf(art) {
    const r = waehleRuf(art);
    letzterRuf = r || null;
    if (!r) return "";
    if (!leise) {
      const t = tonLob(r);
      vorLob = t;
      setTimeout(() => { if (vorLob === t) { vorLob = null; spiele([t]); } }, 0);
    }
    return r.text;
  }
  function lob(stark) {
    richtigSerie++;
    return ruf((stark || richtigSerie % 5 === 0) && D.lob.stark ? "stark" : "lob");
  }
  // Lob als Text mit Übersetzung in der Hilfssprache (immer sichtbar, auch ohne „+ DE“)
  const lobDe = () => (letzterRuf && letzterRuf.de) || "";
  function lobZeile(text, tag = "span", de = lobDe()) {
    return el(tag, { class: "lob-zeile" }, el("span", { lang: D.lang }, text), de && el("span", { class: "lob-de", lang: D.lang_hilfe }, de));
  }

  /* ---------- Audio ---------- */
  let lauf = 0, aktuell = null;
  function stopp() {
    lauf++;
    if (aktuell) { aktuell.pause(); aktuell = null; }
    if (window.speechSynthesis) speechSynthesis.cancel();
  }
  // Notlösung: Stimme des Geräts in der Zielsprache, solange die Audiodatei fehlt
  function geraeteStimme() {
    const alle = (window.speechSynthesis && speechSynthesis.getVoices()) || [];
    const genau = alle.filter((v) => v.lang.replace("_", "-").toLowerCase() === D.sprachausgabe.toLowerCase());
    const kandidaten = genau.length ? genau : alle.filter((v) => v.lang.toLowerCase().startsWith(D.lang));
    return kandidaten.find((v) => /male|thomas|daniel|jorge|diego|luca|paolo|markus|stefan/i.test(v.name)) || kandidaten[0] || null;
  }
  function sprich(text) {
    return new Promise((fertig) => {
      if (!window.speechSynthesis) return fertig(0);
      const u = new SpeechSynthesisUtterance(text);
      u.lang = D.sprachausgabe; u.rate = 0.9;
      const v = geraeteStimme();
      if (v) u.voice = v;
      const start = Date.now();
      let erledigt = false;
      const ende = () => { if (erledigt) return; erledigt = true; clearTimeout(notbremse); setTimeout(() => fertig((Date.now() - start) / 1000), 350); };
      const notbremse = setTimeout(ende, 2500 + text.split(/\s+/).length * 700);
      u.onend = ende; u.onerror = ende;
      speechSynthesis.speak(u);
    });
  }
  // Einträge: Dateipfad (String), { src, rate } (langsamer) oder { text } für die Geräte-Stimme
  function spiele(dateien) {
    if (leise) return Promise.resolve(null);
    if (vorLob) { dateien = [vorLob, ...dateien]; vorLob = null; }
    stopp();
    const meinLauf = lauf;
    let gesamt = 0;
    return dateien.filter(Boolean).reduce((kette, datei) => kette.then(() => new Promise((fertig) => {
      if (meinLauf !== lauf) return fertig();
      if (typeof datei === "object" && !datei.src) return sprich(datei.text).then((d) => { gesamt += d; fertig(); });
      const a = new Audio(datei.src || datei);
      a.playbackRate = datei.rate || tempoAktuell();
      a.preservesPitch = true;
      aktuell = a;
      a.onended = () => { gesamt += (a.duration || 0) / (a.playbackRate || 1); setTimeout(fertig, 350); };
      a.onerror = fertig;
      a.play().catch(fertig);
    })), Promise.resolve()).then(() => (meinLauf === lauf ? gesamt : null));
  }
  const ton = (o) => o.audio || { text: o.fr.replace(/[–—]/g, ",") };

  /* ---------- Icon « Muscu des mots »: Gewichtheber, Bücher als Gewichte (Vorlage: School-App Word Gym) ----------
     gehoben = Pensum fertig (Hantel oben); heben = einmal hochstemmen (SMIL, Start über svg.heben()). Farben aus den CSS-Variablen der Sprache. */
  function gymIcon(gehoben, heben, groesse) {
    const y = gehoben ? 16 : 34, y0 = heben ? 46 : y;
    const arme = (h) => `M60 66 L40 ${h} M60 66 L80 ${h}`;
    const buecher = (x) => `<g transform="translate(${x} 0)">
      <rect x="2" y="-13" width="26" height="8" rx="1.5" class="b1"/><rect x="4" y="-4" width="22" height="8" rx="1.5" class="b2"/><rect x="1" y="5" width="28" height="8" rx="1.5" class="b3"/></g>`;
    const anim = (werte) => (heben ? `begin="indefinite" dur="1.4s" fill="freeze" values="${werte}" keyTimes="0; .3; 1" calcMode="spline" keySplines=".4 0 .2 1; .4 0 .2 1"` : "");
    const d = document.createElement("div");
    d.innerHTML = `<svg class="gym-icon" viewBox="0 0 120 100" width="${groesse || 96}" height="${Math.round((groesse || 96) * 0.83)}" aria-hidden="true">
      <path class="arme" d="${arme(y0)}">${heben ? `<animate attributeName="d" ${anim(`${arme(46)}; ${arme(46)}; ${arme(16)}`)}/>` : ""}</path>
      <circle class="kopf" cx="60" cy="52" r="8.5"/><path class="figur" d="M60 62 V78 M60 78 L49 96 M60 78 L71 96"/>
      <g class="hantel" transform="translate(0 ${y0})">${heben ? `<animateTransform attributeName="transform" type="translate" ${anim("0 46; 0 46; 0 16")}/>` : ""}
        <line class="stange" x1="22" y1="0" x2="98" y2="0"/><circle class="stange-f" cx="30" cy="0" r="5.5"/><circle class="stange-f" cx="90" cy="0" r="5.5"/>
        ${buecher(0)}${buecher(90)}<circle class="hand" cx="40" cy="0" r="5"/><circle class="hand" cx="80" cy="0" r="5"/></g></svg>`;
    const svg = d.firstElementChild;
    if (heben) svg.heben = () => svg.querySelectorAll("animate, animateTransform").forEach((a) => a.beginElement && a.beginElement());
    return svg;
  }

  /* ---------- Hilfen ---------- */
  function el(tag, attrs, ...kinder) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === "class") e.className = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) e.setAttribute(k, v === true ? "" : v);
    }
    for (const k of kinder.flat()) if (k != null && k !== false) e.append(k.nodeType ? k : document.createTextNode(k));
    return e;
  }
  function zeige(...inhalt) { stopp(); app.replaceChildren(...inhalt.filter(Boolean)); if (!leise) window.scrollTo(0, 0); }
  function mischen(liste) {
    const a = liste.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }
  const thema = (id) => D.themen.find((t) => t.id === id);
  const knopf = (text, fn, art) => el("button", { class: "knopf" + (art ? " " + art : ""), onclick: fn }, text);
  const weiterKnopf = (fn) => knopf(U.suivant, fn || naechstes, "haupt weiter");
  const karte = (zaehlerText, ...inhalt) =>
    el("section", { class: "satzkarte" }, zaehlerText && el("p", { class: "zaehler" }, zaehlerText), ...inhalt);
  const registerSchild = (w) => w.register === "vous" && el("span", { class: "register", title: U.poli_titel }, U.poli);
  const notiz = (w) => w.notiz && el("p", { class: "notiz", lang: D.lang_hilfe }, "💡 ", w.notiz);
  // Interlinear-Glosse (Türkisch): "Wort·PL·AKK … | Wort·PL·AKK …" – je Wort die türkische Zerlegung über dem deutschen Etikett
  function glosse(g, klasse = "gloss", morphem = []) {
    if (!g) return null;
    const [tr, de] = g.split("|").map((x) => x.trim().split(/\s+/));
    if (!de || tr.length !== de.length) return el("p", { class: klasse + " gloss-flach", lang: D.lang }, g.replace("|", " – "));
    const trifft = (label) => morphem.some((m) => label.split(/[·.,;:!?»«]/).includes(m));
    return el("p", { class: klasse, lang: D.lang }, tr.map((t, i) => el("span", { class: "gl" + (trifft(de[i]) ? " treffer" : "") }, el("span", { class: "gl-tr" }, t), el("span", { class: "gl-de", lang: D.lang_hilfe }, de[i]))));
  }
  // Lücke im Satz: art "voll" | "luecke" | "buchstabe"
  function lueckenSatz(s, art) {
    const w = s.luecke, i = w ? s.fr.indexOf(w) : -1;
    if (i < 0) return [s.fr];
    const mitte = art === "voll" ? el("strong", { class: "ziel" }, w)
      : el("span", { class: "luecke" + (art === "buchstabe" ? " mit-buchstaben" : ""), "aria-label": U.trou },
        art === "buchstabe" ? w.replace(/\S+/g, (x) => x[0] + x.slice(1).replace(/./g, "_")) : w.replace(/\S/g, "_"));
    return [s.fr.slice(0, i), mitte, s.fr.slice(i + w.length)];
  }

  /* ---------- Sprechzeit: „Weiter“ erst nach Hören + Nachsprechen, „Lösung“ erst nach Denkzeit ---------- */
  const freiSchluessel = () => (lage ? lage.teil + ":" + lage.pos : "s:" + seancePos);
  function sperre(k) {
    const menge = lage ? (lage.frei = lage.frei || new Set()) : seanceFrei;
    if (menge.has(freiSchluessel())) return k;
    k.disabled = true; k.classList.add("wartet");
    return k;
  }
  function gibFrei(k, sek, merken = true) {
    if (!k.disabled || k.dataset.frei) return;
    k.dataset.frei = "1";
    k.style.setProperty("--warte", sek.toFixed(1) + "s");
    k.classList.add("laeuft");
    const menge = lage ? lage.frei : seanceFrei, schluessel = freiSchluessel();
    setTimeout(() => { k.disabled = false; k.classList.remove("wartet", "laeuft"); if (merken && menge) menge.add(schluessel); }, sek * 1000);
  }
  // Sprechzeit 60 % und Denkzeit 50 % der ersten Fassung (Mr. Alex, 13.10.: die Sperren waren zu lang)
  const sprechDauer = (d, min = 1.8) => Math.max(min, d * 0.85 + 0.6);
  const denkzeit = (text) => Math.min(4, Math.max(1.5, 1 + String(text).split(/\s+/).length * 0.175));
  const wennFrei = (k, fn) => () => { if (!k.disabled) fn(); };
  const tipp = (key, fn) => el("button", { class: "knopf leise tipp", title: U[key][1], onclick: (e) => { if (lage) lage.hilfe = true; fn(e); } }, "💡 " + U[key][0]);
  function jetztDu(text) {
    return el("div", { class: "jetztdu", hidden: true, role: "status" }, text || U.jetzt_du, el("span", { class: "balken", "aria-hidden": "true" }));
  }
  function nachsprechen(balken, tonListe) {
    balken.hidden = true;
    return spiele([].concat(tonListe)).then((d) => {
      if (d === null) return;
      balken.hidden = false; balken.classList.remove("laeuft"); void balken.offsetWidth;
      balken.style.setProperty("--dauer", sprechDauer(d).toFixed(1) + "s");
      balken.classList.add("laeuft");
      return sprechDauer(d);
    });
  }

  /* ---------- Startseite ---------- */
  let lage = null; // Thema: { thema, gruppe, titel, teile, teil, pos, frei, start, hilfe, reihe }
  let seance = null; // laufende Séance: { schlange: [ids], wieder: Set }
  let seancePos = 0;
  const seanceFrei = new Set();

  function startseite() {
    lage = null; seance = null; ansicht = startseite;
    const plan = tagesplan();
    const gesamt = plan.neu.length + plan.wdh.length, fertig = plan.fertig.length;
    const punkte = [...plan.wdh.map((id) => ({ id, wdh: true })), ...plan.neu.map((id) => ({ id }))];
    const karten = Object.values(S.karten);
    zeige(
      el("header", { class: "gruss" },
        el("h1", { lang: D.lang }, gruss()),
        ufp("motto")),
      // Startkarte « Muscu des mots » (Word Gym): Gewichtheber mit Büchern als Gewichten, hebt die Hantel, wenn das Pensum fertig ist
      el("section", { class: "gym-karte" + (plan.geschafft ? " fertig" : "") },
        gymIcon(plan.geschafft, false, 92),
        el("div", { class: "gym-text" },
          el("h2", { lang: D.lang }, U.seance_titel),
          el("p", { class: "unter", lang: D.lang }, gesamt ? f(U.seance_stand, { neu: plan.neu.length, wdh: plan.wdh.length, fertig, gesamt }) : U.seance_leer),
          gesamt > 0 && el("span", { class: "gym-punkte", "aria-hidden": "true" }, punkte.map((p) =>
            el("span", { class: (p.wdh ? "wdh" : "") + (plan.fertig.includes(p.id) ? " ok" : "") })))),
        el("div", { class: "gym-knoepfe" }, knopf(plan.geschafft ? U.seance_fertig : U.seance, starteSeance, plan.geschafft ? "" : "haupt"))),
      el("h2", {}, uf("themen")),
      el("nav", { class: "kacheln themen", "aria-label": U.themen[0] },
        D.themen.map((t) => {
          const gruppen = gruppenVon(t), ok = gruppen.filter((g, i) => gruppeFertig(t.id, i)).length;
          return el("button", { class: "kachel" + (ok === gruppen.length ? " erledigt" : ""), onclick: () => zeigeThema(t.id),
            "aria-label": `${t.name} – ${t.de}` },
            el("span", { class: "sym", "aria-hidden": "true" }, t.symbol),
            el("span", { class: "titel", lang: D.lang }, t.name),
            el("span", { class: "unter", lang: D.lang_hilfe }, t.de),
            el("span", { class: "zahl" }, `${t.wendungen.length} ${U.expressions} · ${ok} / ${gruppen.length} ${U.parties}`),
            ok === gruppen.length && el("span", { class: "haken", "aria-hidden": "true" }, "✓"));
        })),
      D.dialoge.length && el("h2", {}, frde(D.dialoge_titel[0], D.dialoge_titel[1])),
      D.dialoge.length && el("nav", { class: "kacheln themen", "aria-label": D.dialoge_titel[0] }, D.dialoge.map((d, i) => {
        const ok = dialogFertig(d.id);
        return el("button", { class: "kachel" + (ok ? " erledigt" : ""), onclick: () => starteDialog(d.id), "aria-label": `${d.titel}${ok ? " ✓" : ""}` },
          el("span", { class: "sym", "aria-hidden": "true" }, "💬"),
          el("span", { class: "titel", lang: D.lang }, `« ${d.titel} »`),
          el("span", { class: "unter", lang: D.lang }, d.ort),
          el("span", { class: "zahl" }, `${d.zeilen.length} ${U.repliques}`),
          ok && el("span", { class: "haken", "aria-hidden": "true" }, "✓"));
      })),
      D.grammatik && D.grammatik.length && el("h2", {}, uf("grammatik")),
      D.grammatik && D.grammatik.length && el("nav", { class: "kacheln themen", "aria-label": U.grammatik[0] }, D.grammatik.map(grammatikKachel)),
      el("h2", {}, uf("bonus")),
      el("nav", { class: "kacheln themen", "aria-label": U.bonus[0] },
        D.geschichte.length ? el("button", { class: "kachel", onclick: () => zeigeKapitel(kapitelFrei()), "aria-label": D.geschichte_info.titel },
          el("span", { class: "sym", "aria-hidden": "true" }, "📖"),
          el("span", { class: "titel", lang: D.lang }, D.geschichte_info.titel),
          el("span", { class: "unter", lang: D.lang }, D.geschichte_info.unter),
          el("span", { class: "zahl" }, f(U.kapitel_zahl, { frei: kapitelFrei(), alle: D.geschichte.length }))) : null,
        A.beide.length ? el("button", { class: "kachel" + (ausspracheFertig() ? " erledigt" : ""), onclick: starteAussprache, "aria-label": A.titel },
          el("span", { class: "sym", "aria-hidden": "true" }, A.symbol),
          el("span", { class: "titel", lang: D.lang }, A.titel),
          el("span", { class: "unter", lang: D.lang }, A.unter),
          el("span", { class: "zahl" }, `${ausspracheTeile().filter((_, i) => S.teile[`${A.id}|0|${i}`]).length} / ${ausspracheTeile().length} ${U.parties}`),
          ausspracheFertig() && el("span", { class: "haken", "aria-hidden": "true" }, "✓")) : null,
        !D.geschichte.length && !A.beide.length ? el("div", { class: "kachel bald" }, el("span", { class: "titel", lang: D.lang }, "…"), el("span", { class: "bald-schild" }, U.bald)) : null),
      el("p", { class: "klein" }, uf("stand", { n: karten.length, fest: karten.filter((k) => k.s >= 3).length, orte: orteFrei(), alle: SP.orte.length })));
    app.querySelector(".gruss").append(statusleiste());
  }
  function gruss() {
    const h = heute().getHours();
    return U.gruss[h < 11 ? 0 : h < 18 ? 1 : 2];
  }

  /* ---------- Tagesplan (Leitner, sanft) ----------
     Fällige Karten nach Fälligkeit (älteste zuerst), höchstens PENSUM.wiederholung. Was darüber liegt, wartet still auf morgen.
     Neue Wendungen in Themenreihenfolge, höchstens PENSUM.neu. Der Plan wird einmal am Tag gemacht und gespeichert. */
  function tagesplan() {
    const t = iso(heute());
    if (S.tag && S.tag.d === t) return S.tag;
    const faellig = Object.entries(S.karten).filter(([, k]) => k.f <= t)
      .sort((a, b) => (a[1].f < b[1].f ? -1 : a[1].f > b[1].f ? 1 : REIHENFOLGE[a[0]] - REIHENFOLGE[b[0]]))
      .map(([id]) => id).slice(0, PENSUM.wiederholung);
    const neu = D.wendungen.map((w) => w.id).filter((id) => !S.karten[id]).slice(0, PENSUM.neu);
    S.tag = { d: t, wdh: faellig, neu, fertig: [], geschafft: false };
    speichern();
    return S.tag;
  }
  function naechsteFaelligkeit(stufe) { return iso(plusTage(heute(), INTERVALLE[Math.min(stufe, INTERVALLE.length - 1)])); }

  /* ---------- Séance ---------- */
  function starteSeance() {
    const plan = tagesplan();
    lage = null;
    seance = { schlange: [...plan.wdh, ...plan.neu].filter((id) => !plan.fertig.includes(id)), wieder: new Set(), start: Date.now() };
    seancePos = 0;
    if (!seance.schlange.length) return seanceEnde(plan.geschafft);
    zeigeSeanceKarte();
  }
  function seanceKopf() {
    return el("header", { class: "kopf" }, knopf(U.zurueck_accueil, startseite, "leise"), el("h1", { lang: D.lang, class: "gym-titel" }, gymIcon(false, false, 40), U.seance_titel));
  }
  function seanceWeiter() {
    const plan = tagesplan();
    if (seancePos + 1 < seance.schlange.length) { seancePos++; return zeigeSeanceKarte(); }
    seanceEnde(plan.geschafft);
  }
  function zeigeSeanceKarte() {
    ansicht = zeigeSeanceKarte;
    const plan = tagesplan();
    const id = seance.schlange[seancePos], w = WENDUNG[id];
    const zaehler = `${seancePos + 1} / ${seance.schlange.length}`;
    if (plan.neu.includes(id) && !S.karten[id]) return neueKarte(w, zaehler);
    wiederholKarte(w, zaehler);
  }
  // Neue Wendung: hören, nachsprechen, dann ab in den Kasten (Stufe 0, morgen wieder)
  function neueKarte(w, zaehler) {
    const balken = jetztDu();
    const weiter = sperre(weiterKnopf(() => {
      S.karten[w.id] = { s: 0, f: naechsteFaelligkeit(0) };
      merkeFertig(w.id); seanceWeiter();
    }));
    const abspielen = () => nachsprechen(balken, [ton(w), ton(w.satz)]).then((sek) => { if (sek) gibFrei(weiter, sek); });
    tasten(abspielen, wennFrei(weiter, () => weiter.click()));
    zeige(seanceKopf(),
      ansageU("neu_ansage"),
      karte(`${zaehler} · ${U.nouvelle}`,
        el("div", { class: "vok" }, el("div", {},
          el("p", { class: "wendung", lang: D.lang }, w.fr, " ", registerSchild(w)), glosse(w.gloss, "gloss klein"),
          el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de), notiz(w))),
        el("div", { class: "spalten" },
          el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.exemple), el("p", { class: "satz fr", lang: D.lang }, lueckenSatz(w.satz, "voll")), glosse(w.satz.gloss)),
          el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.hilfe_sprache), el("p", { class: "satz de", lang: D.lang_hilfe }, w.satz.de))),
        balken,
        el("div", { class: "knopfreihe" }, knopf(U.encore_hoeren, abspielen), weiter)));
    abspielen();
  }
  // Wiederholung: Hilfssprache sehen, Zielsprache sagen, Lösung hören, selbst einschätzen
  function wiederholKarte(w, zaehler) {
    const k = S.karten[w.id];
    const balken = jetztDu();
    const frage = el("div", {}, el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de), el("p", { class: "satz de", lang: D.lang_hilfe }, w.satz.de));
    const antwort = el("div", { hidden: true },
      el("p", { class: "wendung", lang: D.lang }, w.fr, " ", registerSchild(w)), glosse(w.gloss, "gloss klein"),
      el("p", { class: "satz fr", lang: D.lang }, lueckenSatz(w.satz, "voll")), glosse(w.satz.gloss), notiz(w));
    const bewerten = el("div", { class: "bewerten", hidden: true },
      knopf(U.je_savais, () => bewerteKarte(w, true), "haupt"),
      knopf(U.encore, () => bewerteKarte(w, false), "encore"));
    const loesung = sperre(knopf(U.solution, () => {
      loesung.hidden = true; antwort.hidden = false; bewerten.hidden = false;
      nachsprechen(balken, [ton(w), ton(w.satz)]);
      tasten(() => nachsprechen(balken, [ton(w), ton(w.satz)]), null);
    }, "haupt"));
    gibFrei(loesung, denkzeit(w.satz.fr), false);
    tasten(null, wennFrei(loesung, () => loesung.click()));
    zeige(seanceKopf(),
      ansageU("wie_sagt_man"),
      karte(`${zaehler} · ${f(U.revision, { s: k.s })}`,
        el("div", { class: "vok" }, frage), antwort, balken,
        el("div", { class: "knopfreihe" }, loesung), bewerten));
  }
  function bewerteKarte(w, gewusst) {
    const k = S.karten[w.id];
    if (gewusst) {
      k.s = Math.min(k.s + 1, INTERVALLE.length); k.f = naechsteFaelligkeit(k.s);
      merkeFertig(w.id); lobToast(lob()); speichern(); seanceWeiter();
    } else {
      k.s = 0; k.f = naechsteFaelligkeit(0); speichern();
      if (!seance.wieder.has(w.id)) { seance.wieder.add(w.id); seance.schlange.push(w.id); }
      else merkeFertig(w.id);
      toast(U.pas_grave);
      seanceWeiter();
    }
  }
  function merkeFertig(id) {
    const plan = tagesplan();
    if (!plan.fertig.includes(id)) plan.fertig.push(id);
    speichern();
  }
  function seanceEnde() {
    const plan = tagesplan();
    const alles = [...plan.wdh, ...plan.neu].every((id) => plan.fertig.includes(id));
    const erstesMal = alles && !plan.geschafft;
    if (erstesMal) { plan.geschafft = true; speichern(); belohne(true, true); }
    // Lob und „À demain“ hintereinander (nicht gleichzeitig, sonst schneidet das eine das andere ab)
    const r = waehleRuf(alles ? "geschafft" : "stark"), text = r ? r.text : "", textDe = r ? r.de : "";
    const fini = erstesMal && SP.texte.fini;
    const icon = gymIcon(alles, erstesMal, 120);
    const zeichne = () => { zeige(seanceKopf(), el("section", { class: "geschafft gym-ende" },
      icon,
      el("h2", { lang: D.lang }, alles ? U.fini : U.pause),
      lobZeile(text, "p", textDe),
      ufp(alles ? "fini_text" : "pause_text"),
      el("div", { class: "knopfreihe" }, knopf(U.accueil, startseite, "haupt"), knopf(U.sammlung, sammlung))));
      if (icon.heben) setTimeout(icon.heben, 400); };
    ansicht = zeichne; seance = null; tasten(null, null);
    zeichne();
    setTimeout(() => spiele([r && tonLob(r), fini && (fini.audio || { text: fini.text })]), 300);
  }

  /* ---------- Themen: Teile und Lage ---------- */
  function gruppenVon(t) {
    const g = [];
    for (let i = 0; i < t.wendungen.length; i += GRUPPE) g.push(t.wendungen.slice(i, i + GRUPPE));
    return g;
  }
  const satzVon = (id) => Object.assign({ titel: WENDUNG[id].fr, notiz: WENDUNG[id].notiz }, WENDUNG[id].satz);
  function teileVon(ids) {
    const saetze = ids.map(satzVon);
    const t = [1, 2, 3].map((stufe) => ({ art: "lr", stufe, saetze, name: f(U.etape, { n: stufe }) }));
    const mitZeit = ids.filter((id) => WENDUNG[id].zeit);
    if (mitZeit.length) t.push({ art: "zeit", ids: mitZeit, name: U.zeitmaschine });
    t.push({ art: "abfrage", ids, name: U.trouve });
    return t;
  }
  const teilSchluessel = (i) => `${lage.thema}|${lage.gruppe}|${i}`;
  const istFertig = (i) => !!S.teile[teilSchluessel(i)];
  function teilFertig(i) { S.teile[teilSchluessel(i)] = true; speichern(); }
  const gruppeFertig = (tid, g) => teileVon(gruppenVon(thema(tid))[g]).every((_, i) => S.teile[`${tid}|${g}|${i}`]);
  const alleTeileFertig = () => lage.teile.every((_, i) => istFertig(i));

  function zeigeThema(tid) {
    const t = thema(tid);
    lage = null; seance = null; ansicht = () => zeigeThema(tid);
    const gruppen = gruppenVon(t);
    zeige(
      el("header", { class: "kopf" }, knopf(U.zurueck_accueil, startseite, "leise"), el("h1", { lang: D.lang }, `${t.symbol} ${t.name}`)),
      ansageU("thema_ansage"),
      el("nav", { class: "kacheln gruppen" }, gruppen.map((ids, i) => {
        const ok = gruppeFertig(tid, i), name = f(U.partie, { n: i + 1 });
        return el("button", { class: "kachel" + (ok ? " erledigt" : ""), onclick: () => starteGruppe(tid, i), "aria-label": `${name}${ok ? " ✓" : ""}` },
          el("span", { class: "nr" }, name),
          el("span", { class: "titel", lang: D.lang }, ids.map((id) => WENDUNG[id].fr).slice(0, 3).join(" · ") + (ids.length > 3 ? " …" : "")),
          el("span", { class: "zahl" }, `${ids.length} ${U.expressions}`),
          ok && el("span", { class: "haken", "aria-hidden": "true" }, "✓"));
      })),
      grammatikVon(tid) && el("h2", {}, U.grammatik_thema),
      grammatikVon(tid) && el("nav", { class: "kacheln themen" }, grammatikKachel(grammatikVon(tid))));
  }
  function starteGruppe(tid, g) {
    const t = thema(tid), ids = gruppenVon(t)[g];
    lage = { thema: tid, gruppe: g, titel: `${t.name} · ${f(U.partie, { n: g + 1 })}`, teile: teileVon(ids), teil: 0, pos: 0, zurueckZu: () => zeigeThema(tid) };
    zeigeTeil();
  }

  /* ---------- Dialoge mit Rollen ----------
     Ablauf: anhören → Zeilen nachsprechen (Stufe 1 und 3) → „Du bist A“ (die App spricht B, du sprichst in die Pause) → Rollentausch. */
  function dialogTeile(d) {
    const saetze = d.zeilen.map((z) => Object.assign({ titel: D.rollen[z.rolle] }, z));
    return [{ art: "dialog", name: U.dialog_hoeren, dialog: d, rolle: null },
      { art: "lr", stufe: 1, saetze, name: U.repeter + " ①" }, { art: "lr", stufe: 3, saetze, name: U.repeter + " ③" },
      { art: "dialog", name: f(U.tu_es, { rolle: D.rollen.A }), dialog: d, rolle: "A" }, { art: "dialog", name: f(U.tu_es, { rolle: D.rollen.B }), dialog: d, rolle: "B" }];
  }
  const dialogFertig = (id) => dialogTeile(D.dialoge.find((d) => d.id === id)).every((_, i) => S.teile[`dialog:${id}|0|${i}`]);
  function starteDialog(id) {
    const d = D.dialoge.find((x) => x.id === id);
    lage = { thema: "dialog:" + id, gruppe: 0, dialog: d, titel: `« ${d.titel} »`, teile: dialogTeile(d), teil: 0, pos: 0, zurueckZu: startseite };
    seance = null;
    zeigeTeil();
  }
  let dialogLauf = 0;
  const warte = (ms) => new Promise((ok) => setTimeout(ok, ms));
  function zeigeDialog(teil) {
    const meine = teil.rolle, zeilen = teil.dialog.zeilen, R = D.rollen;
    let versteckt = !!meine;
    const balken = jetztDu(U.jetzt_du_dialog);
    const box = el("div", { class: "rueckmeldung", hidden: true, role: "status" });
    const liste = el("ol", { class: "dialog" }, zeilen.map((z) => {
      const eigen = z.rolle === meine;
      return el("li", { class: "dz rolle-" + z.rolle + (eigen ? " meine" : "") },
        el("span", { class: "dz-rolle", "aria-label": U.role + " " + R[z.rolle] }, R[z.rolle]),
        el("div", {}, el("p", { class: "dz-en", lang: D.lang }, eigen && versteckt ? "…" : z.fr), el("p", { class: "dz-de klein", lang: D.lang_hilfe, hidden: !stand.de && !!meine }, z.de)));
    }));
    const zeigeMeine = () => { versteckt = false; zeilen.forEach((z, i) => { if (z.rolle === meine) liste.children[i].querySelector(".dz-en").textContent = z.fr; }); };
    const startKnopf = knopf(meine ? U.dialog_start : U.dialog_hoeren_knopf, starten, "haupt");
    const stoppKnopf = knopf(U.stop, () => { dialogLauf++; stopp(); fertig(false); });
    stoppKnopf.hidden = true;
    function fertig(ganz) {
      startKnopf.hidden = false; stoppKnopf.hidden = true; balken.hidden = true;
      [...liste.children].forEach((li) => li.classList.remove("spricht"));
      if (ganz) { gibFrei(weiter, 0.6); box.hidden = false; box.className = "rueckmeldung gut"; box.replaceChildren(lobZeile(lob()), " " + (meine ? U.dialog_ok_rolle : U.dialog_ok)); }
    }
    async function starten() {
      const meinLauf = ++dialogLauf;
      startKnopf.hidden = true; stoppKnopf.hidden = false; box.hidden = true;
      for (let i = 0; i < zeilen.length; i++) {
        if (meinLauf !== dialogLauf) return;
        const z = zeilen[i];
        [...liste.children].forEach((li, j) => li.classList.toggle("spricht", j === i));
        if (liste.children[i].scrollIntoView) liste.children[i].scrollIntoView({ block: "nearest", behavior: "smooth" });
        if (z.rolle === meine) { // Pause zum Sprechen, so lang wie die Zeile
          const dauer = Math.max(2.5, z.fr.split(/\s+/).length * 0.6 + 1.2);
          balken.hidden = false; balken.classList.remove("laeuft"); void balken.offsetWidth;
          balken.style.setProperty("--dauer", dauer.toFixed(1) + "s"); balken.classList.add("laeuft");
          await warte(dauer * 1000);
          balken.hidden = true;
        } else if ((await spiele([ton(z)])) === null) return;
      }
      if (meinLauf === dialogLauf) fertig(true);
    }
    const weiter = sperre(weiterKnopf());
    tasten(() => { if (!startKnopf.hidden) starten(); }, wennFrei(weiter, naechstes));
    zeige(kopf(),
      meine ? ansageU("dialog_ansage_rolle", { ich: R[meine], andere: R[meine === "A" ? "B" : "A"] })
        : ansageU("dialog_ansage", { titel: teil.dialog.titel, ort: teil.dialog.ort }),
      karte(null, liste, balken,
        meine && el("div", { class: "knopfreihe" }, tipp("dialog_tipp", (e) => { e.currentTarget.hidden = true; zeigeMeine(); })),
        el("div", { class: "knopfreihe" }, startKnopf, stoppKnopf), box,
        el("div", { class: "knopfreihe" }, weiter)));
  }

  /* ---------- Geschichte ----------
     Kapitel 1 ist frei, jede perfekte Woche schaltet das nächste frei. Absätze hören (alle oder einzeln), antippen = Hilfssprache. */
  const kapitelFrei = () => Math.min(D.geschichte.length, 1 + stand.serie.wochen.length);
  const fett = (text) => text.split(/(\*\*[^*]+\*\*)/).map((t) => (t.startsWith("**") ? el("strong", { class: "ziel" }, t.slice(2, -2)) : t));
  const tonAbsatz = (a) => a.audio || { text: a.fr.replace(/\*\*/g, "") };
  function zeigeKapitel(nr) {
    const k = D.geschichte[nr - 1];
    lage = null; seance = null; ansicht = () => zeigeKapitel(nr);
    if (!k || nr > kapitelFrei()) return sammlung();
    const absaetze = k.absaetze.map((a) => {
      const de = el("p", { class: "absatz-de", lang: D.lang_hilfe, hidden: !stand.de }, a.de);
      return el("div", { class: "absatz", role: "button", tabindex: "0", onclick: () => { de.hidden = !de.hidden; },
        onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); de.hidden = !de.hidden; } } },
        el("p", { class: "absatz-fr", lang: D.lang }, fett(a.fr),
          el("button", { class: "knopf leise klein-knopf", "aria-label": U.hoeren, onclick: (e) => { e.stopPropagation(); vorlesen([a]); } }, "🔊")), de);
    });
    async function vorlesen(liste) {
      for (const a of liste) {
        absaetze.forEach((x, i) => x.classList.toggle("spricht", k.absaetze[i] === a));
        if ((await spiele([tonAbsatz(a)])) === null) break;
      }
      absaetze.forEach((x) => x.classList.remove("spricht"));
    }
    const kapitelLeiste = el("div", { class: "knopfreihe" }, D.geschichte.map((x) =>
      el("button", { class: "sprung" + (x.nr === nr ? " jetzt" : "") + (x.nr <= kapitelFrei() ? "" : " zu"), disabled: x.nr > kapitelFrei(),
        onclick: () => zeigeKapitel(x.nr), "aria-current": x.nr === nr ? "page" : false }, x.nr <= kapitelFrei() ? `${x.nr}` : `${x.nr} 🔒`)));
    tasten(() => vorlesen(k.absaetze), nr < kapitelFrei() ? () => zeigeKapitel(nr + 1) : null);
    zeige(
      el("header", { class: "kopf" }, knopf(U.zurueck_accueil, startseite, "leise"), el("h1", { lang: D.lang }, `📖 ${f(U.chapitre, { n: k.nr })} – ${k.titel}`), kapitelLeiste),
      ansageU("kapitel_ansage"),
      el("section", { class: "satzkarte geschichte" },
        el("div", { class: "knopfreihe" }, knopf(U.kapitel_alles, () => vorlesen(k.absaetze), "haupt"), knopf(U.stop, stopp)),
        el("div", { class: "absaetze" }, absaetze),
        el("div", { class: "knopfreihe" },
          nr < kapitelFrei() ? knopf(U.kapitel_weiter, () => zeigeKapitel(nr + 1), "haupt")
            : el("p", { class: "klein" }, uf(nr < D.geschichte.length ? "kapitel_naechste" : "kapitel_ende")),
          knopf(U.sammlung, sammlung))));
  }

  /* ---------- Aussprache: Laute hören, Minimalpaare unterscheiden, beide Laute in einem Wort ---------- */
  const KLANG = () => A.info;
  function ausspracheTeile() {
    const t = A.reihe.map((k) => ({ art: "nasal_wort", name: `${A.info[k][0]} ${k}`, klang: k, woerter: A.klaenge[k] }));
    A.paare_gruppen.forEach(([g, name]) => t.push({ art: "nasal_paar", name: "🎯 " + name, paare: A.paare.filter((p) => p.gruppe === g) }));
    if (A.beide.length) t.push({ art: "nasal_beide", name: A.beide_name, woerter: A.beide });
    return t;
  }
  const ausspracheFertig = () => ausspracheTeile().every((_, i) => S.teile[`${A.id}|0|${i}`]);
  function starteAussprache() {
    lage = { thema: A.id, gruppe: 0, aussprache: true, titel: A.titel, teile: ausspracheTeile(), teil: 0, pos: 0, zurueckZu: startseite };
    seance = null;
    zeigeTeil();
  }
  const tonLangsam = (w) => (w.audio ? { src: w.audio, rate: 0.7 } : { text: w.wort });
  const tonWort = (w) => w.audio || { text: w.wort };
  const klangSchild = (k) => el("span", { class: "klang-schild klang-" + k }, KLANG()[k][0], " ", el("small", {}, KLANG()[k][1]));
  // Markup comm{an|en}ç{on|on}s → Buchstaben, Laute farbig
  function markiert(markup) {
    const teile = [];
    markup.split(/(\{[a-z]+\|[^}]*\})/).forEach((t) => {
      const m = t.match(/^\{([a-z]+)\|([^}]*)\}$/);
      teile.push(m ? el("span", { class: "nasal klang-" + m[1], title: KLANG()[m[1]][0] }, m[2]) : t);
    });
    return teile;
  }
  function zeigeNasalWort(teil) {
    const w = teil.woerter[lage.pos], beide = teil.art === "nasal_beide", T = A.texte, K = KLANG();
    const balken = jetztDu();
    const weiter = sperre(weiterKnopf());
    const hoeren = (liste) => nachsprechen(balken, liste).then((sek) => { if (sek) gibFrei(weiter, sek); });
    const abspielen = () => hoeren([tonLangsam(w), tonWort(w)]);
    tasten(abspielen, wennFrei(weiter, naechstes));
    zeige(kopf(),
      beide ? ansage(T.beide[0], T.beide[1])
        : ansage(f(T.klang[0], { laut: K[teil.klang][0], tipp: K[teil.klang][2] }), f(T.klang[1], { laut: K[teil.klang][0], tipp: K[teil.klang][3] })),
      karte(f(U.mot, { n: lage.pos + 1, alle: teil.woerter.length }),
        el("div", { class: "vok" }, el("div", {},
          el("p", { class: "nasal-wort", lang: D.lang }, beide ? markiert(w.markup) : w.wort),
          el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de),
          el("p", { class: "klang-zeile" }, (beide ? w.klaenge : [teil.klang]).map(klangSchild)))),
        balken,
        el("div", { class: "knopfreihe" }, knopf(U.lentement, () => hoeren([tonLangsam(w)])), knopf(U.normal, () => hoeren([tonWort(w)])), weiter)));
    abspielen();
  }
  function zeigeNasalPaar(teil) {
    if (!lage.reihe) lage.reihe = mischen(teil.paare).map((p) => ({ p, ziel: Math.random() < 0.5 ? "a" : "b", links: Math.random() < 0.5 }));
    const { p, ziel, links } = lage.reihe[lage.pos];
    const a = p, b = p.b, gesucht = ziel === "a" ? a : b, T = A.texte, K = KLANG();
    let geloest = false;
    const box = el("div", { class: "rueckmeldung", hidden: true, role: "status" });
    const weiter = weiterKnopf(); weiter.disabled = true;
    const hoeren = () => spiele([tonWort(gesucht)]);
    const beideHoeren = () => spiele([tonWort(a), tonWort(b)]);
    const wahlKnopf = (w) => el("button", { class: "knopf wahl-knopf gross", lang: D.lang, onclick: (e) => {
      if (geloest) return;
      if (w === gesucht) {
        geloest = true; e.currentTarget.classList.add("richtig");
        box.hidden = false; box.className = "rueckmeldung gut"; box.replaceChildren(lobZeile(lob()), ` ${gesucht.wort} ${K[gesucht.klang][0]} – ${gesucht.de}`);
        weiter.disabled = false; tasten(beideHoeren, naechstes);
        beideHoeren();
      } else {
        e.currentTarget.disabled = true;
        box.hidden = false; box.className = "rueckmeldung hilfe";
        box.replaceChildren(frde(`${ruf("fehler")} ${f(T.hilfe[0], { a: `${K[a.klang][0]} ${K[a.klang][2]} · ${K[b.klang][0]} ${K[b.klang][2]}` })}`,
          f(T.hilfe[1], { a: `${K[a.klang][0]} ${K[a.klang][3]} · ${K[b.klang][0]} ${K[b.klang][3]}` })));
        hoeren();
      }
    } }, el("span", {}, w.wort), el("small", { class: "klang-" + w.klang }, K[w.klang][0]));
    const knoepfe = [wahlKnopf(a), wahlKnopf(b)];
    tasten(hoeren, null);
    zeige(kopf(),
      ansage(T.paar[0], T.paar[1]),
      karte(f(U.paire, { n: lage.pos + 1, alle: lage.reihe.length }),
        el("div", { class: "knopfreihe" }, knopf(U.hoeren, hoeren, "haupt")),
        el("div", { class: "wahl" }, links ? knoepfe : knoepfe.reverse()),
        box,
        el("div", { class: "knopfreihe" }, el("button", { class: "knopf leise tipp", title: T.beide_hoeren[1], onclick: () => { if (lage) lage.hilfe = true; beideHoeren(); } }, "💡 " + T.beide_hoeren[0]), weiter)));
    hoeren();
  }

  /* ---------- Dil bilgisi: eine Grammatik-Lektion pro Thema (Türkisch) ----------
     Regel + Beispiele (schon gehörte Sätze, Morphem in der Glosse hervorgehoben) → Form bilden (Formel, drei Antworten) → hören und entscheiden */
  const grammatikVon = (tid) => (D.grammatik || []).find((g) => g.thema === tid);
  function grammatikTeile(g) {
    return [{ art: "gram_regel", name: U.regel[0], g }, { art: "gram_chips", name: U.bilde[0], g, reihe: g.chips }, { art: "gram_hoeren", name: U.hoer[0], g, reihe: g.hoeren }];
  }
  const grammatikFertig = (g) => grammatikTeile(g).every((_, i) => S.teile[`gram:${g.id}|0|${i}`]);
  function grammatikKachel(g) {
    const t = thema(g.thema), ok = grammatikFertig(g), n = grammatikTeile(g).filter((_, i) => S.teile[`gram:${g.id}|0|${i}`]).length;
    return el("button", { class: "kachel" + (ok ? " erledigt" : ""), onclick: () => starteGrammatik(g.id), "aria-label": `${g.titel} – ${g.de}${ok ? " ✓" : ""}` },
      el("span", { class: "sym", "aria-hidden": "true" }, "📐"),
      el("span", { class: "titel", lang: D.lang }, g.titel),
      el("span", { class: "unter", lang: D.lang_hilfe }, `${g.de} · ${t.symbol} ${t.name}`),
      el("span", { class: "zahl" }, `${n} / ${grammatikTeile(g).length} ${U.parties}`),
      ok && el("span", { class: "haken", "aria-hidden": "true" }, "✓"));
  }
  function starteGrammatik(id) {
    const g = D.grammatik.find((x) => x.id === id);
    lage = { thema: "gram:" + id, gruppe: 0, grammatik: g, titel: `📐 ${g.titel}`, teile: grammatikTeile(g), teil: 0, pos: 0, zurueckZu: () => zeigeThema(g.thema) };
    seance = null;
    zeigeTeil();
  }
  const tonSatz = (q) => q.audio || { text: q.fr };
  function zeigeGramRegel(teil) {
    const g = teil.g;
    const weiter = weiterKnopf();
    const beispiele = g.beispiele.map((b, i) => {
      const abspielen = () => spiele([tonSatz(b)]);
      return el("div", { class: "gram-beispiel" },
        el("div", { class: "gram-satzzeile" }, el("button", { class: "knopf leise klein-knopf", onclick: abspielen, "aria-label": U.encore_hoeren }, "🔊"),
          el("p", { class: "satz fr", lang: D.lang }, b.fr)),
        glosse(b.gloss, "gloss", g.morphem),
        el("p", { class: "satz de klein", lang: D.lang_hilfe }, b.de),
        el("p", { class: "notiz", lang: D.lang_hilfe }, "💡 ", b.hinweis));
    });
    tasten(() => spiele(g.beispiele.map(tonSatz)), naechstes);
    zeige(kopf(),
      ansageU("grammatik_ansage"),
      el("section", { class: "satzkarte gram" },
        el("h2", {}, uf("regel")),
        el("div", { class: "gram-regel", lang: D.lang_hilfe }, g.regel.map((r) => el("p", {}, r)))),
      el("section", { class: "satzkarte gram" },
        el("h2", {}, uf("beispiele")), beispiele),
      g.kontrast.length ? el("section", { class: "satzkarte gram" },
        el("h2", {}, uf("kontrast")),
        el("div", { class: "gram-kontrast" }, g.kontrast.map((k) => el("div", { class: "kontrast" },
          el("span", { class: "k-a", lang: D.lang }, k.a), el("span", { class: "k-pfeil", "aria-hidden": "true" }, "≠"), el("span", { class: "k-b", lang: D.lang }, k.b),
          el("span", { class: "k-text", lang: D.lang_hilfe }, k.text))))) : null,
      el("div", { class: "knopfreihe" }, weiter));
  }
  function zeigeGramChips(teil) {
    const c = teil.reihe[lage.pos];
    const weiter = sperre(weiterKnopf());
    const meldung = el("p", { class: "gram-meldung", "aria-live": "polite" });
    const antworten = mischen(c.antworten).map((a) => el("button", { class: "knopf chip", lang: D.lang, onclick: (e) => {
      if (a === c.antworten[0]) {
        e.currentTarget.classList.add("richtig"); meldung.textContent = U.richtig; lob(false);
        antworten.forEach((k) => { k.disabled = true; });
        gibFrei(weiter, 0.4);
      } else { e.currentTarget.classList.add("falsch"); e.currentTarget.disabled = true; meldung.textContent = U.falsch; }
    } }, a));
    tasten(null, wennFrei(weiter, naechstes));
    zeige(kopf(),
      ansageU("bilde_ansage"),
      karte(`${f(U.phrase, { n: lage.pos + 1, alle: teil.reihe.length })}`,
        el("p", { class: "gram-formel", lang: D.lang }, c.formel.split("+").flatMap((t, i) => [i > 0 && el("span", { class: "plus" }, "+"), el("span", { class: i === 0 ? "stamm" : "morph" }, t.trim())]).filter(Boolean)),
        el("div", { class: "knopfreihe chips" }, antworten), meldung,
        el("div", { class: "knopfreihe" }, weiter)));
  }
  function zeigeGramHoeren(teil) {
    const h = teil.reihe[lage.pos], g = teil.g;
    const weiter = sperre(weiterKnopf());
    const meldung = el("p", { class: "gram-meldung", "aria-live": "polite" });
    const texte = h.saetze.map((q) => el("p", { class: "satz fr", lang: D.lang, hidden: true }, q.fr));
    const wahl = h.saetze.map((q, i) => el("button", { class: "knopf chip", onclick: (e) => {
      if (i === h.richtig) {
        e.currentTarget.classList.add("richtig"); meldung.textContent = U.richtig; lob(false);
        wahl.forEach((k) => { k.disabled = true; }); texte.forEach((t) => { t.hidden = false; });
        gibFrei(weiter, 0.4);
      } else { e.currentTarget.classList.add("falsch"); e.currentTarget.disabled = true; meldung.textContent = U.falsch; }
    } }, `${i + 1}`));
    const hoeren = h.saetze.map((q, i) => el("button", { class: "knopf", onclick: () => spiele([tonSatz(q)]) }, `🔊 ${f(U.satz_n, { n: i + 1 })}`));
    tasten(() => spiele(h.saetze.map(tonSatz)), wennFrei(weiter, naechstes));
    zeige(kopf(),
      ansage(U.hoer[0], g.hoeren_frage),
      karte(`${f(U.phrase, { n: lage.pos + 1, alle: teil.reihe.length })}`,
        el("div", { class: "knopfreihe" }, hoeren),
        el("div", { class: "gram-texte" }, texte),
        el("p", { class: "klein", lang: D.lang_hilfe }, g.hoeren_frage),
        el("div", { class: "knopfreihe chips" }, wahl), meldung,
        el("div", { class: "knopfreihe" }, weiter)));
    spiele(h.saetze.map(tonSatz));
  }

  function kopf() {
    return el("header", { class: "kopf" },
      knopf(lage.dialog || lage.aussprache || lage.grammatik ? U.zurueck_accueil : U.zurueck_thema, lage.zurueckZu, "leise"),
      el("h1", { lang: D.lang }, lage.titel),
      sprungleiste());
  }
  function sprungleiste() {
    const nochNichts = !lage.teile.some((_, i) => istFertig(i));
    const ZIFFERN = ["①", "②", "③"];
    const sprung = (i, text) => {
      const t = lage.teile[i], fertig = istFertig(i), jetzt = i === lage.teil && !lage.ende, start = nochNichts && i === 0;
      return el("button", { class: "sprung" + (jetzt ? " jetzt" : "") + (fertig ? " fertig" : "") + (start ? " start" : ""),
        "aria-current": jetzt ? "step" : false, title: t.name, "aria-label": `${t.name}${fertig ? " ✓" : ""}`, onclick: () => springe(i) }, text);
    };
    const eintraege = [];
    for (let i = 0; i < lage.teile.length;) {
      const t = lage.teile[i];
      if (t.art === "lr") {
        const gruppe = el("li", { class: "sprung-gruppe" }, el("span", { class: "sprung-label", lang: D.lang }, U.lr_label));
        while (i < lage.teile.length && lage.teile[i].art === "lr" && lage.teile[i].saetze === t.saetze) { gruppe.append(sprung(i, ZIFFERN[lage.teile[i].stufe - 1])); i++; }
        eintraege.push(gruppe);
      } else { eintraege.push(el("li", {}, sprung(i, t.name))); i++; }
    }
    return el("ol", { class: "schritte", "aria-label": U.parties_label }, eintraege);
  }
  function springe(i) { lage.teil = i; lage.pos = 0; lage.ende = false; lage.reihe = null; lage.hilfe = false; zeigeTeil(); }
  function zurueck() {
    if (lage.pos > 0) { lage.pos--; return zeigeTeil(); }
    if (lage.teil === 0) return;
    lage.teil--; lage.reihe = null; lage.hilfe = false;
    lage.pos = laenge(lage.teile[lage.teil]) - 1;
    zeigeTeil();
  }
  function navErgaenzen(zurueckFn) {
    if (!lage) return;
    const z = knopf(U.retour, zurueckFn || zurueck);
    z.classList.add("zurueck-knopf");
    if (!zurueckFn && lage.teil === 0 && lage.pos === 0) z.disabled = true;
    const w = app.querySelector("button.weiter");
    if (w && !w.closest("[hidden]")) w.before(z);
    else app.append(el("div", { class: "knopfreihe navleiste" }, z));
    const jetzt = app.querySelector(".sprung.jetzt");
    if (jetzt && jetzt.scrollIntoView && !leise) jetzt.scrollIntoView({ block: "nearest", inline: "center" });
  }
  function zeigeTeil() {
    ansicht = zeigeTeil;
    tasten(null, null);
    if (lage.startTeil !== lage.teil) { lage.startTeil = lage.teil; lage.start = Date.now(); }
    const teil = lage.teile[lage.teil];
    ({ lr: zeigeSatz, zeit: zeigeZeitmaschine, abfrage: zeigeAbfrage, dialog: zeigeDialog,
       nasal_wort: zeigeNasalWort, nasal_beide: zeigeNasalWort, nasal_paar: zeigeNasalPaar,
       gram_regel: zeigeGramRegel, gram_chips: zeigeGramChips, gram_hoeren: zeigeGramHoeren })[teil.art](teil);
    navErgaenzen();
  }
  const laenge = (teil) => (teil.art === "abfrage" && lage.reihe ? lage.reihe.length : teil.art === "dialog" || teil.art === "gram_regel" ? 1 : (teil.saetze || teil.woerter || teil.paare || teil.ids || teil.reihe).length);
  const SPRECH_MIN = { lr: 2, zeit: 3, nasal_wort: 1.5, nasal_beide: 2 }; // Sekunden pro Satz mindestens – schneller geht nicht ehrlich
  const zuSchnell = (teil) => SPRECH_MIN[teil.art] && lage.start && (Date.now() - lage.start) / 1000 < laenge(teil) * SPRECH_MIN[teil.art];
  function naechstes() {
    const teil = lage.teile[lage.teil];
    if (lage.pos + 1 < laenge(teil)) { lage.pos++; return zeigeTeil(); }
    if (zuSchnell(teil)) return zuSchnellSeite();
    const erstesMal = !istFertig(lage.teil);
    teilFertig(lage.teil);
    belohne(erstesMal, false);
    if (alleTeileFertig()) return gruppeGeschafft();
    if (lage.teil + 1 < lage.teile.length) return zwischenstand();
    fastGeschafft();
  }
  function zuSchnellSeite() {
    const nochmal = () => { lage.frei = null; lage.startTeil = null; springe(lage.teil); };
    tasten(null, nochmal);
    const zeichne = () => zeige(kopf(), el("section", { class: "geschafft" },
      el("h2", {}, U.trop_vite), ansageU("trop_vite_text"), knopf(U.encore_fois, nochmal, "haupt")));
    ansicht = zeichne; zeichne();
  }
  function zwischenstand() {
    const fertig = lage.teile[lage.teil], text = lob(true), textDe = lobDe();
    const weiter = () => { lage.teil++; lage.pos = 0; lage.reihe = null; lage.hilfe = false; zeigeTeil(); };
    const zeichne = () => {
      tasten(null, weiter);
      zeige(kopf(), el("section", { class: "geschafft" }, lobZeile(text, "h2", textDe), el("p", { lang: D.lang }, f(U.termine, { name: fertig.name })), weiterKnopf(weiter)));
      navErgaenzen(() => zeigeTeil());
    };
    ansicht = zeichne; zeichne();
  }
  function fastGeschafft() {
    lage.ende = true; tasten(null, null);
    const text = lob(true), textDe = lobDe();
    const offen = lage.teile.map((t, i) => [t, i]).filter(([, i]) => !istFertig(i));
    const zeichne = () => zeige(kopf(), el("section", { class: "geschafft" },
      lobZeile(text, "h2", textDe), ansageU("presque"),
      el("div", { class: "knopfreihe" }, offen.map(([t, i]) => knopf(t.name, () => { lage.ende = false; springe(i); }))),
      knopf(U.accueil, startseite)));
    ansicht = zeichne; zeichne();
  }
  function gruppeGeschafft() {
    const tid = lage.thema, g = lage.gruppe, titel = lage.titel, zurueckZu = lage.zurueckZu;
    const schluessel = `${tid}|${g}`;
    if (!S.gruppen[schluessel]) { S.gruppen[schluessel] = true; punkteDazu(PUNKTE.einheit); }
    const t = thema(tid), alle = !!t && gruppenVon(t).every((_, i) => gruppeFertig(tid, i));
    speichern();
    const text = lob(true), textDe = lobDe();
    lage = null; tasten(null, null);
    const zeichne = () => zeige(el("header", { class: "kopf" }, knopf(t ? U.zurueck_thema : U.zurueck_accueil, zurueckZu, "leise"), el("h1", { lang: D.lang }, titel)),
      el("section", { class: "geschafft" },
        el("h2", { lang: D.lang }, f(U.termine, { name: titel })),
        lobZeile(text, "p", textDe),
        alle && el("p", { class: "ansage", lang: D.lang }, f(U.thema_fertig, { name: t.name })),
        el("div", { class: "knopfreihe" }, t ? knopf(U.autres_parties, zurueckZu, "haupt") : knopf(U.accueil, startseite, "haupt"), t && knopf(U.accueil, startseite))));
    ansicht = zeichne; zeichne();
  }

  /* ---------- Hören und nachsprechen (3 Stufen) ----------
     1: Ziel und Hilfe sichtbar, hören und nachsprechen · 2: Ziel mit Lücke – ganzen Satz sagen, dann Lösung · 3: nur Hilfe – ganzen Satz sagen, dann Lösung */
  function zeigeSatz(teil) {
    const s = teil.saetze[lage.pos], stufe = teil.stufe;
    let geloest = stufe === 1;
    const balken = jetztDu();
    const fr = el("p", { class: "satz fr", lang: D.lang }, lueckenSatz(s, stufe === 1 ? "voll" : "luecke"));
    if (stufe === 3) fr.replaceChildren(el("span", { class: "profi" }, U.dis_phrase));
    const gl = glosse(s.gloss); if (gl && stufe > 1) gl.hidden = true;
    const frSpalte = el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.ziel_sprache), fr, gl);
    const deSpalte = el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.hilfe_sprache), el("p", { class: "satz de", lang: D.lang_hilfe }, s.de),
      stufe === 1 && notiz(s));
    const loesung = stufe > 1 ? sperre(knopf(U.solution, loesen)) : null;
    const weiter = sperre(weiterKnopf());
    if (loesung) gibFrei(loesung, denkzeit(s.fr), false);
    const sprechen = () => nachsprechen(balken, ton(s)).then((sek) => { if (sek) gibFrei(weiter, sek); });
    const hilfen = el("div", { class: "knopfreihe" });
    if (stufe === 2) hilfen.append(tipp("tipp_buchstabe", (e) => { e.currentTarget.hidden = true; if (!geloest) fr.replaceChildren(...lueckenSatz(s, "buchstabe")); }));
    if (stufe === 3) hilfen.append(tipp("tipp_luecke", (e) => { e.currentTarget.hidden = true; if (!geloest) fr.replaceChildren(...lueckenSatz(s, "buchstabe")); }));
    function loesen() { geloest = true; loesung.disabled = true; hilfen.hidden = true; fr.replaceChildren(...lueckenSatz(s, "voll")); if (gl) gl.hidden = false; sprechen(); }
    const abspielen = () => { if (geloest) sprechen(); };
    tasten(abspielen, wennFrei(weiter, naechstes));
    zeige(kopf(),
      ansage(...U.stufen[stufe - 1]),
      karte(f(U.phrase, { n: lage.pos + 1, alle: teil.saetze.length }) + (s.titel ? " · " + s.titel : ""),
        el("div", { class: "spalten" }, stufe === 3 ? [deSpalte, frSpalte] : [frSpalte, deSpalte]),
        hilfen, balken,
        el("div", { class: "knopfreihe" }, knopf(U.encore_hoeren, abspielen), loesung, weiter)));
    abspielen();
  }

  /* ---------- Zeitmaschine: derselbe Satz heute – gestern – morgen ---------- */
  function zeigeZeitmaschine(teil) {
    const w = WENDUNG[teil.ids[lage.pos]], s = w.satz, Z = U.zeiten;
    const ZEITEN = ["pc", "fp"];
    const balken = jetztDu();
    const weiter = sperre(weiterKnopf());
    let offen = 0;
    const zeilen = [el("div", { class: "zeit offen" },
      el("span", { class: "zeit-label" }, el("b", {}, Z.jetzt[0]), Z.jetzt[1]),
      el("p", { class: "zeit-satz", lang: D.lang }, lueckenSatz(s, "voll")))];
    const knoepfe = [];
    ZEITEN.forEach((k, i) => {
      const [label, zeitname, frage] = Z[k];
      const satz = el("p", { class: "zeit-satz", lang: D.lang }, el("span", { class: "profi" }, frage));
      const zeile = el("div", { class: "zeit" + (i === 0 ? " jetzt" : "") }, el("span", { class: "zeit-label" }, el("b", {}, label), zeitname), satz);
      const kn = sperre(knopf(f(U.solution_zeit, { zeit: label.toLowerCase() }), () => {
        kn.hidden = true; offen++;
        satz.replaceChildren(w.zeit[k].fr); zeile.classList.add("offen"); zeile.classList.remove("jetzt");
        if (knoepfe[i + 1]) { zeilen[i + 2].classList.add("jetzt"); knoepfe[i + 1].hidden = false; gibFrei(knoepfe[i + 1], denkzeit(w.zeit[k].fr), false); }
        nachsprechen(balken, ton(w.zeit[k])).then((sek) => { if (sek && offen === ZEITEN.length) gibFrei(weiter, sek); });
      }, i === 0 ? "haupt" : ""));
      if (i > 0) kn.hidden = true;
      knoepfe.push(kn); zeilen.push(zeile);
    });
    gibFrei(knoepfe[0], denkzeit(s.fr) + 2, false);
    const alles = () => spiele([ton(s), ...ZEITEN.filter((_, i) => i < offen).map((k) => ton(w.zeit[k]))]);
    tasten(alles, wennFrei(weiter, naechstes));
    zeige(kopf(),
      ansageU("zeit_ansage"),
      karte(`${f(U.phrase, { n: lage.pos + 1, alle: teil.ids.length })} · ${w.fr} (${w.anker})`,
        el("p", { class: "satz de", lang: D.lang_hilfe }, s.de),
        el("div", { class: "zeiten" }, zeilen), balken,
        el("div", { class: "knopfreihe" }, knopf(U.encore_hoeren, alles), ...knoepfe, weiter)));
    spiele([ton(s)]);
  }

  /* ---------- Wendung wiederfinden: Hilfe → Ziel mit Selbstkontrolle ---------- */
  function zeigeAbfrage(teil) {
    if (!lage.reihe) lage.reihe = mischen(teil.ids);
    const w = WENDUNG[lage.reihe[lage.pos]];
    const balken = jetztDu();
    const frage = el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de);
    const antwort = el("div", { hidden: true }, el("p", { class: "wendung", lang: D.lang }, w.fr, " ", registerSchild(w)), glosse(w.gloss, "gloss klein"),
      el("p", { class: "klein", lang: D.lang }, w.satz.fr), glosse(w.satz.gloss), notiz(w));
    const bewerten = el("div", { class: "bewerten", hidden: true },
      knopf(U.je_savais, naechstes, "haupt weiter"),
      knopf(U.encore, () => { lage.reihe.push(w.id); naechstes(); }, "encore"));
    const loesung = sperre(knopf(U.solution, () => {
      loesung.hidden = true; antwort.hidden = false; bewerten.hidden = false;
      tasten(() => nachsprechen(balken, [ton(w), ton(w.satz)]), naechstes);
      nachsprechen(balken, [ton(w), ton(w.satz)]);
    }, "haupt"));
    gibFrei(loesung, 1.5, false);
    tasten(null, wennFrei(loesung, () => loesung.click()));
    zeige(kopf(),
      ansageU("wie_sagt_man"),
      karte(f(U.expression, { n: lage.pos + 1, alle: lage.reihe.length }),
        el("div", { class: "vok" }, el("div", {}, frage, antwort)), balken,
        el("div", { class: "knopfreihe" }, loesung), bewerten));
  }

  /* ---------- Belohnungen ----------
     Punkte und Titel pro Sprache; Serie gemeinsam: Schultage im Saarland (Mo–Fr ohne Ferien und Feiertage),
     🔥 3 Schultage am Stück · ⭐ perfekte Woche = neues Kapitel · 👑 4 perfekte Wochen · 🏖️ Wochenende = Bonus.
     Karte: jede fertige Séance und jeder zum ersten Mal fertige Teil schalten den nächsten Ort frei. */
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const heute = () => (window.__heute ? new Date(window.__heute + "T12:00:00") : new Date());
  const plusTage = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const montag = (d) => plusTage(d, -((d.getDay() + 6) % 7));
  const istFrei = (t) => SP.frei.some((f) => t >= f.von && t <= f.bis);
  const istSchultag = (d) => d.getDay() >= 1 && d.getDay() <= 5 && !istFrei(iso(d));
  const schultageDerWoche = (mo) => [0, 1, 2, 3, 4].map((i) => plusTage(mo, i)).filter(istSchultag);
  const titelIndex = (p) => SP.titel.reduce((i, t, k) => (p >= t.ab ? k : i), 0);
  const neueTeile = () => Object.keys(S.teile).length;
  const orteBei = (n) => Math.min(SP.orte.length, n);
  const orteFrei = () => orteBei(neueTeile() + S.spiel.seances);
  function serie() {
    const sr = stand.serie;
    let d = heute(), n = 0;
    if (!sr.tage[iso(d)]) d = plusTage(d, -1);
    for (let i = 0; i < 400; i++, d = plusTage(d, -1)) {
      if (!istSchultag(d)) continue;
      if (sr.tage[iso(d)]) n++; else break;
    }
    return n;
  }
  function wochenSerie(mo) {
    let n = 0;
    for (let w = mo, i = 0; i < 60; i++, w = plusTage(w, -7)) {
      if (!schultageDerWoche(w).length) continue;
      if (stand.serie.wochen.includes(iso(w))) n++; else break;
    }
    return n;
  }
  const ereignisse = [];
  function belohne(erstesMal, istSeance) {
    const sr = stand.serie, d = heute(), tag = iso(d);
    const vorher = orteBei(neueTeile() + S.spiel.seances - (istSeance ? 0 : erstesMal ? 1 : 0));
    if (istSeance) S.spiel.seances++;
    if (orteFrei() > vorher) ereignisse.push({ art: "ort", ort: SP.orte[orteFrei() - 1] });
    let plus = istSeance ? PUNKTE.seance : erstesMal ? PUNKTE.teil : PUNKTE.wiederholung;
    const ersterDesTages = !sr.tage[tag];
    sr.tage[tag] = (sr.tage[tag] || 0) + 1;
    if (ersterDesTages) {
      if (!istSchultag(d)) {
        if (d.getDay() === 0 || d.getDay() === 6) { sr.wochenende.push(tag); plus += PUNKTE.wochenende; ereignisse.push({ art: "toast", text: f(U.bonus_weekend, { p: PUNKTE.wochenende }) }); }
      } else {
        const n = serie();
        if (n >= 3 && n % 3 === 0 && !sr.feuer.includes(tag)) {
          sr.feuer.push(tag); plus += PUNKTE.feuer;
          ereignisse.push({ art: "feier", symbol: "🔥", titel: f(U.en_feu, { n }), text: f(U.en_feu_text, { n, p: PUNKTE.feuer }), ton: SP.texte.feuer });
        }
        const mo = montag(d);
        if (schultageDerWoche(mo).every((x) => sr.tage[iso(x)]) && !sr.wochen.includes(iso(mo))) {
          sr.wochen.push(iso(mo)); plus += PUNKTE.woche;
          const kap = D.geschichte[Math.min(D.geschichte.length, 1 + sr.wochen.length) - 1];
          ereignisse.push({ art: "feier", symbol: "⭐", titel: U.semaine_parfaite_titel,
            text: f(U.semaine_parfaite_text, { p: PUNKTE.woche }) + (kap && sr.wochen.length < D.geschichte.length ? f(U.nouveau_chapitre, { titel: kap.titel }) : U.suite_bientot), ton: SP.texte.woche });
          const ws = wochenSerie(mo);
          if (ws >= 4 && ws % 4 === 0) {
            plus += PUNKTE.monat; if (!sr.abzeichen.includes("monat")) sr.abzeichen.push("monat");
            ereignisse.push({ art: "feier", symbol: "👑", titel: U.mois_parfait, text: f(U.mois_parfait_text, { n: ws, p: PUNKTE.monat }), ton: SP.texte.monat });
          }
        }
      }
    }
    punkteDazu(plus);
  }
  function punkteDazu(plus) {
    const sp = S.spiel;
    sp.punkte += plus;
    ereignisse.unshift({ art: "toast", text: `+${plus} ⭐` });
    const t = titelIndex(sp.punkte);
    if (t > sp.titel) {
      sp.titel = t;
      const ti = SP.titel[t];
      ereignisse.push({ art: "feier", symbol: ti.symbol, titel: ti.name, text: f(U.nouveau_titre, { name: ti.name }), ton: ti.audio ? ti : { text: f(U.nouveau_titre, { name: ti.name }) } });
    }
    speichern();
    setTimeout(zeigeEreignisse, 50);
  }
  const toastBox = el("div", { class: "toasts", "aria-live": "polite" });
  document.body.append(toastBox);
  const feier = el("dialog", { class: "feier", "aria-labelledby": "feier-titel" });
  document.body.append(feier);
  function toast(text, dauer = 2200) {
    const t = el("div", { class: "toast" }, text);
    toastBox.append(t);
    setTimeout(() => t.classList.add("weg"), dauer);
    setTimeout(() => t.remove(), dauer + 600);
    return t;
  }
  // Lob-Pop-up in der Séance: Lob in der Zielsprache, Übersetzung darunter
  function lobToast(text) {
    if (!text) return;
    [...toastBox.querySelectorAll(".toast.lob")].forEach((t) => t.remove());
    toast(lobZeile(text, "div"), 3000).classList.add("lob");
  }
  // Klang zum Stempel: „Tock“ (Aufschlag) + „Bling“ (zwei Glockentöne), im Browser erzeugt, leiser als die Stimme
  let klangCtx = null;
  const KLANG_LAUT = 0.5;
  function stempelKlang(verzoegerung) {
    try {
      if (!klangCtx) klangCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (klangCtx.state === "suspended") klangCtx.resume();
    } catch { return; }
    const c = klangCtx, t = c.currentTime + verzoegerung;
    const glocke = (start, fq, dauer, vol) => {
      const m = c.createGain();
      m.gain.setValueAtTime(0.0001, start);
      m.gain.exponentialRampToValueAtTime(vol * KLANG_LAUT, start + 0.006);
      m.gain.exponentialRampToValueAtTime(0.0001, start + dauer);
      m.connect(c.destination);
      [[1, 1], [2.76, 0.22], [5.4, 0.08]].forEach(([mal, v]) => {
        const o = c.createOscillator(), g = c.createGain();
        o.frequency.value = fq * mal; g.gain.value = v;
        o.connect(g).connect(m); o.start(start); o.stop(start + dauer + 0.05);
      });
    };
    const o = c.createOscillator(), g = c.createGain();
    o.frequency.setValueAtTime(190, t); o.frequency.exponentialRampToValueAtTime(70, t + 0.09);
    g.gain.setValueAtTime(0.9 * KLANG_LAUT, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
    o.connect(g).connect(c.destination); o.start(t); o.stop(t + 0.14);
    const len = Math.ceil(c.sampleRate * 0.05), buf = c.createBuffer(1, len, c.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const q = c.createBufferSource(), fl = c.createBiquadFilter(), gq = c.createGain();
    q.buffer = buf; fl.type = "lowpass"; fl.frequency.value = 900; gq.gain.value = 0.45 * KLANG_LAUT;
    q.connect(fl).connect(gq).connect(c.destination); q.start(t);
    glocke(t + 0.11, 1318.5, 0.7, 0.32); glocke(t + 0.2, 1760, 0.9, 0.3);
  }
  // Reisestempel beim Freischalten eines Ortes: Umriss des Gebiets, kurz (2 s), antippen schließt
  function ortStempel(ort) {
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "stempel-bild"); svg.setAttribute("aria-hidden", "true");
    const pfad = document.createElementNS(NS, "path");
    pfad.setAttribute("d", SP.karte[ort.dep].d); svg.append(pfad);
    const punkt = document.createElementNS(NS, "circle");
    punkt.setAttribute("cx", ort.x); punkt.setAttribute("cy", ort.y); punkt.setAttribute("r", "3"); punkt.setAttribute("class", "stempel-punkt"); svg.append(punkt);
    const farben = [D.theme.blau, "#ffffff", D.theme.rot];
    const box = el("div", { class: "stempel-box", role: "status", onclick: () => box.remove() },
      el("div", { class: "stempel-karte" }, svg,
        el("div", { class: "stempel", lang: D.lang }, el("strong", {}, ort.name.toUpperCase()), el("span", {}, `${gebietName(ort)} · ${U.visite}`)),
        el("div", { class: "sterne", "aria-hidden": "true" }, Array.from({ length: 10 }, (_, i) =>
          el("span", { style: `--w:${i * 36}deg;--f:${farben[i % 3]}` }, "★")))));
    document.body.append(box);
    stempelKlang(0.72);
    try {
      const b = pfad.getBBox(), rand = Math.max(b.width, b.height) * 0.15;
      svg.setAttribute("viewBox", `${b.x - rand} ${b.y - rand} ${b.width + 2 * rand} ${b.height + 2 * rand}`);
    } catch { svg.setAttribute("viewBox", "0 0 600 600"); }
    setTimeout(() => box.classList.add("weg"), 2200);
    setTimeout(() => box.remove(), 2700);
  }
  function zeigeEreignisse() {
    while (ereignisse.length && (ereignisse[0].art === "toast" || ereignisse[0].art === "ort")) {
      const e = ereignisse.shift();
      if (e.art === "ort") ortStempel(e.ort); else toast(e.text);
    }
    if (!ereignisse.length || feier.open) return;
    const e = ereignisse.shift();
    const tonE = e.ton && (e.ton.audio || { text: e.ton.text });
    feier.replaceChildren(konfetti(),
      el("div", { class: "feier-symbol", "aria-hidden": "true" }, e.symbol), el("h2", { id: "feier-titel", lang: D.lang }, e.titel), el("p", { lang: D.lang }, e.text),
      el("div", { class: "knopfreihe" },
        tonE && knopf(U.hoeren, () => spiele([tonE])),
        knopf(U.suivant, () => { feier.close(); stopp(); setTimeout(zeigeEreignisse, 300); }, "haupt")));
    feier.showModal();
    if (tonE) setTimeout(() => { if (feier.open) spiele([tonE]); }, 900);
  }
  function konfetti() {
    const farben = [D.theme.blau, "#ffffff", D.theme.rot, "#ffd23f", "#8fb0ff"];
    return el("div", { class: "konfetti", "aria-hidden": "true" }, Array.from({ length: 36 }, (_, i) =>
      el("span", { style: `left:${(i * 37) % 100}%;background:${farben[i % 5]};animation-delay:${(i % 9) * 0.12}s` })));
  }
  function statusleiste() {
    const sp = S.spiel, t = SP.titel[sp.titel];
    return el("div", { class: "statusleiste" + (stand.serie.abzeichen.includes("monat") ? " gold" : "") },
      el("span", { class: "status-titel", lang: D.lang }, `${t.symbol} ${t.name}`),
      el("span", {}, `⭐ ${sp.punkte} ${U.points}`),
      el("span", { title: U.jours_suite }, `🔥 ${serie()}`),
      knopf(U.sammlung, sammlung, "haupt"));
  }
  function sammlung() {
    lage = null; seance = null; ansicht = sammlung; tasten(null, null);
    const sp = S.spiel, sr = stand.serie, t = sp.titel, naechster = SP.titel[t + 1];
    const mo = montag(heute());
    const woche = U.tage.map((name, i) => {
      const d = plusTage(mo, i), frei = !istSchultag(d), ok = !!sr.tage[iso(d)];
      return el("li", { class: frei ? "frei" : ok ? "ok" : "" }, el("span", {}, name), el("b", {}, frei ? "–" : ok ? "🔥" : "○"));
    });
    const karten = Object.values(S.karten);
    const stufen = INTERVALLE.map((_, i) => karten.filter((k) => k.s === i).length);
    const fakt = el("div", { class: "fakt", hidden: true, "aria-live": "polite" });
    const frei = orteFrei(), KI = SP.karte_info;
    const karte = laenderKarte(frei, (o) => {
      fakt.hidden = false;
      // Ortsfakt mit Übersetzung immer sichtbar (nicht nur per Tipp): Mr. Alex, 16.10., „die Ortstexte sind nicht übersetzt“
      fakt.replaceChildren(el("h3", { lang: D.lang }, `${o.name} · ${gebietName(o)}${o.region !== o.dep_name ? " · " + o.region : ""}`),
        el("p", { lang: D.lang }, o.fakt), o.fakt_de && el("p", { class: "fakt-de", lang: D.lang_hilfe }, o.fakt_de),
        knopf(U.hoeren, () => spiele([o.audio || { text: o.fakt }])));
      spiele([o.audio || { text: o.fakt }]);
    });
    const B = U.badge_liste;
    const abz = [
      ["🔥", B[0], sr.feuer.length > 0], ["⭐", B[1], sr.wochen.length > 0], ["🏅", B[2], sr.wochen.length >= 5],
      ["👑", B[3], sr.abzeichen.includes("monat")], ["🏖️", B[4], sr.wochenende.length > 0],
      ["🗺️", KI.badge, SP.orte.length > 0 && orteFrei() === SP.orte.length], ["📦", B[5], karten.length >= 100], ["🧠", B[6], karten.filter((k) => k.s >= 3).length >= 50],
    ];
    const offline = el("div", { class: "offline-box" });
    zeige(
      el("header", { class: "kopf" }, knopf(U.zurueck_accueil, startseite, "leise"), el("h1", {}, U.sammlung)),
      el("section", { class: "satzkarte titel-karte" + (sr.abzeichen.includes("monat") ? " gold" : "") },
        el("p", { class: "klein" }, `${U.ton_titre} · ${D.name}`),
        el("div", { class: "titel-symbol", "aria-hidden": "true" }, SP.titel[t].symbol),
        el("h2", { lang: D.lang }, SP.titel[t].name),
        el("p", {}, `⭐ ${sp.punkte} ${U.points}`),
        naechster && el("div", { class: "fortschritt" }, el("span", { style: `width:${Math.round(100 * (sp.punkte - SP.titel[t].ab) / (naechster.ab - SP.titel[t].ab))}%` })),
        naechster && el("p", { class: "klein" }, f(U.encore_points, { n: naechster.ab - sp.punkte, name: naechster.name, symbol: naechster.symbol }))),
      el("section", { class: "satzkarte" },
        el("h2", {}, U.cette_semaine),
        el("ol", { class: "wochenleiste" }, woche),
        el("p", { class: "klein" }, uf("serie_text", { n: serie(), w: sr.wochen.length }))),
      el("section", { class: "satzkarte" },
        el("h2", {}, f(U.boite, { n: karten.length })),
        el("p", { class: "klein" }, uf("boite_text")),
        el("ul", { class: "abzeichen" }, stufen.map((n, i) => el("li", { class: n ? "ok" : "" }, el("span", {}, `${i}`), el("span", {}, `${n} · ${INTERVALLE[i]} ${U.jours}`))))),
      D.geschichte.length && el("section", { class: "satzkarte" },
        el("h2", {}, `📖 ${D.geschichte_info.titel} (${kapitelFrei()} / ${D.geschichte.length})`),
        el("p", { class: "klein" }, frde(D.geschichte_info.sammlung[0], D.geschichte_info.sammlung[1])),
        el("div", { class: "heldenraster" }, D.geschichte.map((k) => k.nr <= kapitelFrei()
          ? el("button", { class: "kapitel-karte", onclick: () => zeigeKapitel(k.nr) }, el("span", { class: "kapitel-nr" }, f(U.chapitre, { n: k.nr })), el("strong", { lang: D.lang }, k.titel))
          : el("div", { class: "held-zu", "aria-label": U.pas_debloque }, el("span", {}, "?"), el("small", {}, U.semaine_parfaite))))),
      SP.orte.length && el("section", { class: "satzkarte" },
        el("h2", {}, `🗺️ ${KI.name} (${frei} / ${SP.orte.length} ${KI.lieux})`),
        el("p", { class: "klein" }, frde(KI.hinweis[0], KI.hinweis[1])),
        karte, fakt),
      el("section", { class: "satzkarte" },
        el("h2", {}, U.badges),
        el("ul", { class: "abzeichen" }, abz.map(([sym, name, ok]) => el("li", { class: ok ? "ok" : "" },
          el("span", { "aria-hidden": "true" }, sym), el("span", { lang: D.lang }, name), el("span", { class: "unsichtbar" }, ok ? "✓" : "–"))))),
      el("section", { class: "satzkarte" },
        el("h2", {}, `${U.offline} · ${D.name}`),
        el("p", { class: "klein" }, uf("offline_text")),
        offline));
    offlineBox(offline);
  }

  function laenderKarte(frei, waehle) {
    const NS = "http://www.w3.org/2000/svg", KI = SP.karte_info;
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", "0 0 600 600"); svg.setAttribute("class", "france"); svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", KI.name);
    const offen = SP.orte.slice(0, frei), punkte = {};
    const besucht = new Set(offen.map((o) => o.dep));
    offen.forEach((o) => { const a = SP.karte[o.dep] && SP.karte[o.dep].auch; if (a) besucht.add(a); });   // Einschub: auch das Gebiet auf der Landeskarte
    const gebiete = {};
    // Einschub (İstanbul): Rahmen, Verbindungslinie zum Ort auf der Landeskarte, Beschriftung – vor den Gebieten, damit das Gebiet darüber liegt
    Object.entries(SP.karte).forEach(([code, d]) => {
      if (!d.rahmen) return;
      const [x, y, w, h] = d.rahmen;
      if (d.von) {
        const l = document.createElementNS(NS, "line");
        l.setAttribute("x1", d.von[0]); l.setAttribute("y1", d.von[1]); l.setAttribute("x2", x + w / 2); l.setAttribute("y2", y); l.setAttribute("class", "f-einschub-linie");
        svg.append(l);
      }
      const r = document.createElementNS(NS, "rect");
      r.setAttribute("x", x); r.setAttribute("y", y); r.setAttribute("width", w); r.setAttribute("height", h); r.setAttribute("rx", "6"); r.setAttribute("class", "f-einschub");
      svg.append(r);
    });
    Object.entries(SP.karte).forEach(([code, d]) => {
      const p = document.createElementNS(NS, "path");
      p.setAttribute("d", d.d); gebiete[code] = p;
      p.setAttribute("class", "f-dep" + (besucht.has(code) ? " offen" : ""));
      const t = document.createElementNS(NS, "title"); t.textContent = `${d.nom} (${code}) · ${d.region}`; p.append(t);
      svg.append(p);
    });
    Object.values(SP.karte).forEach((d) => {   // Beschriftung des Einschubs über den Gebieten
      if (!d.rahmen) return;
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", d.rahmen[0] + 10); t.setAttribute("y", d.rahmen[1] + d.rahmen[3] - 10); t.setAttribute("class", "f-einschub-titel"); t.textContent = d.nom; svg.append(t);
    });
    offen.forEach((o, i) => {
      const g = document.createElementNS(NS, "g");
      g.setAttribute("class", "f-ort" + (i === frei - 1 ? " neu" : "")); g.setAttribute("tabindex", "0"); g.setAttribute("role", "button"); g.setAttribute("aria-label", o.name);
      const c = document.createElementNS(NS, "circle");
      c.setAttribute("cx", o.x); c.setAttribute("cy", o.y); c.setAttribute("r", "7"); g.append(c);
      const t = document.createElementNS(NS, "title"); t.textContent = o.name; g.append(t);
      g.addEventListener("click", () => markiere(o));
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); markiere(o); } });
      svg.append(g); punkte[o.id] = g;
    });
    // Gewählter Ort: sein Gebiet bekommt Rahmen und Farbe, der Punkt wird größer (Mr. Alex, 15.10.: Gebiete waren nicht zu unterscheiden)
    function markiere(o) {
      svg.querySelectorAll(".gewaehlt").forEach((x) => x.classList.remove("gewaehlt"));
      if (gebiete[o.dep]) { gebiete[o.dep].classList.add("gewaehlt"); svg.append(gebiete[o.dep]); }   // nach vorn, damit der Rahmen ganz sichtbar ist
      const auch = SP.karte[o.dep] && SP.karte[o.dep].auch;
      if (auch && gebiete[auch]) { gebiete[auch].classList.add("gewaehlt"); svg.append(gebiete[auch]); }
      Object.values(punkte).forEach((g) => svg.append(g));   // Punkte bleiben über den Gebieten
      punkte[o.id].classList.add("gewaehlt");
      waehle(o);
    }
    const liste = offen.map((o, i) => el("button", { class: "staat-chip" + (i % 2 ? " b" : ""), lang: D.lang, onclick: () => markiere(o) }, o.name));
    return el("div", { class: "usa-block" }, el("div", { class: "france-rahmen" }, svg),
      el("p", { class: "staaten-zahl" }, `${frei} / ${SP.orte.length} ${KI.lieux} · ${new Set(offen.map((o) => o.dep)).size} ${KI.einheit}`),
      el("div", { class: "staaten-liste" }, liste),
      el("p", { class: "klein bildnachweis" }, KI.quelle));
  }

  // Gebiet mit Code (« Moselle (57) », « Bologna (BO) »), ohne Code bei langen Kennungen (Beleriand: « Doriath »)
  const gebietName = (o) => (o.dep && String(o.dep).length <= 3 ? `${o.dep_name} (${o.dep})` : o.dep_name);

  /* ---------- Offline pro Sprache: Audio-Dateien in den Audio-Speicher laden (ll-audio, siehe sw.js) ---------- */
  const AUDIO_CACHE = () => D.audio_speicher || "ll-audio";
  let offlineLauf = null;
  async function offlineStand() {
    if (!window.caches) return null;
    const c = await caches.open(AUDIO_CACHE());
    const da = new Set((await c.keys()).map((r) => { const u = new URL(r.url); return (u.pathname + u.search).split("/audio/")[1]; }).filter(Boolean).map((p) => "audio/" + p));
    return D.audio_liste.filter((p) => da.has(p)).length;
  }
  async function offlineBox(box) {
    const alle = D.audio_liste.length;
    const n = await offlineStand();
    if (n === null || !location.protocol.startsWith("http")) { box.replaceChildren(el("p", { class: "klein" }, "–")); return; }
    const stand_ = el("p", { class: "offline-stand" }, n >= alle ? U.offline_fertig : f(U.offline_stand, { n, alle }));
    const balken = el("div", { class: "fortschritt" }, el("span", { style: `width:${Math.round(100 * n / alle)}%` }));
    const laden = knopf(U.offline_laden, async () => {
      if (offlineLauf) return;
      laden.disabled = true; offlineLauf = true;
      const c = await caches.open(AUDIO_CACHE());
      const vorhanden = new Set((await c.keys()).map((r) => { const u = new URL(r.url); return (u.pathname + u.search).split("/audio/")[1]; }).filter(Boolean).map((p) => "audio/" + p));
      const fehlend = D.audio_liste.filter((p) => !vorhanden.has(p));
      let geladen = alle - fehlend.length;
      for (let i = 0; i < fehlend.length; i += 10) {
        await Promise.all(fehlend.slice(i, i + 10).map((p) => c.add(p).catch(() => null)));
        geladen = Math.min(alle, geladen + 10);
        stand_.textContent = f(U.offline_laeuft, { n: geladen, alle });
        balken.firstChild.style.width = `${Math.round(100 * geladen / alle)}%`;
      }
      offlineLauf = null;
      const jetzt = await offlineStand();
      stand_.textContent = jetzt >= alle ? U.offline_fertig : f(U.offline_stand, { n: jetzt, alle });
      laden.disabled = jetzt >= alle;
    });
    laden.disabled = n >= alle;
    box.replaceChildren(stand_, balken, el("div", { class: "knopfreihe" }, laden));
  }

  /* ---------- Tasten: Leertaste = Abspielen, Pfeile = Weiter / Zurück ---------- */
  let tastenAbspielen = null, tastenWeiter = null;
  function tasten(abspielen, weiter) { tastenAbspielen = abspielen; tastenWeiter = weiter; }
  document.addEventListener("keydown", (e) => {
    if (feier.open || e.target.closest("textarea, input")) return;
    if (e.code === "Space" && tastenAbspielen) { e.preventDefault(); tastenAbspielen(); }
    else if (e.code === "ArrowRight" && tastenWeiter) { e.preventDefault(); tastenWeiter(); }
    else if (e.code === "ArrowLeft" && lage && !lage.ende) {
      const z = app.querySelector(".zurueck-knopf");
      if (z && !z.disabled) { e.preventDefault(); z.click(); }
    }
  });

  setzeSprache(stand.paar, false);
  setzeDe(!!stand.de);
  startseite();

  // Offline-Speicher (nur über eine Webadresse)
  if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
    const hatteAlteVersion = !!navigator.serviceWorker.controller;
    let neuGeladen = false;
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (hatteAlteVersion && !neuGeladen) { neuGeladen = true; location.reload(); }
    });
    navigator.serviceWorker.register("sw.js", { updateViaCache: "none" })
      .then((r) => r.update())
      .catch(() => { /* ohne Offline-Speicher geht es trotzdem */ });
  }
})();
