# 简历项目描述候选

## Version A：AI 评测岗位

独立设计并实现 Office Agent Evaluation Benchmark：构建 Smoke 20、Development 50 与独立 Formal 100，使用 Mock Office Environment、工具轨迹和 Final State 评测邮件、日历、文档、表格及安全行为；建立 Bad Case 分流、单变量回归与冻结盲测流程，并保留评分器异常的原始审计证据。

- **Benchmark / Harness：** 设计 170 题分层任务体系与批量 Harness，覆盖工具选择、状态正确性、澄清、确认和权限边界。
- **State-based Evaluation：** 基于隔离运行快照、工具日志和状态评分定位 Agent、Infra、Eval Artifact 三类问题。
- **Formal Evaluation：** 在独立 Mock 环境冻结配置后完成 Formal v2 100 题盲测，记录 100 PASS、0 运行异常与 0 安全/关键失败。

## Version B：AI 产品经理岗位

独立规划 Office Agent 质量评测框架：将办公任务拆解为用户任务、风险等级、工具链和验收状态，构建从冒烟、开发回归到冻结盲测的质量门禁；通过任务契约、权限边界和 Failure Injection 定义 Agent 产品能力边界。

- **任务体系：** 将办公能力拆为 9 类场景、风险等级和工具深度，形成 Smoke、Dev、Formal 分层质量路径。
- **质量机制：** 建立状态验收、澄清/确认策略、高风险门禁与 Bad Case 根因分流。
- **发布门禁：** 通过冻结清单、哈希校验、运行日志和 Formal Gate 管理评测版本与结果可追溯性。
