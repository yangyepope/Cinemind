---
name: slack-gif-creator
description: 创建针对 Slack 优化的 GIF 动图的知识和工具。提供约束条件、验证工具和动画概念。当用户请求为 Slack 创建 GIF 动图时使用，例如“帮我做一个 X 正在做 Y 的 Slack GIF”。
license: 完整条款请参阅 LICENSE.txt
---

# Slack GIF 创作大师 (Slack GIF Creator)

一套为 Slack 优化而设计的动画 GIF 创建工具包，包含实用的程序和知识储备。

## Slack 具体要求

**尺寸：**
- 表情包 (Emoji) GIF: 128x128 (推荐)
- 消息 (Message) GIF: 480x480

**参数：**
- FPS (帧率): 10-30 (更低意味着更小的文件体积)
- 颜色数 (Colors): 48-128 (更少意味着更小的文件体积)
- 时长: 表情包 GIF 请保持在 3 秒以内

## 核心工作流

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建构建器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成每一帧
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # 使用 PIL 基元进行绘图
    # (圆、多边形、线条等)

    builder.add_frame(frame)

# 3. 带有优化地保存
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 处理用户上传的图像
如果用户上传了图像，请考虑他们是否想要：
- **直接使用** (例如“让这个动起来”、“把它拆分成帧”)
- **作为灵感** (例如“做一个类似这样的东西”)

使用 PIL 加载并处理图像：
```python
from PIL import Image

uploaded = Image.open('file.png')
# 直接使用，或仅作为颜色/风格参考
```

### 从零开始绘制
从零绘制图形时，请使用 PIL ImageDraw 提供的基元：

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# 圆形/椭圆
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 星形、三角形或任何多边形
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 线条
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 矩形
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**不要使用**：表情符号字体（跨平台不可靠），也不要假设本技能内置了预包装的图形。

### 如何让图形更美观
图形应该看起来精美且具有创意，而不是平淡无奇。方法如下：

**使用粗线条** —— 始终将 `width` 设置为 2 或更高。细线条（width=1）看起来会断断续续，显得不够专业。

**增加视觉深度**：
- 使用渐变背景 (`create_gradient_background`)
- 通过重叠多种形状增加复杂度（例如：星形内部套一个小星形）

**让形状更有趣**：
- 不要只画一个纯色圆 —— 添加高光、环绕带或图案
- 星形可以有光晕（在背后绘制更大、半透明的版本）
- 组合多种形状（星星 + 闪烁，圆圈 + 圆环）

**注重色彩**：
- 使用鲜艳、互补的颜色
- 增加对比度（浅色形状配深色轮廓，深色形状配浅色轮廓）
- 考虑整体构图

**处理复杂形状**（心形、雪花等）：
- 组合多边形和椭圆
- 仔细计算点位以保持对称性
- 添加细节（心形可以有高光曲线，雪花可以有错综的分支）

发挥想象力！一个好的 Slack GIF 应该看起来打磨得很精细，而不是像占位符图形。

## 可用的实用工具

### GIFBuilder (`core.gif_builder`)
负责组装帧并为 Slack 进行优化：
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # 添加 PIL Image 对象
builder.add_frames(frames)  # 添加帧列表
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### 验证器 (`core.validators`)
检查 GIF 是否符合 Slack 的要求：
```python
from core.validators import validate_gif, is_slack_ready

# 详细验证
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# 快速检查
if is_slack_ready('my.gif'):
    print("就绪!")
```

### 缓动函数 (`core.easing`)
实现平滑运动而非线性运动：
```python
from core.easing import interpolate

# 进度从 0.0 到 1.0
t = i / (num_frames - 1)

# 应用缓动
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# 可用选项: linear, ease_in, ease_out, ease_in_out,
#           bounce_out, elastic_out, back_out
```

### 帧辅助程序 (`core.frame_composer`)
处理常见需求的便捷函数：
```python
from core.frame_composer import (
    create_blank_frame,         # 纯色背景
    create_gradient_background,  # 垂直渐变
    draw_circle,                # 圆形辅助
    draw_text,                  # 简单的文本渲染
    draw_star                   # 五角星
)
```

## 动画概念

### 抖动/震动 (Shake/Vibrate)
通过震荡偏移物体位置：
- 使用 `math.sin()` 或 `math.cos()` 配合帧索引
- 加入微小的随机变量以获得自然感
- 同时应用于 x 和/或 y 坐标

### 脉动/心跳 (Pulse/Heartbeat)
律动性地缩放物体大小：
- 使用 `math.sin(t * frequency * 2 * math.pi)` 实现平滑脉动
- 心跳效果：两次快速脉动后暂停（调整正弦波）
- 在基础大小的 0.8 到 1.2 倍之间缩放

### 弹跳 (Bounce)
物体下落并回弹：
- 使用 `interpolate()` 配合 `easing='bounce_out'` 处理着陆
- 使用 `easing='ease_in'` 处理下落（加速）
- 通过每帧增加 y 轴速度来模拟重力

### 旋转/自转 (Spin/Rotate)
围绕中心旋转物体：
- PIL 操作：`image.rotate(angle, resample=Image.BICUBIC)`
- 摇摆效果：使用正弦波代替线性变化的旋转角度

### 渐入/渐出 (Fade In/Out)
逐渐出现或消失：
- 创建 RGBA 图像，调整 alpha 通道
- 或使用 `Image.blend(image1, image2, alpha)`
- 渐入：alpha 从 0 到 1
- 渐出：alpha 从 1 到 0

### 滑入 (Slide)
物体从屏幕外移动到指定位置：
- 起始位置：在帧边界之外
- 结束位置：目标位置
- 使用 `interpolate()` 配合 `easing='ease_out'` 实现平稳停止
- 冲出回弹效果：使用 `easing='back_out'`

### 缩放/变焦 (Zoom)
缩放并定位以获得变焦效果：
- 放大：从 0.1 缩放到 2.0，裁剪中心
- 缩小：从 2.0 缩放到 1.0
- 可以添加运动模糊以增加戏剧感 (PIL 滤镜)

### 爆炸/粒子喷发 (Explode/Particle Burst)
创建向外辐射的粒子：
- 生成具有随机角度和速度的粒子
- 更新每个粒子：`x += vx`, `y += vy`
- 增加重力：`vy += gravity_constant`
- 随时间淡化粒子（降低 alpha 值）

## 优化策略

仅当被要求减小文件体积时，实施以下几种方法：

1. **减少帧数** —— 降低 FPS（如 10 而非 20）或缩短时长
2. **减少颜色** —— `num_colors=48` 而非 128
3. **缩小尺寸** —— 128x128 而非 480x480
4. **移除重复帧** —— 在 save() 中设置 `remove_duplicates=True`
5. **表情包模式** —— `optimize_for_emoji=True` 开启自动优化

```python
# 表情包的最大程度优化
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 设计哲学

本技能提供了：
- **知识**：Slack 的要求和动画原理
- **工具**：GIFBuilder, 验证器, 缓动函数
- **灵活性**：使用 PIL 基元自行创建动画逻辑

本技能**不**提供：
- 死板的动画模板或现成的固定函数
- 表情符号字体渲染（跨平台不可靠）
- 内置的预包装图形库

**关于用户上传**：本技能不含预设图形，但如果用户上传了图像，请使用 PIL 加载并处理它 —— 根据用户的请求解读是直接使用还是作为灵感。

发挥创意！组合多种概念（弹跳 + 旋转，脉动 + 滑动等），并充分利用 PIL 的全部能力。

## 依赖项

```bash
pip install pillow imageio numpy
```
