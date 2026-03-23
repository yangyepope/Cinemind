---
name: brand-guidelines
description: 将 Anthropic 官方品牌颜色和排版应用于任何可能受益于 Anthropic 外观和感觉的工件。当品牌颜色或风格指南、视觉格式或公司设计标准适用时使用。
license: 完整条款请参阅 LICENSE.txt
---

# Anthropic 品牌风格 (Anthropic Brand Styling)

## 概览

要访问 Anthropic 官方品牌标识和风格资源，请使用此 Skill。

**关键词**：品牌管理、企业形象、视觉识别、后期处理、风格设计、品牌颜色、排版、Anthropic 品牌、视觉格式化、视觉设计

## 品牌指南 (Brand Guidelines)

### 颜色 (Colors)

**核心颜色：**

- 深色 (Dark): `#141413` - 主要文本和深色背景
- 浅色 (Light): `#faf9f5` - 浅色背景及深色背景上的文本
- 中灰 (Mid Gray): `#b0aea5` - 次要元素
- 浅灰 (Light Gray): `#e8e6dc` - 微妙的背景

**强调色 (Accent Colors):**

- 橙色 (Orange): `#d97757` - 主要强调色
- 蓝色 (Blue): `#6a9bcc` - 次要强调色
- 绿色 (Green): `#788c5d` - 三级强调色

### 排版 (Typography)

- **标题 (Headings)**: Poppins (备用字体 Arial)
- **正文 (Body Text)**: Lora (备用字体 Georgia)
- **注意**: 为了获得最佳效果，字体应预先安装在您的环境中。

## 功能特性

### 智能字体应用

- 将 Poppins 字体应用于标题（24pt 及以上）
- 将 Lora 字体应用于正文
- 如果自定义字体不可用，自动回退到 Arial/Georgia
- 确保在所有系统上保持可读性

### 文本样式

- 标题 (24pt+): Poppins 字体
- 正文文本: Lora 字体
- 根据背景智能选择颜色
- 保留文本层级和格式

### 形状和强调色

- 非文本形状使用强调色
- 在橙色、蓝色和绿色强调色之间轮换
- 在保持品牌风格的同时增加视觉趣味

## 技术细节

### 字体管理

- 在可用时使用系统中安装的 Poppins 和 Lora 字体
- 提供自动回退到 Arial（标题）和 Georgia（正文）
- 无需安装字体——可使用现有的系统字体
- 为了获得最佳效果，请在您的环境中预装 Poppins 和 Lora 字体

### 颜色应用

- 使用 RGB 颜色值进行精确的品牌匹配
- 通过 python-pptx 的 RGBColor 类应用
- 在不同系统间保持色彩真实度
