"""
演示LangChain中的文本嵌入模型
计算余弦相似度
"""

import os
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

# 1. 实例化嵌入模型对象
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-v3", # 阿里云 DashScope 的兼容模型名
    # langchain 中必须补充完整的 api base 链接，且要带上 /v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    check_embedding_ctx_length=False # 重点：关闭 token 计算，因为 DashScope 接口不接受 pre-tokenized 的 token ID 列表
)

# 2. 准备文本
text1 = "股票市场今日大涨，投资者乐观。"
text2 = "持续上涨的市场让投资者感到满意。"
text3 = "央行降息，刺激经济增长。"
text4 = "股票市场今日大涨，投资者很高兴。"
text5 = "股票市场今日大涨，投资者很悲伤。"
text6 = "股票市场今日大涨，投资者很乐。"

# 3. 对文本进行词嵌入计算（将文本转换为向量）
embed1 = embeddings_model.embed_query(text1)
embed2 = embeddings_model.embed_query(text2)
embed3 = embeddings_model.embed_query(text3)
embed4 = embeddings_model.embed_query(text4)
embed5 = embeddings_model.embed_query(text5)
embed6 = embeddings_model.embed_query(text6)

# 4. 计算余弦相似度
# cosine_similarity 接受的是二维数组，所以我们需要将一维的向量放在列表中传入
# 返回结果也是个二维数组，取 [0][0] 即为相似度标量值
score12 = cosine_similarity([embed1], [embed2])[0][0]
score13 = cosine_similarity([embed1], [embed3])[0][0]
score14 = cosine_similarity([embed1], [embed4])[0][0]
score15 = cosine_similarity([embed1], [embed5])[0][0]
score16 = cosine_similarity([embed1], [embed6])[0][0]

print(f"[{text1}] 和 [{text2}] 的余弦相似度：{score12}")
print(f"[{text1}] 和 [{text3}] 的余弦相似度：{score13}")
print(f"[{text1}] 和 [{text4}] 的余弦相似度：{score14}")
print(f"[{text1}] 和 [{text5}] 的余弦相似度：{score15}")
print(f"[{text1}] 和 [{text6}] 的余弦相似度：{score16}")
