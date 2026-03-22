# Cinemind 项目开发与 AI 助手规则总则

本文档合并了项目中的所有自定义规则，适用于 AI 助手（如 Antigravity AI 等）在协助开发时的全局行为准则。

## 1. 语言规则 (Language Rules)

在所有 agent 会话中，输出内容必须使用**简体中文**，包括：
- 代码注释（如用户未特别指明语言）
- 解释说明
- 错误诊断
- 计划文档（task.md、implementation_plan.md、walkthrough.md 等）
*技术术语（如函数名、命令、代码本身）保持原文，仅说明性文字翻译为中文。*

---

## 2. 基础开发规范

本文档详述了 Cinemind 项目中，无论是编写任何语言的代码或是配置文件时，都应当遵循的基础开发规则。更详细的“工程卓越性”标准请参考 [`.skills/general_programming_excellence/SKILL.md`](file:///d:/8-python-project/Cinemind/.skills/general_programming_excellence/SKILL.md)。

- **中文注释**：所有的代码注释、文档描述以中文作为首选语言。
- **自我解释的代码**：选择具有描述性的变量、函数和类名，使其能够清楚地表明自身用途。
- **模块化设计**：将复杂问题拆分为更小、可复用的代码块（如函数/类/模块）。
- **统一的代码风格**：在整个项目中保持一致的编码风格，并尊重当前编辑文件已有的规范。
- **快速失败 (Fail Fast)**：编写遇到预期外情况时尽早报错的代码，坚决避免静默失败（Silent Failures）。
- **不要重复自己 (DRY)**：将通用的逻辑提炼出来，避免出现重复的代码块。
- **保持简单 (KISS)**：优先采用简单、可读性强的方案，而不是试图编写看似“聪明”实则晦涩难懂的代码。

---

## 3. Python 最佳实践
# Cinemind 项目开发与 AI 助手规则总则

本文档合并了项目中的所有自定义规则，适用于 AI 助手（如 Antigravity AI 等）在协助开发时的全局行为准则。

## 1. 语言规则 (Language Rules)

在所有 agent 会话中，输出内容必须使用**简体中文**，包括：
- 代码注释（如用户未特别指明语言）
- 解释说明
- 错误诊断
- 计划文档（task.md、implementation_plan.md、walkthrough.md 等）
*技术术语（如函数名、命令、代码本身）保持原文，仅说明性文字翻译为中文。*

---

## 2. 基础开发规范

本文档详述了 Cinemind 项目中，无论是编写任何语言的代码或是配置文件时，都应当遵循的基础开发规则。更详细的“工程卓越性”标准请参考 [`.skills/general_programming_excellence/SKILL.md`](file:///d:/8-python-project/Cinemind/.skills/general_programming_excellence/SKILL.md)。

- **中文注释**：所有的代码注释、文档描述以中文作为首选语言。
- **自我解释的代码**：选择具有描述性的变量、函数和类名，使其能够清楚地表明自身用途。
- **模块化设计**：将复杂问题拆分为更小、可复用的代码块（如函数/类/模块）。
- **统一的代码风格**：在整个项目中保持一致的编码风格，并尊重当前编辑文件已有的规范。
- **快速失败 (Fail Fast)**：编写遇到预期外情况时尽早报错的代码，坚决避免静默失败（Silent Failures）。
- **不要重复自己 (DRY)**：将通用的逻辑提炼出来，避免出现重复的代码块。
- **保持简单 (KISS)**：优先采用简单、可读性强的方案，而不是试图编写看似“聪明”实则晦涩难懂的代码。

---

## 3. Python 最佳实践

本文档详述了为 Cinemind 项目编写 Python 代码时应当遵循的具体规则。

- **中文环境**：编写的所有注释、配置说明文件，均使用中文。
- **符合 PEP 8 规范**：格式编排、命名习惯和代码结构均应遵循标准的 Python 代码风格指南（PEP 8）。
- **类型提示 (Type Hinting)**：为所有函数的参数及返回值使用类型提示（利用原生 Python 类型特性或 `typing` 模块）。
- **文档字符串 (Docstrings)**：对于所有的公共模块、类和方法，都需添加标准的文档字符串（如 Google 或 Sphinx 风格）。要求全部使用中文书写。
- **逐行详尽注释 (Line-by-line Comments)**：对于业务逻辑复杂的模块（如 RAG 链、自定义 Service 等），强制要求执行“语句级”详细中文注释。注释应解释“为什么这么做”以及“底层逻辑”，而不仅是简单翻译。

- **异常处理**：
  - 应当捕获特定的异常，而非使用裸露的 `except:` 或者随意捕获宽泛的 `Exception`（除非在极端必要的情况下）。
  - 无论何时抛出或捕获异常，都应提供意义明确的错误提示信息。
- **虚拟环境**：始终依靠虚拟环境（如 venv/conda）来隔离项目相关的外部依赖。
- **路径操作**：推荐使用 `pathlib` 库进行所有的文件系统路径拼接、处理，而不是较老旧的 `os.path` 模块。
- **字符串格式化**：相比拼接等旧式格式化方法，始终优先使用 f 字符串（`f"..."`）。

---

## 4. 自动操作日志记录 (Operation Logging)

每当 AI 助手完成一次实质性的操作（包括但不限于代码修改、文件创建、命令运行、Git 提交等），**必须**立即更新记录。

### 强制要求
1. **唯一性**：操作完成后，在告知用户之前，优先更新记录。**严禁覆盖旧的记录文件**，应根据任务内容创建唯一的文件名。
2. **命名格式**：目标文件命名推荐为 `walkthrough_[任务描述]_[日期].md`。或在项目根目录的 `walkthrough.md` 中以追加（Append）模式记录，但需确保时间戳清晰。
3. **格式要素**：
   - 标题必须包含 `[YYYY-MM-DD HH:mm:ss]`。
   - 逻辑必须分层（操作描述、改动详情、验证结果）。
   - 使用 Markdown 检查清单 `- [x]` 记录验证。
4. **归档要求**：记录应按时间顺序保留在项目目录中，作为项目的历史证据。

> [!IMPORTANT]
> 记录日志不是可选的，作为工作流程中不可分割的一部分。它旨在让用户随时掌握项目的历史变迁。

---

## 6. LangChain 会话持久化规范 (Memory Persistence)

在实现长短期记忆（Long-Term Memory）时，必须遵循以下性能与安全规范：

- **优先使用批量写入**：必须重写 `add_messages`（复数形式）而非单个 `add_message`。
- **官方序列化**：统一使用 `langchain_core.messages` 中的 `message_to_dict` 和 `messages_from_dict` 进行数据转换。
- **Pydantic 校验**：所有持久化到磁盘或数据库的消息，必须通过 Pydantic 模型进行结构校验。
- **路径安全**：严禁直接将 `session_id` 作为文件名，必须进行合法性检查（如 `isalnum()`）以防止路径穿越攻击。
- **Streamlit 异步稳定性**：在 Streamlit 环境下初始化具备异步 I/O 的组件（如 Chroma, LangChain 引擎）时，必须执行 `asyncio.get_running_loop()` 校验补丁，并配合 `st.cache_resource` 实现并发安全与资源单例化，严禁 Event Loop 闭环后强行复用报错。
- **视觉化日志规范**：项目必须采用具备色彩分级的终端日志系统，关键节点应配合 Emoji（如 ✅, ❌, 🧠）进行语义化标记。详细标准见 [`.skills/logging_excellence/SKILL.md`](file:///d:/1-application/python_project/Cinemind/.skills/logging_excellence/SKILL.md)。
- **技能参考**：详细实现细节请参考 [`.skills/langchain_memory_persistence/SKILL.md`](file:///d:/8-python-project/Cinemind/.skills/langchain_memory_persistence/SKILL.md) 及 [`.skills/streamlit_rag_stability/SKILL.md`](file:///d:/8-python-project/Cinemind/.skills/streamlit_rag_stability/SKILL.md)。
