from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value # the content of the tag
        self.children = children # a list of HTMLNode objects representing the children
        self.props = props # a dictionary of key-value pairs representing the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError("to_html method hasn't been implemented yet")
    
    def props_to_html(self):
        if self.props is None or len(self.props.keys()) == 0:
            return ""
        
        string_list = list(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
        return " ".join(string_list)

    def __repr__(self): # this method should return a string object
        return f"HTMLNode(tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): # only props can be None, and not tag and value, since this is a leaf node
        if value is None: 
            raise ValueError("Leaf node must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props) # explicitly set children to none (overwriting)
        # super().__init__(tag, value, props=None) # we're overriding the given props variable with None
    
    def to_html(self): # renders a leaf node as a html string
        if self.value is None:
            raise ValueError("No value assigned to the leaf node") # all leaf nodes must have a value
        elif self.tag is None:
            return self.value
        
        match self.tag:
            case "p":
                return f'<p>{self.value}</p>'
            case "b":
                return f'<b>{self.value}</b>'
            case "i":
                return f'<i>{self.value}</i>'
            case "a":
                return f'<a {self.props_to_html()}>{self.value}</a>' # converts the attribute of the anchor tag to a string
            case "li":
                return f'<li>{self.value}</li>'
            case "code":
                return f'<code>{self.value}</code>'
            case "blockquote":
                return f'<blockquote>{self.value}</blockquote>'
            case "img": # yet to test properly -- I don't know how exactly it's supposed to render
                return f'<img {self.props_to_html()} />'
            case "span":
                return f'<span>{self.value}</span>'
            
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None): 
        super().__init__(tag=tag, value=None, children=children, props=props) 

    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        
        output_string_list = []

        for i in range(len(self.children)): # recursively call to_html on all the children nodes (which may or may not be leaf nodes)
            child = self.children[i]
            output_string_list.append(child.to_html())
        output_string = "".join(output_string_list)
        
        output_string = f'<{self.tag}>{output_string}</{self.tag}>' # we concatenate the outputs of all the child nodes
        return output_string
    
    




def text_node_to_html_node(text_node): # converts a text node to a leaf node

    match text_node.text_type: # this can be one of many different types
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("link", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", value="", props={"src": text_node.url, "alt": text_node.text}) 

        case _:
            raise Exception("Invalid type for text node")   
        
