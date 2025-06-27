from htmlnode import HTMLNode
from md_parser import markdown_to_blocks, text_to_textnodes
from blocktype import BlockType, block_to_blocktype
from parentnode import ParentNode
from leafnode import text_node_to_html_node
from textnode import TextNode, TextType
from typing import List
import re

BLOCK_TYPE_TO_HTML_TAG = {
    BlockType.paragraph: "p",
    BlockType.quote: "blockquote",
    BlockType.unordered_list: "ul",
    BlockType.ordered_list: "ol",
    BlockType.code: "code",
}

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes: List[HTMLNode] = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        block_tag_name = get_parent_tag_name(block, block_type)
        children = get_block_children(block, block_type)
        blocknode = ParentNode(block_tag_name, children)
        if block_type == BlockType.code:
            blocknode = ParentNode("pre", [blocknode])
        nodes.append(blocknode)
    return ParentNode("div", nodes)

def get_block_children(block: str, parent_type: BlockType) -> List[HTMLNode]:
    return block_content_processors[parent_type](block)

def text_to_html_nodes(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: List[HTMLNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def get_heading_children(heading: str) -> List[HTMLNode]:
    content = re.sub(BlockType.heading.value, "", heading)
    return text_to_html_nodes(content)

def get_paragraph_children(paragraph: str) -> List[HTMLNode]:
    return text_to_html_nodes(paragraph)

def get_quotes_children(quotes: str) -> List[HTMLNode]:
    lines = [re.sub(BlockType.quote.value, "", line) for line in quotes.split("\n")]
    full_content = "\n".join(lines)
    return text_to_html_nodes(full_content)

def get_unordered_list_children(u_list: str) -> List[ParentNode]:
    return get_list_item_children(u_list, BlockType.unordered_list)

def get_ordered_list_children(o_list: str) -> List[ParentNode]:
    return get_list_item_children(o_list, BlockType.ordered_list)

def get_list_item_children(list_block: str, list_type: BlockType) -> List[ParentNode]:
    lines = list_block.split("\n")
    html_nodes: List[ParentNode] = []
    
    assert isinstance(list_type.value, str)
    pattern = list_type.value
    
    for line in lines:
        content = re.sub(pattern, "", line)
        li_children = text_to_html_nodes(content)
        li_parent = ParentNode("li", li_children)
        html_nodes.append(li_parent)
    return html_nodes

def get_code_children(code: str) -> List[HTMLNode]:
    lines = code.split('\n')
    code_content = "\n".join(lines[1:-1])
    code_text = TextNode(code_content, TextType.TEXT)
    return [text_node_to_html_node(code_text)]

block_content_processors = {
    BlockType.heading: get_heading_children,
    BlockType.code: get_code_children,
    BlockType.paragraph: get_paragraph_children,
    BlockType.quote: get_quotes_children,
    BlockType.ordered_list: get_ordered_list_children,
    BlockType.unordered_list: get_unordered_list_children,
}

def get_parent_tag_name(block: str, block_type: BlockType) -> str:
    if block_type == BlockType.heading:
        return get_header_tag(block)
    return BLOCK_TYPE_TO_HTML_TAG.get(block_type, "p")

def get_header_tag(block: str) -> str:
    count = len(block) - len(block.lstrip('#'))
    return f"h{count}"