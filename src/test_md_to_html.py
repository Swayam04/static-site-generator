import unittest

from md_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph(self):
        markdown = "This is a simple paragraph."
        node = markdown_to_html_node(markdown)
        expected_html = "<div><p>This is a simple paragraph.</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_multiple_paragraphs(self):
        markdown = """
This is the first paragraph.

This is the second paragraph, with _italic_ text.
"""
        node = markdown_to_html_node(markdown)
        expected_html = "<div><p>This is the first paragraph.</p><p>This is the second paragraph, with <i>italic</i> text.</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_heading(self):
        markdown = "## This is an H2"
        node = markdown_to_html_node(markdown)
        expected_html = "<div><h2>This is an H2</h2></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_blockquote(self):
        markdown = "> This is a quote.\n> It has two lines."
        node = markdown_to_html_node(markdown)
        expected_html = "<div><blockquote>This is a quote.\nIt has two lines.</blockquote></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_unordered_list(self):
        markdown = "- First item\n- Second item\n- Third item"
        node = markdown_to_html_node(markdown)
        expected_html = "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item"
        node = markdown_to_html_node(markdown)
        expected_html = "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_code_block(self):
        markdown = "```python\ndef my_func():\n    return 42\n```"
        node = markdown_to_html_node(markdown)
        expected_html = "<div><pre><code>def my_func():\n    return 42</code></pre></div>"
        self.assertEqual(node.to_html(), expected_html)
        
    def test_full_document(self):
        markdown = """
# My Document

This is the introduction. It contains `code` and **bold** text.

## A List of Items

* Item one
* Item two with a [link](https://example.com)

> A concluding thought.

"""
        node = markdown_to_html_node(markdown)
        expected_html = (
            "<div>"
            "<h1>My Document</h1>"
            "<p>This is the introduction. It contains <code>code</code> and <b>bold</b> text.</p>"
            "<h2>A List of Items</h2>"
            "<ul><li>Item one</li><li>Item two with a <a href=\"https://example.com\">link</a></li></ul>"
            "<blockquote>A concluding thought.</blockquote>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected_html)

if __name__ == '__main__':
    unittest.main()