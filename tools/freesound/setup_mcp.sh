#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="${ROOT_DIR}/tools/freesound/FreesoundMCPServer"
REPO_URL="https://github.com/timjrobinson/FreesoundMCPServer.git"

if ! command -v node >/dev/null 2>&1; then
  echo "node is required for the Freesound MCP server" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required for the Freesound MCP server" >&2
  exit 1
fi

if [ ! -d "${SERVER_DIR}/.git" ]; then
  git clone "${REPO_URL}" "${SERVER_DIR}"
fi

cd "${SERVER_DIR}"
npm install
npm run build

cat <<EOF
Freesound MCP server is ready:
  ${SERVER_DIR}/dist/index.js

Set FREESOUND_API_KEY in your agent environment, then use the config snippets in:
  ${ROOT_DIR}/docs/mcp/freesound.md
EOF
