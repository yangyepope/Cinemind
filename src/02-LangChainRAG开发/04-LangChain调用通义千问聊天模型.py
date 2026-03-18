import os
import sys
# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# langchain_community
from langchain_community.chat_models.tongyi import ChatTongyi
# langchain_core.messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 得到模型对象，qwen3-max就是聊天模型
# 填写 api_key 或设置 DASHSCOPE_API_KEY 环境变量
model = ChatTongyi(
    model="qwen3-max",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
)

# 准备消息列表
messages = [
    SystemMessage(content="你是一位唐诗专家，请用唐诗的风格回答"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照这个风格，再写一首关于春天的唐诗")
]

# 调用stream流式执行
res = model.stream(input=messages)

# for循环迭代打印输出，通过.content来获取到内容
for chunk in res:
    print(chunk.content, end="", flush=True)
