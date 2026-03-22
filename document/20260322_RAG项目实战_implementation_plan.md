# RAG 项目实战：企业级三合一架构重构计划
(已于 2026-03-22 完成)

## 0. 设计理念
- **极致解耦**：Core (算力) / Service (逻辑) / UI (渲染) 三位一体。
- **环境自举**：自动嗅探路径并补全 database/data 目录。
- **安全加固**：MD5 防重盾 + Session ID 路径穿越校验。

## 1. 核心变更
### Core 层
- `rag_chain.py`: LCEL 旗舰链条组装。
- `vector_store.py`: 基于 `langchain-chroma` 的单例化数据网关。
- `history_manager.py`: 具备安全过滤的文件记忆中心。

### Service 层
- `kb_service.py`: 封装了文档切片、指纹审计与异步入库逻辑。

### UI 层
- `app.py`: 玻璃态对话母港。
- `pages/1_📚_知识库录入平台.py`: B 端管理台。

### 3. 增强特性 (New)
- **全链路逐行注释**：每一个 Python 语句均配有详细的中文逻辑说明。
- **Asyncio 闭环补丁**：在 `core/vector_store.py` 中实现了自动检测并重置循环的逻辑，防范 `Event loop is closed` 错误。

## 4. 规则与技能进化 (Refinement)
- **规则升级**：将“逐行详细注释”从临时要求升级为 Cinemind 项目文档规范 (Rule 1)。
- **稳定性沉淀**：将 Streamlit 异步环境下的单例资源管理总结为 Standard Skill。

## 5. 验证方案
- [x] Streamlit 多页切换验证
- [x] MD5 拦截上传文件防御验证
- [x] Session 隔离历史记忆验证
- [x] 跨盘符路径自举验证
- [x] **逐行注释 100% 覆盖率验证**
- [x] **Windows 环境下 Asyncio 闭环异常捕捉验证**
