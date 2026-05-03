import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_txtnoteq(self):
        node = TextNode("Blabla", TextType.BOLD)
        node2 = TextNode("Blablabla", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_txttypenoteq(self):
        node = TextNode("Blabla", TextType.BOLD)
        node2 = TextNode("Blabla", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_urlnoteq(self):
        node = TextNode("Blabla", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("Blabla", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    def test_urlnone(self):
        node = TextNode("Blabla", TextType.BOLD, None)
        node2 = TextNode("Blabla", TextType.BOLD, None)
        self.assertEqual(node, node2)

    
class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")

    def test_tag(self):
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")   

    def test_link(self):
        node = TextNode("blabla", TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "blabla")
        self.assertEqual(html_node.props, {"href": "www.boot.dev"})

    def test_img(self):
        node = TextNode("some text", TextType.IMAGE, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.boot.dev", "alt": "some text"})

    def test_faulty_type(self):
        node = TextNode("haha", "fake_type") #TextNode.__init__ doesn't validate text_type at all, so we can just pass this in -> avoids python Attribute error
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
            



if __name__ == "__main__":
    unittest.main()