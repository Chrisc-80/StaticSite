import unittest
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links
)

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_node_unchanged(self):
        # Test that non-TEXT nodes are left unchanged
        node = TextNode("**bold text**", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "**bold text**")
        self.assertEqual(result[0].text_type, TextType.BOLD)
    
    def test_text_node_without_delimiter(self):
        # Test that TEXT nodes without the delimiter remain unchanged
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_text_node_with_delimiters(self):
        # Test splitting a TEXT node with delimiters
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiter_pairs(self):
        # Test multiple delimiter pairs in a single node
        node = TextNode("Text with `code` and more `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(result), 4)
        # Add assertions for each part
    
    def test_bold_delimiter(self):
        # Test with a different delimiter (bold)
        node = TextNode("Text with **bold** words", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        # Add assertions for each part
    
    def test_unclosed_delimiter(self):
        # Test that an error is raised for unclosed delimiters
        node = TextNode("Text with unclosed `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()