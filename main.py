#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(text: str) -> str:
    base = re.sub(r"[^\w\-\s]", "", text.strip().lower())
    base = re.sub(r"[\s_]+", "-", base)
    base = base.strip("-")
    return base or "keyword"


def generate_title(keyword: str, audience: str) -> str:
    return f"{keyword}实战指南：帮{audience}在30天内实现可量化增长"


def generate_body(keyword: str, brand: str, audience: str, tone: str) -> str:
    sections = [
        (
            "痛点洞察",
            f"围绕“{keyword}”，许多{audience}常见问题是投放成本高、转化链路长、内容复用率低。"
            f"{brand}建议先建立统一内容资产库，再做渠道拆分分发。",
        ),
        (
            "策略框架",
            "建议采用“人群细分 → 卖点映射 → 内容矩阵 → 数据复盘”的四步法，"
            f"以{keyword}为核心主题，构建教育型、对比型、案例型三类内容。",
        ),
        (
            "执行清单",
            "1) 每周产出3条短内容与1篇长内容；"
            "2) 每条内容附带明确CTA；"
            "3) 统一UTM参数追踪渠道表现；"
            "4) 每7天复盘并替换低效话术。",
        ),
        (
            "转化示例",
            f"以{keyword}专题页为承接，设置“免费诊断/领取模板/预约演示”三段式转化路径，"
            "通常可在2-4周内看到线索质量提升。",
        ),
        (
            "行动建议",
            f"基于当前业务阶段，优先上线一个“{keyword}最小可行活动（MVP）”，"
            f"按{tone}的表达方式持续优化文案与落地页。",
        ),
    ]

    return "\n".join(f"<h2>{html.escape(title)}</h2>\n<p>{html.escape(content)}</p>" for title, content in sections)


def render_page(keyword: str, title: str, body_html: str, brand: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif; line-height: 1.7; margin: 0; background: #f6f8fb; color: #1f2937; }}
    .container {{ max-width: 900px; margin: 32px auto; background: #fff; padding: 32px; border-radius: 14px; box-shadow: 0 12px 28px rgba(0,0,0,.08); }}
    h1 {{ margin-top: 0; color: #0f172a; }}
    h2 {{ margin-top: 28px; color: #1d4ed8; }}
    .meta {{ font-size: 14px; color: #6b7280; margin-bottom: 18px; }}
    .badge {{ display: inline-block; background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 999px; font-size: 12px; margin-right: 8px; }}
    a {{ color: #2563eb; }}
  </style>
</head>
<body>
  <main class=\"container\">
    <span class=\"badge\">营销内容生成</span>
    <span class=\"badge\">关键词：{html.escape(keyword)}</span>
    <h1>{html.escape(title)}</h1>
    <p class=\"meta\">品牌：{html.escape(brand)} ｜ 生成时间：{now}</p>
    {body_html}
    <hr />
    <p><a href=\"index.html\">返回目录</a></p>
  </main>
</body>
</html>
"""


def render_index(items: list[tuple[str, str]]) -> str:
    links = "\n".join(
        f'<li><a href="{html.escape(filename)}">{html.escape(keyword)}</a></li>'
        for keyword, filename in items
    )
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>营销内容目录</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif; margin: 0; background: #f6f8fb; color: #111827; }}
    .container {{ max-width: 900px; margin: 32px auto; background: #fff; padding: 28px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,.08); }}
    li {{ margin: 8px 0; }}
    a {{ color: #1d4ed8; }}
  </style>
</head>
<body>
  <main class=\"container\">
    <h1>批量生成结果</h1>
    <p>点击下方关键词查看对应营销内容页面：</p>
    <ul>
      {links}
    </ul>
  </main>
</body>
</html>
"""


def load_keywords(args: argparse.Namespace) -> list[str]:
    keywords = list(args.keywords or [])

    if args.keyword_file:
        lines = Path(args.keyword_file).read_text(encoding="utf-8").splitlines()
        keywords.extend(line.strip() for line in lines if line.strip())

    # 去重并保持顺序
    unique_keywords: list[str] = []
    seen: set[str] = set()
    for kw in keywords:
        if kw not in seen:
            unique_keywords.append(kw)
            seen.add(kw)

    return unique_keywords


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="自动化营销内容生成系统")
    parser.add_argument("--keywords", nargs="*", help="直接输入关键词（可多个）")
    parser.add_argument("--keyword-file", help="关键词文件路径（每行一个关键词）")
    parser.add_argument("--output-dir", default="output", help="输出目录，默认 output")
    parser.add_argument("--brand", default="增长引擎", help="品牌名称")
    parser.add_argument("--audience", default="中小企业营销负责人", help="目标受众")
    parser.add_argument("--tone", default="专业且有行动号召", help="文案语气")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    keywords = load_keywords(args)

    if not keywords:
        raise SystemExit("未提供关键词。请使用 --keywords 或 --keyword-file。")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    index_items: list[tuple[str, str]] = []
    used_filenames: set[str] = set()

    for keyword in keywords:
        title = generate_title(keyword, args.audience)
        body_html = generate_body(keyword, args.brand, args.audience, args.tone)

        base_name = f"{slugify(keyword)}.html"
        filename = base_name
        counter = 2
        while filename in used_filenames:
            filename = f"{slugify(keyword)}-{counter}.html"
            counter += 1

        used_filenames.add(filename)
        index_items.append((keyword, filename))

        page_html = render_page(keyword, title, body_html, args.brand)
        (out_dir / filename).write_text(page_html, encoding="utf-8")

    (out_dir / "index.html").write_text(render_index(index_items), encoding="utf-8")

    print(f"已生成 {len(index_items)} 个页面到目录：{out_dir.resolve()}")
    print("入口文件：", (out_dir / "index.html").resolve())


if __name__ == "__main__":
    main()
