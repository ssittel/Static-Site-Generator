from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    list_of_blocks = []
    raw_blocks = markdown.split('\n\n')
    for block in raw_blocks:
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        list_of_blocks.append(stripped_block)
    return list_of_blocks


def block_to_block_type(markdown_block): #make sure to just feed a singular markdown_block, not a list
    if markdown_block.startswith(("# ", "## ", "### ","#### ", "##### ", "###### ")): #.startswith can accept a tuple
        return BlockType.HEADING
    
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    if markdown_block.startswith(">"):
        lines = markdown_block.split('\n')
        for line in lines:
            if line.startswith(">") != True:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if markdown_block.startswith("- "):
        lines = markdown_block.split('\n')
        for line in lines:
            if line.startswith("- ") != True:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if markdown_block.startswith("1. "):
        lines = markdown_block.split('\n')

        for index, line in enumerate(lines):
            if line.startswith(f"{index + 1}. ") != True:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
            
    return BlockType.PARAGRAPH

#from here Block to HTML stuff starts

def markdown_to_html_node(markdown):
    list_of_blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in list_of_blocks:
        type_of_block = block_to_block_type(block) #call this function once, so we can just check the BlockType later
        if type_of_block == BlockType.PARAGRAPH:
            lines = block.split("\n")
            block_wo_newlines = " ".join(lines) #we wanted to remove the newlines and put in spaces instead
            children = text_to_children(block_wo_newlines)
            parent_node = ParentNode("p", children)
            block_nodes.append(parent_node)
        
        elif type_of_block == BlockType.HEADING:
            count, formatted_block = prepare_headings(block)
            tag = f"h{count}"
            children = text_to_children(formatted_block)
            parent_node = ParentNode(tag, children)
            block_nodes.append(parent_node)

        elif type_of_block == BlockType.QUOTE:
            formatted_block = prepare_quote(block)
            children = text_to_children(formatted_block)
            parent_node = ParentNode("blockquote", children)
            block_nodes.append(parent_node)

        elif type_of_block == BlockType.UNORDERED_LIST:
            parent_node = prepare_uls(block)
            block_nodes.append(parent_node)

        elif type_of_block == BlockType.ORDERED_LIST:
            parent_node = prepare_ols(block)
            block_nodes.append(parent_node)

        elif type_of_block == BlockType.CODE:
            parent_node = prepare_code(block)
            block_nodes.append(parent_node)

    return ParentNode("div", block_nodes) #wrap everything in <div> tag at the end



#central helper function

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

#helper functions for different block types

def prepare_headings(raw_block): #feed in the textblock from the list of blocks, remove the #s and also count them
    split_text = raw_block.split(" ", 1)
    count = len(split_text[0])
    formatted_block = split_text[1]
    return count, formatted_block

def prepare_quote(raw_block):
    formatted_block = ""
    lines = raw_block.split("\n") #each line starts with ">" or "> "
    for line in lines:
        if line.startswith("> "):
            line = line[2:]
        elif line.startswith(">"):
            line = line[1:]
        formatted_block += f"{line} " 
    return formatted_block.strip()

def prepare_uls(raw_block): 
    li_nodes = []
    lines = raw_block.split("\n")
    for line in lines:
        line = line[2:]
        children = text_to_children(line)
        inner_parent_node = ParentNode("li", children)
        li_nodes.append(inner_parent_node)
    outer_parent_node = ParentNode("ul", li_nodes)
    return outer_parent_node

def prepare_ols(raw_block): 
    li_nodes = []
    lines = raw_block.split("\n")
    for line in lines:
        line = line[3:]
        children = text_to_children(line)
        inner_parent_node = ParentNode("li", children)
        li_nodes.append(inner_parent_node)
    outer_parent_node = ParentNode("ol", li_nodes)
    return outer_parent_node

def prepare_code(raw_block):
    stripped_text = raw_block[4:-3] #slice of "```\n" from the start and "```" from the back
    node = TextNode(stripped_text, TextType.TEXT)
    html_node = text_node_to_html_node(node)
    inner_parent_node = ParentNode("code", [html_node]) #wrap html node in <code> tag, ParentNode expects a list as input
    outer_parent_node = ParentNode("pre", [inner_parent_node]) #wrap in <pre> tag
    return outer_parent_node




