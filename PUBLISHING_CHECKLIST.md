# GitHub 发布检查清单

- [ ] 在 GitHub 新建空仓库，不勾选自动创建 README、`.gitignore` 或 License。
- [ ] 确认 `.env`、API Key、终端历史、原始逐题运行日志和完整 Formal 题集不在本目录。
- [ ] 用 `git status` 检查待提交文件；不确定的文件先不要提交。
- [ ] 将本目录全部内容上传；项目根目录中的其他文件不是本次公开发布内容。
- [ ] 仓库描述建议：`A reproducible mock benchmark for tool-using office agents.`
- [ ] README 与简历中保留 Mock、单模型、有限样本等边界，不描述生产上线或真实客户结果。

## 本公开版的取舍

公开：核心实现、测试、Smoke 示例、评分规则、架构与方法文档、聚合结果、项目复盘。

未公开：本地 API 配置、完整 Development/Formal 题集、完整 Mock 文件、历史调试材料、逐题状态快照与原始运行日志。这些内容要么可能削弱基准独立性，要么体积大且不利于他人阅读。
