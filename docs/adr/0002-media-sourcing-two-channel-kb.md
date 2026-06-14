# Media sourcing = two-channel Asset Knowledge Base, biased to community/MCP tooling and minimal human intervention

Media that fills a Recreation comes from two channels: (1) the user's **owned** long-form content
(YouTube tutorials/demos), Gemini-segmented into reusable **Asset Segments**; and (2) **stock**,
reached through MCP **Stock Connectors** (Pexels / Coverr / Freesound). The default posture is to
reuse or build on community / MCP tooling and automate sourcing keyed to the **Beat Sheet**. Any
beat that can only be filled by hand (e.g. a specific-person authority clip with no stock source)
is shipped manually but logged as an automation gap — manual is never the intended design.

## Why

End goal is least human intervention. Generating every asset bespoke is costly and off-brand for a
personal creator; manual sourcing doesn't scale. Reuse-owned + outsource-stock-via-agents is the
scalable middle.

## Trade-off / consequences

- Depends on third-party MCP availability, quality, and licensing. The first Stock Connector is now
  Freesound for SFX search: `timjrobinson/FreesoundMCPServer` is bootstrapped under
  `tools/freesound/`, with shared setup docs in `docs/mcp/freesound.md`.
- Freesound search uses token auth through MCP. Original-quality downloads require Freesound OAuth2,
  so the repo owns a small downloader (`scripts/freesound_download.py`) that downloads final picks
  and records attribution metadata in `assets/sfx/freesound/manifest.json`.
- Some beats (specific-person authority footage) have **no** stock source and stay manual until a
  bespoke automation is built.

## reel-1-pedro (first application)

- **SFX / audio accents** → first live Stock Connector trial via Freesound MCP + OAuth downloader.
- **Music bed** → still needs a separate music-safe stock connector or source.
- **8 Claude Code screencasts** → recorded once manually, then Gemini-segmented into the KB so they
  become owned-channel inventory for future short-form.
- **Authority b-roll** → real Boris podcast/interview clip, sourced manually; the known
  not-yet-automated gap.
