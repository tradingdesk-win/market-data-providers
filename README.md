# tradingdesk market-data-providers

TradingDesk 与社区维护的独立行情配置仓库。配置由 TradingDesk 用户主动下载并导入，主程序不会自动安装、下载或启用这些配置。

## 使用 | Usage

下载配置文件的 **Raw** 内容，在 TradingDesk 中打开“全局设置 → 数据源管理”，导入本地 YAML，查看预览并确认后执行测试、启用，并在图表设置中选择默认数据源。

Download the **Raw** YAML file. In TradingDesk, open **Global Settings → Data Sources**, import the local YAML, review and confirm it, run a test, enable the provider, and select it as the default source in chart settings.

### 可导入数据源 | Available providers

| 数据源 / Provider | 文件 / File | 市场 / 品种 | K 线周期 / Periods |
| --- | --- | --- | --- |
| 新浪财经 / Sina Finance | `providers/sina/config.yaml` | CN / STOCK | 15m、30m、1h、2h、1d |
| 新浪财经港股 / Sina HK | `providers/sina-hk/config.yaml` | HK / STOCK | 实时、批量实时；无 K 线 |
| 新浪财经美股 / Sina US | `providers/sina-us/config.yaml` | US / STOCK | 实时、批量实时；无 K 线 |
| 腾讯财经 / Tencent Finance | `providers/tencent/config.yaml` | CN、HK、US / STOCK | 1d、1w、1M (HK/US live-checked for 1d only) |
| Tushare | `providers/tushare/config.yaml` | CN / STOCK | 1d |
| Tushare Pro 港股 | `providers/tushare-hk/config.yaml` | HK / STOCK | 1d |
| Tushare Pro 美股 | `providers/tushare-us/config.yaml` | US / STOCK | 1d |
| 同花顺 iFinD / HiThink | `providers/hithink/config.yaml` | CN / STOCK | 1d |
| Binance Spot | `providers/binance/config.yaml` | CRYPTO / CRYPTO (Spot) | 1m、5m、15m、30m、1h、2h、4h、1d、1w、1M；实时 / 批量实时 |
| OKX Spot | `providers/okx/config.yaml` | CRYPTO / CRYPTO (Spot) | 实时 / 批量实时 |

所有配置默认禁用。股票配置按各自声明的市场范围使用；新浪 A 股配置保持 CN-only，港美股实时行情使用独立的 `sina-hk` / `sina-us` 配置，不提供历史 K 线。腾讯配置已对代表性港股和美股代码进行实时、批量实时及日线接口检查，使用 `00700.HK` 和 `AAPL.US` 形式的市场限定代码。其他周/月线未在港美市场验证。Binance 配置覆盖 Spot 公共 K 线和 ticker，OKX 配置仅覆盖 Spot 公共 ticker，均不覆盖衍生品。配置可用性不代表全部股票、周期或未来接口均可用，也不代表上游授权或行情许可。

All configurations are disabled by default. Use each stock configuration only for its declared markets. Tencent representative HK/US symbols were checked against single quote, batch quote, and daily K-line endpoints using market-qualified inputs such as `00700.HK` and `AAPL.US`. Sina mainland equities remain CN-only; separate `sina-hk` and `sina-us` configurations provide realtime quotes without historical K-lines. Other HK/US weekly and monthly periods were not checked. Binance covers public Spot candlesticks and tickers; OKX covers public Spot tickers only. Neither covers derivatives. Availability is not guaranteed for every symbol, period, or future API response, and verification does not imply upstream authorization or market-data licensing.

Crypto journal pairs use canonical `BASE-QUOTE` form (for example, `BTC-USDT`). Binance maps this to `BTCUSDT`; OKX uses `BTC-USDT`. Returned prices remain in the quote asset and are not converted (USDT is not treated as USD). Binance batch quotes use JSON-array `symbols` requests with a 100-symbol maximum. See each config for official documentation, rate-limit notes, and verification scope. Binance BTC-USDT latest and backwards-paginated K-lines were live-checked on 2026-10-19 for every declared period; ticker mappings and OKX retain fixture-only verification.

### Binance K 线与测试 | Binance K-lines and testing

测试标的可选 `BTC-USDT`、`ETH-USDT`，也可手工输入其他现货交易对。K 线使用 UTC 开盘时间（毫秒），通过 `endTime` 向历史翻页，每页最多 500 条；省略 `startTime` 以取得游标前最近一页，应用会在本地过滤起始时间。月线为 `1M`，分钟线为 `1m`。

Use `BTC-USDT` or `ETH-USDT` as probe symbols, or enter another Spot pair manually. K-lines use UTC open timestamps in milliseconds and backwards pagination via `endTime`, with up to 500 rows per page. `startTime` is omitted to fetch the latest page before the cursor; the application filters the start bound locally. Monthly candles use `1M`, while minute candles use `1m`.

已导入的旧配置不会随仓库文件自动更新。可以把新文件内容写入应用实际的 `config/chart_api/binance.yaml`（保留原来的 `enabled` 状态），再点击“重载”；或停用并删除旧 Binance 配置，重新导入本文件后测试、启用。设置页“检查”验证的是实时端点，K 线需在图表中确认。

Imported configurations do not update automatically. Replace the contents of the application's actual `config/chart_api/binance.yaml`, retaining its `enabled` state, then click Reload; alternatively disable and delete the old Binance configuration, import this file, test, and enable it again. The settings connectivity check uses the realtime endpoint; verify K-lines in the chart.

### 新浪港股、美股实时行情 | Sina HK/US realtime quotes

`sina-hk` / `sina-us` 1.0.1 修正 YAML 字段层级，港股名称、价格和更新时间索引，以及美股代码大小写。测试输入使用 `00700.HK`、`00005.HK` 或 `AAPL.US`、`MSFT.US`。2026-10-19 已实测这些标的的单条与批量实时行情；两份配置均不提供历史 K 线。

Version 1.0.1 corrects the YAML field hierarchy, HK quote field/time indices, and US request casing. Use `00700.HK` / `00005.HK` or `AAPL.US` / `MSFT.US` as probe symbols. Single and batch realtime quotes for these symbols were live-checked on 2026-10-19. Neither configuration provides historical K-lines.

美股配置使用 `gb_{{code_lower}}`，需要运行支持该模板的新版桌面程序。替换已导入的 `config/chart_api/sina-hk.yaml` / `sina-us.yaml` 后点击“重载”，或停用删除旧配置后重新导入、测试、启用。保持 `enabled` 状态符合自己的选择。

The US configuration uses `gb_{{code_lower}}` and requires the updated desktop build. Replace the imported `config/chart_api/sina-hk.yaml` / `sina-us.yaml` and click Reload, or disable/delete the old configuration and import, test, and enable the updated one. Retain your chosen enabled state when replacing a file.

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

### Binance 1.2.0: live candlesticks

Optional `api.kline_stream.url` and `response.kline_stream` describe a public WSS
connection and an object parser. `symbol_field`, `period_field` and `closed_field`
are required inside the selected object, alongside timestamp/OHLC/volume mappings.
`{{symbol_lower}}` uses the provider's normalized pair (BTC-USDT → btcusdt);
`{{period}}` uses `period_mapping`. Older configurations remain REST-only.

The desktop subscribes only while a chart is visible, buffers updates during REST
history/recovery, and merges candles by UTC opening timestamp. Standard Binance
streams update most intervals about every two seconds. Disconnects use bounded
backoff with jitter and REST gap recovery; the UI distinguishes live from periodic
refresh. Provisional pushed candles never enter the valuation cache. No API key
is required. See [Binance stream documentation](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams).

Replace the actual development `config/chart_api/binance.yaml`, retain `enabled`,
and reload/restart the desktop. Existing running subscriptions use their original
configuration snapshot; reopening the chart applies the new settings.
