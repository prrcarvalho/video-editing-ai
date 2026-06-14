# Freesound MCP Tooling

This directory holds the project-local Freesound Stock Connector.

## MCP server

Community server:

- Repo: `https://github.com/timjrobinson/FreesoundMCPServer.git`
- Cloned commit: `77c486ae44963224ef3ea940009fa982634eeae9`
- Local path: `tools/freesound/FreesoundMCPServer`

After cloning, the direct npm dependencies were upgraded to clear `npm audit` findings:

- `@modelcontextprotocol/sdk` `^1.15.0` -> `^1.29.0`
- `axios` `^1.10.0` -> `^1.17.0`
- `tsx` `^4.20.3` -> `^4.22.4`
- `typescript` `^5.8.3` -> `^5.9.3`
- `@types/node` `^24.0.10` -> `^25.9.3`

Run setup/build with:

```sh
./tools/freesound/setup_mcp.sh
```

Run from any MCP client with:

```sh
./tools/freesound/run_mcp.sh
```

The wrapper loads `~/.config/video_editing_ai/freesound.env` before starting the server, keeping Freesound credentials out of repo and agent config files.

Cross-agent configuration lives in [docs/mcp/freesound.md](../../docs/mcp/freesound.md).
