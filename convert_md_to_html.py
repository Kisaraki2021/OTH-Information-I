#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import markdown2
from pathlib import Path

# ドキュメントディレクトリ
docs_dir = Path(__file__).parent / "docs"

# 変換対象のマークダウンファイルとHTMLファイルの対応
files_to_convert = [
    ("s1-final-printout.md", "s1-final-printout.html", "情報I 1学期期末考査 対策プリント"),
    ("s1-final.md", "s1-final.html", "情報I 1学期期末考査 対策プリント"),
    ("s1-middle-printout.md", "s1-middle-printout.html", "情報I 1学期中間考査 対策プリント"),
    ("s1-middle.md", "s1-middle.html", "情報I 1学期中間考査 対策プリント"),
    ("s2-final.md", "s2-final.html", "情報I 2学期期末考査 対策プリント"),
    ("s2-middle-printout.md", "s2-middle-printout.html", "情報I 2学期中間考査 対策プリント"),
    ("s2-middle.md", "s2-middle.html", "情報I 2学期中間考査 対策プリント"),
    ("s3-final.md", "s3-final.html", "情報I 3学期学年末考査 対策プリント"),
]

# テンプレートのHTMLヘッダー（s3-final-printout-orange.htmlから抽出）
html_template_header = '''<!DOCTYPE html>
<html>

<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-7QN61849JJ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());

    gtag('config', 'G-7QN61849JJ');
  </script>
  <title>{title}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <link rel="stylesheet"
    href="file:///c:\\Users\\yutoi\\.vscode\\extensions\\shd101wyy.markdown-preview-enhanced-0.8.20\\crossnote\\dependencies\\katex\\katex.min.css">

  <style>
    html body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      font-size: 16px;
      line-height: 1.6;
      color: #000;
      background: #fff;
      padding: 16px;
      margin: 0;
    }}

    html body img {{
      max-width: 100%;
      height: auto;
    }}

    html body code {{
      font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
      font-size: .85em;
      color: #000;
      background-color: #f0f0f0;
      border-radius: 3px;
      padding: .2em 0;
    }}

    html body code::after,
    html body code::before {{
      letter-spacing: -.2em;
      content: '\\00a0';
    }}

    html body h1,
    html body h2,
    html body h3,
    html body h4,
    html body h5,
    html body h6 {{
      font-weight: 600;
      margin: 16px 0 12px 0;
      page-break-after: avoid;
    }}

    html body>p {{
      margin-top: 0;
      margin-bottom: 16px;
      word-wrap: break-word;
    }}

    html body>ol,
    html body>ul {{
      margin-bottom: 16px;
    }}

    html body ol,
    html body ul {{
      padding-left: 2em;
    }}

    html body li {{
      margin-bottom: 0;
    }}

    html body li>p {{
      margin-top: 0;
      margin-bottom: 0;
    }}

    html body hr {{
      height: 4px;
      margin: 32px 0;
      background-color: #d6d6d6;
      border: 0 none;
    }}

    html body blockquote {{
      margin: 16px 0;
      font-size: inherit;
      padding: 0 15px;
      color: #5c5c5c;
      background-color: #f0f0f0;
      border-left: 4px solid #d6d6d6;
    }}

    /* s2-final と同じ「強調はオレンジ」 */
    html body strong {{
      color: #ff833c;
    }}

    .markdown-preview {{
      width: 100%;
      height: 100%;
      box-sizing: border-box;
    }}

    /* A4印刷向け */
    @page {{
      size: A4;
      margin: 12mm;
    }}

    @media print {{
      html body {{
        padding: 0;
      }}

      html body img {{
        display: block;
        max-width: 100%;
        break-inside: avoid;
        page-break-inside: avoid;
      }}
    }}

    /* 画像サイズ調整（A4でちょうどよく） */
    html body img.license-badge {{
      width: 55mm;
      max-width: 70%;
    }}

    html body img.flowchart-symbol {{
      width: 55mm;
      max-width: 80%;
      margin: 6px 0 10px 0;
    }}

    @media print {{
      html body img.license-badge {{
        width: 50mm;
      }}

      html body img.flowchart-symbol {{
        width: 45mm;
      }}
    }}
  </style>
  <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function () {{
      // your code here
    }});
  </script>
</head>

<body for="html-export">

  <div class="crossnote markdown-preview">
'''

html_template_footer = '''
  </div>
</body>

</html>'''

def convert_markdown_to_html(md_file, html_file, title):
    """マークダウンファイルをHTMLに変換"""
    md_path = docs_dir / md_file
    html_path = docs_dir / html_file
    
    if not md_path.exists():
        print(f"Error: {md_file} not found")
        return False
    
    # マークダウンを読み込む
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # マークダウンをHTMLに変換
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # タイトルをファイルから取得（最初のH1またはファイルから）
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content)
    if match:
        title = match.group(1)
    
    # 完全なHTMLを構築
    full_html = html_template_header.format(title=title) + html_content + html_template_footer
    
    # HTMLファイルに書き込む
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ Created: {html_file}")
    return True

# メイン処理
if __name__ == "__main__":
    print("Converting Markdown files to HTML...")
    success_count = 0
    
    for md_file, html_file, title in files_to_convert:
        if convert_markdown_to_html(md_file, html_file, title):
            success_count += 1
    
    print(f"\nTotal: {success_count}/{len(files_to_convert)} files converted successfully")
