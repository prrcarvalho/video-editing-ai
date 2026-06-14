# Formula Gap Analysis — reel-1-pedro vs instagram-real (viral reference)

Sources:
- Viral reference: `gemini_pipeline/outputs/instagram-real_20260612T152106Z.md`
- Recreation: `gemini_pipeline/outputs/reel-1-pedro/final_20260612T173223Z.md`

Method: 7 dimension comparisons (hook, cut cadence/visuals, loops, audio, captions, structure/arc, ending/CTA), every claimed gap adversarially verified against both reports (56 confirmed, 0 rejected), plus a completeness pass (7 additional gaps). 63 total deviations.

---

## TL;DR

**The script is a near-perfect clone. The edit is not.** Loop architecture, micro-loop sequence, emotion beats, CTA mechanic, music role, and pre-term vocal pauses all match the viral formula 1:1. What was not copied is the **editing grammar** and the **timing grid** — and that's where the viral formula actually lives:

1. **The viral reel is a 16-shot hard-cut montage; yours is one continuous take.** 15 hard cuts in 24s, with 8 of 16 shots being *real software screencasts* (50% of the rotation). Yours has zero hard cuts and zero real screencasts — all visual change is overlays/punch-ins on the same talking-head shot.
2. **Everything in yours lands ~25–40% late.** Punch word: 0.7s (viral) vs 2.0s (yours). Hook end: 1.3s vs 2.5s. Core reveal: 5.8s vs 8.8s. CTA: 21.8s vs 27.0s. Runtime: 24.0s vs 30.0s.
3. **Caption grammar differs.** Viral: compressed 1–3 word white lowercase fragments, center-screen, new chunk every ~1.2s, including standalone caption swaps mid-shot. Yours: verbatim full sentences, below-chin, ALL-CAPS punch words, yellow/cyan coloring, red full-screen flash, gradient blocks, animated entries.
4. **The escalation engine was replaced.** Viral rapid-fires 4 stacked tactical tips at ~1.3s cadence (the "never feels finished" mechanic). Yours has one consequence beat + one 3.5s static asset hold.
5. **The ending isn't loopable.** Viral ends on a clean face frame matching frame 1 (seamless auto-replay into the hook), single ask, no end graphics, no music duck. Yours ends zoomed-in with badge + SEGUE animation, dual ask, music duck.

---

## The exact formula — retimed 24.0s grid for the re-edit

```
00:00.0  Headshot (locked, no punch-in) + caption "usa o claude code" — fast, emphatic VO from frame 1
         Small live terminal overlay top-left, visibly active within 0.5s (mute-proof signal)
00:00.7  CAPTION SWAP (no cut, no flash, no SFX): "da maneira errada"
00:01.3  HARD CUT → real terminal screencast, prompt being typed — "abre o terminal..."
00:02.3  CAPTION SWAP on held screencast — punchline "e rezam que corra bem" (sarcastic drop)
00:03.2  HARD CUT → third-party authority b-roll (Claude Code creator podcast clip, ~1.3s)
00:04.5  HARD CUT → headshot — pivot "explicou o oposto"
00:05.8  HARD CUT → FULL-FRAME graphic card "SECÇÃO 1: PLAN MODE" (speaker off-screen, hold 2.2s)
         Vocal micro-pause right before "plan mode". This cut IS the payoff moment.
00:07.1  CAPTION SWAP on held card — "não em execute mode" (standalone negation beat)
00:08.0  HARD CUT → slower-kinetic shot (terminal close-up recommended) — VO decelerates: "primeiro planeias"
00:09.5  HARD CUT → screencast: checklist/task UI executing — sharp snap on "executas"
00:11.0  HARD CUT → headshot — re-engage, open tip stack: "e não fica por aí"
00:12.5  HARD CUT → screencast: different color-theme terminal (tip 1)
00:13.8  HARD CUT → screencast: fast compilation output (tip 2) — rapid, exciting VO
00:14.8  HARD CUT → screencast: live checklist updating (tip 3)
00:16.0  HARD CUT → screencast: scrolling configs (tip 4)
00:17.4  HARD CUT → screencast: split chat UI — tip stack closes
00:18.8  HARD CUT → headshot — macro close: "não é só prompting" (high energy)
00:20.1  HARD CUT → screencast: real CLAUDE.md / terminal summary block —
         "como um [pause] co-fundador de sistema" (punchline beat, separate from macro close)
00:21.8  HARD CUT → headshot close-up — "comenta criador" (single ask, no follow prompt, no graphics)
00:23.0  CAPTION SWAP: "guia grátis" — last spoken word before the cut is "guia"
00:24.0  HARD END. No tail fade, no music duck, frame matches 00:00.0 framing → seamless rewatch loop.
```

Edit grammar rules (from the viral beat sheet — only two interrupt species exist):
- **Hard cuts and caption swaps. Nothing else.** No slides, pops, fades, camera-shake VFX, gesture beats, or animated text. Every graphic enters/exits on a single frame.
- **No full-frame source holds longer than ~2.0s.** Target true ASL 1.4s; first 6 seconds at ~1.15s.
- **Any shot held >1.5s gets a caption-only swap at its midpoint** (viral does this at 00:00.7, 00:02.3, 00:07.1, 00:23.0).
- **Captions: 1–3 word white lowercase fragments, center-screen, static (no tracking/animation), ~20 chunks over the runtime.** Emphasis = isolating the word in its own chunk timed to a vocal pre-pause — never color, caps, or size.
- **Audio: one flat ~115 BPM minor-key lo-fi synth bed at constant level start-to-cut.** Voice fast/compressed, zero dead air, micro-pause *before* "plan mode" and before "co-fundador".

---

## Decisions to make consciously (your reel "fixed" the viral video's own listed weaknesses)

The viral report lists exactly 3 weaknesses: no SFX, flat audio energy, generic stock b-roll at 00:08.0. Your reel deviates on all three *in the direction the viral analysis recommends*. Exact replication says revert; the evidence says these are upgrades. Decide per item:

| Your deviation | Exact formula says | Viral report's own verdict |
| --- | --- | --- |
| 5 SFX hits (pop, whoosh, ticks, clack, chime) | Remove all | Weakness #1: lack of SFX is exploitable — **keep (but sync within ~100ms of cuts)** |
| Chime on the reveal (frisson element) | Remove | Weakness #2: flat audio at the reveal is exploitable — **keep** |
| Real-footage replacement for the 00:08.0 stock-b-roll slot | Insert stock b-roll | Weakness #3: stock clip is the weakest shot — **use a terminal close-up instead** |
| Music duck −30% at CTA | Keep constant volume | Part of "flat audio" weakness, but the duck breaks the seamless audio loop — **lean revert** |
| In-body CLAUDE.md asset showcase | Reference guide only in CTA | The one element where you outscored the viral (Payoff 10/10 vs 8/10, drives Saves) — **keep, but as a real full-frame screencast at the 00:20.1 slot, not a 3.5s static mockup** |

Everything else (red flash, color captions, ALL-CAPS, end-screen graphics, dual ask, single-take overlay style, 30s runtime) is a deviation with no evidence in its favor — revert to the formula.

---

## What already matches (do not touch)

- Hook classification (contrarian myth-bust on the same behavior), voice + text from frame one, identical viewer question at hook end.
- Macro loop opens 00:00.0; **4 micro loops in the identical 1:1 sequence** (mistake → creator's secret → how plan mode works → escalation), micro-loop-1 closing on the same sarcastic "pray it works" punchline.
- Macro close at ~78–82% of runtime; lead-magnet loop opens at ~90% in both; comment-keyword → DM-funnel CTA mechanic; hard cut on the CTA with zero outro sag.
- Music bed role (ambient, minor-key, lo-fi, flat, not an editing driver), high-energy compressed voice, **pre-term micro-pause before "plan mode"**, beat-for-beat vocal emotion arc (sarcastic drop → authority shift → aggressive spike on the negative keyword → climactic close → command CTA).
- No emojis/ornament in captions; caption updates synced to phonetic transients; Problem → Agitate → Reveal skeleton.

---

## Full deviation list (63 items, verified)


### Critical impact

**1. Contrarian punch word timing**
- Viral: 'the wrong way' lands at 00:00.7 — punch delivered within the first second, while the scroll-stop decision is still being made (beat sheet row 00:00.7; Hook score justification cites it explicitly).
- Yours: 'ERRADA' lands at 00:02.0 — 1.3s later, nearly 3x the viral delay (beat sheet row 00:02.0; Hook Autopsy 'full-screen red flash text ERRADA at 00:02.0').
- Fix: Time-compress or re-record the opening sentence so the full contrarian line completes by ~00:01.3, and retime captions so the 'ERRADA' punch flashes at exactly 00:00.7. Practical edit: speed the 00:00.0–00:02.5 VO segment ~1.5x (or re-record at viral pace), then move the ERRADA caption event from 00:02.0 to 00:00.7.

**2. Hook end point / hook duration**
- Viral: Hook ends at 00:01.3, where it hard-cuts to a terminal screen share showing the common mistake ('They open it...' / 'type what').
- Yours: Hook ends at 00:02.5, with the 'Abre o terminal' beat not starting until 00:02.9 — and it cuts back to the same talking head instead of a screen share.
- Fix: Trim the hook to end at 00:01.3 (it currently runs to 00:02.5). At the new 00:01.3 hook exit, hard cut to a real terminal screen recording showing a prompt being typed (matching viral Cut 2 at 00:01.3), instead of the digital cut back to the same headshot at 00:02.9.

**3. Mute-proof opening visual (in-frame software activity)**
- Viral: Opening frame is speaker center frame WITH a code overlay top-left, and 'a background terminal UI element changes immediately within the first 00:00.5, signalling immediate activity' — a muted scroller sees live software in second one.
- Yours: Opening frame is a plain mid-shot holding a phone as microphone with no software UI anywhere; the first UI graphic only appears at 00:08.8, and the muted scroll-stopper (red flash) doesn't arrive until 00:02.0 — past the 0–1s scroll decision window.
- Fix: Composite a small live terminal/Claude Code screen-recording overlay in the top-left of the frame starting at 00:00.0, with visible state change (text streaming or command executing) within the first 0.5s, so the muted opening signals software activity exactly like the viral frame.

**4. Hard cuts vs. single continuous take (rotation mechanism)**
- Viral: 16 distinct full-frame shots joined by 15 hard cuts in 24.0s (beat sheet 00:01.3-00:21.8; Replication Spec enumerates 'Cut 1'-'Cut 16'). Full rotation pattern: Headshot(00:00.0) -> Screencast(00:01.3) -> B-roll(00:03.2) -> Headshot(00:04.5) -> Graphic card(00:05.8) -> B-roll(00:08.0) -> Screencast(00:09.5) -> Headshot(00:11.0) -> Screencast x5 (00:12.5, 00:13.8, 00:14.8, 00:16.0, 00:17.4) -> Headshot(00:18.8) -> Screencast(00:20.1) -> Headshot(00:21.8).
- Yours: Zero hard cuts. One continuous talking-head take for all 30.0s ('the physical footage is a single continuous take' - recreation Beat Sheet Analysis). All visual change is digital punch-ins/outs (00:01.0, 00:07.5, 00:14.0, 00:24.5), frame shifts (00:06.0, 00:02.9), a color flash (00:02.0), and graphic overlays (00:08.8, 00:11.0, 00:19.0, 00:27.0) layered on the same shot.
- Fix: Re-edit as a 16-shot, 15-hard-cut montage. Keep the talking head only in 5 anchor slots (00:00.0 hook, ~00:04.5 pivot, ~00:11.0 mid re-engage, ~00:18.8 synthesis, ~00:21.8 CTA, proportionally retimed) and hard-cut to full-frame non-headshot material in every gap, reproducing the viral pattern H->SR->BR->H->GFX->BR->SR->H->SR->SR->SR->SR->SR->H->SR->H.

**5. Real software screencast count (core source type)**
- Viral: 8 of 16 shots (50% of the rotation) are real screen recordings of actual software: terminal input 00:01.3, automation script executing 00:02.3, checklist UI ticking 00:09.5, red terminal config 00:12.5, code compilation 00:13.8, live checklist updating 00:14.8, scrolling terminal configs 00:16.0, split chat UI 00:17.4, terminal summary block 00:20.1. Viral Mute-Proofness 8/10 credits them: 'Screen recordings and text tell the whole story.'
- Yours: 0 real screencasts. The only 'software' visuals are static graphic mockups overlaid on the creator's chest: 3-step checklist pop-up at 00:11.0 and a CLAUDE.md UI mockup at 00:19.0. The recreation report itself lists this as Vulnerability #1: 'Lack of Real Software B-Roll... relies entirely on static graphical mockups.'
- Fix: Capture 8 distinct real Claude Code screen recordings and hard-cut to them full-frame at the retimed viral slots: terminal typing ~00:01.3, task checklist executing ~00:09.5, different color-theme terminal ~00:12.5, fast compilation output ~00:13.8, live checklist ~00:14.8, scrolling config ~00:16.0, split chat UI ~00:17.4, and the real CLAUDE.md file open in a terminal/editor ~00:20.1 (this last one replaces the 00:19.0 static mockup overlay).

**6. Average shot length (physical cut cadence)**
- Viral: ASL 1.41s overall (17 visual changes over 24.0s) and 1.16s during the opening 00:00.0-00:05.8; the full-frame source changes every 1.0-1.5 seconds throughout.
- Yours: ~4.5s ASL for physical framing shifts, and the true full-frame source never changes once across 30.0s; only the overlay-adjusted figure (~1.3s) approaches the viral number (recreation Beat Sheet Analysis).
- Fix: Cut so that no full-frame visual source persists longer than ~2.0s anywhere in the timeline. Target an overall true ASL of 1.4s, and front-load the first 6 seconds at ~1.15s ASL with full-frame changes at 00:00.0, 00:01.3, 00:03.2, 00:04.5, and 00:05.8.

**7. Rapid 4-shot screencast escalation run**
- Viral: 00:13.8-00:17.4: four consecutive hard cuts between distinct screen recordings at 1.0-1.4s intervals (00:13.8 compilation, 00:14.8 checklist, 00:16.0 scrolling configs, 00:17.4 split chat UI), fired immediately after the 'And that's not all' escalation line.
- Yours: The equivalent escalation section (00:17.2-00:22.5) is covered by one CLAUDE.md mockup overlay held for ~3.5s (00:19.0-00:22.5) over the unchanged talking-head take.
- Fix: Replace the single 3.5s mockup hold with a four-shot run of distinct full-frame real screencasts, one hard cut every 1.0-1.4s, starting right after the escalation line ('e não fica por aí', retimed to ~00:13.8) and ending ~00:17.4.

**8. Payoff moment placement**
- Viral: Biggest payoff lands at 00:05.8 (Plan Mode graphic reveal), ~24% into a 24.0s runtime; Section C 'Biggest Payoff Moment: 00:05.8'
- Yours: Peak payoff lands at 00:11.0-00:13.0 (3-step blueprint reveal), ~37% into a 30.0s runtime; the analogous 'PLAN MODE' concept panel doesn't even appear until 00:08.8
- Fix: Compress the segment 00:00.0-00:11.0 by ~5 seconds: tighten the mistake-agitation VO (00:02.9-00:08.8) so the 'O SEGREDO: PLAN MODE' panel slides in at ~00:05.8 and the 3-step blueprint pops within ~00:06-00:07, putting the payoff at ~24% of runtime like the viral.

**9. Hook voice pacing / negative-keyword landing time**
- Viral: Fast, emphasized delivery from frame one; the contrarian keyword 'the wrong way' lands at 00:00.7 and the whole hook is complete by 00:01.3
- Yours: 'Measured, confident' opening delivery; the contrarian keyword 'ERRADA' doesn't land until 00:02.0 and the hook only completes at 00:02.5
- Fix: Re-record or time-compress the opening VO line so it is delivered fast and emphasized, with 'ERRADA' hitting at ~00:00.7-00:01.0 and the full hook statement finished by 00:01.3 (currently nearly 2x slower than the viral).

**10. Verbatim captions vs compressed keyword fragments**
- Viral: Speech is COMPRESSED into 1–3 word high-impact fragments, ~20 text blocks over 24.0s (one new chunk every ~1.2s): 'use claude code' (00:00.0), 'the wrong way' (00:00.7), 'start in' (00:05.8), 'not build mode' (00:07.1), 'just prompting' (00:18.8), 'like a system' (00:20.1). Hook Autopsy: 'compresses them into high-impact fragments'; Section D: '2–3 words per phase'. Text changes also fill gaps between hard cuts.
- Yours: VERBATIM transcription of speech (Hook Autopsy: 'Verbatim Duplication'). Beat sheet shows full-sentence blocks: 'Ele diz que a maioria das sessões começa' (00:08.8, 8 words), 'estás a usar o Claude Code como um verdadeiro CO-FUNDADOR de sistema' (00:24.5, 11 words), 'comenta CRIADOR e recebes o guia completo' (00:27.0, 7 words). Only ~17 blocks over 30s with holds up to 3.5s (00:19.0→00:22.5), despite Section D claiming '2–4 words maximum'.
- Fix: Rebuild the entire caption track as 1–3 word keyword fragments with a new chunk every ~1.0–1.4s (~20+ blocks over 30s). Concretely: 00:00.0 'usa o Claude Code' → 00:00.7 'da forma errada'; 00:08.8 split 'Ele diz que a maioria das sessões começa' into 'a maioria' → 'das sessões'; 00:24.5 reduce the 11-word line to 'como co-fundador'; 00:27.0 split CTA into 'comenta criador' → 'guia completo' (mirroring viral's 00:21.8 'creator' → 00:23.0 'free guide'). Use mid-cut text changes to fill gaps between cuts, as viral does at 00:00.7, 00:02.3, 00:07.1, 00:23.0.

**11. Core reveal landing point**
- Viral: Plan Mode reveal graphic lands at 00:05.8 - 24.2% into a 24.0s runtime - and the report names it the single biggest payoff moment.
- Yours: PLAN MODE panel slides in at 00:08.8 - 29.3% into a 30.0s runtime - 3.0s later in absolute terms and ~5 points later proportionally; the Clarity segment of the emotion arc does not even start until 00:11.0 (37% in) vs viral 00:05.8 (24% in).
- Fix: Re-time the front half so the PLAN MODE panel hits at 00:05.8: trim the problem statement to end by 00:01.3, the agitation list to end by 00:03.2, and the authority line ('mas o gajo que criou o Claude Code... explicou o oposto') to run 00:03.2-00:05.8, so the panel slide-in lands exactly at 00:05.8.

**12. Total runtime budget**
- Viral: 24.0s total; hard cut at 00:24.0 designed for seamless rewatch loop back to the hook headshot.
- Yours: 30.0s total (hard cut at 00:30.0) - 25% longer. The extra 6.0s decomposes as: +1.6s problem (00:00.0-00:02.9 vs 1.3s), +1.2s agitate (00:02.9-00:06.0 vs 1.9s), +0.2s authority pivot, +0.7s consequence/asset block (00:14.0-00:22.5 = 8.5s vs viral escalation 7.8s), +1.5s synthesis (00:22.5-00:27.0 = 4.5s vs 3.0s), +0.8s CTA (3.0s vs 2.2s).
- Fix: Cut the edit from 30.0s to 24.0s using the viral phase map as the timing grid: problem 00:00.0-00:01.3, agitate 00:01.3-00:03.2, authority 00:03.2-00:05.8, reveal/clarity 00:05.8-00:11.0, escalation 00:11.0-00:18.8, synthesis 00:18.8-00:21.8, CTA 00:21.8-00:24.0. Biggest single trims: synthesis -1.5s (tighten 00:22.5-00:27.0 to 3.0s), problem -1.6s, agitate -1.2s, CTA -0.8s.

**13. Reveal-segment arousal level (arc shape inversion)**
- Viral: The reveal segment 00:05.8-00:11.0 is 'Clarity / Enlightenment - HIGH arousal'; the arc shape is HIGH -> low-mid -> HIGH -> mid -> HIGH (triple peak, reveal is the second peak).
- Yours: The equivalent Clarity segment 00:11-00:17 is explicitly 'Low Arousal'; the arc shape is HIGH -> mid -> LOW -> HIGH -> mid - the reveal sits in an arousal valley instead of a peak, and the overall arc has one fewer high-arousal peak.
- Fix: Raise arousal across the blueprint walkthrough (currently 00:11.0-00:14.0; 00:05.8-00:11.0 after re-timing): push vocal energy/pace back up to the hook's level, and add a visual state change roughly every 1.3s through the 3-step list instead of holding one static overlay, so the reveal segment plays as a HIGH-arousal enlightenment peak like viral 00:05.8-00:11.0.

**14. Escalation engine: stacked tips vs single consequence + asset**
- Viral: After the reveal segment, micro loop 4 (00:11.0-00:17.4) rapid-fires FOUR secondary tactical tips at ~1.2-1.4s cadence (cuts at 00:12.5, 00:14.8, 00:16.0, 00:17.4); the report credits this with ensuring 'the viewer never feels they have consumed all the information until the end.'
- Yours: Replaces the tip-stack with one consequence/warning beat ('resultados CAOTICOS' 00:14.0-00:17.2) plus one long asset showcase (CLAUDE.md overlay 00:19.0-00:22.5) - a single 'but wait, there's more' loop instead of four stacked value beats.
- Fix: Rebuild 00:14.0-00:22.5 (retimed to 00:11.0-00:18.8) as a rapid escalation stack: open a micro-loop from a headshot beat at 00:11.0 ('e nao fica por ai'), then deliver 3-4 distinct secondary tactical tips at ~1.3-1.4s each (target cut points 00:12.5, 00:14.8, 00:16.0, 00:17.4), closing the stack at 00:17.4 before the synthesis at 00:18.8.

**15. End-screen graphics**
- Viral: No end-screen graphics at all. Final segment (00:21.8–00:24.0) is a clean presenter headshot close-up with only the subtitle text; the video hard-stops on the face frame (Section D, replication spec 00:24.0).
- Yours: Instagram 'CRIADOR' badge and 'SEGUE' mouse-cursor click animation pop up as an end-screen graphic overlay at 00:27.0 and persist until the cut at 00:30.0 (beat sheet 00:27.0, replication spec 00:27.0 'Slide up actionable platform native graphic assets').
- Fix: Delete the CRIADOR badge and SEGUE cursor-click animation overlays from 00:27.0–00:30.0. The final 3 seconds should be a clean talking-head frame with caption text only, exactly like the viral's Cut 16.

**16. Loopability back to frame 1 (rewatch loop)**
- Viral: Ending engineered as a rewatch loop: 'transitioning from the final face frame straight back to the hook headshot' (Section D); replication spec 00:24.0 specifies 'seamless loop back to Cut 1'. Last frame visually matches first frame.
- Yours: Last frame at 00:30.0 carries graphic overlays (badge + cursor animation) and is in a punched-in zoom state from the 00:24.5 'abrupt 20% digital camera zoom'; frame 1 (00:00.0) is a clean mid-shot holding phone. The visual discontinuity breaks the seamless loop back to the hook.
- Fix: At ~00:29.0–00:30.0, punch the digital zoom back out to the 00:00.0 baseline framing/scale and remove all overlays so the final frame visually matches frame 1, making the Instagram auto-replay read as a seamless loop into the hook.

**17. Reveal delivered as full-frame graphic takeover vs partial side-panel overlay** *(completeness pass)*
- Viral: The core reveal at 00:05.8 is a HARD CUT to a full-frame stylized graphic — 'UI Graphic: "Section 1 Plan Mode" 3D card' occupies the entire frame as its own shot (Cut 5: 'Custom Graphic Card Reveal'); the speaker leaves the screen entirely. The viral report names this its #1 strategic decision: 'Shifting from raw software UI to a clean 3D graphic block isolated the core concept and signaled a premium, structured insight [Prediction Error / Orienting Response].'
- Yours: The reveal at 00:08.8 is a 'Sleek cyan panel slides in' — a partial overlay placed 'into the empty screen space next to speaker' (replication spec 00:08.8) while the talking head stays on screen; the follow-up checklist at 00:11.0 likewise 'pops up over left chest'. The concept never gets an isolated full-frame moment.
- Fix: At the reveal beat (00:05.8 once retimed per the timing fixes), replace the side-panel slide-in with a hard cut to a full-frame stylized 3D framework card that fills the entire frame with the speaker fully off-screen; hold it ~2.2s (matching viral 00:05.8–00:08.0), then hard-cut back. Do not composite the reveal graphic over the talking-head shot.


### Moderate impact

**18. Opening voice pace**
- Viral: Fast, emphasized delivery from frame one ('Fast, emphasized "Most people"' at 00:00.0; replication spec: 'Rapid, high-volume delivery') — the entire contrarian sentence fits in 1.3s.
- Yours: Measured, confident pace at 00:00.0 ('Measured, confident. Accent on "maior"'), stretching the same sentence across 2.5s.
- Fix: Re-record the 00:00.0–00:02.5 opening line at a fast, high-energy clip with hard emphasis on 'maior parte', so the sentence resolves in ~1.3s. This is the root-cause fix that enables the punch-word and hook-end retimings above.

**19. Caption compression and change cadence**
- Viral: Two compressed keyword-fragment blocks in 1.3s: 'use claude code' at 00:00.0 → 'the wrong way' at 00:00.7. Text 'compresses [speech] into high-impact fragments' and deliberately skips filler words like 'Most people'.
- Yours: Three verbatim blocks across 2.5s: 'A maior parte das pessoas' at 00:00.0 → 'usa o Claude Code' at 00:01.0 → 'ERRADA' at 00:02.0. Report classifies it as 'Verbatim Duplication'.
- Fix: Reduce to two caption blocks: Block A 'usa o Claude Code' at 00:00.0, Block B 'da maneira ERRADA' at 00:00.7. Drop the 'A maior parte das pessoas' caption entirely (keep it in VO only), matching viral's keyword-compression style where text skips the subject phrase.

**20. Punch delivery mechanism (text change vs full-frame flash)**
- Viral: Punch lands via an in-place caption swap with NO cut, NO frame filter, NO motion — beat sheet 00:00.7 cut type is 'None (Text change)'; the static frame lets the text alone fire the orienting response.
- Yours: Punch lands via a 'violent full-screen crimson filter' flash-frame transition at 00:02.0 ('Full screen turns stark red overlay', 'Flash frame transition').
- Fix: For exact replication, replace the full-screen red flash at the punch moment with a static-frame caption change: keep the same headshot frame and grading, and swap to high-contrast bold text 'da maneira ERRADA' at the retimed 00:00.7 — no overlay filter, no transition.

**21. Third-party authority b-roll shot**
- Viral: Hard cut at 00:03.2 to a podcast clip of the Claude Code creator - real third-party authority footage occupying its own ~1.3s full-frame shot ('Introduce authority figure to validate claim').
- Yours: The authority claim ('mas o gajo que criou o Claude Code', 00:06.0) is delivered on the same talking-head take with only a positional frame reset; no third-party footage appears anywhere in 00:00-00:30.
- Fix: On the authority line (retimed to ~00:03.2), hard-cut to ~1.3s of real third-party footage of the Claude Code creator (podcast/interview clip), then hard-cut back to the headshot for the pivot phrase at ~00:04.5.

**22. Total runtime and stretched beat grid**
- Viral: 24.0s total runtime; core-concept graphic lands at 00:05.8, escalation montage starts 00:13.8, CTA begins 00:21.8, hard end at 00:24.0.
- Yours: 30.0s total (25% longer); the same structural beats land late: concept graphic at 00:08.8, escalation at 00:17.2, CTA at 00:27.0, end at 00:30.0.
- Fix: Trim the edit to 24.0s: compress voiceover pauses and dead frames so the core-concept reveal lands at ~00:05.8, the escalation run begins at ~00:13.8, the CTA starts at ~00:21.8, and the file hard-ends at exactly 00:24.0.

**23. Graphic-overlay over-rotation (source-type proportions)**
- Viral: Exactly 1 stylized graphic shot in the entire rotation - the 'Section 1 Plan Mode' 3D card, 00:05.8-00:08.0 (~2.2s, 1 of 16 shots, ~6%); every other non-headshot visual is real footage (screencast or b-roll).
- Yours: Graphics carry nearly the entire interrupt load: red full-screen flash 00:02.0, cyan panel 00:08.8, 3-step checklist pop-up 00:11.0, red/pink gradient text block 00:15.5, CLAUDE.md mockup 00:19.0, end-screen badge animation 00:27.0 - roughly 6 graphic events vs. 0 real-footage inserts.
- Fix: Keep exactly one stylized graphic card - the Plan Mode reveal - as its own full-frame ~2.2s shot retimed to 00:05.8. Convert the 00:11.0 checklist and 00:19.0 CLAUDE.md overlays into real full-frame screencasts (see screencast fix), and drop the 00:15.5 gradient block in favor of a screencast cut, so real footage carries the rotation as in the viral mix (8 screencasts : 2 b-roll : 1 graphic).

**24. Micro loop 4 leak (unclosed loop)**
- Viral: All four micro loops are explicitly closed before the macro close — micro loop 4 closes at 00:17.4, macro closes at 00:18.8; report states 'No leak present' and 'zero informational leaks' (Loop Management 9/10)
- Yours: Micro loop 4 ('What is the shortcut tool?') opens at 00:17.2 and is never marked closed; the CLAUDE.md reveal at 00:19.0 and its fade-out at 00:22.5 are both 'None' in the loop column, so the loop dangles into the macro close at 00:24.5
- Fix: Re-edit the 00:19.0 beat so the CLAUDE.md overlay explicitly resolves micro loop 4: on-screen text and voice should name the file as THE shortcut ('este é o atalho: um ficheiro CLAUDE.md') the instant the panel slides in, and treat 00:22.5 (panel fade-out) as the hard close — every micro loop must be closed before the macro close at 00:24.5, mirroring viral 00:17.4 < 00:18.8

**25. Micro loop 2 -> 3 chaining broken**
- Viral: Closing one loop opens the next on the SAME beat: micro loop 2 closes and micro loop 3 opens simultaneously at 00:05.8 (single beat row: 'Micro loop 2 closed / Micro loop 3 open' on the Plan Mode card reveal)
- Yours: Micro loop 2 closes at 00:08.8 (PLAN MODE panel) but micro loop 3 does not open until 00:11.0 (3-step checklist) — a 2.2s window with zero open micro loops; the report's prose claims it 'instantly spawns' the next loop but its own beat sheet contradicts this
- Fix: Move the micro loop 3 opener to 00:08.8: as the 'O SEGREDO: PLAN MODE' panel slides in, immediately add a tease line ('e funciona em 3 passos...') in voice + caption so the how-does-it-work question opens on the same beat the secret is revealed, then pay it off with the checklist at 00:11.0

**26. Micro loop 3 -> 4 gap doubled**
- Viral: Gap between micro loop 3 close (00:09.5) and micro loop 4 open (00:11.0) is 1.5 seconds
- Yours: Gap between micro loop 3 close (00:14.0) and micro loop 4 open (00:17.2) is 3.2 seconds, filled by the unanchored CAOTICOS agitation beat at 00:15.5 — the longest open-loop vacuum in either edit
- Fix: Pull the micro loop 4 opener ('e não fica por aí') forward from 00:17.2 to ~00:15.5, overlapping or immediately following the CAOTICOS beat, so the no-open-loop window shrinks to <=1.5s to match the viral cadence

**27. Rewatch loop (seamless loop-back to hook) missing**
- Viral: Ending is engineered as a rewatch loop: final frame at 00:24.0 is the speaker's face that transitions 'straight back to the hook headshot'; replication spec specifies 'seamless loop back to Cut 1' with no tail
- Yours: From 00:27.0 to the 00:30.0 blackout the frame is covered by end-screen graphics (Instagram CRIADOR badge + SEGUE cursor click animation); the report describes only an 'AUDIOVISUAL BLACKOUT: Instant timeline cut' with no loop-back design — auto-replay lands on graphics, not a frame matching the 00:00.0 hook
- Fix: Remove or fade out the CRIADOR badge and SEGUE cursor animation by ~00:29.3 so the final ~0.7s ends on a clean mid-shot of the creator framed identically to 00:00.0, making Instagram's auto-replay read as a seamless loop back into the hook

**28. SFX presence** *(viral-weakness — see decision table)*
- Viral: Zero SFX anywhere: every beat-sheet row 00:00.0-00:23.0 shows 'None'; Section B explicitly states 'Dedicated SFX drops are not utilized'
- Yours: Five SFX hits layered in: impact pop at 00:02.0, UI whoosh at 00:08.8, UI tick sounds at 00:11.0, keyboard clack at 00:19.0, digital click chime at 00:27.0 (all [INFERRED])
- Fix: To match the viral formula exactly, mute/delete all five SFX layers (00:02.0 pop, 00:08.8 whoosh, 00:11.0 ticks, 00:19.0 clack, 00:27.0 chime) so the only audio is voice + flat music bed. Note: the viral report's Weakness #1 ('Complete Lack of SFX') says adding precise SFX is the exploit, so this deviation may be intentionally better.

**29. End-of-video music behavior at CTA**
- Viral: Music stays continuous and flat at full level through the CTA (00:21.8-00:23.0 rows show 'Continuous') all the way to the hard cut at 00:24.0; Section C: 'no structural drops... or moments of total silence'
- Yours: Track volume drops at the CTA: beat sheet 00:27.0 'Track volume drops slightly'; replication spec 00:27.0 'Drop background music volume level by 30%'
- Fix: Remove the ~30% music volume duck at 00:27.0; keep the music bed at its constant body-level volume through the entire CTA until the instant hard cut at 00:30.0, so the ending audio is indistinguishable from the body (supports the seamless rewatch loop).

**30. Full-screen red flash word at hook**
- Viral: Hook punctuation is a plain white caption change — 'the wrong way' at 00:00.7 — with no color overlay or frame takeover; the scroll-stop comes from text speed plus a hard cut to a terminal screen at 00:01.3. Section D confirms no color gimmicks; Captions score 9/10 for 'minimal cognitive friction'.
- Yours: Full-screen stark red overlay with massive bold single word 'ERRADA' at 00:02.0 ('Flash frame transition', 'full-screen red flash'); replication spec codifies it as 'FRAME FLASH INTERRUPT... massive, bold single keyword'. The negative keyword also lands ~1.3s later than viral's (00:02.0 vs 00:00.7).
- Fix: At 00:02.0, delete the full-frame red overlay and oversized word treatment. Render 'errada' as a standard white caption chunk in the normal caption position, move the negative-keyword text change earlier to ~00:00.7, and follow it with a hard cut to a real screen recording at ~00:01.3 — exactly the viral mechanic.

**31. Yellow/cyan keyword coloring**
- Viral: Uniform clean white text throughout; key technical terms are emphasized by ISOLATION — the word gets its own standalone chunk timed to a vocal pause (e.g., 'start in' 00:05.8 → 'not build mode' 00:07.1). No color emphasis anywhere (Section D, Captions 9/10).
- Yours: Section D: 'Heavy keyword signaling is achieved by changing specific tech terms into branded system colors (Yellow/Cyan)'; replication spec 00:06.0: 'Highlight authoritative target nouns using contrasting yellow/neon font variations'. Applied around 00:06.0–00:11.0 (e.g., PLAN MODE region).
- Fix: Strip all yellow/cyan font color styling from the caption layer (notably in the 00:06.0–00:11.0 segment). Recolor every caption to the same white. Emphasize key terms instead by giving each its own standalone 1–2 word chunk synced to the pre-term vocal pause, copying viral's 00:05.8/00:07.1 isolation pattern.

**32. Red/pink gradient text block on negative keyword**
- Viral: The analogous 'messy results' beat (00:12.5) uses a plain white caption chunk; the red in that moment comes from the B-ROLL (a 'Red-themed terminal config screen'), never from the caption styling itself.
- Yours: At 00:15.5 the caption text itself 'changes to a glaring red/pink gradient block' on 'a maioria recebe resultados CAÓTICOS'; replication spec 00:14.0 codifies 'negative-consequence keywords highlighted in block gradients'.
- Fix: At 00:15.5, remove the red/pink gradient block styling and render 'resultados caóticos' as a plain white chunk (or just 'caóticos' as an isolated chunk). If red is desired on this beat, cut to a red-themed screen recording behind the white text, as viral does at 00:12.5 — color belongs to the visual source, not the caption layer.

**33. Problem-phase duration**
- Viral: Problem statement is complete and agitation begins at 00:01.3 ('They open it...' transition; hook end point 00:01.3).
- Yours: Problem statement runs until 00:02.9 (hook end point declared at 00:02.5, 'Abre o terminal' agitation cut at 00:02.9) - 1.6s longer in the steepest retention-decay zone of the video.
- Fix: Compress the spoken line 'A maior parte das pessoas usa o Claude Code [de forma] ERRADA' (00:00.0-00:02.9) to finish by 00:01.3 - use a tighter take or 10-15% speed-up - so the agitation beat ('Abre o terminal') starts at 00:01.3.

**34. Agitate-to-authority pivot timing**
- Viral: Authority figure (clip of the Claude Code creator) enters at 00:03.2, only 1.9s after agitation starts; pivot phrase 'the opposite' at 00:04.5.
- Yours: Authority line 'mas o gajo que criou o Claude Code' enters at 00:06.0 - 2.8s later than viral - with 'explicou o oposto' at 00:07.5 vs viral 00:04.5.
- Fix: Tighten the agitation list (00:02.9-00:05.0: 'Abre o terminal / escrevem o que querem / e rezam que corra bem') to a 1.9s read so the authority beat starts at 00:03.2 and the 'oposto' pivot lands at 00:04.5.

**35. Reveal and peak payoff unified vs split**
- Viral: The biggest payoff moment IS the reveal cut itself: 00:05.8, the hard cut to the 'Plan Mode' card resolves the hook tension in one beat.
- Yours: The reveal panel appears at 00:08.8 but the report places the Peak Payoff Moment at 00:11.0-00:13.0 (the 3-step Planeias/Avalias/Executas checklist) - payoff energy is deferred 2.2s past the reveal, splitting one moment into two.
- Fix: Stage the PLAN MODE panel as the payoff itself: make the 00:08.8 slide-in (retimed to 00:05.8) the visual climax (full-attention cut, biggest graphic, vocal pre-pause then emphasis), and treat the 3-step checklist at 00:11.0 as the start of the execution/clarity stretch rather than the headline moment - matching viral where reveal beat = payoff beat.

**36. Final-segment arousal at CTA**
- Viral: The last emotion segment 00:18.8-00:24.0 (Empowerment/Desire) holds HIGH arousal all the way through the CTA to the hard cut at 00:24.0.
- Yours: Arousal drops for the tail: Empowerment/Desire HIGH ends at 00:26, then 00:26-00:30 'Urgency/Action' falls to MID arousal for the CTA itself.
- Fix: Keep the climactic delivery energy from the 00:24.5 punch-in running unchanged through the CTA read at 00:27.0-00:30.0 (retimed 00:21.8-00:24.0) - same pace, same volume, direct command tone - so the final segment stays HIGH arousal to the last frame like viral 00:18.8-00:24.0.

**37. Single-ask vs dual-ask CTA**
- Viral: One single conversion ask in the tail: comment CREATOR to get the guide (00:21.8–00:24.0). No follow prompt anywhere in the ending.
- Yours: Two simultaneous asks at 00:27.0: the spoken/written comment ask ('comenta CRIADOR') plus a visual follow ask via the 'SEGUE' cursor-click animation, splitting the viewer's single conversion action.
- Fix: Remove the SEGUE follow animation at 00:27.0; keep only the comment-CRIADOR ask so 100% of end-of-video intent funnels into the comment trigger, as in the viral.

**38. Two-beat CTA caption structure**
- Viral: CTA is split into two text beats: action-word beat 'creator' at 00:21.8 (Lead magnet loop open), then a separate subtitle change to the value incentive 'free guide' at 00:23.0 (Lead magnet loop closed), keeping a text-change interrupt firing ~1 second before end of file.
- Yours: Single combined caption beat at 00:27.0 ('comenta CRIADOR e recebes o guia completo') with no further on-screen text change during the final 3.0 seconds (last text event in beat sheet is 00:27.0).
- Fix: Split the CTA caption into two beats: show 'comenta CRIADOR' at 00:27.0, then change the caption to the incentive/asset name ('guia gratuito') at ~00:28.3, mirroring the viral's 00:21.8 → 00:23.0 two-beat cadence so a text interrupt still fires in the final ~1.5s.

**39. Animated overlay transitions (slide/pop/fade) vs instant-only edit grammar** *(completeness pass)*
- Viral: Every visual change in the viral edit is instantaneous: the cut-type column contains only 'Hard cut', 'Direct cut', or 'None (Text change)' across all 20 rows (00:00.0–00:23.0); zero slide-ins, pop-ups, or fades anywhere, and the spec ends with 'No tail fade' (E.4, 00:24.0).
- Yours: Graphics enter and exit with eased animations: 'Slide UI Graphic' at 00:08.8, 'Pop-up overlay' at 00:11.0, 'Fade out' of the CLAUDE.md window at 00:22.5, and 'Slide up actionable platform native graphic assets' at 00:27.0 (beat sheet + replication spec). The 00:22.5 fade is the only fade in either video.
- Fix: Make all graphic entries/exits single-frame instant events: cut the 00:08.8 panel and 00:11.0 checklist in on one frame (no slide/pop animation), remove the 00:22.5 fade-out and replace it with an instant removal or hard cut, and pop the 00:27.0 CTA graphics in instantly (if kept at all — the team's fix already removes end-screen graphics).

**40. Standalone mid-hold caption-swap interrupts on held shots** *(completeness pass)*
- Viral: Four beat rows are pure text-change interrupts fired while the shot HOLDS — cut type 'None (Text change)' at 00:00.7, 00:02.3 ('for the best' on the held automation-script screencast), 00:07.1 ('not build mode' splitting the 2.2s Plan Mode card hold), and 00:23.0. The pattern note states this is deliberate: 'Text changes fill the gaps between hard cuts to keep the text-based orienting response continuously firing.'
- Yours: Zero standalone caption-swap interrupts: every text update in the beat sheet rides on a simultaneous kinetic/graphic event (punch-in 00:01.0, flash 00:02.0, gesture 00:03.9, shake 00:05.0, slide 00:08.8, pop 00:11.0, etc.), and during the longest holds the caption freezes too — no text change between 00:11.0 and 00:14.0 (3.0s) or between 00:19.0 and 00:22.5 (3.5s).
- Fix: Decouple the two interrupt channels: any shot or graphic held longer than ~1.5s must get a caption-only swap at its midpoint with no accompanying motion — e.g., split the 00:19.0–00:22.5 caption into two fragments with a swap at ~00:20.7, and split the 00:11.0–00:14.0 block with a swap at ~00:12.5. After the team's hard cuts are added, alternate cut-interrupt / text-interrupt as in the viral rows 00:01.3→00:02.3 and 00:05.8→00:07.1.


### Minor impact

**41. SFX on the punch word** *(viral-weakness — see decision table)*
- Viral: No SFX anywhere in the hook (SFX column 'None' at 00:00.0 and 00:00.7); the viral report's Weakness #1 explicitly flags 'Complete Lack of SFX' as a flaw a competitor could exploit.
- Yours: An 'Impact pop [INFERRED]' SFX accompanies 'ERRADA' at 00:02.0.
- Fix: For an exact copy of the viral formula, delete the impact pop SFX at the punch moment so the cut is acoustically silent like the viral's 00:00.7 text change. Note: the viral analysis itself flags SFX absence as the viral video's #1 weakness, so retaining the pop is a deliberate improvement — decide consciously rather than by accident.

**42. Camera motion inside the hook**
- Viral: Frame is fully static from 00:00.0 to the hook-end hard cut at 00:01.3 — the only interrupts are text changes (cut type 'None (Text change)' at 00:00.7).
- Yours: A 'slight digital punch-in' (kinetic scaling) fires at 00:01.0, adding a motion interrupt the viral hook does not have.
- Fix: Remove the digital punch-in at 00:01.0 and keep the frame locked from 00:00.0 until the hook-end hard cut, letting caption changes carry all interrupts inside the hook as the viral does.

**43. Contextual stock b-roll at the pacing downshift** *(viral-weakness — see decision table)*
- Viral: Hard cut at 00:08.0 to stock b-roll (man thinking at a desk in a library), timed to the deliberately slowed 'Slows down first' vocal beat. The viral report's own Weakness #3 flags this clip as out of place and recommends a terminal close-up instead.
- Yours: No b-roll at the corresponding pacing-downshift beat; 00:14.0 is just a digital punch-out on the same continuous take.
- Fix: For an exact formula copy, insert ~1.5s of slow-kinetic b-roll at the retimed ~00:08.0 slot. Since the viral analysis flags this exact clip as its weakest shot, the better-than-source option it recommends is a close-up screencast of a terminal command executing in the same slot - either way, a dedicated full-frame shot must fill this position.

**44. Final proof screencast before the CTA**
- Viral: 00:20.1: hard cut to a screen recording (multi-line terminal summary block) inserted between the synthesis headshot (00:18.8) and the CTA headshot (00:21.8) as a final conceptual proof shot.
- Yours: Goes directly from the climactic punch-in on the creator's face (00:24.5) to the CTA end-screen graphics (00:27.0) with no intervening proof shot.
- Fix: Insert a ~1.7s full-frame screencast of a terminal summary/result block between the climax line and the CTA headshot (retimed slot ~00:20.1-00:21.8).

**45. First micro loop opens late and runs long**
- Viral: Micro loop 1 opens at 00:01.3 (5.4% of runtime, the instant the hook ends) and closes at 00:02.3 — a 1.0s open-to-punchline turnaround
- Yours: Micro loop 1 opens at 00:02.9 (9.7% of runtime) and closes at 00:05.0 — a 2.1s turnaround, more than double the viral duration even after adjusting for the 30s vs 24s runtime
- Fix: Tighten the hook so 'Abre o terminal' (micro loop 1 open) lands by ~00:01.8-02.0, and compress the three-item mistake list so the punchline 'rezam que corra bem' closes the loop within ~1.0-1.3s of opening (target close ~00:03.0-03.3)

**46. Lead magnet loop never closes**
- Viral: Lead magnet loop is a two-beat open/close pair: opens 00:21.8 on the command ('Comment CREATOR') and explicitly closes 00:23.0 on a separate text beat naming the incentive ('free guide'), 1.0s before end of file
- Yours: Interaction loop opens at 00:27.0 with command and incentive merged into a single beat ('comenta CRIADOR e recebes o guia completo') and is never marked closed before the 00:30.0 cut — one beat held for 3.0s instead of the viral two-beat structure
- Fix: Split the CTA into two beats: 00:27.0 caption/voice = 'comenta CRIADOR' (loop open), then ~00:28.5 a separate caption change isolating the incentive ('guia completo gratis') as the loop close, ending the file ~1.0s after the close like the viral 00:23.0 -> 00:24.0

**47. Macro close merged with punchline beat**
- Viral: Macro loop closes at 00:18.8 on the synthesis line ('just prompting'), then a SEPARATE conceptual punchline beat lands at 00:20.1 ('like a system') before the CTA — close first, punchline second
- Yours: The synthesis line ('não estás só a fazer melhores prompts') at 00:22.5 carries no loop event, and the macro close is merged with the punchline ('CO-FUNDADOR') in a single beat at 00:24.5 — one beat doing two jobs
- Fix: Restructure the ending into two beats like the viral: close the macro at ~00:22.5-23.5 on the synthesis line (mark it with a cut or punch-in so it reads as resolution), then deliver 'CO-FUNDADOR de sistema' as a standalone punchline beat at ~00:24.5-25.0 before the CTA at 00:27.0

**48. Music bed BPM and style**
- Viral: ~115 BPM lo-fi ELECTRONIC SYNTH PULSE [INFERRED], Section C, running 00:00.0-00:24.0
- Yours: ~95 BPM HIP-HOP lo-fi DRUM PATTERN [INFERRED], Section C, running 00:00.0-00:30.0
- Fix: Swap the music bed for a mid-tempo lo-fi electronic synth-pulse track at ~115 BPM, minor key, with a completely flat arrangement (no drops/risers), laid under the full runtime at constant level.

**49. Frisson stack on the payoff reveal** *(viral-weakness — see decision table)*
- Viral: Payoff at 00:05.8 is PURELY VISUAL; Section C: only 'Visual reveal' present, all audio frisson elements absent ('The audio track remains completely static')
- Yours: Payoff at 00:11.0-00:13.0 fires a 'new sound entering' frisson element (interface pop/chime [INFERRED]) together with the visual reveal; Section C lists 'New sound entering: Present' and 'Fired together on visual reveal: Present'
- Fix: To match exactly, remove the interface pop/chime under the 3-step panel reveal at 00:11.0 so the payoff is carried by visuals alone over static audio. Note: the viral report's Weakness #2 ('Flat Audio Energy') recommends exactly this kind of audio accent at the reveal, so this deviation may be intentionally better.

**50. Second pre-term micro-pause placement**
- Viral: Second micro-pause is placed before the climactic framework-synthesis term: '...using Claude Code [pause] like a system' at 00:20.1 (Section C and Strategic Decision #2)
- Yours: Second micro-pause is placed before the negative agitation word 'CAOTICOS' at 00:16.0; no pause is reported before the climactic framework term 'CO-FUNDADOR de sistema' at 00:24.5
- Fix: Add a tiny breath/micro-pause immediately before 'CO-FUNDADOR' in the climax line at 00:24.5 (e.g. '...como um verdadeiro [pause] CO-FUNDADOR de sistema'), mirroring the viral's pause before 'like a system' at 00:20.1.

**51. All-caps bold emphasis words**
- Viral: Lowercase/sentence-case fragments throughout, including the CTA keyword — 'use claude code' (00:00.0), 'the wrong way' (00:00.7), 'creator' (00:21.8), 'free guide' (00:23.0). No capitalization-based emphasis.
- Yours: Repeated bold all-caps emphasis words: 'ERRADA' (00:02.0), 'CAÓTICOS' (00:15.5), 'CO-FUNDADOR' (00:24.5), 'CRIADOR' (00:27.0); replication spec 00:24.5 prescribes 'large capitalized bold lettering'.
- Fix: Recase 'ERRADA' (00:02.0), 'CAÓTICOS' (00:15.5), 'CO-FUNDADOR' (00:24.5) and 'CRIADOR' (00:27.0) to the same lowercase/sentence case and weight as the rest of the caption track; let chunk isolation and the vocal spike carry the emphasis, as viral does with lowercase 'creator' at 00:21.8.

**52. Caption placement**
- Viral: Center-screen keyword chunking (Section D: 'Uses center-screen keyword chunking'), keeping the text in the dead-center attention zone across all visual source types.
- Yours: Captions anchored 'right below the chin line' (Section D) / 'center-low alignment' (replication spec 00:00.0); the recreation's own scorecard dings this — Captions 8/10: 'position stays a bit static'.
- Fix: Move the caption anchor from below-chin/center-low up to true center-screen for the entire 00:00.0–00:30.0 runtime, matching viral's center-screen placement.

**53. Language and caption word economy**
- Viral: All-English captions whose fragments are inherently short ('type what' 00:01.3, 'for the best' 00:02.3, 'own work' 00:16.0), with zero connective filler words on screen.
- Yours: European Portuguese captions that retain connectives and filler because they are verbatim: 'Portanto, não estás só a fazer melhores prompts,' (00:22.5), 'e rezam que corra bem.' (00:05.0). Portuguese phrasing runs longer, inflating chunk size beyond the viral 2–3 word spec. (English tech terms like 'PLAN MODE', 'execute mode', 'CLAUDE.md' are already kept, which helps.)
- Fix: Keep Portuguese for the target audience, but compress harder than the English original to hit the 2–3 word target: cut connectives/articles from the caption layer (e.g., 00:22.5 'Portanto, não estás só a fazer melhores prompts' → 'não é só prompting', mirroring viral's 00:18.8 'just prompting'), and keep the English tech terms as the standalone keyword chunks.

**54. Payoff-vs-promise relationship**
- Viral: Section D: 'Matches.' The hook promises a usage correction and the body delivers exactly that - operational guidelines, no extra asset shown in-body; the 'free guide' is mentioned only inside the CTA at 00:23.0 (scored 8/10).
- Yours: Section D: 'exceeds its promise' - delivers the mental model PLUS a visible ready-to-use CLAUDE.md asset injected into the body at 00:19.0-00:22.5 (scored 10/10, driving Saves).
- Fix: For exact formula mimicry, remove the mid-body CLAUDE.md showcase (00:19.0-00:22.5) and reference the guide only verbally inside the CTA line (viral: 'free guide' at 00:23.0), reallocating those 3.5s to the secondary tip stack. NOTE: this is the one structural element where the recreation outscores the viral (10/10 vs 8/10, plus a Saves driver) - only revert if exact replication is prioritized over that gain.

**55. Macro loop closure point**
- Viral: Macro loop closes at 00:18.8 (78.3% of runtime), leaving 5.2s for punchline + CTA.
- Yours: Macro loop closes at 00:24.5 (81.7% of runtime) - 5.7s later in absolute terms, leaving 5.5s of tail; proportionally close but absolutely drifted by the longer front half.
- Fix: After applying the 24.0s re-time, place the macro-close beat ('CO-FUNDADOR de sistema' punch-in, currently 00:24.5) at 00:18.8, with the conceptual punchline cut at 00:20.1 and the CTA at 00:21.8.

**56. Post-reveal pacing-contrast beat (slow-then-snap)** *(viral-weakness — see decision table)*
- Viral: Inside the reveal segment, the edit deliberately decelerates at 00:08.0 ('Slows down first' - slower voice pacing matched to b-roll) then snaps back with sharp delivery on 'execute' at 00:09.5 - a kinetic pacing contrast that mirrors the content.
- Yours: No equivalent deceleration/snap beat: the reveal segment 00:08.8-00:14.0 runs at a constant 'rhythmic, instructional cadence' (00:11.0) with no tempo contrast before re-engaging the stakes at 00:14.0.
- Fix: In the retimed reveal segment, slow the voice read for ~1.5s at ~00:08.0 (on the 'primeiro planeias' idea) then cut to a sharp, fast 'executas' beat at ~00:09.5. Note: the viral report flags the stock b-roll used at its 00:08.0 beat as a weakness - replicate the pacing mechanic but pair it with a terminal/UI close-up (the viral report's own suggested improvement) rather than stock footage.

**57. Lead magnet framing keyword**
- Viral: Asset framed with cost-free framing — 'free guide' is the final on-screen text (00:23.0) and the video ends directly on the word 'guide' at 00:24.0 (Strategic Decision 3: 'ending directly on the word guide').
- Yours: Asset framed with completeness framing — 'o guia completo' (the complete guide) at 00:27.0; the 'free' incentive word is absent from the CTA line.
- Fix: Change the CTA line/caption at 00:27.0 to 'comenta CRIADOR e recebes o guia gratuito' (or 'guia grátis') so the free-cost framing matches, and ensure the final spoken word before the 00:30.0 cut is the asset noun ('guia'), as the viral ends on 'guide'.

**58. CTA music treatment (tail audio behavior)** *(viral-weakness — see decision table)*
- Viral: Music bed runs flat and continuous through the CTA and end of file — 'Flat and continuous line. There are no structural drops' (Section C); no volume change at 00:21.8–00:24.0, which also keeps the audio loop seamless back to 00:00.0.
- Yours: Track volume drops at the CTA: 'Track volume drops slightly' at 00:27.0 (beat sheet); replication spec 00:27.0 specifies 'Drop background music volume level by 30%'. This also creates an audio discontinuity against frame 1 on loop.
- Fix: For an exact copy of the viral formula, keep the music bed at constant volume from 00:27.0 through the 00:30.0 cut (remove the 30% duck). Note: the viral report flags 'Flat Audio Energy' as a viral weakness, so this duck may be a deliberate improvement — only revert if exact replication is the priority.

**59. CTA sound effects** *(viral-weakness — see decision table)*
- Viral: Zero SFX anywhere including the CTA — every SFX cell in the beat sheet is 'None' and Weakness 1 explicitly states 'Complete Lack of SFX'.
- Yours: Adds a 'Digital click chime [INFERRED]' tied to the end-screen cursor animation at 00:27.0 (beat sheet; replication spec 00:27.0 'Introduce a clear click chime sound effect').
- Fix: For exact replication, remove the click chime at 00:27.0 (it also disappears automatically if the SEGUE cursor animation is deleted). The viral analysis flags its own lack of SFX as a weakness, so keeping the chime is a defensible deliberate upgrade — revert only if exact-formula fidelity is the goal.

**60. Gesture and simulated-shake VFX as interrupt types (foreign to the viral grammar)** *(completeness pass)*
- Viral: The viral interrupt vocabulary contains exactly two species: hard cuts and caption swaps. No row in the 00:00.0–00:23.0 beat sheet uses a performance gesture, VFX overlay, or camera shake as an interrupt; the sarcastic micro-loop-1 punchline at 00:02.3 ('hope for the best') is delivered by a plain text change over a new screencast.
- Yours: Three added interrupt species: 'Native hand motion' gesture beat at 00:03.9, 'Subtle camera shake effect [INFERRED] / VFX overlay' on the punchline at 00:05.0, and 'Creator shakes head playfully / Performance tick' at 00:17.2 — none of which exist anywhere in the viral edit.
- Fix: Delete the camera-shake VFX at 00:05.0 and stop relying on the 00:03.9 gesture and 00:17.2 head-shake as interrupts; per the team's screencast fixes, cover those beats with hard cuts to real footage (e.g., a screencast on the punchline beat, mirroring viral 00:02.3) so the only interrupt mechanisms are cuts and caption swaps.

**61. Reveal-negation contrast as its own dedicated text beat** *(completeness pass)*
- Viral: The X-not-Y contrast gets a standalone beat: 'start in' at 00:05.8 is followed 1.3s later by a dedicated caption swap to 'not build mode' at 00:07.1 ('None (Text change)', purpose 'Form a stark workflow contrast', voice 'Stressed "not build"') while the reveal card holds; E.4 codifies it as '[00:07.1] Subtitle Change: Subtitle Block H (Negative contrast phrase)'.
- Yours: The negation 'não em execute mode' has no beat of its own — it arrives 2.2s after the 00:08.8 reveal, buried at the front of the 00:11.0 verbatim block ('não em execute mode. Primeiro planeias...') that simultaneously pops the checklist and opens Micro Loop 3, fusing three jobs into one beat.
- Fix: While the reveal graphic holds, fire a standalone caption swap ~1.3s after the reveal showing only the negation fragment ('não em execute mode' / 'não em build mode') with no other visual event, and only then advance to the checklist beat with 'Primeiro planeias...'.

**62. Series-numbered framing on the reveal graphic title** *(completeness pass)*
- Viral: The reveal card is titled 'Section 1 Plan Mode' (beat sheet 00:05.8) — numbered-section framing that implies a larger multi-part framework beyond this video.
- Yours: The panel is titled 'O SEGREDO: PLAN MODE' (beat sheet 00:08.8) — a 'the secret' framing with no section numbering and no implied series structure.
- Fix: Retitle the reveal graphic to numbered-section framing, e.g. 'SECÇÃO 1: PLAN MODE', so the on-graphic text structure (ordinal + framework name) matches the viral card.

**63. Kinetic/animated caption rendering vs static text blocks** *(completeness pass)*
- Viral: Captions are static instant-swap text chunks; Section D explicitly notes 'There are no decorative emojis or distracting animations, leaving the focus on the code screens and text' (Captions 9/10 for 'minimal cognitive friction').
- Yours: Captions are described as animated: 'dynamic, high-contrast tracking captions' (Hook Autopsy) and 'kinetic keyword captions ... displayed dynamically' (Section D); the spec calls for 'rhythmic fragment text tracking verbal list items' (E.4, 00:02.9).
- Fix: Render every caption block as a static text element that appears/disappears on a single frame with zero motion, tracking, or per-word animation — the only caption 'animation' allowed is the instantaneous swap from one chunk to the next.
