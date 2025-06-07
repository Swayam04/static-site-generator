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
        
    def test_sinle_link(self):
        text = 'Visit my [website](https://www.example.com)'
        res = extract_markdown_links(text)
        self.assertListEqual([('website', 'https://www.example.com')], res)
    
    def test_single_image(self):
        text = 'Visit my ![image](/path/to/my/image.jpg)'
        res = extract_markdown_images(text)
        self.assertListEqual([('image', '/path/to/my/image.jpg')], res)
    
    def test_multiple_links(self):
        text2 = "See [Page One](/page1.html) or [Google](http://google.com)."
        res = extract_markdown_links(text2)
        self.assertListEqual([('Page One', '/page1.html'), ('Google', 'http://google.com')], res)
        
    def test_multiple_images(self):
        text2 = "See ![Image](/photo.jpg) or ![WebImage](http://imgur.com/lotr.jpg)."
        res = extract_markdown_images(text2)
        self.assertListEqual([('Image', '/photo.jpg'), ('WebImage', 'http://imgur.com/lotr.jpg')], res)
    
    def test_no_match_link(self):
        text = 'Visit my ![image](/path/to/my/image.jpg)'
        res = extract_markdown_links(text)
        self.assertListEqual([], res)
    
    def test_no_match_image(self):
        text = 'Visit my [website](https://www.example.com)'
        res = extract_markdown_images(text)
        self.assertListEqual([], res)
        