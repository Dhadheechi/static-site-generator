from textnode import TextNode, TextType
from generate import generate_page, generate_pages_recursively

import os
import shutil
def copy_static_to_public(dir_path, abs_path="."):
    if dir_path == ".":
        if os.path.exists(os.path.join(abs_path, "public")):
            shutil.rmtree(os.path.join(abs_path, "public")) # delete everything from the destination on the first invocation of this recursive function
        os.mkdir(os.path.join(abs_path, "public"))
    current_dir = os.path.join(abs_path, f"static/{dir_path}")
    current_dir_public = os.path.join(abs_path, f"public/{dir_path}")
    for f in os.listdir(current_dir):
        path = os.path.join(current_dir, f)
        if os.path.isfile(path):
            file_path = os.path.join(current_dir, f)
            with open("log.txt", "a") as file:
               file.write(file_path)
            file_path_public = os.path.join(current_dir_public, f)
            shutil.copy(file_path, file_path_public)
        else:
            folder_path = os.path.join(current_dir_public, f)
            os.mkdir(folder_path)
            rel_path = f"{dir_path}/{f}"
            copy_static_to_public(rel_path, abs_path) # the new relative path


if __name__ == "__main__":
    copy_static_to_public(".")
    generate_pages_recursively("content/", "template.html", "public")
