from typing import List
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes : List[TextNode], delimiter : str, text_type : TextType) -> List[TextNode]:
    new_nodes = []
    delimiter_len = len(delimiter)
    if delimiter_len == 0:
        return old_nodes

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        stack = []
        text = old_node.text
        i = 0
        current_segment_text = []

        while i < len(text):
            potential_delimiter = text[i : i + delimiter_len]

            if potential_delimiter == delimiter:
                if current_segment_text:
                    if not stack:
                        new_nodes.append(TextNode("".join(current_segment_text), TextType.TEXT))
                    else:
                        new_nodes.append(TextNode("".join(current_segment_text), text_type))
                    current_segment_text = []

                if not stack:
                    stack.append(delimiter)
                else:
                    stack.pop()

                i += delimiter_len
            else:
                current_segment_text.append(text[i])
                i += 1

        if current_segment_text:
            if stack:
                raise ValueError(f"Invalid Markdown: Unclosed delimiter '{delimiter}' at end of text: {old_node.text}")
            else:
                new_nodes.append(TextNode("".join(current_segment_text), TextType.TEXT))
        elif stack:
            raise ValueError(f"Invalid Markdown: Unclosed delimiter '{delimiter}' in text: {old_node.text}")

    return new_nodes
