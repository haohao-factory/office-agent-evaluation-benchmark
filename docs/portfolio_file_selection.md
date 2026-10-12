# GitHub / 作品集文件筛选建议

## 建议公开

`README_FINAL.md`、`docs/final_architecture.md`、`docs/phase_timeline.md`、指标说明、最终复盘、Formal v2 报告、冻结清单（确认无敏感路径后）。

## 建议保留但不展示

完整运行日志、每题状态快照、历史调试报告、全部 Bad Case 细节；面试追问时可展示局部证据。

## 建议不提交 GitHub

`.env`、本地 API Key、运行时目录、缓存、任何真实凭证、系统绝对路径、无必要的大型二进制输出。

## 包含本地路径需清理

发布前搜索用户目录、项目目录、临时目录、用户名和绝对 API 配置路径。

## API Key / Secret 风险检查

确认环境变量、`.env`、shell history、日志和截图中不存在 key、token、endpoint 中的私有标识。

## Mock Sensitive Data 检查

当前数据应仅使用虚构姓名、公司、邮箱和文件；发布前仍需人工检查，不由自动化替用户决定公开范围。

