from enum import Enum
from typing import Optional

class TextType(Enum):
    TEXT = 'text'
    BOLD = '**bold**'
    ITALIC = '_italics_'
    CODE = '`code`'
    LINK = '[anchor text](url)'
    IMAGE = '[alt text](url)'
    
class TextNode:
    
    def __init__(self, 
                 text : str, 
                 text_type : TextType, 
                 url: Optional[str] = None
                ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"