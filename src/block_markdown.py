def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n") # this is a double newline - a blank line
    blocks = list(map(lambda x: x.strip(), blocks))

    return blocks

