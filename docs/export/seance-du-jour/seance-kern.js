// Referenz-Auszug aus app/app.js (Language Learning, 16.10.2026): Kern der « Séance du jour ».
// Nicht lauffähig für sich allein – zeigt Ablauf, Zustandsmodell und Regeln. Erklärung in README.md.

  const PUNKTE = { teil: 10, wiederholung: 5, seance: 30, einheit: 50, feuer: 30, wochenende: 20, woche: 100, monat: 200 };

  const heute = () => (window.__heute ? new Date(window.__heute + "T12:00:00") : new Date());

  const plusTage = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };

  const montag = (d) => plusTage(d, -((d.getDay() + 6) % 7));

  const istFrei = (t) => SP.frei.some((f) => t >= f.von && t <= f.bis);

  const istSchultag = (d) => d.getDay() >= 1 && d.getDay() <= 5 && !istFrei(iso(d));

  const schultageDerWoche = (mo) => [0, 1, 2, 3, 4].map((i) => plusTage(mo, i)).filter(istSchultag);

  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;

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

  function starteSeance() {
    const plan = tagesplan();
    lage = null;
    seance = { schlange: [...plan.wdh, ...plan.neu].filter((id) => !plan.fertig.includes(id)), wieder: new Set(), start: Date.now() };
    seancePos = 0;
    if (!seance.schlange.length) return seanceEnde(plan.geschafft);
    zeigeSeanceKarte();
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
          el("p", { class: "wendung", lang: D.lang }, w.fr, " ", registerSchild(w)),
          el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de), notiz(w))),
        el("div", { class: "spalten" },
          el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.exemple), el("p", { class: "satz fr", lang: D.lang }, lueckenSatz(w.satz, "voll"))),
          el("div", { class: "spalte" }, el("span", { class: "sprache" }, U.hilfe_sprache), el("p", { class: "satz de", lang: D.lang_hilfe }, w.satz.de))),
        balken,
        el("div", { class: "knopfreihe" }, knopf(U.encore_hoeren, abspielen), weiter)));
    abspielen();
  }

  function wiederholKarte(w, zaehler) {
    const k = S.karten[w.id];
    const balken = jetztDu();
    const frage = el("div", {}, el("p", { class: "wendung-de", lang: D.lang_hilfe }, w.de), el("p", { class: "satz de", lang: D.lang_hilfe }, w.satz.de));
    const antwort = el("div", { hidden: true },
      el("p", { class: "wendung", lang: D.lang }, w.fr, " ", registerSchild(w)),
      el("p", { class: "satz fr", lang: D.lang }, lueckenSatz(w.satz, "voll")), notiz(w));
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
    const zeichne = () => zeige(seanceKopf(), el("section", { class: "geschafft" },
      el("h2", { lang: D.lang }, alles ? U.fini : U.pause),
      lobZeile(text, "p", textDe),
      ufp(alles ? "fini_text" : "pause_text"),
      el("div", { class: "knopfreihe" }, knopf(U.accueil, startseite, "haupt"), knopf(U.sammlung, sammlung))));
    ansicht = zeichne; seance = null; tasten(null, null);
    zeichne();
    setTimeout(() => spiele([r && tonLob(r), fini && (fini.audio || { text: fini.text })]), 300);
  }

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

  const sprechDauer = (d, min = 1.8) => Math.max(min, d * 0.85 + 0.6);

  const denkzeit = (text) => Math.min(4, Math.max(1.5, 1 + String(text).split(/\s+/).length * 0.175));

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
      if (datei.rate) a.playbackRate = datei.rate;
      aktuell = a;
      a.onended = () => { gesamt += a.duration || 0; setTimeout(fertig, 350); };
      a.onerror = fertig;
      a.play().catch(fertig);
    })), Promise.resolve()).then(() => (meinLauf === lauf ? gesamt : null));
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

  const ton = (o) => o.audio || { text: o.fr.replace(/[–—]/g, ",") };

  function lueckenSatz(s, art) {
    const w = s.luecke, i = w ? s.fr.indexOf(w) : -1;
    if (i < 0) return [s.fr];
    const mitte = art === "voll" ? el("strong", { class: "ziel" }, w)
      : el("span", { class: "luecke" + (art === "buchstabe" ? " mit-buchstaben" : ""), "aria-label": U.trou },
        art === "buchstabe" ? w.replace(/\S+/g, (x) => x[0] + x.slice(1).replace(/./g, "_")) : w.replace(/\S/g, "_"));
    return [s.fr.slice(0, i), mitte, s.fr.slice(i + w.length)];
  }

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
