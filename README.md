# market-data-providers
TradingBea 与社区维护的独立行情配置仓库。与 TradingDesk 主程序分开发行，不会自动安装或启用。

## 使用

下载配置的原始 YAML → TradingDesk 设置 / 数据源管理 → 导入本地 YAML → 查看预览并确认 → 测试 → 启用 → 图表设置选择默认数据源。

## 可导入配置

| 数据源 | 文件 | 市场 / 品种 | 配置声明的 K 线周期 |
| --- | --- | --- | --- |
| 东方财富 | `providers/eastmoney/config.yaml` | CN / STOCK | 15m、30m、1h、1d、1w、1M |
| 新浪财经 | `providers/sina/config.yaml` | CN / STOCK | 15m、30m、1h、2h、1d |
| 腾讯财经 | `providers/tencent/config.yaml` | CN / STOCK | 1d、1w、1M |
| 选股宝 | `providers/xuangubao/config.yaml` | CN / STOCK | 15m、1h、2h、1d、1w、1M |

2026-09-09 已使用 TradingDesk 实际通用解析器验证四份配置的单标的实时行情、双标的批量行情和近两周日 K 线。测试标的是 `000001.SZ`，批量另含 `600000.SS`；实时和批量价格一致，日 K 线非空且时间戳、价格有效。这不代表全部股票、其他周期或未来接口可用性得到保证。

四份配置均默认禁用，仅声明中国大陆股票，不应使用默认美股标的 AAPL 测试。下载时保存 **Raw 原始 YAML**，不要保存 GitHub 网页。导入后将测试标的改成 `000001.SZ`，测试、启用并选择默认源；账户如已有独立行情源，需要同步更改账户设置。

此次转换统一使用 HTTPS，修正选股宝字段映射与东方财富日期范围。新浪旧分时接口返回 `Service not found`，已去掉；其他分时接口本轮未验证，也暂不发布。腾讯旧配置错误地在日/周/月接口上声明分钟周期，现已移除分钟周期。其他非日线周期沿用历史映射，尚未逐项实测。

`examples/minimal.yaml` 仍为虚构示例，不能获得真实行情。配置由 TradingBea 与社区维护，并不表示获得上游数据服务商的授权、背书或服务保证；使用前自行确认适用条款。主程序不打包、不自动下载这些配置。

在 TradingDesk 主仓库执行实际解析器验证（联网测试为手动操作，不在 PR CI 中请求第三方接口）：

```sh
CHART_API_EXTERNAL_CONFIGS="$PWD/market-data-providers/providers" go test ./backend/services/chart_api -run TestExternalProviderConfigs -v
CHART_API_EXTERNAL_CONFIGS="$PWD/market-data-providers/providers" CHART_API_LIVE_TEST=1 go test ./backend/services/chart_api -run TestExternalProviderConfigs -count=1 -v
```

## 组织方式

每个数据源存放于 `providers/<id>/config.yaml`，以配置的 `supported_markets`（CN、US、HK、CRYPTO）及 `supported_types` 分类。跨市场配置只保留一份，避免按市场/资产目录复制后版本不一致。

## 本地验证

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
```

Schema 校验发布格式；TradingDesk 导入器仍会执行自己的 Go 模型校验，不保证接口可达或响应兼容。

## Gitea 同步

将本仓库原有 GitHub main 历史完整导入 Gitea（不要另建不相关历史）。启用 Actions，为 `ubuntu-latest` 标签配置可执行 checkout/setup-python 的隔离 Runner，并设置仓库 Secret `MARKET_PROVIDERS_GITHUB_TOKEN`。Token 仅授权此 GitHub 仓库，需 Contents 写权限；首次推送 workflow 文件还需 Workflows 写权限。

`.gitea/workflows/validate-and-mirror.yml` 先校验，再仅在 main push 时普通推送到 GitHub main；PR 作业不读取镜像令牌。不部署到 Runner 工作目录长期运行，不使用强制镜像，不推送删除或所有 refs。Gitea URL、Runner 和 Secret 需管理员配置，本地文件不代表远端部署完成。
