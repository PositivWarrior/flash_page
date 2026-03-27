import sys
import os
import shutil
from textnode import TextNode, TextType
from block_markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
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

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)

    for entry in entries:
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):
            if entry.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]


    static_path = "./static"
    docs_path = "./docs"
    content_path = "./content"
    template_path = "./template.html"

    print("Starting sync and generation...")
    copy_static_files_to_public(static_path, docs_path)

    generate_pages_recursive(content_path, template_path, docs_path, basepath)

    print("Build finieshed successfully!")

if __name__ == "__main__":
    main()