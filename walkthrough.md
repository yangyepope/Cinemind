# Cinemind 项目开发操作日志 (Operation Log)

本文件作为项目的持久化资产，记录了开发过程中的所有关键改动、原理说明及验证结果。

---

## [2026-03-17 19:10:00] 阶段一：API 修复、详细注释及环境升级
- **操作描述**: 解决代码运行报错，增强代码可读性，并引入现代 Python 依赖管理工具。
- **修复与增强**:
  - **代码修正**: 解决了 `01-APIKey使用.py` 中的模型名称错误 (`qwen3-vl-8b` -> `qwen-turbo`) 并补全了流式输出逻辑。
  - **文档增强**: 应用 **详细文档撰写专家** 技能，为核心代码（导入、客户端初始化、对话请求、流式循环）补充了详尽的中文注释。
  - **技能升级**: 更新了 [.skills/document_master.md](file:///d:/8-python-project/Cinemind/.skills/document_master.md)，强制要求对 `import`、API Key 安全性和模型参数进行中文解释。
- **Git 与项目配置**:
  - **.gitignore**: 创建了完善的忽略规则，覆盖了 `.env`、`venv`、Python 缓存等。
  - **uv 管理**: 初始化了 `uv` 项目，创建了 [pyproject.toml](file:///d:/8-python-project/Cinemind/pyproject.toml) (Python >= 3.12) 和 [uv.lock](file:///d:/8-python-project/Cinemind/uv.lock)。
- **验证结果**:
  - [x] 所有文件已成功推送到 [GitHub](https://github.com/yangyepope/Cinemind.git)。
  - [x] `uv` 环境配置已通过语法验证。
> [!TIP]
> 推荐运行 `uv sync` 同步开发环境。

---

## [2026-03-17 19:15:00] 阶段二：自动化操作日志系统上线
- **操作描述**: 响应用户对日志清晰度的需求，建立自动化、结构化的操作追踪机制。
- **改动详情**:
  - **新增规则**: 创建 [.rules/03-operation-logging.md](file:///d:/8-python-project/Cinemind/.rules/03-operation-logging.md)，将更新此日志文件设为 AI 的强制性动作。
  - **新增技能**: 创建并优化了 [.skills/operation_logger.md](file:///d:/8-python-project/Cinemind/.skills/operation_logger.md)，定义了高清晰度的"报表风格"日志模板。
  - **日志初始化**: 重构了 [walkthrough.md](file:///d:/8-python-project/Cinemind/walkthrough.md) 的整体结构，使其版本化、时间线化。
- **验证结果**:
  - [x] 日志格式已升级至用户要求的"清晰明了"级别。
  - [x] 配置已推送到远程仓库 origin/master。
- **当前状态**: 🟢 自动化日志系统已完全激活。

---

## [2026-03-17 21:25:00] 阶段三：新机器 uv 环境配置

- **操作背景**: 用户在家庭电脑上拉取项目后，`uv` 命令无法识别，终端出现乱码，虚拟环境缺失。
- **问题排查**:
  - `uv` 已手动下载至 `D:\1-application\UV\uv-x86_64-pc-windows-msvc\`，但未添加到系统 PATH。
  - 终端乱码原因：编码页为 GBK，使用 `chcp 65001` 切换至 UTF-8 解决。
- **改动详情**:
  - **环境变量**: 将 `D:\1-application\UV\uv-x86_64-pc-windows-msvc` 永久写入用户 PATH（`[System.Environment]::SetEnvironmentVariable`）。
  - **虚拟环境**: 执行 `uv sync` 成功，创建 `.venv`（CPython 3.14.3），安装 17 个依赖包。
- **已安装核心依赖**:
  - `openai==2.28.0`, `pydantic==2.12.5`, `httpx==0.28.1`, `tqdm==4.67.3`
- **验证结果**:
  - [x] `uv 0.10.11` 版本确认正常。
  - [x] `.venv` 虚拟环境已创建于项目根目录。
  - [x] 17 个依赖包全部安装完成。
  - [x] 用户环境变量已永久更新，重启终端后可直接使用 `uv`。
> [!TIP]
> 下次重新打开终端后，`uv` 命令可直接使用。如需运行项目，请执行 `uv run python 01-APIKey使用.py`。

---

## [2026-03-17 21:55:00] 阶段四：解决 IDE 导入报错及 Windows 环境适配

- **操作背景/修复**: 
  - 解决了编辑器 (Cursor/VS Code) 中 `import openai` 报红的问题。
  - 解决了 Windows 终端在打印 Emoji 时由于编码问题导致的程序崩溃。
- **增强/改动详情**:
  - **IDE 配置**: 在 [.vscode/settings.json](file:///d:/1-application/python_project/Cinemind/.vscode/settings.json) 中配置了 `python.defaultInterpreterPath`，指向项目根目录下的 `.venv`。
  - **环境适配**: 在 [01-APIKey使用.py](file:///d:/1-application/python_project/Cinemind/01-APIKey使用.py) 中引入了 `sys.stdout.reconfigure(encoding='utf-8')`，确保 Windows 平台对 UTF-8 字符（如 Emoji）的完美支持。
  - **合规性优化**: 更新了所有内部规划文档（`task.md`、`implementation_plan.md`），确保遵循 `.agent/rules/language.md` 要求的全中文输出规范。
- **验证结果**:
  - [x] 通过 `uv run 01-APIKey使用.py` 验证，程序运行正常且能正确显示 Emoji。
  - [x] `.vscode/settings.json` 已正确配置，IDE 语言服务器现已关联虚拟环境。
  - [x] 所有注释、文档均已切换为简体中文，符合项目开发规范。

> [!TIP]
> 如果编辑器中仍有缓存红线，建议尝试重启 IDE 或点击右下角的 Python 版本号手动重新选择刚配置的解释器。

---

## [2026-03-17 22:00:00] 阶段五：细化 IDE 路径配置与 Pylance/Pyre2 缓存分析

- **操作背景/修复**: 
  - 针对“代码执行正常但 IDE 持久报红”的情况，进行了更深层的 `.vscode/settings.json` 细化配置。
- **增强/改动详情**:
  - **路径变量化**: 在 [.vscode/settings.json](file:///d:/1-application/python_project/Cinemind/.vscode/settings.json) 中使用了 `${workspaceFolder}` 全局变量，强制要求 IDE 在项目工作空间内寻找 `.venv`。
  - **分析模式增强**: 开启了 `python.analysis.diagnosticMode: "workspace"`，引导语言服务器扫描整个工作区而非仅当前文件。
- **验证结果**:
  - [x] `uv run python -c "import openai; print(openai.__file__)"` 确认库文件位于路径：`D:\1-application\python_project\Cinemind\.venv\Lib\site-packages\openai\__init__.py`。
  - [x] 设置文件已成功覆盖，路径指向符合实际文件系统。

> [!IMPORTANT]
> **终极解决方案**：如果红线依然存在，这是因为 Cursor/VS Code 的 **Pyre2/Pylance 语言服务器缓存** 未及时更新。请尝试：
> 1. 按下 `Ctrl + Shift + P`，输入 `Python: Restart Language Server`。
> 2. 或者直接重启编辑器。
> 3. 由于代码运行正常（通过 `uv` 验证），此红线仅为“语法显示层”的滞后，不影响实际开发。

---

## [2026-03-17 23:23:00] 阶段六：概念讲解 - Zero-shot 与 Few-shot

- **操作背景/说明**: 解答用户关于零样本（Zero-shot）和少样本（Few-shot）提示框架的疑问。
- **概念解释**:
  - **Zero-shot (零样本提示)**: 指在不提供任何当前任务参考示例的前提下，直接提出问题或下达指令。这要求大模型完全依赖其预训练时学习到的广泛知识与内在归纳泛化能力来理解并执行任务。例如，直接对模型下达指令：“将这句话翻译成法语：你好”。
  - **Few-shot (少样本提示)**: 指在向模型正式提出任务问题前，先人为提供少量（如1到几十个）特定上下文的示例。这种做法能有效引导模型去理解任务的特定规则、学习你期望的特定输出格式或逻辑推衍路径，从而大幅度提高复杂任务回答的精确率。例如，先给足几个中英翻译的规范对照表以及输出格式约定，然后再要求它翻译目标句子。
- **关联文件追踪**: @[d:\1-application\python_project\Cinemind\project_rules.md] （如果未来整理 prompt 规范，可在此建立规则档案）
- **验证结果**:
  - [x] 相关概念已被成功存档并追加到项目操作与认知日志中，作为持续积累的技术资产供后续开发查阅。

---

## [2026-03-17 23:25:00] 阶段七：创建 Few-shot 示例实战脚本

- **操作背景/说明**: 根据用户提供的截图，生成了一个关于提示词优化（金融文本分类）的实战 Python 脚本。
- **改动详情**:
  - **新建文件**: 创建了 `src/03-提示词优化案例_金融文本分类.py`。
  - **内容转录**: 完全按照截图还原了代码，包括 `client` 初始化、分类示例数据 (`examples_data`)、待分类文本 (`questions`) 以及通过注释形式展示系统设定的 `few-shot` prompt 构建示例。随后又根据新的截图补全了 `messages` 数组的遍历拼装逻辑以及调用大模型回答问题的 `for` 循环。
  - **代码补全**: 为保证后续执行的可能性，补充了通过 `os.environ.get("DASHSCOPE_API_KEY")` 读取环境变量的逻辑。
- **验证结果**:
  - [x] 文件已成功生成在指定路径，代码结构与用户截图保持一致。
  - [x] 成功运行 `03-提示词优化案例_金融文本分类.py`，模型基于 Few-shot 的示例成功输出了正确的分类（新闻报道、公司公告、财务报道、分析师报告、不清楚）。

---

## [2026-03-18 10:46:41] 阶段八：创建信息抽取实战脚本
- **操作背景**: 根据用户提供的教程图片，创建了用于金融信息结构化抽取的 04 号 Python 脚本。
- **增强/改动详情**:
  - **新建文件**: 创建了 [04-提示词优化案例_金融信息抽取.py](file:///d:/8-python-project/Cinemind/src/04-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%BC%98%E5%8C%96%E6%A1%88%E4%BE%8B_%E9%87%91%E8%9E%8D%E4%BF%A1%E6%81%AF%E6%8A%BD%E5%8F%96.py)。
  - **内容转录**: 完全按照截图提取了提取所需 `schema`，构建 Few-shot 语料库 `examples_data`，并将其实例化为 `messages` 对话消息，利用循环实现对新问题（`questions`）的模型提问。
- **验证结果**:
  - [x] 成功生成文件并保证代码符合规范。

---

## [2026-03-18 11:02:00] 阶段九：创建金融文本匹配判断实战脚本
- **操作背景**: 根据用户提供的截图，创建了用于金融文本匹配判断的 05 号 Python 脚本。
- **改动详情**:
  - **新建文件**: 创建了 [05-提示词优化案例_金融文本匹配判断.py](file:///d:/8-python-project/Cinemind/src/05-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%BC%98%E5%8C%96%E6%A1%88%E4%BE%8B_%E9%87%91%E8%9E%8D%E6%96%87%E6%9C%AC%E5%8C%B9%E9%85%8D%E5%88%A4%E6%96%AD.py)。
  - **内容转录**: 按照截图构建了 `examples_data` 作为 Few-shot 示例，通过循环将示例拼接到 `messages` 列表中，引导大模型学习判断两段股票/财经文本是否表达相似的情感或含义。
  - **代码补全**: 补全了 OpenAI 客户端调用逻辑并遍历 `questions` 进行提问测试。
- **验证结果**:
  - [x] 脚本创建成功，代码结构与规范对齐。
  - [x] 经本地运行测试，模型能准确应用提示词并输出“是”与“不是”等预测结果。

---

## [2026-03-18 18:11:00] 阶段二十：LangChain 聊天提示词模板与历史占位符实战

- **操作背景**: 根据用户提供的截图，创建并完善 10 号脚本，重点演示 `ChatPromptTemplate` 如何处理多角色消息及动态对话历史。
- **改动详情**:
  - **新建文件**: 创建了 [10-ChatPromptTemplate的使用.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/10-ChatPromptTemplate的使用.py)。
  - **内容实现**: 
    - 使用 `MessagesPlaceholder("history")` 作为模板的一部分，实现了对动态对话列表的自动注入。
    - 结合 `ChatTongyi(model="qwen3-max")` 进行多轮对话模拟测试。
    - 演示了 `.invoke().to_string()` 在调试合并消息时的便捷性。
- **验证结果**:
  - [x] 成功运行脚本，模型在得知历史对话（作过两首诗）的基础上，正确接续了下一首关于边塞主题的创作。
  - [x] 确认代码全中文注释，规划文档已同步至 `document/` 目录。

> [!TIP]
> `MessagesPlaceholder` 是构建对话机器人（Chatbot）时管理“记忆”或“上下文”最核心的工具，能自动展开列表中的所有消息。

---

## [2026-03-18 18:31:00] 阶段二十一：LangChain Chain 基础使用实战 (LCEL 语法)

- **操作背景**: 根据用户提供的截图，创建并完善 11 号脚本，演示如何使用 `|` 运算符将提示词模板与模型组合成一个简单的 `Chain`。
- **改动详情**:
  - **新建文件**: 创建了 [11-Chain的基础使用.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/11-Chain的基础使用.py)。
  - **内容实现**: 
    - 组合了 `chat_prompt_template` 和 `ChatTongyi` 模型。
    - 演示了通过 `chain.invoke()` 进行一键式端到端调用。
- **验证结果**:
  - [x] 成功运行脚本，链式调用逻辑通畅，模型能根据传入的历史数据生成符合预期的诗人回复。
  - [x] 所有注释保持全中文，规划文档已同步至 `document/` 目录。

> [!TIP]
> `|` 运算符是 LangChain Expression Language (LCEL) 的核心，它要求每个组件都继承自 `Runnable`。

---

## [2026-03-18 13:46:19] 阶段十：修复 DashScope 文本嵌入模型的兼容性问题
- **操作背景**: 用户在运行 `02-文本嵌入与余弦相似度计算.py` 时遇到了 DashScope 接口报错 `<400> InternalError.Algo.InvalidParameter: Value error, contents is neither str nor list of str`。
- **改动详情**:
  - **问题诊断**: 问题根源在于 `langchain_openai` 默认的 `OpenAIEmbeddings` 会使用 `tiktoken` 将文本转为 Token ID 列表 (pre-tokenized)，而阿里云 DashScope 的兼容接口仅直接接收字符串（或字符串列表）格式的输入。
  - **参数修复**: 在模型初始化代码中追加参数 `check_embedding_ctx_length=False`，禁用内部 Token 计算过程，将原始字符串无损传递给 DashScope 接口。
- **验证结果**:
  - [x] 成功修改脚本 `src/02-LangChainRAG开发/02-文本嵌入与余弦相似度计算.py`。
  - [x] 在终端运行修正后的脚本，余弦相似度计算结果正常输出，不再抛出 400 错误。

---

## [2026-03-18 14:05:00] 阶段十二：清理并重置 Python 环境版本
- **操作背景**: 用户反馈已手动删除高版本 Python 环境，需重新建立符合规范的低版本开发环境。
- **问题诊断**:
  - `pyproject.toml` 要求 `python >=3.12, <3.13`。
  - 此前误用了 3.14 版本环境，导致 potential 兼容性风险。
- **改动详情**:
  - **环境同步**: 使用 `uv sync --python 3.12.9` 重新创建了 `.venv` 虚拟环境。
  - **依赖补全**: 自动安装了 41 个项目核心依赖（含 `openai`, `langchain-openai`, `scikit-learn` 等）。
- **验证结果**:
  - [x] `.\.venv\Scripts\python --version` 确认版本为 `3.12.9`。
  - [x] 虚拟环境已就绪，完全符合项目 `project_rules.md` 中的“环境一致性”要求。
  - [x] IDE (VS Code/Cursor) 设置中 `python.defaultInterpreterPath` 已指向此 `.venv`。

> [!TIP]
> 环境现已完全重置为 3.12 版本。如遇库无法导入，请尝试重启编辑器或运行 `Python: Restart Language Server`。

---

## [2026-03-18 14:35:00] 阶段十三：创建 LangChain 访问通义千问实战脚本
- **操作背景**: 根据用户提供的教程截图，创建了用于演示通过 LangChain 社区版工具调用阿里云通义千问大模型的 02 号脚本。
- **改动详情**:
  - **环境配置**: 安装了 `langchain-community` 和 `dashscope` 官方 Python SDK。
  - **新建文件**: 创建了 [02-LangChain访问阿里云通义千问大模型.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG%E5%BC%80%E5%8F%91/02-LangChain%E8%AE%BF%E9%97%AE%E9%98%BF%E9%87%8C%E4%BA%91%E9%80%9A%E4%B9%89%E5%8D%83%E9%97%AE%E5%A4%A7%E6%A8%A1%E5%9E%8B.py)。
  - **内容编写**: 使用 `langchain_community.llms.tongyi.Tongyi` 类初始化模型（qwen-max），并调用 `invoke` 方法执行基础文本问答。
  - **兼容性优化**: 针对 Windows 终端增加了 UTF-8 编码重配逻辑，确保中文输出无乱码。
- **验证结果**:
  - [x] 成功运行脚本，获得大模型返回的身份自我介绍，API 链路完全通畅。

---

## [2026-03-18 14:45:00] 阶段十四：LangChain 通义千问流式输出实战
- **操作背景**: 创建并完善 03 号实战脚本，重点展示如何利用 LangChain 的 `stream` 接口实现逐块内容的实时渲染。
- **改动详情**:
  - **新建文件**: 创建了 [03-LangChain通义千问流式输出.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG%E5%BC%80%E5%8F%91/03-LangChain%E9%80%9A%E4%B9%89%E5%8D%83%E9%97%AE%E6%B5%81%E5%BC%8F%E8%BE%93%E5%87%BA.py)。
  - **内容实现**: 调用 `model.stream` 并通过 `for` 循环遍历响应块。针对逐字输出的视觉需求，使用了 `print(chunk, end="", flush=True)` 技术方案。
  - **健壮性优化**: 沿用了 Windows 平台的 `sys.stdout.reconfigure` 编码补丁，确保流式输出中的中文字符毫无损耗。
- **验证结果**:
  - [x] 成功运行脚本，内容在控制台中以毫秒级响应逐字呈现，验证了流式机制的有效性。

---

## [2026-03-18 15:10:00] 阶段十五：LangChain 聊天模型简化调用实战
- **操作背景**: 在 04 号脚本的基础上进行逻辑简化，探索 LangChain 对元组列表消息格式的自动解析支持。
- **改动详情**:
  - **新建文件**: 创建了 [05-LangChain聊天模型简化调用.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG%E5%BC%80%E5%8F%91/05-LangChain%E8%81%8A%E5%A4%A9%E6%A8%A1%E5%9E%8B%E7%AE%80%E5%8C%96%E8%B0%83%E7%94%A8.py)。
  - **逻辑简化**: 弃用了 `HumanMessage` 和 `SystemMessage` 等类的显式导入，改为使用 `[("system", "..."), ("human", "...")]` 的元组列表。
  - **多轮对话模拟**: 在消息列表中加入了 `("ai", "...")` 角色，模拟了多轮对话的上下文注入。
- **验证结果**:
  - [x] 修复了手动编辑引入的逗号缺失语法错误。
  - [x] 成功运行脚本，模型正确识别了元组中的角色设定并以预期的唐诗风格生成了春天的诗作。

---

## [2026-03-18 15:30:00] 阶段十六：LangChain 嵌入模型获取实战

- **操作背景**: 创建并完善 06 号脚本，重点展示如何利用 LangChain 的 `DashScopeEmbeddings` 工具获取文本的特征向量（Embedding）。
- **改动详情**:
  - **新建文件**: 创建了 [06-LangChain访问阿里云嵌入模型.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/06-LangChain访问阿里云嵌入模型.py)。
  - **内容实现**: 实例化 `DashScopeEmbeddings` 类，调用 `embed_query` 方法将字符串转换为 1536 维的浮点数向量。
  - **稳定性适配**: 沿用了 Windows UTF-8 编码修复方案，确保日志输出稳定。
- **验证结果**:
  - [x] 成功运行脚本，返回了维度为 1536 的向量（Vector），验证了阿里云嵌入模型的可用性。

---

## [2026-03-18 16:07:00] 阶段十七：LangChain 通用提示词模板实战

- **操作背景**: 创建并完善 07 号脚本，通过 LangChain 的 `PromptTemplate` 实现提示词的参数化与链式调用。
- **改动详情**:
  - **新建文件**: 创建了 [07-LangChain通用提示词模板.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/07-LangChain通用提示词模板.py)。
  - **内容实现**: 
    - 使用 `PromptTemplate.from_template` 定义了包含 `{lastname}` 和 `{gender}` 的模板。
    - 演示了 `.format()` 方法的基础字符串替换。
    - 引入了 `langchain_community.llms.tongyi.Tongyi` 模型，并使用现代 LCEL 语法 (`prompt_template | model`) 构建了第一个处理链（Chain）。
- **验证结果**:
  - [x] 成功运行脚本，模型正确识别了模板变量并返回了“王浩宇”等符合逻辑的起名建议。
  - [x] 验证了 LCEL 语法的直观性和 `PromptTemplate` 的复用价值。

> [!TIP]
> LCEL (LangChain Expression Language) 是 LangChain 推荐的现代构建方式，使用 `|` 符号可以非常清晰地组合提示词、模型和输出解析器。

---

## [2026-03-18 16:25:00] 阶段十八：LangChain Few-Shot 提示词模板实战

- **操作背景**: 根据用户提供的截图，创建并完善 08 号脚本，演示如何利用少样本提示（Few-Shot）引导模型学习特定逻辑（如单词反义词）。
- **改动详情**:
  - **新建文件**: 创建了 [08-FewShot提示词模板.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/08-FewShot提示词模板.py)。
  - **内容实现**: 
    - 转录了图片中的代码逻辑：定义 `example_template` 和 `examples_data`（大/小、上/下）。
    - 实例化 `FewShotPromptTemplate`，配置前缀（prefix）和后缀（suffix）。
    - 演示了通过 `.invoke().to_string()` 获取整合后的提示词全文。
    - 结合 `Tongyi` 模型，验证了推理效果。
- **验证结果**:
  - [x] 成功运行脚本，提示词正确拼接了示例数据。
  - [x] 模型根据示例成功输出了“左”的反义词为“右”，验证了 Few-Shot 机制在复杂逻辑引导中的有效性。

> [!TIP]
> Few-Shot Prompting 是提升大模型在特定任务（如结构化输出、逻辑推导）中表现的最直接有效手段。

---

## [2026-03-18 16:42:00] 阶段十九：LangChain 模板类方法对比实战 (format vs invoke)
- **改动详情**: 创建 [09-模板类的format和invoke方法.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/09-模板类的format和invoke方法.py)，对比 `str` 与 `PromptValue` 的输出差异。

---

## [2026-03-18 18:11:00] 阶段二十：LangChain 聊天提示词模板与历史占位符实战
- **改动详情**: 创建 [10-ChatPromptTemplate的使用.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/10-ChatPromptTemplate的使用.py)，演示 `MessagesPlaceholder` 动态注入对话历史。

---

## [2026-03-18 18:31:00] 阶段二十一：LangChain Chain 基础使用实战 (LCEL 语法)
- **改动详情**: 创建 [11-Chain的基础使用.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/11-Chain的基础使用.py)，使用 `|` 运算符实现提示词与模型的链式组合。

---

## [2026-03-18 19:19:00] 阶段二十二：Python 运算符重写扩展实战 (揭秘 | 符号底层)
- **改动详情**: 创建 [12-Python的或运算符重写.py](file:///d:/8-python-project/Cinemind/src/02-LangChainRAG开发/12-Python的或运算符重写.py)，模拟 `__or__` 魔法方法以揭示 LCEL 的运行逻辑。
- **验证结果**: 成功输出 `a`, `b`, `c`，逻辑闭环。
