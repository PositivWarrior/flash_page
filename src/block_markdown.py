def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in raw_blocks:
        cleaned_block = block.strip()

        if cleaned_block == "":
            continue

        filtered_blocks.append(cleaned_block)

    return filtered_blocks