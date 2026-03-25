# Cinemind 项目开发与 AI 助手规则总则 (Master Rules)

本文档定义了 Cinemind 项目的全局开发、架构及协作准则，适用于 AI 助手协助开发时的所有行为。

---

## 1. 语言与工作流规范 (Language & Workflow)

- **简体中文优先**：在所有 agent 会话和输出中，必须使用简体中文，包括代码注释、解释说明、错误诊断及所有计划文档（`task.md`、`implementation_plan.md`、`walkthrough.md` 等）。
- **技术术语保持原文**：函数名、库名、变量名等技术性称谓保持英文，仅解释性文字翻译。
- **自动操作日志 (Operation Logging)**：
    - 项目根目录下的 [walkthrough.md](file:///d:/8-python-project/Cinemind/walkthrough.md) 为唯一持久化操作记录。
    - 每项实质性改动后，必须以 `## [YYYY-MM-DD HH:mm:ss] 阶段名：任务短评` 格式追加记录识别改动及验证结果。
- **计划文档同步**：所有实施方案、任务清单等计划文档必须同步至 [document/](file:///d:/8-python-project/Cinemind/document/) 目录，命名遵循 `document/YYYYMMDD_[任务简述]_[文档类型].md`。

---

## 2. 编程标准与 Python 最佳实践 (Coding Standards)

- **模块化与 DRY**：将复杂逻辑拆分为可复用的最小单元。
- **快速失败 (Fail Fast)**：编写尽早报错的代码，坚决避免静默失败。
- **类型提示与规范**：Python 代码严格遵循 PEP 8，强制要求 Type Hinting。
- **中文文档字符串 (Docstrings)**：对于所有公共模块、类和方法，必须添加标准的 Google Style 中文文档字符串。
- **极致注释 (Why over What)**：针对业务逻辑复杂的模块，强制执行“逐行”详细中文注释。
- **环境与路径**：强制使用 `pathlib` 处理路径。

---

## 3. 高阶架构原则 (Architecture Rules)

- **分层与解耦**：遵循 **Clean Architecture** (整洁架构)。
- **依赖注入 (DI)**：深度集成 FastAPI 的 `Depends` (Annotated)。
- **异步优先**：所有 I/O 密集型操作必须使用 `async/await`。
- **Pydantic v2 核心**：核心业务数据传递强制使用 Pydantic 模型。
- **全局异常机制**：统一响应格式，由全局拦截器捕获自定义异常。

---

## 4. 需求分析与设计规范 (Analysis & Design)

- **先问后写 (Ask Before Coding)**：禁止立即编码。必须先进行 **MECE** 分析并确认模糊点。
- **多维度拆解**：从功能需求、非功能需求、边界条件三个维度分析。
- **架构对齐 (DDD)**：识别聚合根、实体和值对象。
- **源码拆解要求**：涉及源码解析时，必须输出 Mermaid 图示及性能对比表。

---

## 5. 专家化身与审计模式 (AI Personas)

AI 助手应能切换至以下专家身份：架构审核员、安全卫士、性能优化专家、压力测试员。

---

## 6. 技术栈最佳实践 (Tech Stack)

| 模块 | 推荐技术 | 说明 |
| :--- | :--- | :--- |
| **数据验证** | **Pydantic v2** | 极速解析。 |
| **可观测性** | **Loguru + Prometheus** | 日志与监控。 |
| **代码规范** | **Ruff + mypy** | 格式化与校验。 |
| **ORM 框架** | **SQLModel / SQLAlchemy 2.0+** | 异步支持。 |

---

> **结语**：总则旨在确保项目的高质量与可维护性。框架相关的特定细节（如 LangChain/Streamlit）请参考 [`.rules/04-框架特有规范.md`](file:///d:/8-python-project/Cinemind/.rules/04-框架特有规范.md)。
