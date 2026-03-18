import sys
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. 初始化聊天模型
model = ChatTongyi(model="qwen3-max")

# 2. 定义提示词模板
prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其它内容。"
)

# 3. 组成链：此处演示 prompt | model | model 的错误用法（或作为引子）
# 注意：直接将模型输出（AIMessage）传给另一个模型通常会报错，除非中间有解析器
chain = prompt | model | model

# 4. 调用链
# 预警：此行代码运行时可能会由于模型输出类型不匹配而报错，这正是教学中引出 StrOutputParser 的原因
try:
    res = chain.invoke({"lastname": "张", "gender": "女儿"})
    print(res.content)
except Exception as e:
    """
    Invalid input type <class 'langchain_core.messages.ai.AIMessage'>. 
    Must be a PromptValue, str, or list of BaseMessages.
    
    """

    print(f"\n[运行报错，符合教学预期]: {e}")
    print(
        "提示：这是因为模型输出的是 AIMessage 对象，不能直接作为下一个模型的输入。需要使用 StrOutputParser 处理。"
    )

# 5. 展示“第二个示例（正确用法）”
# StrOutputParser 的作用是将 AIMessage 提取为字符串，这样第二个模型就能直接处理了
parser = StrOutputParser()

# 构建正确链条: 提示词 -> 模型 -> 解析器 -> 模型
chain_fixed = prompt | model | parser | model

print("\n--- 第二个示例：修正后的链式调用 (使用 StrOutputParser) ---")
try:
    res_fixed = chain_fixed.invoke({"lastname": "张", "gender": "女儿"})
    print(f"[最终回答]:\n{res_fixed.content}")
except Exception as e:
    print(f"[意外错误]: {e}")

# 6. 展示“第三个示例：连环解析（最终输出纯文本）”
# 结构: 提示词 -> 模型 -> 解析器 -> 模型 -> 解析器
# 通过在末尾再加一层 parser，最终invoke的结果将直接是 str 类型，而非 AIMessage
chain_triple = prompt | model | parser | model | parser

print("\n--- 第三个示例：连环解析后的链式调用 (最终输出字符串) ---")
try:
    res_final = chain_triple.invoke({"lastname": "张", "gender": "女儿"})
    print(f"[最终解析后的文本结果]:\n{res_final}")
    print(f"验证返回类型: {type(res_final)}")
except Exception as e:
    print(f"[意外错误]: {e}")
