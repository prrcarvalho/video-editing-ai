#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydoll-python>=2.0",
# ]
# ///
"""
Recovery tool: harvest fresh Gemini session cookies (__Secure-1PSID /
__Secure-1PSIDTS) from a dedicated, pipeline-owned Chrome profile and rewrite
~/.gemini_cookies.env.

The profile lives at ~/.gemini_pipeline_chrome and has its own Google session,
fully decoupled from your daily Chrome — the pipeline's cookie rotation can
never log out your real browser, and vice versa.

First run: a Chrome window opens on gemini.google.com — log in to Google once.
Every later run is unattended: the window appears for a few seconds while
cookies are read, then closes.

Usage:
    uv run refresh_cookies.py
    uv run refresh_cookies.py --login-timeout 600
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions

PROFILE_DIR = Path.home() / ".gemini_pipeline_chrome"
COOKIE_ENV_PATH = Path(
    os.environ.get("GEMINI_COOKIE_ENV", "~/.gemini_cookies.env")
).expanduser()
COOKIE_CACHE_DIR = Path(
    os.environ.get("GEMINI_COOKIE_PATH", Path.home() / ".cache" / "gemini_webapi")
)

LOGIN_HINT_AFTER = 10  # seconds before assuming a first-run login is needed
POLL_INTERVAL = 2


def write_cookie_env(psid: str, psidts: str | None) -> None:
    """Atomically rewrite the cookie env file, mode 600, still `source`-able."""
    content = (
        "# Managed by gemini_video.py — auto-updated with rotated cookies after each run.\n"
        "# Recovery when the session is dead: uv run refresh_cookies.py\n"
        f"export GEMINI_1PSID='{psid}'\n"
        f"export GEMINI_1PSIDTS='{psidts or ''}'\n"
    )
    tmp = COOKIE_ENV_PATH.with_name(COOKIE_ENV_PATH.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, content.encode("utf-8"))
    finally:
        os.close(fd)
    os.replace(tmp, COOKIE_ENV_PATH)


def previous_psid() -> str | None:
    try:
        for line in COOKIE_ENV_PATH.read_text(encoding="utf-8").splitlines():
            stripped = line.strip().removeprefix("export ").strip()
            if stripped.startswith("GEMINI_1PSID="):
                return stripped.split("=", 1)[1].strip("'\"") or None
    except OSError:
        pass
    return None


async def harvest(login_timeout: float) -> tuple[str, str | None]:
    options = ChromiumOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    # --no-first-run / --no-default-browser-check are pydoll defaults;
    # re-adding them raises ArgumentAlreadyExistsInOptions.

    # Headed on purpose: Google blocks logins from headless browsers.
    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://gemini.google.com/app")

        waited = 0.0
        hinted = False
        while waited <= login_timeout:
            cookies = await tab.get_cookies()
            jar = {
                c["name"]: c["value"]
                for c in cookies
                if c.get("domain", "").endswith("google.com")
            }
            psid = jar.get("__Secure-1PSID")
            if psid:
                return psid, jar.get("__Secure-1PSIDTS")
            if not hinted and waited >= LOGIN_HINT_AFTER:
                hinted = True
                print(
                    "First run: log in to Google in the Chrome window that just "
                    f"opened; waiting up to {login_timeout / 60:.0f} min...",
                )
            await asyncio.sleep(POLL_INTERVAL)
            waited += POLL_INTERVAL

    sys.exit(
        "error: no Google session found before timeout. Re-run and complete the "
        "login in the Chrome window, or raise --login-timeout."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="refresh_cookies",
        description="Harvest fresh Gemini cookies from the pipeline's Chrome profile",
    )
    parser.add_argument(
        "--login-timeout",
        type=float,
        default=300,
        help="seconds to wait for the one-time Google login (default: 300)",
    )
    args = parser.parse_args()

    old_psid = previous_psid()
    psid, psidts = asyncio.run(harvest(args.login_timeout))

    # A fresh harvest supersedes every cached session the library may hold
    # (and a new 1PSID would orphan old cache files anyway).
    for stale in COOKIE_CACHE_DIR.glob(".cached_cookies_*.json"):
        stale.unlink(missing_ok=True)

    write_cookie_env(psid, psidts)
    changed = "changed" if old_psid != psid else "unchanged"
    print(f"updated {COOKIE_ENV_PATH} (session id {changed})")
    if not psidts:
        print("note: __Secure-1PSIDTS not present; the library will bootstrap from 1PSID")
    print("verify with: uv run gemini_video.py models")


if __name__ == "__main__":
    main()
