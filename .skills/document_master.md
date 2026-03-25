---
name: 详细文档撰写专家
description: 当由于此技能被触发时，将会强制 AI 在生成代码或配置文件时留下大量的注释，不仅详细解释每段代码用于何处，还要阐述其背后的原理和内部逻辑。所有注释必须使用中文。
---

# 详细文档撰写专家技能

当触发此技能时，你**必须**扮演一位极具耐心的编程导师。你的核心目的不应仅仅是能够把代码写出来跑通，而是要通过最透彻的手段将其解析清楚。

一旦你需要生成、编写、或者修改任何代码、脚本以及配置文件，你**必须强制遵循**以下规定：

1. **内联注释 (使用纯中文)**：
   - 为你写下的几乎每一个逻辑代码块、甚至是关键的行内逻辑，附加上详细的中文注释。
   - 重点解释*为什么*要选择这种处理方式，而不简单是复述*这段代码做了什么*。
   - 对于每一行 `import`，必须用行内注释说明引入该模块的用途。

2. **区块解析 (使用纯中文)**：
   - 在写下任何主要的函数、类定义或者复杂的一段逻辑之前，必须使用块注释或文档字符串（Docstring）描述出其总体的**核心目标**、**底层原理**以及**分步落地的具体逻辑**。

3. **API Key 与环境变量注释**：
   - 凡涉及 API Key、Token、Secret 等敏感信息的代码行，必须注释说明：
     - 该 Key 的来源平台（如阿里云百炼、OpenAI 等）
     - 推荐的安全获取方式（优先环境变量，并给出设置命令示例）
     - 不要将真实 Key 硬编码在代码中的警告提示

4. **模型调用注释**：
   - 在调用大语言模型 API 时，必须注释说明所用模型的名称含义、适用场景、计费特点（如有）。
   - 对 `stream`、`temperature`、`max_tokens` 等关键参数，必须逐一注释其作用和取值影响。
   - 对流式输出的循环处理逻辑，必须注释每一步的数据结构含义。

5. **配置文件解析 (使用纯中文)**：
   - 当遇到系统配置文件生成工作（比如 JSON, YAML, TOML, CFG 格式）时，利用其能够支持的注释格式（如 `#`），去说明配置文件中每一个键（Key）的含义、为何在这里需要定义这个值、以及这个值会实际产生的系统影响。

6. **表达的清晰度与完备性**：
   - 永远不要假设阅读代码的人能够心领神会任何隐含的背景知识。
   - 必须使用专业、清楚、易懂的中文语言对各项实现细节进行毫无保留地拆解说明。

**预期的输出效果示例（以阿里云 DashScope 调用为例）：**
```python
import os                  # 用于读取系统环境变量，避免将敏感信息硬编码在代码中
from openai import OpenAI  # 阿里云 DashScope 兼容 OpenAI 接口，可直接复用此客户端库

# -------------------------------------------------------
# 初始化 DashScope 客户端
# 安全说明：API Key 优先从环境变量读取，防止密钥泄露到代码仓库
# 设置环境变量方法（PowerShell）：$env:DASHSCOPE_API_KEY = "sk-你的key"
# 获取 Key 地址：https://bailian.console.aliyun.com/
# -------------------------------------------------------
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY", "sk-占位符，请替换为真实Key"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # DashScope 的 OpenAI 兼容端点
)

def chat_with_stream():
    """
    核心目标：以流式方式调用通义千问模型，实现逐字输出效果
    底层原理：stream=True 时，服务端将响应拆分为多个 chunk 依次推送，
              客户端按序拼接打印，视觉上产生"打字机"效果，减少首字延迟
    分步逻辑：
      1. 构造包含 system 和 user 角色的 messages 列表
      2. 发起流式请求，获取迭代器对象 response
      3. 遍历每个 chunk，提取 delta.content 并实时打印
    """
    response = client.chat.completions.create(
        model="qwen-turbo",  # 通义千问 Turbo：响应快、成本低，适合高频对话场景
        messages=[...],
        stream=True,         # 开启流式：模型边生成边推送，避免等待完整响应
        temperature=0.7,     # 温度系数：0=确定性输出，1=最具创意，0.7 为均衡推荐值
    )
    for chunk in response:   # 每个 chunk 是一个增量数据包
        # chunk.choices[0].delta.content：本次增量的文字片段，流结束时为 None
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## 7. Markdown 文档中的可视化表格规范

当需要在任何 `.md` 文档中呈现结构化数据（如技术栈对照、参数说明、配置清单等），**必须**优先使用 HTML `<table>` 代替纯 Markdown 表格语法，以确保在所有查看器中都能渲染为带边框的直观表格。

**标准朴素风格模板**：

```html
<table style="border-collapse: collapse; width: 100%;">
  <thead>
    <tr>
      <th style="border: 1px solid #d0d0d0; padding: 6px 12px; background-color: #f0f0f0; text-align: left;">列名一</th>
      <th style="border: 1px solid #d0d0d0; padding: 6px 12px; background-color: #f0f0f0; text-align: left;">列名二</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #d0d0d0; padding: 6px 12px;">数据行</td>
      <td style="border: 1px solid #d0d0d0; padding: 6px 12px;">数据内容</td>
    </tr>
  </tbody>
</table>
```

**规范要点**：
- 使用灰色细边框 `#d0d0d0`，表头仅用浅灰背景 `#f0f0f0` 区分，无彩色装饰。
- 行内联样式，保证在不同 Markdown 渲染器下的样式一致性。
- VS Code 中使用 `Ctrl + Shift + V` 预览验证渲染效果。
