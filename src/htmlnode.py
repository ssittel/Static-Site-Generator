

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'HTMLNode(tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props})'


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props: #covers both "None" and an empty dict
            return ""
        string_to_return = ""
        for key, value in self.props.items():
            string_to_return = string_to_return + f' {key}="{value}"'
        return string_to_return


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        tag_open = f"<{self.tag}{self.props_to_html()}>"
        tag_close = f"</{self.tag}>"
        return f"{tag_open}{self.value}{tag_close}"
    
    def __repr__(self):
        return f'LeafNode(tag= {self.tag}, value= {self.value}, props= {self.props})'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("Please provide a tag")
        if self.children is None:
            raise ValueError("Instances of the ParentNode class must have children")
        
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
