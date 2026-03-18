
import sys
from langchain_community.embeddings import DashScopeEmbeddings

# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 创建模型对象
# 确保已设置 DASHSCOPE_API_KEY 环境变量
model = DashScopeEmbeddings()

print("--- 1. 单个查询嵌入 (embed_query) ---")
# 用于为一个字符串生成嵌入向量
query_text = "我喜欢你"
query_result = model.embed_query(query_text)
print(f"文本: '{query_text}'")
print(f"向量维度: {len(query_result)}")
print(f"向量前5位: {query_result[:5]}...")

print("\n--- 2. 批量文档嵌入 (embed_documents) ---")
# 用于为一组字符串生成嵌入向量（通常用于构建向量数据库）
doc_texts = ["我喜欢你", "我讨厌你"] * 5 # 模拟批量数据
doc_results = model.embed_documents(doc_texts)
print(f"输入文档数量: {len(doc_texts)}")
print(f"返回向量数量: {len(doc_results)}")
print(f"首个向量维度: {len(doc_results[0])}")
print(f"首个向量前5位: {doc_results[0][:5]}...")

print("\n--- 验证结束 ---")
