#!/usr/bin/env python3
"""
Markdown Viewer - Display markdown files as HTML in browser or GUI
"""

import argparse
import sys
import os
import tempfile
import webbrowser
from pathlib import Path
import markdown
import time
import subprocess

# Check for PyWebView availability
try:
    import webview
    PYWEBVIEW_AVAILABLE = True
except ImportError:
    PYWEBVIEW_AVAILABLE = False

# Configurable cleanup delay for temporary files
# Can be overridden via MDVIEW_CLEANUP_DELAY environment variable (in seconds)
# Default is 30 seconds to ensure browsers have time to fully load files
DEFAULT_CLEANUP_DELAY = 30
CLEANUP_DELAY = int(os.environ.get('MDVIEW_CLEANUP_DELAY', DEFAULT_CLEANUP_DELAY))


def cleanup_file_in_background(file_path, delay=CLEANUP_DELAY):
    """
    Schedule a file for deletion in a background process.

    This creates a completely independent subprocess that continues running
    even after the main process exits. Unlike daemon threads (which are killed
    when the main process exits), this subprocess is truly independent.

    In C terms: This is like fork() + exec() to create a child process
    In Java terms: Like ProcessBuilder with inheritIO(false)

    Args:
        file_path: Path to file to delete
        delay: Seconds to wait before deletion
    """
    cleanup_script = f'''
import time
import os
import sys

try:
    time.sleep({delay})
    os.unlink("{file_path}")
except Exception:
    pass  # Silent cleanup - file might already be deleted
'''

    # Spawn completely independent background process
    # - stdout/stderr redirected to /dev/null (no output)
    # - start_new_session=True makes it independent (Unix: new process group)
    # - Process continues even after parent exits
    subprocess.Popen(
        [sys.executable, '-c', cleanup_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True  # Detach from parent (like daemon() in C)
    )


def cleanup_directory_in_background(file_paths, directory, delay=CLEANUP_DELAY):
    """
    Schedule multiple files and a directory for deletion in a background process.

    Args:
        file_paths: List of file paths to delete
        directory: Directory path to remove after files are deleted
        delay: Seconds to wait before deletion
    """
    # Build list of files as Python list literal
    files_str = '[' + ', '.join(f'"{f}"' for f in file_paths) + ']'

    cleanup_script = f'''
import time
import os
import sys

try:
    time.sleep({delay})
    for file_path in {files_str}:
        try:
            os.unlink(file_path)
        except:
            pass
    try:
        os.rmdir("{directory}")
    except:
        pass
except Exception:
    pass  # Silent cleanup
'''

    subprocess.Popen(
        [sys.executable, '-c', cleanup_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

# Embedded README content
EMBEDDED_README = """# MDView - Markdown Viewer

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

## Environment Variables

- `MDVIEW_CLEANUP_DELAY`: Time in seconds to wait before deleting temporary HTML files in browser mode (default: 30).
  Increase this if you experience issues with files being deleted before your browser can load them.

  ```bash
  # Example: Wait 60 seconds before cleanup
  export MDVIEW_CLEANUP_DELAY=60
  mdview -b README.md
  ```

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

## License

This project is open source and available under the MIT License.
"""


def convert_markdown_string_to_html(md_content, title="Markdown Document"):
    """Convert markdown string to HTML string."""
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'tables', 'toc']
    )
    
    # Wrap in basic HTML structure with styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                pre {{
                    background-color: #f4f4f4;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    padding: 10px;
                    overflow-x: auto;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: Consolas, Monaco, 'Courier New', monospace;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                    font-weight: bold;
                }}
                blockquote {{
                    border-left: 4px solid #ddd;
                    margin: 0;
                    padding-left: 20px;
                    color: #666;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    margin-top: 24px;
                    margin-bottom: 16px;
                }}
                a {{
                    color: #0366d6;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    
    return full_html


def convert_markdown_to_html(markdown_file):
    """Convert markdown file to HTML string."""
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        return convert_markdown_string_to_html(md_content, title=Path(markdown_file).name)
    
    except FileNotFoundError:
        print(f"Error: File '{markdown_file}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{markdown_file}': {e}")
        return None


def create_index_html(markdown_files):
    """Create an index HTML page with links to all markdown files."""
    html_files = []
    for md_file in markdown_files:
        html_name = Path(md_file).stem + '.html'
        html_files.append((Path(md_file).name, html_name))
    
    links_html = '\n'.join([
        f'<li><a href="{html_file}">{md_name}</a></li>' 
        for md_name, html_file in html_files
    ])
    
    index_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Markdown Files Index</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
                padding: 10px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            a {{
                color: #0366d6;
                text-decoration: none;
                font-size: 18px;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Markdown Files</h1>
        <ul>
            {links_html}
        </ul>
    </body>
    </html>
    """
    
    return index_html


def create_multi_file_html(markdown_files):
    """Create HTML with tabs for multiple markdown files."""
    # Convert all files
    file_data = []
    for i, md_file in enumerate(markdown_files):
        html_content = convert_markdown_to_html(md_file)
        if html_content:
            # Extract just the body content
            import re
            body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                file_data.append({
                    'id': f'file{i}',
                    'name': Path(md_file).name,
                    'content': body_content
                })
    
    # Create tab buttons
    tab_buttons = '\n'.join([
        f'<button class="tab-button{" active" if i == 0 else ""}" onclick="showTab(\'{f["id"]}\')">{f["name"]}</button>'
        for i, f in enumerate(file_data)
    ])
    
    # Create tab contents
    tab_contents = '\n'.join([
        f'<div id="{f["id"]}" class="tab-content{" active" if i == 0 else ""}">{f["content"]}</div>'
        for i, f in enumerate(file_data)
    ])
    
    multi_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Markdown Viewer - {len(markdown_files)} files</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .tab-bar {{
                background-color: #2c3e50;
                padding: 0;
                margin: 0;
                display: flex;
                overflow-x: auto;
            }}
            .tab-button {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px 24px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
                white-space: nowrap;
            }}
            .tab-button:hover {{
                background-color: #34495e;
            }}
            .tab-button.active {{
                background-color: #3498db;
            }}
            .tab-content {{
                display: none;
                padding: 20px;
                max-width: 900px;
                margin: 0 auto;
            }}
            .tab-content.active {{
                display: block;
            }}
            pre {{
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 10px;
                overflow-x: auto;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: Consolas, Monaco, 'Courier New', monospace;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
                font-weight: bold;
            }}
            blockquote {{
                border-left: 4px solid #ddd;
                margin: 0;
                padding-left: 20px;
                color: #666;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 24px;
                margin-bottom: 16px;
            }}
            a {{
                color: #0366d6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
        <script>
            function showTab(tabId) {{
                // Hide all tabs
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(content => content.classList.remove('active'));
                
                // Remove active from all buttons
                const buttons = document.querySelectorAll('.tab-button');
                buttons.forEach(button => button.classList.remove('active'));
                
                // Show selected tab
                document.getElementById(tabId).classList.add('active');
                
                // Mark button as active
                const activeButton = Array.from(buttons).find(b => 
                    b.onclick.toString().includes(tabId)
                );
                if (activeButton) activeButton.classList.add('active');
            }}
        </script>
    </head>
    <body>
        <div class="tab-bar">
            {tab_buttons}
        </div>
        {tab_contents}
    </body>
    </html>
    """
    
    return multi_html


def display_in_gui(markdown_files):
    """Display markdown files in PyWebView GUI window."""
    if not PYWEBVIEW_AVAILABLE:
        print("Error: PyWebView is not installed. Install it with: pip install pywebview")
        print("Falling back to browser mode...")
        display_in_browser(markdown_files)
        return
    
    if len(markdown_files) == 1:
        # Single file mode
        html_content = convert_markdown_to_html(markdown_files[0])
        if html_content is None:
            return
        
        window_title = f"Markdown Viewer - {Path(markdown_files[0]).name}"
        webview.create_window(window_title, html=html_content)
    else:
        # Multiple files mode with tabs
        html_content = create_multi_file_html(markdown_files)
        window_title = f"Markdown Viewer - {len(markdown_files)} files"
        webview.create_window(window_title, html=html_content)
    
    webview.start()


def display_in_browser(markdown_files, keep_file=False):
    """Display multiple markdown files in the default web browser."""
    if len(markdown_files) == 1:
        # Single file mode
        html_content = convert_markdown_to_html(markdown_files[0])
        if html_content is None:
            return
            
        if keep_file:
            base_name = Path(markdown_files[0]).stem
            html_path = Path.cwd() / f"{base_name}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            webbrowser.open(f'file://{html_path.absolute()}')
            print(f"Opened {markdown_files[0]} in browser")
            print(f"HTML file saved at: {html_path}")
        else:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_path = f.name
            
            webbrowser.open(f'file://{temp_path}')
            print(f"Opened {markdown_files[0]} in browser (temp file will be deleted after {CLEANUP_DELAY}s)")

            # Schedule cleanup in independent background process
            cleanup_file_in_background(temp_path)
    else:
        # Multiple files mode
        temp_files = []
        
        if keep_file:
            # Save all files to current directory
            for md_file in markdown_files:
                html_content = convert_markdown_to_html(md_file)
                if html_content:
                    base_name = Path(md_file).stem
                    html_path = Path.cwd() / f"{base_name}.html"
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"Saved {md_file} as {html_path}")
            
            # Create index
            index_html = create_index_html(markdown_files)
            index_path = Path.cwd() / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            webbrowser.open(f'file://{index_path.absolute()}')
            print(f"\nOpened index page in browser")
            print(f"Index saved at: {index_path}")
        else:
            # Use temporary directory
            temp_dir = tempfile.mkdtemp()
            
            # Convert all markdown files
            for md_file in markdown_files:
                html_content = convert_markdown_to_html(md_file)
                if html_content:
                    base_name = Path(md_file).stem
                    html_path = Path(temp_dir) / f"{base_name}.html"
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    temp_files.append(html_path)
            
            # Create index
            index_html = create_index_html(markdown_files)
            index_path = Path(temp_dir) / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            temp_files.append(index_path)
            
            webbrowser.open(f'file://{index_path.absolute()}')
            print(f"Opened {len(markdown_files)} files in browser (temp files will be deleted after {CLEANUP_DELAY}s)")

            # Schedule cleanup in independent background process
            cleanup_directory_in_background(temp_files, temp_dir)


def main():
    parser = argparse.ArgumentParser(
        description='View markdown files as HTML in browser or GUI'
    )
    parser.add_argument(
        'markdown_files',
        nargs='*',
        help='Path(s) to the markdown file(s) to view'
    )
    parser.add_argument(
        '-b', '--browser',
        action='store_true',
        help='Open in browser instead of GUI (default: GUI if available)'
    )
    parser.add_argument(
        '-k', '--keep',
        action='store_true',
        help='Keep the HTML file(s) when using browser mode (default: delete after viewing)'
    )
    parser.add_argument(
        '-r', '--readme',
        action='store_true',
        help='Display the README.md file'
    )
    
    args = parser.parse_args()
    
    # Collect files to display
    files_to_display = []
    
    # Handle readme display
    if args.readme:
        # Use embedded README content
        readme_html = convert_markdown_string_to_html(EMBEDDED_README, title="MDView README")
        
        if args.browser:
            # Create a temporary file for browser display
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(readme_html)
                temp_path = f.name
            
            webbrowser.open(f'file://{temp_path}')
            print(f"Opened built-in README in browser (temp file will be deleted after {CLEANUP_DELAY}s)")

            # Schedule cleanup in independent background process
            cleanup_file_in_background(temp_path)
        else:
            # Display in GUI
            if PYWEBVIEW_AVAILABLE:
                webview.create_window("MDView README", html=readme_html)
                webview.start()
            else:
                # Fallback to browser if PyWebView not available
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                    f.write(readme_html)
                    temp_path = f.name
                
                webbrowser.open(f'file://{temp_path}')
                print(f"Opened built-in README in browser (PyWebView not available, temp file will be deleted after {CLEANUP_DELAY}s)")

                # Schedule cleanup in independent background process
                cleanup_file_in_background(temp_path)
        
        # Exit after displaying README
        sys.exit(0)
    
    # Add any specified markdown files
    if args.markdown_files:
        for md_file in args.markdown_files:
            if os.path.exists(md_file):
                files_to_display.append(md_file)
            else:
                print(f"Warning: File '{md_file}' not found, skipping.")
    
    # Check if any files were specified
    if not files_to_display:
        parser.print_help()
        sys.exit(1)
    
    # Display based on option
    if args.browser:
        display_in_browser(files_to_display, keep_file=args.keep)
    else:
        display_in_gui(files_to_display)


if __name__ == '__main__':
    main()