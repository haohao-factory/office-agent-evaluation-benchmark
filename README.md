# Office Agent Evaluation Benchmark

一个用于评测日常办公 Agent 的可执行原型，基于 LangGraph、Mock Office Environment 和状态评分（state-based grading）。项目关注的不是模型是否“回答得像对”，而是 Agent 是否在隔离的办公状态中完成了正确、可审计且符合风险边界的操作。

## 项目覆盖

- 场景：Email、Calendar、Document、Spreadsheet、File、Contacts、Research、Cross-tool Workflow 与 Safety。
- 机制：每题隔离环境、工具调用日志、最终状态检查、规则评分、人工复核记录、Bad Case 分流与回归流程。
- 数据集：公开版提供 Smoke 20 示例；Development 与 Certification Formal 题集未公开，以保留独立评测价值。
- 正式认证：冻结的 Formal v2 在 `deepseek-v4-pro-0813` 上记录为 100/100 PASS、0 Runtime Error、0 Safety Failure、0 Critical Failure。此结论仅适用于冻结的 Mock 环境、Agent 配置和模型版本，不代表生产环境或所有模型。

## 仓库结构

- `agent/`：LangGraph 单 Agent、状态和提示词。
- `environment/runtime/`：隔离运行环境的创建、重置与状态存取。
- `graders/`：规则、任务、状态和 Formal 评分器。
- `runners/`：单题、批量与 Formal 执行入口。
- `dataset/smoke/`：20 题公开 Smoke 示例。
- `rubric/`：评分规则。
- `docs/`：架构、方法、指标与项目演进说明。
- `reports/`：脱敏的最终项目材料与 Formal v2 聚合结果。

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

将 `.env` 中的环境变量填入你自己的 OpenAI-compatible API 配置；`.env` 不应提交到 GitHub。公开版不含完整 Mock 初始文件和正式题集，适合展示架构、评测方法与代码框架。

## 重要边界

这是一个独立实现的 Mock Office Agent Evaluation Benchmark，不连接真实 Gmail、Microsoft 365 或企业 OA，也没有真实客户、生产用户或收入数据。完整边界见 `reports/final/authenticity_check.md`。
