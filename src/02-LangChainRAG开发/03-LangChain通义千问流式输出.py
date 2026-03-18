import os
import sys
# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# langchain_community
from langchain_community.llms.tongyi import Tongyi

# 初始化模型
# 填写 api_key 或设置 DASHSCOPE_API_KEY 环境变量
model = Tongyi(
    model="qwen-max",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
)

# 使用 stream 方法进行流式输出
print("--- 开始流式输出 ---")
# 这里的 input 可以是字符串，也可以是消息列表
for chunk in model.stream(input="请写一段关于人工智能未来发展的短评。"):
    # 打印每个数据块，设置 flush=True 确保实时同步到终端，end="" 防止自动换行
    print(chunk, end="", flush=True)

print("\n--- 输出结束 ---")
