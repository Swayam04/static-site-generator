from blocktype import block_to_blocktype, BlockType
import unittest

class BlockTypeTest(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a standard paragraph."
        self.assertEqual(block_to_blocktype(block), BlockType.paragraph)

        block_multi = "This is a paragraph\nthat spans multiple lines\nwithout any special markers."
        self.assertEqual(block_to_blocktype(block_multi), BlockType.paragraph)

    def test_heading(self):
        block_h1 = "# This is a heading 1"
        self.assertEqual(block_to_blocktype(block_h1), BlockType.heading)

        block_h6 = "###### This is a heading 6"
        self.assertEqual(block_to_blocktype(block_h6), BlockType.heading)

    def test_invalid_heading(self):
        block_multi_line = "# This is a heading\nbut it has two lines."
        self.assertEqual(block_to_blocktype(block_multi_line), BlockType.paragraph)
        
        block_too_many_hashes = "####### Not a heading"
        self.assertEqual(block_to_blocktype(block_too_many_hashes), BlockType.paragraph)

    def test_code_block(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.code)

        block_with_lang = "```python\nimport os\npass\n```"
        self.assertEqual(block_to_blocktype(block_with_lang), BlockType.code)

    def test_invalid_code_block(self):
        block_no_close = "```\nprint('This will not work')"
        self.assertEqual(block_to_blocktype(block_no_close), BlockType.paragraph)

        block_single_line = "```print('hello')```"
        self.assertEqual(block_to_blocktype(block_single_line), BlockType.paragraph)

    def test_quote_block(self):
        block_single = "> To be or not to be"
        self.assertEqual(block_to_blocktype(block_single), BlockType.quote)

        block_multi = "> This is the first line.\n> This is the second."
        self.assertEqual(block_to_blocktype(block_multi), BlockType.quote)
        
    def test_invalid_quote_block(self):
        block_mixed = "> This is a quote.\nThis line is not."
        self.assertEqual(block_to_blocktype(block_mixed), BlockType.paragraph)

    def test_unordered_list(self):
        block_dash = "- Red\n- Green\n- Blue"
        self.assertEqual(block_to_blocktype(block_dash), BlockType.unordered_list)
        
        block_star = "* Red\n* Green\n* Blue"
        self.assertEqual(block_to_blocktype(block_star), BlockType.unordered_list)

        block_mixed = "- Red\n* Green"
        self.assertEqual(block_to_blocktype(block_mixed), BlockType.unordered_list)

    def test_invalid_unordered_list(self):
        block_mixed = "- A list item\nAnd a normal paragraph line"
        self.assertEqual(block_to_blocktype(block_mixed), BlockType.paragraph)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_blocktype(block), BlockType.ordered_list)
        
        block_non_sequential = "1. First item\n5. Fifth item"
        self.assertEqual(block_to_blocktype(block_non_sequential), BlockType.ordered_list)

    def test_invalid_ordered_list(self):
        block_mixed = "1. First item\nThis is not a list item"
        self.assertEqual(block_to_blocktype(block_mixed), BlockType.paragraph)