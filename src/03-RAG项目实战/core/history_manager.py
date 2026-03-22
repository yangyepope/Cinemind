"""
 Cinemind 03-RAG 实战项目 - 会话历史管理器 (History Manager)
 
 本模块负责本地磁盘化存储用户的聊天记录，并提供基于 Session ID 的多租户隔离。
 遵循项目开发规范：包含路径安全过滤。
"""

# 导入必要的库
from pathlib import Path  # 处理物理文件路径
from langchain_community.chat_message_histories import FileChatMessageHistory  # 导入文件流消息历史组件
from langchain_core.chat_history import BaseChatMessageHistory  # 导入消息历史基类
from config.settings import SESSION_HISTORY_DIR  # 导入会话存储根目录

# 定义全局存储字典，用于在内存中缓存已打开的文件历史对象，提升响应速度
# Key: session_id (str), Value: FileChatMessageHistory 实例
_history_store: dict[str, BaseChatMessageHistory] = {}

def session_history_store(session_id: str) -> BaseChatMessageHistory:
    """
    获取或创建指定会话的文件历史记录器。
    
    Args:
        session_id: 用户请求附带的唯一会话标识符。
        
    Returns:
        挂载了本地文件的消息历史对象。
    """
    # --- 安全水位线：路径穿越防范 ---
    # 遵循规范：强制检查 session_id 是否为纯字母数字组合
    # 理由：防止黑客通过 "../../etc/passwd" 等构造性 ID 越权读写系统文件
    if not session_id.isalnum():
        # 如果校验不通过，直接重置为默认隔离区 "default_session"
        session_id = "default_session"

    # --- 缓存命中逻辑 ---
    # 如果该会话已经存在于内存池中，直接返回，避免频繁创建 IO 对象
    if session_id not in _history_store:
        # 遵循规范：全量使用 Pathlib 进行路径拼接
        # 构造结果如：database/sessions/user123.json
        file_path: Path = SESSION_HISTORY_DIR / f"{session_id}.json"
        
        # 实例化文件消息历史记录器
        # 该组件会自动处理消息的序列化（Message to Dict）与反序列化
        _history_store[session_id] = FileChatMessageHistory(str(file_path))
        
    # 返回对应的历史记录处理对象
    return _history_store[session_id]
