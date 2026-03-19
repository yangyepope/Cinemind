import os
import json
from typing import List, Dict, Any, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

# 1. 定义存储模型
class SessionHistoryModel(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)

# 2. 实现高效的历史管理类
class OfficialPydanticHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_root: str = "sessions"):
        # 安全检查：防止路径穿越
        if not session_id.isalnum():
             raise ValueError("session_id 必须为字母或数字")
             
        self.session_id = session_id
        self.storage_root = storage_root
        self.file_path = os.path.join(self.storage_root, f"{session_id}.json")
        
        if not os.path.exists(self.storage_root):
            os.makedirs(self.storage_root)

    @property
    def messages(self) -> List[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                validated_session = SessionHistoryModel.model_validate(raw_data)
                return messages_from_dict(validated_session.messages)
        except Exception:
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """批量追加消息，减少 IO 开销"""
        current_data = None
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    old_raw = json.load(f)
                    current_data = SessionHistoryModel.model_validate(old_raw)
            except Exception:
                pass
        
        if not current_data:
            current_data = SessionHistoryModel(session_id=self.session_id)
        
        # 批量序列化
        new_dicts = [message_to_dict(m) for m in messages]
        current_data.messages.extend(new_dicts)

        # 物理保存（单次写入）
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(current_data.model_dump_json(indent=2))

    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
