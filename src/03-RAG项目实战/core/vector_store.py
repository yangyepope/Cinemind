"""
 Cinemind 03-RAG 实战项目 - 向量存储中枢 (Vector Store Core)
 
 本模块负责初始化与管理 Chroma 高维向量数据库，为 RAG 链条提供核心检索驱动。
 针对 Streamlit 的 Asyncio 闭环问题进行了容错处理。
"""

# 导入必要的库
import asyncio  # 导入 asyncio 用于处理异步事件循环
import chromadb  # 导入 chromadb 原生库以进行底层客户端管理
from langchain_chroma import Chroma  # 导入 LangChain 对 Chroma 的封装
from langchain_community.embeddings import DashScopeEmbeddings  # 导入通义千问嵌入模型
from config.settings import CHROMA_DB_DIR  # 从配置模块导入数据库存储路径

def init_vector_store() -> Chroma:
    """
    初始化并返回 Chroma 向量存储对象。
    
    采用显式客户端初始化模式，有效规避 Streamlit 在页面刷新时导致的 
    "RuntimeError: Event loop is closed" 异常。
    
    Returns:
        初始化完成的 Chroma 实例。
    """
    # --- Asyncio 稳定性补丁 ---
    # 彻底解决 Streamlit 多线程环境下 "RuntimeError: Event loop is closed"
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # --- 核心组件初始化 ---
    
    # 实例化通义千问嵌入模型，该模型将文本转化为 1536 维向量
    embeddings: DashScopeEmbeddings = DashScopeEmbeddings()
    
    # 使用原生 chromadb 客户端以获得更高的稳定性
    # PersistentClient 保证数据持久化到指定磁盘目录
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    
    # 将原生客户端注入 LangChain 的 Chroma 包装器中
    # 这样做可以复用 LangChain 的检索接口，同时享受原生客户端的连接稳定性
    vector_store: Chroma = Chroma(
        client=client,  # 注入显式创建的客户端
        embedding_function=embeddings,  # 关联嵌入模型
        collection_name="cinemind_rag_knowledge"  # 定义集合名称（类似于数据库表名）
    )
    
    # 返回构建好的向量存储实例，供 RAG 链条调用
    return vector_store
