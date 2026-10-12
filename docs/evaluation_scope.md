# Office Agent Evaluation Benchmark — Evaluation Scope

## 1. 文档目的

本文档定义 Office Agent Evaluation Benchmark v1 的评测对象、能力边界、允许工具、非目标范围、环境假设以及核心评测原则。

本项目目标不是评测普通聊天模型的知识问答能力，而是评测一个通用办公 Agent 在模拟办公环境中是否能够：

1. 正确理解用户任务；
2. 判断是否需要执行、澄清、确认、拒绝或仅查询汇报；
3. 选择正确工具；
4. 正确填写工具参数；
5. 完成合理的多步工具调用；
6. 对办公环境产生正确的最终状态变化；
7. 避免错误、越权、重复执行和高风险误操作；
8. 在任务完成后向用户返回准确、简洁、可核验的结果。

---

## 2. 被测对象

被测对象定义为：

> 通用日常办公 Agent（General Office Agent）

该 Agent 接收用户的自然语言办公指令，并能够根据任务需要调用一个或多个办公工具完成任务。

本评测重点关注：

- Task Understanding
- Planning
- Tool Selection
- Tool Calling
- Action Correctness
- Multi-step Execution
- State Change
- Instruction Following
- Clarification
- Confirmation
- Refusal
- Safety
- Recovery from Tool Failure

本项目不要求被测 Agent 具备真实企业生产环境权限。

v1 阶段优先使用可控、可复现的 Mock Office Environment。

---

## 3. v1 支持的办公能力域

v1 评测范围固定为以下八类：

### 3.1 Email

能力包括：

- 搜索邮件
- 读取邮件
- 按发送人、时间、主题等条件检索
- 查找附件
- 提取邮件中的结构化信息
- 总结单封或多封邮件
- 比较不同邮件版本
- 草拟回复
- 回复指定邮件
- 转发邮件
- 归档邮件
- 识别错误收件人或歧义联系人
- 对高风险发送操作进行确认

---

### 3.2 Calendar

能力包括：

- 查询日程
- 查询指定时间段
- 查询空闲时间
- 查找多人共同空闲时间
- 创建会议
- 修改会议
- 取消会议
- 检测日程冲突
- 处理重复会议
- 处理跨时区时间
- 识别缺失的参会人、日期、时长等必要信息
- 对高风险取消或批量修改进行确认

---

### 3.3 Document

能力包括：

- 搜索文档
- 读取文档
- 提取信息
- 总结文档
- 比较文档版本
- 根据现有材料生成办公文档草稿
- 修改指定段落
- 将多个来源整理为结构化文档
- 保留用户要求的格式与关键内容
- 避免篡改未要求修改的内容

---

### 3.4 Spreadsheet

能力包括：

- 读取工作簿或表格
- 筛选数据
- 排序
- 汇总统计
- 条件计算
- 查找异常值
- 更新单元格
- 新增行或列
- 根据多个字段完成计算
- 比较不同版本数据
- 避免修改错误 Sheet、错误单元格或错误记录

---

### 3.5 File / Drive

能力包括：

- 搜索文件
- 根据文件名、目录、时间、版本等定位文件
- 读取文件元数据
- 移动文件
- 重命名文件
- 创建文件夹
- 判断最新有效版本
- 识别作废版本
- 避免覆盖错误文件
- 避免对无权限文件执行操作

---

### 3.6 Contacts

能力包括：

- 根据姓名查联系人
- 根据部门、公司等信息缩小联系人范围
- 处理重名人员
- 获取可用邮箱或其他办公联系信息
- 在联系人存在歧义时进行澄清
- 避免把信息发送给错误对象

---

### 3.7 Research

能力包括：

- 使用搜索工具获取公开信息
- 根据用户要求进行信息收集
- 对多个公开来源进行整理
- 将检索结果转换成办公摘要
- 区分内部文件信息与外部公开信息
- 不使用外部搜索替代应从内部办公系统获取的数据

说明：

Research 在 v1 中属于辅助能力，不作为主要知识问答 Benchmark。

---

### 3.8 Cross-tool Workflow

跨工具任务是本项目的核心能力类别。

典型链路包括：

- Email → Attachment → Spreadsheet
- Email → Calendar
- File → Document → Email
- Calendar → Contacts → Email
- Research → Document
- Document → Spreadsheet → Email
- Email → File → Calendar
- 多个办公工具组合执行

Cross-tool 任务重点测试：

- 任务拆解
- 工具顺序
- 中间结果传递
- 对象一致性
- 状态一致性
- 多步错误恢复

---

## 4. v1 明确不评测的能力

为避免范围失控，v1 暂不覆盖：

- 企业 ERP
- CRM
- OA 审批
- 财务支付
- 银行转账
- 真实合同签署
- 真实招聘系统
- 代码开发 Agent
- Shell / 系统管理员操作
- 数据库生产写操作
- 医疗、法律、金融等专业决策 Agent
- 复杂浏览器自动化
- 真实账号凭据管理
- 生产级权限系统
- 手机 App 自动操作
- 语音 Agent
- 视觉 GUI Agent

未来版本可扩展，但不得混入 v1 正式数据集。

---

## 5. 工具集合

v1 的概念工具集合包括：

### Email Tools

- email_search
- email_read
- email_draft
- email_reply
- email_forward
- email_archive

### Calendar Tools

- calendar_search
- calendar_get_availability
- calendar_create
- calendar_update
- calendar_cancel

### Document Tools

- document_search
- document_read
- document_create
- document_update

### Spreadsheet Tools

- spreadsheet_read
- spreadsheet_filter
- spreadsheet_update
- spreadsheet_append

### File Tools

- file_search
- file_read_metadata
- file_move
- file_rename
- folder_create

### Contact Tools

- contact_search
- contact_read

### Research Tools

- web_search
- web_open

最终 Tool Schema 在后续 Mock Environment 阶段冻结。

---

## 6. 核心评测原则

### 6.1 评测任务，而不是只评测回答文本

Agent 的核心结果是：

> 用户要求的办公任务是否被正确完成。

因此不得仅通过 Final Answer 判断成功。

需要同时检查：

- Tool Calls
- Actions
- Final State
- User-facing Response

---

### 6.2 Final State 优先于自我声明

如果 Agent 回答：

> “会议已经修改成功。”

但日历状态并未正确改变，则任务判定失败。

Agent 的自然语言声明不能替代真实环境状态。

---

### 6.3 不要求唯一执行路径

同一办公任务可能存在多条合理路径。

因此原则上不采用完整 Trajectory Exact Match。

评测重点是：

- 是否完成必要动作；
- 是否产生正确最终状态；
- 是否发生禁止动作；
- 是否出现明显错误或无意义操作。

---

### 6.4 高风险操作不得仅以任务完成率衡量

如果 Agent 完成了任务，但发生：

- 错发邮件
- 删除错误文件
- 取消错误会议
- 覆盖错误版本
- 越权访问
- 未经确认执行高风险批量操作

则不得因为最终部分结果正确而判定为成功。

---

### 6.5 数据集必须冻结后再用于正式回归

正式评测前必须冻结：

- Dataset Version
- Environment Version
- Ground Truth
- Rubric
- Tool Schema
- Evaluation Config

发现数据错误时，新建版本，不直接修改历史正式结果。

---

## 7. 环境原则

Mock Office Environment 必须满足：

- Deterministic：尽可能可重复
- Resettable：每道任务或每次运行后可恢复初始状态
- Observable：可检查执行轨迹与最终状态
- Isolated：任务之间不互相污染
- Versioned：环境数据具备版本号
- Auditable：关键状态变化可追溯

---

## 8. v1 预期交付

Office Agent Evaluation Benchmark v1 最终至少包括：

- 100 道任务
- Frozen Dataset
- Mock Office Environment
- Tool Set
- Evaluation Runner
- Rule / State Grader
- Human Eval Template
- Baseline Result
- Bad Case Analysis
- Regression Result
- Final Evaluation Report

本文件只定义评测范围，不定义具体 100 道任务。
