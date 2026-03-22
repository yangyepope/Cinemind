import sys
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

# 1. 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 2. 初始化模型
# 使用通义千问大模型
model = ChatTongyi(model="qwen-max")

# 3. 定义提示词模板
# {} 为占位符，由后面相似度搜索的结果 context 和用户输入 input 填充
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "以为我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}。",
        ),
        ("user", "用户提问：{input}"),
    ]
)

# 4. 初始化向量存储并配置嵌入模型 (text-embedding-v3)
# InMemoryVectorStore 是内存存储，适合简单场景
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

# 5. 准备资料（模拟向向量库中添加背景知识）
# add_texts 接收一个 list[str]
print("--- 正在向向量库添加参考资料 ---")
vector_store.add_texts(
    [
        # "减肥就是要少吃多练",
        # "在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来",
        # "跑步是很好的运动哦",
        # "123"
    ]
)

# 6. 用户输入
input_text = "怎么减肥？"

# langchain中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"

    return formatted_str


# 定义辅助显示函数
def print_prompt(p):
    """打印渲染后的提示词以供观察"""
    print("\n--- 最终生成的提示词 ---")
    print(p.to_string())
    print("=" * 30)
    return p


# chain
chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func}
    | prompt
    | print_prompt
    | model
    | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)
"""
retriever:
    - 输入：用户的提问       str
    - 输出：向量库的检索结果   list[Document]
prompt:
    - 输入：用户的提问 + 向量库的检索结果 dict
    - 输出：完整的提示词       PromptValue
"""
