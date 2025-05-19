import unittest

from textnode import TextNode, TextType, text_to_textnodes


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_eq2(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_text_to_textnode(self):
		result = text_to_textnodes(
			"This is **text** with an _italic_ word and a `code block`
			and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
			)
		expected = [
    	TextNode("This is ", TextType.TEXT),
    	TextNode("text", TextType.BOLD),
    	TextNode(" with an ", TextType.TEXT),
    	TextNode("italic", TextType.ITALIC),
    	TextNode(" word and a ", TextType.TEXT),
    	TextNode("code block", TextType.CODE),
    	TextNode(" and an ", TextType.TEXT),
    	TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    	TextNode(" and a ", TextType.TEXT),
    	TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertEqual(result, expected)

if __name__ == "__main__":
	unittest.main()
