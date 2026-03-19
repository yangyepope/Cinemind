import sys
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 初始化模型和解析器
model = ChatTongyi(model="qwen3-max")
str_parser = StrOutputParser()

# 2. 定义第一个提示词模板：负责起名
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，仅告知我名字，不要额外信息。"
)

# 3. 定义第二个提示词模板：负责解析名字含义
second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我解析含义。"
)

# 4. 定义自定义转换逻辑 (RunnableLambda)
# 作用：将第一个模型的输出 (AIMessage) 转换为第二个模板需要的字典格式 ({"name": "xxx"})
# 函数的入参: AIMessage -> dict ({"name": "xxx"})
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 5. 组合链 (Chain)
# 链路：起名模板 | 起名模型 | 自定义转换逻辑 | 解析模板 | 解析模型 | 字符串解析器
chain = first_prompt | model | my_func | second_prompt | model | str_parser

if __name__ == '__main__':
    print("--- 正在通过 RunnableLambda 执行双重 Prompt 链式调用 ---")
    
    # 6. 执行调用 (使用流式输出)
    input_data = {"lastname": "曹", "gender": "女孩"}
    for chunk in chain.stream(input_data):
        print(chunk, end="", flush=True)

    print("\n--- 验证结束 ---")
