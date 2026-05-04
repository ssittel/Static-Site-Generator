import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path
#from htmlnode import to_html -> this is not needed, as importing an object (markdown_to_html_node returns a ParentNode) automatically brings that
#objects class and its associated properties with it

def extract_title(markdown): #string processing function for the markdown we get from generate_page
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception('no h1 header found')



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path) as f: #using the with block is idomatic in Python as the file is then close as soon as reading it is done
        md_file_contents = f.read()
    
    with open(template_path) as f:
        templ_file_contents = f.read()

    html_string = markdown_to_html_node(md_file_contents).to_html()
    page_title = extract_title(md_file_contents)

    templ_file_contents_upd = templ_file_contents.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(templ_file_contents_upd)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path): #dir_path_content is our content-dir -> all the subdirs are visible from here
    stuff_in_current_dir = os.listdir(dir_path_content)

    for thing in stuff_in_current_dir:
        from_path = os.path.join(dir_path_content, thing) #only full_path, if we've gotten to the last subdir/file
        dest_path = os.path.join(dest_dir_path, thing) #we mirror the subdirs in our dest-folder

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html") #we need to change the suffix. in generate_this is taken care of with the inputs
            generate_page(from_path, template_path, dest_path)
        else:
            generate_page_recursive(from_path, template_path, dest_path)



   
    