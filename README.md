# Flash Page

**Flash Page** is a custom Python-based Static Site Generator (SSG). It takes raw Markdown content and a customizable HTML template, and generates a complete static website ready for deployment. The project is designed to be lightweight, easy to understand, and relies on built-in Python libraries without external dependencies for its core generation features.

## Features

- **Markdown Parsing:** Recursively processes directories of Markdown files (`.md`) and converts them into structurally matching HTML files.
- **Custom HTML Templates:** Uses a simple `{{ Title }}` and `{{ Content }}` interpolation system to generate comprehensive HTML pages.
- **Static Assets Management:** Automatically copies images, stylesheets, and other static files from a `static/` directory to the output directory.
- **Basepath Support:** Allows configuration of a base path (e.g., `"/flash_page/"`) making it perfectly suited for deployments on GitHub Pages or nested subdirectories.
- **Dependency-Free Core:** Written in pure Python without requiring large external libraries like `Hugo` or `Jekyll`.

## Project Structure

```text
flash_page/
├── src/                    # Python source code for the markdown compiler
│   ├── main.py             # Main entry point for the site generation
│   ├── block_markdown.py   # Text and block markdown parsing logic
│   └── ...                 # Other parsing utilities (e.g. textnode.py)
├── content/                # Directory containing your Markdown files
├── static/                 # Directory for static assets (CSS, images)
├── docs/                   # The generated static HTML site (Output directory)
├── template.html           # The base HTML template
├── build.sh                # Shell script to build the site with GitHub Pages base path
├── main.sh                 # Shell script to build and serve the site locally
└── test.sh                 # Shell script to run unit tests
```

## Prerequisites

- **Python 3.x** is required to run the site generation scripts.

## Usage

### 1. Local Development

To build the static site and test it locally, you can use the provided bash scripts.

Run the main script to start a local web server:

```bash
./main.sh
```

*Note: The script currently defaults to building the output into the `docs/` folder instead of `public/` to support direct GitHub Pages deployments from the `docs` branch folder.*

### 2. Building for Production (GitHub Pages)

If you are deploying to GitHub Pages under a repository name like `https://<username>.github.io/flash_page/`, you need to build the site with the correct base path so structural links and assets resolve correctly.

Run the build script:

```bash
./build.sh
```

This will run `python3 src/main.py "/flash_page/"`, creating the site in the `docs/` directory. You can then configure GitHub Pages to serve from the `docs/` folder on your `main` branch.

### 3. Running Tests

The project includes a suite of unit tests to ensure the Markdown parsing logic functions correctly. To run the tests:

```bash
./test.sh
```

## How It Works

1. **Clean up:** The script starts by recursively deleting the existing `docs/` directory to ensure a clean slate.
2. **Static Assets:** It copies all files and folders from `static/` into `docs/`.
3. **Generation:** It recursively crawls the `content/` directory.
4. **Parsing:** For every `.md` file, it:
   - Reads the Markdown.
   - Converts the Markdown into an internal AST (Abstract Syntax Tree) using `TextNode` and HTML node representations.
   - Serializes the AST to raw HTML.
   - Extracts the primary `<h1>` header to use as the page title.
5. **Templating:** It injects the generated HTML and Title into `template.html`.
6. **Writing:** It outputs the final `.html` file into the `docs/` directory, mirroring the original directory structure from `content/`.

## License

This project is open-source and available under the [MIT License](LICENSE).
