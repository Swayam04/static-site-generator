from typing import Optional, List, Dict

class HTMLNode:
    def __init__(self,
                 tag: Optional[str] = None,
                 value: Optional[str] = None,
                 children: Optional[List["HTMLNode"]] = None,
                 props: Optional[Dict[str, str]] = None
                ) -> None:
        self.tag = tag
        self.value = value
        self.children: List["HTMLNode"] = children if children is not None else []
        self.props: Dict[str, str] = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError('Abstract Method')

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{val}"' for key, val in self.props.items())

    def __repr__(self) -> str:
        parts = []
        if self.tag is not None:
            parts.append(f"tag='{self.tag}'")
        if self.value is not None:
            display_value = self.value if len(self.value) < 20 else self.value[:17] + "..."
            parts.append(f"value='{display_value}'")
        if self.children:
            parts.append(f"children=<{len(self.children)} nodes>")
        if self.props:
            parts.append(f"props={len(self.props)} items")
        return f"HTMLNode({', '.join(parts)})"
    
    def open_tag(self):
        if not self.tag:
            if self.props:
                raise ValueError("Props cannot exist without a tag.")
            return ""
        return f"<{self.tag}{self.props_to_html()}>"
    
    def close_tag(self):
        if not self.tag:
            return ""
        return f"</{self.tag}>"

    def __to_string(self, indent_level: int = 0) -> str:
        indent = '   ' * indent_level
        inner_indent = '   ' * (indent_level + 1)

        props_html = self.props_to_html()
        lines = []

        if self.tag:
            lines.append(f"{indent}<{self.tag}{props_html}>")
        else:
            if self.value is not None:
                lines.append(f"{indent}{self.value}")

        if self.tag and self.value is not None:
            lines.append(f"{inner_indent}{self.value}")

        for child in self.children:
            lines.append(child.__to_string(indent_level + 1))

        if self.tag:
            lines.append(f"{indent}</{self.tag}>")

        return "\n".join(lines)