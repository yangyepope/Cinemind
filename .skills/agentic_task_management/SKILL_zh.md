---
name: 智能任务驱动管理 (Agentic Task Management)
description: 强制要求 AI 在处理复杂请求时，先行构建 `task.md` 任务清单，并以此驱动整个研发生命周期的可追踪性。
---

# 智能任务驱动管理规范 (Agentic Task Management Guidelines)

当用户提出一个新的非琐碎需求、Bug 修复或架构解析请求时，请严格按照以下“原子任务化”流程执行，确保整个协作路径具备上帝视角的清晰度。

## 1. 核心触发逻辑 (Trigger)
不再只是口头答应用户。每当收到一个具有阶段性深度的请求时，**第一笔动作** 必须是执行 `write_to_file` 或 `multi_replace_file_content` 来初始化或更新 `task.md`。

## 2. `task.md` 构建标准
任务清单必须包含以下四个维度，并实时跟随进度勾选 `[x]`：
- **阶段一：研究与对齐 (Research & Alignment)**：包括读取源码、查看现有文档、确认用户意图。
- **阶段二：方案设计 (Planning)**：包括制定 `implementation_plan.md` 并请求用户 Review。
- **阶段三：编码与执行 (Execution)**：包含具体的代码修改、文件新建、以及增量调整。
- **阶段四：验证与归档 (Verification & Archival)**：包括终端测试、生成 `walkthrough.md` 走读文档、以及将过程任务记录归档。

## 3. 实时状态反馈与语言对齐 (Task Boundary & Language)
- **简体中文优先**：每次调用 `task_boundary` 工具时，其 `TaskName`, `TaskSummary`, `TaskStatus` 参数必须全部手动录入简体中文，严禁出现系统默认的英文输出。
- **主动对齐**：向用户汇报前，自检是否已同步更新内部及项目目录侧的 `task.md`。

在本会话的所有核心任务完成后，必须主动将任务清单 (`task.md`) 和实施方案 (`implementation_plan.md`) 归档：
- **存储目录**：同步至项目根目录的 `document/` 文件夹。
- **目录结构**：使用序列号命名子目录（如 `01-XXX解析`, `02-YYY优化`）。
- **文件命名规范**：强制使用 `YYYYMMDD_HHMMSS` 精准时间戳作为前缀，且**必须以技术核心内容命名**（严禁“优化”、“修复”等笼统词汇，例如：`20260324_174000_RunnableBranch_空上下文熔断修复_task.md`）。

---
**实施原则**：让“说”服从于“做”，让“做”留存在“档”。
