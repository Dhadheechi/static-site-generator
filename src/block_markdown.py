from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n") # this is a double newline - a blank line
    blocks = []
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue

        if block.startswith("#"): # for a heading block, split whatever that follows into a new block
            parts = block.split("\n", 1) # split only once
            blocks.append(parts[0].strip())
            if len(parts) > 1 and parts[1].strip():
                blocks.append(parts[1])
        else:
            blocks.append(block)
    return blocks

def block_to_block_type(markdown_block):
    heading_starts = ("# ", "## ", "### ", "#### ", "##### ", "###### ",)
    ordered_list_starts = [f"{i+1}. " for i in range(len(markdown_block.split("\n")))]
    # nums = list(range(len(markdown_block.split("\n"))))
    if markdown_block.startswith(heading_starts):
        return BlockType.heading
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.code
    elif list(filter(lambda x: x.startswith(">"), markdown_block.split("\n"))) == markdown_block.split("\n"):
        return BlockType.quote
    elif list(filter(lambda x: x.startswith("- "), markdown_block.split("\n"))) == markdown_block.split("\n"):
        return BlockType.unordered_list
    elif list(map(lambda x: x[:3], markdown_block.split("\n"))) == ordered_list_starts:
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

def get_tag_from_block_type(block_type, block_start):
    match block_type:
        case "heading":
            length = len(block_start)
            return f"h{length}"
        case "code":
            return "code"
        case "quote":
            return "blockquote"
        case "unordered_list":
            return "ul"
        case "ordered_list":
            return "ol"
        case "paragraph":
            return "p"


def text_to_children(text, tag, block_type): # should convert a single markdown block to a HTML node with all it's children nodes
    match block_type:
        case "heading":
            heading_type = int(tag[1])
            hashes = "#" * heading_type
            heading = text.splitlines()[0].lstrip(f"{hashes} ")
            # heading_node = LeafNode(tag, heading)
            textnodes = text_to_textnodes(heading)
            htmlnodes = list(map(lambda x: text_node_to_html_node(x), textnodes))
            block_html_node = ParentNode(tag, children=htmlnodes, props=None)
            return block_html_node
        case "unordered_list":
            block_lines = list(map(lambda x: x[2:], text.splitlines()))
            textnodes = list(map(lambda x: text_to_textnodes(x), block_lines))
            htmlnodes = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y), x)), textnodes))
            htmlnodes = list(map(lambda x: ParentNode("li", children=x, props=None), htmlnodes))
            block_html_node = ParentNode(tag, children=htmlnodes, props=None)
            return block_html_node
        case "ordered_list":
            block_lines = list(map(lambda x: x[3:], text.splitlines()))
            textnodes = list(map(lambda x: text_to_textnodes(x), block_lines))
            htmlnodes = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y), x)), textnodes))
            htmlnodes = list(map(lambda x: ParentNode("li", children=x, props=None), htmlnodes))
            block_html_node = ParentNode(tag, children=htmlnodes, props=None)
            return block_html_node
        case "quote":
            block_lines = "\n".join(list(map(lambda x: x[2:], text.splitlines())))
            # block_replaced = block_lines.replace("\n", " ") # replace newline in paragraph with space
            textnodes = text_to_textnodes(block_lines)
            htmlnodes = list(map(lambda x: text_node_to_html_node(x), textnodes))
            block_html_node = ParentNode(tag, children=htmlnodes, props=None) 
            return block_html_node
        case "code":
            block_text = text.strip("```").lstrip()

            block_html_node = ParentNode(tag="pre",children=[text_node_to_html_node(TextNode(block_text, TextType.CODE))], props=None)
            return block_html_node
        case "paragraph":
            if text == "": 
                return
            block_replaced = text.replace("\n", " ") # replace newline in paragraph with space
            textnodes = text_to_textnodes(block_replaced)
            htmlnodes = list(map(lambda x: text_node_to_html_node(x), textnodes))
            block_html_node = ParentNode(tag, children=htmlnodes, props=None) 
            return block_html_node
        case _:
            raise ValueError(f"Unknown block type: {block_type}")



def markdown_to_html_node(markdown): # converts a full markdown document into a single HTMLNode
    blocks = markdown_to_blocks(markdown) 
    # print("Number of blocks: ", len(blocks))
    block_children = []
    for block in blocks: # convert each block into an appropriate HTML node
        block_type = block_to_block_type(block).value
        block_start = block.split()[0]
        tag = get_tag_from_block_type(block_type, block_start)
        block_html_node = text_to_children(block, tag, block_type)
        block_children.append(block_html_node)
        # print(len(block_children))
    return ParentNode(tag="div", children=block_children)

def extract_title(markdown):
    markdown = markdown.strip()
    if not markdown.startswith("# "): 
        raise Exception("Markdown file must start with an h1 header")
    return markdown.splitlines()[0].lstrip("# ").rstrip()
               


