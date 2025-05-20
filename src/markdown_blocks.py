from enum import Enum

class BlockType(Enum):
	PARAGRAPH = 'paragraph'
	HEADING = 'heading'
	CODE = 'code'
	QUOTE = 'quote'
	UNORDERED_LIST = 'unordered_list'
	ORDERED_LIST = 'ordered_list'

def block_to_block_type(text_node):
    if text_node.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if text_node.startswith("```") and text_node.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in text_node.splitlines()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in text_node.splitlines()):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(text_node.splitlines(), start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks