import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("i", "Hello")
        node = ParentNode("", [child_node])
        with self.assertRaisesRegex(ValueError, "Tag is mandatory for parent nodes."):
            node.to_html()
    
    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "A parent node must have at least one child node."):
            node.to_html()
            
    def test_to_html_with_props(self):
        child_node = LeafNode("p", "Hello")
        props = {"class": "text", "id": "main"}
        parent_node = ParentNode("div", [child_node], props)
        self.assertEqual(
            parent_node.to_html(),
            '<div class="text" id="main"><p>Hello</p></div>'
        )
    
    def test_to_html_with_mixed_children(self):
        child1 = LeafNode("em", "Italic")
        child2 = ParentNode("span", [LeafNode("strong", "Bold")])
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><em>Italic</em><span><strong>Bold</strong></span></div>"
        )

    
    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "Deep content")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>Deep content</p></article></section></div>"
        )



        
            
        