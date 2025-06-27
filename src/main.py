from fs_utils import copy_to_destination, generate_pages

def main():
    copy_to_destination("static", "public")
    generate_pages("content", "template.html", "public")

if __name__ == '__main__':
    main()