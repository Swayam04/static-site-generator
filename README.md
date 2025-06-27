# Static Site Generator

A Python-based static site generator that converts Markdown content into a complete HTML website with CSS styling and static assets.

## Features

- **Markdown to HTML Conversion**: Supports headers, paragraphs, lists, code blocks, quotes, and inline formatting
- **Template System**: Uses HTML templates with placeholder substitution
- **Static Asset Management**: Automatically copies CSS, images, and other static files
- **Recursive Directory Processing**: Maintains directory structure from content to output
- **Inline Formatting Support**: Bold, italic, code, links, and images
- **Built-in Development Server**: Includes local server for testing

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Unix-like environment (Linux, macOS, WSL)

### Installation

1. Clone or download this repository
2. No additional dependencies required - uses Python standard library only

### Usage

#### Build the Site

```bash
python3 src/main.py
```

This will:
1. Clear the `public/` directory
2. Copy all files from `static/` to `public/`
3. Convert all `.md` files in `content/` to `.html` files in `public/`
4. Maintain the directory structure

#### Build and Serve

```bash
./main.sh
```

This will build the site and start a local development server at `http://localhost:8888`

#### Run Tests

```bash
./test.sh
```

Or run individual test files:
```bash
python3 src/test_md_parser.py
```

## Supported Markdown Features

### Block Elements

- **Headings**: `# H1` through `###### H6`
- **Paragraphs**: Regular text blocks
- **Code Blocks**: Fenced with triple backticks (\`\`\`)
- **Blockquotes**: Lines starting with `>`
- **Unordered Lists**: Lines starting with `*` or `-`
- **Ordered Lists**: Lines starting with `1.`, `2.`, etc.

### Inline Elements

- **Bold**: `**text**`
- **Italic**: `*text*`
- **Code**: `` `text` ``
- **Links**: `[text](url)`
- **Images**: `![alt text](url)`

## Directory Structure Requirements

### Content Directory (`content/`)

Place your Markdown files here. The directory structure will be preserved in the output:

```
content/
├── index.md              # → public/index.html
├── about.md              # → public/about.html
└── blog/
    ├── post1.md          # → public/blog/post1.html
    └── post2.md          # → public/blog/post2.html
```

### Static Directory (`static/`)

Place CSS, images, and other static assets here:

```
static/
├── index.css             # → public/index.css
├── script.js             # → public/script.js
└── images/
    └── photo.jpg         # → public/images/photo.jpg
```

## Development

### Running Tests

The project includes comprehensive unit tests:

```bash
# Run all tests
./test.sh

# Run specific test module
python3 src/test_md_parser.py
python3 src/test_md_to_html.py
```

### Adding New Features

1. **New Markdown Elements**: Extend the parsing logic in `md_parser.py`
2. **New Block Types**: Add to `BlockType` enum in `blocktype.py`
3. **HTML Modifications**: Extend HTML node classes in `htmlnode.py`

## License

This project is part of a course at [boot.dev](https://www.boot.dev/courses/build-static-site-generator-python).
