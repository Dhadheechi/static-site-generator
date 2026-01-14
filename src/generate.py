import os
from block_markdown import markdown_to_html_node, extract_title
from htmlnode import LeafNode, ParentNode, HTMLNode
def generate_page(from_path, template_path, dest_path):
    print(f"Genearting page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r+") as t:
        template = t.read()
        
    html = markdown_to_html_node(markdown).to_html() 
    title = extract_title(markdown)
    new_html = template.replace("{{ Title }}", title) # replace() returns a copy of the string; so we need to assign it
    new_html = new_html.replace("{{ Content }}", html)
    
    dest_dir = os.path.dirname(dest_path) # gets the directory name of a given path
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as d:
        d.write(new_html)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, abs_path = "."):
    content_path = os.path.join(abs_path, dir_path_content)
    public_path = os.path.join(abs_path, dest_dir_path)

    for f in os.listdir(content_path):
        content_file_path = os.path.join(content_path, f)
        if os.path.isfile(content_file_path):
            html_file = f.split(".")[0] + ".html"
            public_file_path = os.path.join(public_path, html_file)
            generate_page(content_file_path, template_path, public_file_path)
        else:
            rel_content_path = f"{dir_path_content}/{f}"
            rel_public_path = f"{dest_dir_path}/{f}"
            generate_pages_recursively(rel_content_path, template_path, rel_public_path, abs_path)





     
