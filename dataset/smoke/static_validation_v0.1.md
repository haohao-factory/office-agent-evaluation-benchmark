# Smoke Set Static Validation v0.1

## Per-task Results

| Task ID | Agent Necessity | Clarity | GT Judgeable | Behavior | Risk | Tool Coverage | Duplicate | Forbidden Actions | Result |
|---|---|---|---|---|---|---|---|---|---|
| SMK-001 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-002 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-003 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-004 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-005 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-006 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-007 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-009 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-010 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-011 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-012 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-013 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-014 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-015 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-016 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-017 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-018 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-019 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SMK-020 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## Gate Checks

- Agent Necessity PASS: 20/20
- GT Judgeable FAIL: 0/20
- Expected Behavior coverage: EXECUTE, REPORT, CLARIFY, CONFIRM, REFUSE — PASS
- Risk coverage: LOW, MEDIUM, HIGH — PASS
- Cross-tool tasks with two or more tool domains: 5/5 — PASS
- Pure template duplicates: 0 — PASS
- HIGH-risk tasks with forbidden actions: 3/3 — PASS
- Overall FAIL: 0
- Overall REVIEW: 0
- Difficulty distribution: L1=4, L2=6, L3=7, L4=3 — PASS

## Phase 2.1 Revision Summary

- Original result: PASS=12, REVIEW=8, FAIL=0.
- Revised tasks: SMK-003, SMK-008, SMK-010, SMK-012, SMK-014, SMK-015, SMK-016, SMK-017; SMK-011 was relabeled from L2 to L1 to correct the fixed difficulty distribution.
- The revised records specify deterministic object-selection constraints, result or final-state conditions, and forbidden actions without inventing Phase 3 mock IDs.
- Revised result: PASS=20, REVIEW=0, FAIL=0.
- Revised difficulty distribution: L1=4, L2=6, L3=7, L4=3.
- PHASE_2_GATE = PASS

No Mock Environment, Tool, Runner, Agent, or Baseline work has been started.
