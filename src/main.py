from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter
from markdown_blocks import text_to_children
import os, shutil
from gencontents import generate_page, generate_page_recursive


def static_to_public(source, destination):

    if os.path.exists(destination): #check if the dir exists, if so delete it with all of its contents
        shutil.rmtree(destination)
    
    os.mkdir(destination) #you pass in the directory you want to create -> since destination was deleted, that's what it gets replaced with

    for name in os.listdir(source): #os.listdir returns ONLY NAMES of items, not their full paths
        from_path = os.path.join(source, name) #now from_path is something like "static/index.css"
        to_path = os.path.join(destination, name)

        log_line = f" * {from_path} -> {to_path}" #here we log what we're doing
        print(log_line)
        with open("copy.log", "a") as f: #this setup opens the file a lot (fine for smaller projects)
            f.write(log_line + "\n")



        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path) #we give shutil.copy the FULL path already, so this works nicely
        else:
            static_to_public(from_path, to_path)





    







def main():
    static_to_public("static", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/contact/index.html")

    generate_page_recursive("content", "template.html", "public")

    




if __name__ == "__main__":
    main()