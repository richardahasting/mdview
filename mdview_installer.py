#!/usr/bin/env python3
"""
MDView Installer - Everything you need to install MDView in one file!

Just run: python3 mdview_installer.py

MDView is a Python application to view Markdown files as rendered HTML in a 
native GUI window or web browser.

Created with ❤️ for the Markdown community
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_banner():
    """Print a nice banner."""
    banner = f"""
{BLUE}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {BOLD}███╗   ███╗██████╗ ██╗   ██╗██╗███████╗██╗    ██╗{RESET}{BLUE}         ║
║  {BOLD}████╗ ████║██╔══██╗██║   ██║██║██╔════╝██║    ██║{RESET}{BLUE}         ║
║  {BOLD}██╔████╔██║██║  ██║██║   ██║██║█████╗  ██║ █╗ ██║{RESET}{BLUE}         ║
║  {BOLD}██║╚██╔╝██║██║  ██║╚██╗ ██╔╝██║██╔══╝  ██║███╗██║{RESET}{BLUE}         ║
║  {BOLD}██║ ╚═╝ ██║██████╔╝ ╚████╔╝ ██║███████╗╚███╔███╔╝{RESET}{BLUE}         ║
║  {BOLD}╚═╝     ╚═╝╚═════╝   ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝{RESET}{BLUE}         ║
║                                                              ║
║            {YELLOW}Markdown Viewer Installation Script{BLUE}               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def check_python_version():
    """Check if Python version is 3.6 or higher."""
    if sys.version_info < (3, 6):
        print(f"{RED}Error: Python 3.6 or higher is required.{RESET}")
        print(f"Your version: Python {sys.version}")
        sys.exit(1)


def check_directory_writable(directory_path):
    """
    Check if a directory is writable by the current user.
    
    Args:
        directory_path (Path): Path to check
        
    Returns:
        bool: True if writable, False otherwise
    """
    try:
        # Convert to Path object if it's a string
        path = Path(directory_path)
        
        # If directory doesn't exist, check if parent is writable
        if not path.exists():
            parent = path.parent
            if not parent.exists():
                return False
            return os.access(parent, os.W_OK)
        
        # If directory exists, check if it's writable
        return os.access(path, os.W_OK)
    except (OSError, PermissionError):
        return False


def find_writable_user_directory():
    """
    Find a writable directory for user installation.
    
    Returns:
        tuple: (Path, bool) - (directory_path, needs_sudo)
    """
    # List of preferred directories in order of preference
    candidates = []
    
    if sys.platform == "win32":
        candidates = [
            Path.home() / "AppData" / "Local" / "Programs" / "mdview",
            Path.home() / "bin",
            Path.cwd() / "mdview_install"
        ]
    else:
        candidates = [
            Path.home() / "bin", 
            Path.home() / ".local" / "bin",
            Path.home() / ".bin",
            Path.cwd() / "mdview_install"
        ]
    
    for candidate in candidates:
        if check_directory_writable(candidate):
            print(f"    {GREEN}✓ Found writable directory: {candidate}{RESET}")
            return candidate, False
        else:
            print(f"    {YELLOW}⚠ Directory not writable: {candidate}{RESET}")
    
    # If no user directories are writable, suggest system directories
    print(f"    {YELLOW}No user directories are writable. System installation may be needed.{RESET}")
    if sys.platform == "win32":
        return Path("C:/Program Files/mdview"), True
    else:
        # Try system directories in order of preference
        system_candidates = [
            Path("/usr/local/bin"),
            Path("/opt/local/bin"),  # MacPorts
            Path("/usr/bin"),        # System bin (last resort)
        ]
        
        for sys_candidate in system_candidates:
            if sys_candidate.exists() or check_directory_writable(sys_candidate.parent):
                print(f"    {YELLOW}Using system directory: {sys_candidate}{RESET}")
                return sys_candidate, True
        
        # Final fallback
        print(f"    {YELLOW}Using default system directory: /usr/local/bin{RESET}")
        return Path("/usr/local/bin"), True


def is_pipx_available():
    """
    Check if pipx is available on the system.

    Returns:
        bool: True if pipx is available, False otherwise
    """
    # Method 1: Check if pipx is in PATH
    if shutil.which("pipx") is not None:
        try:
            # Method 2: Try to run pipx --version to confirm it works
            result = subprocess.run(
                ["pipx", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    return False


def check_pipx():
    """Check if pipx is available."""
    return is_pipx_available()


def is_pip_available():
    """
    Check if pip is available on the system.
    
    Returns:
        bool: True if pip is available, False otherwise
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

def install_dependencies():
    """Install required dependencies with pip/pipx detection."""
    print(f"\n{YELLOW}Installing dependencies...{RESET}")
    
    # Check what's available
    pip_available = is_pip_available()
    pipx_available = is_pipx_available()
    
    print(f"  • Checking package managers:")
    print(f"    {GREEN if pip_available else RED}{'✓' if pip_available else '✗'} pip {'available' if pip_available else 'not available'}{RESET}")
    print(f"    {GREEN if pipx_available else RED}{'✓' if pipx_available else '✗'} pipx {'available' if pipx_available else 'not available'}{RESET}")
    
    if not pip_available and not pipx_available:
        print(f"\n{RED}✗ Neither pip nor pipx is available!{RESET}")
        print(f"{YELLOW}Please install pip or pipx first:{RESET}")
        print(f"  • For pip: https://pip.pypa.io/en/stable/installation/")
        print(f"  • For pipx: https://pypa.github.io/pipx/installation/")
        return False
    
    if not pip_available and pipx_available:
        print(f"\n{YELLOW}⚠ Only pipx is available. Note that pipx cannot install Python libraries.{RESET}")
        print(f"{YELLOW}The markdown library is required for MDView to function.{RESET}")
        print(f"{YELLOW}Consider installing pip or using pipx to install the packaged version of MDView.{RESET}")
        return False
    
    # Check if user site-packages directory is writable
    try:
        import site
        user_site = Path(site.getusersitepackages())
        if user_site.exists() and not check_directory_writable(user_site):
            print(f"    {YELLOW}⚠ User site-packages directory not writable: {user_site}{RESET}")
        elif not user_site.exists():
            # Check if parent directory is writable for creation
            if not check_directory_writable(user_site.parent):
                print(f"    {YELLOW}⚠ Cannot create user site-packages directory{RESET}")
    except Exception:
        print(f"    {YELLOW}⚠ Could not check user site-packages directory{RESET}")
    
    # Required dependency
    print("  • Installing markdown library...")
    try:
        # Try with --user first
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "markdown>=3.4.0"], 
                      capture_output=True, check=True)
        print(f"    {GREEN}✓ markdown installed{RESET}")
    except subprocess.CalledProcessError:
        try:
            # If that fails, try with --break-system-packages --user
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--user", "markdown>=3.4.0"], 
                          capture_output=True, check=True)
            print(f"    {GREEN}✓ markdown installed{RESET}")
        except subprocess.CalledProcessError as e:
            print(f"    {RED}✗ Failed to install markdown{RESET}")
            print(f"    Error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            print(f"    {YELLOW}Note: You may need to install manually: pip install --user markdown{RESET}")
            if pipx_available:
                print(f"    {YELLOW}pipx cannot install libraries. Consider using the packaged version of MDView.{RESET}")
            return False
    
    # Optional dependency
    print("\n  • Installing pywebview (optional, for GUI mode)...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "pywebview>=5.0"], 
                      check=True, capture_output=True)
        print(f"    {GREEN}✓ pywebview installed (GUI mode available){RESET}")
    except:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--user", "pywebview>=5.0"], 
                          check=True, capture_output=True)
            print(f"    {GREEN}✓ pywebview installed (GUI mode available){RESET}")
        except:
            print(f"    {YELLOW}⚠ pywebview not installed (browser mode only){RESET}")
    
    return True

def get_install_location(auto_install=False, install_path=None):
    """Get installation location with simplified, direct approach."""
    
    # Handle command line arguments first
    if install_path:
        path = Path(install_path).expanduser()
        print(f"\n{YELLOW}Using custom installation path: {path}{RESET}")
        needs_sudo = not check_directory_writable(path.parent if not path.exists() else path)
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path, needs_sudo
        except (PermissionError, OSError):
            return path, True
    
    if auto_install:
        # Auto mode: pick the best user directory automatically
        user_dir = Path.home() / ".local" / "bin"
        print(f"\n{YELLOW}Auto-installing to: {user_dir}{RESET}")
        try:
            user_dir.mkdir(parents=True, exist_ok=True)
            return user_dir, False
        except (PermissionError, OSError):
            return user_dir, True
    
    # Interactive mode: ask user directly
    print(f"\n{YELLOW}Where would you like to install MDView?{RESET}")
    
    # Prepare options based on platform - ensure directories exist or are creatable
    options = []
    
    if sys.platform == "win32":
        # Windows options
        user_dir = Path.home() / "AppData" / "Local" / "Programs" / "mdview"
        options.append((user_dir, "User directory (recommended)", False))
        
        # Check if we can access system directory
        system_dir = Path("C:/Program Files/mdview")
        options.append((system_dir, "System directory (requires admin)", True))
    else:
        # Unix/Linux/macOS options
        user_dir = Path.home() / ".local" / "bin"
        options.append((user_dir, "User directory (recommended)", False))
        
        # Find existing system directory
        system_candidates = ["/usr/local/bin", "/opt/local/bin", "/usr/bin"]
        system_dir = None
        for candidate in system_candidates:
            candidate_path = Path(candidate)
            if candidate_path.exists():
                system_dir = candidate_path
                break
        
        if system_dir is None:
            system_dir = Path("/usr/local/bin")  # Default fallback
        
        options.append((system_dir, "System directory (requires sudo)", True))
    
    # Current directory option
    current_dir = Path.cwd()
    options.append((current_dir, "Current directory", False))
    
    # Display options with status
    for i, (path, description, default_needs_sudo) in enumerate(options, 1):
        exists_status = "exists" if path.exists() else "will be created"
        writable = check_directory_writable(path.parent if not path.exists() else path)
        access_status = "✓ writable" if writable else "⚠ may need elevated privileges"
        
        print(f"{i}. {description}")
        print(f"   Path: {path} ({exists_status})")
        print(f"   Access: {access_status}")
        print()
    
    print(f"{len(options) + 1}. Enter custom path")
    
    while True:
        try:
            choice = input(f"\nEnter your choice (1-{len(options) + 1}): ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{YELLOW}Installation cancelled.{RESET}")
            sys.exit(0)
        
        # Handle numbered choices
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                selected_path, description, default_needs_sudo = options[choice_num - 1]
                print(f"\n{YELLOW}Selected: {description}{RESET}")
                print(f"Installing to: {selected_path}")
                
                # Check actual write permissions
                actual_needs_sudo = not check_directory_writable(
                    selected_path.parent if not selected_path.exists() else selected_path
                )
                
                try:
                    selected_path.mkdir(parents=True, exist_ok=True)
                    return selected_path, actual_needs_sudo
                except (PermissionError, OSError):
                    return selected_path, True
                    
            elif choice_num == len(options) + 1:
                # Custom path
                try:
                    custom_path = input("Enter the installation path: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{YELLOW}Installation cancelled.{RESET}")
                    sys.exit(0)
                
                if custom_path:
                    path = Path(custom_path).expanduser()
                    print(f"\n{YELLOW}Using custom path: {path}{RESET}")
                    needs_sudo = not check_directory_writable(
                        path.parent if not path.exists() else path
                    )
                    
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        return path, needs_sudo
                    except (PermissionError, OSError):
                        return path, True
        except ValueError:
            pass
        
        print(f"{RED}Invalid choice. Please try again.{RESET}")

def create_mdview_script():
    """Return the complete mdview.py source code."""
    return '#!/usr/bin/env python3\n"""\nMarkdown Viewer - Display markdown files as HTML in browser or GUI\n"""\n\nimport argparse\nimport sys\nimport os\nimport tempfile\nimport webbrowser\nfrom pathlib import Path\nimport markdown\nimport time\nimport threading\n\n# Check for PyWebView availability\ntry:\n    import webview\n    PYWEBVIEW_AVAILABLE = True\nexcept ImportError:\n    PYWEBVIEW_AVAILABLE = False\n\n# Configurable cleanup delay for temporary files\n# Can be overridden via MDVIEW_CLEANUP_DELAY environment variable (in seconds)\n# Default is 30 seconds to ensure browsers have time to fully load files\nDEFAULT_CLEANUP_DELAY = 30\nCLEANUP_DELAY = int(os.environ.get(\'MDVIEW_CLEANUP_DELAY\', DEFAULT_CLEANUP_DELAY))\n\n# Embedded README content\nEMBEDDED_README = """# MDView - Markdown Viewer\n\nA Python application to view Markdown files as rendered HTML in a native GUI window or web browser.\n\n## Features\n\n- View single or multiple Markdown files simultaneously\n- Native GUI window using PyWebView (when installed)\n- Fallback to web browser if GUI dependencies are not available\n- Convert Markdown files to HTML with syntax highlighting and table support\n- Multi-file support with tabs in GUI mode\n- Multi-file browser mode creates an index page with links\n- Support for common Markdown extensions (tables, code highlighting, etc.)\n- Option to keep generated HTML files or auto-delete after viewing\n\n## Installation\n\n1. Clone or download this repository\n2. Install dependencies:\n\n```bash\npip install -r requirements.txt\n```\n\nFor GUI mode support (optional but recommended):\n\n```bash\npip install pywebview\n```\n\n\n## Usage\n\n### View Single File\n\n#### GUI Mode (default if PyWebView is installed)\n```bash\npython mdview.py your_file.md\n```\n\n#### Browser Mode\n```bash\npython mdview.py -b your_file.md\n```\n\n### View Multiple Files\n\n#### GUI Mode with Tabs\n```bash\npython mdview.py file1.md file2.md file3.md\n```\n\n#### Browser Mode with Index Page\n```bash\npython mdview.py -b file1.md file2.md file3.md\n```\n\n## Command Line Options\n\n- `markdown_files`: Path(s) to the markdown file(s) to view (accepts multiple files)\n- `-b`, `--browser`: Force browser mode instead of GUI\n- `-k`, `--keep`: Keep the HTML file(s) instead of auto-deleting after viewing\n- `-r`, `--readme`: Display this README.md file\n- `-h`, `--help`: Show help message and exit\n\n## Environment Variables\n\n- `MDVIEW_CLEANUP_DELAY`: Time in seconds to wait before deleting temporary HTML files in browser mode (default: 30).\n  Increase this if you experience issues with files being deleted before your browser can load them.\n\n  ```bash\n  # Example: Wait 60 seconds before cleanup\n  export MDVIEW_CLEANUP_DELAY=60\n  mdview -b README.md\n  ```\n\n## Examples\n\nView a single file in GUI:\n```bash\npython mdview.py README.md\n```\n\nView multiple files with tabs:\n```bash\npython mdview.py docs/*.md\n```\n\nForce browser mode:\n```bash\npython mdview.py -b README.md\n```\n\nKeep the generated HTML files:\n```bash\npython mdview.py -b -k report.md\n# Creates report.html in current directory\n```\n\nView the built-in README:\n```bash\npython mdview.py -r\n# or in browser\npython mdview.py -r -b\n```\n\n## Dependencies\n\n- **markdown**: For converting Markdown to HTML\n- **pywebview** (optional): For native GUI window display\n\n## License\n\nThis project is open source and available under the MIT License.\n"""\n\n\ndef convert_markdown_string_to_html(md_content, title="Markdown Document"):\n    """Convert markdown string to HTML string."""\n    # Convert markdown to HTML with extensions\n    html_content = markdown.markdown(\n        md_content,\n        extensions=[\'extra\', \'codehilite\', \'tables\', \'toc\']\n    )\n    \n    # Wrap in basic HTML structure with styling\n    full_html = f"""\n    <!DOCTYPE html>\n    <html>\n    <head>\n        <meta charset="utf-8">\n        <title>{title}</title>\n        <style>\n                body {{\n                    font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif;\n                    line-height: 1.6;\n                    color: #333;\n                    max-width: 900px;\n                    margin: 0 auto;\n                    padding: 20px;\n                    background-color: #f5f5f5;\n                }}\n                pre {{\n                    background-color: #f4f4f4;\n                    border: 1px solid #ddd;\n                    border-radius: 3px;\n                    padding: 10px;\n                    overflow-x: auto;\n                }}\n                code {{\n                    background-color: #f4f4f4;\n                    padding: 2px 4px;\n                    border-radius: 3px;\n                    font-family: Consolas, Monaco, \'Courier New\', monospace;\n                }}\n                table {{\n                    border-collapse: collapse;\n                    width: 100%;\n                    margin: 15px 0;\n                }}\n                th, td {{\n                    border: 1px solid #ddd;\n                    padding: 8px;\n                    text-align: left;\n                }}\n                th {{\n                    background-color: #f4f4f4;\n                    font-weight: bold;\n                }}\n                blockquote {{\n                    border-left: 4px solid #ddd;\n                    margin: 0;\n                    padding-left: 20px;\n                    color: #666;\n                }}\n                h1, h2, h3, h4, h5, h6 {{\n                    margin-top: 24px;\n                    margin-bottom: 16px;\n                }}\n                a {{\n                    color: #0366d6;\n                    text-decoration: none;\n                }}\n                a:hover {{\n                    text-decoration: underline;\n                }}\n            </style>\n        </head>\n        <body>\n            {html_content}\n        </body>\n        </html>\n        """\n    \n    return full_html\n\n\ndef convert_markdown_to_html(markdown_file):\n    """Convert markdown file to HTML string."""\n    try:\n        with open(markdown_file, \'r\', encoding=\'utf-8\') as f:\n            md_content = f.read()\n        \n        return convert_markdown_string_to_html(md_content, title=Path(markdown_file).name)\n    \n    except FileNotFoundError:\n        print(f"Error: File \'{markdown_file}\' not found.")\n        return None\n    except Exception as e:\n        print(f"Error reading file \'{markdown_file}\': {e}")\n        return None\n\n\ndef create_index_html(markdown_files):\n    """Create an index HTML page with links to all markdown files."""\n    html_files = []\n    for md_file in markdown_files:\n        html_name = Path(md_file).stem + \'.html\'\n        html_files.append((Path(md_file).name, html_name))\n    \n    links_html = \'\\n\'.join([\n        f\'<li><a href="{html_file}">{md_name}</a></li>\' \n        for md_name, html_file in html_files\n    ])\n    \n    index_html = f"""\n    <!DOCTYPE html>\n    <html>\n    <head>\n        <meta charset="utf-8">\n        <title>Markdown Files Index</title>\n        <style>\n            body {{\n                font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif;\n                line-height: 1.6;\n                color: #333;\n                max-width: 900px;\n                margin: 0 auto;\n                padding: 20px;\n                background-color: #f5f5f5;\n            }}\n            h1 {{\n                color: #2c3e50;\n                border-bottom: 2px solid #3498db;\n                padding-bottom: 10px;\n            }}\n            ul {{\n                list-style-type: none;\n                padding: 0;\n            }}\n            li {{\n                margin: 10px 0;\n                padding: 10px;\n                background-color: white;\n                border-radius: 5px;\n                box-shadow: 0 2px 4px rgba(0,0,0,0.1);\n            }}\n            a {{\n                color: #0366d6;\n                text-decoration: none;\n                font-size: 18px;\n            }}\n            a:hover {{\n                text-decoration: underline;\n            }}\n        </style>\n    </head>\n    <body>\n        <h1>Markdown Files</h1>\n        <ul>\n            {links_html}\n        </ul>\n    </body>\n    </html>\n    """\n    \n    return index_html\n\n\ndef create_multi_file_html(markdown_files):\n    """Create HTML with tabs for multiple markdown files."""\n    # Convert all files\n    file_data = []\n    for i, md_file in enumerate(markdown_files):\n        html_content = convert_markdown_to_html(md_file)\n        if html_content:\n            # Extract just the body content\n            import re\n            body_match = re.search(r\'<body>(.*?)</body>\', html_content, re.DOTALL)\n            if body_match:\n                body_content = body_match.group(1)\n                file_data.append({\n                    \'id\': f\'file{i}\',\n                    \'name\': Path(md_file).name,\n                    \'content\': body_content\n                })\n    \n    # Create tab buttons\n    tab_buttons = \'\\n\'.join([\n        f\'<button class="tab-button{" active" if i == 0 else ""}" onclick="showTab(\\\'{f["id"]}\\\')">{f["name"]}</button>\'\n        for i, f in enumerate(file_data)\n    ])\n    \n    # Create tab contents\n    tab_contents = \'\\n\'.join([\n        f\'<div id="{f["id"]}" class="tab-content{" active" if i == 0 else ""}">{f["content"]}</div>\'\n        for i, f in enumerate(file_data)\n    ])\n    \n    multi_html = f"""\n    <!DOCTYPE html>\n    <html>\n    <head>\n        <meta charset="utf-8">\n        <title>Markdown Viewer - {len(markdown_files)} files</title>\n        <style>\n            body {{\n                font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif;\n                line-height: 1.6;\n                color: #333;\n                margin: 0;\n                padding: 0;\n                background-color: #f5f5f5;\n            }}\n            .tab-bar {{\n                background-color: #2c3e50;\n                padding: 0;\n                margin: 0;\n                display: flex;\n                overflow-x: auto;\n            }}\n            .tab-button {{\n                background-color: transparent;\n                color: white;\n                border: none;\n                padding: 12px 24px;\n                cursor: pointer;\n                font-size: 14px;\n                transition: background-color 0.3s;\n                white-space: nowrap;\n            }}\n            .tab-button:hover {{\n                background-color: #34495e;\n            }}\n            .tab-button.active {{\n                background-color: #3498db;\n            }}\n            .tab-content {{\n                display: none;\n                padding: 20px;\n                max-width: 900px;\n                margin: 0 auto;\n            }}\n            .tab-content.active {{\n                display: block;\n            }}\n            pre {{\n                background-color: #f4f4f4;\n                border: 1px solid #ddd;\n                border-radius: 3px;\n                padding: 10px;\n                overflow-x: auto;\n            }}\n            code {{\n                background-color: #f4f4f4;\n                padding: 2px 4px;\n                border-radius: 3px;\n                font-family: Consolas, Monaco, \'Courier New\', monospace;\n            }}\n            table {{\n                border-collapse: collapse;\n                width: 100%;\n                margin: 15px 0;\n            }}\n            th, td {{\n                border: 1px solid #ddd;\n                padding: 8px;\n                text-align: left;\n            }}\n            th {{\n                background-color: #f4f4f4;\n                font-weight: bold;\n            }}\n            blockquote {{\n                border-left: 4px solid #ddd;\n                margin: 0;\n                padding-left: 20px;\n                color: #666;\n            }}\n            h1, h2, h3, h4, h5, h6 {{\n                margin-top: 24px;\n                margin-bottom: 16px;\n            }}\n            a {{\n                color: #0366d6;\n                text-decoration: none;\n            }}\n            a:hover {{\n                text-decoration: underline;\n            }}\n        </style>\n        <script>\n            function showTab(tabId) {{\n                // Hide all tabs\n                const contents = document.querySelectorAll(\'.tab-content\');\n                contents.forEach(content => content.classList.remove(\'active\'));\n                \n                // Remove active from all buttons\n                const buttons = document.querySelectorAll(\'.tab-button\');\n                buttons.forEach(button => button.classList.remove(\'active\'));\n                \n                // Show selected tab\n                document.getElementById(tabId).classList.add(\'active\');\n                \n                // Mark button as active\n                const activeButton = Array.from(buttons).find(b => \n                    b.onclick.toString().includes(tabId)\n                );\n                if (activeButton) activeButton.classList.add(\'active\');\n            }}\n        </script>\n    </head>\n    <body>\n        <div class="tab-bar">\n            {tab_buttons}\n        </div>\n        {tab_contents}\n    </body>\n    </html>\n    """\n    \n    return multi_html\n\n\ndef display_in_gui(markdown_files):\n    """Display markdown files in PyWebView GUI window."""\n    if not PYWEBVIEW_AVAILABLE:\n        print("Error: PyWebView is not installed. Install it with: pip install pywebview")\n        print("Falling back to browser mode...")\n        display_in_browser(markdown_files)\n        return\n    \n    if len(markdown_files) == 1:\n        # Single file mode\n        html_content = convert_markdown_to_html(markdown_files[0])\n        if html_content is None:\n            return\n        \n        window_title = f"Markdown Viewer - {Path(markdown_files[0]).name}"\n        webview.create_window(window_title, html=html_content)\n    else:\n        # Multiple files mode with tabs\n        html_content = create_multi_file_html(markdown_files)\n        window_title = f"Markdown Viewer - {len(markdown_files)} files"\n        webview.create_window(window_title, html=html_content)\n    \n    webview.start()\n\n\ndef display_in_browser(markdown_files, keep_file=False):\n    """Display multiple markdown files in the default web browser."""\n    if len(markdown_files) == 1:\n        # Single file mode\n        html_content = convert_markdown_to_html(markdown_files[0])\n        if html_content is None:\n            return\n            \n        if keep_file:\n            base_name = Path(markdown_files[0]).stem\n            html_path = Path.cwd() / f"{base_name}.html"\n            with open(html_path, \'w\', encoding=\'utf-8\') as f:\n                f.write(html_content)\n            \n            webbrowser.open(f\'file://{html_path.absolute()}\')\n            print(f"Opened {markdown_files[0]} in browser")\n            print(f"HTML file saved at: {html_path}")\n        else:\n            with tempfile.NamedTemporaryFile(mode=\'w\', suffix=\'.html\', delete=False) as f:\n                f.write(html_content)\n                temp_path = f.name\n            \n            webbrowser.open(f\'file://{temp_path}\')\n            print(f"Opened {markdown_files[0]} in browser (temp file will be deleted after {CLEANUP_DELAY}s)")\n\n            def delete_temp_file():\n                time.sleep(CLEANUP_DELAY)\n                try:\n                    os.unlink(temp_path)\n                except:\n                    pass\n            \n            cleanup_thread = threading.Thread(target=delete_temp_file)\n            cleanup_thread.daemon = True\n            cleanup_thread.start()\n    else:\n        # Multiple files mode\n        temp_files = []\n        \n        if keep_file:\n            # Save all files to current directory\n            for md_file in markdown_files:\n                html_content = convert_markdown_to_html(md_file)\n                if html_content:\n                    base_name = Path(md_file).stem\n                    html_path = Path.cwd() / f"{base_name}.html"\n                    with open(html_path, \'w\', encoding=\'utf-8\') as f:\n                        f.write(html_content)\n                    print(f"Saved {md_file} as {html_path}")\n            \n            # Create index\n            index_html = create_index_html(markdown_files)\n            index_path = Path.cwd() / "index.html"\n            with open(index_path, \'w\', encoding=\'utf-8\') as f:\n                f.write(index_html)\n            \n            webbrowser.open(f\'file://{index_path.absolute()}\')\n            print(f"\\nOpened index page in browser")\n            print(f"Index saved at: {index_path}")\n        else:\n            # Use temporary directory\n            temp_dir = tempfile.mkdtemp()\n            \n            # Convert all markdown files\n            for md_file in markdown_files:\n                html_content = convert_markdown_to_html(md_file)\n                if html_content:\n                    base_name = Path(md_file).stem\n                    html_path = Path(temp_dir) / f"{base_name}.html"\n                    with open(html_path, \'w\', encoding=\'utf-8\') as f:\n                        f.write(html_content)\n                    temp_files.append(html_path)\n            \n            # Create index\n            index_html = create_index_html(markdown_files)\n            index_path = Path(temp_dir) / "index.html"\n            with open(index_path, \'w\', encoding=\'utf-8\') as f:\n                f.write(index_html)\n            temp_files.append(index_path)\n            \n            webbrowser.open(f\'file://{index_path.absolute()}\')\n            print(f"Opened {len(markdown_files)} files in browser (temp files will be deleted after {CLEANUP_DELAY}s)")\n\n            # Clean up after delay\n            def delete_temp_files():\n                time.sleep(CLEANUP_DELAY)\n                for temp_file in temp_files:\n                    try:\n                        os.unlink(temp_file)\n                    except:\n                        pass\n                try:\n                    os.rmdir(temp_dir)\n                except:\n                    pass\n            \n            cleanup_thread = threading.Thread(target=delete_temp_files)\n            cleanup_thread.daemon = True\n            cleanup_thread.start()\n\n\ndef main():\n    parser = argparse.ArgumentParser(\n        description=\'View markdown files as HTML in browser or GUI\'\n    )\n    parser.add_argument(\n        \'markdown_files\',\n        nargs=\'*\',\n        help=\'Path(s) to the markdown file(s) to view\'\n    )\n    parser.add_argument(\n        \'-b\', \'--browser\',\n        action=\'store_true\',\n        help=\'Open in browser instead of GUI (default: GUI if available)\'\n    )\n    parser.add_argument(\n        \'-k\', \'--keep\',\n        action=\'store_true\',\n        help=\'Keep the HTML file(s) when using browser mode (default: delete after viewing)\'\n    )\n    parser.add_argument(\n        \'-r\', \'--readme\',\n        action=\'store_true\',\n        help=\'Display the README.md file\'\n    )\n    \n    args = parser.parse_args()\n    \n    # Collect files to display\n    files_to_display = []\n    \n    # Handle readme display\n    if args.readme:\n        # Use embedded README content\n        readme_html = convert_markdown_string_to_html(EMBEDDED_README, title="MDView README")\n        \n        if args.browser:\n            # Create a temporary file for browser display\n            with tempfile.NamedTemporaryFile(mode=\'w\', suffix=\'.html\', delete=False) as f:\n                f.write(readme_html)\n                temp_path = f.name\n            \n            webbrowser.open(f\'file://{temp_path}\')\n            print(f"Opened built-in README in browser (temp file will be deleted after {CLEANUP_DELAY}s)")\n\n            # Clean up after delay\n            def delete_temp_file():\n                time.sleep(CLEANUP_DELAY)\n                try:\n                    os.unlink(temp_path)\n                except:\n                    pass\n\n            cleanup_thread = threading.Thread(target=delete_temp_file)\n            cleanup_thread.daemon = True\n            cleanup_thread.start()\n        else:\n            # Display in GUI\n            if PYWEBVIEW_AVAILABLE:\n                webview.create_window("MDView README", html=readme_html)\n                webview.start()\n            else:\n                # Fallback to browser if PyWebView not available\n                with tempfile.NamedTemporaryFile(mode=\'w\', suffix=\'.html\', delete=False) as f:\n                    f.write(readme_html)\n                    temp_path = f.name\n                \n                webbrowser.open(f\'file://{temp_path}\')\n                print(f"Opened built-in README in browser (PyWebView not available, temp file will be deleted after {CLEANUP_DELAY}s)")\n\n                # Clean up after delay\n                def delete_temp_file():\n                    time.sleep(CLEANUP_DELAY)\n                    try:\n                        os.unlink(temp_path)\n                    except:\n                        pass\n\n                cleanup_thread = threading.Thread(target=delete_temp_file)\n                cleanup_thread.daemon = True\n                cleanup_thread.start()\n        \n        # Exit after displaying README\n        sys.exit(0)\n    \n    # Add any specified markdown files\n    if args.markdown_files:\n        for md_file in args.markdown_files:\n            if os.path.exists(md_file):\n                files_to_display.append(md_file)\n            else:\n                print(f"Warning: File \'{md_file}\' not found, skipping.")\n    \n    # Check if any files were specified\n    if not files_to_display:\n        parser.print_help()\n        sys.exit(1)\n    \n    # Display based on option\n    if args.browser:\n        display_in_browser(files_to_display, keep_file=args.keep)\n    else:\n        display_in_gui(files_to_display)\n\n\nif __name__ == \'__main__\':\n    main()'

def install_mdview(install_dir, needs_sudo):
    """Install mdview to the specified directory."""
    print(f"\n{YELLOW}Installing MDView...{RESET}")
    
    # Create the mdview script
    script_path = install_dir / "mdview"
    
    try:
        # Write the script
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(create_mdview_script())
        
        # Make it executable on Unix-like systems
        if sys.platform != "win32":
            os.chmod(script_path, 0o755)
        
        print(f"{GREEN}✓ MDView installed successfully!{RESET}")
        print(f"  Location: {script_path}")
        
        # Add to PATH advice
        if install_dir not in os.environ.get('PATH', '').split(os.pathsep):
            print(f"\n{YELLOW}Note: {install_dir} is not in your PATH.{RESET}")
            if sys.platform == "win32":
                print(f"To use 'mdview' from anywhere, add this to your PATH:")
                print(f"  {install_dir}")
            else:
                print(f"To use 'mdview' from anywhere, add this to your ~/.bashrc or ~/.zshrc:")
                print(f"  export PATH=\"$PATH:{install_dir}\"")
        
        return True
        
    except PermissionError:
        print(f"{RED}✗ Permission denied. Try running with sudo/admin privileges.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}✗ Installation failed: {e}{RESET}")
        return False

def detect_shell():
    """
    Detect the user's shell and return appropriate config file.
    
    Returns:
        Path: Path to shell config file, or None if not detectable
    """
    import pwd
    
    try:
        # Get user's default shell
        user_shell = pwd.getpwuid(os.getuid()).pw_shell
        shell_name = Path(user_shell).name
        
        home = Path.home()
        
        # Map shells to their config files
        shell_configs = {
            'bash': [home / '.bashrc', home / '.bash_profile', home / '.profile'],
            'zsh': [home / '.zshrc', home / '.zprofile'],
            'fish': [home / '.config' / 'fish' / 'config.fish'],
            'csh': [home / '.cshrc'],
            'tcsh': [home / '.tcshrc', home / '.cshrc'],
        }
        
        # Return first existing config file, or first option if none exist
        if shell_name in shell_configs:
            configs = shell_configs[shell_name]
            for config in configs:
                if config.exists():
                    return config
            # If no config exists, return the primary one
            return configs[0]
        
        # Default fallback - try common files
        common_configs = [home / '.zshrc', home / '.bashrc', home / '.profile']
        for config in common_configs:
            if config.exists():
                return config
        
        # If nothing exists, default to .bashrc
        return home / '.bashrc'
        
    except Exception:
        # Fallback if we can't detect
        return Path.home() / '.bashrc'


def is_path_in_config(config_file, directory):
    """
    Check if a directory is already in PATH in the config file.
    
    Args:
        config_file (Path): Path to shell config file
        directory (Path): Directory to check for
        
    Returns:
        bool: True if directory is already in PATH
    """
    if not config_file.exists():
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the directory in PATH exports
        dir_str = str(directory)
        
        # Common patterns for PATH modification
        patterns = [
            f'export PATH="$PATH:{dir_str}"',
            f'export PATH="${{PATH}}:{dir_str}"',
            f'export PATH=$PATH:{dir_str}',
            f'export PATH=${{{dir_str}}}:$PATH',
            f'PATH="$PATH:{dir_str}"',
            f'PATH="${{PATH}}:{dir_str}"',
            f'PATH=$PATH:{dir_str}',
        ]
        
        for pattern in patterns:
            if pattern in content:
                return True
        
        # Also check if directory is literally mentioned in any PATH line
        for line in content.split('\n'):
            if 'PATH' in line and dir_str in line:
                return True
                
        return False
        
    except Exception:
        return False


def add_to_path(config_file, directory):
    """
    Add directory to PATH in shell config file.
    
    Args:
        config_file (Path): Path to shell config file
        directory (Path): Directory to add to PATH
        
    Returns:
        bool: True if successfully added, False otherwise
    """
    try:
        # Create config file if it doesn't exist
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing content
        content = ""
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Add PATH export line
        path_line = f'\n# Added by MDView installer\nexport PATH="$PATH:{directory}"\n'
        
        # Append to file
        with open(config_file, 'a', encoding='utf-8') as f:
            f.write(path_line)
        
        return True
        
    except Exception as e:
        print(f"    {RED}✗ Failed to update {config_file}: {e}{RESET}")
        return False


def update_user_path(install_dir, auto_mode=False):
    """
    Update user's shell configuration to include install directory in PATH.
    
    Args:
        install_dir (Path): Directory that was installed to
        auto_mode (bool): If True, don't prompt user for confirmation
        
    Returns:
        bool: True if PATH was updated or already correct
    """
    # Skip for system directories - they should already be in PATH
    system_dirs = [
        Path("/usr/local/bin"),
        Path("/opt/local/bin"), 
        Path("/usr/bin"),
        Path("/bin"),
    ]
    
    if install_dir in system_dirs:
        print(f"    {GREEN}✓ System directory {install_dir} should already be in PATH{RESET}")
        return True
    
    # Detect shell config file
    config_file = detect_shell()
    if not config_file:
        print(f"    {YELLOW}⚠ Could not detect shell configuration file{RESET}")
        return False
    
    print(f"    {YELLOW}Checking PATH in {config_file}...{RESET}")
    
    # Check if already in PATH
    if is_path_in_config(config_file, install_dir):
        print(f"    {GREEN}✓ {install_dir} is already in PATH{RESET}")
        return True
    
    # Ask user for permission (unless in auto mode)
    if auto_mode:
        response = 'y'
        print(f"    {YELLOW}Adding {install_dir} to PATH in {config_file}...{RESET}")
    else:
        print(f"    {YELLOW}The installation directory {install_dir} is not in your PATH.{RESET}")
        print(f"    {YELLOW}Add it to {config_file}? [Y/n]: {RESET}", end="")
        
        try:
            response = input().strip().lower()
            if response in ['n', 'no']:
                print(f"    {YELLOW}Skipping PATH update. You can manually add:{RESET}")
                print(f"    {YELLOW}export PATH=\"$PATH:{install_dir}\"{RESET}")
                return False
        except (EOFError, KeyboardInterrupt):
            # Default to yes if non-interactive
            response = 'y'
    
    if response in ['', 'y', 'yes']:
        if add_to_path(config_file, install_dir):
            print(f"    {GREEN}✓ Added {install_dir} to PATH in {config_file}{RESET}")
            print(f"    {YELLOW}Restart your shell or run: source {config_file}{RESET}")
            return True
        else:
            print(f"    {RED}✗ Failed to update PATH{RESET}")
            return False
    
    return False


def find_existing_mdview():
    """
    Find existing mdview installations on the system.
    
    Returns:
        list: List of tuples (path, version) for found installations
    """
    found_installations = []
    
    # Check if mdview is in PATH
    mdview_in_path = shutil.which("mdview")
    if mdview_in_path:
        version = get_mdview_version(mdview_in_path)
        found_installations.append((Path(mdview_in_path), version))
    
    # Common installation directories to check
    common_dirs = []
    
    if sys.platform == "win32":
        common_dirs = [
            Path.home() / "AppData" / "Local" / "Programs" / "mdview" / "mdview",
            Path.home() / "bin" / "mdview",
            Path("C:/Program Files/mdview/mdview"),
        ]
    else:
        common_dirs = [
            Path("/usr/local/bin/mdview"),
            Path("/usr/bin/mdview"),
            Path("/opt/local/bin/mdview"),  # MacPorts
            Path.home() / ".local" / "bin" / "mdview",
            Path.home() / "bin" / "mdview",
            Path.home() / ".bin" / "mdview",
        ]
    
    # Check each common directory
    for mdview_path in common_dirs:
        if mdview_path.exists() and mdview_path.is_file():
            # Avoid duplicates if already found in PATH
            if not any(str(mdview_path) == str(p[0]) for p in found_installations):
                version = get_mdview_version(mdview_path)
                found_installations.append((mdview_path, version))
    
    # Check pipx installations
    pipx_installations = find_pipx_mdview()
    found_installations.extend(pipx_installations)
    
    return found_installations


def get_mdview_version(mdview_path):
    """
    Try to get the version of an mdview installation.
    
    Args:
        mdview_path: Path to mdview executable
        
    Returns:
        str: Version string or "unknown" if version cannot be determined
    """
    try:
        # Try to run mdview -h and look for version info
        result = subprocess.run(
            [str(mdview_path), "-h"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            # Look for version in help output
            import re
            content = result.stdout + result.stderr
            version_match = re.search(r'version\s+([0-9.]+)', content, re.IGNORECASE)
            if version_match:
                return version_match.group(1)
    except:
        pass
    
    # Try to read the file and look for version info
    try:
        with open(mdview_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # Read first 2000 chars
            # Look for version patterns
            import re
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return version_match.group(1)
            
            # Look for version in comments
            version_match = re.search(r'#\s*Version:?\s*([0-9.]+)', content)
            if version_match:
                return version_match.group(1)
    except:
        pass
    
    return "unknown"


def find_pipx_mdview():
    """
    Find mdview installations managed by pipx.
    
    Returns:
        list: List of tuples (path, version) for pipx installations
    """
    installations = []
    
    if not is_pipx_available():
        return installations
    
    try:
        # Run pipx list to find mdview
        result = subprocess.run(
            ["pipx", "list", "--short"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'mdview' in line.lower():
                    # Try to extract version from pipx output
                    # Format is usually: package_name version
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        version = parts[1]
                    else:
                        version = "pipx-managed"
                    
                    # Find the actual executable
                    pipx_bin = Path.home() / ".local" / "bin" / "mdview"
                    if pipx_bin.exists():
                        installations.append((pipx_bin, version))
    except:
        pass
    
    return installations


def prompt_reinstall(existing_installations):
    """
    Prompt user about existing installations and ask if they want to reinstall.
    
    Args:
        existing_installations: List of (path, version) tuples
        
    Returns:
        bool: True if user wants to proceed with reinstallation
    """
    print(f"\n{YELLOW}⚠ MDView is already installed!{RESET}")
    print(f"\nFound {len(existing_installations)} existing installation(s):\n")
    
    for i, (path, version) in enumerate(existing_installations, 1):
        print(f"  {i}. {BOLD}{path}{RESET}")
        print(f"     Version: {version}")
        
        # Check if it's in PATH
        if shutil.which("mdview") == str(path):
            print(f"     {GREEN}✓ Available in PATH{RESET}")
        else:
            print(f"     {YELLOW}⚠ Not in PATH{RESET}")
        
        # Check if writable
        if check_directory_writable(path.parent):
            print(f"     {GREEN}✓ Writable (can be updated){RESET}")
        else:
            print(f"     {RED}✗ Not writable (requires elevated privileges){RESET}")
        print()
    
    print(f"{YELLOW}What would you like to do?{RESET}")
    print("1. Reinstall/Update MDView (overwrites existing)")
    print("2. Install to a different location")
    print("3. Cancel installation")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{YELLOW}Installation cancelled.{RESET}")
            return False
        
        if choice == "1":
            print(f"\n{YELLOW}Proceeding with reinstallation...{RESET}")
            return True
        elif choice == "2":
            print(f"\n{YELLOW}You'll be prompted for a new installation location...{RESET}")
            return True
        elif choice == "3":
            print(f"\n{YELLOW}Installation cancelled.{RESET}")
            return False
        else:
            print(f"{RED}Invalid choice. Please enter 1, 2, or 3.{RESET}")


def check_existing_and_prompt():
    """
    Check for existing installations and prompt user if found.
    
    Returns:
        bool: True if installation should proceed, False otherwise
    """
    print(f"\n{YELLOW}Checking for existing MDView installations...{RESET}")
    
    existing_installations = find_existing_mdview()
    
    if not existing_installations:
        print(f"{GREEN}✓ No existing MDView installations found.{RESET}")
        return True
    
    # Found existing installations, prompt user
    return prompt_reinstall(existing_installations)


def should_install_to_location(target_path):
    """
    Check if we should proceed with installation to the target location.
    
    Args:
        target_path: Path where we plan to install
        
    Returns:
        bool: True if we should proceed
    """
    print(f"\n{YELLOW}Checking target installation location...{RESET}")
    
    target_mdview = target_path / "mdview"
    existing_installations = find_existing_mdview()
    
    # Check if target location already has mdview
    target_exists = any(str(target_mdview) == str(path) for path, version in existing_installations)
    
    if target_exists:
        print(f"\n{YELLOW}⚠ MDView is already installed at the target location:{RESET}")
        print(f"  {target_mdview}")
        
        # Find the existing installation details
        for path, version in existing_installations:
            if str(path) == str(target_mdview):
                print(f"  Version: {version}")
                if shutil.which("mdview") == str(path):
                    print(f"  {GREEN}✓ Available in PATH{RESET}")
                else:
                    print(f"  {YELLOW}⚠ Not in PATH{RESET}")
                break
        
        while True:
            try:
                response = input(f"\nOverwrite existing installation? [y/N]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return False
            
            if response in ['y', 'yes']:
                print(f"{YELLOW}Proceeding with overwrite...{RESET}")
                return True
            elif response in ['', 'n', 'no']:
                print(f"{YELLOW}Installation cancelled.{RESET}")
                return False
            else:
                print(f"{RED}Please enter 'y' for yes or 'n' for no.{RESET}")
    
    # Show other existing installations if any (not at target location)
    other_installations = [
        (path, version) for path, version in existing_installations 
        if str(path) != str(target_mdview)
    ]
    
    if other_installations:
        print(f"\n{BLUE}ℹ Found {len(other_installations)} other MDView installation(s):{RESET}")
        for path, version in other_installations:
            print(f"  • {path} (version: {version})")
            if shutil.which("mdview") == str(path):
                print(f"    {GREEN}✓ Available in PATH{RESET}")
            else:
                print(f"    {YELLOW}⚠ Not in PATH{RESET}")
    
    print(f"{GREEN}✓ Target location is clear for installation.{RESET}")
    return True


def create_test_file():
    """Create a test markdown file."""
    test_content = """# MDView Test File

This is a test file to verify your MDView installation is working correctly.

## Features Test

### Code Block
```python
def hello_mdview():
    print("Hello from MDView!")
```

### Table
| Feature | Status |
|---------|--------|
| HTML Rendering | ✓ |
| Syntax Highlighting | ✓ |
| Tables | ✓ |

### List
- ✓ Easy to install
- ✓ Easy to use
- ✓ Beautiful output

**Congratulations!** If you can see this properly formatted, MDView is working! 🎉
"""
    
    test_path = Path.cwd() / "mdview_test.md"
    try:
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        return test_path
    except PermissionError:
        # If we can't write to current directory, try user's home directory
        test_path = Path.home() / "mdview_test.md"
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        return test_path

def main():
    """Main installation process."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='MDView Installer - Install MDView markdown viewer',
        epilog=f'''
Default installation locations:
  Auto mode will try (in order):
    • ~/.local/bin (Unix/macOS) or ~/AppData/Local/Programs/mdview (Windows)
    • ~/bin
    • ~/.bin (Unix/macOS only)
    • ./mdview_install (current directory)
  
  System installation (option 2) will try:
    • /usr/local/bin (if exists)
    • /opt/local/bin (MacPorts, if exists)
    • /usr/bin (last resort)
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--auto', '-a', action='store_true', 
                       help='Automatic installation to first writable user directory (no prompts)')
    parser.add_argument('--path', '-p', type=str, 
                       help='Custom installation path')
    parser.add_argument('--no-deps', action='store_true',
                       help='Skip dependency installation')
    parser.add_argument('--no-path-update', action='store_true',
                       help='Skip updating PATH in shell configuration')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Skip existing installation check and force reinstall')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check Python version
    check_python_version()
    
    print(f"{GREEN}✓ Python {sys.version.split()[0]} detected{RESET}")
    
    # Get install location early
    install_dir, needs_sudo = get_install_location(auto_install=args.auto, install_path=args.path)
    
    # Check for existing installations (unless in force mode)
    if not args.force:
        if not should_install_to_location(install_dir):
            sys.exit(0)
    
    # Install dependencies (unless skipped)
    if not args.no_deps:
        if not install_dependencies():
            print(f"\n{RED}Failed to install dependencies. Exiting.{RESET}")
            sys.exit(1)
    else:
        print(f"{YELLOW}Skipping dependency installation...{RESET}")
    
    # Install MDView
    if install_mdview(install_dir, needs_sudo):
        print(f"\n{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}Installation complete!{RESET}")
        
        # Update PATH in shell configuration
        path_updated = False
        if not args.no_path_update:
            print(f"\n{YELLOW}Updating shell configuration...{RESET}")
            path_updated = update_user_path(install_dir, auto_mode=args.auto)
        else:
            print(f"\n{YELLOW}Skipping PATH update (--no-path-update specified){RESET}")
        
        print(f"\n{YELLOW}Quick test:{RESET}")
        
        # Create test file
        test_file = create_test_file()
        print(f"Created test file: {test_file}")
        
        # Show how to run
        if path_updated or install_dir in os.environ.get('PATH', '').split(os.pathsep):
            print(f"\nTry running: {BOLD}mdview mdview_test.md{RESET}")
            print(f"Or view the docs: {BOLD}mdview -r{RESET}")
            if path_updated:
                print(f"{YELLOW}Note: You may need to restart your shell or run 'source ~/.zshrc' (or ~/.bashrc){RESET}")
        else:
            mdview_path = install_dir / "mdview"
            print(f"\nTry running: {BOLD}{mdview_path} mdview_test.md{RESET}")
            print(f"Or view the docs: {BOLD}{mdview_path} -r{RESET}")
            print(f"\n{YELLOW}To add to PATH manually, add this to your shell config:{RESET}")
            print(f"{YELLOW}export PATH=\"$PATH:{install_dir}\"{RESET}")
        
        print(f"\n{BLUE}Thank you for installing MDView! ❤️{RESET}")
        
        # Suggest pipx for cleaner installation
        if is_pipx_available():
            print(f"\n{BLUE}💡 Tip: For a cleaner installation, consider using pipx:{RESET}")
            print(f"    pipx install mdview")
            print(f"    This creates an isolated environment for MDView and its dependencies.")
    else:
        print(f"\n{RED}Installation failed. Please try again.{RESET}")

if __name__ == "__main__":
    main()
