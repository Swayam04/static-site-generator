from htmlnode import HTMLNode
import unittest

node_leaf_simple = HTMLNode(tag="p", value="This is a simple paragraph.")

node_leaf_with_props = HTMLNode(
    tag="a",
    value="Click Me",
    props={"href": "https://example.com", "target": "_blank"}
)

node_raw_text = HTMLNode(value="Just some raw text content.")

node_empty = HTMLNode()
node_empty_with_props = HTMLNode(props={"data-empty": "true"})


node_only_value = HTMLNode(tag="span", value="Just a value here.")

class TestHTMLNode(unittest.TestCase):
    
    def test_props_func(self):
        self.assertEqual(node_leaf_with_props.props_to_html(), ' href="https://example.com" target="_blank"')
        self.assertEqual(node_leaf_simple.props_to_html(), '')
    
    def test_simple_node(self):
        expected_html = "HTMLNode(tag='p', value='This is a simple ...')"
        self.assertEqual(expected_html, repr(node_leaf_simple))
        
    def test_to_string_empty_node(self):
        self.assertEqual(repr(node_empty), "HTMLNode()")

    def test_to_string_empty_node_with_props(self):
        self.assertEqual(repr(node_empty_with_props), "HTMLNode(props=1 items)")