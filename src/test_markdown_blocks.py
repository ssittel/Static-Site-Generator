import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdowntoBlocks(unittest.TestCase):
    def testsimpleblock(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        actual = markdown_to_blocks(md)
        self.assertEqual(
            actual,
            ["# This is a heading",
             "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
             "- This is the first list item in a list block\n- This is a list item\n- This is another list item"]
        )

    def testtoomanynewlines(self):
        md = """# This is a heading

        
This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


- This is the first list item in a list block
- This is a list item
- This is another list item"""
        actual = markdown_to_blocks(md)
        self.assertEqual(
            actual,
            ["# This is a heading",
             "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
             "- This is the first list item in a list block\n- This is a list item\n- This is another list item"]
        )

    def testmissingnewline(self):
        md = """# This is a heading
This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        actual = markdown_to_blocks(md)
        self.assertEqual(
            actual,
            ["# This is a heading\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
             "- This is the first list item in a list block\n- This is a list item\n- This is another list item"]
        )


class TestBlocksToBlockType(unittest.TestCase):
    def testheadingsnormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[0])
        self.assertEqual(actual, BlockType.HEADING)
        
    def testheadingsbroken(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[1])
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def testcodenormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[2])
        self.assertEqual(actual, BlockType.CODE)

    def testcodebroken(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[3])
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def testquotenormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[4])
        self.assertEqual(actual, BlockType.QUOTE)

    def testalsoquotenormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[5])
        self.assertEqual(actual, BlockType.QUOTE)

    def testulistnormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list\n- Next element\n- last element""",
            """- This is a failed unordered list\nwhere the second line\n- is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[6])
        self.assertEqual(actual, BlockType.UNORDERED_LIST)

    def testulistbroken(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list
            2. starts with
            3. numbers""",
            """1. this ordered list
            3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[7])
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def testolistnormal(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list\n2. starts with\n3. numbers""",
            """1. this ordered list\n3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[8])
        self.assertEqual(actual, BlockType.ORDERED_LIST)

    def testolistbroken(self):
        list_of_blocks = [
            "# This is a heading",
            "##This is a failed heading",
            "```\nThis is some code```",
            "````\nFailed code``",
            "> This is a quote",
            ">This is also a quote",
            """- This is an unordered list
            - Next element
            - last element""",
            """- This is a failed unordered list
            where the second line
            - is missing a dash""",
            """1. an ordered list\n2. starts with\n3. numbers""",
            """1. this ordered list\n3. will fail"""
        ]
        actual = block_to_block_type(list_of_blocks[9])
        self.assertEqual(actual, BlockType.PARAGRAPH)


class TestMarkdowntoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is *bolded* paragraph
text in a p
tag here

This is another paragraph with __italic__ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the *same* even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe *same* even with inline stuff\n</code></pre></div>",
        )
        
    def test_ul(self):
        md = """
- This is *bold* text that should appear
- in the format of
- an unordered list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bold</b> text that should appear</li><li>in the format of</li><li>an unordered list</li></ul></div>",
        )