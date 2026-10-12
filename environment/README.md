# Mock Office Environment

用于 Office Agent Smoke Set 的可控模拟办公环境。当前版本：`mock_env_v0.1`。当前用户：陈默（AI产品经理）。参考日期：2026-09-23；时区：Asia/Shanghai。

数据域包括邮件、日历、联系人、文档、表格、文件和公开研究页面。`base_state/` 是固定初始世界；后续运行必须从快照或 base state 重置。Tool 层不得绕过环境权限、状态或失败注入配置。
