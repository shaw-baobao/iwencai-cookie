# iwencai-cookie

iWenCai（爱问财）Cookie 自动获取工具。用于自动获取接口常用的 `hexin-v` 或 `v` Cookie，方便在爬取或调用相关接口时复用。

本仓库内的可执行代码位于 `tools/iwencai-cookie` 目录，提供了：
- 直接运行的脚本：`tools/iwencai-cookie/get_cookie.py`
- 可安装的包与命令：`iwencai-cookie`（安装后提供 `iwencai-get-cookie` 命令）

## 特性
- 优先通过 `requests` 直接访问站点尝试拿到 Cookie
- 请求方式失败时，若安装了 Playwright，则自动启用 Chromium（默认无头）获取 Cookie
- 支持输出为环境变量导出语句，或只打印原始 Cookie 字符串

## 环境要求
- Python 3.9+
- 依赖：`requests`
- 可选：`playwright`（在 `requests` 失败时会使用浏览器方案）
  - 若使用 Playwright，请先安装浏览器内核：`playwright install chromium`

## 安装
如果只想直接运行脚本，无需安装，见“快速开始”。

如需安装为命令行工具：
1) 进入子目录并安装（可选安装 Playwright）
```
cd tools/iwencai-cookie
pip install -e .           # 只用 requests
# 或
pip install -e .[playwright]  # 带浏览器方案

# 如需浏览器方案，请安装内核
playwright install chromium
```

安装完成后，会得到命令 `iwencai-get-cookie`。

## 快速开始
- 方式一：直接运行脚本（无需安装）
```
python tools/iwencai-cookie/get_cookie.py
```

- 方式二：使用安装后的命令
```
iwencai-get-cookie
```

运行成功后，默认会输出建议导出的环境变量，例如：
```
建议导出为环境变量：
export WENCAI_HEXIN_V='xxxxxx'
export WENCAI_COOKIE='hexin-v=xxxxxx'
```

如果需要仅打印原始 Cookie 字符串（形如 `hexin-v=xxxxxx; v=yyyyyy`），可加 `--print-only`。

## 命令行参数
- `--print-only`：只打印 Cookie 字符串，不输出 export 语句
- `--headless`：强制使用无头浏览器（默认即为无头）
- `--headful`：使用有头浏览器（更便于观察，部分反爬场景更稳）
- `--wait-ms <int>`：页面加载后额外等待的毫秒数，默认 `1500`

示例：
```
# 仅打印 Cookie 字符串
iwencai-get-cookie --print-only

# 使用有头浏览器，并将等待时间调大到 3000ms
iwencai-get-cookie --headful --wait-ms 3000
```

直接运行脚本时参数相同：
```
python tools/iwencai-cookie/get_cookie.py --print-only
```

## 工作原理
1) 通过 `requests.Session()` 访问 `https://www.iwencai.com/` 等页面，读取会话产生的 `hexin-v` 或 `v` Cookie。
2) 若请求方式未拿到 Cookie，且环境已安装 Playwright，则启动 Chromium（默认无头），访问结果页并从浏览器上下文中读取 Cookie。

## 常见问题
- 只拿到了 `v` 没有 `hexin-v`？
  - 接口校验可能不同；请求法通常以 `hexin-v` 为主，若没有可尝试使用浏览器方案（`--headful`/安装 Playwright）并适当增加等待时间。
- 使用 Playwright 报错或无浏览器？
  - 执行：`playwright install chromium`
- 获取失败？
  - 尝试加 `--headful` 并提高 `--wait-ms`，或手动登录/访问站点后再试。

## 目录结构
- `tools/iwencai-cookie/pyproject.toml`：包元数据与依赖
- `tools/iwencai-cookie/iwencai_cookie/__init__.py`：核心逻辑（requests 优先，回退到 Playwright）
- `tools/iwencai-cookie/iwencai_cookie/__main__.py`：命令行入口
- `tools/iwencai-cookie/get_cookie.py`：可直接运行的脚本入口

—— 欢迎根据你的场景二次封装使用。
