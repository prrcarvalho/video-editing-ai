# Freesound Stock Connector

Freesound is the first SFX Stock Connector for the Asset Knowledge Base. Agents use the community MCP server for search, metadata, analysis, and similarity, then use the repo-local downloader for original-quality downloads and attribution capture.

## Source choice

Use `timjrobinson/FreesoundMCPServer` as the shared MCP server.

Why this one:

- It exposes search plus richer catalog inspection: sound details, analysis, similar sounds, users, and packs.
- It is a stdio MCP server, so it can be shared by Codex, Claude Code, OpenCode, and other coding agents.
- It honestly does not implement OAuth2 downloads, which keeps search concerns separate from credentialed asset acquisition.

The server uses Freesound token auth for read/search APIs. Freesound's original download endpoint requires OAuth2, so downloads are handled by `scripts/freesound_download.py`.

## One-time setup

Get a Freesound API credential from:

<https://freesound.org/apiv2/apply>

Set these in your shell or agent secret store:

```sh
export FREESOUND_API_KEY="..."
export FREESOUND_CLIENT_ID="..."
export FREESOUND_CLIENT_SECRET="..."
export FREESOUND_REDIRECT_URI="http://freesound.org/home/app_permissions/permission_granted/"
```

On this machine, secrets are loaded from `~/.config/video_editing_ai/freesound.env`. Keep that file user-readable only and do not commit it.

Build the MCP server:

```sh
./tools/freesound/setup_mcp.sh
```

Authorize downloads:

```sh
./scripts/freesound_download.py login
```

The configured Freesound redirect URL is the fallback page:

```text
http://freesound.org/home/app_permissions/permission_granted/
```

After authorizing in the browser, Freesound shows a short-lived authorization code. Paste that code back into the terminal. You can also pass it directly:

```sh
./scripts/freesound_download.py login --code "PASTE_CODE_HERE"
```

The OAuth token is stored outside the repo at `~/.config/video_editing_ai/freesound-oauth.json`.

## Shared MCP command

All agents should point to the same built server:

```text
command: node
args: /Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/FreesoundMCPServer/dist/index.js
env: FREESOUND_API_KEY
```

On this machine, all clients can instead run the wrapper, which loads the private env file before starting Node:

```text
/Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/run_mcp.sh
```

## Codex

Add this to `~/.codex/config.toml`:

```toml
[mcp_servers.freesound]
command = "/Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/run_mcp.sh"
args = []
```

If your Codex version expects literal env values instead of `env_vars`, use:

```toml
[mcp_servers.freesound]
command = "node"
args = ["/Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/FreesoundMCPServer/dist/index.js"]

[mcp_servers.freesound.env]
FREESOUND_API_KEY = "paste-key-here"
```

## Claude Code

Use a user-scoped MCP so every project can search Freesound:

```sh
claude mcp add freesound \
  -- /Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/run_mcp.sh
```

Verify inside Claude Code:

```text
/mcp
```

## OpenCode

Add this to `~/.config/opencode/opencode.jsonc` or the project/user config you prefer:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "freesound": {
      "type": "local",
      "command": [
        "/Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/run_mcp.sh"
      ],
      "enabled": true
    }
  }
}
```

## Agent workflow

1. Search with the Freesound MCP using beat-specific queries.
2. Prefer `Creative Commons 0` / CC0 results first.
3. Accept attribution licenses only when the manifest can preserve the attribution.
4. Avoid `Attribution NonCommercial` for commercial or ambiguous usage.
5. Audition preview URLs before downloading originals.
6. Download the final chosen sound through:

```sh
./scripts/freesound_download.py download SOUND_ID \
  --usage "beat name / cue" \
  --description "why this sound was selected"
```

Downloaded originals land in `assets/sfx/freesound/`, and attribution metadata is appended to `assets/sfx/freesound/manifest.json`.

## Reel-1 Pedro starter queries

- `short whoosh duration:[0.2 TO 1.5]`
- `subtle riser duration:[1 TO 4]`
- `glitch transition duration:[0.2 TO 2]`
- `soft impact duration:[0.1 TO 1.5]`
- `notification ping duration:[0.1 TO 1]`
- `keyboard typing duration:[0.5 TO 3]`
- `mouse click duration:[0.05 TO 0.5]`
- `camera shutter duration:[0.2 TO 2]`
- `digital pop duration:[0.05 TO 0.5]`
