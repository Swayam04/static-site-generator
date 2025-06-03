import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq1(self):
        node = TextNode("text1", TextType.BOLD)
        node2 = TextNode("text1", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("text1", TextType.BOLD)
        node2 = TextNode("text2", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_not_eq3(self):
        node = TextNode("text1", TextType.BOLD, 'https://www.example.com')
        node2 = TextNode("text1", TextType.BOLD, 'https://www.example.org')
        self.assertNotEqual(node, node2)
    
    def test_url_isCorrect(self):
        node = TextNode("text1", TextType.TEXT)
        node2 = TextNode("text2", TextType.TEXT, 'https://www.example.com')
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)
    
    def test_repr(self):
        node2 = TextNode("text2", TextType.TEXT, 'https://www.example.com')
        self.assertEqual("TextNode(text2, text, https://www.example.com)", repr(node2))



if __name__ == "__main__":
    unittest.main()