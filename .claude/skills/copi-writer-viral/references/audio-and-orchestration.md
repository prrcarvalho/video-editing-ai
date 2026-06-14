# Audio & Multisensory Orchestration

The non-obvious layer most creators get wrong. The other reference files cover *what to say* and
*how to structure it*; this covers *how to make every sensory channel fire together* so the video
feels "just better." Read this when the task involves music choice, sound design, voice/prosody,
beat-matching, or end-to-end orchestration. Science backing is in `research-foundations.md` §§10–13.

## The one idea that reorganizes everything
**Score and emotion-arc FIRST, then cut visuals to it.** Most editors cut the visuals, then drop
music on top. Elite retention is the inverse: lock the audio bed and the emotional intensity curve,
mark the beats, *then* place every cut, text reveal, and SFX hit onto that grid. The video is a
**stacked time-series of synchronized multimodal events**, not footage with a song behind it.

---

## 1. The 100ms rule (temporal binding window) — the highest-leverage non-obvious fact
Synchronized audio + visual fuse into a single, *amplified* percept only inside a ~100–250 ms window
(superadditivity; §10). An SFX placed 300 ms off its matching cut is perceptually decoupled and does
nothing. Placed within ~100 ms it fuses and hits harder than the two events separately.

- **Stack reveal events tight:** SFX hit + hard cut + text pop + vocal-emphasis word should all land
  within ~100 ms of each other. Scrub frame-by-frame to verify (≈3 frames at 30fps).
- **Inverse effectiveness:** the *weaker* each element, the *bigger* the proportional boost from
  pairing them. A tiny 2-frame text pop + a faint high tick captures attention disproportionately —
  which is why micro-events stacked on beats feel so satisfying. You don't need big elements; you
  need *coincident* ones.

## 2. Beat-matching — cut on the beat because attention peaks there
The auditory cortex entrains to a beat; attention is heightened *at expected beat times* (§11). So:
- **Cut on downbeats and half-bar accents — NOT every beat.** On-beat cuts land at attentional peaks;
  off-beat cuts land in troughs. Cutting *every* beat feels frantic and violates coherence (overload).
- **Bass strengthens entrainment.** Bass-heavy beds (kick, 808, sub) make beat-matched cuts feel more
  satisfying than thin beds — the low end is doing neurological work, not just sounding "full."
- Motivated cuts (match-on-action, a real visual change) on the beat beat arbitrary beat-cuts.
- Reference point: modern film averages ~2.8s shots; viral short-form runs ~0.8–2s per visual change.

## 3. The frisson reveal recipe (manufacturing the "chills" moment)
The documented acoustic signature of musical chills (Huron; §12) is also the exact recipe for the
"this changes everything" reveal. On the payoff beat, stack:
1. **Pre-silence** — drop the bed for 200–400 ms first (contrast primes the next event).
2. **Subito forte** — sudden large loudness jump.
3. **Frequency broadening** — add sub-bass AND high treble at once (the "trailer boom" + sparkle).
4. **New instrument/voice entry** — something that wasn't there a moment ago.
5. Fire it all on the visual reveal + text pop, inside the 100 ms window.
> Non-obvious corollary: **anticipation is itself rewarding** (a different dopamine pathway than the
> peak). The *build* to the reveal matters as much as the reveal. Don't rush to the drop — earn it.

## 4. Emotion → audio vector (pick the bed from the target feeling)
Map the target emotion to acoustic features, then choose the bed. (Solid psychophysics; the
genre labels are craft layered on top.)
- **Tempo ↔ arousal:** fast (>120 BPM) = high arousal+valence (hype/announce); slow (<76 BPM) =
  contemplative (ethics/deep-dive). **Non-obvious:** mid-tempo (~100–110 BPM, near resting heart
  rate) is the *lowest*-arousal zone — which makes it *correct* for tutorials, where you do NOT want
  sympathetic arousal competing with learning.
- **Mode ↔ valence:** major = hope/empowerment; minor = dread/gravitas. Minor→major modulation
  manufactures relief on a payoff.
- **Timbre:** brighter and rougher = stronger attention capture (cuts through phone speakers). Use for
  risers/stings; avoid for tutorial beds.
- **Sub-bass (<60 Hz):** felt in the body, not heard. Reserve for product/result reveals.

Quick map: model launch → awe, minor→major, 90→128 BPM accelerando, sub-bass drop. Tutorial →
calm-focus, major/modal, ~100 BPM, lo-fi, low dynamic range, no vocals. Breaking news → anxiety,
minor, 120–140 BPM, ticking motif. Workflow win → empowerment, major, 110–125 BPM, uplifting pluck.

## 5. Music vs. narration relationship (the counterintuitive one)
Instinct says "dense topic → add energetic music to keep it lively." Wrong for upskilling content.
Three valid strategies:
- **All matched** (tempo ≈ cut rate ≈ speech rate) — hype/announcements only.
- **Calm voice over driving bed** — the "calm expert in the storm" authority move.
- **Sparse bed under fast narration** — *default for AI tutorials.* Let the voice carry the cognitive
  load; keep music below the voice in arousal (sparse, <90 BPM, sometimes drop it entirely during
  dense screen-recording). Energetic music competes for the verbal channel and tanks comprehension.

## 6. Trending sound strategy (timing + the discovery mechanic)
Audio is a **discovery cluster**: the platform surfaces your video to people who engaged with other
videos using that sound. Two non-obvious plays:
- **The Breakout window is the golden window.** Sound lifecycle: Ignition (<1k uses, day 1–2, risky) →
  **Breakout (1k–50k uses, ~24–48h old — the algorithm aggressively tests these, ride here)** → Peak
  (>100k) → Saturation (>1M, dead). Scan daily; deploy Breakout-stage sounds that match your emotion
  vector. (Lifecycle windows are creator-observed, not platform-published — directional.)
- **Build a signature original sound.** A 15–30s original audio motif attached to your shorts turns
  every reuse by others into a discovery path *back to you*. Reuse it across your own posts for sonic
  brand identity (the one-signature-sound model).
- Business accounts are limited to the Commercial Music Library — default to CML or original audio.

## 7. Voice & prosody (the package previously had none of this)
- **Speech rate is an EDIT, not a delivery.** Deliver ~155 WPM raw, then jump-cut/silence-trim to
  ~180–200 WPM effective (tutorials) or 200–230 (news/hype). The physiological speaking ceiling is
  ~215 WPM, so anything faster on screen is post-production. Comprehension cliff is ~275 WPM — don't
  cross it.
- **Pause BEFORE the key term, not after** (200–600 ms). The pre-pause is a signaling cue that boosts
  encoding; the post-pause lets the payoff land.
- **Whisper-then-spike on reveals** — drop to low/soft, then jump loud on the key word (vocal subito
  forte). Mirrors the frisson recipe in the voice itself.
- **Flat/monotone prosody breaks neural coupling** (§13) — the listener's brain stops syncing. Pitch
  range and loudness variation aren't theatrics; they're the coupling mechanism.
- **Synthetic/cloned voice still partially breaks coupling** — micro-prosody reads as uncanny. Use a
  human voice for high-stakes upskilling content; TTS is acceptable for high-volume distribution clips.
- **Mix:** voice 6–8 dB above the bed average; side-chain duck the music 1.5–3 dB under the voice;
  high-pass <80 Hz, presence boost 2–5 kHz, de-ess 5–8 kHz, noise floor <−60 dBFS in pauses.

## 8. Loudness is a retention lever, not just a spec
Quiet audio is one of the fastest ways to get scrolled past, and **YouTube only normalizes *down*,
never up** — so quiet stays quiet. Master to **−14 LUFS / −1 dBTP** as canonical; prepare a hot
**−10 to −12 LUFS** "social master" for TikTok/Reels. (Targets shift; verify quarterly. Dual-master
is the safe practice.)

## 9. The 8-track orchestration beat-sheet (the unit of work)
Author this BEFORE cutting. For each beat, specify the eight layers and the target emotion. At every
musical accent, fire ≥3 layers coincidentally (within the 100 ms window).

| t | Music state | SFX | Voice (WPM/pitch/emotion) | Visual | Cut/Motion | On-screen text | Color | Target emotion |
|---|---|---|---|---|---|---|---|---|
| 0.0 | silence→bed in | whoosh+tick | "OpenAI just dropped—" 180/high/shocked | head, wide eyes | hard cut from black, 5% punch | "just dropped" | sat+10 | surprise |
| 3.0 | silence (1 beat) | — | (600ms pause) | chart, blurred | static | hidden | — | anticipation peak |
| 3.5 | sub-bass DROP, full | boom+sub+sparkle | "92.4%." slow/low/declarative | chart fly-in | match cut + zoom | "92.4%" large | warm punch | **frisson** |
| … | … | … | … | … | … | … | … | … |

Discipline: score + emotion arc first → mark downbeats → place script beats on beats → cut visuals to
the locked timeline. Not the other way around.

## 10. Solid vs. folklore (audio-specific)
**Solid (peer-reviewed):** superadditivity & temporal binding window (Stein & Meredith; ~100–250 ms);
beat entrainment enhanced by low frequencies (Nozaradan, Lenc); dopamine in anticipation vs peak
(Salimpoor & Zatorre 2011); frisson acoustic correlates (Huron 2006); speech-compression cliff ~275
WPM (Foulke & Sticht 1969); prosody as emotional contagion (Larrouy-Maestri et al.).
**Folklore (directional only):** "beat-synced = 2.3× engagement" (self-referential vendor blog);
"trending sounds = 2–5× reach" (untraceable; the clustering *mechanism* is real, the multiplier is
not); specific BPM-to-genre tables (craft on top of psychophysics); exact trending-sound lifecycle
day-windows (algorithm-observed, not published). Plan on the mechanism, not the multiplier.
