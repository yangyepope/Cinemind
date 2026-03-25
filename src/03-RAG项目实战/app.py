"""
 Cinemind 03-RAG 实战项目 - 主程序入口 (Main Application)

 负责构建 2C 端对话界面，集成 RAG 语音引擎与历史会话流。
 包含：密码鉴权（防止未授权访问）、请求限速（防止 API 成本失控）。
"""


# 导入 Streamlit 核心库用于构建 Web 界面
import streamlit as st
# 导入 UUID 库用于生成唯一的会话 ID
import uuid
# 导入时间库用于计算推理耗时与限速
import time
from datetime import datetime

# 导入业务层核心引擎与日志工具
from core.rag_chain import RagPipelineEngine  # 导入具备 LCEL 链条的 RAG 引擎
from utils.logger import get_sys_logger  # 导入全局日志记录器

# --- Asyncio & Debug 补丁 ---
try:
    from langchain_core.globals import set_debug
    set_debug(False)
except ImportError:
    pass

# 实例化本模块专用日志器
logger = get_sys_logger("MainApp")

# ============================================================
# 安全层 1：密码鉴权（Authentication Guard）
# 读取 .streamlit/secrets.toml 中的 APP_PASSWORD 字段
# 若未配置，默认任何人均可访问（适用于开发模式）
# 生产环境请在 secrets.toml 中配置：APP_PASSWORD = "你的密码"
# ============================================================
def _check_auth() -> bool:
    """
    检查用户是否已通过密码鉴权。
    使用 st.session_state 记录鉴权状态，避免每次刷新都要重新输入。
    """
    # 安全属性：尝试从 Streamlit Secrets 读取配置，若文件不存在则静默回退
    try:
        required_password = st.secrets.get("APP_PASSWORD", None)
    except Exception:
        # 兼容性处理：若无 secrets.toml 文件，则默认不开启密码
        required_password = None

    # 若未配置密码，直接放行（开发模式）
    if not required_password:
        return True

    # 检查当前会话是否已鉴权通过
    if st.session_state.get("authenticated", False):
        return True

    # 展示密码输入界面
    st.title("🔐 影心 Cinemind — 访问验证")
    password_input = st.text_input("请输入访问密码：", type="password")
    if st.button("确认进入"):
        if password_input == required_password:
            st.session_state.authenticated = True
            # 鉴权成功，强制刷新以进入主界面
            st.rerun()
        else:
            st.error("❌ 密码错误，请联系管理员获取访问权限。")
    return False


# --- 优先执行鉴权检查，鉴权未通过则停止渲染主界面 ---
if not _check_auth():
    st.stop()

# ============================================================
# 安全层 2：请求限速（Rate Limiting）
# 每分钟最大请求次数通过 secrets 配置，默认 10 次/分钟
# 防止单用户大量调用导致 API 成本失控
# ============================================================
try:
    _MAX_REQUESTS_PER_MINUTE: int = int(st.secrets.get("MAX_REQUESTS_PER_MINUTE", 3))
except Exception:
    # 备选库：若无 secrets 配置，默认每分钟限速 3 次
    _MAX_REQUESTS_PER_MINUTE = 3

def _check_rate_limit() -> bool:
    """
    检查当前会话是否超过限速阈值（每分钟最大请求次数）。

    Returns:
        True 表示允许继续，False 表示已超速拦截。
    """
    now = datetime.now()

    # 初始化限速状态（首次访问）
    if "rate_limit_requests" not in st.session_state:
        st.session_state.rate_limit_requests = []

    # 清理 1 分钟以前的请求记录（滑动窗口）
    st.session_state.rate_limit_requests = [
        t for t in st.session_state.rate_limit_requests
        if (now - t).total_seconds() < 60
    ]

    # 检查是否超出阈值
    if len(st.session_state.rate_limit_requests) >= _MAX_REQUESTS_PER_MINUTE:
        return False

    # 记录本次请求时间戳
    st.session_state.rate_limit_requests.append(now)
    return True


# --- 1. 页面级全局配置 ---

# 设置网页标签、图标及宽屏布局
st.set_page_config(
    page_title="影心 Cinemind - RAG 智能导购",
    page_icon="🤖",
    layout="wide"
)

# --- 2. 核心组件单例化 (保证性能与 Asyncio 稳定) ---

# 使用 st.cache_resource 确保引擎在内存中仅存一份，避免重复初始化导致的资源浪费
@st.cache_resource
def get_rag_engine() -> RagPipelineEngine:
    """
    单例工厂：获取 RAG 推理引擎。
    """
    # 记录日志：首次或刷新后引擎加载
    logger.info("Main Thread Requesting RAG Engine singleton...")
    # 直接实例化对象
    return RagPipelineEngine()

# --- 3. 会话状态与核心逻辑初始化 ---

# 赋予用户一个唯一的 Session ID，用于多轮对话历史的磁盘隔离
if "session_id" not in st.session_state:
    # 随机生成一个 UUID
    st.session_state.session_id = str(uuid.uuid4())
    # 记录日志：新用户分配 ID
    logger.info(f"New Session Identity Assigned: {st.session_state.session_id}")

# --- 4. 侧边栏 UI 布局 ---

# 定义控制台侧边栏
with st.sidebar:
    # 展示品牌标题
    st.title("🛡️ 影心后台控制台")
    # 展示当前生效的会话 ID，方便排错
    st.info(f"当前 Session: {st.session_state.session_id}")
    # 水平分割线
    st.divider()
    # 操作说明说明
    st.caption("注：对话历史已自动序列化至本地数据库，重新启动后可根据 Session ID 找回。")
    # 添加清除当前 UI 视窗记忆的按钮
    if st.button("🗑️ 清除当前视窗记录", use_container_width=True):
        # 清空 session_state 中的历史消息
        st.session_state.messages = []
        # 强制 Streamlit 重新渲染，清空界面
        st.rerun()

# --- 5. 主对话界面渲染 ---

# 展示主页面标题
st.title("🤖 影心 Cinemind - 星级导购")
# 展示子标题描述
st.markdown("---")

# 初始化消息展示池
if "messages" not in st.session_state or not st.session_state.messages:
    # 预设一条来自 AI 导购的情绪化开场白
    st.session_state.messages = [{"role": "assistant", "content": "您好！我是影心 Cinemind 品牌旗舰店的星级导购，很高兴为您服务。请问有什么可以帮您的？"}]

# 遍历并绘制所有历史对话气泡
for msg in st.session_state.messages:
    # 根据 role (user/assistant) 自动选择头像与气泡方向
    with st.chat_message(msg["role"]):
        # 渲染 Markdown 格式的消息内容
        st.markdown(msg["content"])

# 6. 用户交互处理逻辑
# st.chat_input 负责接收底层用户的终端输入
if prompt := st.chat_input("您可以询问关于产品详情、库存或售后政策..."):
    # 在用户按下回车后，立即在当前视窗绘制提问气泡
    with st.chat_message("user"):
        st.markdown(prompt)
    # 将问题同步追加到历史列表
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 发起 AI 推理（先过限速检查）
    with st.chat_message("assistant"):
        # 限速拦截：超过每分钟阈值时直接返回提示，不发起 LLM 调用
        if not _check_rate_limit():
            rate_msg = f"⏳ 您的请求过于频繁，每分钟最多 {_MAX_REQUESTS_PER_MINUTE} 次。请稍候片刻再试。"
            st.warning(rate_msg)
            st.session_state.messages.append({"role": "assistant", "content": rate_msg})
            logger.warning(f"Rate limit triggered | SID: {st.session_state.session_id}")
        else:
            # 展示流式加载动画，增强用户体验
            with st.spinner("正在查阅内部库存文档与品牌白皮书..."):
                try:
                    # 记录推理开始时间点
                    start_time = time.time()
                    # 获取单例 RAG 引擎
                    engine = get_rag_engine()
                    # 传入问题与 ID，静待引擎回音
                    response_text = engine.execute(prompt, st.session_state.session_id)

                    # 计算总共消耗的秒数
                    cost_time = time.time() - start_time
                    # 拼接耗时信息（置灰显示，提升专业感）
                    final_output = f"{response_text}\n\n---\n*⏱️ 核心引擎检索与生成共耗时: {cost_time:.2f}s*"

                    # 在 UI 上展示最终渲染的结果
                    st.markdown(final_output)
                    # 将回答内容同步追加到历史列表
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    # 记录审计日志：完成一次闭环交互
                    logger.info(f"Interaction Cycle Complete | SID: {st.session_state.session_id} | Payload: {len(response_text)} chars")
                except Exception as e:
                    # 记录原始技术报错到日志系统，供开发人员调试（脱敏前内容）
                    logger.error(f"ENGINE CRITICAL ERROR | SID: {st.session_state.session_id} | Detail: {str(e)}")
                    
                    # 向终端用户展示友好的提示信息（脱敏后内容）
                    # 避免展示 SSLError 或 API 域名等可能暴露后端架构或让用户产生恐惧感的信息
                    friendly_error = "❌ 抱歉，当前导购系统业务繁忙，请稍微休息一下再试。"
                    st.error(friendly_error)
                    
                    # 将反馈同步追加到会话历史，保持对话流连贯
                    st.session_state.messages.append({"role": "assistant", "content": friendly_error})
