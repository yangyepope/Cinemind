---
name: langchain_memory_persistence
description: 在 LangChain 中实现持久化聊天历史的最佳实践。
---

# LangChain 会话持久化最佳实践

本技能提供了在 LangChain 应用中实现长期记忆的准则和参考实现。

## 核心原则

### 1. 性能：使用 `add_messages` (复数)
在自定义 `BaseChatMessageHistory` 子类时，必须重写 `add_messages` 而不是 `add_message`。
- **原因**：`RunnableWithMessageHistory` 会在对话结束时同时发送多条消息（AI 和 Human）。使用复数版本可以确保所有消息在一次 I/O 操作中完成（一次文件写入或一次数据库事务）。
- **影响**：减少 50% 以上的磁盘磨损和网络延迟。

### 2. 合规：使用 Pydantic 与官方序列化工具
使用 Pydantic 模型作为存储结构，并统一使用 `message_to_dict` / `messages_from_dict` 进行序列化。
- **原因**：确保数据完整性，并安全地处理复杂的消息属性（如 `tool_calls` 或 `additional_kwargs`）。
- **准则**：严禁直接存储消息对象；必须先序列化为标准字典。

### 3. 安全：路径与 ID 防护
- **准则**：严禁在未经过滤的情况下直接将 `session_id` 作为文件名。
- **防护**：必须使用正则表达式或白名单（如 `isalnum()`）确保 `session_id` 仅包含字母或数字，防止路径穿越攻击（Path Traversal）。

## 参考实现

```python
from typing import List, Dict, Any, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

class SessionHistoryModel(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)

class SecurePersistentHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_root: str):
        # 安全：校验 session_id 是否合法
        if not session_id.isalnum():
            raise ValueError("非法的 session_id")
        self.session_id = session_id
        self.file_path = os.path.join(storage_root, f"{session_id}.json")
        # ... 路径创建逻辑 ...

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # 批量序列化并在一次 I/O 中保存
        new_dicts = [message_to_dict(m) for m in messages]
        # ... 追加并写入逻辑 ...
```

## 错误处理
- **韧性**：对历史记录的所有操作应进行 `try-except` 包装。除非用户明确要求，否则不要让历史记录的加载/保存失败导致整个 AI 对话链条崩溃。
