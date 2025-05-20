from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    # Convert text with inline markdown to HTMLNodes
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        # Convert each TextNode to an HTMLNode
        # Depending on your implementation, you might need to use 
        # a function like text_node_to_html_node
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes 

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return HTMLNode("p", None, None, children)

def heading_to_html_node(block):
    # Determine heading level (h1-h6)
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # Remove the heading markers and whitespace
    content = block[level:].strip()
    
    children = text_to_children(content)
    return HTMLNode(f"h{level}", None, None, children)

def code_to_html_node(block):
    # Remove the ``` from the beginning and end
    # This assumes the first line is just ``` and the last line is just ```
    lines = block.split("\n")
    if len(lines) >= 3:  # At minimum we need opening ```, content, closing ```
        code_content = "\n".join(lines[1:-1])
    else:
        code_content = ""
    
    # For code blocks, don't process inline markdown
    # Instead, create a text node directly
    text_node = TextNode(code_content, "text")
    code_node = text_node_to_html_node(text_node)
    
    # Wrap in a pre tag
    return HTMLNode("pre", None, None, [HTMLNode("code", None, None, [code_node])])

def quote_to_html_node(block):
    # Remove the > prefix from each line
    lines = block.split("\n")
    # Strip the > and one space after it (if present)
    content_lines = []
    for line in lines:
        if line.startswith("> "):
            content_lines.append(line[2:])
        elif line.startswith(">"):
            content_lines.append(line[1:])
    
    # Join the lines back together
    content = "\n".join(content_lines)
    
    # Process inline markdown
    children = text_to_children(content)
    
    # Create a blockquote node
    return HTMLNode("blockquote", None, None, children)

def unordered_list_to_html_node(block):
    # Split into lines
    lines = block.split("\n")
    
    # Create a list item node for each line
    list_items = []
    for line in lines:
        # Remove the "- " prefix
        if line.startswith("- "):
            item_content = line[2:]
        elif line.startswith("-"):
            item_content = line[1:]
        else:
            item_content = line
            
        # Process inline markdown for this item
        item_children = text_to_children(item_content)
        
        # Create an li node and add to list
        li_node = HTMLNode("li", None, None, item_children)
        list_items.append(li_node)
    
    # Create the ul node with all list items as children
    return HTMLNode("ul", None, None, list_items)

def ordered_list_to_html_node(block):
    # Split into lines
    lines = block.split("\n")
    
    # Create a list item node for each line
    list_items = []
    for i, line in enumerate(lines, start=1):
        # The line should start with "1. ", "2. ", etc.
        # We'll use a more general approach to extract the content
        parts = line.split(". ", 1)
        if len(parts) == 2 and parts[0].isdigit():
            item_content = parts[1]
        else:
            # If the format isn't as expected, just use the whole line
            item_content = line
            
        # Process inline markdown for this item
        item_children = text_to_children(item_content)
        
        # Create an li node and add to list
        li_node = HTMLNode("li", None, None, item_children)
        list_items.append(li_node)
    
    # Create the ol node with all list items as children
    return HTMLNode("ol", None, None, list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # Create a parent div node
    parent_node = HTMLNode("div", None, None, [])
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # Convert the block to an HTMLNode based on its type
        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        elif block_type == BlockType.ULIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.OLIST:
            block_node = ordered_list_to_html_node(block)
        else:
            # Default to paragraph if type is unknown
            block_node = paragraph_to_html_node(block)
        
        # Add the block node as a child to the parent node
        parent_node.children.append(block_node)
    
    return parent_node