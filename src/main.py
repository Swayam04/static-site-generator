from fs_utils import copy_to_destination, generate_pages
import argparse

arg_parser = argparse.ArgumentParser(description="Static Site Generator")
arg_parser.add_argument("-d", "--directory", dest="directory_path", type=str, required=False, default="/",
                        help="Full path of directory to organize.")

def main():
    args = arg_parser.parse_args()
    basepath = args.directory_path
    copy_to_destination("static", "docs")
    generate_pages("content", "template.html", "docs", basepath)

if __name__ == '__main__':
    main()