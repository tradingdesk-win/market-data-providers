# 贡献配置

- 每个配置唯一保存到 `providers/<id>/config.yaml`；跨市场不复制文件，以 `supported_markets`、`supported_types` 提供分类。
- 附 README 说明支持范围、接口文档、维护者、版本、使用前提和最后测试结果。声明维护者不代表身份认证，也不代表数据授权。
- 提交前运行 `python scripts/validate.py` 和 `python -m unittest discover -s scripts -p 'test_*.py'`。
- 发布配置必须默认禁用。禁止提交 API Key、Cookie、私钥、交易数据或授权信息；扫描只是辅助，需人工审查。
- CI 只做静态验证，不向行情接口发送请求；不得执行配置中提供的脚本。
- GitHub PR 可作为贡献入口，由维护者审查后导入 Gitea 并合并；不要在公开镜像直接产生未同步的提交。
- GitHub main 若与 Gitea 分叉，镜像任务失败并人工整合，禁止 force push。
