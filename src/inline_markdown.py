import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type): # we are given a specific delimiter, so only check for that
    new_nodes = []
    for old_node in old_nodes: # all nodes must have the same separating delimiter 
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            new_strings=  old_node.text.split(delimiter)
            if len(new_strings) % 2 == 0: 
                raise Exception("Closing delimiter not found -- Invalid markdown syntax")
            for i in range(len(new_strings)):
                if i % 2 == 0: # this is a text string
                    if new_strings[i] == "":
                         continue
                    new_nodes.extend([TextNode(new_strings[i], TextType.TEXT)]) # even if it's an empty string, add it
                else: # this is a formatted string
                    new_nodes.extend([TextNode(new_strings[i], text_type)])

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            if len(matches) == 0:
                 new_nodes.append(old_node)
            else:
                remaining_string = old_node.text
                for match in matches: # match is a tuple (alt text, link)
                    new_strings = remaining_string.split(f"[{match[0]}]({match[1]})", 1) # a maxsplit of only 1
                    if not new_strings[0] == "": # just an empty text, then don't add it
                            new_nodes.extend([TextNode(new_strings[0], TextType.TEXT)])
                    new_nodes.extend([TextNode(match[0], TextType.LINK, match[1])])

                    remaining_string = new_strings[1]
                
                if remaining_string != "": # if there's some remaining text after we're done with all our matches, then add it as a last text node
                    new_nodes.extend([TextNode(remaining_string, TextType.TEXT)])
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            if len(matches) == 0:
                 new_nodes.append(old_node)
            else:
                remaining_string = old_node.text
                for match in matches: # match is a tuple (alt text, link)
                    new_strings = remaining_string.split(f"![{match[0]}]({match[1]})", 1) # a maxsplit of only 1
                    if not new_strings[0] == "": # just an empty text, then don't add it
                            new_nodes.extend([TextNode(new_strings[0], TextType.TEXT)])
                    new_nodes.extend([TextNode(match[0], TextType.IMAGE, match[1])])

                    remaining_string = new_strings[1]
                
                if remaining_string != "": # if there's some remaining text after we're done with all our matches, then add it as a last text node
                    new_nodes.extend([TextNode(remaining_string, TextType.TEXT)])
    
    return new_nodes
             

# ![alt text](image link)
def extract_markdown_images(text): # returns a list of tuples, each containing the alt text and the url of the image
    #matches = re.findall(r"!\[([^\[\]*)\]\(([^\(\)*])\)", text) # [alt text] shouldn't further contain any [], and (link) shouldn't contain any further () 
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # [alt text] shouldn't further contain any [], and (link) shouldn't contain any further () 
    return matches

# [alt text](link)
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # same as for images but doesn't match if it starts with !
    return matches


def text_to_textnodes(text):
    original_text_node = TextNode(text, TextType.TEXT)
    # just apply all the functions one after the other -- this is why each split function is required to work on multiple nodes
    new_nodes = split_nodes_delimiter([original_text_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes


text = "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

print(text_to_textnodes(text))

