#!/usr/bin/env python3
# split_epub.py
import argparse
import re
import subprocess
import zipfile
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Split an EPUB into per-chapter Markdown files")
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
        container = z.read("META-INF/container.xml").decode()
        opf_path = re.search(r'full-path="([^"]+\.opf)"', container).group(1)
        opf_content = z.read(opf_path).decode()
        opf_dir = str(Path(opf_path).parent)

        manifest = dict(re.findall(r'id="([^"]+)"[^>]+href="([^"]+\.x?html?)"', opf_content))
        spine_ids = re.findall(r'<itemref\s+idref="([^"]+)"', opf_content)

        result = []
        for i, item_id in enumerate(spine_ids):
            if item_id in manifest:
                href = manifest[item_id]
                full_path = f"{opf_dir}/{href}" if opf_dir and opf_dir != "." else href
                result.append((i + 1, item_id, full_path))
        return result


# def extract_title_from_html(html_bytes: bytes) -> str:
#     html = html_bytes.decode("utf-8", errors="replace")

#     # This epub uses <p class="..."> for titles, not <h1>/<h2>
#     # The first <p> in the body is always the chapter/section title
#     body_match = re.search(r"<body[^>]*>(.*)", html, re.IGNORECASE | re.DOTALL)
#     search_area = body_match.group(1) if body_match else html

#     m = re.search(r"<p[^>]*>(.*?)</p>", search_area, re.IGNORECASE | re.DOTALL)
#     if m:
#         raw = re.sub(r"<[^>]+>", "", m.group(1))
#         title = re.sub(r"\s+", " ", raw).strip()
#         if title:
#             return title

#     return ""

# def extract_title_from_html(html_bytes: bytes) -> str:
#     html = html_bytes.decode("utf-8", errors="replace")

#     body_match = re.search(r"<body[^>]*>(.*)", html, re.IGNORECASE | re.DOTALL)
#     search_area = body_match.group(1) if body_match else html

#     # Collect first few <p> tags to inspect
#     paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", search_area, re.IGNORECASE | re.DOTALL)
#     texts = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", p)).strip() for p in paragraphs]
#     texts = [t for t in texts if t]  # drop empty

#     if not texts:
#         return ""

#     # Detect chapter heading pattern: first <p> is "Chapter N" or "Preface" etc.,
#     # second <p> is the subtitle → join them
#     chapter_line = re.match(r"^(Chapter\s+\d+|Preface|Introduction|Conclusion|Index|Appendix.*)$", texts[0], re.IGNORECASE)
#     if chapter_line and len(texts) >= 2:
#         # e.g. "Chapter 1" + "Introduction" → "Ch01_Introduction"
#         num_match = re.search(r"\d+", texts[0])
#         num = f"{int(num_match.group()):02d}" if num_match else ""
#         prefix = f"Ch{num}" if num else texts[0]
#         return f"{prefix}_{texts[1]}"

#     # Fallback: just use first non-empty paragraph
#     return texts[0]

def extract_title_from_html(html_bytes: bytes) -> str:
    html = html_bytes.decode("utf-8", errors="replace")

    body_match = re.search(r"<body[^>]*>(.*)", html, re.IGNORECASE | re.DOTALL)
    search_area = body_match.group(1) if body_match else html

    def clean(raw: str) -> str:
        text = re.sub(r"<[^>]+>", "", raw)
        return re.sub(r"\s+", " ", text).strip()

    # Strategy 1: semantic section type via data-type attribute
    # e.g. <section data-type="chapter"> → look for <h1> inside
    section_match = re.search(r'<section[^>]+data-type="([^"]+)"[^>]*>(.*?)</section>',
                               search_area, re.IGNORECASE | re.DOTALL)
    if section_match:
        section_type = section_match.group(1)   # "chapter", "preface", etc.
        section_body = section_match.group(2)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", section_body, re.IGNORECASE | re.DOTALL)
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", section_body, re.IGNORECASE | re.DOTALL)
        heading = clean(h1.group(1)) if h1 else (clean(h2.group(1)) if h2 else "")
        if heading:
            return heading

    # Strategy 2: <h1> / <h2> anywhere in body (standard epub)
    for tag in ["h1", "h2"]:
        m = re.search(fr"<{tag}[^>]*>(.*?)</{tag}>", search_area, re.IGNORECASE | re.DOTALL)
        if m:
            t = clean(m.group(1))
            if t:
                return t

    # Strategy 3: Philosophy-of-SD pattern — first <p> is chapter label,
    # second <p> is chapter title; join only when first <p> matches "Chapter N"
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", search_area, re.IGNORECASE | re.DOTALL)
    texts = [clean(p) for p in paragraphs]
    texts = [t for t in texts if t]

    if not texts:
        return ""

    chapter_label = re.match(r"^(Chapter\s+\d+)$", texts[0], re.IGNORECASE)
    if chapter_label and len(texts) >= 2:
        num_match = re.search(r"\d+", texts[0])
        num = f"{int(num_match.group()):02d}" if num_match else ""
        return f"Ch{num}_{texts[1]}"

    # Strategy 4: fallback — first <p> only (Preface, Index, etc.)
    return texts[0]

def slugify(text: str, max_len: int = 60) -> str:
    """Convert a title to a safe filename slug."""
    # Remove page references like "(p. 157)"
    text = re.sub(r"\(p\.\s*\d+\)", "", text)
    # Keep alphanumerics, spaces, hyphens
    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:max_len]


def extract_and_convert(epub_path: Path, spine_items: list, output_dir: Path):
    with zipfile.ZipFile(epub_path) as z:
        for idx, item_id, internal_path in spine_items:
            try:
                html_bytes = z.read(internal_path)
            except KeyError:
                print(f"  [SKIP] 找不到: {internal_path}")
                continue

            title = extract_title_from_html(html_bytes)
            slug = slugify(title) if title else item_id
            out_md = output_dir / f"{idx:03d}_{slug}.md"

            tmp_html = Path(f"/tmp/_split_epub_{idx:03d}.html")
            tmp_html.write_bytes(html_bytes)

            result = subprocess.run(
                ["pandoc", str(tmp_html), "-f", "html", "-t", "markdown",
                 "--wrap=none", "-o", str(out_md)],
                capture_output=True, text=True,
            )

            tmp_html.unlink()

            if result.returncode == 0:
                print(f"  [OK] {out_md.name}")
            else:
                print(f"  [ERR] {item_id}: {result.stderr.strip()}")


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