# Cinemind 项目开发与 AI 助手规则总则

本文档定义了 Cinemind 项目的全局开发准则，适用于 AI 助手协助开发时的所有行为。

## 1. 语言与注释规范 (Language & Documentation)

- **简体中文优先**：在所有 agent 会话和输出中，必须使用简体中文，包括代码注释、解释说明、错误诊断及所有计划文档（task.md 等）。
- **技术术语保持原文**：函数名、库名、变量名等技术性称谓保持英文，仅解释性文字翻译。
- **模块文档 (Docstrings)**：对于所有公共模块、类和方法，必须添加标准的中文文档字符串（Google 或 Sphinx 风格）。要求全部使用中文。
- **逐行详尽注释 (Line-by-line Comments)**：对于业务逻辑复杂的模块（如 RAG 链、自定义 Service 等），强制要求执行“语句级”详细中文注释。注释应解释“为什么这么做”以及“底层逻辑”，而不仅是翻译代码。

---

## 2. 核心开发原则 (Core Development)

- **模块化设计**：将复杂逻辑拆分为可复用的最小单元。遵循 DRY (Don't Repeat Yourself) 原则。
- **快速失败 (Fail Fast)**：尽早捕获并显式处理预期的错误，坚决避免静默失败。
- **PEP 8 规范**：Python 代码必须严格遵循 PEP 8 命名习惯与结构编排（建议使用 `f-string` 处理字符串格式化）。
- **类型提示 (Type Hinting)**：强制要求为所有函数参数及返回值添加类型提示。

---

## 3. 源码拆解与架构分析规范 (Source Code Teardown)

每当涉及复杂源码拆解、核心机制解析或原理解析时，**必须**输出以下图示及分析：
- **静态类图** (`classDiagram`)：展示组件间的依赖与继承关系。
- **宏观时序图** (`sequenceDiagram`)：展示交互路径（用户 -> 拦截器 -> 执行器 -> 存储）。
- **逻辑流程图** (`graph TD`)：划分明确的执行阶段（环境准备、核心执行、后处理）。
- **底层表现对比**：使用表格对比不同实现方案的物理性能差异（如 I/O 次数）。

---

## 4. 自动化操作日志 (Operation Logging)

- **唯一主日志**：项目根目录下的 [walkthrough.md](file:///d:/8-python-project/Cinemind/walkthrough.md) 为项目唯一持久化操作记录。
- **记录格式**：每项实质性改动后，必须以 `## [YYYY-MM-DD HH:mm:ss] 阶段名：任务短评` 格式追加记录，包含操作描述、改动详情、验证结果。
- **清理习惯**：严禁创建冗余的临时日志文件。除 `walkthrough.md` 外的同类记录应在任务结束后及时清理。

---

## 5. 计划文档管理 (Planning Documentation)

- **同步要求**：所有实施方案 (`implementation_plan`)、任务清单 (`task`) 等计划类文档必须同步至 [document/](file:///d:/8-python-project/Cinemind/document/) 目录。
- **命名规范**：使用 `document/YYYYMMDD_[任务简述]_[文档类型].md` 格式进行存档。

---

## 6. 环境与安全规范 (Environment & Security)

- **路径操作**：强制使用 `pathlib` (Path) 处理路径，禁止使用字符串拼接或 `os.path`。
- **虚拟环境隔离**：始终确认并在项目根目录下的 `.venv` 或指定的虚拟环境中运行代码。
- **路径安全防护**：处理涉及用户输入（如 `session_id`）的文件路径时，必须执行非法字符过滤或 `isalnum()` 检查以防止路径穿越攻击。

---

## 7. LangChain 特色组件规范 (Specialized Components)

- **批量 I/O 优化**：自定义 `BaseChatMessageHistory` 子类必须重写 `add_messages` 批量方法，严禁退化为单次 I/O。
- **官方序列化**：统一使用 `message_to_dict` 和 `messages_from_dict` 以保留 MetaData。
- **Pydantic 数据建模**：持久化数据（如 JSON/DB 存储）必须通过 Pydantic 模型层进行结构校验。
- **Streamlit 异步稳定性**：在 Streamlit 环境下初始化具备异步 I/O 的组件（如 Chroma, LangChain 引擎）时，必须执行 `asyncio.get_running_loop()` 校验补丁，并配合 `st.cache_resource` 实现单例生命周期管理，以防止“Event loop is closed”报错。
