import sys
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 0. 定义路径 (相对于脚本文件)
current_dir = Path(__file__).parent
file_path = current_dir / "data" / "info.csv"
persist_db_path = current_dir / "data" / "chroma_db"

# 1. 初始化向量存储 (Chroma 持续化存储)
# 确保已设置 DASHSCOPE_API_KEY 环境变量
print(f"--- 正在初始化 Chroma 数据库: {persist_db_path.name} ---")
vector_store = Chroma(
    persist_directory=str(persist_db_path),
    embedding_function=DashScopeEmbeddings()
)

# 2. 加载 CSV 数据
# loader = CSVLoader(
#     file_path=str(file_path),
#     encoding="utf-8",
#     source_column="source",
# )

# documents = loader.load()

# # 3. 添加文档到向量存储
# # 注意：Chroma 会自动处理持久化
# print("--- 正在添加文档到 Chroma ---")
# vector_store.add_documents(
#     documents=documents,
#     ids=["id" + str(i) for i in range(1, len(documents) + 1)]
# )

# # 4. 演示删除文档 (示例: id1, id2)
# print("--- 正在演示删除文档: id1, id2 ---")
# vector_store.delete(["id1", "id2"])

# 5. 相似度搜索
print("--- 正在搜索: 'Python是不是简单易学呀' ---")
result = vector_store.similarity_search(
    query="Python是不是简单易学呀",
    k=3
)

# 6. 打印结果
print("\n--- 检索结果如下 ---")
for i, doc in enumerate(result):
    print(f"结果 {i+1}:")
    print(f"内容: {doc.page_content}")
    print(f"来源: {doc.metadata.get('source')}")
    print("-" * 20)

print(f"✅ 数据库已持久化保存至: {persist_db_path}")
