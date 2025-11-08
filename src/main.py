from textnode import TextNode, TextType


def main():
    text_node = TextNode("this is some text", TextType.LINK, "dhadheechi.github.io")
    print(text_node)

main()