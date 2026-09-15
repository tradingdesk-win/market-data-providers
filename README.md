# tradingdesk market-data-providers

TradingDesk 与社区维护的独立行情配置仓库。配置由 TradingDesk 用户主动下载并导入，主程序不会自动安装、下载或启用这些配置。

## 使用 | Usage

下载配置文件的 **Raw** 内容，在 TradingDesk 中打开“全局设置 → 数据源管理”，导入本地 YAML，查看预览并确认后执行测试、启用，并在图表设置中选择默认数据源。

Download the **Raw** YAML file. In TradingDesk, open **Global Settings → Data Sources**, import the local YAML, review and confirm it, run a test, enable the provider, and select it as the default source in chart settings.

### 可导入数据源 | Available providers

| 数据源 / Provider | 文件 / File | 市场 / 品种 | K 线周期 / Periods |
| --- | --- | --- | --- |
| 东方财富 / EastMoney | `providers/eastmoney/config.yaml` | CN / STOCK | 15m、30m、1h、1d、1w、1M |
| 新浪财经 / Sina Finance | `providers/sina/config.yaml` | CN / STOCK | 15m、30m、1h、2h、1d |
| 腾讯财经 / Tencent Finance | `providers/tencent/config.yaml` | CN / STOCK | 1d、1w、1M |
| Tushare | `providers/tushare/config.yaml` | CN / STOCK | 1d |

所有配置默认禁用，仅声明中国大陆股票。测试时请使用 `000001.SZ` 等 A 股代码，不要使用默认美股标的 `AAPL`。配置可用性不代表全部股票、周期或未来接口均可用。

All configurations are disabled by default and declare mainland China equities only. Use symbols such as `000001.SZ` for testing; do not use the default US symbol `AAPL`. Availability is not guaranteed for every symbol, period, or future API response.

### Tushare Token

请自行准备可用的 Tushare Pro Token。导入或启用 `providers/tushare/config.yaml` 后，在 TradingDesk 的“全局设置 → 数据源管理”中将 Token 直接输入 Tushare 的 Token 输入框；应用会自动加载该设置，无需设置环境变量或修改 YAML。不要把真实 Token 提交到仓库或写入日志。

Prepare a valid Tushare Pro Token yourself. After importing or enabling `providers/tushare/config.yaml`, enter the token directly in the Tushare Token field under **Global Settings → Data Sources** in TradingDesk. The application loads this setting automatically; no environment variable or YAML edit is required. Never commit a real token or write it to logs.

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
