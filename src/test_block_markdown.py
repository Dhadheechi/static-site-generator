import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title
# from htmlnode import HTMLNode, ParentNode, LeafNode

class TestMarkdowntoBlock(unittest.TestCase):
    def test_markdown_to_blocks(self): # newlines shouldn't be indented, if so, the tabs would be included
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlocktoBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

    def test_block_to_quote(self):
        block = "> This is a list\n> with items"
        self.assertEqual(block_to_block_type(block), BlockType.quote)


    def test_block_to_code(self):
        block = "1. This is an ordered list\n2. with items\n3. with some more items"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)
    
    def test_block_to_heading(self):
        block = "### This is a heading text"
        self.assertEqual(block_to_block_type(block), BlockType.heading)
    
    def test_block_to_not_heading(self):
        block = "####### This is not a heading text"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

class TestBlocktoHTML(unittest.TestCase):
    def test_paragraphs(self):
         md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

         node = markdown_to_html_node(md)
         html = node.to_html()
         self.assertEqual(
             html,
             "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
         )

    def test_codeblock(self):
         md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

         node = markdown_to_html_node(md)
         html = node.to_html()
         self.assertEqual(
             html,
             "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
         )

    def test_heading(self):
         md = """
### This is the heading 
This is some **bolded** text under a heading.
This is some more _italic_ text under the same heading

This is some more text in a different paragraph block.
"""

         node = markdown_to_html_node(md)
         html = node.to_html()
         self.assertEqual(
             html,
             "<div><h3>This is the heading</h3><p>This is some <b>bolded</b> text under a heading. This is some more <i>italic</i> text under the same heading</p><p>This is some more text in a different paragraph block.</p></div>",
         ) # it's important to treat the newlines as separators, and not content

    def test_unordered_list(self):
        md = """
- This is some **bolded** text in an ordered list.
- This is some more _italic_ text in the ordered list.
- This is some `code` text in the ordered list.

This is some more text in a different paragraph block.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ul><li>This is some <b>bolded</b> text in an ordered list.</li><li>This is some more <i>italic</i> text in the ordered list.</li><li>This is some <code>code</code> text in the ordered list.</li></ul><p>This is some more text in a different paragraph block.</p></div>",
       )
    def test_ordered_list(self):
        md = """
1. This is some **bolded** text in an ordered list.
2. This is some more _italic_ text in the ordered list.
3. This is some `code` text in the ordered list.

This is some more text in a different paragraph block.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ol><li>This is some <b>bolded</b> text in an ordered list.</li><li>This is some more <i>italic</i> text in the ordered list.</li><li>This is some <code>code</code> text in the ordered list.</li></ol><p>This is some more text in a different paragraph block.</p></div>",
       )

    def test_quote(self):
        md = """
> This is some **bolded** text in an ordered list.
> This is some more _italic_ text in the ordered list.
> This is some `code` text in the ordered list.

This is some more text in a different paragraph block.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><blockquote>This is some <b>bolded</b> text in an ordered list.\nThis is some more <i>italic</i> text in the ordered list.\nThis is some <code>code</code> text in the ordered list.</blockquote><p>This is some more text in a different paragraph block.</p></div>",
       )
    
    def test_extract_title(self):
         md = """
# some title 
This is some **bolded** text under a heading.
This is some more _italic_ text under the same heading

This is some more text in a different paragraph block.
"""
         title = extract_title(md)
         self.assertEqual(
                title, 
                "some title"
         )

    def test_extract_title_and_ensure_strip(self):
         md = """
# some title 
This is some **bolded** text under a heading.
This is some more _italic_ text under the same heading

This is some more text in a different paragraph block.
"""
         title = extract_title(md)
         self.assertNotEqual(
                title, 
                "some title "
         )
        
if __name__ == "__main__":
    unittest.main()
