from typing import Dict, List, Optional
from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    
    def __init__(self, 
                 tag: str, 
                 children: List[HTMLNode], 
                 props: Optional[Dict[str, str]] = None
                ) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is mandatory for parent nodes.")
        elif not self.children:
            raise ValueError("A parent node must have at least one child node.")
        
        nodes : List[str] = []
        nodes.append(self.open_tag())
        nodes.extend(child.to_html() for child in self.children)
        nodes.append(self.close_tag())
        
        return "".join(nodes)
        