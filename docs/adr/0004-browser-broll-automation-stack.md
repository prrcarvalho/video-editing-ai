# Browser B-roll automation = scripted browser replay plus HyperFrames polish

Automated browser B-roll for Recreations should be produced as deterministic
Screencast Asset Segments. The default stack is:

- `playwright-cli-patched` for browser automation, replay, traces, snapshots,
  network logs, and raw video capture.
- HyperFrames for vertical-video composition, synthetic cursor/click/zoom
  polish, captions, SFX, and final assembly.
- Demo browser profiles or saved storage state by default, not a creator's
  daily Chrome profile.

Pydoll, Scrapling, Screen Studio, Remotion, and Higgsfield stay specialist
tools. Use Pydoll for CDP-level network/event work, Scrapling for crawling and
public reference gathering, Screen Studio for manual premium one-takes,
Remotion for future React-template products, and Higgsfield for generated
cinematic filler. They are not the source of truth for factual UI demos.

## Why

The existing pipeline already treats real screencasts as high-value Asset
Segments, but prior recut work identified missing raw screencasts as the
blocker. A scripted replay lane makes those assets repeatable: the first pass
captures or infers the workflow, and the replay becomes the polished B-roll.

Browser automation video alone is not enough for social content. Automation
does not reliably move the real macOS cursor, and raw recordings rarely have
the click emphasis, drag clarity, zoom rhythm, or mobile readability needed for
short-form B-roll. Those visual indicators should be generated as deterministic
timeline layers.

## Trade-off / consequences

- This creates a real production lane without replacing the existing
  Exemplar-led and Idea-led Recreation workflow.
- Network logs are useful evidence but cannot recreate visual intent by
  themselves. Demo specs must preserve locators, user-visible state, scroll
  position, screenshots, cursor timing, and acceptance notes.
- HyperFrames remains the default renderer because this repo already uses it
  for vertical reels and its HTML composition model is agent-friendly.
- Remotion may be introduced later if React component templates or editor-style
  app infrastructure become more important than continuity with the current
  HyperFrames projects.
- Any workflow that needs personal accounts, private data, posting, uploads, or
  purchases must pass through explicit approval and redaction before capture is
  stored as reusable knowledge.
