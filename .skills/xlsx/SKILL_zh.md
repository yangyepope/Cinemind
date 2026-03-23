---
name: xlsx
description: "每当电子表格文件作为主要输入或输出时，请使用此技能。这意味着任何涉及以下操作的任务：打开、读取、编辑或修复现有的 .xlsx、.xlsm、.csv 或 .tsv 文件（例如：添加列、计算公式、格式化、绘图、清理杂乱数据）；从头开始或从其他数据源创建新的电子表格；或在表格文件格式之间进行转换。当用户通过名称或路径提及电子表格文件（甚至是随口提及，如“我下载文件夹里的 xlsx”）并希望对其执行操作或从中生成内容时，应特别触发此技能。此外，该技能也适用于将杂乱的表格数据文件（错误的行、错位的表头、垃圾数据）清理并重构为规范的电子表格。交付成果必须是一个电子表格文件。当主要交付成果是 Word 文档、HTML 报告、独立的 Python 脚本、数据库流水线或 Google Sheets API 集成时，即使涉及表格数据，也不要触发此技能。"
license: 专有。完整条款请参阅 LICENSE.txt
---

# 输出要求 (Requirements for Outputs)

## 所有 Excel 文件

### 专业字体
- 除非用户另有说明，否则所有交付成果均使用一致且专业的字体（例：Arial, Times New Roman）。

### 零公式错误
- 交付的每个 Excel 模型都**必须**保证零公式错误（#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?）。

### 保护现有模板（在更新模板时）
- 修改文件时，研究并**完全匹配**现有的格式、样式和约定。
- 绝不要对已有成熟格式模式的文件强加标准化格式。
- 现有模板的约定**始终优先**于这些准则。

## 财务模型 (Financial models)

### 颜色编码标准
除非用户另有说明或已有模板约定。

#### 行业标准颜色规范
- **蓝色文本 (RGB: 0,0,255)**: 硬编码的输入，以及用户将在情景分析中更改的数字。
- **黑色文本 (RGB: 0,0,0)**: 所有的公式和计算过程。
- **绿色文本 (RGB: 0,128,0)**: 同一工作簿中其他工作表的链接引用。
- **红色文本 (RGB: 255,0,0)**: 指向其他文件的外部链接引用。
- **黄色背景 (RGB: 255,255,0)**: 需要关注的关键假设或需要更新的单元格。

### 数字格式标准

#### 必选格式规则
- **年度**: 格式化为文本字符串（例：“2024”而非“2,024”）。
- **货币**: 使用 $#,##0 格式；**务必**在标题中注明单位（例：“Revenue ($mm)”）。
- **零值**: 使用数字格式使所有零值显示为“-”，包括百分比（例：“$#,##0;($#,##0);-”）。
- **百分比**: 默认为 0.0% 格式（保留一位小数）。
- **倍数**: 估值倍数（EV/EBITDA, P/E）格式化为 0.0x。
- **负数**: 使用括号 (123) 而非负号 -123。

### 公式构建规则

#### 假设值的放置
- 将所有假设值（增长率、毛利率、倍数等）放在独立的假设单元格中。
- 在公式中使用单元格引用，而非硬编码数值。
- 示例：使用 `=B5*(1+$B$6)` 而非 `=B5*1.05`。

#### 公式错误预防
- 验证所有单元格引用是否正确。
- 检查范围中的“差一错误 (off-by-one errors)”。
- 确保所有预测期间的公式保持一致。
- 使用边界情况进行测试（零值、负数）。
- 验证没有无意中产生的循环引用。

#### 硬编码数值的文档要求
- 在单元格旁添加批注或备注。格式：“来源: [系统/文档], [日期], [具体参考], [URL(如果适用)]”。
- 示例：
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"

# XLSX 创建、编辑与分析

## 概览

用户可能会要求你创建、编辑或分析 .xlsx 文件的内容。针对不同的任务，你可以使用不同的工具和工作流。

## 重要要求

**公式重算需使用 LibreOffice**: 你可以假设已安装 LibreOffice，以便通过 `scripts/recalc.py` 脚本重新计算公式值。该脚本在首次运行时会自动配置 LibreOffice，即使在受限的沙盒环境中也能运行。

## 读取与分析数据

### 使用 pandas 进行数据分析
对于数据分析、可视化和基础操作，推荐使用 **pandas**，它提供了强大的数据处理能力：

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel('file.xlsx')  # 默认读取第一个工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 以字典形式读取所有工作表

# 分析
df.head()      # 预览数据
df.info()      # 列信息
df.describe()  # 统计摘要

# 写入 Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 文件工作流

## 关键：使用公式，而非硬编码数值 (Use Formulas, Not Hardcoded Values)

**务必使用 Excel 公式，而非在 Python 中计算好结果后再硬编码到单元格中。** 这能确保电子表格是动态且可更新的。

### ❌ 错误做法 —— 硬编码计算后的结果
```python
# 差：在 Python 中求和并硬编码
total = df['Sales'].sum()
sheet['B10'] = total  # 硬编码了 5000

# 差：在 Python 中计算增长率
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # 硬编码了 0.15
```

### ✅ 正确做法 —— 使用 Excel 公式
```python
# 好：让 Excel 自己求和
sheet['B10'] = '=SUM(B2:B9)'

# 好：将增长率编写为 Excel 公式
sheet['C5'] = '=(C4-C2)/C2'
```

这适用于所有计算 —— 总计、百分比、比率、差值等。当源数据改变时，电子表格应能自动重新计算。

## 常用工作流
1. **选择工具**: pandas 用于处理数据，openpyxl 用于处理公式/格式。
2. **创建/加载**: 创建新工作簿或加载现有文件。
3. **修改**: 添加/编辑数据、公式和格式。
4. **保存**: 写入文件。
5. **重新计算公式（如果使用了公式，则为必选项）**: 使用 `scripts/recalc.py` 脚本。
   ```bash
   python scripts/recalc.py output.xlsx
   ```
6. **验证并修复错误**: 
   - 脚本会返回包含错误详情的 JSON。
   - 如果 `status` 为 `errors_found`，检查 `error_summary` 获取具体错误类型和位置并修复。

### 使用 openpyxl 创建新文件 (示例)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
sheet = wb.active

# 添加公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式化
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')

wb.save('output.xlsx')
```

## 公式重算 (Recalculating formulas)

由 openpyxl 创建或修改的 Excel 文件包含字符串形式的公式，但没有计算后的值。使用提供的 `scripts/recalc.py` 脚本执行重算：

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

该脚本会自动设置 LibreOffice 宏，重算所有工作表的所有公式，并扫描所有单元格中的 Excel 错误（#REF!, #DIV/0! 等）。

## 公式验证清单

### 核心校验
- [ ] **测试 2-3 个样本引用**: 在构建完整模型前验证其取值是否正确。
- [ ] **列映射**: 确认 Excel 列字母匹配（例：第 64 列是 BL，而非 BK）。
- [ ] **行偏移**: 记住 Excel 行是从 1 开始索引的（DataFrame 第 5 行 = Excel 第 6 行）。

### 常见坑点
- [ ] **NaN 处理**: 使用 `pd.notna()` 检查空值。
- [ ] **零分母**: 在公式中使用 `/` 前检查分母是否为零 (#DIV/0!)。
- [ ] **跨表引用**: 链接不同工作表时使用正确格式 (`Sheet1!A1`)。

## 最佳实践

### 库的选择
- **pandas**: 最适合数据分析、批量操作和简单的数据导出。
- **openpyxl**: 最适合复杂的格式化、公式处理和 Excel 特有功能。

### openpyxl 使用说明
- 单元格索引是从 1 开始的。
- 使用 `data_only=True` 读取计算后的值：`load_workbook('file.xlsx', data_only=True)`。
- **警告**: 如果以 `data_only=True` 打开并保存，公式将被替换为值并永久丢失。
- 公式会被保留但不会自动计算 —— 请使用 `scripts/recalc.py` 更新值。

## 代码风格指南
**重要**: 在生成用于 Excel 操作的 Python 代码时：
- 编写精简、干练的 Python 代码，避免不必要的注释或 print 语句。
- 电子表格本身：在具有复杂公式或重要假设的单元格中添加批注，并记录硬编码数值的数据来源。
