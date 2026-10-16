# « Séance du jour » – handover for another app

How the daily vocabulary practice in *Language Learning* works, and everything another
session needs to rebuild it (for example in the Year 6 / Year 9 pupils' app).
Written so that a fresh Claude session can take it over without reading the original repo.

Files in this folder:

| File | What it is |
|---|---|
| `README.md` | This document: concept, flow, rules, state model, screens. |
| `seance-fr.json` | Data export (French pack): 212 phrases with sentences, gaps, notes and audio paths; praise lists with translations; UI strings; pensum, intervals, points, school holidays. |
| `seance-kern.js` | Reference extract of the original functions (plan, cards, evaluation, rewards, audio player). Not runnable on its own, for reading. |
| Audio | Not copied here (32 MB). Public under `https://langenbachalex.github.io/Languages/` + the `audio` path in the JSON (strip the `?v=` part or keep it, both work), or in the repo under `app/audio/fr-de/`. Folders: `wendungen/` (phrase), `saetze/` (sentence, `_pc` passé composé, `_fp` futur proche), `lob/` (praise), `spiel/` (end-of-séance texts). Voice: Mr. Alex's cloned voice (ElevenLabs), loudness −18 LUFS. |

---

## 1. Idea in one paragraph

Every day the learner gets a small, fixed workload: **3 new phrases and up to 8 revisions**
(`pensum`). New phrases are heard and repeated; revisions are recalled from the German prompt,
said aloud, then self-rated « Je savais » or « Encore ». Each phrase lives in a box with a
level 0–7 and a due date; a known card climbs one level and comes back after
1, 3, 7, 14, 30, 60, 120 days (`intervalle_tage`), a failed card drops to level 0, comes back
tomorrow, and is asked again later in the same séance. Finishing the day's plan gives points,
keeps a school-day streak, and after a perfect school week unlocks a story chapter.
There is no typing and no multiple choice in the séance: it is listen, speak, self-assess.

## 2. Data model

### Phrase (`wendungen[]` in the JSON)

```
id        "ep_01"                      stable key, used in the learner's state
thema     "profs"                      theme id (see `themen`)
fr        "corriger des copies"        target language
de        "Klassenarbeiten korrigieren" help language
register  "tu" | "vous"                "vous" shows a small « poli » badge
anker     "corriger"                   anchor word (not used in the séance)
notiz     "une copie = …"              optional teacher's note, shown under the solution
audio     "audio/fr-de/wendungen/ep_01.mp3?v=…"
satz      { fr, de, luecke, audio }    example sentence; `luecke` is the literal substring of
                                       `fr` that forms the gap elsewhere in the app
zeit      { pc: {fr, audio}, fp: {fr, audio} }   optional tense variants (not used in the séance)
```

Order matters: `wendungen` is in curriculum order (theme by theme). New cards are taken from the
front of the list, in this order.

### Learner state (localStorage, one object per language pair)

```
{
  karten:  { "ep_01": { s: 2, f: "2026-10-19" }, … }   s = level 0..7, f = due date (ISO, local)
  tag:     { d: "2026-10-16", wdh: [ids], neu: [ids], fertig: [ids], geschafft: false }
  spiel:   { punkte: 0, titel: 0, seances: 0 }
  teile:   {}   gruppen: {}                             (theme progress, not needed for the séance)
}
```

Shared across language pairs (one per learner):

```
serie: { tage: { "2026-10-16": 1, … }, wochen: ["2026-10-12", …], feuer: [dates], wochenende: [dates], abzeichen: [] }
```

A card that is not in `karten` has never been learned. A card appears in `karten` the moment
the learner finishes its "new" screen, with `s: 0` and `f: tomorrow`.

## 3. The daily plan (`tagesplan()`)

Computed once per calendar day and cached in `tag`; the same plan is shown all day, even
after reloads.

1. `t` = today as ISO date (local time, not UTC).
2. **Revisions** `wdh`: all cards with `f <= t`, sorted by due date (oldest first), ties by
   curriculum order, then cut to `pensum.wiederholung` (8). Overdue cards are not punished,
   they are just first in line.
3. **New** `neu`: the first `pensum.neu` (3) phrases of the curriculum that are not in `karten`.
4. `fertig` = ids completed today, `geschafft` = whether the whole plan was completed once.

The home button shows the plan state: « {neu} nouvelles · {wdh} à réviser · {fertig} / {gesamt} faites »
and a row of small dots, one per card (revision dots styled differently, done dots filled).

## 4. Running a séance

Queue = `[...wdh, ...neu]` minus the ids already in `fertig`. Revisions come first so that the
new material is fresh at the end. Position counter « 2 / 11 » in the card header.

Empty queue → jump straight to the end screen.

For each id: if it is a new card (in `neu` and not yet in `karten`) show the **new-card
screen**, otherwise the **revision screen**.

### New-card screen (`neueKarte`)

```
Nouvelle expression ! Écoute et répète.
┌ 3 / 11 · nouvelle ───────────────────────────┐
│ corriger des copies            [poli badge]   │   ← target, large
│ Klassenarbeiten korrigieren                   │   ← help language
│ 💡 note                                       │
│ Exemple                 | Deutsch              │
│ Ce soir, je **corrige des copies** …  | Heute Abend … │  ← gap text in bold
│ [À toi ! Répète. ▮▮▮▮▮ ]                      │   ← speaking bar, appears after audio
│ [🔊 Encore]  [Suivant ➜]                      │
└──────────────────────────────────────────────┘
```

- On entry the phrase audio and then the sentence audio play (350 ms gap between files).
- Then the **speaking bar** runs: duration = max(1.8 s, 0.85 × audio length + 0.6 s).
  « Suivant » is disabled until that bar has run once (`sperre` / `gibFrei`). Once unlocked for
  this position it stays unlocked (so going back and forth does not re-lock).
- « Suivant »: `karten[id] = { s: 0, f: tomorrow }`, add id to `fertig`, next card.
  No praise on new cards.

### Revision screen (`wiederholKarte`)

```
Comment dit-on en français ? Dis-le à voix haute, puis « Solution ».
┌ 2 / 11 · révision · niveau 1 ────────────────┐
│ fix und fertig sein                           │   ← help language prompt
│ Nach sechs Stunden Unterricht bin ich fix und fertig.  │
│ [Solution]   (disabled for a thinking time)   │
└──────────────────────────────────────────────┘
after « Solution »:
│ être crevé                       [poli badge] │
│ Après six heures de cours, je suis **crevé**. │
│ 💡 note                                       │
│ [À toi ! Répète. ▮▮▮▮▮ ]                      │
│ [😊 Je savais]  [🔁 Encore]                   │
```

- Thinking time before « Solution » unlocks: min(4 s, max(1.5 s, 1 + words × 0.175)).
- « Solution » reveals the phrase and sentence, plays both, starts the speaking bar.
- Keyboard: Space = hear again, Enter = next/solution (nice on desktop, optional).

### Self-assessment (`bewerteKarte`)

```
Je savais:  s = min(s + 1, 7);  f = today + intervalle[min(s, 6)]   (level 7 → 120 days)
            add to fertig; praise pop-up (see 6); save; next
Encore:     s = 0;  f = tomorrow;  save
            first failure in this séance → push id to the END of the queue (asked again)
            second failure            → counts as done (add to fertig), no endless loop
            toast « Pas grave ! Elle revient tout à l'heure. »; next
```

So a failed card is asked twice per séance at most, and always returns tomorrow.

### End screen (`seanceEnde`)

- `alles` = every id of `wdh` and `neu` is in `fertig`.
- First time `alles` becomes true today → `geschafft = true`, rewards (see 7).
- Shows « C'est fini pour aujourd'hui ! » (or « Pause ! » if the learner left early),
  one praise line from the `geschafft` (or `stark`) list with its translation, the explanatory
  text (`fini_text` / `pause_text`), then plays praise audio followed by `spiel_texte.fini`
  (« C'est fini pour aujourd'hui. À demain ! ») – sequentially, never at the same time.
- Leaving early is harmless: `fertig` is kept, re-opening the séance continues with the rest.

## 5. Audio rules

- Every phrase and sentence has an mp3; fallback is the device's speech synthesis with
  `lang = "fr"` if a file is missing (`{ text }` entries in `spiele`).
- Files are played in sequence with a 350 ms gap; starting a new playback stops the old one
  (`stopp()` increments a run counter, late callbacks are ignored).
- A "quiet" mode skips all audio and resolves immediately (speaking bars then use the minimum).
- Audio URLs carry a content hash (`?v=…`) so replaced recordings bypass browser caches; the
  service worker caches audio by full URL and app files ignoring the query.

## 6. Praise (`lob`)

Four lists in the JSON: `lob` (54 everyday praises), `stark` (14, for streaks), `fehler` (10,
gentle), `geschafft` (3, end of day), `voll`, `doch`. Each entry: `text` (French), `de`
(German translation), `audio`, `gruppe` (similarity groups, to avoid two « bravo »-type
praises in a row).

Choice (`waehleRuf`): keep a history of the last 40 praises; prefer an entry not used in the
last rounds of the same kind and not in the same group as the previous ones; fall back
gradually; never repeat the immediately preceding one.

Praise rule (`lob`): count correct answers in a row; every 5th correct answer (or an explicit
"strong" moment) takes from `stark`, otherwise from `lob`.

Display: in the séance a pop-up (toast, 3 s) with the French text large and the German
translation underneath; the audio plays at the same time. On end screens the praise is a
line with the translation under it. The learner may not understand the praise otherwise,
that is why the translation is always shown, independent of the « + DE » help toggle.

## 7. Points, streak, calendar (`belohne`)

Points: finishing the day's séance = 30; a theme part first time = 10, repeat = 5;
a whole theme group = 50. Title thresholds (`titel`) are in the original pack, pupils' app can
use its own.

Streak counts **school days only**: Monday–Friday minus the dates in `schulfreie_tage`
(Saarland holidays 2026/27 in the export, adapt to your calendar). A weekend or holiday
practice does not break the streak and gives a +20 weekend bonus instead.

- Every 3rd consecutive school day: 🔥 « Tu es en feu ! » +30, once per day.
- All school days of a week done: ⭐ « Semaine parfaite » +100, unlocks the next story chapter.
- 4 perfect weeks in a row: 👑 +200, badge « monat ».

Events are queued (`ereignisse`) and shown after the screen renders: toasts for points,
a modal « fête » dialog with sound for streaks, titles and new chapters.

## 8. Things that proved important in beta

- **Ask the learner to speak before they may continue.** The locked « Suivant » with the
  running bar is what turns listening into practice. First version was too strict; the current
  durations (60 % speaking, 50 % thinking of the first draft) feel right for an adult; for
  pupils consider a shorter minimum.
- **Praise needs translation.** Learners hear « Quel accent ! » and do not know what it means.
- **Single words in TTS drift into other languages.** Only full sentences are safe. If you
  record isolated words, speak them inside a carrier sentence and cut the carrier off
  (see `werkzeuge/audio.py`, `TRAEGERSATZ`).
- **Dates must be local, not UTC**, or the plan flips at 1 a.m. and the streak breaks.
- **Cache the plan for the day.** Recomputing on every screen makes cards appear and
  disappear while the learner works.
- Keep the plan small. 3 + 8 takes 5–8 minutes; that is the whole point.

## 9. Minimal rebuild checklist

1. Load `seance-fr.json`; keep `wendungen` order.
2. State per learner: `karten`, `tag`, `spiel`, shared `serie`.
3. Implement `tagesplan`, the two card screens, `bewerteKarte`, `seanceEnde` as in section 3–4
   (`seance-kern.js` has the originals, ~300 lines of plain JS, no framework).
4. Audio player with sequential playback, stop-on-new, 350 ms gap, speech-synthesis fallback.
5. Praise pop-up with translation; praise chooser with history.
6. Points and school-day streak with your own holiday list.
7. Serve the mp3 files from your app or link to the GitHub Pages URL above.
