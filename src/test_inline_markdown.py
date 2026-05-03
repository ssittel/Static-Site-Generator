import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineSplitDelimiter(unittest.TestCase):
    def test_code_delimiters(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)]
        self.assertEqual(actual, expected)


    def test_bold_delimiters(self):
        node = TextNode("This is text with a *bold* word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [TextNode("This is text with a ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" word", TextType.TEXT, None)]
        self.assertEqual(actual, expected)

    def test_italic_delimiters(self):
        node = TextNode("This is text with a __italic__ word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "__", TextType.ITALIC)
        expected = [TextNode("This is text with a ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word", TextType.TEXT, None)]
        self.assertEqual(actual, expected)

    def test_no_delimiters(self):
        node = TextNode("This is text with a normal word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a normal word", TextType.TEXT, None)]
        self.assertEqual(actual, expected)

    def test_unclosed_delimiters(self):
        node = TextNode("This is text with a `unclosed word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "`", TextType.CODE)

    def test_multiple_delimiters(self):
        node = TextNode("This is __text__ with a __italic__ word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "__", TextType.ITALIC)
        expected = [TextNode("This is ", TextType.TEXT, None), TextNode("text", TextType.ITALIC, None), TextNode(" with a ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word", TextType.TEXT, None)]
        self.assertEqual(actual, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_one_markdown_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_two_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and here is another one ![img](www.boots.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("img", "www.boots.png")], matches)

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images("There is no image here at all")
        self.assertEqual([], matches)




class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_one_markdown_link(self):
        matches = extract_markdown_links("This is text with a link to [boot dev](https://boot.dev)")
        self.assertListEqual([("boot dev", "https://boot.dev")], matches)

    def test_extract_two_markdown_links(self):
        matches = extract_markdown_links("This is text with links to [boot dev](https://boot.dev) and to [yt](https://youtube.com)")
        self.assertListEqual([("boot dev", "https://boot.dev"), ("yt", "https://youtube.com")], matches)

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links("There is no link here at all")
        self.assertEqual([], matches)

    def test_ignore_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) but no links!")
        self.assertEqual([], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_one_image(self):
        old_nodes = [TextNode("This is a text with an ![image](www.image.com) and some more text!", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode(" and some more text!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_two_image(self):
        old_nodes = [TextNode("This is a text with an ![image](www.image.com) and another ![image2](www.image2.com) and some more text!", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "www.image2.com"),
                TextNode(" and some more text!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_no_images(self):
        old_nodes = [TextNode("This is a text with no images :(", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with no images :(", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_start_with_image(self):
        old_nodes = [TextNode("![image](www.yoda.com) This is a text with an!", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
                TextNode(" This is a text with an!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_ends_with_image(self):
        old_nodes = [TextNode("This is a text with an ![image](www.yoda.com)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [   
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
            ],
            new_nodes,
        )

    def test_only_an_image(self):
        old_nodes = [TextNode("![image](www.yoda.com)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [   
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        old_nodes = [TextNode("![image](www.yoda.com)", TextType.TEXT),
                     TextNode("Blablabla", TextType.TEXT),
                     TextNode("Haha ![catpic](www.cute_cats.com), aww", TextType.TEXT)
                     ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
                TextNode("Blablabla", TextType.TEXT),
                TextNode("Haha ", TextType.TEXT),
                TextNode("catpic", TextType.IMAGE, "www.cute_cats.com"),
                TextNode(", aww", TextType.TEXT)
            ],
            new_nodes
        )

    def test_images_and_links(self):
        old_nodes = [TextNode("![image](www.yoda.com)", TextType.TEXT),
                     TextNode("Blablabla", TextType.TEXT),
                     TextNode("Haha [catpics](www.cute_cats.com), aww", TextType.TEXT)
                     ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
                TextNode("Blablabla", TextType.TEXT),
                TextNode("Haha [catpics](www.cute_cats.com), aww", TextType.TEXT),
            ],
            new_nodes
        )

    def test_adjacent_images(self):
        old_nodes = [TextNode("Blablabla ![image](www.yoda.com)![cats](catpics.com)", TextType.TEXT),
                     ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("Blablabla ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.yoda.com"),
                TextNode("cats", TextType.IMAGE, "catpics.com"),
            ],
            new_nodes
        )

    def test_non_text_type(self):
        old_nodes = [TextNode("This is a text with an ![image](www.image.com) and some more text!", TextType.BOLD)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an ![image](www.image.com) and some more text!", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_empty_string(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_malformed_markdown(self):
        old_nodes = [TextNode("![image](www.image.com", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("![image](www.image.com", TextType.TEXT)
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_one_link(self):
        old_nodes = [TextNode("This is a text with an [link](www.link.com) and some more text!", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.link.com"),
                TextNode(" and some more text!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_two_link(self):
        old_nodes = [TextNode("This is a text with an [link](www.link.com) and another [link2](www.link2.com) and some more text!", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.link.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "www.link2.com"),
                TextNode(" and some more text!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_no_links(self):
        old_nodes = [TextNode("This is a text with no links :(", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with no links :(", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_start_with_link(self):
        old_nodes = [TextNode("[link](www.yoda.com) This is a text with an!", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "www.yoda.com"),
                TextNode(" This is a text with an!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_ends_with_link(self):
        old_nodes = [TextNode("This is a text with an [link](www.yoda.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [   
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.yoda.com"),
            ],
            new_nodes,
        )

    def test_only_an_link(self):
        old_nodes = [TextNode("[link](www.yoda.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [   
                TextNode("link", TextType.LINK, "www.yoda.com"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        old_nodes = [TextNode("[link](www.yoda.com)", TextType.TEXT),
                     TextNode("Blablabla", TextType.TEXT),
                     TextNode("Haha [catpic](www.cute_cats.com), aww", TextType.TEXT)
                     ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "www.yoda.com"),
                TextNode("Blablabla", TextType.TEXT),
                TextNode("Haha ", TextType.TEXT),
                TextNode("catpic", TextType.LINK, "www.cute_cats.com"),
                TextNode(", aww", TextType.TEXT)
            ],
            new_nodes
        )

    def test_images_and_links(self):
        old_nodes = [TextNode("[link](www.yoda.com)", TextType.TEXT),
                     TextNode("Blablabla", TextType.TEXT),
                     TextNode("Haha ![catpics](www.cute_cats.com), aww", TextType.TEXT)
                     ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "www.yoda.com"),
                TextNode("Blablabla", TextType.TEXT),
                TextNode("Haha ![catpics](www.cute_cats.com), aww", TextType.TEXT),
            ],
            new_nodes
        )

    def test_adjacent_links(self):
        old_nodes = [TextNode("Blablabla [link](www.yoda.com)[cats](catpics.com)", TextType.TEXT),
                     ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("Blablabla ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.yoda.com"),
                TextNode("cats", TextType.LINK, "catpics.com"),
            ],
            new_nodes
        )

    def test_non_text_type(self):
        old_nodes = [TextNode("This is a text with an [link](www.link.com) and some more text!", TextType.BOLD)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is a text with an [link](www.link.com) and some more text!", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_empty_string(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_malformed_markdown(self):
        old_nodes = [TextNode("[link](www.link.com", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("[link](www.link.com", TextType.TEXT)
            ],
            new_nodes,
        )



class TestTexttoTextNode(unittest.TestCase):
    def test_mixed_string(self):
        text = "This is some *bold* text and some __italic__ text and also some `code` as an example."
        actual = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text and some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text and also some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" as an example.", TextType.TEXT)
            ],
            actual
        )

    def test_regular_string(self):
        text = "This is some text with no special formatting."
        actual = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is some text with no special formatting.", TextType.TEXT)
            ],
            actual
        )

    def test_link_and_image(self):
        text = "Some *bold* text as well as an ![image](www.img.png) and a [link](www.link.com)"
        actual = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text as well as an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.img.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.link.com")
            ],
            actual
        )