#!/usr/bin/env python3
"""
Extract hierarchical bookmarks from a PDF file.

Usage:
    python extract_bookmarks.py <path_to_pdf>
    python extract_bookmarks.py <path_to_pdf> --output bookmarks.txt
    python extract_bookmarks.py <path_to_pdf> --format json
    python extract_bookmarks.py <path_to_pdf> --format markdown
    python extract_bookmarks.py <path_to_pdf> --format yaml

Output formats:
    text     - Indented plain text (default)
    markdown - Markdown with # headings
    json     - JSON array (flat, with level field)
    yaml     - YAML nested tree
"""

import sys
import json
import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf is not installed. Run:  pip install pypdf")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Recursive bookmark extraction
# ---------------------------------------------------------------------------

def extract_bookmarks(outlines, reader, level=0):
    """
    Recursively walk the PDF outline tree and return a flat list of dicts:
        { title, page, level }
    """
    results = []

    for item in outlines:
        if isinstance(item, list):
            # Nested list → children are one level deeper than their parent
            results.extend(extract_bookmarks(item, reader, level + 1))
        else:
            # Resolve page number (1-based); gracefully handle failures
            page_num = None
            try:
                if item.page is not None:
                    page_num = reader.get_destination_page_number(item) + 1
            except Exception:
                pass

            results.append({
                "title": item.title.strip() if item.title else "(untitled)",
                "page":  page_num,
                "level": level,
            })

            # If this bookmark has children they appear as the *next* element
            # in the outline list (a sub-list), handled by the loop above.

    return results


def get_bookmarks(pdf_path):
    """Open the PDF and return the bookmark list."""
    reader = PdfReader(str(pdf_path))

    if not reader.outline:
        return []

    return extract_bookmarks(reader.outline, reader, level=0)


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(bookmarks):
    """Indented plain-text tree."""
    lines = []
    for bm in bookmarks:
        indent = "  " * bm["level"]
        page   = f"  (p. {bm['page']})" if bm["page"] is not None else ""
        lines.append(f"{indent}{bm['title']}{page}")
    return "\n".join(lines)


def format_markdown(bookmarks):
    """Markdown headings (level 0 → #, level 1 → ##, …, capped at ######)."""
    lines = []
    for bm in bookmarks:
        hashes = "#" * min(bm["level"] + 1, 6)
        page   = f" *(p. {bm['page']})*" if bm["page"] is not None else ""
        lines.append(f"{hashes} {bm['title']}{page}")
    return "\n".join(lines)


def format_json(bookmarks):
    """JSON array of bookmark objects."""
    return json.dumps(bookmarks, indent=2, ensure_ascii=False)


def _bookmarks_to_tree(bookmarks):
    """Convert flat bookmark list into a nested tree for YAML output."""
    root = []
    stack = []  # list of (level, children_list)

    for bm in bookmarks:
        node = {"title": bm["title"]}
        if bm["page"] is not None:
            node["page"] = bm["page"]

        while stack and stack[-1][0] >= bm["level"]:
            stack.pop()

        target = stack[-1][1] if stack else root
        target.append(node)
        children = []
        node["children"] = children
        stack.append((bm["level"], children))

    def prune(nodes):
        for node in nodes:
            if not node["children"]:
                del node["children"]
            else:
                prune(node["children"])

    prune(root)
    return root


def format_yaml(bookmarks):
    """YAML nested tree."""
    try:
        import yaml
    except ImportError:
        print("Error: pyyaml is not installed. Run:  pip install pyyaml")
        sys.exit(1)

    class IndentedDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow=flow, indentless=False)

    return yaml.dump(
        _bookmarks_to_tree(bookmarks),
        Dumper=IndentedDumper,
        allow_unicode=True,
        sort_keys=False,
    )


FORMATTERS = {
    "text":     format_text,
    "markdown": format_markdown,
    "json":     format_json,
    "yaml":     format_yaml,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract hierarchical bookmarks from a PDF file."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--output", "-o",
        help="Write output to this file instead of printing to stdout",
    )
    parser.add_argument(
        "--format", "-f",
        choices=list(FORMATTERS.keys()),
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}")
        sys.exit(1)
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Warning: file does not have a .pdf extension: {pdf_path}")

    print(f"Reading: {pdf_path}", file=sys.stderr)
    bookmarks = get_bookmarks(pdf_path)

    if not bookmarks:
        print("No bookmarks found in this PDF.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(bookmarks)} bookmarks.", file=sys.stderr)

    output_text = FORMATTERS[args.format](bookmarks)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(output_text, encoding="utf-8")
        print(f"Saved to: {out_path}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()