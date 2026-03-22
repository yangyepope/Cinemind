# ✨ 影心 Cinemind · 离线私属 RAG 企业级架构引擎

本项目彻底摆脱了实验级的扁平脚本结构，是一个基于 LangChain LCEL 倒排检索、Streamlit 多页面原生核心路由、Chroma 纯本地高维库，并严格遵守高内聚低耦合企业级规范的**现代化 RAG 独立底座**。

---

## 🚀 进阶级工程全景目录 (Enterprise Architecture)

```text
src/03-RAG项目实战/
├── .env.example             # 环境鉴权变量配置脱敏模板
├── .gitignore               # Git 提交流程隔离忽略清单
├── README.md                # ⚓ 项目架构大黄皮书（本文件）
├── pyproject.toml           # 📦 UV 现代化原生项目依赖中枢 (替代 requirements)
├── uv.lock                  # 🔒 UV 次世代依赖环境防暴走锁表
├── app.py                   # 🎈 Streamlit 主界路由 (承载带耗时探头的 C 端对话瀑布流)
├── pages/                   # Streamlit 原生多页跨域路由系统
│   └── 1_📚_知识库录入平台.py  # 内部高权限物理隔离的防重后台页
├── config/                  # ⚙️ 全局配置层
│   ├── __init__.py 
│   └── settings.py          # 持久化绝对路径计算探针、大模型标号统一定义
├── core/                    # 🧠 核心重算力层 (LCEL 大电闸单例池)
│   ├── __init__.py
│   ├── history_manager.py   # 纯长记忆流式 I/O 抽象防腐管理
│   ├── rag_chain.py         # Retriever + Prompt + LLM 的链式核心外包集成引擎
│   └── vector_store.py      # Chroma 原生倒排库配置中心与独立连通器
├── services/                # 🛠️ 繁重业务微服务下沉层
│   ├── __init__.py
│   └── kb_service.py        # CPU 耗时文本切片、MD5 指纹比对去重的防爆破脏写独立单元
├── utils/                   # 🔧 杂项通用生态护城河
│   ├── __init__.py
│   └── logger.py            # 扼杀野生 print，输出格式标准化 Logging 的控制台拦截器
├── data/                    # 📄 数据与指纹物料实体落舱区
│   ├── source_docs/         # 存放用户拖拽上来的纯金 .txt
│   └── md5_cache.text       # 独立剥离的全局去重指纹物理校验池，硬核防刷
└── database/                # 💾 底层轻应用数据库体量区
    ├── chroma_db/           # Chroma 原生 SQLite 向量高维空间驻留目录
    └── sessions/            # 用户 BaseChatMessageHistory 会话列阵的静态流浪舱
```

### 💡 核心改造与降维打击理念
1. **模块与高耗算力隔离 (Decoupling)**：不再将所有的 LCEL 核心链、文件记忆提取混在一起。`core` 和 `services` 各行其道，强制引入类单例化引擎池，完美压制前端极速重绘刷新带来的 Chroma 长连接重载耗时和 OOM 内存泄露危险。
2. **多页原生跨域 (Multi-Page)**：通过 `app.py`（C 端门店展示）和 `pages/`（B 端暗网后台库管）切割物理边界，完美合成并展现了一个带有玻璃态 UI 的一体化大型生态体验网。
3. **安全自举探针系统 (DevOps)**：无论根项目被拷贝后发生什么盘符偏移甚至服务器迁移，系统在首轮通电开机时，都能利用 `settings.py` 内极客级的 `os.path` 绝对坐标自举探针侦察定位，并抢着挂载修筑所有缺失的库缓存必须通道（防爆错自启逻辑）！

---

## 🏗️ 深度架构解剖 (Architectural Deep Dive)

### 1. 顶层分发网关 (Multi-Page App)
- `app.py`: **C端核心母港**。彻底被抽取剥离了肮脏的嵌段与切分逻辑！现在它是一片极纯粹的视觉渲染区，维护着带有动态光影渲染的旗舰交互瀑布流（以及内置毫秒级链式算力探头）。
- `pages/1_📚_知识库录入平台.py`: **B端隔离后台**。在 Streamlit 侧栏动态生成了无缝切换路由；管理员在此处的玻璃态监控面板上，直接全盘掌控 Chroma 物理集群体积，并下达防重验证的数据切分入库军令状。

### 2. 算力隔离群落 (Core)
- `core/rag_chain.py`: **LCEL 终极心脏**。抛弃粗糙的函数，采用 `RagPipelineEngine` 单例体防腐层封装；确保用户网页哪怕在一秒内疯狂被刷新重绘，其底层的 LLM 通信池和向量长连接也永远只会被实例化单例一次，彻底击毙多重启动造成的系统死锁！
- `core/vector_store.py`: **倒排索引网关**。所有关于 Chroma 和 Embedding 大模型（如 DashScope）的调度和参数调整均收敛于此闭环内。
- `core/history_manager.py`: **流浪地球记忆工厂**。将极客般的 `BaseChatMessageHistory` 文件写入逻辑进行了高度提纯抽象。

### 3. 防弹衣堡垒 (Services)
- `services/kb_service.py`: 将最繁杂丑陋“向量倒排化前处理”全数关进了隔离区。包含了 `get_str_digest` -> `exists_in_cache` 的全周期 MD5 防重系统链，为知识库上了一层坚不可摧的指纹防暴盾。

### 4. 万物底座与 DevOps 基建
- `config/settings.py` 绝对护航：所有长驻变量统一下沉配置。无论您以后将该项目扔至哪个驱动器运行，它在启动初始化时都能利用 `os.path` 探针完美探出自己的绝对坐标轴，并在首轮自举内，霸道地扫雷为您全自动强行建仓修筑起 `database/sessions/` 和 `database/chroma_db/` 目录群！
- `utils/logger.py`: 配置了标准化带 Emoji 角标的 `StreamHandler`，整顿了满天飞的野生 `print` 控制台污染！

---

## 🛠️ 基于 UV 的次世代极速跑通指北

本项目彻底扫清并抛弃了臃肿缓慢的古典 `pip` 依赖堆叠体系与 `requirements.txt` 手工管理，全量接轨基于 Rust 打造、微秒级并行的次世代包管理器 **`uv`**！

### 1. 引擎权限令牌密语装载 (Environment Setup)
参照项目护城河下发的 `.env.example` 标准复印并在本机挂出您的隐秘 `.env` 文件，随后填入对应大模型厂商的核心底座秘钥：
```bash
cp .env.example .env
# nano .env （在此处写入您的诸如 DASHSCOPE_API_KEY 的绝密金钥）
```

### 2. 依赖矩阵闪电重构 (UV Native Dependencies Sync)
忘掉古典的手写管理模式！所有的核心大盘依赖库早已硬核内联统一定义于 `pyproject.toml` 以及绝对固化的 `uv.lock` 中。
系统重装仅需一行极简的敲击，`uv` 巨无霸引擎将在数十毫秒内为您极速拉取并严格建立物理隔离的极净环境容器：
```bash
uv sync
```

### 3. 主路由超维大电闸通电 (Release the RAG Engine)
在基于强锁定的虚拟环境结界内，安全无损挂载并执行引擎路由：
```bash
uv run streamlit run app.py
```
*(系统完全启动后，左侧导购大门和右向的密库录入后台将在局域网 `:8501` 为您敞开，尽情体验毫秒级问答跟踪反馈特效吧！)*
