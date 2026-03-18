import sys
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 定义聊天提示词模板
# MessagesPlaceholder 用于在对话中动态插入一组消息（如对话历史）
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗"),
    ]
)

# 2. 模拟对话历史数据
history_data = [
    ("human", "你来写一个唐诗"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
]

# 3. 格式化并预览提示词
# 调用 invoke 传入包含 history 的字典
# to_string() 可以方便地查看合并后的完整文本
prompt_text = chat_prompt_template.invoke({"history": history_data}).to_string()

print("--- 格式化后的完整提示词预览 ---")
print(prompt_text)

print("\n--- 大模型回复 ---")
# 4. 初始化聊天模型（根据图片使用 qwen3-max）
model = ChatTongyi(model="qwen3-max")

# 5. 调用模型执行推理
res = model.invoke(prompt_text)

print(f"[AI 回答内容]:\n{res.content}")
print("--- 诊断信息 ---")
print(f"1. 消息角色属性 (res.type): {res.type}")
print(f"2. Python 对象类类型 (type(res)): {type(res)}")
print(f"3. 完整对象内容: {res}")

print("\n--- 验证结束 ---")
