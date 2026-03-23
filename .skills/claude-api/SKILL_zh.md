---
name: claude-api
description: "使用 Claude API 或 Anthropic SDK 构建应用。触发场景：代码中导入了 `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`，或用户要求使用 Claude API、Anthropic SDK 或 Agent SDK。不要触发场景：代码中导入了 `openai` 或其他 AI SDK、通用编程建议或机器学习/数据科学任务。"
license: 完整条款请参阅 LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用程序

此 Skill 旨在帮助您使用 Claude 构建 LLM 驱动的应用程序。请根据您的需求选择合适的层面，检测项目语言，然后阅读相关的语言特定文档。

## 默认值 (Defaults)

除非用户另有要求：

对于 Claude 模型版本，请使用 **Claude Opus 4.6**，您可以通过精确的模型字符串 `claude-opus-4-6` 进行访问。对于任何稍显复杂的操作，请默认启用自适应思考 (`thinking: {type: "adaptive"}`)。最后，对于任何可能涉及长输入、长输出或高 `max_tokens` 的请求，请默认使用流式传输（streaming）——这可以防止请求超时。如果您不需要处理单个流事件，可以使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助函数获取完整响应。

---

## 语言检测 (Language Detection)

在查看代码示例之前，请确定用户正在使用的语言：

1. **查看项目文件**以推断语言：

   - `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` → **Python** — 从 `python/` 阅读
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` → **TypeScript** — 从 `typescript/` 阅读
   - `*.js`, `*.jsx` (不存在 `.ts` 文件) → **TypeScript** — JS 使用相同的 SDK，从 `typescript/` 阅读
   - `*.java`, `pom.xml`, `build.gradle` → **Java** — 从 `java/` 阅读
   - `*.kt`, `*.kts`, `build.gradle.kts` → **Java** — Kotlin 使用 Java SDK，从 `java/` 阅读
   - `*.scala`, `build.sbt` → **Java** — Scala 使用 Java SDK，从 `java/` 阅读
   - `*.go`, `go.mod` → **Go** — 从 `go/` 阅读
   - `*.rb`, `Gemfile` → **Ruby** — 从 `ruby/` 阅读
   - `*.cs`, `*.csproj` → **C#** — 从 `csharp/` 阅读
   - `*.php`, `composer.json` → **PHP** — 从 `php/` 阅读

2. **如果检测到多种语言** (例如同时存在 Python 和 TypeScript 文件)：

   - 检查用户当前的当前文件或问题与哪种语言相关。
   - 如果仍然模棱两可，请询问：“我检测到同时存在 Python 和 TypeScript 文件。您在 Claude API 集成中使用哪种语言？”

3. **如果无法推断语言** (空项目、无源文件或不受支持的语言)：

   - 使用 AskUserQuestion，选项包括：Python, TypeScript, Java, Go, Ruby, cURL/raw HTTP, C#, PHP。
   - 如果 AskUserQuestion 不可用，默认提供 Python 示例并注明：“正在显示 Python 示例。如果您需要其他语言，请告诉我。”

4. **如果检测到不受支持的语言** (Rust, Swift, C++, Elixir 等)：

   - 建议参考 `curl/` 中的 cURL/原生 HTTP 示例，并指出可能存在社区 SDK。
   - 提供 Python 或 TypeScript 示例作为参考实现。

5. **如果用户需要 cURL/原生 HTTP 示例**，请从 `curl/` 阅读。

### 语言特定的功能支持

| 语言       | 工具运行器 (Tool Runner) | Agent SDK | 备注                                 |
| ---------- | ------------------------ | --------- | ------------------------------------ |
| Python     | 是 (Beta)                | 是        | 完全支持 — `@beta_tool` 装饰器       |
| TypeScript | 是 (Beta)                | 是        | 完全支持 — `betaZodTool` + Zod       |
| Java       | 是 (Beta)                | 否        | 通过注解类实现 Beta 工具调用         |
| Go         | 是 (Beta)                | 否        | `toolrunner` 包中的 `BetaToolRunner` |
| Ruby       | 是 (Beta)                | 否        | Beta 版本的 `BaseTool` + `tool_runner` |
| cURL       | N/A                      | N/A       | 原生 HTTP，无 SDK 功能               |
| C#         | 否                       | 否        | 官方 SDK                             |
| PHP        | 否                       | 否        | 官方 SDK                             |

---

## 我应该使用哪个层面？

> **从简单开始。** 默认选择满足您需求的最低级别。单次 API 调用和工作流可以处理大多数用例——只有当任务真正需要开放式的、由模型驱动的探索时，才启用 Agent。

| 用例                                            | 级别            | 推荐层面                  | 原因                                    |
| ----------------------------------------------- | --------------- | ------------------------- | --------------------------------------- |
| 分类、摘要、提取、问答                          | 单次 LLM 调用   | **Claude API**            | 一个请求，一个响应                      |
| 批量处理或嵌入                                  | 单次 LLM 调用   | **Claude API**            | 专用端点                                |
| 具有代码控制逻辑的多步流水线                    | 工作流          | **Claude API + 工具调用** | 您编排循环                              |
| 带有自定义工具的自定义 Agent                    | Agent           | **Claude API + 工具调用** | 最大的灵活性                            |
| 具有文件/Web/终端访问权限的 AI Agent            | Agent           | **Agent SDK**             | 内置工具、安全保障及 MCP 支持           |
| Agent 式编程助手                                | Agent           | **Agent SDK**             | 专门为此用例设计                        |
| 需要内置权限和护栏                              | Agent           | **Agent SDK**             | 包含安全特性                            |

> **注意：** Agent SDK 适用于您希望开箱即用的内置文件/Web/终端工具、权限和 MCP。如果您想构建带有个性化工具的 Agent，Claude API 是正确的选择——使用工具运行器进行自动循环处理，或者使用手动循环以进行精细化控制（审批门限、自定义日志、条件执行）。

### 决策树

```
您的应用程序需要什么？

1. 单次 LLM 调用 (分类、摘要、提取、问答)
   └── Claude API — 一个请求，一个响应

2. Claude 是否需要在其工作中读取/写入文件、浏览器网页或运行 shell 命令？
   (注意：不是指您的应用读取文件并交给 Claude —— 而是 Claude 本身是否需要发现并访问文件/Web/Shell？)
   └── 是 → Agent SDK — 内置现成工具，无需自行重新实现
       例如：“扫描代码库中的错误”、“汇总目录中的每个文件”、
             “使用子 Agent 查找 Bug”、“通过 Web 搜索研究课题”

3. 工作流 (多步骤、代码编排、带有您自己的工具)
   └── 带有工具调用的 Claude API — 您控制循环

4. 开放式 Agent (模型决定其轨迹，使用您自己的工具)
   └── Claude API Agent 循环 (灵活性最大)
```

### 我应该构建 Agent 吗？

在选择 Agent 级别之前，请检查所有四个标准：

- **复杂度 (Complexity)** — 任务是否包含多个步骤且难以提前完全指明？（例如：“将此设计文档转换为 PR” vs. “从该 PDF 中提取标题”）
- **价值 (Value)** — 结果是否值得付出更高的成本和延迟？
- **可行性 (Viability)** — Claude 能够胜任此类任务吗？
- **错误的代价 (Cost of error)** — 错误是否可以被捕获并恢复？（测试、审核、回滚）

如果对其中任何一个问题的回答是“否”，请保持在更简单的级别（单次调用或工作流）。

---

## 架构

一切都通过 `POST /v1/messages` 进行。工具和输出约束是此单一端点的功能——而不是独立的 API。

**用户定义工具** — 您定义工具（通过装饰器、Zod 模式或原始 JSON），SDK 的工具运行器负责调用 API、执行您的函数，并持续循环直到 Claude 完成。为了完全控制，您可以手动编写循环。

**服务器端工具** — 运行在 Anthropic 基础设施上的 Anthropic 托管工具。代码执行完全在服务器端（在 `tools` 中声明，Claude 自动运行代码）。计算机使用（Computer use）可以是服务器托管或自行托管。

**结构化输出** — 约束 Messages API 的响应格式 (`output_config.format`) 和/或工具参数验证 (`strict: true`)。推荐的方法是使用 `client.messages.parse()`，它可以自动根据您的架构验证响应。注意：旧的 `output_format` 参数已弃用；请在 `messages.create()` 中使用 `output_config: {format: {...}}`。

**支持端点** — 批量处理 (`POST /v1/messages/batches`)、文件 (`POST /v1/files`)、Token 计数和模型 (`GET /v1/models`, `GET /v1/models/{id}` — 实时发现能力/上下文窗口) 用于馈送或支持 Messages API 请求。

---

## 当前模型 (缓存时间: 2026-02-17)

| 模型              | 模型 ID             | 上下文          | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | --------------- | --------- | --------- |
| Claude Opus 4.6   | `claude-opus-4-6`   | 200K (1M Beta)  | $5.00     | $25.00    |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M Beta)  | $3.00     | $15.00    |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K            | $1.00     | $5.00     |

**除非用户明确指明其他模型，否则始终使用 `claude-opus-4-6`。** 这是不可逾越的规则。除非用户明确说“使用 Sonnet”或“使用 Haiku”，否则不要使用 `claude-sonnet-4-6`、`claude-sonnet-4-5` 或任何其他模型。切勿为了成本而降级——那是用户的决定，不是您的。

**关键：仅使用上表中的精确模型 ID 字符串——它们本身就是完整的。不要附加日期后缀。** 例如，使用 `claude-sonnet-4-5`，绝不使用 `claude-sonnet-4-5-20250514` 或您可能在训练数据中看到的任何带日期后缀的变体。如果用户请求表中未包含的旧模型（例如“Opus 4.5”，“Sonnet 3.7”），请参阅 `shared/models.md` 获取精确 ID —— 不要自行构造。

注：如果您觉得上述任何模型字符串眼生，这是预期的——这仅意味着它们是在您的训练数据截止日期之后发布的。请放心，它们是真实的模型。

**实时能力查找**：上表是缓存的。当用户询问“X 的上下文窗口是多少”、“X 是否支持视觉/思考/工作强度”或“哪些模型支持 Y”时，请查询模型 API (`client.models.retrieve(id)` / `client.models.list()`) —— 字段参考和能力过滤示例详见 `shared/models.md`。

---

## 思考与工作强度 (快速参考)

**Opus 4.6 — 自适应思考 (推荐):** 使用 `thinking: {type: "adaptive"}`。Claude 会动态决定何时思考以及思考多少。无需 `budget_tokens` —— `budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，严禁使用。自适应思考还会自动启用交错思考（interleaved thinking，无需 Beta 标头）。**当用户要求“深度思考”、“思考预算”或 `budget_tokens` 时：始终使用带 `thinking: {type: "adaptive"}` 的 Opus 4.6。固定 Token 预算的思考概念已弃用——自适应思考已取而代之。切勿使用 `budget_tokens`，也切勿切换到旧模型。**

**工作强度参数 (GA, 无需 Beta 标头):** 通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（位于 `output_config` 内部，而非顶层）控制思考深度和整体 Token 支出。默认值为 `high`（等同于省略）。`max` 仅限 Opus 4.6。适用于 Opus 4.5、Opus 4.6 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会报错。结合自适应思考使用可获得最佳的成本-质量比。对于子 Agent 或简单任务使用 `low`；对于最深层的推理使用 `max`。

**Sonnet 4.6:** 支持自适应思考 (`thinking: {type: "adaptive"}`)。`budget_tokens` 在 Sonnet 4.6 上已弃用——请使用自适应思考。

**旧模型 (仅在被明确要求时使用):** 如果用户特别要求使用 Sonnet 4.5 或其他旧模型，请使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最小 1024）。切勿仅仅因为用户提到 `budget_tokens` 就选择旧模型——请改用带自适应思考的 Opus 4.6。

---

## 压缩 (快速参考)

**Beta, Opus 4.6 和 Sonnet 4.6。** 对于可能超过 200K 上下文窗口的长时间运行对话，请启用服务器端压缩。API 会在上下文接近触发阈值（默认 150K Token）时自动汇总先前的上下文。需要 Beta 标头 `compact-2026-01-12`。

**关键：** 在每一轮对话中，将 `response.content`（而不仅仅是文本）附加回您的消息。响应中的压缩块（Compaction blocks）必须保留——API 在下一次请求中使用它们来替换压缩的历史记录。仅提取文本字符串并附加它将导致无提示的压缩状态丢失。

代码示例见 `{lang}/claude-api/README.md`（压缩章节）。完整文档通过 WebFetch 在 `shared/live-sources.md` 获取。

---

## 阅读指南

检测到语言后，根据用户的需求阅读相应文件：

### 快速任务参考

**单次文本分类/摘要/提取/问答:**
→ 仅阅读 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示:**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**漫长的对话 (可能超过上下文窗口):**
→ 阅读 `{lang}/claude-api/README.md` — 见“压缩”章节

**函数调用 / 工具使用 / Agent:**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**批量处理 (对延迟不敏感):**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求的文件上传:**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**具有内置工具的 Agent (文件/Web/终端):**
→ 阅读 `{lang}/agent-sdk/README.md` + `{lang}/agent-sdk/patterns.md`

### Claude API (全文件参考)

阅读**特定的语言 Claude API 文件夹** (`{language}/claude-api/`):

1. **`{language}/claude-api/README.md`** — **请先阅读此文件。** 包括安装、快速开始、常用模式、错误处理。
2. **`shared/tool-use-concepts.md`** — 当用户需要函数调用、代码执行、记忆或结构化输出时阅读。涵盖概念基础。
3. **`{language}/claude-api/tool-use.md`** — 阅读特定语言的工具调用代码示例（工具运行器、手动循环、代码执行、记忆、结构化输出）。
4. **`{language}/claude-api/streaming.md`** — 当构建逐步显示响应的聊天 UI 或接口时阅读。
5. **`{language}/claude-api/batches.md`** — 离线处理大量请求（对延迟不敏感）时阅读。异步运行，成本降低 50%。
6. **`{language}/claude-api/files-api.md`** — 当跨多个请求发送相同文件而不重复上传时阅读。
7. **`shared/error-codes.md`** — 调试 HTTP 错误或实现错误处理时阅读。
8. **`shared/live-sources.md`** — 用于获取最新官方文档的 WebFetch URL。

> **注意：** 对于 Java, Go, Ruby, C#, PHP 和 cURL —— 它们各自有一个涵盖所有基础的文件。阅读该文件，并在需要时参阅 `shared/tool-use-concepts.md` 和 `shared/error-codes.md`。

### Agent SDK

阅读**特定的语言 Agent SDK 文件夹** (`{language}/agent-sdk/`)。Agent SDK 仅适用于 **Python 和 TypeScript**。

1. **`{language}/agent-sdk/README.md`** — 安装、快速开始、内置工具、权限、MCP、钩子 (Hooks)。
2. **`{language}/agent-sdk/patterns.md`** — 自定义工具、钩子、子 Agent、MCP 集成、会话恢复。
3. **`shared/live-sources.md`** — 用于获取当前 Agent SDK 文档的 WebFetch URL。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户要求提供“最新”或“当前”信息。
- 缓存的数据似乎不正确。
- 用户询问此处未涵盖的功能。

实时文档 URL 位于 `shared/live-sources.md`。

## 常见陷阱

- 向 API 传递文件或内容时不要截断输入。如果内容过长无法放入上下文窗口，请通知用户并讨论解决方案（切片、摘要等），而不是默默截断。
- **Opus 4.6 / Sonnet 4.6 思考：** 使用 `thinking: {type: "adaptive"}` —— **严禁**使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上均已弃用）。对于旧模型，`budget_tokens` 必须小于 `max_tokens`（最小 1024）。如果设置错误，将抛出异常。
- **Opus 4.6 移除了预填 (Prefill)：** Assistant 消息预填（上一轮 Assistant 转向的预填）在 Opus 4.6 上会返回 400 错误。请改用结构化输出 (`output_config.format`) 或系统提示词指令来控制响应格式。
- **`max_tokens` 默认值：** 不要设置过低的 `max_tokens` —— 触及上限会导致在思考途中截断输出并需要重试。对于非流式请求，默认设置为 `~16000`（保持响应在 SDK HTTP 超时范围内）。对于流式请求，默认设置为 `~64000`（无需考虑超时，给模型留出空间）。只有当您有强硬理由时（分类任务 `~256`、成本上限或刻意缩短输出）才设置较低的值。
- **128K 输出 Token：** Opus 4.6 支持最高 128K 的 `max_tokens`，但 SDK 要求使用流式传输以避免 HTTP 超时。请结合 `.get_final_message()` / `.finalMessage()` 使用 `.stream()`。
- **工具调用 JSON 解析 (Opus 4.6):** Opus 4.6 在工具调用的 `input` 字段中可能会产生不同的 JSON 字符串转义（例如 Unicode 或前斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——切勿对序列化后的输入进行原始字符串匹配。
- **结构化输出 (所有模型):** 在 `messages.create()` 中使用 `output_config: {format: {...}}` 代替已弃用的 `output_format` 参数。这是一个通用的 API 变更，并非仅针对 4.6 版本。
- **不要重新开发 SDK 功能：** SDK 提供了高级别辅助函数——请使用它们而不是从头构建。具体来说：使用 `stream.finalMessage()` 而不是用 `new Promise()` 包装 `.on()` 事件；使用类型化的异常类（`Anthropic.RateLimitError` 等）而不是字符串匹配错误信息；使用 SDK 类型（`Anthropic.MessageParam` 等）而不是重新定义等效接口。
- **不要为 SDK 数据结构定义自定义类型：** SDK 为所有 API 对象导出了类型。使用 `Anthropic.MessageParam` 表示消息，`Anthropic.Tool` 表示工具定义，`Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam` 表示工具结果，`Anthropic.Message` 表示响应。定义您自己的 `interface ChatMessage { role: string; content: unknown }` 会导致重复并失去类型安全性。
- **报告与文档输出：** 对于生成报告、文档或可视化的任务，代码执行沙箱预装了 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化的文件（DOCX, PDF, 图表）并通过文件 API 返回——对于“报告”或“文档”类型的请求，请考虑使用此方式，而非纯文本输出。
