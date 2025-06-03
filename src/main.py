from textnode import *

def main():
    dummy_text = 'Gandalf the Gray'
    dummy_type = TextType.TEXT
    dummy_url = 'https://www.middleearth.com'
    dummy_node = TextNode(dummy_text, dummy_type, dummy_url)
    print(dummy_node)

if __name__ == '__main__':
    main()