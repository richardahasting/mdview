# MDView - Markdown Viewer

A Python application to view Markdown files as rendered HTML in a native GUI window or web browser.

## Features

- View single or multiple Markdown files simultaneously
- Native GUI window using PyWebView (when installed)
- Fallback to web browser if GUI dependencies are not available
- Convert Markdown files to HTML with syntax highlighting and table support
- Multi-file support with tabs in GUI mode
- Multi-file browser mode creates an index page with links
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

For GUI mode support (optional but recommended):

```bash
pip install pywebview
```


## Usage

### View Single File

#### GUI Mode (default if PyWebView is installed)
```bash
python mdview.py your_file.md
```

#### Browser Mode
```bash
python mdview.py -b your_file.md
```

### View Multiple Files

#### GUI Mode with Tabs
```bash
python mdview.py file1.md file2.md file3.md
```

#### Browser Mode with Index Page
```bash
python mdview.py -b file1.md file2.md file3.md
```

## Command Line Options

- `markdown_files`: Path(s) to the markdown file(s) to view (accepts multiple files)
- `-b`, `--browser`: Force browser mode instead of GUI
- `-k`, `--keep`: Keep the HTML file(s) instead of auto-deleting after viewing
- `-r`, `--readme`: Display this README.md file
- `-h`, `--help`: Show help message and exit

## Examples

View a single file in GUI:
```bash
python mdview.py README.md
```

View multiple files with tabs:
```bash
python mdview.py docs/*.md
```

Force browser mode:
```bash
python mdview.py -b README.md
```

Keep the generated HTML files:
```bash
python mdview.py -b -k report.md
# Creates report.html in current directory
```

View the built-in README:
```bash
python mdview.py -r
# or in browser
python mdview.py -r -b
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