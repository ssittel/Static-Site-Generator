from textnode import TextNode,TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_pieces = node.text.split(delimiter)
            if len(split_pieces) % 2 == 0:
                raise Exception("invalid markdown: unclosed delimiter")

            for index, piece in enumerate(split_pieces):
                if index % 2 == 0:
                    even_piece_node = TextNode(piece, TextType.TEXT)
                    new_nodes.append(even_piece_node)
                else:
                    odd_piece_node = TextNode(piece, text_type)
                    new_nodes.append(odd_piece_node)
    return new_nodes

   

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        image_list = extract_markdown_images(old_node.text) #get a list of tuples consisting of image_alt and image_link from the old node's text
        
        if old_node.text_type != TextType.TEXT: #if e.g. the text is already bold, just append it as is
            new_nodes.append(old_node)
            continue
        if image_list == []:    #if there are no images, just append the old node as is
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text  #keeping track of the remaining text is useful, as we chop off from the front
        for image_alt, image_url in image_list: #you can go through both elements of the tuples in the list this way
            sections = remaining_text.split(f"![{image_alt}]({image_url})", 1)  #split the text using the image as the delimiter
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = sections[1]
        if remaining_text != "":    
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        link_list = extract_markdown_links(old_node.text)
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if link_list == []:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for link_anchor, link_url in link_list:
            sections = remaining_text.split(f"[{link_anchor}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    return node


