from typing import Dict, Optional
from htmlnode import HTMLNode
from textnode import TextNode, TextType

class LeafNode(HTMLNode):
    
    def __init__(self, 
                 tag: Optional[str], 
                 value: str,
                 props: Optional[Dict[str, str]] = None
                ) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError('Value attribute mandatory for leaf nodes')
        return f"{self.open_tag()}{self.value}{self.close_tag()}"


 
def text_node_to_html_node(text_node : TextNode) -> HTMLNode:
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        else:
            raise ValueError("URL mandatory for links")
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        else:
            raise ValueError("Source URL mandatory for Image tags")
    else:
        raise ValueError("Unknown TextNode type")
    