import sys # 导入系统底层库，用于环境相关配置
import os  # 导入文件路径操作库，保证跨平台路径兼容
import json # 导入 JSON 数据交换格式库，用于基础数据处理
from typing import List, Dict, Any, Sequence # 导入常用类型提示工具，提高 IDE 代码智能感知
from pydantic import BaseModel, Field # 导入 Pydantic 基类与字段映射器，实现数据强校验

# 从 LangChain 核心包导入聊天模型、提示词模板及相关核心组件
from langchain_community.chat_models.tongyi import ChatTongyi # 阿里云通义千问模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # 动态提示词与消息占位符
from langchain_core.output_parsers import StrOutputParser # 将对话输出转为纯字符串的解析器
from langchain_core.runnables.history import RunnableWithMessageHistory # 赋予 Runnable 会话记忆能力的装饰器
from langchain_core.chat_history import BaseChatMessageHistory # 聊天历史记录管理器的标准基类接口

# --- 关键导入：导入 LangChain 官方推荐的消息序列化工具 ---
from langchain_core.messages import (
    BaseMessage,        # 所有消息类型的基类
    message_to_dict,    # 将消息对象安全转为标准字典的方法 (官方工具)
    messages_from_dict  # 将标准字典列表一键还原为消息对象的方法 (官方工具)
)

# 在 Windows 操作系统环境下执行时，强制切换标准输出流为 UTF-8 编码，防止中文终端显示乱码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# --- 1. Pydantic 模型定义：专门用于定义存储在磁盘上的 JSON 结构 ---

class SessionHistoryModel(BaseModel):
    """
    会话历史持久化模型：
    利用 Pydantic 确保存储在本地 JSON 里的数据格式百分之百符合预期。
    """
    session_id: str = Field(..., description="唯一会话 ID，用于查找用户记忆") # 必填字段
    # 直接存储官方字典格式：官方 message_to_dict 会自动处理 Human, AI, System, Tool 等各种类型
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="包含所有对话记录的标准字典列表") 

# --- 2. 自定义历史管理类：深度整合官方序列化逻辑与 Pydantic 校验 ---

class OfficialPydanticHistory(BaseChatMessageHistory):
    """
    使用官方序列化工具与 Pydantic 结合实现的长期记忆管理类。
    """
    def __init__(self, session_id: str, storage_root: str = "sessions_official"):
        """
        初始化管理器：设置会话 ID 并预备好存储目录
        :param session_id: 当前会话的唯一标识
        :param storage_root: 存放记录文件的本地根目录
        """
        self.session_id = session_id # 保存当前会话身份
        self.storage_root = storage_root # 保存记录根路径
        # 拼接出该会话对应的 JSON 文件物理全路径
        self.file_path = os.path.join(self.storage_root, f"{session_id}.json")
        
        # 启动时主动检查存储目录是否存在，若缺失则递归创建所有层级的文件夹
        if not os.path.exists(self.storage_root):
            os.makedirs(self.storage_root) # 按需创建文件夹

    @property
    def messages(self) -> List[BaseMessage]:
        """
        该属性负责从硬盘读取、校验并实时还原消息对象。
        :return: 返回 LangChain 可以识别的 BaseMessage 对象列表
        """
        if not os.path.exists(self.file_path): # 如果该用户还没有历史记录文件
            return [] # 视为新对话，直接返回空列表
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f: # 开启 UTF-8 编码的读取流
                raw_data = json.load(f) # 载入 JSON 字符串并转为 Python 原生字典
                # 通过 Pydantic 校验数据的完整性：如果不符合模型定义，这里会立即抛出清晰的错误
                validated_session = SessionHistoryModel.model_validate(raw_data)
                
                # --- 调用核心黑科技：官方 messages_from_dict ---
                # 该函数能完美将由 message_to_dict 产生的字典序列，精准还原为消息实例类
                return messages_from_dict(validated_session.messages) 
        except Exception as err: # 拦截文件读取、解码或 Pydantic 验证中可能出现的异常
            print(f"读取历史文件发生致命异常 [{self.session_id}]: {err}") # 打印错误详细信息，方便排查
            return [] # 报错时保守返回空列表，避免整个链条崩溃

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        当对话发生变化时，将捕获到的新消息序列批量追加并刷写到磁盘文件中。
        :param messages: LangChain 传递进来的实时消息序列
        """
        # 第一步：准备好 Session 模型容器
        current_data = None
        
        # 第二步：尝试读取磁盘上现有的历史片段
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    old_raw = json.load(f)
                    current_data = SessionHistoryModel.model_validate(old_raw)
            except Exception:
                pass
        
        # 如果是新会话，则创建一个空白模型
        if not current_data:
            current_data = SessionHistoryModel(session_id=self.session_id)
        
        # --- 第三步：批量调用官方序列化工具 ---
        # 使用列表推导式一次性处理所有传入的消息
        new_dicts = [message_to_dict(m) for m in messages]
        
        # 第四步：将转化后的字典列表追加到模型中
        current_data.messages.extend(new_dicts)

        # 第五步：执行物理持久化（仅需一次写入操作）
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(current_data.model_dump_json(indent=2))

    def clear(self) -> None:
        """
        应用户或业务系统的请求，彻底抹除该 Session 的物理记录文件（谨慎操作）
        """
        if os.path.exists(self.file_path): # 严谨判断文件存在性
            os.remove(self.file_path) # 执行磁盘文件删除操作

# --- 3. 核心应用场景逻辑构建 ---

# 实例化大语言模型（此处以阿里的通义千问 3.0 最大规模模型为例）
tongyi_llm = ChatTongyi(model="qwen3-max")

# 编排包含上下文语义环境的提示词脚手架
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你现在不仅具备短期记忆，还通过持久化文件具备了长期记忆能力。请务必结合上下文为大卫服务。"), # 顶层人格设定
    MessagesPlaceholder("chat_history"), # 动态历史消息插入点
    ("human", "{input}") # 用
])

# 利用 LCEL 管道连接符，极简构建出“模板 -> 模型 -> 字符串”的核心处理路径
core_inference_chain = chat_prompt_template | tongyi_llm | StrOutputParser()

def factory_get_history(session_id: str) -> BaseChatMessageHistory:
    """
    提供给 LangChain 回调层使用的“历史工厂函数”
    """
    # 获取运行当前代码文件的本地绝对位置，确保在任何工作目录下调用均能正确找到存储点
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    # 定义该项目的长期记忆存放核心仓库目录：sessions_official
    target_vault_dir = os.path.join(workspace_dir, "sessions_official")
    # 构造并返回真正负责读写磁盘的逻辑句柄
    return OfficialPydanticHistory(session_id, storage_root=target_vault_dir)

# 将核心对话逻辑通过 RunnableWithMessageHistory 进行最后一道包装，激活自动存储与加载历史的神奇功能
final_application_chain = RunnableWithMessageHistory(
    core_inference_chain,          # 核心大模型推理链
    factory_get_history,           # 根据运行时配置实时生成/寻找历史记录的工厂
    input_messages_key="input",    # 系统从输入字典中读取查询内容的 Key
    history_messages_key="chat_history" # 系统回填历史记录到提示词模板时对应的槽位名
)

# --- 4. 程序的主入口演示：在此见证长期记忆的神奇表现 ---

if __name__ == "__main__":
    # 配置本次对话环节的元数据标识：将用户 A 命名为 'dave_long_term'
    runtime_configs = {"configurable": {"session_id": "dave_long_term"}}
    
    # print("\n>>> 官方优化版：长期会话记忆系统运行中 <<<\n")
    
    # # 模拟第一次场景：大卫向助手透露了隐私信息
    # print("--- 步骤 1：告知个人特征（建立长期记忆点） ---")
    # step_1_res = final_application_chain.invoke({"input": "我是大卫。我非常喜欢喝拿铁咖啡。"}, config=runtime_configs)
    # print(f"助手回复: {step_1_res}")

    # # 模拟第二次场景：测试跨运行（Persistence）状态下的逻辑保持能力
    # print("\n--- 步骤 2：深度语义召回演示 ---")
    # step_2_res = final_application_chain.invoke({"input": "我记不清我喜欢喝什么了，你能告诉我是哪种咖啡吗？"}, config=runtime_configs)
    # print(f"助手回复: {step_2_res}") # 由于已持久化，AI 能够直接从 sessions_official/dave_long_term.json 中读取并回答

    # print("\n>>> 演示圆满成功：记忆已通过官方标准格式安全存盘 <<<")
    step_1_res = final_application_chain.invoke({"input": "我是谁，我喜欢喝什么"}, config=runtime_configs)
    print(f"助手回复: {step_1_res}")
