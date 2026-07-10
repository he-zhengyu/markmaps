import importlib.util
from pathlib import Path
import shutil
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "split_epub-2.py"
spec = importlib.util.spec_from_file_location("split_epub_2", SCRIPT_PATH)
split_epub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(split_epub)


@unittest.skipUnless(shutil.which("pandoc"), "pandoc is required for markdown conversion")
class CleanMarkdownTests(unittest.TestCase):
    def test_google_doc_spans_are_removed_without_splitting_words(self):
        html = b"""
        <html xmlns="http://www.w3.org/1999/xhtml"><body>
          <p class="c3">
            <span class="c4">The core idea uses smaller s</span>
            <span class="c4">ub-prob</span>
            <span class="c4">lems.</span>
          </p>
        </body></html>
        """

        markdown = split_epub.html_to_markdown(html)

        self.assertIn("smaller sub-problems.", markdown)
        self.assertNotIn("<span", markdown)
        self.assertNotIn("{.c", markdown)

    def test_single_cell_code_tables_become_fenced_code_blocks(self):
        html = b"""
        <html xmlns="http://www.w3.org/1999/xhtml"><body>
          <table class="c13"><tbody><tr><td>
            <p>
              <span class="c17">import os</span>
            </p>
            <p>
              <span class="c17">from langchain_openai import ChatOpenAI</span>
            </p>
            <p>
              <span class="c17">&#160; &#160;llm = ChatOpenAI(temperature=0)</span>
            </p>
          </td></tr></tbody></table>
        </body></html>
        """

        markdown = split_epub.html_to_markdown(html)

        self.assertIn("```python\nimport os\nfrom langchain_openai import ChatOpenAI\n  llm = ChatOpenAI", markdown)
        self.assertIn("from langchain_openai import ChatOpenAI", markdown)
        self.assertNotIn("| import os |", markdown)

    def test_google_redirect_links_are_unwrapped(self):
        html = b"""
        <html xmlns="http://www.w3.org/1999/xhtml"><body>
          <p>
            <a href="https://www.google.com/url?q=https://example.com/docs&amp;sa=D">
              Example Docs
            </a>
          </p>
        </body></html>
        """

        markdown = split_epub.html_to_markdown(html)

        self.assertIn("[Example Docs](https://example.com/docs)", markdown)
        self.assertNotIn("google.com/url", markdown)


class OutputFilenameTests(unittest.TestCase):
    def test_chapter_file_uses_real_chapter_number_as_prefix(self):
        html = b"""
        <html><body>
          <p><span>Chapter 1: Prompt </span><span>Chaining</span></p>
          <h1>Prompt Chaining Pattern Overview</h1>
        </body></html>
        """

        name = split_epub.build_output_filename(
            9,
            "a7main",
            "7/GoogleDoc/Chapter1PromptChaining.xhtml",
            html,
        )

        self.assertEqual(name, "009_ch01_Prompt_Chaining_Pattern_Overview.md")


if __name__ == "__main__":
    unittest.main()
