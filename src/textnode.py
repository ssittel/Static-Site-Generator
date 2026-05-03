from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text    #text content of the node
        self.text_type = text_type  #type of text this node contains; member of the TextType enum
        self.url = url  #url of the link or image, if the text is a link -> default to None, if nothing is passed in


    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})" #self.text_type.value is needed so we return the value specifically and not e.g. "BOLD" (aka the name)
            

def text_node_to_html_node(text_node):

    if text_node.text_type == TextType.TEXT:
        transformed_node = LeafNode(None, text_node.text)
        return transformed_node
    
    elif text_node.text_type == TextType.BOLD:
        transformed_node = LeafNode("b", text_node.text)
        return transformed_node
    
    elif text_node.text_type == TextType.ITALIC:
        transformed_node = LeafNode("i", text_node.text)
        return transformed_node
    
    elif text_node.text_type == TextType.CODE:
        transformed_node = LeafNode("code", text_node.text)
        return transformed_node
    
    elif text_node.text_type == TextType.LINK:
        transformed_node = LeafNode("a", text_node.text, {"href": text_node.url})
        return transformed_node
    
    elif text_node.text_type == TextType.IMAGE:
        transformed_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        return transformed_node
    
    else:
        raise Exception("invalid text_type")