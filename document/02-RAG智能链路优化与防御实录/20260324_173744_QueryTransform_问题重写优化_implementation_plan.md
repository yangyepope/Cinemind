# Implementation Plan: RAG Chain Optimization (2026-03-24)

本方案旨在解决 `rag_health_check` 识别出的“检索单一性”与“提示词鲁棒性”风险。

## 用户审核项

> [!IMPORTANT]
> - **问题重写**：增加一次额外的 LLM 调用，将模糊提问重写为独立查询。
> - **防御性分支**：若检索结果为空，直接返回提示，跳过后续推理。

## 拟定变更

### RAG 推理引擎

#### [修改] [rag_chain.py](file:///d:/8-python-project/Cinemind/src/03-RAG项目实战/core/rag_chain.py)

1.  **查询重写逻辑**：
    -   新增 `rewrite_prompt` 指令，要求 LLM 基于历史生成独立查询。
    -   构造 `self.rewrite_chain`。
2.  **分支路由逻辑**：
    -   重构 `self.rag_chain` 使用 `RunnableBranch`。
    -   条件：`lambda x: not x["context"].strip()` -> 返回预设话术。

## 验证计划

1.  **手动测试**：输入“那另一个呢？”验证重写效果。
2.  **边界测试**：输入无关问题验证空上下文熔断。
