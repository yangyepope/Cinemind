---
name: logging_excellence
description: 在终端输出中实现具备颜色级联与 Emoji 标识的企业级日志系统。
---

# 终端日志卓越性技能 (Logging Excellence)

本技能旨在通过色彩管理与视觉语义化，提升系统在调试与生产环境下的可观测性（Observability）。

## 1. 核心视觉原则

- **颜色分级**：
  - `DEBUG`: 灰色 (Gray) - 底层流转信息。
  - `INFO`: 绿色 (Green) - 正常业务逻辑启动或完成。
  - `WARNING`: 黄色 (Yellow) - 预期的异常或边界触发。
  - `ERROR`: 红色 (Red) - 严重故障或逻辑中断。
  - `CRITICAL`: 闪烁/背景红 (Bold Red) - 毁灭性系统崩溃。

- **Emoji 语义化**：
  - 启动阶段：🚀
  - 数据注入：📥
  - 逻辑计算：🧠
  - 成功完成：✅
  - 拦截阻断：🛡️
  - 报错信息：❌

## 2. 推荐实现模式 (无依赖版)

优先使用 ANSI 转义码实现彩色打印，确保项目的轻量化与环境兼容性。

```python
import logging

class ColorFormatter(logging.Formatter):
    """
    基于 ANSI 转义码的彩色日志格式化器。
    """
    # 定义 ANSI 颜色转义序列
    COLORS = {
        'DEBUG': "\033[38;20m",   # 灰色
        'INFO': "\033[32;20m",    # 绿色
        'WARNING': "\033[33;20m", # 黄色
        'ERROR': "\033[31;20m",   # 红色
        'CRITICAL': "\033[31;1m"  # 加粗红
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, self.RESET)}%(asctime)s - %(name)s - %(levelname)s - %(message)s{self.RESET}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
```

## 3. 验证准则
- [ ] 终端输出是否能够直观通过颜色区分级别。
- [ ] 日志行是否包含清晰的时间戳。
- [ ] 模块名称 (Name) 是否能精准定位到具体的 `.py` 文件。
