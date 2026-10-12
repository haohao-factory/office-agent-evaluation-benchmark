# 5分钟项目介绍初稿

## 背景与问题

我独立完成了一个 Office Agent Evaluation Benchmark。传统准确率只看最终文本，但办公任务本质上是有状态的：检索来源、选择对象、写入状态、权限、外发和失败恢复都会影响质量。

## 设计

我将任务覆盖邮件、日历、文档、表格、文件、联系人、研究、跨工具和安全。任务按难度、风险、行为类型和工具深度分层。Smoke 20 用于工程守护，Development 50 用于开发和 Bad Case，独立 Formal 100 用于冻结盲测。

## Agent 与环境

Agent 使用 LangGraph 单 Agent Loop：Agent Node 产生工具调用，Tool Node 操作 Mock Environment，再回到 Agent Node，Finalize 写入结果。环境有 immutable base state、每题 runtime snapshot、权限控制和 failure injection。这样可以检查 Final State，而非仅依赖语言表述。

## 评测方法

Harness 保存工具轨迹、回复和最终状态。规则评分关注行为约束，状态评分关注写入是否正确，任务评分综合给出 PASS/PARTIAL/FAIL。高风险取消、外部发送、澄清、确认、拒绝和异常进入复核。Bad Case 用 Agent/Infra/Eval Artifact 三分法，而不是把所有 FAIL 都归因给模型。

## 代表性问题与回归

例如 timeout_after_commit：调用超时不代表未提交，正确策略是先搜索状态，避免重复创建。另一个例子是 Formal v1 的 Grader null-error：100 个 Raw 失败是评分器自身异常。我保留 raw evidence，修复并测试评分器，不重写历史结果；随后建立全新 Formal v2。

## Formal 与边界

Formal v2 在冻结数据、环境、Agent、模型、图、工具和评分器后，一次完成 100/100 PASS，安全、关键和运行异常均为 0。我不会把它说成生产成绩：项目仍是 Mock Environment、单模型和有限样本。它证明的是一套可复现的 Agent Eval 工作流，而不是现实企业系统已上线。
