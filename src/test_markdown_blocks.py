import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md = "### This is Heading"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```This is Code```"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = ">This is Quote line one\n>This is Quote line two"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = "- This is unordered list line one\n- This is unordered list line two\n- This is unordered list line three"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.UNORDERED_LIST)

         def test_block_to_block_type_unordered_list(self):
        md = "- This is unordered list line one\n- This is unordered list line two\n- This is unordered list line three"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.UNORDERED_LIST)

if __name__ == "__main__":
    unittest.main()