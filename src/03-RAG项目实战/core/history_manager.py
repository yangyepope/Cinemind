"""
 Cinemind 03-RAG 实战项目 - 会话历史管理器 (History Manager)

 本模块负责本地磁盘化存储用户的聊天记录，并提供基于 Session ID 的多租户隔离。
 遵循项目开发规范：包含路径安全过滤 + LRU 内存缓存防泄漏 + 会话文件过期清理。
"""

# 导入必要的库
from pathlib import Path                   # 处理物理文件路径
from collections import OrderedDict        # 引入 OrderedDict 实现 LRU 缓存逐出策略
from datetime import datetime, timedelta   # 用于会话文件过期时间计算
from langchain_community.chat_message_histories import FileChatMessageHistory  # 文件流消息历史组件
from langchain_core.chat_history import BaseChatMessageHistory                 # 消息历史基类
from config.settings import SESSION_HISTORY_DIR, SESSION_CACHE_LIMIT           # 会话存储目录与缓存上限

# 使用 OrderedDict 实现 LRU 缓存：
# - 最近使用的会话排在头部，最久未使用的排在尾部
# - 当缓存超过 SESSION_CACHE_LIMIT 时，自动淘汰尾部项，防止内存无限增长
_history_store: OrderedDict[str, BaseChatMessageHistory] = OrderedDict()


def session_history_store(session_id: str) -> BaseChatMessageHistory:
    """
    获取或创建指定会话的文件历史记录器。
    内置 LRU 逐出策略，防止内存无限增长。

    Args:
        session_id: 用户请求附带的唯一会话标识符。

    Returns:
        挂载了本地文件的消息历史对象。
    """
    # --- 安全水位线：路径穿越防范 ---
    # 强制检查 session_id 是否合法（仅允许字母、数字和连字符）
    # 防止黑客通过 "../../etc/passwd" 等构造性 ID 越权读写系统文件
    if not all(c.isalnum() or c == '-' for c in session_id):
        session_id = "default_session"

    # --- LRU 缓存命中逻辑 ---
    if session_id in _history_store:
        # 将命中的会话移到头部（标记为最近使用）
        _history_store.move_to_end(session_id, last=False)
        return _history_store[session_id]

    # --- 创建新会话 ---
    # 全量使用 Pathlib 进行路径拼接，构造如：database/sessions/user123.json
    file_path: Path = SESSION_HISTORY_DIR / f"{session_id}.json"

    # 实例化文件消息历史记录器（自动处理序列化与反序列化）
    _history_store[session_id] = FileChatMessageHistory(str(file_path))
    # 将新建会话移到头部（最近使用）
    _history_store.move_to_end(session_id, last=False)

    # --- LRU 逐出：超过上限时淘汰尾部（最久未使用的）---
    while len(_history_store) > SESSION_CACHE_LIMIT:
        # popitem(last=True) 弹出尾部项：仅释放内存，磁盘文件保留不删除
        _history_store.popitem(last=True)

    return _history_store[session_id]


def cleanup_expired_sessions(expire_days: int = 30) -> int:
    """
    过期会话静默清理器：删除超过指定天数未被访问的会话磁盘文件。
    建议定期（如每日凌晨）调用此函数，防止磁盘满载。

    Args:
        expire_days: 超过多少天未修改的文件被视为过期，默认 30 天。

    Returns:
        删除的文件数量。
    """
    # 计算过期时间阈值
    threshold = datetime.now() - timedelta(days=expire_days)
    deleted_count = 0

    # 遍历会话历史目录下的所有 .json 文件
    for session_file in SESSION_HISTORY_DIR.glob("*.json"):
        # 获取文件的最后修改时间
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < threshold:
            # 超过阈值，删除磁盘文件
            session_file.unlink()
            # 同时从内存缓存中移除（如果存在）
            _history_store.pop(session_file.stem, None)
            deleted_count += 1

    return deleted_count
