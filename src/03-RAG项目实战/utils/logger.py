"""
 Cinemind 03-RAG 实战项目 - 彩色日志记录器 (Colorized Standardized Logger)
 
 遵循项目开发规范：中文 Docstring + 类型提示 + ANSI 彩色格式化。
"""

import logging  # 导入 Python 原生 logging 库用于日志管理

# --- ANSI 颜色转义码定义 ---
# 理由：直接使用转义码可避免引入 colorlog 等第三方库，保持项目极度轻量
GREY = "\x1b[38;20m"       # 调试信息 - 灰色
GREEN = "\x1b[32;20m"      # 正常信息 - 绿色
YELLOW = "\x1b[33;20m"     # 警告信息 - 黄色
RED = "\x1b[31;20m"        # 错误信息 - 红色
BOLD_RED = "\x1b[31;1m"    # 致命错误 - 红色加粗
RESET = "\x1b[0m"          # 重置颜色

class ColorFormatter(logging.Formatter):
    """
    自定义彩色格式化器，根据日志级别动态切换终端文字颜色。
    """
    
    # 建立日志级别与颜色的映射关系
    FORMATS = {
        logging.DEBUG: GREY + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.INFO: GREEN + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.WARNING: YELLOW + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.ERROR: RED + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.CRITICAL: BOLD_RED + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
    }

    def format(self, record):
        """
        重写 format 方法，在每一行日志输出前拦截并注入颜色代码。
        """
        # 根据当前日志级别获取对应的颜色模板
        log_fmt = self.FORMATS.get(record.levelno)
        # 实例化一个临时的基础格式化器执行最终渲染
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def get_sys_logger(module_name: str) -> logging.Logger:
    """
    获取全局统一的彩色系统日志记录器。
    
    采用标准化的色彩分级与 Emoji 标识，极大提升复杂链路下的排错效率。
    
    Args:
        module_name: 模块标识符，建议传入 __name__。
        
    Returns:
        配置完成的彩色 Logger 实例。
    """
    # 实例化一个指定名称的日志对象
    logger: logging.Logger = logging.getLogger(module_name)
    
    # 如果该记录器尚未挂载处理器（防止在 Streamlit 多次重刷时出现重复输出）
    if not logger.handlers:
        # 创建一个标准的终端串行流处理器 (StreamHandler)
        handler: logging.StreamHandler = logging.StreamHandler()
        
        # 注入自定义的彩色格式化逻辑
        handler.setFormatter(ColorFormatter())
        
        # 将处理器添加到记录器队列
        logger.addHandler(handler)
        
    # 设置系统默认日志级别为 INFO，屏蔽海量库底层的杂讯
    logger.setLevel(logging.INFO)
    
    # 防止日志消息向上传递至 root 记录器，导致控制台重复打印（Streamlit 特性需求）
    logger.propagate = False
    
    # 返回配置完成的记录器
    return logger
