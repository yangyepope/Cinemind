import sys
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory
import os

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 实例化模型
model = ChatTongyi(model="qwen3-max")

# 2. 定义聊天提示词模板，包含历史记录占位符
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史返回用户问题。"),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

# 3. 结果解析器
str_parser = StrOutputParser()

# 中间调试函数：打印提示词全文
def print_prompt(full_prompt):
    print("\n" + "="*20 + " 完整提示词渲染内容 " + "="*20)
    print(full_prompt.to_string())
    print("="*60 + "\n")
    return full_prompt

# 4. 构建基础链条 (包含调试步骤)
base_chain = prompt | print_prompt | model | str_parser

# 5. 会话历史存储 (内存字典)
store = {}

# 获取指定 session_id 的历史对象
def get_history(session_id: str):
    # 确保存储目录存在
    session_dir = os.path.join(os.path.dirname(__file__), "sessions")
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # 构造历史记录文件路径
    file_path = os.path.join(session_dir, f"{session_id}.json")
    
    # 返回基于文件的历史记录对象
    return FileChatMessageHistory(file_path)

# 6. 整合会话记忆功能
# 将基础链条包装，使其具备自动存取历史的能力
with_message_history = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",          # 用户输入的 key
    history_messages_key="chat_history", # 历史记录在提示词中的 key
)

if __name__ == '__main__':
    # 配置会话标识
    config_a = {"configurable": {"session_id": "user_a"}}
    # config_b = {"configurable": {"session_id": "user_b"}}

    print("--- 场景 1: 用户 A 的第一轮对话 ---")
    res1 = with_message_history.invoke({"input": "小明有两只猫。"}, config=config_a)
    print(f"[AI]: {res1}")

    print("\n--- 场景 2: 用户 A 的第二轮对话 ---")
    res2 = with_message_history.invoke({"input": "小刚有3只狗。"}, config=config_a)
    print(f"[AI]: {res2}")

    print("\n--- 场景 3: 用户 A 的第三轮对话 (应能想起名字) ---")
    res3 = with_message_history.invoke({"input": "一共有多少只宠物？"}, config=config_a)
    print(f"[AI]: {res3}")

    print("\n--- 验证结束 ---")
