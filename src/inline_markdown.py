from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            text = old_node.text

            if delimiter in text:
                # Count occurrences of delimiter
                delimiter_count = text.count(delimiter)

                # Check for unclosed delimiters
                if delimiter.count % 2 != 0:
                    raise ValueError(f"Invalid markdown: Unclosed delimiter {delimiter}")
                
                # Split and create new nodes
                parts = text.split(delimiter)
                for i in range(len(parts)):
                    if parts[i] == "":
                        continue # Skip empty parts
                    current_type = text_type if i % 2 == 1 else TextType.TEXT
                    result.append(TextNode(parts[i], current_type))
            
            else:
                result.append(old_node)

        else:
            result.append(old_node)

    return result
