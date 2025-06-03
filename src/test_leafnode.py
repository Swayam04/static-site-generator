import unittest
from leafnode import *
from textnode import TextNode, TextType

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Link</a>')
    
    def test_leaf_to_html_plain(self):
        node = LeafNode(None, "Hello!")
        self.assertEqual(node.to_html(), "Hello!")

class TestTextToHTML(unittest.TestCase):
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link_text_with_url(self):
        node = TextNode("LOTR", TextType.LINK, url="https://lordoftherings.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "LOTR")
        self.assertEqual(html_node.props, {"href": "https://lordoftherings.com"})

    def test_link_text_missing_url(self):
        node = TextNode("LOTR", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("URL mandatory", str(context.exception))

    def test_image_with_url(self):
        node = TextNode("LOTR poster", TextType.IMAGE, url="poster.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "poster.png", "alt": "LOTR poster"})

    def test_image_missing_url(self):
        node = TextNode("Missing poster", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Source URL mandatory", str(context.exception))