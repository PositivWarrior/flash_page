import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is *italic* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_error_no_closing(self):
        node = TextNode("This has no **closing", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()