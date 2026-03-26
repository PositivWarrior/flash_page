import os
import shutil
from textnode import TextNode, TextType
from block_markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    title = extract_title(markdown_content)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

def copy_static_files_to_public(source, destination):
    if os.path.exists(destination):
        print(f"Deleting directory: {destination}")
        shutil.rmtree(destination)

    print(f"Creating directory: {destination}")
    os.mkdir(destination)

    recursive_copy(source, destination)

def recursive_copy(src, dst):
    items = os.listdir(src)

    for item in items:
        source_path = os.path.join(src, item)
        dest_path = os.path.join(dst, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            recursive_copy(source_path, dest_path)

def main():
    static_path = "./static"
    public_path = "./public"

    print("Starting static sync...")
    copy_static_files_to_public(static_path, public_path)

    print("Generating index page...")
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )

if __name__ == "__main__":
    main()