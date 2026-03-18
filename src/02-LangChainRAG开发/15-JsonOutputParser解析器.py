import sys
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 初始化聊天模型
model = ChatTongyi(model="qwen3-max")

# 2. 第一个提示词模板：要求输出 JSON
# 注意：提示词明确要求返回 JSON 格式，且 key 为 name
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，"
    "并封装为JSON格式返回给我。要求key是name，value就是你起的名字，请严格遵守格式要求。"
)

# 3. 第二个提示词模板：接收第一个模板解析后的 {name} 变量
second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

# 4. 初始化解析器
# JsonOutputParser 的作用是将模型返回的 JSON 字符串解析为 Python 的 dict 对象
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

# 5. 构建链 (Chain)
# 逻辑流转：
# prompt1 -> model -> (JSON字符串) -> json_parser -> (dict) -> prompt2 -> model -> (AIMessage) -> str_parser -> (str)
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

# 6. 调用链（升级为流式输出）
print("--- 正在执行双重 Prompt 链式解析 (JSON -> Dict -> String) ---")
print("提示：由于中间涉及 JSON 解析，结果将在第一个模型完成起名后开始流式渲染...\n")

# 使用 stream 方法进行流式调用
# 注意：在多级 Chain 中，前序步骤（Json解析）完成后，后续输出将逐字流出
for chunk in chain.stream({"lastname": "张", "gender": "女儿"}):
    print(chunk, end="", flush=True)

print("\n\n--- 验证结束 ---")
