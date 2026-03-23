# 导入类型提示库
from typing import List  # 处理列表类型注解
from operator import itemgetter  # 导入对象提取器，用于从字典中取值

# 导入 LangChain 核心组件
from langchain_community.chat_models import ChatTongyi  # 导入阿里云通义千问大模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示词模板与历史占位符
from langchain_core.runnables import RunnablePassthrough  # 导入数据透传组件，用于链条中的数据流转
from langchain_core.output_parsers import StrOutputParser  # 导入字符串输出解析器，将模型返回的对象转为纯文本
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入具备会话记忆功能的链条包装器
from langchain_core.documents import Document  # 导入文档对象模型

# 导入内部核心子模块
from core.vector_store import init_vector_store  # 导入向量库初始化函数
from core.history_manager import session_history_store  # 导入会话历史管理函数
from config.settings import TOP_K_RETRIEVAL  # 导入检索参数（如：取前 3 段）
from utils.logger import get_sys_logger  # 导入系统日志工具

# 实例化当前模块的专用日志记录器
logger = get_sys_logger("RagEngine")

def format_docs(docs: List[Document]) -> str:
    """
    文档清洗过滤器：将检索到的多段 Document 聚合为一段易于 LLM 理解的纯文本。
    
    Args:
        docs: 检索出来的原始文档列表。
        
    Returns:
        使用双换行符拼接后的背景文本。
    """
    # 遍历文档列表，提取 page_content 属性并用双换行拼接
    return "\n\n".join(doc.page_content for doc in docs)


# 1. 定义一个超级简单的“观察哨”函数
# rag_chain.py

def inspect_data(data):
    # 改用全局日志器 logger，它一定会显示在终端
    logger.info("="*30)
    logger.info(f"观测点提示 - 当前字段: {list(data.keys())}")
    
    if "history" in data:
        logger.info(f"-> 历史消息注入状态: 已加载 {len(data['history'])} 条")
        
    if "context" in data:
        # 只打印前 50 个词，防止日志刷屏
        logger.info(f"-> 检索文本注入状态: {data['context'][:50]}...")
    
    logger.info("="*30)
    return data


class RagPipelineEngine:
    """
    Cinemind RAG 一体化推理大电闸。
    负责管理从 用户输入 -> 检索 -> 增强 -> 推理 -> 记忆持久化 的全生命周期。
    """
    
    def __init__(self) -> None:
        """
        构造函数：初始化所有底层算法组件。
        """
        # 记录引擎启动日志
        logger.info("Initializing Top-Level RAG Inference Engine...")
        
        # 1. 初始化大语言模型 (LLM)：默认调用通义千问
        self.llm: ChatTongyi = ChatTongyi()
        
        # 2. 初始化高维向量数据库：ChromaDB
        self.vector_store = init_vector_store()
        
        # 3. 构造检索器 (Retriever)：配置相似度检索参数
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K_RETRIEVAL}  # 仅提取最相关的 K 条记录
        )
        
        # 4. 设计系统提示词防御阵地：确立“影心导购”的人设
        # system 指令：强制模型查表回答，杜绝幻觉
        # history 占位符：自动注入此前的对话上下文
        # human 变量：承接当前用户的提问
        self.prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
            ("system", "🎯 你是影心 Cinemind 品牌旗舰店的星级导购专家。你必须基于【系统灌入的机密语料】对客人详细解答。如果系统缺乏相关库存知识知识，请直接礼貌承认无能为力，严禁出现逻辑幻觉。\n\n【机密库存语料】：\n{context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 5. 组装核心 LCEL 生态链条：
        # 使用 RunnablePassthrough.assign 动态向输入字典中注入 context
        # context 支线：从输入字典提取 input 并透传给检索器，再经过 format_docs 函数转为字符串背景
        # 链条说明：数据准备 (注入 context) | 模版渲染 | 模型推理 | 结果清洗
        self.rag_chain = (
            RunnablePassthrough.assign(
                context=itemgetter("input") | self.retriever | format_docs
            )
            | inspect_data  # <--- 插入观察哨
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        # 6. 挂载会话记忆外壳：将静态链条升级为具备“回头看”能力的动态链条
        self.final_chain: RunnableWithMessageHistory = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history=session_history_store,  # 关联磁盘持久化策略
            input_messages_key="input",  # 指明输入变量名
            history_messages_key="history",  # 指明历史占位符名
        )

    def execute(self, query: str, session_id: str) -> str:
        """
        外部调用接口：执行一次端到端的 RAG 对话。
        
        Args:
            query: 用户提问文本。
            session_id: 唯一会话识别码（用于区分不同客人的导购记录）。
            
        Returns:
            AI 最终产出的导购话术。
        """
        # 记录请求审计日志
        logger.info(f"Incoming Request Hits Engine | Track_ID: {session_id} | Payload: {query[:30]}...")
        
        # 发起链条调用，以字典形式传入 Query，确保 RunnableWithMessageHistory 能正确处理历史 Injection
        return self.final_chain.invoke(
            {"input": query}, 
            config={"configurable": {"session_id": session_id}}
        )
