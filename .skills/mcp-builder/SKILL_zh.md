---
name: mcp-builder
description: 创建高质量 MCP（模型上下文协议）服务器的指南，使 LLM 能够通过精心设计的工具与外部服务进行交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论使用 Python (FastMCP) 还是 Node/TypeScript (MCP SDK)。
license: 完整条款请参阅 LICENSE.txt
---

# MCP 服务器开发指南

## 概览

创建 MCP（模型上下文协议）服务器，使 LLM 能够通过精心设计的工具与外部服务进行交互。MCP 服务器的质量衡量标准是它能否有效地帮助 LLM 完成现实世界的任务。

---

# 开发流程

## 🚀 高层工作流

创建一个高质量的 MCP 服务器涉及四个主要阶段：

### 阶段 1：深度调研与规划

#### 1.1 理解现代 MCP 设计

**API 覆盖 vs. 工作流工具：**
在全面的 API 端点覆盖与专门的工作流工具之间取得平衡。工作流工具在执行特定任务时由于其便捷性可能更好，而全面的覆盖则赋予智能体组合操作的灵活性。性能因客户端而异——某些客户端受益于结合基础工具的代码执行，而另一些客户端则在更高层级的工作流下表现更好。如果不确定，请优先考虑全面的 API 覆盖。

**工具命名与可发现性：**
清晰、具有描述性的工具名称有助于智能体快速找到正确的工具。使用一致的前缀（例如：`github_create_issue`、`github_list_repos`）并采用面向动作的命名方式。

**上下文管理：**
智能体受益于简洁的工具描述以及对结果进行过滤/分页的能力。设计的工具应返回重点明确、相关的数据。某些客户端支持代码执行，这可以帮助智能体高效地过滤和处理数据。

**可操作的错误消息：**
错误消息应通过具体的建议和后续步骤引导智能体找到解决方案。

#### 1.2 研读 MCP 协议文档

**导航 MCP 规范：**
从站点地图开始查找相关页面：`https://modelcontextprotocol.io/sitemap.xml`
然后获取带有 `.md` 后缀的具体页面以获取 markdown 格式（例如：`https://modelcontextprotocol.io/specification/draft.md`）。

需要回顾的关键页面：
- 规范概览与架构 (Specification overview and architecture)
- 传输机制 (Transport mechanisms) (可流式 HTTP, stdio)
- 工具、资源与提示词定义 (Tool, resource, and prompt definitions)

#### 1.3 研读框架文档

**推荐技术栈：**
- **语言**：TypeScript（具有高质量的 SDK 支持，在许多执行环境如 MCPB 中具有良好的兼容性。此外，AI 模型擅长通过广泛使用的代码库、静态类型和优秀的 lint 工具生成 TypeScript 代码）。
- **传输**：远程服务器使用可流式 HTTP，采用无状态 JSON（相比有状态会话和流式响应，更易于扩展和维护）。本地服务器使用 stdio。

**加载框架文档：**
- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) —— 核心指南

**针对 TypeScript (推荐)：**
- **TypeScript SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) —— TypeScript 模式与示例

**针对 Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) —— Python 模式与示例

#### 1.4 规划你的实现

**理解 API：**
审查服务的 API 文档，以确定关键端点、身份验证要求和数据模型。根据需要使用 Web 搜索和 WebFetch。

**工具选择：**
优先考虑全面的 API 覆盖。列出要实现的端点，从最常见的操作开始。

---

### 阶段 2：实现

#### 2.1 设置项目结构

参阅语言特定的设置指南：
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) —— 项目结构、package.json、tsconfig.json
- [🐍 Python 指南](./reference/python_mcp_server.md) —— 模块组织、依赖项

#### 2.2 实现核心基础设施

创建共享实用工具：
- 带有身份验证的 API 客户端
- 错误处理辅助函数
- 响应格式化 (JSON/Markdown)
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入 Schema (Input Schema)：**
- 使用 Zod (TypeScript) 或 Pydantic (Python)
- 包含约束条件和清晰的描述
- 在字段描述中添加示例

**输出 Schema (Output Schema)：**
- 在可能的情况下为结构化数据定义 `outputSchema`
- 在工具响应中使用 `structuredContent`（TypeScript SDK 特性）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 功能的简要总结
- 参数描述
- 返回类型 schema

**具体实现：**
- 为 I/O 操作使用 async/await
- 带有可操作消息的适当错误处理
- 在适用时支持分页
- 使用现代 SDK 时同时返回文本内容和结构化数据

**注解 (Annotations)：**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### 阶段 3：评审与测试

#### 3.1 代码质量

评审重点：
- 无重复代码 (DRY 原则)
- 一致的错误处理
- 全面的类型覆盖
- 清晰的工具描述

#### 3.2 构建与测试

**TypeScript:**
- 运行 `npm run build` 以验证编译
- 使用 MCP Inspector 进行测试：`npx @modelcontextprotocol/inspector`

**Python:**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 进行测试

参阅语言特定的指南以获取详细的测试方法和质量清单。

---

### 阶段 4：创建评估 (Evaluations)

在实现 MCP 服务器后，创建全面的评估来测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 以获取完整的评估准则。**

#### 4.1 理解评估目的

使用评估来测试 LLM 是否能有效地利用你的 MCP 服务器回答现实、复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请遵循评估指南中概述的流程：

1. **工具检查 (Tool Inspection)**：列出可用工具并了解其能力
2. **内容探索 (Content Exploration)**：使用“只读”操作探索可用数据
3. **问题生成 (Question Generation)**：创建 10 个复杂、现实的问题
4. **答案验证 (Answer Verification)**：亲自解决每个问题以验证答案

#### 4.3 评估要求

确保每个问题都满足：
- **独立性**：不依赖于其他问题
- **只读性**：仅需非破坏性操作
- **复杂性**：需要多次工具调用和深度探索
- **现实性**：基于人类关心的真实用例
- **可验证性**：具有可通过字符串比较验证的单一、清晰答案
- **稳定性**：答案不会随时间改变

#### 4.4 输出格式

创建一个符合此结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于使用动物代号启动 AI 模型的讨论。其中一个模型需要一个使用 ASL-X 格式的特定安全等级。那个以斑点野猫命名的模型所确定的数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

开发期间根据需要加载这些资源：

### 核心 MCP 文档 (优先加载)
- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 的站点地图开始，然后获取带有 `.md` 后缀的特定页面
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) —— 通用 MCP 准则，包括：
  - 服务器和工具命名规范
  - 响应格式指南 (JSON vs Markdown)
  - 分页最佳实践
  - 传输选择 (可流式 HTTP vs stdio)
  - 安全与错误处理标准

### SDK 文档 (在阶段 1/2 加载)
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 语言特定的实现指南 (在阶段 2 加载)
- [🐍 Python 实现指南](./reference/python_mcp_server.md) —— 完整的 Python/FastMCP 指南，包含：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 注册工具
  - 完整的代码示例
  - 质量清单

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) —— 完整的 TypeScript 指南，包含：
  - 项目结构
  - Zod schema 模式
  - 使用 `server.registerTool` 注册工具
  - 完整的代码示例
  - 质量清单

### 评估指南 (在阶段 4 加载)
- [✅ 评估指南](./reference/evaluation.md) —— 完整的评估创建指南，包含：
  - 问题创建准则
  - 答案验证策略
  - XML 格式规范
  - 示例问题与答案
  - 使用提供的脚本运行评估
