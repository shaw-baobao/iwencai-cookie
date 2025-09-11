from __future__ import annotations

import argparse
from typing import Dict

from iwencai_cookie import auto_fetch_cookie


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-fetch iWenCai cookie (hexin-v or v)")
    parser.add_argument("--print-only", action="store_true", help="只打印 cookie 字符串")
    parser.add_argument("--headless", action="store_true", help="使用无头浏览器（默认）")
    parser.add_argument("--headful", action="store_true", help="使用有头浏览器，便于观察（反爬时更稳）")
    parser.add_argument("--wait-ms", type=int, default=1500, help="页面加载后等待毫秒，默认1500")
    args = parser.parse_args()

    headless = not args.headful  # 默认无头；指定 --headful 时使用有头
    ck = auto_fetch_cookie(headless=headless, wait_ms=args.wait_ms)
    if not ck:
        print("自动获取 cookie 失败：请改用浏览器或提供 --cookie/--hexin-v")
        return
    cookie_str = "; ".join([f"{k}={v}" for k, v in ck.items()])
    if args.print_only:
        print(cookie_str)
    else:
        print("建议导出为环境变量：")
        if ck.get("hexin-v"):
            print(f"export WENCAI_HEXIN_V='{ck['hexin-v']}'")
        print(f"export WENCAI_COOKIE='{cookie_str}'")


if __name__ == "__main__":
    main()

