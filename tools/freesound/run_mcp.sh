#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${FREESOUND_ENV_FILE:-$HOME/.config/video_editing_ai/freesound.env}"
SERVER_JS="/Users/pedrocarvalho/projects/video_editing_ai/tools/freesound/FreesoundMCPServer/dist/index.js"

if [ -f "${ENV_FILE}" ]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

exec node "${SERVER_JS}"
