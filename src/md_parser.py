from typing import List, Tuple
from textnode import TextNode, TextType
import re

pattern_map = {
    TextType.IMAGE : r"!\[(?P<alt>.*?)\]\((?P<url>.*?)\)", 
    TextType.LINK : r"(?<!!)\[(?P<alt>.*?)\]\((?P<url>.*?)\)"
}

def markdown_to_blocks(markdown : str) -> List[str]:
    res = [s.strip() for s in markdown.split("\n\n") if s.strip()]
    return res

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    processors = [
        (split_nodes_delimiter, ('**', TextType.BOLD)),
        (split_nodes_delimiter, ('_', TextType.ITALIC)),
        (split_nodes_delimiter, ('`', TextType.CODE)),
        (split_nodes_image, ()),
        (split_nodes_link, ()),
    ]

    for processor, args in processors:
        nodes = processor(nodes, *args)

    return nodes

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

def split_nodes_image(old_nodes : List[TextNode]) -> List[TextNode]:
    return split_link_types(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes : List[TextNode]) -> List[TextNode]:
    return split_link_types(old_nodes, TextType.LINK)

def split_link_types(old_nodes: List[TextNode], link_type: TextType) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    regex = re.compile(pattern_map[link_type])
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        last_index = 0
        for match in regex.finditer(text):
            if match.start() > last_index:
                new_nodes.append(TextNode(text[last_index:match.start()], TextType.TEXT))
            new_nodes.append(TextNode(match.group('alt'), link_type, match.group('url')))
            last_index = match.end()

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    
    return new_nodes

def extract_title(markdown : str) -> str:
    md_blocks = markdown_to_blocks(markdown)
    h1_pattern = r"^#\s+"

    for block in md_blocks:
        if re.match(h1_pattern, block):
            return re.sub(h1_pattern, "", block).strip()
    raise ValueError("No title found in markdown. A title is mandatory.")

