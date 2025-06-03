from typing import Dict, List, Optional
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    
    def __init__(self, 
                 tag: Optional[str], 
                 value: str,
                 props: Optional[Dict[str, str]] = None
                ) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError('Value attribute mandatory for leaf nodes')
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    