# Browser B-roll Automation

This lane turns a Beat Sheet row with source-type `screencast` into a reusable
Screencast Asset Segment. It is for real browser or web-app demonstrations that
need social-video polish: synthetic cursor movement, click states, drag paths,
small zooms, captions, SFX, and A-roll timing.

## Stack

Default:

1. `playwright-cli-patched` records and replays the browser workflow.
2. The replay emits raw capture, trace, snapshots, and network evidence.
3. HyperFrames composes the raw capture into the Recreation with cursor, zoom,
   caption, and audio layers.
4. The approved result is stored as an Asset Segment for future reuse.

Specialist tools:

- Use Pydoll when CDP-level event or network monitoring is the core problem.
- Use Scrapling for public crawling, reference gathering, and durable scraping.
- Use Screen Studio when a human one-take with the real macOS cursor is the
  chosen capture mode.
- Use Remotion only for a future React-template renderer lane.
- Use Higgsfield for generated cinematic filler, not factual UI demos.

## Artifact Contract

Store each automated demo under:

```text
recreations/<recreation_slug>/assets/screencasts/<shot_id>/
  demo_run_spec.json
  automation_run_manifest.json
  replay.mjs
  hyperframes_notes.md
  raw/
    browser_capture.webm
  styled/
    screencast_asset_segment.mp4
  traces/
  snapshots/
  network/
```

`demo_run_spec.json` is the source of truth for the requested browser B-roll. It
includes target URL, viewport, duration, Beat Sheet row IDs, privacy mode, tool
policy, workflow steps, wait conditions, and visual treatment.

`automation_run_manifest.json` records what actually happened: tool versions,
browser/profile policy, script path, raw capture path, trace path, styled render
path, network evidence, redactions, and approval state.

`replay.mjs` is the deterministic replay script consumed by
`playwright-cli-patched run-code --filename replay.mjs`.

`hyperframes_notes.md` tells the assembly agent how to place the styled
screencast in the final Recreation.

The JSON contract lives in
`docs/schemas/browser_broll_automation.schema.json`.

## Production Workflow

1. Plan from the Beat Sheet. Identify the rows that need browser B-roll, the
   desired duration, the emotional purpose, and the mobile readability risk.
2. Capture or infer the workflow. Use Playwright codegen, manual observation, or
   an agent-authored step list. Do not rely on network logs alone.
3. Normalize into replay. Use stable locators, deterministic viewport, explicit
   waits, slow typing, readable pauses, and bounded retries.
4. Record evidence. Run the replay with video, trace, snapshots, and network
   logs. Use a demo profile or saved storage state unless the user explicitly
   authorizes a real Chrome session.
5. Compose visual polish. Add a synthetic cursor layer, click ripple, drag
   state, zoom boxes, caption cues, and SFX in HyperFrames.
6. Approve as an Asset Segment. Save the styled MP4 and manifest under the
   Recreation folder, then index it in the Asset Knowledge Base when it is
   useful beyond one project.

## Step Semantics

Each browser step must declare one action:

- `goto`
- `click`
- `fill`
- `type`
- `press`
- `hover`
- `drag`
- `scroll`
- `wait`
- `snapshot`
- `assert_visible`

Steps that interact with UI should include either a locator or target bounds.
Steps that click, drag, or reveal small UI should include cursor and zoom
instructions. Every step may include a caption cue and SFX cue, but those cues
are timing hints for the renderer, not browser actions.

## Privacy Rules

- Default to demo profiles or saved storage state.
- Do not store cookies, private local storage, private browsing history,
  passwords, API keys, payment data, personal messages, or unredacted personal
  identifiers in reusable artifacts.
- Mark any necessary private context in `redaction_notes` and keep the raw
  evidence out of the Asset Knowledge Base until reviewed.
- Browser demos that post, upload, purchase, send, delete, or change permissions
  require explicit approval at action time.

## Acceptance Checks

- The replay can run three times with the same visible states and comparable
  duration.
- The styled output is 1080x1920 unless the Beat Sheet says otherwise.
- No cursor, caption, or zoom layer covers the UI element the viewer needs to
  understand.
- Every click has a visible state change or deliberate hold, plus an optional
  click ripple/SFX cue.
- The manifest lists all raw, trace, network, and styled outputs.
- The final Recreation acceptance pass can identify screen recording, cursor
  motion, click/tap indicators, zooms, and timing as intended.
