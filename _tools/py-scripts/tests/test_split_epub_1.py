import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "split_epub-1.py"
spec = importlib.util.spec_from_file_location("split_epub_1", SCRIPT_PATH)
split_epub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(split_epub)


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

    def test_chapter_number_can_fall_back_to_internal_path(self):
        html = b"<html><body><h1>Model Context Protocol (MCP)</h1></body></html>"

        name = split_epub.build_output_filename(
            18,
            "a16main",
            "16/GoogleDoc/Chapter10ModelContextProtocol%28MCP%29.xhtml",
            html,
        )

        self.assertEqual(name, "018_ch10_Model_Context_Protocol_MCP.md")


if __name__ == "__main__":
    unittest.main()
