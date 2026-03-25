from enum import Enum

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