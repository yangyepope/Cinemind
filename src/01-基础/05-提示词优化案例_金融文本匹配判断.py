import os
from openai import OpenAI

# 获取client对象，OpenAI类对象
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    # base_url="http://localhost:11434/v1"
)

examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财报披露，公司ITCAST更赚钱了。")
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。")
    ]
}

questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势愈加明显。"),
    ("股票市场今日大涨，投资者乐观。", "持续上涨的市场让投资者感到满意。")
]

messages = [
    {"role": "system", "content": "你帮我完成文本匹配，我给你2个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考如下示例："}
]

for label, pairs in examples_data.items():
    for pair in pairs:
        messages.append({"role": "user", "content": f"句子1：[{pair[0]}]句子2：[{pair[1]}]"})
        messages.append({"role": "assistant", "content": label})

# 向模型提问
for q in questions:
    current_messages = messages + [
        {"role": "user", "content": f"按照上述示例，回答这2个句子的情况。句子1：[{q[0]}]，句子2：[{q[1]}]"}
    ]
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=current_messages
    )

    print(f"句子1：[{q[0]}]\n句子2：[{q[1]}]\n判断结果：{response.choices[0].message.content}\n")
