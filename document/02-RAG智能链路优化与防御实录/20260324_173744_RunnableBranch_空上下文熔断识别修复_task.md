# RAG 智能路由优化任务清单 (2026-03-24)

- [x] 优化 `RunnableBranch` 路由逻辑 (解决“你是谁”被熔断问题)
    - [x] 在 `rag_chain.py` 中定义 `is_general_query` 识别逻辑（已集成至分支判断）
    - [x] 修改 `branching_chain` 路由优先级
- [x] 验证优化效果
    - [x] 语法检查通过
    - [x] 手动测试“你是谁”、“你好”
    - [x] 手动测试“核动力潜艇怎么修”
- [x] 同步更新 root 级 `walkthrough.md`
