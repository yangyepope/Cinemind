"""
示例：使用 PyPDFLoader 加载普通及加密的 PDF 文档。
演示 mode="single" 与 lazy_load() 的高效配合。
"""

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def run_pypdf_loader_example() -> None:
    """
    运行 PDF 加载示例。
    """
    # 1. 定义数据路径 (使用 pathlib)
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"
    
    # 文件 A: 普通 PDF
    pdf1_path = data_dir / "pdf1.pdf"
    # 文件 B: 加密 PDF (密码: 123456)
    pdf2_path = data_dir / "pdf2.pdf"

    # --- 演示加载普通 PDF ---
    if pdf1_path.exists():
        print(f"--- 正在加载普通文档: {pdf1_path.name} ---")
        loader1 = PyPDFLoader(
            file_path=str(pdf1_path),
            mode="page"  # 默认按页切分，每个 Page 一个 Document
        )
        
        i = 0
        for doc in loader1.lazy_load():
            i += 1
            # 仅展示前 50 个字符以保持输出整洁
            content_preview = doc.page_content.replace("\n", " ")[:50]
            print(f"页面 {i}: {content_preview}...")
        
        print(f"✅ 普通文档加载完成，总页数: {i}\n")
    else:
        print(f"⚠️ 找不到文件: {pdf1_path}")

    # --- 演示加载加密 PDF ---
    if pdf2_path.exists():
        print(f"--- 正在尝试加载文件: {pdf2_path.name} ---")
        try:
            # 尝试使用密码加载
            loader2 = PyPDFLoader(
                file_path=str(pdf2_path),
                mode="single", # 默认按页切分，每个 Page 一个 Document，single 表示将整个 PDF 视为一个 Document
                password="123456" # PDF 的密码
            )
            for doc in loader2.lazy_load():
                print("✅ 使用密码 '123456' 成功解密并读取！")
                print(f"内容预览: {doc.page_content[:100]}...")
        except Exception as e:
            if "Not an encrypted file" in str(e):
                print("💡 发现：该文件实际上并没有加密。正在尝试直接加载...")
                loader_no_pass = PyPDFLoader(file_path=str(pdf2_path), mode="single")
                for doc in loader_no_pass.lazy_load():
                    print(f"✅ 直接加载成功！内容预览: {doc.page_content[:100]}...")
            else:
                print(f"❌ 加载失败: {e}")
        
        print("处理完成。")
    else:
        print(f"⚠️ 找不到文件: {pdf2_path}")

if __name__ == "__main__":
    run_pypdf_loader_example()
