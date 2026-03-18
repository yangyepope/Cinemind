import sys
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 定义聊天提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗"),
    ]
)

# 2. 准备对话历史数据
history_data = [
    ("human", "你来写一个唐诗"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
]

# 3. 初始化聊天模型
model = ChatTongyi(model="qwen3-max")

# 4. 组成链：要求每一个组件都是 Runnable 接口的子类
# 使用 | 符号实现 LCEL (LangChain 表达式语言)
chain = chat_prompt_template | model

print("--- 正在通过链 (Chain) 发起调用 ---")
# 5. 通过链去调用 invoke
# 输入为字典，包含模板对应的占位符变量
# res = chain.invoke({"history": history_data})

# print(f"[AI 回答]:\n{res.content}")

# print("\n--- 验证结束 ---")

for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end="", flush=True)
