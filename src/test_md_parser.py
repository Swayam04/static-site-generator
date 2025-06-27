from md_parser import *
import unittest
from textnode import TextNode, TextType

class MDParserTest(unittest.TestCase):
    
    def test_split_nodes_plain_text(self):
        old_nodes = [ 
                     TextNode("This is plain textnode.", TextType.TEXT),
                     TextNode("This is plain textnode 2.", TextType.TEXT)
                    ]
        new_nodes = split_nodes_delimiter(old_nodes, "", TextType.TEXT)
        self.assertEqual(len(old_nodes), len(new_nodes))
        for i in range(len(old_nodes)):
            self.assertEqual(old_nodes[i].text, new_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, TextType.TEXT)
    
    def test_split_no_delimiter_present(self):
        old_nodes = [TextNode("This text has no bold.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [TextNode("This text has no bold.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_single_pair_middle(self):
        old_nodes = [TextNode("This is **bold** text.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_single_pair_start_end(self):
        old_nodes = [TextNode("**Bold text only**", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Bold text only", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_starts_with_delimiter(self):
        old_nodes = [TextNode("**Start bold** and end plain.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Start bold", TextType.BOLD),
            TextNode(" and end plain.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_ends_with_delimiter(self):
        old_nodes = [TextNode("Starts plain and **ends bold**", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Starts plain and ", TextType.TEXT),
            TextNode("ends bold", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_pairs(self):
        old_nodes = [TextNode("This is **one** and **two** bold sections.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" bold sections.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_mixed_node_types(self):
        old_nodes = [
            TextNode("Plain text.", TextType.TEXT),
            TextNode("Existing Bold", TextType.BOLD),
            TextNode("Another plain **with bold**.", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Plain text.", TextType.TEXT),
            TextNode("Existing Bold", TextType.BOLD),
            TextNode("Another plain ", TextType.TEXT),
            TextNode("with bold", TextType.BOLD),
            TextNode(".", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_single_char_delimiter(self):
        old_nodes = [TextNode("This is *italic* text.", TextType.TEXT)]
        delimiter = "*"
        text_type = TextType.ITALIC
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_dollar_delimiter(self):
        old_nodes = [TextNode("Price is $200$.", TextType.TEXT)]
        delimiter = "$"
        text_type = TextType.CODE
        expected_nodes = [
            TextNode("Price is ", TextType.TEXT),
            TextNode("200", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_empty_old_nodes(self):
        old_nodes = []
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.reddit.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.reddit.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_starts_and_ends(self):
        node = TextNode("![Start](a.png)Middle![End](b.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start", TextType.IMAGE, "a.png"),
                TextNode("Middle", TextType.TEXT),
                TextNode("End", TextType.IMAGE, "b.jpg"),
            ],
            new_nodes,
        )

    def test_split_link_empty_content(self):
        node = TextNode("Before [](https://empty.com) After", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://empty.com"),
                TextNode(" After", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_no_matches(self):
        node = TextNode("This has no image syntax.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This has no image syntax.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_malformed_no_paren(self):
        node = TextNode("A link [text] without a url", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("A link [text] without a url", TextType.TEXT)],
            new_nodes,
        )
    
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_multiple_blanks(self):
        md = """Block one.


Block two.



Block three."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one.",
                "Block two.",
                "Block three."
            ],
        )

    def test_markdown_to_blocks_leading_blanks(self):
        md = """

First block.
Second line of first block.

Third block."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block.\nSecond line of first block.",
                "Third block."
            ],
        )

    def test_markdown_to_blocks_trailing_blanks(self):
        md = """First block.
Second line.

Last block.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block.\nSecond line.",
                "Last block."
            ],
        )

    def test_markdown_to_blocks_all_blanks(self):
        md = """

Block A.


Block B.


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block A.",
                "Block B."
            ],
        )

    def test_markdown_to_blocks_single_line(self):
        md = """Line one.

Line two.

Line three."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Line one.",
                "Line two.",
                "Line three."
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    def test_markdown_to_blocks_only_blanks(self):
        md = """

   

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    def test_simple_h1_title(self):
        """Tests a basic case with one H1 title."""
        markdown = """
                    # This is the Title

                    This is some paragraph text.
                    """
        self.assertEqual(extract_title(markdown), "This is the Title")

    def test_finds_first_h1_only(self):
        """Tests that the function returns only the first H1 if multiple exist."""
        markdown = """
                    # The Real Title

                    Some content.

                    ## A Subheading

                    More content.

                    # Another H1 That Should Be Ignored
                    """
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_handles_variable_whitespace(self):
        """Tests that it correctly strips the prefix with multiple spaces."""
        markdown = "#   A Title with extra spaces"
        self.assertEqual(extract_title(markdown), "A Title with extra spaces")

    def test_raises_error_if_no_h1(self):
        """Tests that a ValueError is raised when no H1 exists at all."""
        markdown = "This is a document with no title."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_raises_error_with_other_headings(self):
        """Tests that a ValueError is raised if only H2, H3, etc. exist."""
        markdown = """
                    ## This is not a title

                    ### This is also not a title

                    A paragraph.
                    """
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_ignores_non_heading_hash(self):
        """Tests that a line starting with # but no space is not a title."""
        markdown = "#NotATitle\nSome text here."
        with self.assertRaises(ValueError):
            extract_title(markdown)