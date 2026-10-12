# Certification Formal Evaluation Report v2.0

## Executive Summary

A fresh, independent Formal 100 was frozen and run once with `agent_dev_optimized_v0.1` and `deepseek-v4-pro-0813`. All 100 tasks passed. The invalid Formal v1 raw result remains unchanged and is not used here.

## Setup and Freeze

Dataset `certification_formal_v2.0`; environment `formal_mock_env_v2.0`; batch `FORMAL-v2-deepseek-v4-pro-0813`; SHA256 freeze files: 20; hash mismatches after run: 0.

## Overall Results

PASS 100; PARTIAL 0; FAIL 0; Runtime Error 0; Safety Failure 0; Critical Failure 0.

## By Category

| Category | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| Email | 12/12 | 0 | 0 |
| Calendar | 10/10 | 0 | 0 |
| Document | 10/10 | 0 | 0 |
| Spreadsheet | 10/10 | 0 | 0 |
| File / Drive | 10/10 | 0 | 0 |
| Contacts | 6/6 | 0 | 0 |
| Research | 7/7 | 0 | 0 |
| Cross-tool Workflow | 25/25 | 0 | 0 |
| Safety / Clarification / Failure | 10/10 | 0 | 0 |

## By Difficulty

| Difficulty | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| L1 | 10/10 | 0 | 0 |
| L2 | 25/25 | 0 | 0 |
| L3 | 40/40 | 0 | 0 |
| L4 | 25/25 | 0 | 0 |

## By Tool Depth

| Depth | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| 1 | 35/35 | 0 | 0 |
| 2 | 35/35 | 0 | 0 |
| 3 | 30/30 | 0 | 0 |

## By Expected Behavior

| Behavior | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| EXECUTE | 46/46 | 0 | 0 |
| REPORT | 22/22 | 0 | 0 |
| CLARIFY | 10/10 | 0 | 0 |
| CONFIRM | 12/12 | 0 | 0 |
| REFUSE | 10/10 | 0 | 0 |

## By Risk

| Risk | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| LOW | 25/25 | 0 | 0 |
| MEDIUM | 45/45 | 0 | 0 |
| HIGH | 30/30 | 0 | 0 |

## Review, Bad Cases, and Safety

52 required HIGH-risk/CLARIFY/CONFIRM/REFUSE records were reviewed. There are no FAIL/PARTIAL bad cases, no safety failures, and no critical failures.

## Development vs Formal

Development 50 measured 42/50 raw PASS. Certification Formal v2 is a distinct, newly frozen set; results are not paired or directly comparable. Its complete 100/100 run provides a clean certification measurement under this mock environment.

## Limitations

This remains a Mock Office Environment with finite samples; it is not a live Gmail, Microsoft 365, or OA integration, and one-model performance does not represent all models.

## Conclusion

Certification Formal v2 meets the evaluation gate. No Formal-after-run Agent optimization or rerun was performed.
