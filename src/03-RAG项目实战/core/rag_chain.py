# 导入类型提示库
from typing import List  # 处理列表类型注解

# 导入 LangChain 核心组件
from langchain_community.chat_models import ChatTongyi  # 导入阿里云通义千问大模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示词模板与历史占位符
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableBranch
)  # 导入数据流转与控制组件
from langchain_core.output_parsers import StrOutputParser  # 导入字符串输出解析器
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入会话记忆包装器
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


# 指代词与省略语义词典：若用户输入包含这些词，则说明问题依赖上下文，需要 LLM 重写
# 否则视为独立完整问题，直接跳过重写链，节省一次 LLM 调用（Token + 延迟减半）
_REFERENCE_KEYWORDS = [
    "它", "他", "她", "它们", "他们", "她们",
    "这个", "那个", "这种", "那种", "这款", "那款",
    "上面", "上述", "前面", "刚才", "之前说的",
    "这", "那", "此", "该",
]

def _needs_rewrite(input_text: str) -> bool:
    """
    短路检测器：判断用户当前输入是否包含指代词或省略语义。
    
    原理：
        - 有指代词 → 问题语义不完整 → 必须触发 LLM 重写以补全语义
        - 无指代词 → 问题自包含    → 直接跳过重写，节省一次 LLM 调用
    
    Args:
        input_text: 用户的原始输入字符串。
    
    Returns:
        True 表示需要重写，False 表示可以直接用原始输入检索。
    """
    return any(keyword in input_text for keyword in _REFERENCE_KEYWORDS)


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
        # 4. 设计“问题重写”防御阵地：将模糊提问转为标准检索 Query
        self.rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", "根据对话历史和当前输入，生成一个【独立且具备完整语义】的搜索查询。仅仅输出重写后的查询字符串，不要有任何多余解释。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.rewrite_chain = self.rewrite_prompt | self.llm | StrOutputParser()

        # 5. 设计系统提示词防御阵地：确立“影心导购”的人设
        self.prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
            ("system", "🎯 你是影心 Cinemind 品牌旗舰店的星级导购专家。你必须基于【系统灌入的机密语料】对客人详细解答。如果系统缺乏相关库存知识知识，请直接礼貌承认无能为力，严禁出现逻辑幻觉。\n\n【机密库存语料】：\n{context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 6. 组装核心 LCEL 生态链条：
        # 第一部分：数据增强支线 (Context + 短路重写)
        # 优化说明：引入 _needs_rewrite 短路机制
        # - 若问题含指代词（如"它", "这个"）→ 触发 LLM 重写（第 1 次 LLM 调用）
        # - 若问题语义自包含                 → 直接复用原始 input，跳过重写，节省一次调用
        def smart_rewrite(x: dict) -> str:
            """智能重写路由：按需触发 LLM 改写，避免不必要的双重调用。"""
            if _needs_rewrite(x["input"]):
                # 检测到指代词，上下文依赖，必须重写
                logger.debug(f"[QueryRewrite] 检测到指代词，触发 LLM 重写 | 原始: {x['input'][:30]}")
                return self.rewrite_chain.invoke(x)
            else:
                # 问题自包含，直接透传原始输入
                logger.debug(f"[QueryRewrite] 问题自包含，跳过重写 | 原始: {x['input'][:30]}")
                return x["input"]

        data_prepare_chain = RunnablePassthrough.assign(
            # 通过 smart_rewrite 按需决定是否调用 LLM
            standalone_query = RunnableLambda(smart_rewrite),
            # 用 standalone_query 的结果去向量库检索相关文档
            context = (lambda x: x.get("standalone_query", x["input"])) | self.retriever | format_docs
        )

        # 第二部分：防御性分支（熔断机制）
        # 优先级逻辑：
        # 1. 如果输入包含常见的人设/基础对话关键词，允许直达 LLM 触发人设回复
        # 2. 如果 standalone_query 判定为不需要检索（由 LLM 重写阶段决定）也可以直达
        # 3. 只有明确需要知识库且 context 为空时，才熔断
        
        branching_chain = RunnableBranch(
            (
                # 分支 A：人设与元对话识别（启发式关键词匹配）
                # 覆盖场景：
                #   - 问候与寒暄：你好、早上好、在吗 等
                #   - 人设询问：你是谁、你是AI吗、你有什么功能 等
                #   - 求助与引导：帮我、怎么用、如何开始 等
                #   - 情绪表达：谢谢、太厉害了、好的 等（避免错误进入检索）
                #   - 退出与结束：再见、拜拜、结束 等
                #   - 购物引导：我想买、推荐一下、帮我选 等（直达人设引导）
                lambda x: any(k in x["input"].lower() for k in [
                    # --- 问候与寒暄 ---
                    "你好", "您好", "hi", "hello", "早上好", "下午好", "晚上好",
                    "在吗", "在不在", "有人吗", "客服", "人工",
                    # --- 人设与身份询问 ---
                    "你是谁", "你是什么", "你是ai", "你是机器人", "你是人吗",
                    "你是哪位", "你叫什么", "你的名字", "介绍一下你自己",
                    "你有什么功能", "功能", "你能做什么", "你会什么",
                    "你是影心吗", "你是导购吗",
                    # --- 求助与操作引导 ---
                    "帮我", "帮一下", "请帮", "怎么用", "如何使用",
                    "怎么开始", "如何开始", "怎么操作", "教我",
                    "我不会", "我该怎么", "我应该怎么",
                    # --- 购物意图引导 ---
                    "我想买", "我要买", "想购买", "帮我选", "推荐一下",
                    "有什么推荐", "什么好", "买什么好", "怎么选",
                    # --- 情绪与反馈 ---
                    "谢谢", "感谢", "太棒了", "好的", "明白了",
                    "知道了", "了解了", "收到", "666", "厉害",
                    # --- 退出与结束 ---
                    "再见", "拜拜", "bye", "结束", "退出", "没问题了", "就这样",
                ]),
                self.prompt | self.llm | StrOutputParser()
            ),
            (
                # 分支 B：知识检索缺失（物理熔断）
                lambda x: not x["context"].strip() or "无能为力" in x["context"],
                RunnableLambda(lambda x: "🎯 尊敬的客人，关于您的这个问题，影心机密库中暂时没有查到详细记录。您可以尝试换一个问法，或者咨询人工客服。")
            ),
            # 默认分支：正常 RAG 推理
            self.prompt | self.llm | StrOutputParser()
        )

        self.rag_chain = (
            data_prepare_chain
            | inspect_data  # <--- 插入观察哨
            | branching_chain
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
