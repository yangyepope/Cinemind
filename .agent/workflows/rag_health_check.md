---
description: 对当前的 RAG 链条进行全方位的底层健康检查与优化建议
---

# RAG 链路健康检查 (RAG Health Check)

本工作流旨在自动分析 `src/03-RAG项目实战/core/rag_chain.py` 中的 LCEL 逻辑，并根据项目的底层架构规范提供优化建议。

## 执行步骤

1.  **代码静态扫描**
    读取 `src/03-RAG项目实战/core/rag_chain.py` 源码，识别所有的 `Runnable` 组件。

2.  **规范对齐检查**
    对比 `.skills/source_code_teardown` 和 `general_programming_excellence` 中的规范：
    -   检查是否使用了 `RunnablePassthrough.assign` 进行上下文注入。
    -   检查是否正确配置了 `RunnableWithMessageHistory`。
    -   检查是否包含必要的 `inspect_data` 观察哨。

3.  **性能与安全性评估**
    -   评估 `retriever` 的调用深度。
    -   检查是否存在在链条中直接修改全局变量的隐患。

4.  **输出优化报告**
    在对话框中输出一份包含“现状解析”、“潜在风险”和“优化代码片段”的详细报告。

---

// turbo
## 触发自检
如果你现在想立刻运行此检查，请直接回复：“执行 RAG 健康检查”。
