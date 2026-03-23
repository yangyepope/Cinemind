---
name: webapp-testing
description: 使用 Playwright 与本地 Web 应用交互并进行测试的工具包。支持验证前端功能、调试 UI 行为、捕获浏览器截图以及查看浏览器日志。
license: 完整条款请参阅 LICENSE.txt
---

# Web 应用测试 (Web Application Testing)

要测试本地 Web 应用，请编写原生的 Python Playwright 脚本。

**可用的辅助脚本**:
- `scripts/with_server.py` - 管理服务器生命周期（支持多个服务器）

**务必先运行带 `--help` 的脚本**以查看用法。在确有必要进行自定义之前，请不要读取源码。这些脚本可能非常庞大，会污染你的上下文窗口。它们应该作为“黑盒脚本”直接调用，而不是被吸纳到你的上下文窗口中。

## 决策树：选择你的方法

```
用户任务 → 是静态 HTML 吗？
    ├─ 是 → 直接读取 HTML 文件以识别选择器 (Selectors)
    │        ├─ 成功 → 使用选择器编写 Playwright 脚本
    │        └─ 失败/不完整 → 视为动态应用（见下方）
    │
    └─ 否 (动态 Web 应用) → 服务器是否正在运行？
        ├─ 否 → 运行: python scripts/with_server.py --help
        │        然后使用辅助程序并编写简化的 Playwright 脚本
        │
        └─ 是 → 侦察后行动：
            1. 导航并等待 networkidle (网络空闲)
            2. 截图或检查 DOM
            3. 从渲染状态识别选择器
            4. 使用发现的选择器执行动作
```

## 示例：使用 with_server.py

启动服务器前，请先运行 `--help`，然后使用辅助程序：

**单个服务器:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多个服务器（例如：后端 + 前端）:**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

要创建自动化脚本，仅需包含 Playwright 逻辑（服务器由程序自动管理）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # 始终在无头模式下启动 chromium
    page = browser.new_page()
    page.goto('http://localhost:5173') # 服务器已在运行并就绪
    page.wait_for_load_state('networkidle') # 关键：等待 JS 执行
    # ... 你的自动化逻辑
    browser.close()
```

## “侦察后行动”模式 (Reconnaissance-Then-Action)

1. **检查渲染后的 DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **从检查结果中识别选择器**

3. **使用发现的选择器执行动作**

## 常见坑点

❌ **不要**在动态应用中等待 `networkidle` 之前就开始检查 DOM。
✅ **务必**在检查前等待 `page.wait_for_load_state('networkidle')`。

## 最佳实践

- **将捆绑的脚本视为“黑盒”** —— 要完成任务，请考虑 `scripts/` 中现有的脚本是否能提供帮助。这些脚本能可靠地处理常见的复杂工作流，而不会弄乱上下文窗口。使用 `--help` 查看用法，然后直接调用。
- 使用 `sync_playwright()` 编写同步脚本。
- 完成后务必关闭浏览器。
- 使用具有描述性的选择器：`text=`、`role=`、CSS 选择器或 ID。
- 添加适当的等待：`page.wait_for_selector()` 或 `page.wait_for_timeout()`。

## 参考文件

- **examples/** - 展示常见模式的示例：
  - `element_discovery.py` - 发现页面上的按钮、链接和输入框
  - `static_html_automation.py` - 为本地 HTML 使用 file:// URLs
  - `console_logging.py` - 在自动化过程中捕获控制台日志
