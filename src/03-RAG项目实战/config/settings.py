"""
 Cinemind 03-RAG 实战项目 - 全局配置中心 (Configuration Center)
 
 本模块负责定义项目全路径拓扑、模型引擎参数以及底层文件夹的自动化预埋。
 遵循 Cinemind 项目开发规范：强制使用 pathlib 处理路径。
"""

# 导入所需的库
from pathlib import Path  # 导入 pathlib 库用于处理跨平台文件路径
from dotenv import load_dotenv  # 导入 dotenv 用于加载环境变量 (.env 文件)
import os  # 导入 os 库用于访问系统环境变量

# 初始化环境：从当前执行目录或父目录查找 .env 文件并加载
load_dotenv()

# --- 核心路径自举逻辑 ---

# 定义项目根目录：(__file__) 是当前文件 settings.py 所在位置，.parent.parent 指向 src/03-RAG项目实战/
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# 定义持久化存储目录：用于存放所有的动态数据
DATA_DIR: Path = BASE_DIR / "database"

# 定义向量数据库存储路径：Chroma 所有的索引文件将落地于此
CHROMA_DB_DIR: Path = DATA_DIR / "chroma_db"

# 定义会话历史序列化路径：存放用户的聊天记录 JSON 文件
SESSION_HISTORY_DIR: Path = DATA_DIR / "sessions"

# 定义文件指纹缓存路径：用于 MD5 去重，防止同一个知识点被重复喂入
MD5_CACHE_PATH: Path = DATA_DIR / "md5_cache.text"

# 定义原始文档存储路径：存放用户上传的原始文档，等待处理
SOURCE_DOCS_DIR: Path = BASE_DIR / "data" / "source_docs"

# 执行自举：如果 database 等关键目录不存在，则递归创建它们
# 遍历所有需要确保存在的目录
for _path in [CHROMA_DB_DIR, SESSION_HISTORY_DIR, SOURCE_DOCS_DIR]:
    # 确保父目录存在，不存在则自动创建 (exist_ok=True 避免重复创建报错)
    _path.mkdir(parents=True, exist_ok=True)

# 如果指纹缓存文件不存在，则初始化一个空文件以免读取时报错
if not MD5_CACHE_PATH.exists():
    # 使用 touch 命令创建一个空文件
    MD5_CACHE_PATH.touch()

# --- 业务算法配置参数 ---

# 定义 RAG 检索时的 Top-K 值：每次提问从知识库提取最相关的 3 段背景
TOP_K_RETRIEVAL: int = 3

# 定义嵌入大模型标号：用于将文本转换为向量，从环境变量中获取，若无则使用默认值
EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-v2")

# 定义核心推理大模型标号：用于生成回答，从环境变量中获取，若无则使用默认值
LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "qwen-turbo")

# 定义系统提示词版本或标识（可选，当前保留默认配置路径）
# 所有的业务级配置建议在此处收口，避免在业务代码中硬编码语义。

# 定义文档切分块大小：每个向量化单元的最大字符数
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))

# 定义相邻块重叠字符数：保证切分处的语义连续性
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

# 定义内存中最大会话缓存数量：超出后自动淘汰最久未访问的会话（LRU策略）
SESSION_CACHE_LIMIT: int = int(os.getenv("SESSION_CACHE_LIMIT", "500"))

# --- 环境自举维护系统 ---

def _enforce_environment() -> None:
    """
    自动化执行底层数据仓储目录的扫描与建仓，防御文件读写越界。
    保证项目在首次运行或迁移后能自动补全物理目录结构。
    """
    # 定义所有必须存在的物理目录路径列表
    _folders: list[Path] = [CHROMA_DB_DIR, SESSION_HISTORY_DIR, SOURCE_DOCS_DIR]
    # 遍历列表，逐一检查并创建
    for _folder in _folders:
        # parents=True 表示递归创建父目录，exist_ok=True 表示目录存在时不报错
        _folder.mkdir(parents=True, exist_ok=True)

# 执行自举（首次运行即建仓，且仅调用一次）
_enforce_environment()
