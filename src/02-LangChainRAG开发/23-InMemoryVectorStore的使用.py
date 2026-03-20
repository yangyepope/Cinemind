import sys
from pathlib import Path
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 0. 定义绝对路径 (相对于脚本文件，最稳健)
current_dir = Path(__file__).parent
file_path = current_dir / "data" / "info.csv"

# 1. 初始化向量存储 (向量数据库)
# 向量数据库 存储的是 向量 也就是 数字
# 而大模型 也就是 Embedding 负责将 字符 转换成 数字 (向量)
# 所以 InMemoryVectorStore 在初始化的时候 必须 传入一个 嵌入模型
# 确保已设置 DASHSCOPE_API_KEY 环境变量
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

# 2. 加载 CSV 数据
loader = CSVLoader(
    file_path=str(file_path),
    encoding="utf-8",
    source_column="source",     # 指定本条数据的来源是哪里
)

# 3. 加载文档
documents = loader.load()

# 4. 向量存储的 新增、删除、检索
# id1 id2 id3 id4 ...
# 向向量存储中 添加 文档
print("--- 正在添加文档到向量数据库 ---")
vector_store.add_documents(
    documents=documents,           # 被添加的文档, 类型: list[Document]
    ids=["id" + str(i) for i in range(1, len(documents) + 1)]  # 给添加的文档提供id (字符型)
)

# 5. 删除文档 (示例: 传入 [id, id...])
print("--- 正在演示删除文档: id1, id2 ---")
vector_store.delete(["id1", "id2"])

# 6. 检索相似文档
# 检索 返回类型 list[Document]
print("--- 正在进行相似度搜索: 'Python是不是简单易学呀' ---")
result = vector_store.similarity_search(
    query="Python是不是简单易学呀",
    k=3            # 检索的结果要几个
)

# 7. 打印检索结果
print("\n--- 检索结果如下 ---")
for i, doc in enumerate(result):
    print(f"结果 {i+1}:")
    print(f"内容: {doc.page_content}")
    print(f"来源: {doc.metadata.get('source')}")
    print("-" * 20)
