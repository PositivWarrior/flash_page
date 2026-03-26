import os
import shutil
from textnode import TextNode, TextType

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
    print("Sync complete!")

if __name__ == "__main__":
    main()