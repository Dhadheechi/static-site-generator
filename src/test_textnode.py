import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase): # this piece of code tests our TextNode class, the _eq_ methods in it etc
    def test_eq(self):
        node = TextNode("This is a Text Node", TextType.BOLD)
        node2 = TextNode("This is a Text Node", TextType.BOLD)

        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a Text Node", TextType.BOLD)
        node2 = TextNode("This is a different Text Node", TextType.BOLD)

        self.assertNotEqual(node, node2)
    
    def test_not_same_type(self):
        node = TextNode("This is a Text Node", TextType.BOLD)
        node2 = TextNode("This is a Text Node", TextType.ITALIC)   
        self.assertNotEqual(node, node2)    
    
    def test_url_missing(self):
        node = TextNode("This is a Text Node", TextType.LINK, url="somewebsite.com")
        node2 = TextNode("This is a Text Node", TextType.LINK) # here url is missing so these two are not equal
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()