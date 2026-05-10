#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

# ドキュメントディレクトリ
docs_dir = Path(__file__).parent / "docs"

# 変換対象のマークダウンファイルとHTMLファイルの対応
files_to_convert = [
    ("s1-final-printout.md", "s1-final-printout.html"),
    ("s1-final.md", "s1-final.html"),
    ("s1-middle-printout.md", "s1-middle-printout.html"),
    ("s1-middle.md", "s1-middle.html"),
    ("s2-final.md", "s2-final.html"),
    ("s2-middle-printout.md", "s2-middle-printout.html"),
    ("s2-middle.md", "s2-middle.html"),
    ("s3-final.md", "s3-final.html"),
]

def build_html_template(title, content):
    """HTMLテンプレートを構築"""
    return f'''<!DOCTYPE html>
<html>

<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-7QN61849JJ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
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

{content}

  </div>
</body>

</html>'''

def convert_markdown_file(md_file, html_file):
    """マークダウンファイルをHTMLにコピー（基本的にコンテンツ部分だけを抽出）"""
    md_path = docs_dir / md_file
    html_path = docs_dir / html_file
    
    if not md_path.exists():
        print(f"✗ {md_file} not found")
        return False
    
    # マークダウンを読み込む
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # タイトルを最初のH1から取得
    title = "Untitled"
    for line in md_content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # マークダウンの内容をプレーンテキストで囲む（高度な変換は避ける）
    # ここでは基本的に <pre> タグで囲む（本来はMarkdown Preview Enhancedのエクスポート機能が必要）
    # ただし、基本的なHTMLタグ変換を行う
    
    content = convert_simple_markdown(md_content)
    
    # 完全なHTMLを構築
    full_html = build_html_template(title, content)
    
    # ファイルに保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ {html_file} created")
    return True

def convert_simple_markdown(md_text):
    """シンプルなマークダウン変換（基本的なパターンのみ）"""
    result = []
    lines = md_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 見出し
        if line.startswith('# '):
            result.append(f'<h1>{escape_html(line[2:].strip())}</h1>')
        elif line.startswith('## '):
            result.append(f'<h2>{escape_html(line[3:].strip())}</h2>')
        elif line.startswith('### '):
            result.append(f'<h3>{escape_html(line[4:].strip())}</h3>')
        elif line.startswith('#### '):
            result.append(f'<h4>{escape_html(line[5:].strip())}</h4>')
        elif line.startswith('##### '):
            result.append(f'<h5>{escape_html(line[6:].strip())}</h5>')
        elif line.startswith('###### '):
            result.append(f'<h6>{escape_html(line[7:].strip())}</h6>')
        # 横線
        elif line.strip() == '---' or line.strip() == '***':
            result.append('<hr>')
        # 空行
        elif line.strip() == '':
            result.append('')
        # リスト
        elif line.lstrip().startswith('- ') or line.lstrip().startswith('* '):
            list_html = process_list(lines, i)
            if list_html:
                result.extend(list_html[0])
                i = list_html[1] - 1
        # 段落
        else:
            result.append(f'<p>{convert_inline_markdown(escape_html(line))}</p>')
        
        i += 1
    
    return '\n'.join(result)

def escape_html(text):
    """HTMLの特殊文字をエスケープ"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def convert_inline_markdown(text):
    """インライン要素の変換（bold、code、link等）"""
    # **bold** → <strong>
    text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', text)
    # `code` → <code>
    text = re.sub(r'`([^`]+?)`', r'<code>\1</code>', text)
    # [link](url) → <a href>
    text = re.sub(r'\[([^\]]+?)\]\(([^)]+?)\)', r'<a href="\2">\1</a>', text)
    # ![image](url) → <img>
    text = re.sub(r'!\[([^\]]*?)\]\(([^)]+?)\)', r'<img alt="\1" src="\2">', text)
    return text

def process_list(lines, start_idx):
    """リスト処理"""
    result = ['<ul>']
    i = start_idx
    
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        
        if stripped.startswith('- ') or stripped.startswith('* '):
            indent = len(line) - len(stripped)
            text = stripped[2:].strip()
            result.append(f'<li>{convert_inline_markdown(escape_html(text))}</li>')
            i += 1
        elif line.strip() == '':
            i += 1
        else:
            break
    
    result.append('</ul>')
    return (result, i)

# メイン処理
if __name__ == "__main__":
    print("Converting Markdown files to HTML...\n")
    success_count = 0
    
    for md_file, html_file in files_to_convert:
        if convert_markdown_file(md_file, html_file):
            success_count += 1
    
    print(f"\nTotal: {success_count}/{len(files_to_convert)} files converted")
