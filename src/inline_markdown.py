from textnode import TextNode, TextType
import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
    
        split_nodes = []
        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: no closing delimeter {delimiter} found")

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(parts[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")    

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]    

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
            
    return new_nodes

    