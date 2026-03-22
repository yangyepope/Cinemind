"""
 Cinemind 03-RAG 实战项目 - 知识库录入平台 (KB Management Page)
 
 本模块作为 B 端后台隔离区，负责非结构化语料的指纹审计、自动化切片及向量化挂载。
"""

# 导入系统与文件处理库
from pathlib import Path  # 处理物理路径
import sys  # 用于动态路径修复

# 导入 Streamlit Web 框架
import streamlit as st

# --- 1. 模块搜索路径自愈逻辑 ---
# 理由：Streamlit 在多级目录运行 Page 时有时会丢失对上一级包的识别
# 获取当前文件的父目录的父目录，即项目根目录 src/03-RAG项目实战/
_current_path = Path(__file__).resolve()
_project_root = _current_path.parent.parent
# 强制将根目录推入 sys.path 的最前端，确保 services/config 等内部包引用绝对稳健
if str(_project_root) not in sys.path:
    # 使用 insert(0, ...) 赋予最高搜索优先级
    sys.path.insert(0, str(_project_root))

# --- 2. 核心业务与配置导入 ---
# 注意：这些导入必须发生在 sys.path 修复之后
from services.kb_service import EnterpriseKBService  # noqa: E402 # 导入知识库同步核心
from config.settings import MD5_CACHE_PATH, CHROMA_DB_DIR  # noqa: E402 # 导入文件指纹池与向量库物理路径

# --- 3. 页面全局配置 ---
# 设置网页标签页显示名称、Emoji 图标及布局
st.set_page_config(
    page_title="影心 Cinemind - 知识库管理",
    page_icon="📚",
    layout="centered"
)

# --- 4. 业务组件单例化 ---

# 使用 st.cache_resource 确保知识库服务在应用生命周期内只有一个物理连接
@st.cache_resource
def get_kb_service() -> EnterpriseKBService:
    """
    单例工厂：获取企业知识库加工服务。
    """
    # 实例化知识库同步核心
    return EnterpriseKBService()

# --- 5. 主界面布局渲染 ---

# 显示页面头图或标题
st.title("📚 影心知识库 - 自动化录入")
# 展示系统定位
st.markdown("#### B 端专属：非结构化语料的数字指纹审计与向量挂载系统")
st.markdown("---")

# 6. 核心数据资产总览 (Metrics)
# 在侧边栏创建监控面板
with st.sidebar:
    st.header("📊 硬件级监控面板")
    
    # 指标 A：统计指纹库容量
    # 使用 Pathlib 读取 MD5 缓存文件的行数，代表已录入的文档指纹数
    file_count: int = 0
    if MD5_CACHE_PATH.exists():
        # 按行切分并计数
        file_count = len(MD5_CACHE_PATH.read_text(encoding="utf-8").splitlines())
    
    # 指标 B：统计向量库物理占用
    # 递归遍历 Chroma 目录下的所有文件并累加 stat().st_size
    db_size_mb: float = 0.0
    if CHROMA_DB_DIR.exists():
        # rglob('*') 递归搜索所有二进制分块文件
        db_size_mb = sum(f.stat().st_size for f in CHROMA_DB_DIR.rglob('*') if f.is_file()) / (1024 * 1024)
    
    # 创建布局列
    m_col1, m_col2 = st.columns(2)
    # 渲染 Metrics
    m_col1.metric("已录入指纹", f"{file_count} 段")
    m_col2.metric("库体体积", f"{db_size_mb:.2f} MB")
    
    # 品牌提示
    st.divider()
    st.info("💡 核心提示：底层的 MD5 算法系统会自动在内存与磁盘双重阻断任何重复投喂行为。")

# 7. 文档上传交互主逻辑
st.write("### 📤 原材料投递区")
# file_uploader 提供拖拽上传能力
uploaded_file = st.file_uploader(
    "请上传 PDF 或 TXT 格式的产品手册/业务文档", 
    type=["txt", "pdf"],
    help="本系统将自动执行文本提取 -> 语义分片 -> 向量化，并永久封存在本地数据中心。"
)

# 响应上传事件
if uploaded_file is not None:
    # 获取被选中的文件名
    file_name = uploaded_file.name
    # 初始化内容占位符
    file_content = ""
    
    # 开启状态指示器（Spinner 的升级版，支持多步状态流）
    with st.status(f"正在将 [{file_name}] 同步至高维知识空间...", expanded=True) as status:
        try:
            # 第一阶段：原始数据解压与读取
            st.write("1. 正在解析原始字符流...")
            # 简化逻辑：此处统一按 UTF-8 读取（实际生产环境建议根据后端编码自适应）
            file_content = uploaded_file.read().decode("utf-8")
            
            # 第二阶段：调用单例服务执行向量化同步
            st.write("2. 正在执行 MD5 指纹审计与高维向量注入...")
            # 获取后台服务实例
            kb_service = get_kb_service()
            # 发起同步请求
            success, message = kb_service.sync_to_kb(file_content, file_name)
            
            # 第三阶段：根据闭环结果反馈 UI
            if success:
                # 更新状态为成功，并自动收起面板
                status.update(label="✅ 文档同步成功！", state="complete", expanded=False)
                # 弹出成功通知
                st.success(message)
                # 燃放礼花增强交互快感
                st.balloons()
            else:
                # 指纹重复导致的查重失败，标红处理
                status.update(label="⚠️ 数据投喂已拦截", state="error", expanded=True)
                st.warning(message)
                
        except Exception as e:
            # 异常反馈逻辑：显示具体故障原因
            status.update(label="❌ 录入流水线发生阻塞故障", state="error")
            st.error(f"故障诊断详情: {str(e)}")
