# 作品集项目摘要

## 100字版

独立设计 Office Agent Evaluation Benchmark，使用 LangGraph、Mock Office Environment 和状态评分评测邮件、日历、文档、表格及安全行为。建立 Smoke/Dev/Formal 分层、Bad Case 分流与冻结盲测；Certification Formal v2 在当前 Mock 条件下 100/100 通过。

## 300字版

本项目面向办公 Agent 的工具调用与状态变更质量评测。除最终回答外，还检查工具选择、最终状态、权限、澄清、确认和失败恢复。项目包含可重置的 Mock Office Environment、每题隔离快照、批量运行器、工具轨迹、规则/状态/任务评分和 Bad Case 回归。任务体系分为 Smoke 20、Development 50 和独立 Formal 100。开发中曾定位 Formal Grader 的空值异常，保留无效原始结果后修复并补测试，随后以新的独立环境完成 Certification Formal v2 冻结盲测。该项目是个人独立的 Mock benchmark，不是生产系统。

## 600字版

Office Agent 的可靠性不能只靠文本准确率衡量：它要搜索正确来源、操作正确对象、在写入后留下正确状态，并在外发、取消、权限和超时等高风险场景中遵守边界。本项目独立构建了 Office Agent Evaluation Benchmark，将任务划分为邮件、日历、文档、表格、文件、联系人、研究、跨工具和安全场景，并为每题定义预期行为、风险、工具链、禁止动作和状态验收。

实现采用 LangGraph 单 Agent 工具循环和 Mock Office Environment。环境拥有 immutable base state、每题 isolated runtime、权限与 failure injection；Harness 保存工具轨迹、最终回复和 Final State，通过规则、状态和任务评分输出结果。Smoke 20 负责工程守护，Development 50 用于 Bad Case 与回归，Formal 100 作为冻结后盲测。项目中特别强调区分 Agent Failure、Infrastructure Failure 与 Evaluation Artifact，避免将评分器或任务契约问题误判成模型能力问题。

在 Formal v1 中，评分器对成功工具结果的空 error 处理不当，导致 100 个 Raw 运行异常。项目保留原始日志，修复评分器并增加测试，而非覆盖旧记录；随后使用独立 Certification Formal v2，冻结数据、环境、模型、Agent、Graph、工具和评分器后完成一次 100 题盲测。结果在当前 Mock 条件下为 100/100 PASS，运行、安全和关键失败均为 0。该结果不代表真实企业生产、所有模型或所有办公任务的 100% 成功率。
