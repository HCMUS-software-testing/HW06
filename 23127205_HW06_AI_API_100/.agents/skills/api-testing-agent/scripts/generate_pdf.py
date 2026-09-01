#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: 100% PDF.js Compatible PDF Generator with Mermaid Rendering
Author: Lam Huu Khanh (Student ID: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Generates clean, 100% standard PDF documents compatible with all PDF viewers.
  - Automatically renders Mermaid flowcharts into crisp vector SVG diagrams.
  - Sanitizes color emojis to prevent Type3 font pattern errors in PDF.js.
  - Embeds local images as Base64 Data URIs.
  - Formatted tables, code blocks, alerts, and A4 print layout.
=============================================================================
"""

import os
import re
import sys
import base64
import mimetypes
import argparse
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import markdown
from playwright.sync_api import sync_playwright

CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
}

* {
    box-sizing: border-box;
}

body {
    font-family: Arial, "Helvetica Neue", "Segoe UI", Tahoma, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

h1 {
    font-size: 16.5pt;
    font-weight: bold;
    color: #1e40af;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 5px;
    margin-top: 0;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h2 {
    font-size: 13.5pt;
    font-weight: bold;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
}

h3 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

h4 {
    font-size: 10.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 4px;
}

p {
    margin-top: 4px;
    margin-bottom: 8px;
    font-size: 9.8pt;
    color: #334155;
}

ul {
    list-style-type: disc !important;
    margin: 6px 0 10px 0 !important;
    padding-left: 22px !important;
}

ol {
    list-style-type: decimal !important;
    margin: 6px 0 10px 0 !important;
    padding-left: 22px !important;
}

li {
    margin-bottom: 3px;
    line-height: 1.55;
    font-size: 9.8pt;
    color: #334155;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
    color: #1e293b;
}

th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.8pt;
    background-color: #f1f5f9;
    color: #b91c1c;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}

pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 8px 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.4pt;
    line-height: 1.45;
    margin: 8px 0;
    border: 1px solid #334155;
    page-break-inside: avoid;
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
}

pre code {
    background: transparent !important;
    color: inherit !important;
    padding: 0 !important;
    border: none !important;
    white-space: pre-wrap !important;
}

blockquote {
    margin: 8px 0;
    padding: 8px 14px;
    background-color: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 0 4px 4px 0;
    color: #1e40af;
    font-size: 9.4pt;
    page-break-inside: avoid;
}

blockquote p {
    margin: 0;
    color: #1e40af;
}

img {
    max-width: 95%;
    max-height: 480px;
    display: block;
    margin: 10px auto;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
    page-break-inside: avoid;
}

hr {
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 14px 0;
}

.mermaid {
    text-align: center;
    margin: 14px auto;
    background-color: #ffffff;
    padding: 10px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    page-break-inside: avoid !important;
}

.mermaid svg {
    max-width: 100% !important;
    height: auto !important;
    display: inline-block;
    margin: 0 auto;
}

.doc-header-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 5px;
    margin-bottom: 12px;
    font-size: 8pt;
    color: #64748b;
}

.doc-footer-banner {
    margin-top: 24px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
    font-size: 8pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
}
"""

EMOJI_REPLACEMENTS = {
    '🔹': '[+] ',
    '📌': '[Lưu ý] ',
    '🐛': '[Bug] ',
    '✅': '[Pass] ',
    '❌': '[Fail] ',
    '⭐': '[*] ',
    '🟢': '[Pass] ',
    '🔴': '[Fail] ',
    '🏆': '[Score] ',
    '👉': '-> ',
    '💡': '[Note] ',
    '✔️': '[x] ',
    '⚠️': '[Warning] ',
    '🎉': '',
    '🚀': '',
    '🔥': '',
}


def sanitize_markdown(md_text: str) -> str:
    """Sanitize color emojis and alerts that trigger PDF.js Type3 pattern bugs."""
    clean_text = md_text
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        clean_text = clean_text.replace(emoji, replacement)

    # Pre-process GitHub alerts
    clean_text = re.sub(r'>\s*\[!NOTE\]\s*\n(>.*(?:\n>.*)*)', r'<blockquote><strong>NOTE:</strong> \1</blockquote>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'>\s*\[!WARNING\]\s*\n(>.*(?:\n>.*)*)', r'<blockquote><strong>WARNING:</strong> \1</blockquote>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'>\s*\[!IMPORTANT\]\s*\n(>.*(?:\n>.*)*)', r'<blockquote><strong>IMPORTANT:</strong> \1</blockquote>', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'>\s*\[!TIP\]\s*\n(>.*(?:\n>.*)*)', r'<blockquote><strong>TIP:</strong> \1</blockquote>', clean_text, flags=re.IGNORECASE)

    # Clean local file links
    clean_text = re.sub(r'\[([^\]]+)\]\(file:///[^\)]+\)', r'<strong>\1</strong>', clean_text)
    return clean_text


def preprocess_mermaid_blocks(html_content: str) -> str:
    """Transform <pre><code class="language-mermaid">...</code></pre> into <div class="mermaid">...</div>"""
    return re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<div class="mermaid">\1</div>',
        html_content,
        flags=re.DOTALL
    )


def embed_images_as_base64(html_content: str, base_dir: Path) -> str:
    """Find local image references and encode them as base64 Data URIs."""
    def replacer(match):
        src = match.group(1)
        if src.startswith(('http://', 'https://', 'data:')):
            return match.group(0)

        # Resolve relative and absolute paths
        clean_src = src.replace('file:///', '').replace('file://', '')
        img_path = (base_dir / clean_src).resolve()

        if not img_path.exists():
            search_candidates = [
                base_dir / "screenshots" / os.path.basename(clean_src),
                base_dir / "reports" / "screenshots" / os.path.basename(clean_src),
                base_dir.parent / "reports" / "screenshots" / os.path.basename(clean_src),
                base_dir.parent / "agent-skill" / os.path.basename(clean_src),
                Path(clean_src)
            ]
            for c in search_candidates:
                if c.exists() and c.is_file():
                    img_path = c
                    break

        if img_path.exists() and img_path.is_file():
            mime_type, _ = mimetypes.guess_type(str(img_path))
            if not mime_type:
                mime_type = "image/png"
            try:
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                return f'src="data:{mime_type};base64,{b64}"'
            except Exception:
                return match.group(0)

        return match.group(0)

    return re.sub(r'src=["\'](.*?)["\']', replacer, html_content)


def md_to_html(md_path: Path) -> str:
    """Convert Markdown file to styled HTML 100% compatible with PDF.js & Mermaid."""
    with open(md_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    sanitized_md = sanitize_markdown(raw_text)

    # Convert to HTML with tables and fenced code extensions
    html_body = markdown.markdown(sanitized_md, extensions=['tables', 'fenced_code', 'nl2br', 'toc'])
    html_body = preprocess_mermaid_blocks(html_body)
    html_body = embed_images_as_base64(html_body, md_path.parent)

    title = md_path.stem.replace('-', ' ').title()

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{CSS_TEMPLATE}</style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="doc-header-banner">
        <span><strong>HCMUS - Khoa CNTT</strong> | Kiểm Thử Phần Mềm (HW06 - API Testing)</span>
        <span>Sinh viên: <strong>Lâm Hữu Khánh</strong> (MSSV: <strong>23127205</strong>)</span>
    </div>
    {html_body}
    <div class="doc-footer-banner">
        <span>Báo cáo bài tập cá nhân HW06 — Khoa CNTT, Trường ĐH KHTN, ĐHQG-HCM</span>
        <span>Học kỳ 3 (2025-2026)</span>
    </div>
</body>
</html>"""


def convert_single_file(playwright_browser, md_file: Path, pdf_file: Path = None) -> bool:
    """Convert a single Markdown file to PDF cleanly with Mermaid rendering."""
    if not md_file.exists():
        print(f"[-] File not found: {md_file}")
        return False

    if pdf_file is None:
        pdf_file = md_file.with_suffix(".pdf")

    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    html_content = md_to_html(md_file)

    page = playwright_browser.new_page()
    try:
        page.set_content(html_content, wait_until="networkidle")

        # Initialize and render Mermaid diagrams if present
        page.evaluate("""async () => {
            if (window.mermaid && document.querySelector('.mermaid')) {
                mermaid.initialize({
                    startOnLoad: false,
                    theme: 'neutral',
                    fontFamily: 'Arial, sans-serif'
                });
                await mermaid.run();
            }
        }""")

        # Brief wait for SVG layout stability
        page.wait_for_timeout(500)

        # Pure standard PDF without Chromium Type3 header/footer patterns
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
        )
        size_kb = pdf_file.stat().st_size // 1024
        print(f"✅ [SUCCESS] Created PDF ({size_kb} KB): {pdf_file.name}")
        return True
    except Exception as e:
        print(f"❌ [ERROR] Failed to convert {md_file.name}: {e}")
        return False
    finally:
        page.close()


def find_reports_dir() -> Path:
    candidates = [
        Path("reports"),
        Path("HW06/reports"),
        Path("23127205_HW06_AI_API_100/reports"),
        Path("../reports"),
        Path("../../reports"),
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c.resolve()
    return Path("reports").resolve()


def main():
    parser = argparse.ArgumentParser(description="100% PDF.js Compatible PDF Generator with Mermaid Rendering")
    parser.add_argument("--input", "-i", type=str, help="Input Markdown file path")
    parser.add_argument("--output", "-o", type=str, help="Output PDF file path")
    parser.add_argument("--all", "-a", action="store_true", help="Convert all markdown files in reports/")

    args = parser.parse_args()

    print("=" * 70)
    print("  PDF.JS COMPATIBLE PDF GENERATOR (WITH VECTOR MERMAID RENDERING)")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        if args.input:
            in_path = Path(args.input).resolve()
            out_path = Path(args.output).resolve() if args.output else in_path.with_suffix(".pdf")
            convert_single_file(browser, in_path, out_path)
        else:
            rep_dir = find_reports_dir()
            print(f"[INFO] Scanning markdown files in: {rep_dir}")
            md_files = list(rep_dir.glob("*.md"))
            success_count = 0
            for f in md_files:
                if convert_single_file(browser, f):
                    success_count += 1
            print(f"\n[DONE] Successfully converted {success_count}/{len(md_files)} documents.")

        browser.close()


if __name__ == "__main__":
    main()
