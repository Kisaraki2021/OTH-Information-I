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

# テンプレートのHTMLヘッダー
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

{content}

  </div>
</body>

</html>'''

def convert_line(line):
    """マークダウンのテキスト行をHTMLに変換"""
    # **bold** to <strong>
    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
    # ***italic bold*** to <strong><em>
    line = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', line)
    # `code` to <code>
    line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
    # ![alt](url) to <img>
    line = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img alt="\1" src="\2">', line)
    # [link](url) to <a>
    line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
    return line

def markdown_to_html(md_content):
    """シンプルなマークダウンからHTMLへの変換"""
    lines = md_content.split('\n')
    html_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 見出し
        if line.startswith('# '):
            html_lines.append(f'<h1>{convert_line(line[2:].strip())}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{convert_line(line[3:].strip())}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{convert_line(line[4:].strip())}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{convert_line(line[5:].strip())}</h4>')
        
        # 横線
        elif line.strip().startswith('---'):
            html_lines.append('<hr>')
        
        # テーブル
        elif '|' in line:
            # テーブル全体を取得
            table_lines = [line]
            i += 1
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            i -= 1
            html_lines.append(convert_table(table_lines))
        
        # リスト
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            list_lines = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ') or (lines[i].startswith('\t') and lines[i].strip())):
                list_lines.append(lines[i])
                i += 1
            i -= 1
            html_lines.append(convert_list(list_lines))
        
        # 番号付きリスト
        elif re.match(r'^\d+\.\s', line.strip()):
            list_lines = []
            while i < len(lines) and (re.match(r'^\d+\.\s', lines[i].strip()) or (lines[i].startswith('\t') and lines[i].strip())):
                list_lines.append(lines[i])
                i += 1
            i -= 1
            html_lines.append(convert_ordered_list(list_lines))
        
        # 段落
        elif line.strip() and not line.startswith('```'):
            html_lines.append(f'<p>{convert_line(line.strip())}</p>')
        
        # コードブロック
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            html_lines.append(f'<pre><code>{code_text}</code></pre>')
        
        i += 1
    
    return '\n'.join(html_lines)

def convert_table(table_lines):
    """テーブルをHTMLに変換"""
    rows = [row.strip().split('|')[1:-1] for row in table_lines]
    
    html = '<table>\n'
    
    # ヘッダー
    if len(rows) > 0:
        html += '<tr>'
        for cell in rows[0]:
            html += f'<th>{convert_line(cell.strip())}</th>'
        html += '</tr>\n'
    
    # 区切り行をスキップしてデータ行
    for row in rows[2:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{convert_line(cell.strip())}</td>'
        html += '</tr>\n'
    
    html += '</table>'
    return html

def convert_list(lines):
    """リストをHTMLに変換"""
    html = '<ul>\n'
    
    for line in lines:
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 2  # 2スペースでインデント
        
        text = line.strip()
        if text.startswith('- '):
            text = text[2:]
        elif text.startswith('* '):
            text = text[2:]
        
        if indent_level == 0:
            html += f'<li>{convert_line(text)}</li>\n'
        else:
            # ネストされたリスト
            html = html.rstrip('</li>\n')
            if indent_level == 1:
                html += '\n<ul>\n'
                html += f'<li>{convert_line(text)}</li>\n'
                html += '</ul>\n</li>\n'
    
    html += '</ul>'
    return html

def convert_ordered_list(lines):
    """番号付きリストをHTMLに変換"""
    html = '<ol>\n'
    
    for line in lines:
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 2
        
        text = line.strip()
        match = re.match(r'^\d+\.\s+(.*)$', text)
        if match:
            text = match.group(1)
        
        if indent_level == 0:
            html += f'<li>{convert_line(text)}</li>\n'
        else:
            html = html.rstrip('</li>\n')
            if indent_level == 1:
                html += '\n<ol>\n'
                html += f'<li>{convert_line(text)}</li>\n'
                html += '</ol>\n</li>\n'
    
    html += '</ol>'
    return html

def get_title_from_markdown(md_content):
    """マークダウンから最初の見出しをタイトルとして取得"""
    for line in md_content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"

def convert_markdown_file(md_file, html_file):
    """マークダウンファイルをHTMLに変換して保存"""
    md_path = docs_dir / md_file
    html_path = docs_dir / html_file
    
    if not md_path.exists():
        print(f"✗ {md_file} not found")
        return False
    
    # マークダウンを読み込む
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # タイトルを取得
    title = get_title_from_markdown(md_content)
    
    # HTMLに変換
    html_content = markdown_to_html(md_content)
    
    # 完全なHTMLを構築
    full_html = html_template_header.format(title=title, content=html_content)
    
    # ファイルに保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ {html_file} created")
    return True

# メイン処理
if __name__ == "__main__":
    print("Converting Markdown files to HTML...\n")
    success_count = 0
    
    for md_file, html_file in files_to_convert:
        if convert_markdown_file(md_file, html_file):
            success_count += 1
    
    print(f"\nTotal: {success_count}/{len(files_to_convert)} files converted")
