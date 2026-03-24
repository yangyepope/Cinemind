# RAG Chain Optimization & Hardening Task List (2026-03-24)

- [x] 遵循项目规则：同步计划文档至 `document/` 文件夹
- [x] 实现问题重写逻辑 (Risk A: Query Transformation)
    - [x] 定义重写提示词 (Rewrite Prompt)
    - [x] 创建 `query_transform_chain`
    - [x] 集成至 `rag_chain`
- [x] 实现防御性分支逻辑 (Risk B: Defensive Branching)
    - [x] 定义“空上下文”熔断逻辑
    - [x] 使用 `RunnableBranch` 进行路由
    - [x] 验证 Token 节省与响应质量
- [x] 最终验证与归档
    - [x] 再次运行 `rag_health_check` 工作流
    - [x] 创建 `walkthrough.md` 记录
