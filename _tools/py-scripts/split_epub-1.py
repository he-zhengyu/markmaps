#!/usr/bin/env python3
# split_epub.py
import argparse
import html as html_module
import re
import subprocess
import urllib.parse
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
            # href may be URL-encoded in OPF while zip stores decoded names (or vice versa)
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

    # Strategy 1: semantic <section data-type="..."> → inner heading
    section_match = re.search(r'<section[^>]+data-type="([^"]+)"[^>]*>(.*?)</section>',
                               search_area, re.IGNORECASE | re.DOTALL)
    if section_match:
        section_body = section_match.group(2)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", section_body, re.IGNORECASE | re.DOTALL)
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", section_body, re.IGNORECASE | re.DOTALL)
        heading = clean_html_text(h1.group(1)) if h1 else (clean_html_text(h2.group(1)) if h2 else "")
        if heading:
            return heading

    # Strategy 2: first <h1>/<h2> anywhere
    for tag in ["h1", "h2"]:
        m = re.search(fr"<{tag}[^>]*>(.*?)</{tag}>", search_area, re.IGNORECASE | re.DOTALL)
        if m:
            t = clean_html_text(m.group(1))
            if t:
                return t

    # Strategy 3: "Chapter N" label + title spread across two <p> tags
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", search_area, re.IGNORECASE | re.DOTALL)
    texts = [clean_html_text(p) for p in paragraphs]
    texts = [t for t in texts if t]
    if not texts:
        return ""

    chapter_label = re.match(r"^(Chapter\s+\d+)$", texts[0], re.IGNORECASE)
    if chapter_label and len(texts) >= 2:
        num_match = re.search(r"\d+", texts[0])
        num = f"{int(num_match.group()):02d}" if num_match else ""
        return f"Ch{num}_{texts[1]}"

    # Strategy 4: fallback — first non-empty <p>
    return texts[0]


def slugify(text: str, max_len: int = 60) -> str:
    text = html_module.unescape(text)            # &amp; -> &, &#160; -> NBSP
    text = re.sub(r"\(p\.\s*\d+\)", "", text)
    text = re.sub(r"[\u00a0\s]+", " ", text)      # normalize NBSP + whitespace
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


def extract_and_convert(epub_path: Path, spine_items: list, output_dir: Path):
    with zipfile.ZipFile(epub_path) as z:
        for idx, item_id, internal_path in spine_items:
            try:
                html_bytes = z.read(internal_path)
            except KeyError:
                print(f"  [SKIP] 找不到: {internal_path}")
                continue

            out_md = output_dir / build_output_filename(idx, item_id, internal_path, html_bytes)

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
