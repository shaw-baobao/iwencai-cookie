from __future__ import annotations

from typing import Dict, Optional


def auto_fetch_cookie(headless: bool = True, wait_ms: int = 1500) -> Optional[Dict[str, str]]:
    """Try to obtain iWenCai cookie (hexin-v or v) automatically.

    Strategy:
    1) Simple HTTP requests to iWenCai endpoints and read Session cookies.
    2) If Playwright is installed, launch Chromium (headless by default) and read cookies.
    """
    ck = _fetch_cookie_via_requests()
    if ck:
        return ck
    ck = _fetch_cookie_via_playwright(headless=headless, wait_ms=wait_ms)
    return ck


def _fetch_cookie_via_requests() -> Optional[Dict[str, str]]:
    try:
        import requests
    except Exception:
        return None
    sess = requests.Session()
    sess.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        }
    )
    urls = [
        "https://www.iwencai.com/",
        "https://iwencai.com/",
        "https://www.iwencai.com/unifiedwap/result?w=上证指数",
    ]
    try:
        for u in urls:
            sess.get(u, timeout=10)
        jar = sess.cookies.get_dict()
        kv: Dict[str, str] = {}
        if jar.get("hexin-v"):
            kv["hexin-v"] = jar.get("hexin-v", "")
        if jar.get("v") and "v" not in kv:
            kv["v"] = jar.get("v", "")
        return kv or None
    except Exception:
        return None


def _fetch_cookie_via_playwright(headless: bool = True, wait_ms: int = 1500) -> Optional[Dict[str, str]]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(
                "https://www.iwencai.com/unifiedwap/result?w=上证指数",
                wait_until="load",
                timeout=30000,
            )
            page.wait_for_timeout(wait_ms)
            cookies = page.context.cookies()
            browser.close()
            kv: Dict[str, str] = {}
            for c in cookies:
                name = c.get("name")
                if name in ("hexin-v", "v"):
                    kv[name] = c.get("value", "")
            return kv or None
    except Exception:
        return None

