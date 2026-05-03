import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_node_with_mult_prop(self):
        node = HTMLNode("b", "blabla", None, {"GTA": "San Andreas", "Website": "GTASA.com"})
        actual = node.props_to_html()
        expected = ' GTA="San Andreas" Website="GTASA.com"'
        self.assertEqual(actual, expected)

    def test_props_none(self):
        node = HTMLNode("b", "blabla", None, None)
        actual = node.props_to_html()
        expected = ""
        self.assertEqual(actual, expected)

    def test_no_args(self):
        node = HTMLNode()
        self.assertIsNone(node.tag) #attributes belong to node, not self. However assert is called on self (the test case)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_string(self):
        node = HTMLNode("b", "blabla", None, {"GTA": "San Andreas", "Website": "GTASA.com"})
        actual = repr(node)
        expected = "HTMLNode(tag= b, value= blabla, children= None, props= {'GTA': 'San Andreas', 'Website': 'GTASA.com'})"
        self.assertEqual(actual, expected)


class TestLeafNode(unittest.TestCase):

    def test_html_formatting(self):
        node = LeafNode("b", "blabla", {"GTA": "Vice City", "Website": "GTAVC.com"}) #testing the actual HTML formatting
        actual = node.to_html()
        expected = '<b GTA="Vice City" Website="GTAVC.com">blabla</b>'
        self.assertEqual(actual, expected)

    def test_no_tag(self):
        node = LeafNode(None, "blabla", {"GTA": "Vice City", "Website": "GTAVC.com"}) #no tag
        actual = node.to_html()
        expected = 'blabla'
        self.assertEqual(actual, expected)

    def test_no_text(self):
        node = LeafNode("b", None, {"GTA": "Vice City", "Website": "GTAVC.com"}) #no text
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):

    def test_one_child(self):
        child = LeafNode("p", "I love cheese", {"Cheese": "is great", "Website": "cheese.com"})
        parent_node = ParentNode("b", [child])
        actual = parent_node.to_html()
        expected = '<b><p Cheese="is great" Website="cheese.com">I love cheese</p></b>'
        self.assertEqual(actual, expected)

    def test_one_child_with_parent_props(self):
        child = LeafNode("p", "I love cheese", {"Cheese": "is great", "Website": "cheese.com"})
        parent_node = ParentNode("b", [child], {"Pizza": "Margharita"})
        actual = parent_node.to_html()
        expected = '<b Pizza="Margharita"><p Cheese="is great" Website="cheese.com">I love cheese</p></b>'
        self.assertEqual(actual, expected)
    
    
    def test_multiple_children(self):
        child1 = LeafNode(None, "blabla", {"GTA": "III", "Website": "GTAIII.com"})
        child2 = LeafNode("p", "hello", {"GTA": "Vice City", "Website": "GTAVC.com"})
        parent_node = ParentNode("b", [child1, child2])
        actual = parent_node.to_html()
        expected = '<b>blabla<p GTA="Vice City" Website="GTAVC.com">hello</p></b>'
        self.assertEqual(actual, expected)

    def test_nested_parent_node(self):
        child = LeafNode(None, "blabla", {"GTA": "III"})
        other_parent = ParentNode("p", [child], {"GTA": "Vice City"})
        parent_node = ParentNode("b", [other_parent]) #props is None, but doesn't have to written out cuz of the default in the constructor
        actual = parent_node.to_html()
        expected = '<b><p GTA="Vice City">blabla</p></b>'
        self.assertEqual(actual, expected)

    def test_missing_tag(self):
        child = LeafNode("p", "I love cheese", {"Cheese": "is great", "Website": "cheese.com"})
        parent_node = ParentNode(None, [child], {"Pizza": "Margharita"})
        with self.assertRaises(ValueError):
            parent_node.to_html()
        
    def test_missing_children(self):
        parent_node = ParentNode("b", None, {"Pizza": "Margharita"})
        with self.assertRaises(ValueError):
            parent_node.to_html()