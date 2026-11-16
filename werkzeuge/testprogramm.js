// Festes Testprogramm für Language Learning (Mr. Alex, 15.11.2026). Vorher bauen: python3 werkzeuge/bauen.py
// Aufruf:  node werkzeuge/testprogramm.js                 alles (Kern, alle Sprachen, Wege, drei Formate, Offline-Liste)
//          node werkzeuge/testprogramm.js --nur=fr-de      nur eine Sprache (Kern und Offline-Liste immer)
//          node werkzeuge/testprogramm.js --format=handy   nur ein Format (laptop 1366×768, handy 360×740, ipad 820×1180)
//          node werkzeuge/testprogramm.js --schnell        nur Kern, Laden und Offline-Liste
// Ausgabe: je Prüfung eine Zeile, am Ende „ALLES OK“ oder die Fehlerliste; Rückgabewert 1 bei Fehlern.
// Grenzen: Chromium (auch für das iPad-Format, kein echtes Safari); Klang, Aussprache und Aussehen prüft kein Test.
const { execFileSync } = require("child_process");
const http = require("http"), fs = require("fs"), path = require("path");
const BASIS = path.join(__dirname, ".."), APP = path.join(BASIS, "app");
const arg = (n) => (process.argv.find((a) => a.startsWith(`--${n}=`)) || "").split("=")[1];
const NUR = arg("nur"), FORMAT = arg("format"), SCHNELL = process.argv.includes("--schnell");
const FORMATE = { laptop: [1366, 768], handy: [360, 740], ipad: [820, 1180] };
const fehler = [];
const ok = (name, bed, info = "") => { console.log(`${bed ? "✓" : "✗"} ${name}${info ? " – " + info : ""}`); if (!bed) fehler.push(name + (info ? " – " + info : "")); };

// 1. Lernkern
try { execFileSync("node", [path.join(__dirname, "lernkern_test.js")], { stdio: "pipe" }); ok("Lernkern-Tests", true); }
catch (e) { ok("Lernkern-Tests", false, String(e.stdout).split("\n").filter((z) => z.startsWith("FEHLER")).join(" | ")); }

// 2. Offline-Liste: jede Kern-Datei steht in sw.js (sonst kommt ein Update nicht aufs Gerät)
for (const ordner of ["", "english"]) {
  const sw = fs.readFileSync(path.join(APP, ordner, "sw.js"), "utf8");
  const fehlt = fs.readdirSync(path.join(APP, ordner)).filter((n) => /\.(js|css|html|webmanifest)$/.test(n) && n !== "sw.js" && !sw.includes(`"${n}"`));
  ok(`Offline-Liste ${ordner || "Wurzel"}`, fehlt.length === 0, fehlt.join(", "));
}

const srv = http.createServer((q, r) => {
  let u = decodeURIComponent(q.url.split("?")[0]); if (u.endsWith("/")) u += "index.html";
  const f = path.join(APP, u);
  fs.readFile(f, (e, d) => {
    if (e) { r.writeHead(404); r.end(); return; }
    const typ = f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".mp3") ? "audio/mpeg" : f.endsWith(".png") ? "image/png" : "text/html";
    r.writeHead(200, { "Content-Type": typ }); r.end(d);
  });
}).listen(0);
const URL = `http://localhost:${srv.address().port}/`;

(async () => {
  const { chromium } = require("/opt/node-tools/node_modules/playwright");
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const paare = Object.keys((() => { const w = { SPRACHEN: {} }; for (const f of fs.readdirSync(APP).filter((n) => /^daten_.*\.js$/.test(n))) new Function("window", fs.readFileSync(path.join(APP, f), "utf8"))(w); return w.SPRACHEN; })())
    .filter((p) => !NUR || p === NUR);
  const neueSeite = async (w, h) => {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    p.setDefaultTimeout(5000);
    p.fehlerListe = [];
    p.on("pageerror", (e) => p.fehlerListe.push(e.message));
    p.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) p.fehlerListe.push(m.text()); });
    p.on("response", (r) => { if (r.status() === 404 && !/\.mp3/.test(r.url())) p.fehlerListe.push("404 " + r.url()); });
    await p.addInitScript(() => { localStorage.setItem("ll-leise", "1"); });
    return p;
  };
  const stand = (paar, sp) => ({ paar, de: false, serie: { tage: {}, wochen: [], feuer: [], wochenende: [], abzeichen: [] }, sprachen: { [paar]: sp } });
  const breit = (p) => p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1 ? `${document.documentElement.scrollWidth} > ${window.innerWidth}` : "");

  // 3. Jede Sprache: lädt ohne Fehler, Hauptwege
  for (const paar of paare) {
    const p = await neueSeite(390, 860);
    await p.goto(URL); await p.waitForTimeout(250);
    const info = await p.evaluate((paar) => { const D = window.SPRACHEN[paar]; return { ws: D.wendungen.map((w) => w.id), th: D.themen[0].id, thName: D.themen[0].name, dlg: (D.dialoge[0] || {}).id }; }, paar);
    const sp = { teile: { [`${info.th}|0|0`]: { am: "2020-01-01", s: 0 } }, karten: {}, tag: null, gruppen: {}, spiel: { punkte: 0, titel: 0, seances: 3 } };
    info.ws.slice(0, 6).forEach((id, i) => { sp.karten[id] = { s: [0, 1, 2, 4, 6, 3][i], f: "2020-01-01" }; });
    if (info.dlg) sp.teile[`dialog:${info.dlg}|0|0`] = { am: "2026-01-01", s: 3 };
    await p.evaluate((st) => localStorage.setItem("languages-v1", JSON.stringify(st)), stand(paar, sp));
    await p.reload(); await p.waitForTimeout(350);
    const wege = [];
    const weg = async (name, fn) => { try { await fn(); wege.push(name); } catch (e) { p.fehlerListe.push(`${name}: ${e.message.split("\n")[0]}`); } };
    await weg("Start", async () => { await p.waitForSelector(".gym-karte", { timeout: 3000 }); });
    await weg("Power Up", async () => { await p.waitForSelector(".powerup-zeile", { timeout: 2000 }); });
    if (!SCHNELL) {
      await weg("Séance", async () => {
        await p.click(".gym-karte .knopf"); await p.waitForTimeout(250);
        for (let i = 0; i < 25 && !(await p.$(".gym-ende")); i++) {
          if (await p.$(".abruf-wahl")) { await p.click(".abruf-wahl .wahl-knopf >> nth=0"); await p.click("button.weiter"); }
          else if (await p.$(".tipp-feld")) { await p.fill(".tipp-feld", "x"); await p.keyboard.press("Enter"); await p.click("button.weiter"); }
          else if (await p.$(".bewerten")) { await p.$eval(".knopfreihe .knopf", (k) => { k.disabled = false; k.click(); }); await p.click(".bewerten .knopf.haupt"); }
          else await p.$eval("button.weiter", (k) => { k.disabled = false; k.click(); });
          await p.waitForTimeout(120);
        }
        await p.waitForSelector(".gym-ende", { timeout: 2000 });
      });
      await weg("Memory", async () => { await p.click('button:has-text("Memory")'); await p.waitForSelector(".memory-karte", { timeout: 2000 }); });
      await weg("Thema-Teil", async () => { await p.goto(URL); await p.waitForTimeout(250); await p.click(`nav.themen .kachel:has-text("${info.thName}")`); await p.click("nav.gruppen .kachel >> nth=0"); await p.waitForSelector(".sprung", { timeout: 2000 }); });
      if (info.dlg) await weg("Dialog", async () => { await p.goto(URL); await p.waitForTimeout(250); await p.click('.kachel:has(.sym:text("💬")) >> nth=0'); await p.waitForSelector("main .knopf", { timeout: 2000 }); });
      await weg("Sammlung und Karte", async () => { await p.goto(URL); await p.waitForTimeout(250); await p.click(".statusleiste .knopf"); await p.waitForSelector(".f-dep", { timeout: 3000 }); });
    }
    ok(`${paar}: lädt ohne Fehler, Wege ${wege.join(", ")}`, p.fehlerListe.length === 0, p.fehlerListe.slice(0, 3).join(" | "));
    await p.close();
  }

  // 4. Passt auf den Bildschirm (Startseite, Séance-Karte, Thema-Teil) in den drei Formaten
  if (!SCHNELL) for (const [fname, [w, h]] of Object.entries(FORMATE).filter(([n]) => !FORMAT || n === FORMAT)) {
    for (const paar of paare.filter((x) => ["fr-de", "ar-de"].includes(x) || NUR)) {
      const p = await neueSeite(w, h);
      await p.goto(URL); await p.waitForTimeout(200);
      const [id, thName] = await p.evaluate((paar) => [window.SPRACHEN[paar].wendungen[0].id, window.SPRACHEN[paar].themen[0].name], paar);
      await p.evaluate((st) => localStorage.setItem("languages-v1", JSON.stringify(st)), stand(paar, { teile: {}, karten: { [id]: { s: 4, f: "2020-01-01" } }, tag: null, gruppen: {}, spiel: { punkte: 0, titel: 0, seances: 0 } }));
      await p.reload(); await p.waitForTimeout(300);
      const zuBreit = [];
      const pruefe = async (wo) => { const r = await breit(p); if (r) zuBreit.push(`${wo} ${r}`); };
      await pruefe("Start");
      await p.click(".gym-karte .knopf"); await p.waitForTimeout(250); await pruefe("Séance");
      await p.goto(URL); await p.waitForTimeout(200); await p.click(`nav.themen .kachel:has-text("${thName}")`); await p.click("nav.gruppen .kachel >> nth=0"); await p.waitForTimeout(250); await pruefe("Thema");
      ok(`${paar} ${fname} ${w}×${h}: passt auf den Bildschirm`, zuBreit.length === 0 && p.fehlerListe.length === 0, [...zuBreit, ...p.fehlerListe].slice(0, 3).join(" | "));
      await p.close();
    }
  }

  // 5. IPA (Französisch, Spanisch, Italienisch): Schalter nur dort, zuerst aus; an = Lautschrift unter Wendung und Beispielsatz;
  //    in Schritt 2/3 verdeckt; in Sprachen ohne IPA (Deutsch) kein Schalter
  for (const paar of ["fr-de", "es-de", "it-de"].filter((x) => !NUR || x === NUR)) {
    const p = await neueSeite(390, 860); p.setDefaultTimeout(5000);
    const probleme = [];
    try {
      await p.goto(URL); await p.waitForTimeout(200);
      const th = await p.evaluate((paar) => window.SPRACHEN[paar].themen[0].name, paar);
      await p.evaluate((st) => localStorage.setItem("languages-v1", JSON.stringify(st)), stand(paar, { teile: {}, karten: {}, tag: null, gruppen: {}, spiel: { punkte: 0, titel: 0, seances: 0 } }));
      await p.reload(); await p.waitForTimeout(300);
      if (await p.$eval(".ipa-knopf", (k) => k.hidden)) probleme.push("Schalter fehlt");
      await p.click(`nav.themen .kachel:has-text("${th}")`); await p.click("nav.gruppen .kachel >> nth=0"); await p.waitForTimeout(250);
      if (await p.$(".ipa")) probleme.push("IPA sichtbar, obwohl aus");
      await p.click(".ipa-knopf"); await p.waitForTimeout(200);
      const z = await p.$$eval(".ipa", (x) => x.filter((e) => e.offsetParent).map((e) => e.textContent));
      if (!z.length || !z[0].startsWith("[")) probleme.push("IPA fehlt nach dem Einschalten");
      await p.click(".sprung >> nth=1"); await p.waitForTimeout(250);
      if ((await p.$$eval(".ipa", (x) => x.filter((e) => e.offsetParent).length)) > 0) probleme.push("IPA in Schritt 2 sichtbar (verrät die Lösung)");
      await p.click('.sprachen button[data-paar="de-fr"]'); await p.waitForTimeout(250);
      if (!(await p.$eval(".ipa-knopf", (k) => k.hidden))) probleme.push("Schalter in Deutsch sichtbar");
    } catch (e) { probleme.push(e.message.split("\n")[0]); }
    ok(`${paar}: IPA zuschaltbar (Schalter, an/aus, in Schritt 2 verdeckt)`, probleme.length === 0 && p.fehlerListe.length === 0, [...probleme, ...p.fehlerListe].slice(0, 3).join(" | "));
    await p.close();
  }

  // 5b. Geschichte (fr/es/it/pt, Mr. Alex 16.11.): Kapitel 1 offen, Kapitel n öffnet sich mit fertigem Thema n,
  //     Wendungen antippbar, « Chapitre lu » erst nach Mindestzeit, 20 Punkte beim ersten Mal, 5 bei Wiederholung (einmal am Tag), Power Up
  for (const paar of ["fr-de", "es-de", "it-de", "pt-de"].filter((x) => !NUR || x === NUR)) {
    const p = await neueSeite(390, 860);
    const probleme = [];
    try {
      await p.goto(URL); await p.waitForTimeout(200);
      const th2 = await p.evaluate((x) => window.SPRACHEN[x].themen[1].id, paar);
      await p.evaluate((st) => localStorage.setItem("languages-v1", JSON.stringify(st)), stand(paar, { teile: {}, karten: {}, tag: null, gruppen: {}, spiel: { punkte: 0, titel: 0, seances: 0 } }));
      await p.reload(); await p.waitForTimeout(300);
      const lies = () => p.evaluate((x) => JSON.parse(localStorage.getItem("languages-v1")).sprachen[x], paar);
      await p.click(`.kachel[aria-label="${await p.evaluate((x) => window.SPRACHEN[x].geschichte_info.titel, paar)}"]`); await p.waitForTimeout(250);
      if (!(await p.$(".kopf .sprung.jetzt"))) probleme.push("Kapitel 1 öffnet nicht");
      if (!(await p.$eval(".kopf .sprung >> nth=1", (k) => k.disabled))) probleme.push("Kapitel 2 offen ohne Thema 2");
      const links = await p.$$eval(".wendung-link", (x) => x.length);
      if (links < 20) probleme.push(`nur ${links} antippbare Wendungen`);
      await p.click(".wendung-link >> nth=0"); await p.waitForTimeout(150);
      if (!(await p.$(".toast"))) probleme.push("Antippen zeigt keine Wendung");
      const lu = `button:has-text("${(await p.evaluate((x) => window.SPRACHEN[x].ui.kapitel_lu, paar)).replace("✓ ", "")}")`;
      if (!(await p.$eval(lu, (k) => k.disabled))) probleme.push("« Chapitre lu » sofort frei");
      await p.$eval(lu, (k) => { k.disabled = false; k.click(); }); await p.waitForTimeout(300);
      let s = await lies();
      if (s.spiel.punkte !== 20) probleme.push(`erstes Lesen ${s.spiel.punkte} Punkte statt 20`);
      if (!s.teile["kapitel:1|0|0"]) probleme.push("Kapitel nicht als Power-Up-Teil gespeichert");
      if (!(await p.$eval(lu, (k) => k.disabled))) probleme.push("zweimal am Tag möglich");
      // Wiederholung an einem anderen Tag: 5 Punkte
      await p.evaluate((x) => { const st = JSON.parse(localStorage.getItem("languages-v1")); st.sprachen[x].kapitel_tag = { 1: "2020-01-01" }; localStorage.setItem("languages-v1", JSON.stringify(st)); }, paar);
      await p.reload(); await p.waitForTimeout(300);
      await p.click(`.kachel[aria-label="${await p.evaluate((x) => window.SPRACHEN[x].geschichte_info.titel, paar)}"]`); await p.waitForTimeout(250);
      await p.$eval(lu, (k) => { k.disabled = false; k.click(); }); await p.waitForTimeout(300);
      s = await lies();
      if (s.spiel.punkte !== 25) probleme.push(`Wiederholung ergibt ${s.spiel.punkte - 20} statt 5 Punkte`);
      // Thema 2 fertig → Kapitel 2 offen
      await p.evaluate(([x, tid]) => { const st = JSON.parse(localStorage.getItem("languages-v1")); for (let g = 0; g < 8; g++) for (let i = 0; i < 12; i++) st.sprachen[x].teile[`${tid}|${g}|${i}`] = { am: "2026-01-01", s: 0 }; localStorage.setItem("languages-v1", JSON.stringify(st)); }, [paar, th2]);
      await p.reload(); await p.waitForTimeout(300);
      await p.click(`.kachel[aria-label="${await p.evaluate((x) => window.SPRACHEN[x].geschichte_info.titel, paar)}"]`); await p.waitForTimeout(250);
      if (!(await p.$(".kopf .sprung.jetzt:has-text('2')"))) probleme.push("Kapitel 2 nach fertigem Thema 2 nicht offen");
      if (await p.$eval(".kopf .sprung >> nth=2", (k) => !k.disabled)) probleme.push("Kapitel 3 offen ohne Thema 3");
    } catch (e) { probleme.push(e.message.split("\n")[0]); }
    ok(`${paar}: Geschichte (Kapitel je Thema, Wendungen antippbar, 20/5 Punkte, Power Up)`, probleme.length === 0 && p.fehlerListe.length === 0, [...probleme, ...p.fehlerListe].slice(0, 3).join(" | "));
    await p.close();
  }

  // 6. English-Ausgabe lädt
  { const p = await neueSeite(390, 860); await p.goto(URL + "english/"); await p.waitForTimeout(400);
    ok("English-Ausgabe lädt", p.fehlerListe.length === 0 && !!(await p.$(".gym-karte")), p.fehlerListe.slice(0, 2).join(" | ")); await p.close(); }

  await b.close(); srv.close();
  console.log(fehler.length ? `\n${fehler.length} FEHLER:\n- ${fehler.join("\n- ")}` : "\nALLES OK");
  process.exit(fehler.length ? 1 : 0);
})().catch((e) => { console.log("✗ Testprogramm abgebrochen – " + e.message); srv.close(); process.exit(1); });
