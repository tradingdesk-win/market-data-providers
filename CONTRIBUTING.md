# 贡献配置

- 每个配置唯一保存到 `providers/<id>/config.yaml`；跨市场不复制文件，以 `supported_markets`、`supported_types` 提供分类。
- 附 README 说明支持范围、接口文档、维护者、版本、使用前提和最后测试结果。声明维护者不代表身份认证，也不代表数据授权。
- 提交前运行 `python scripts/validate.py` 和 `python -m unittest discover -s scripts -p 'test_*.py'`。
- 发布配置必须默认禁用。禁止提交 API Key、Cookie、私钥、交易数据或授权信息；扫描只是辅助，需人工审查。
- CI 只做静态验证，不向行情接口发送请求；不得执行配置中提供的脚本。
- 通过仓库托管平台提交 PR，由维护者审查后合并；已停用的数据源目录及相关代码不得提交或推送。
