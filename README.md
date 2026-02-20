# MDView - Markdown Viewer

A Python application to view Markdown files as rendered HTML in your system browser or a native GUI window.

## Features

- View single or multiple Markdown files simultaneously
- Opens in system browser by default (no extra dependencies needed)
- Native GUI window using PyWebView via `-g/--gui` flag (optional)
- Convert Markdown files to HTML with syntax highlighting and table support
- Multi-file browser mode creates an index page with links
- Multi-file GUI mode provides a tabbed interface
- Support for common Markdown extensions (tables, code highlighting, etc.)
- Option to keep generated HTML files or auto-delete after viewing

## Installation

### Quick Install (Recommended)

Download and run the self-contained installer:

```bash
# Download the installer
curl -O https://raw.githubusercontent.com/your-repo/mdview/main/mdview_installer.py

# Run the installer
python3 mdview_installer.py
```

The installer will:
- Detect your system and package manager (pip/pipx)
- Check for existing installations
- Install to your preferred location
- Add mdview to your PATH

### Manual Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

For GUI mode support (optional):

```bash
pip install pywebview
```


## Usage

### View Single File

#### Browser Mode (default)
```bash
python mdview.py your_file.md
```

#### GUI Mode (requires pywebview)
```bash
python mdview.py -g your_file.md
```

### View Multiple Files

#### Browser Mode with Index Page
```bash
python mdview.py file1.md file2.md file3.md
```

#### GUI Mode with Tabs
```bash
python mdview.py -g file1.md file2.md file3.md
```

## Command Line Options

- `markdown_files`: Path(s) to the markdown file(s) to view (accepts multiple files)
- `-g`, `--gui`: Open in native GUI window using PyWebView (requires pywebview)
- `-k`, `--keep`: Keep the HTML file(s) instead of auto-deleting after viewing
- `-r`, `--readme`: Display this README.md file
- `-h`, `--help`: Show help message and exit

## Environment Variables

- `MDVIEW_CLEANUP_DELAY`: Time in seconds to wait before deleting temporary HTML files (default: 30).
  Increase this if your browser is slow to load files before they are cleaned up.

  ```bash
  # Example: Wait 60 seconds before cleanup
  export MDVIEW_CLEANUP_DELAY=60
  mdview README.md
  ```

## Examples

View a single file in browser (default):
```bash
python mdview.py README.md
```

View multiple files with an index page:
```bash
python mdview.py docs/*.md
```

Open in native GUI window:
```bash
python mdview.py -g README.md
```

Keep the generated HTML files:
```bash
python mdview.py -k report.md
# Creates report.html in current directory
```

View the built-in README:
```bash
python mdview.py -r
# or in GUI window
python mdview.py -r -g
```

## Dependencies

- **markdown**: For converting Markdown to HTML
- **pywebview** (optional): For native GUI window display

## Building

To build the self-contained installer:

```bash
bash build.sh
```

This will:
1. Generate the `mdview_installer.py` with embedded source code
2. Create distribution packages
3. Run tests to verify functionality

## License

This project is open source and available under the Apache License 2.0.