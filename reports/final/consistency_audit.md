# 数字一致性审计

| 项目 | 历史/最终数字 | 状态 | 说明 |
|---|---:|---|---|
| Phase 6 | 17/20 | 历史基线 | 初始动态基线 |
| Phase 7 | 20/20 | 历史回归 | Smoke 修复后结果 |
| Phase 8 | 38/50 | 历史原始泛化 | Development 原始结果 |
| Phase 9 | 42/50 | 最终 Dev 基线 | Smoke 20/20，运行异常 0 |
| Formal v1 | 0/100 Raw | 无效历史记录 | Grader null-error，原始日志保留 |
| Formal v1 离线重评 | 76 PASS / 24 PARTIAL | 诊断证据 | 不替代 Raw Formal |
| Formal v2 | 100/100 | 最终认证结果 | 独立冻结盲测 |
| Formal v2 Runtime / Safety / Critical | 0 / 0 / 0 | 最终认证指标 | 已保存 Gate Report |

**结论：** 关键数字一致。不同数字代表不同阶段、不同数据集或历史无效运行；未覆盖历史记录。
