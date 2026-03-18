import os
import sys
# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# langchain_community
from langchain_community.chat_models.tongyi import ChatTongyi

# 得到模型对象
# 填写 api_key 或设置 DASHSCOPE_API_KEY 环境变量
model = ChatTongyi(
    model="qwen3-max",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
)

# 简化消息列表写法：使用元组形式替代显式的 Message 对象
messages = [
    ("system", "你是一位唐诗专家，请用唐诗的风格回答"),
    ("human", "写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照这个风格，再写一首关于春天的唐诗")
]

# 调用stream流式执行
# 这里的 input 直接传入元组列表，LangChain 内部会自动解析
res = model.stream(input=messages)

# for循环迭代打印输出
for chunk in res:
    # 这里的 chunk 依然是消息块对象，需要通过 .content 获取文本
    print(chunk.content, end="", flush=True)

print("\n--- 输出结束 ---")
