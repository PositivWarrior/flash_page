from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # Nagłówki: od # do ######
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Bloki kodu: start i koniec to ```
    if len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Dzielimy blok na linie, aby sprawdzić typy wielolinijkowe
    lines = block.split("\n")
    
    # Cytaty: każda linia zaczyna się od >
    if block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
            
    # Listy nienumerowane: każda linia zaczyna się od "- "
    if block.startswith("- "):
        is_unordered = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered = False
                break
        if is_unordered:
            return BlockType.UNORDERED_LIST
            
    # Listy numerowane: każda linia zaczyna się od "i. " (gdzie i startuje od 1)
    if block.startswith("1. "):
        is_ordered = True
        for i in range(len(lines)):
            expected_start = f"{i + 1}. "
            if not lines[i].startswith(expected_start):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST
            
    # Jeśli nic nie pasuje, to zwykły akapit
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in raw_blocks:
        cleaned_block = block.strip()

        if cleaned_block == "":
            continue

        filtered_blocks.append(cleaned_block)

    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return create_ul_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return create_ol_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading_node(block):
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")

    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_code_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    # Code block nie parsuje inline markdowna!
    raw_text_node = LeafNode(None, text)
    code_node = ParentNode("code", [raw_text_node])
    return ParentNode("pre", [code_node])

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_ul_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def create_ol_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        # Odcinamy cyfrę, kropkę i spację (np. "1. ")
        pos = line.find(". ")
        text = line[pos + 2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found in markdown")

