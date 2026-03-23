---
name: web-artifacts-builder
description: 一套用于创建精细的、多组件 claude.ai HTML Artifacts 的工具集，使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 Artifact —— 不适用于简单的单文件 HTML/JSX Artifact。
license: 完整条款请参阅 LICENSE.txt
---

# Web Artifacts 构建器

要构建强大的前端 claude.ai Artifacts，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发你的 Artifact
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示 Artifact
5. (可选) 测试 Artifact

**技术栈**: React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计与样式准则

非常重要：为了避免所谓的“AI 废话/同质化 (AI slop)”，请避免过度使用居中布局、紫色渐变、整齐划一的圆角以及 Inter 字体。

## 快速开始

### 第 1 步：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <项目名称>
cd <项目名称>
```

这将创建一个配置齐全的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ Tailwind CSS 3.4.1 (带有 shadcn/ui 主题系统)
- ✅ 配置了路径别名 (`@/`)
- ✅ 预安全了 40+ 个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖
- ✅ 配置了 Parcel 用于打包 (通过 .parcelrc)
- ✅ Node 18+ 兼容性 (自动检测并固定 Vite 版本)

### 第 2 步：开发你的 Artifact

通过编辑生成的文件来构建 Artifact。请参阅下方的**常见开发任务**获取指导。

### 第 3 步：打包为单个 HTML 文件

将 React 应用打包为单个 HTML Artifact：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` —— 一个包含所有 JavaScript、CSS 和内联依赖项的独立 Artifact。该文件可以直接在 Claude 对话中作为 Artifact 分享。

**要求**：你的项目根目录下必须有一个 `index.html`。

**脚本的作用**：
- 安装打包依赖项 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 构建（无 Source map）
- 使用 html-inline 将所有资产内联到单个 HTML 中

### 第 4 步：与用户共享 Artifact

最后，在对话中与用户分享打包好的 HTML 文件，以便他们将其作为 Artifact 查看。

### 第 5 步：测试/可视化 Artifact (可选)

注意：这是一个完全可选的步骤。仅在必要或被要求时执行。

要测试/可视化 Artifact，请使用可用工具（包括其他 Skill 或内置工具如 Playwright 或 Puppeteer）。通常，避免预先测试 Artifact，因为这会增加从请求到看到成品之间的延迟。如果被要求或出现问题，请在展示 Artifact 之后再进行测试。

## 参考资料

- **shadcn/ui 组件库**: https://ui.shadcn.com/docs/components
