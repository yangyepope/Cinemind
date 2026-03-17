import os                  # 用于读取系统环境变量
from openai import OpenAI  # 导入 OpenAI 兼容客户端（阿里云 DashScope 支持此接口）

# -------------------------------------------------------
# 初始化客户端
# 使用阿里云百炼平台的 DashScope API，兼容 OpenAI 接口格式
# API Key 优先从环境变量 DASHSCOPE_API_KEY 读取，读不到则使用默认值
# 请将下方默认值替换为你在 https://bailian.console.aliyun.com/ 获取的真实 Key
# 推荐设置环境变量：$env:DASHSCOPE_API_KEY = "sk-你的key"
# -------------------------------------------------------
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY", "sk-bfb1f4771d92481b93f987dc615c3d17"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里云 DashScope 兼容端点
)

def chat_example():
    """演示如何调用阿里云 Qwen 模型进行对话（流式输出版本）"""
    try:
        # 发起对话请求
        # messages 是对话历史列表，role 有三种：system（系统设定）、user（用户）、assistant（模型回复）
        response = client.chat.completions.create(
            model="qwen-turbo",   # 使用通义千问 Turbo 模型（速度快、价格低）
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."  # 系统提示：设定模型的角色和行为
                },
                {
                    "role": "user",
                    "content": "你好，你在干什么"              # 用户发送的消息内容
                }
            ],
            stream=True,  # 开启流式输出：模型边生成边返回，避免长时间等待
        )

        # 逐块接收并打印流式返回的内容
        print("Assistant: ", end="", flush=True)  # 先打印前缀，不换行
        for chunk in response:                     # 遍历每个数据块
            # chunk.choices[0].delta.content 是当前块的文字片段，可能为 None
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)  # 实时打印，不换行
        print()  # 全部内容输出完毕后换行

    except Exception as e:
        # 捕获所有异常并打印错误信息（如网络错误、鉴权失败、模型不存在等）
        print(f"发生错误：{e}")

# 程序入口：直接运行此文件时执行，被其他模块导入时不执行
if __name__ == "__main__":
    chat_example()

