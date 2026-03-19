from langchain_community.document_loaders import JSONLoader
from pathlib import Path
import json

# 1. 定义文件路径
# __file__ 是当前脚本的路径，.parent 获取当前脚本所在的文件夹
# 然后拼接 data 文件夹路径
data_dir = Path(__file__).parent / "data"


def demo_stus_array():
    """
    演示加载 JSON 数组文件 (stus.json)
    """
    print("--- 1. 加载 JSON 数组 (stus.json) ---")
    file_path = data_dir / "stus.json"

    # jq_schema=".[]" 表示遍历数组中的每一个元素（对象）
    # 每个元素都会被加载为一个 LangChain Document
    loader = JSONLoader(
        file_path=str(file_path),
        jq_schema=".[]",
        text_content=False,  # 如果为 False，则整个对象会作为 page_content
    )

    docs = loader.load()
    for doc in docs:
        print(f"内容: {doc.page_content}")
        print(f"元数据: {doc.metadata}")
    print(f"加载成功，共 {len(docs)} 个文档\n")


def demo_stu_single():
    """
    演示加载单个嵌套的 JSON 对象 (stu.json)
    """
    print("--- 2. 加载单个嵌套 JSON 对象 (stu.json) ---")
    file_path = data_dir / "stu.json"

    # jq_schema="." 表示加载整个根对象
    loader = JSONLoader(file_path=str(file_path), jq_schema=".", text_content=False)

    docs = loader.load()
    for doc in docs:
        print(f"内容: {doc.page_content}")
        print(f"元数据: {doc.metadata}")
    print(f"加载成功，共 {len(docs)} 个文档\n")


def demo_stu_json_lines():
    """
    演示加载 JSON Lines 文件 (stu_json_lines.json)
    每一行都是一个独立的 JSON 对象
    """
    print("--- 3. 加载 JSON Lines 文件 (stu_json_lines.json) ---")
    file_path = data_dir / "stu_json_lines.json"

    # json_lines=True 必须设置为 True 以解析此类格式
    loader = JSONLoader(
        file_path=str(file_path), jq_schema=".name", json_lines=True, text_content=False
    )

    docs = loader.load()
    for doc in docs:
        print(f"内容: {doc.page_content}")
        print(f"元数据: {doc.metadata}")
    print(f"加载成功，共 {len(docs)} 个文档\n")


if __name__ == "__main__":
    # 注意：运行此脚本需要安装 jq 库 (pip install jq)
    # Windows 环境下可能需要额外的 jq 运行环境支持
    try:
        demo_stus_array()
        demo_stu_single()
        demo_stu_json_lines()
    except Exception as e:
        print(f"运行演示出错: {e}")
        print("提示: JSONLoader 依赖 jq 库，请确保已执行 pip install jq")
