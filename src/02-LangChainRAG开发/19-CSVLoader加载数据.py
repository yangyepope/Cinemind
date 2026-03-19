"""
本模块演示如何使用 LangChain 的 CSVLoader 从 CSV 文件加载数据。
包含批量加载和懒加载（分行加载）的示例。
"""

from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from typing import Iterator
from pathlib import Path


def main() -> None:
    """
    执行 CSV 加载演示的主函数。
    """
    # 路径处理：使用 pathlib 获取当前脚本目录下的 data/stu.csv
    # 遵循项目规则，使用 pathlib 进行路径拼接
    current_dir = Path(__file__).parent
    data_file_path = current_dir / "data" / "stu.csv"

    # 初始化 CSVLoader
    # file_path: CSV 文件路径
    # csv_args: 传递给 Python csv 模块的参数
    # encoding: 文件编码
    loader = CSVLoader(
        file_path=str(data_file_path),
        csv_args={
            "delimiter": ",",        # 指定分隔符
            "quotechar": '"',        # 指定带有分隔符文本的引号包围字符
            # 如果数据原本有表头，就不用下面的代码，如果没有可以使用 fieldnames 指定
            # "fieldnames": ['name', 'age', 'gender', 'hobby']
        },
        encoding="utf-8"           # 指定编码为 UTF-8
    )

    # 1. 批量加载 .load() -> [Document, Document, ...]
    # 会一次性将所有数据加载到内存中
    # print("--- 批量加载示例 ---")
    # documents = loader.load()
    # for document in documents:
    #     print(f"类型: {type(document)}, 内容: {document}")

    # 2. 懒加载 .lazy_load() -> Iterator[Document]
    # 逐行加载，适用于处理大文件，节省内存
    print("--- 懒加载示例 ---")
    doc_iterator: Iterator[Document] = loader.lazy_load()
    for document in doc_iterator:
        print(document)


if __name__ == "__main__":
    main()
