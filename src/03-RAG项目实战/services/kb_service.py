# 导入原生库
import hashlib  # 用于计算文本 MD5 指纹以便去重
import threading  # 引入线程锁，防御并发写入指纹文件时的竞争条件
from typing import List, Tuple  # 导入类型提示注解

# 导入 LangChain 相关组件
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 导入递归字符文本切分器
from langchain_core.documents import Document  # 导入文档对象模型

# 导入项目配置与核心组件
from config.settings import MD5_CACHE_PATH, CHUNK_SIZE, CHUNK_OVERLAP  # 从 settings 导入指纹库路径与切分参数
from core.vector_store import init_vector_store  # 导入向量库初始化函数
from utils.logger import get_sys_logger  # 导入日志记录工具

# 实例化知识库服务专用日志器
logger = get_sys_logger("KnowledgeBaseService")

# 全局线程锁：保护 MD5 指纹文件的并发写入安全性
# 当多用户同时上传文档时，此锁防止两个线程同时写入导致文件损坏
_md5_cache_lock = threading.Lock()

class EnterpriseKBService:
    """
    企业级知识库服务中心。
    负责从“原材料（上传的文档）”到“成品（持久化的向量）”的全自动化加工流程。
    """
    
    def __init__(self) -> None:
        """
        构造函数：初始化向量库连接与切分算法策略。
        """
        # 日志记录：子系统启动标识
        logger.info("Booting Knowledge Base Subsystem (MD5 Defense Array & Vectorizer Modules)...")
        
        # 1. 挂载向量数据库后台
        self.chroma = init_vector_store()
        
        # 2. 配置切分器策略：从设置中读取切分参数，不再硬编码
        # chunk_size: 每个块的最大字符数； chunk_overlap: 相邻块重叠字符数（保证语义不丢失）
        self.spliter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    def get_str_digest(self, payload: str) -> str:
        """
        数字指纹生成器：计算输入文本的 MD5 摘要。
        
        Args:
            payload: 文档原始文本内容。
            
        Returns:
            32 位 MD5 十六进制摘要。
        """
        # 将字符串转为 utf-8 字节流并进行 md5 加密后转为十六进制输出
        return hashlib.md5(payload.encode("utf-8")).hexdigest()

    def exists_in_cache(self, str_digest: str) -> bool:
        """
        指纹审计器：检查指纹是否已存在于本地防御池中。
        
        Args:
            str_digest: 待核验的指纹字符串。
            
        Returns:
            若已存在（命中）返回 True，否则返回 False。
        """
        try:
            # 使用上下文管理器打开指纹文件
            with open(MD5_CACHE_PATH, "r", encoding="utf-8") as f:
                # 如果指纹存在于文件中，说明该文件此前已被喂入过
                return str_digest in f.read()
        except FileNotFoundError:
            # 如果文件完全不存在，说明是第一次喂料，直接返回未命中
            return False

    def mark_cache(self, str_digest: str) -> None:
        """
        指纹入库员：将新文档的指纹永久记入防御池。
        内置线程锁，保证高并发场景下文件内容不会损坏。
        
        Args:
            str_digest: 已通过验证的新指纹。
        """
        # 加锁后再写入，防止并发写入竞争条件导致文件损坏
        with _md5_cache_lock:
            # 以“追加模式”打开指纹缓存文件
            with open(MD5_CACHE_PATH, "a", encoding="utf-8") as f:
                # 写入指纹并强制换行
                f.write(str_digest + "\n")

    def sync_to_kb(self, text_payload: str, filename: str) -> Tuple[bool, str]:
        """
        同步中枢：将原始文本同步推入向量知识库。
        
        Args:
            text_payload: 原始全文内容。
            filename: 文件名（用于元数据追踪）。
            
        Returns:
            (成功标志, 交互提示消息)。
        """
        # 1. 计算当前文档的数字指纹
        digest: str = self.get_str_digest(text_payload)
        
        # 2. 执行查重：如果是重复投喂，则触发防御拦截
        if self.exists_in_cache(digest):
            # 记录警告日志：拦截重复上传行为
            logger.warning(f"Rejecting Duplicate Upload! Payload MD5: {digest} exactly matches an existing record.")
            # 返回拦截信号，告知用户已存在
            return False, "系统级拦截：检测到完全一致的原始文档指纹，禁止污染当前语料库空间！"

        # 3. 文档肢解阶段：将长篇大论切分为适合 embedding 处理的小段落
        logger.info("Splitting raw text stream into structured chunks...")
        texts: List[str] = self.spliter.split_text(text_payload)
        
        # 4. 封装元数据：为每一块碎片打上“出生证明（来源文件名）”
        docs: List[Document] = [Document(page_content=t, metadata={"source": filename}) for t in texts]
        
        # 5. 向量持久化阶段：全量并发写入 Chroma
        if docs:
            logger.info(f"Embedding and injecting {len(docs)} documents into Chroma...")
            # 调用底层向量库实例的 add_documents 方法
            self.chroma.add_documents(docs)
            
        # 6. 后处理：在指纹池盖章放行，防止下次被重复投喂
        self.mark_cache(digest)
        
        # 记录成功日志
        logger.info(f"Successfully processed batch and stamped MD5 signature: [{digest}]")
        
        # 返回成功信号
        return True, "原生底层防爆破拦截通过，向量知识已装载完毕并在指纹池内被盖章放行！"
