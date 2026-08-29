import urllib.request
from bs4 import BeautifulSoup, Tag, NavigableString
import re
import os

def element_to_markdown(el):
    if isinstance(el, NavigableString):
        text = str(el)
        # Normalize whitespace inside text node
        text = re.sub(r'\s+', ' ', text)
        return text
    
    if not isinstance(el, Tag):
        return ""
    
    tag_name = el.name.lower()
    
    # Ignore hidden / script / style / svg / nav / button tags
    if tag_name in ['script', 'style', 'noscript', 'svg', 'iframe', 'button', 'form']:
        return ""
    
    # Check if element is hidden via inline style or attribute
    style = el.get('style', '')
    if 'display:none' in style.replace(' ', '') or el.get('aria-hidden') == 'true':
        return ""
    
    # Formatting helper for children
    def inner_markdown():
        res = []
        for child in el.children:
            res.append(element_to_markdown(child))
        return "".join(res)
    
    # Headings
    if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(tag_name[1])
        heading_text = inner_markdown().strip()
        if heading_text:
            return f"\n\n{'#' * level} {heading_text}\n\n"
        return ""
    
    # Paragraphs
    if tag_name == 'p':
        text = inner_markdown().strip()
        if text:
            return f"\n\n{text}\n\n"
        return ""
    
    # Formatting
    if tag_name in ['strong', 'b']:
        text = inner_markdown().strip()
        if text:
            return f"**{text}**"
        return ""
    
    if tag_name in ['em', 'i']:
        text = inner_markdown().strip()
        if text:
            return f"*{text}*"
        return ""
    
    if tag_name == 'code':
        text = inner_markdown().strip()
        if text:
            return f"`{text}`"
        return ""
    
    if tag_name == 'a':
        text = inner_markdown().strip()
        href = el.get('href', '')
        if href and href.startswith('/'):
            href = 'https://cloud.google.com' + href
        if text and href:
            return f"[{text}]({href})"
        elif text:
            return text
        return ""
    
    if tag_name == 'img':
        alt = el.get('alt', '').strip()
        src = el.get('src', '') or el.get('data-src', '')
        if src and src.startswith('/'):
            src = 'https://cloud.google.com' + src
        if src:
            return f"\n\n![{alt}]({src})\n\n"
        return ""
    
    # Lists
    if tag_name == 'ul':
        items = []
        for li in el.find_all('li', recursive=False):
            item_text = element_to_markdown(li).strip()
            if item_text:
                # Indent lines if multiline
                lines = item_text.split('\n')
                formatted = "- " + lines[0]
                for l in lines[1:]:
                    if l.strip():
                        formatted += "\n  " + l
                items.append(formatted)
        return "\n\n" + "\n".join(items) + "\n\n"
    
    if tag_name == 'ol':
        items = []
        idx = 1
        for li in el.find_all('li', recursive=False):
            item_text = element_to_markdown(li).strip()
            if item_text:
                lines = item_text.split('\n')
                formatted = f"{idx}. " + lines[0]
                for l in lines[1:]:
                    if l.strip():
                        formatted += "\n  " + l
                items.append(formatted)
                idx += 1
        return "\n\n" + "\n".join(items) + "\n\n"
    
    if tag_name == 'li':
        return inner_markdown().strip()
    
    # Tables
    if tag_name == 'table':
        rows = []
        for tr in el.find_all('tr'):
            cells = []
            is_header = False
            for th_or_td in tr.find_all(['th', 'td']):
                if th_or_td.name == 'th':
                    is_header = True
                cell_text = element_to_markdown(th_or_td).strip().replace('\n', ' ')
                cells.append(cell_text)
            if cells:
                rows.append((is_header, cells))
        
        if not rows:
            return ""
        
        md_table = []
        # Header row
        header_row = rows[0][1]
        md_table.append("| " + " | ".join(header_row) + " |")
        md_table.append("| " + " | ".join(["---"] * len(header_row)) + " |")
        
        start_idx = 1 if rows[0][0] else 0
        for is_h, cells in rows[start_idx:]:
            # match column count
            while len(cells) < len(header_row):
                cells.append("")
            md_table.append("| " + " | ".join(cells[:len(header_row)]) + " |")
            
        return "\n\n" + "\n".join(md_table) + "\n\n"
    
    # Blockquotes
    if tag_name == 'blockquote':
        text = inner_markdown().strip()
        lines = [f"> {line}" for line in text.split('\n') if line.strip()]
        return "\n\n" + "\n".join(lines) + "\n\n"
    
    # Default container divs/sections
    return inner_markdown()

def clean_markdown(md):
    # Fix multiple newlines
    md = re.sub(r'\n{3,}', '\n\n', md)
    # Fix spaces around inline elements
    md = re.sub(r' +', ' ', md)
    # Clean up empty headers or broken list formatting
    lines = md.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.rstrip())
    return "\n".join(cleaned_lines).strip()

def extract_google_cloud_learn(url, output_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8"
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html_doc = response.read().decode('utf-8')

    soup = BeautifulSoup(html_doc, 'html.parser')
    
    # Meta information
    title_tag = soup.find('title')
    title_text = title_tag.get_text(strip=True) if title_tag else "Kecerdasan Buatan (AI) | Google Cloud"
    
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_desc = meta_desc_tag['content'] if meta_desc_tag and 'content' in meta_desc_tag.attrs else ""
    
    # Decompose script, style, nav, footer, etc.
    for s in soup(["script", "style", "nav", "noscript", "svg", "header", "footer", "form", "iframe"]):
        s.decompose()

    # Find main article container
    h1 = soup.find('h1')
    if h1:
        parent = h1.parent
        while parent and parent.name != 'body':
            h2s = parent.find_all('h2')
            if len(h2s) >= 4:
                break
            parent = parent.parent
        container = parent
    else:
        container = soup.body

    # Convert to markdown
    raw_md = element_to_markdown(container)
    final_md = clean_markdown(raw_md)
    
    # Prepend header metadata
    header_block = f"""---
title: "{title_text}"
source: "{url}"
description: "{meta_desc}"
extracted_at: "2026-07-22"
---

"""
    full_document = header_block + final_md
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_document)
    
    print(f"Successfully extracted {len(full_document)} characters to {output_path}")

if __name__ == "__main__":
    url = "https://cloud.google.com/learn/what-is-artificial-intelligence?hl=id"
    out_file = os.path.join(os.path.dirname(__file__), "what-is-artificial-intelligence.md")
    extract_google_cloud_learn(url, out_file)
