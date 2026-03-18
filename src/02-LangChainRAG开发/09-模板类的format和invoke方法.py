import sys
from langchain_core.prompts import PromptTemplate

# 确保在 Windows 终端能正确输出 UTF-8 字符
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

"""
继承关系说明：
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
"""

# 定义模板
template = PromptTemplate.from_template("我的邻居姓{lastname}, 爱好的运动是{hobby}")

print("--- 1. 使用 format 方法 ---")
# format 方法进行纯字符串替换，解析占位符生成提示词
res = template.format(lastname="张大明", hobby="足球")
print(f"输出结果: {res}")
print(f"返回类型: {type(res)}")

print("\n--- 2. 使用 invoke 方法 ---")
# invoke 方法是 Runnable 接口的标准方法，解析占位符生成提示词，但返回的是 PromptValue 类对象
res2 = template.invoke({"lastname": "周杰伦", "hobby": "篮球"})
print(f"输出结果: {res2}")
print(f"返回类型: {type(res2)}")

print("\n--- 3. 两种方法的区别总结 ---")
print("1. 功能: format 是纯字符替换; invoke 是标准 Runnable 接口。")
print("2. 返回值: format 返回字符串; invoke 返回 PromptValue 类对象。")
print("3. 传参: format 接受 key=value; invoke 接受 字典对象。")

print("\n--- 验证结束 ---")
