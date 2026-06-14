#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["gemini-webapi[browser]>=2.0", "orjson"]
# ///
"""Diagnostic: dump the raw model list from the Gemini GetUserStatus RPC."""

import asyncio
import os
from pathlib import Path

import orjson as json
from gemini_webapi import GeminiClient, set_log_level
from gemini_webapi.constants import GRPC
from gemini_webapi.types import RPCData
from gemini_webapi.utils import extract_json_from_response, get_nested_value


async def main():
    client = GeminiClient()
    await client.init(timeout=60, auto_refresh=False)
    try:
        response = await client._batch_execute(
            [RPCData(rpcid=GRPC.GET_USER_STATUS, payload="[]")]
        )
        response_json = extract_json_from_response(response.text)

        for part in response_json:
            part_body_str = get_nested_value(part, [2])
            if not part_body_str:
                continue
            part_body = json.loads(part_body_str)
            models_list = get_nested_value(part_body, [15])
            if not isinstance(models_list, list):
                continue
            print(f"raw registry entries: {len(models_list)}\n")
            for model_data in models_list:
                if not isinstance(model_data, list):
                    print(f"  (non-list entry) {model_data!r}")
                    continue
                model_id = get_nested_value(model_data, [0], "")
                display_name = get_nested_value(model_data, [1], "")
                description = get_nested_value(model_data, [2], "")
                print(f"  id={model_id!r}  display={display_name!r}")
                print(f"      desc={description!r}")
                # any extra fields beyond the three the library reads
                if len(model_data) > 3:
                    print(f"      extra[3:]={model_data[3:]!r}")
    finally:
        await client.close()


set_log_level("WARNING")
# Same durable cookie-cache location as gemini_video.py (not volatile $TMPDIR)
os.environ.setdefault(
    "GEMINI_COOKIE_PATH", str(Path.home() / ".cache" / "gemini_webapi")
)
Path(os.environ["GEMINI_COOKIE_PATH"]).mkdir(parents=True, exist_ok=True)
asyncio.run(main())
