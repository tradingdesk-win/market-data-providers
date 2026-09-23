# tradingdesk market-data-providers

TradingDesk 与社区维护的独立行情配置仓库。配置由 TradingDesk 用户主动下载并导入，主程序不会自动安装、下载或启用这些配置。

## 使用 | Usage

下载配置文件的 **Raw** 内容，在 TradingDesk 中打开“全局设置 → 数据源管理”，导入本地 YAML，查看预览并确认后执行测试、启用，并在图表设置中选择默认数据源。

Download the **Raw** YAML file. In TradingDesk, open **Global Settings → Data Sources**, import the local YAML, review and confirm it, run a test, enable the provider, and select it as the default source in chart settings.

### 可导入数据源 | Available providers

| 数据源 / Provider | 文件 / File | 市场 / 品种 | K 线周期 / Periods |
| --- | --- | --- | --- |
| 新浪财经 / Sina Finance | `providers/sina/config.yaml` | CN / STOCK | 15m、30m、1h、2h、1d |
| 腾讯财经 / Tencent Finance | `providers/tencent/config.yaml` | CN、HK、US / STOCK | 1d、1w、1M (HK/US live-checked for 1d only) |
| Tushare | `providers/tushare/config.yaml` | CN / STOCK | 1d |
| Tushare Pro 港股 | `providers/tushare-hk/config.yaml` | HK / STOCK | 1d |
| Tushare Pro 美股 | `providers/tushare-us/config.yaml` | US / STOCK | 1d |
| 同花顺 iFinD / HiThink | `providers/hithink/config.yaml` | CN / STOCK | 1d |
| Binance Spot | `providers/binance/config.yaml` | CRYPTO / CRYPTO (Spot) | 实时 / 批量实时 |
| OKX Spot | `providers/okx/config.yaml` | CRYPTO / CRYPTO (Spot) | 实时 / 批量实时 |

所有配置默认禁用。除腾讯配置外，股票配置仅声明中国大陆股票；新浪原始实时接口虽然能返回部分港美股响应，但字段格式与当前 CN 解析器不兼容，日线端点也未返回港美股数据，因此仍保持 CN-only。腾讯配置已对代表性港股和美股代码进行实时、批量实时及日线接口检查，使用 `00700.HK` 和 `AAPL.US` 形式的市场限定代码。其他周/月线未在港美市场验证。Binance 和 OKX 配置仅覆盖 Spot 公共 ticker，不覆盖衍生品。配置可用性不代表全部股票、周期或未来接口均可用，也不代表上游授权或行情许可。

All configurations are disabled by default. Stock configurations declare mainland China equities only except Tencent, whose representative HK/US symbols were checked against single quote, batch quote, and daily K-line endpoints using market-qualified inputs such as `00700.HK` and `AAPL.US`. Sina's raw realtime endpoint returned sample HK/US payloads, but their field layouts are incompatible with the current CN parser and its configured daily endpoint returned no HK/US rows, so Sina remains CN-only. Other HK/US weekly and monthly periods were not checked. Binance and OKX cover public Spot tickers only, not derivatives. Availability is not guaranteed for every symbol, period, or future API response, and verification does not imply upstream authorization or market-data licensing.

Crypto journal pairs use canonical `BASE-QUOTE` form (for example, `BTC-USDT`). Binance maps this to `BTCUSDT`; OKX uses `BTC-USDT`. Returned prices remain in the quote asset and are not converted (USDT is not treated as USD). Binance batch quotes use JSON-array `symbols` requests with a 100-symbol maximum. See each config for official documentation, rate-limit notes, and the fixture-only verification scope. No live verification was performed for these catalog entries.

### Tushare Token

请自行准备可用的 Tushare Pro Token。导入或启用 `providers/tushare/config.yaml` 后，在 TradingDesk 的“全局设置 → 数据源管理”中将 Token 直接输入 Tushare 的 Token 输入框；应用会自动加载该设置，无需设置环境变量或修改 YAML。不要把真实 Token 提交到仓库或写入日志。

Prepare a valid Tushare Pro Token yourself. After importing or enabling `providers/tushare/config.yaml`, enter the token directly in the Tushare Token field under **Global Settings → Data Sources** in TradingDesk. The application loads this setting automatically; no environment variable or YAML edit is required. Never commit a real token or write it to logs.

### 同花顺 Financial-API Key

请自行准备同花顺 Financial-API Key。导入或启用 `providers/hithink/config.yaml` 后，在 TradingDesk 的“全局设置 → 数据源管理”中填写 Key；应用会通过 `X-api-key` 请求头在运行时注入。不要把真实 Key 写入 YAML、日志或 Git 提交。当前配置仅支持 A 股日线 (`1d`) 历史 K 线、实时快照和批量实时快照。

## 目录结构 | Layout

每个数据源存放于 `providers/<id>/config.yaml`，使用 `supported_markets`（CN、US、HK、CRYPTO）和 `supported_types` 分类。跨市场配置只保留一份，避免版本不一致。

Each provider lives at `providers/<id>/config.yaml`. Use `supported_markets` (CN, US, HK, CRYPTO) and `supported_types` for classification. Keep cross-market providers in one file to avoid version drift.

## 本地验证 | Local validation

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
```

配置由 TradingBea 与社区维护，不代表上游服务商的授权、背书或服务保证；使用者应自行确认适用条款。

Configurations are maintained by TradingBea and the community and do not imply authorization, endorsement, or service guarantees from upstream providers. Confirm applicable terms before use.
