# 自动化营销内容生成系统

一个可批量根据关键词生成营销标题与正文，并导出为 HTML 页面的轻量项目。

## 功能

- 输入单个或多个关键词
- 自动生成营销标题 + 内容
- 每个关键词输出一个独立 HTML 页面
- 支持批量生成（命令行参数或关键词文件）
- 自动生成索引页 `index.html`

## 运行环境

- Python 3.9+

## 快速开始

### 1) 直接传入关键词批量生成

```bash
python3 main.py --keywords "AI营销" "私域增长" "跨境电商"
```

### 2) 从文件批量读取关键词

创建 `keywords.txt`（每行一个关键词）：

```text
AI营销
私域增长
跨境电商
```

运行：

```bash
python3 main.py --keyword-file keywords.txt
```

## 输出说明

默认输出目录为 `output/`：

- `output/index.html`：总入口页（展示全部关键词页面链接）
- `output/<slug>.html`：每个关键词对应的营销内容页

## 常用参数

- `--keywords`：直接输入多个关键词
- `--keyword-file`：从文本文件读取关键词（每行一个）
- `--output-dir`：自定义输出目录（默认 `output`）
- `--brand`：品牌名（默认 `增长引擎`）
- `--audience`：目标受众（默认 `中小企业营销负责人`）
- `--tone`：文案语气（默认 `专业且有行动号召`）

示例：

```bash
python3 main.py \
  --keyword-file keywords.txt \
  --output-dir dist \
  --brand "NovaGrowth" \
  --audience "电商运营团队" \
  --tone "简洁直接"
```

## 项目结构

```text
.
├── main.py
├── README.md
└── output/              # 运行后自动生成
```
