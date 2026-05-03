from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter
from markdown_blocks import text_to_children

def main():

    #node = HTMLNode("b", "blabla", None, {"GTA": "San Andreas", "Website": "GTASA.com"})
    #print(node)
    #print(node.props_to_html())
    
    #node_leaf = LeafNode("b", "blabla", {"GTA": "San Andreas", "Website": "GTASA.com"})
    #html_formatted = node_leaf.props_to_html()
    #print(html_formatted)
    #print(node.props_to_html())
    
    #node_leaf = LeafNode("b", "blabla", {"GTA": "San Andreas", "Website": "GTASA.com"})
    #html_formatted = node_leaf.to_html()
    #print(html_formatted)

    
    #child1 = LeafNode(None, "blabla", {"GTA": "III", "Website": "GTAIII.com"})
    #child2 = LeafNode("p", "hello", {"GTA": "Vice City", "Website": "GTAVC.com"})
    #parent_node = ParentNode("b", [child1, child2], None)
    #print(parent_node.to_html())

    #node = TextNode("This is text with a 'code block' word", TextType.TEXT)
    #split_nodes_delimiter([node], "'", TextType.CODE)

   # x = text_to_children("Hello *world*")
    #print(x)




if __name__ == "__main__":
    main()