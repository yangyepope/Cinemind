---
name: streamlit_rag_stability
description: 解决 Streamlit 环境下 RAG 推理链的异步稳定性与事件循环冲突问题。
---

# Streamlit RAG 稳定性增强技能

本技能旨在解决 RAG 应用在 Streamlit 多页架构中常见的 `RuntimeError: Event loop is closed` 以及资源重复加载导致的内存溢出问题。

## 1. 异步冲突补丁 (Asyncio Patch)

### 现象
Streamlit 的脚本重运行机制会频繁开关主线程的事件循环。如果底层库（如 `chromadb` 或 `langchain-chroma`）缓存了旧的 Loop 引用，在下一次请求时会因 Loop 已关闭而崩溃。

### 解决方案
在初始化任何包含异步 I/O 的 Resource 之前，必须执行以下“自愈逻辑”：

```python
import asyncio

def ensure_valid_loop():
    """确保当前环境具备可用的事件循环容器。"""
    try:
        # 尝试检测运行中的 Loop
        asyncio.get_running_loop()
    except RuntimeError:
        # 如果当前线程无运行中的 Loop，强制新建并注入上下文
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
```

## 2. 资源单例化 (Resource Singleton)

### 准则
大模型实例 (`llm`)、向量库连接 (`vector_store`) 以及 RAG 完整链条 (`RagPipelineEngine`) **绝对禁止**在全局直接实例化或在 `app.py` 顶层直接创建。

### 正确模式
统一使用 `st.cache_resource` 进行单例包装：

```python
import streamlit as st

@st.cache_resource
def load_rag_engine():
    # 执行补丁
    ensure_valid_loop()
    # 执行昂贵的初始化
    return RagPipelineEngine()

# 在 UI 处按需获取
engine = load_rag_engine()
```

## 3. 跨页路径修复 (Path Resolution)

### 准则
在 Streamlit 的 `pages/` 目录下，由于执行上下文变化，常会出现无法导入父级包的情况。

### 推荐模板
在 Page 的文件最顶层（Import 之前）注入以下代码：

```python
from pathlib import Path
import sys

# 动态反查项目根目录
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# 注意：后续的内部导入必须添加 # noqa: E402 以绕过 Ruff/Flake8 的顶层导入检查
from my_module import my_func  # noqa: E402
```

### 为什么需要 `# noqa: E402`？
Ruff 默认要求所有 `import` 语句位于文件顶部。但在 Streamlit 页面中，如果子视图需要引用根目录的包，必须先动态修改 `sys.path`，这会导致后续的 `import` 被判定为违规。使用 `# noqa: E402` 可以在保证运行成功的前提下消除警告。

## 4. 验证指标
- [ ] 连续点击 Rerun 5 次不报错。
- [ ] 切换多页面后再返回对话页，历史记忆保持正常。
- [ ] 内存曲线在文件上传后保持平稳平稳，无阶梯状上升。
