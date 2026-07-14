#!/usr/bin/env python3
import argparse
import html as html_module
import re
import subprocess
import urllib.parse
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


PANDOC_TO = "gfm"


def parse_args():
    parser = argparse.ArgumentParser(description="Split an EPUB into cleaner per-chapter Markdown files")
    parser.add_argument("epub", type=Path, help="Path to the input .epub file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output directory (default: <epub_stem>_chapters/)",
    )
    return parser.parse_args()


def get_spine_order(epub_path):
    with zipfile.ZipFile(epub_path) as z:
        names = set(z.namelist())

        container = z.read("META-INF/container.xml").decode()
        opf_path = re.search(r'full-path="([^"]+\.opf)"', container).group(1)
        opf_content = z.read(opf_path).decode()
        opf_dir = str(Path(opf_path).parent)

        manifest = dict(re.findall(r'id="([^"]+)"[^>]+href="([^"]+\.x?html?)"', opf_content))
        spine_ids = re.findall(r'<itemref\s+idref="([^"]+)"', opf_content)

        result = []
        for i, item_id in enumerate(spine_ids):
            if item_id not in manifest:
                continue
            href = manifest[item_id]
            candidates = []
            for h in (href, urllib.parse.unquote(href)):
                full = f"{opf_dir}/{h}" if opf_dir and opf_dir != "." else h
                candidates.append(full)
            real_path = next((c for c in candidates if c in names), candidates[0])
            result.append((i + 1, item_id, real_path))
        return result


def clean_html_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_chapter_number_from_html(html_bytes: bytes) -> int | None:
    html = html_bytes.decode("utf-8", errors="replace")
    candidates = []

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        candidates.append(clean_html_text(title_match.group(1)))

    body_match = re.search(r"<body[^>]*>(.*)", html, re.IGNORECASE | re.DOTALL)
    search_area = body_match.group(1) if body_match else html
    blocks = re.findall(r"<(?:p|h1|h2)[^>]*>(.*?)</(?:p|h1|h2)>", search_area, re.IGNORECASE | re.DOTALL)
    candidates.extend(clean_html_text(block) for block in blocks[:10])

    for text in candidates:
        match = re.search(r"\bChapter\s+(\d+)\b", text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def extract_chapter_number_from_path(internal_path: str) -> int | None:
    path = urllib.parse.unquote(internal_path)
    match = re.search(r"Chapter\s*(\d+)", Path(path).name, re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_title_from_html(html_bytes: bytes) -> str:
    html = html_bytes.decode("utf-8", errors="replace")

    body_match = re.search(r"<body[^>]*>(.*)", html, re.IGNORECASE | re.DOTALL)
    search_area = body_match.group(1) if body_match else html

    section_match = re.search(
        r'<section[^>]+data-type="([^"]+)"[^>]*>(.*?)</section>',
        search_area,
        re.IGNORECASE | re.DOTALL,
    )
    if section_match:
        section_body = section_match.group(2)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", section_body, re.IGNORECASE | re.DOTALL)
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", section_body, re.IGNORECASE | re.DOTALL)
        heading = clean_html_text(h1.group(1)) if h1 else (clean_html_text(h2.group(1)) if h2 else "")
        if heading:
            return heading

    for tag in ["h1", "h2"]:
        m = re.search(fr"<{tag}[^>]*>(.*?)</{tag}>", search_area, re.IGNORECASE | re.DOTALL)
        if m:
            t = clean_html_text(m.group(1))
            if t:
                return t

    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", search_area, re.IGNORECASE | re.DOTALL)
    texts = [clean_html_text(p) for p in paragraphs]
    texts = [t for t in texts if t]
    if not texts:
        return ""

    chapter_label = re.match(r"^(Chapter\s+\d+)$", texts[0], re.IGNORECASE)
    if chapter_label and len(texts) >= 2:
        num_match = re.search(r"\d+", texts[0])
        num = f"{int(num_match.group()):02d}" if num_match else ""
        return texts[1]

    return texts[0]


def slugify(text: str, max_len: int = 60) -> str:
    text = html_module.unescape(text)
    text = re.sub(r"\(p\.\s*\d+\)", "", text)
    text = re.sub(r"[\u00a0\s]+", " ", text)
    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:max_len]


def build_output_filename(idx: int, item_id: str, internal_path: str, html_bytes: bytes) -> str:
    title = extract_title_from_html(html_bytes)
    slug = slugify(title) if title else item_id
    chapter_num = (
        extract_chapter_number_from_html(html_bytes)
        or extract_chapter_number_from_path(internal_path)
    )
    if chapter_num is not None:
        return f"{idx:03d}_ch{chapter_num:02d}_{slug}.md"
    return f"{idx:03d}_{slug}.md"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def strip_namespaces(root: ET.Element) -> None:
    for element in root.iter():
        if isinstance(element.tag, str):
            element.tag = local_name(element.tag)
        renamed = {}
        for key, value in element.attrib.items():
            renamed[local_name(key)] = value
        element.attrib.clear()
        element.attrib.update(renamed)


def text_content(element: ET.Element) -> str:
    return "".join(element.itertext())


def clean_code_line(raw: str) -> str:
    trimmed = raw.strip(" \t\r\n")
    leading = re.match(r"^[\u00a0 ]+", trimmed)
    if leading and "\u00a0" in leading.group(0):
        prefix = " " * leading.group(0).count("\u00a0")
        rest = trimmed[len(leading.group(0)):]
        return (prefix + rest.replace("\u00a0", " ")).rstrip()
    return trimmed.replace("\u00a0", " ").rstrip()


def normalize_google_redirect(href: str) -> str:
    parsed = urllib.parse.urlparse(href)
    if parsed.netloc in {"google.com", "www.google.com"} and parsed.path == "/url":
        query = urllib.parse.parse_qs(parsed.query)
        if query.get("q"):
            return query["q"][0]
    return href


def strip_presentation_attributes(root: ET.Element) -> None:
    for element in root.iter():
        kept = {}
        for key, value in element.attrib.items():
            if element.tag == "a" and key == "href":
                kept[key] = normalize_google_redirect(value)
            elif element.tag == "img" and key in {"src", "alt", "title"}:
                kept[key] = value
            elif element.tag == "ol" and key == "start":
                kept[key] = value
            elif element.tag in {"td", "th"} and key in {"colspan", "rowspan"}:
                kept[key] = value
            elif element.tag == "code" and key == "class":
                kept[key] = value
        element.attrib.clear()
        element.attrib.update(kept)


def add_text_at(parent: ET.Element, index: int, text: str | None) -> None:
    if not text:
        return
    if index == 0:
        parent.text = (parent.text or "") + text
        return
    previous = list(parent)[index - 1]
    previous.tail = (previous.tail or "") + text


def unwrap_child(parent: ET.Element, index: int) -> None:
    children = list(parent)
    child = children[index]
    grandchildren = list(child)
    tail = "" if child.tail and not child.tail.strip() else (child.tail or "")

    parent.remove(child)
    add_text_at(parent, index, child.text)

    for offset, grandchild in enumerate(grandchildren):
        parent.insert(index + offset, grandchild)

    add_text_at(parent, index + len(grandchildren), tail)


def unwrap_tags(parent: ET.Element, tags: set[str]) -> None:
    for child in list(parent):
        unwrap_tags(child, tags)

    index = 0
    while index < len(parent):
        child = list(parent)[index]
        if child.tag in tags:
            unwrap_child(parent, index)
        else:
            index += 1


def lines_from_single_cell_table(table: ET.Element) -> list[str] | None:
    cells = [element for element in table.iter() if element.tag in {"td", "th"}]
    if len(cells) != 1:
        return None

    paragraphs = [element for element in cells[0].iter() if element.tag == "p"]
    if paragraphs:
        return [clean_code_line(text_content(paragraph)) for paragraph in paragraphs]

    raw = text_content(cells[0])
    return [clean_code_line(line) for line in raw.splitlines()]


def looks_like_code(lines: list[str]) -> bool:
    non_empty = [line.strip() for line in lines if line.strip()]
    if not non_empty:
        return False
    if len(non_empty) > 1:
        return True

    line = non_empty[0]
    command_prefixes = ("pip ", "uv ", "python ", "npm ", "git ", "docker ", "kubectl ", "helm ", "curl ")
    return line.startswith(command_prefixes) or line[0] in "{[<" or "=" in line


def infer_code_language(lines: list[str]) -> str:
    non_empty = [line.strip() for line in lines if line.strip()]
    if not non_empty:
        return ""

    first = non_empty[0]
    joined = "\n".join(non_empty)
    if first.startswith("{") or first.startswith("["):
        return "json"
    if re.search(r"^(from\s+\w+|import\s+\w+|def\s+\w+|class\s+\w+)", joined, re.MULTILINE):
        return "python"
    if first.startswith(("pip ", "uv ", "python ", "npm ", "git ", "docker ", "kubectl ", "helm ", "curl ")):
        return "bash"
    return ""


def replace_code_tables(parent: ET.Element) -> None:
    for child in list(parent):
        replace_code_tables(child)

    index = 0
    while index < len(parent):
        child = list(parent)[index]
        if child.tag != "table":
            index += 1
            continue

        lines = lines_from_single_cell_table(child)
        if lines is None or not looks_like_code(lines):
            index += 1
            continue

        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        pre = ET.Element("pre")
        code = ET.SubElement(pre, "code")
        language = infer_code_language(lines)
        if language:
            code.set("class", f"language-{language}")
        code.text = "\n".join(lines) + "\n"
        pre.tail = child.tail

        parent.remove(child)
        parent.insert(index, pre)
        index += 1


def remove_empty_paragraphs(parent: ET.Element) -> None:
    for child in list(parent):
        remove_empty_paragraphs(child)

    for child in list(parent):
        if child.tag != "p":
            continue
        has_media = any(descendant.tag in {"img", "video", "audio"} for descendant in child.iter())
        if not has_media and not text_content(child).strip():
            parent.remove(child)


def normalize_html(html_bytes: bytes) -> str:
    raw = html_bytes.decode("utf-8", errors="replace")
    root = ET.fromstring(raw)
    strip_namespaces(root)
    replace_code_tables(root)
    unwrap_tags(root, {"span"})
    remove_empty_paragraphs(root)
    strip_presentation_attributes(root)
    return ET.tostring(root, encoding="unicode", method="html")


def fallback_normalize_html(html_bytes: bytes) -> str:
    text = html_bytes.decode("utf-8", errors="replace")
    text = re.sub(r"</?span\b[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+(class|id|style)=\"[^\"]*\"", "", text, flags=re.IGNORECASE)
    return text


def postprocess_markdown(markdown: str) -> str:
    markdown = markdown.replace("\xa0", " ")
    markdown = re.sub(r"</?span\b[^>]*>", "", markdown, flags=re.IGNORECASE)
    markdown = re.sub(r"\s*\{#[^}]+}", "", markdown)
    markdown = re.sub(r"\s*\{\.[^}]+}", "", markdown)
    markdown = re.sub(r"^``` ([A-Za-z0-9_-]+)$", r"```\1", markdown, flags=re.MULTILINE)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip() + "\n"


def html_to_markdown(html_bytes: bytes) -> str:
    try:
        normalized_html = normalize_html(html_bytes)
    except ET.ParseError:
        normalized_html = fallback_normalize_html(html_bytes)

    result = subprocess.run(
        [
            "pandoc",
            "-f", "html",
            "-t", PANDOC_TO,
            "--wrap=none",
            "--markdown-headings=atx",
        ],
        input=normalized_html,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return postprocess_markdown(result.stdout)


def extract_and_convert(epub_path: Path, spine_items: list, output_dir: Path):
    with zipfile.ZipFile(epub_path) as z:
        for idx, item_id, internal_path in spine_items:
            try:
                html_bytes = z.read(internal_path)
            except KeyError:
                print(f"  [SKIP] 找不到: {internal_path}")
                continue

            out_md = output_dir / build_output_filename(idx, item_id, internal_path, html_bytes)

            try:
                markdown = html_to_markdown(html_bytes)
                out_md.write_text(markdown, encoding="utf-8")
            except (RuntimeError, FileNotFoundError) as error:
                print(f"  [ERR] {item_id}: {error}")
                continue

            print(f"  [OK] {out_md.name}")


def main():
    args = parse_args()

    epub_path: Path = args.epub
    if not epub_path.exists():
        raise SystemExit(f"错误：找不到文件 {epub_path}")

    output_dir: Path = args.output or Path(f"{epub_path.stem}_chapters")
    output_dir.mkdir(parents=True, exist_ok=True)

    spine = get_spine_order(epub_path)
    print(f"共找到 {len(spine)} 个章节，输出到 {output_dir}/")
    extract_and_convert(epub_path, spine, output_dir)
    print("\n完成！")


if __name__ == "__main__":
    main()
