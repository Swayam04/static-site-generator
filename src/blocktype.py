from enum import Enum, auto
import re

class BlockType(Enum):
    paragraph = auto()
    heading = r"^#{1,6}\s+"
    code = r"^```([^\n]*)$"
    quote = r"^>\s*"
    unordered_list = r"^[-*]\s+"
    ordered_list = r"^\d+\.\s+"

def all_lines_match(lines: list[str], pattern: str) -> bool:
    return all(re.match(pattern, line) for line in lines)

def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")
    first_line = lines[0]

    match first_line:
        case line if re.match(BlockType.heading.value, line):
            return check_heading_block(lines)
        case line if re.match(BlockType.code.value, line):
            return check_code_block(lines)
        case line if re.match(BlockType.quote.value, line):
            return check_quote_block(lines)
        case line if re.match(BlockType.unordered_list.value, line):
            return check_unordered_list_block(lines)
        case line if re.match(BlockType.ordered_list.value, line):
            return check_ordered_list_block(lines)
        case _:
            return BlockType.paragraph

def check_heading_block(lines: list[str]) -> BlockType:
    return BlockType.heading if len(lines) == 1 else BlockType.paragraph

def check_code_block(lines: list[str]) -> BlockType:
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return BlockType.code
    return BlockType.paragraph

def check_quote_block(lines: list[str]) -> BlockType:
    return BlockType.quote if all_lines_match(lines, BlockType.quote.value) else BlockType.paragraph

def check_unordered_list_block(lines: list[str]) -> BlockType:
    return BlockType.unordered_list if all_lines_match(lines, BlockType.unordered_list.value) else BlockType.paragraph

def check_ordered_list_block(lines: list[str]) -> BlockType:
    return BlockType.ordered_list if all_lines_match(lines, BlockType.ordered_list.value) else BlockType.paragraph

    