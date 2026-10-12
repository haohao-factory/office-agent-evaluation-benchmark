# Office Agent Evaluation Benchmark — 项目总复盘

## 1. Project Background

本项目独立设计并实现了一个 Office Agent Evaluation Benchmark。办公 Agent 不仅要答对文本问题，还要在邮件、日历、文档、表格和文件状态中做出正确、可审计且安全的操作，因此评测同时覆盖 Tool、Final State、Safety 与 Behavior。

## 2. Evaluation Scope

覆盖 Email、Calendar、Document、Spreadsheet、File / Drive、Contacts、Research、Cross-tool Workflow 与 Safety / Clarification / Failure 九类办公任务。

## 3. Evaluation Architecture

```text
Task → LangGraph Agent → Mock Tools → Mock Office Environment → Runtime State
     → Evaluation Harness → Rule / State / Task Grader → Review → Metrics / Bad Case / Regression
```

## 4. Dataset Evolution

- Smoke 20：工程冒烟和回归护栏。
- Development 50：开发期泛化、Bad Case 分流与单变量回归。
- Certification Formal 100：冻结后、独立环境中的一次正式盲测。

## 5. Mock Environment

环境提供 immutable base state、per-task isolated runtime、reset、权限限制、failure injection 与状态审计。Mock 设计用于验证评测方法，非真实企业系统。

## 6. Agent Architecture

采用 LangGraph 单 Agent：Agent Node 调用 LLM，Tool Node 执行 Mock Tools，状态保存消息与工具轨迹，Finalize 写入最终回复；最大步数限制为 20。

## 7. Evaluation Harness

批量运行器为每题创建隔离快照，保存 tool calls、最终回复与最终状态。评分层包含规则、状态与任务判断；高风险、澄清、确认、拒绝及异常结果进入复核记录。

## 8. Metrics

使用任务成功率、工具选择、状态正确性、澄清/确认准确性、安全失败率、高风险成功率、运行异常与关键失败等指标。它们共同避免“文字回答看起来正确、但状态已被错误修改”的误判。

## 9. Bad Case Methodology

Bad Case → Root Cause → Candidate Fix → 单变量 Regression → Keep / Rollback。Phase 9 明确区分 INFRA、EVAL_ARTIFACT 与 Agent 行为，不把基础设施错误计为能力失败。

## 10. Key Milestones

- Phase 6：20 题基线 17/20。
- Phase 7：Smoke 回归达到 20/20。
- Phase 8：Development 50 原始泛化结果 38/50。
- Phase 9：稳定 Development Baseline 42/50，Smoke 20/20，运行异常 0。
- Phase 10：保留无效 Formal v1 原始记录；修复评分器后，在独立 Certification Formal v2 完成 100/100 单次冻结盲测。

## 11. Formal Result

Certification Formal v2 使用冻结的 `agent_dev_optimized_v0.1`、`deepseek-v4-pro-0813`、独立 `formal_mock_env_v2.0` 与冻结评分器，一次运行 100 PASS、0 Runtime Error、0 Safety Failure、0 Critical Failure。运行后冻结文件哈希无变化。

## 12. Limitations

这是 Mock Office Environment；不是企业生产环境；只测试一个模型；100 题样本有限；Mock Tools 与真实 Gmail、Microsoft 365、OA/API 存在差异。Formal 100% 不代表真实生产环境或所有办公任务 100%。

## 13. Final Lessons

Agent Eval 不等于普通 QA：Final State 与安全约束同样重要；需把 INFRA、评测 Artifact 与 Agent Failure 分流；Dev 用于开发而 Formal 必须冻结；明确记录原始失败比“修掉历史记录”更可靠。
