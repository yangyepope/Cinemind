"""
示例：使用 TextLoader 加载文档并应用 RecursiveCharacterTextSplitter 进行智能分段。
基于 Cinemind 项目规范和 LangChain 最佳实践。
"""

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_document_splitting_example() -> None:
    """
    运行文档分段示例逻辑。
    """
    # 1. 定义文件路径 (使用 pathlib)
    # 输入文件路径：src/02-LangChainRAG开发/data/python文档分段.txt
    current_dir = Path(__file__).parent
    file_path = current_dir / "data" / "python文档分段.txt"
    
    if not file_path.exists():
        print(f"❌ 错误：找不到输入文件 {file_path}")
        return

    # 2. 加载文档
    # 使用 TextLoader 记载纯文本文件，指定编码为 utf-8
    print(f"正在加载文档: {file_path.name}...")
    loader = TextLoader(str(file_path), encoding="utf-8")
    docs = loader.load() # 返回 [Document] 列表
    
    # 3. 初始化分段器 (RecursiveCharacterTextSplitter)
    # 根据用户提供的图片参数进行配置
    print("正在初始化 RecursiveCharacterTextSplitter...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # 分段的最大字符数
        chunk_overlap=50,      # 分段之间允许重叠字符数
        # 文本自然段落分隔的依据符号 (包含常见的中英文标点)
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        length_function=len    # 统计字符的依据函数
    )
    
    # 4. 执行分段
    print("开始对文档进行分段处理...")
    split_docs = splitter.split_documents(docs)
    
    # 5. 输出结果概览
    print("-" * 30)
    print("✅ 处理完成！")
    print(f"原始文档数量: {len(docs)}")
    print(f"分段后的文档数量: {len(split_docs)}")
    print("-" * 30)
    
    # 打印前 3 个分段的内容片段
    for i, doc in enumerate(split_docs[:3]):
        content_preview = doc.page_content.replace("\n", " ")[:1000]
        print(f"分段 {i+1} (长度 {len(doc.page_content)}): {content_preview}...")

if __name__ == "__main__":
    run_document_splitting_example()
