import sys
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 确保在 Windows 终端能正确输出 UTF-8 字符（如 Emoji）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 定义提示词模板
# 使用 {variable} 定义占位符
template = "我的邻居姓{lastname}, 刚生了{gender}, 你帮我起个名字, 简单回答。"

# 2. 从字符串模板中创建 PromptTemplate 对象
prompt_template = PromptTemplate.from_template(template)

print("--- 1. 模板的基本属性 ---")
print(f"输入变量: {prompt_template.input_variables}")
print(f"模板内容: {prompt_template.template}")

print("\n--- 2. 格式化模板 (生成最终提示词) ---")
# 使用 .format() 方法填充变量
prompt_text = prompt_template.format(lastname="张", gender="女儿")
print(f"格式化结果: {prompt_text}")

print("\n--- 3. 结合大模型进行调用 (LCEL 链式语法) ---")
# 初始化通义千问大模型
# 确保已设置 DASHSCOPE_API_KEY 环境变量
model = Tongyi(model="qwen-max")

# 使用 | 符号将提示词模板和模型连接起来，形成一个简单的 Chain
chain = prompt_template | model

# 调用整个链条
# 输入为一个字典，key 对应模板中的变量名
res = chain.invoke(input={"lastname": "王", "gender": "儿子"})

print("问题: 王家生了儿子，起什么名字？")
print(f"回答: {res}")

print("\n--- 验证结束 ---")
