import os
import sys
# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# langchain_community
from langchain_community.llms.tongyi import Tongyi

# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
# 填写 api_key 或设置 DASHSCOPE_API_KEY 环境变量
model = Tongyi(
    model="qwen-max",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
)

# 调用invoke向模型提问
res = model.invoke(input="你是谁呀能做什么？")

print(res)
