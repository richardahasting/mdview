# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MDView is a Python-based Markdown viewer that converts Markdown files to HTML and displays them either in a web browser or a native GUI window using PyWebView. The project follows a single-file architecture with all functionality contained in `mdview.py`.

## Commands

### Build and Distribution
```bash
# Build distribution packages
./build.sh  # Creates both source and wheel distributions in dist/

# Alternative build commands
python3 setup.py sdist         # Source distribution only
python3 setup.py bdist_wheel   # Wheel distribution only
```

### Installation
```bash
# Basic installation
pip install -r requirements.txt

# Install from source
pip install .

# Install with GUI support
pip install .[gui]  # or
pip install pywebview

# Interactive installer
python install.py [--system] [--with-gui]
```

### Running the Application
```bash
# View single file in browser (default)
python mdview.py <markdown_file>

# View in native GUI window (requires pywebview)
python mdview.py -g <markdown_file>

# View multiple files (index in browser, tabs in GUI)
python mdview.py file1.md file2.md file3.md

# Keep generated HTML files
python mdview.py -k report.md

# View embedded README
python mdview.py -r

# Configure temp file cleanup delay (in seconds, default is 30)
MDVIEW_CLEANUP_DELAY=60 python mdview.py <markdown_file>
```

### Environment Variables

- `MDVIEW_CLEANUP_DELAY`: Time in seconds to wait before deleting temporary HTML files in browser mode (default: 30).
  Increase this if you experience issues with files being deleted before your browser can load them, or if you need more time to view the content.
  ```bash
  # Example: Wait 60 seconds before cleanup
  export MDVIEW_CLEANUP_DELAY=60
  python mdview.py -b README.md
  ```

### Testing
No formal test suite exists. Test manually using:
```bash
# Test browser mode (default)
python mdview.py README.md

# Test GUI mode
python mdview.py -g README.md

# Test multi-file support
python mdview.py README.md INSTALLER_README.md

# Test GUI fallback (when PyWebView not installed)
pip uninstall pywebview
python mdview.py -g README.md  # Should fall back to browser
```

## Architecture

### Single-File Design
All functionality is contained in `mdview.py` (~740 lines) with these key components:

- **convert_markdown_string_to_html()**: Core conversion with GitHub-style CSS
- **convert_markdown_to_html()**: File-based wrapper for single files
- **create_index_html()**: Generates index page for multi-file browser mode
- **create_multi_file_html()**: Creates tabbed interface for multi-file GUI mode
- **display_in_gui()**: PyWebView-based native window display
- **display_in_browser()**: Browser display with temporary file management
- **main()**: CLI argument parsing and mode selection

### Key Design Patterns
- **Browser-First Default**: System browser requires no extra dependencies
- **Opt-In GUI**: `-g/--gui` enables PyWebView; falls back to browser if not installed
- **Subprocess Cleanup**: Temp files deleted via detached subprocess (survives parent exit, 30s default)
- **Embedded Documentation**: README content included in script for `-r` flag
- **Multi-Mode Support**: Both browser (index page) and GUI (tabs) for multiple files

### Markdown Extensions Used
- `extra`: Additional markdown features
- `codehilite`: Syntax highlighting for code blocks
- `tables`: Table support
- `toc`: Table of contents generation

## Project Structure

```
mdview/
├── mdview.py              # Main application (single file)
├── setup.py               # Package configuration
├── requirements.txt       # Core dependencies
├── build.sh              # Build script
├── install.py            # Interactive installer
├── README.md             # User documentation
├── CLAUDE.md             # This file
├── INSTALLER_README.md   # Installer documentation
└── mdview_installer.py   # Self-contained installer
```

## Key Dependencies

- **markdown>=3.4.0**: Required for markdown to HTML conversion
- **pywebview>=5.0**: Optional for native GUI mode (falls back to browser if missing)
- **Python 3.6+**: Minimum Python version

## Development Notes

### CSS Styling
The application embeds GitHub-style CSS directly in generated HTML:
- Responsive design (max-width: 900px)
- Code block styling with syntax highlighting
- Table styling with borders and alternating row colors
- Blockquote styling with left border

### Distribution Methods
1. **PyPI Package**: Standard installation via pip
2. **Self-Contained Installer**: `mdview_installer.py` includes all dependencies
3. **Direct Script**: Can run `mdview.py` directly if dependencies installed

### Multi-File Support
- **GUI Mode**: Creates tabbed interface with JavaScript tab switching
- **Browser Mode**: Generates index.html with links to individual files
- Files are processed in the order provided on command line

### Temporary File Handling
- Browser mode creates temporary HTML files in system temp directory
- Files auto-delete after 30 seconds unless `-k/--keep` flag used
- Cleanup handled by a detached subprocess (`subprocess.Popen` with `start_new_session=True`) — survives parent process exit, unlike daemon threads
- Delay configurable via `MDVIEW_CLEANUP_DELAY` environment variable

## Important Notes

- Browser is the default mode; `-g/--gui` opts into PyWebView (falls back to browser if not installed)
- No automated tests exist - all testing is manual
- License: Apache 2.0 (LICENSE file and all references)
- The entire README is embedded in the script for the `-r` flag functionality

## Building the Installer

The `mdview_installer.py` is a self-contained installer that embeds the entire mdview.py script. To regenerate it:

### Automatic Build
```bash
./build.sh  # Automatically rebuilds installer as part of the build process
```

### Manual Build
```bash
python3 build_installer.py
```

### How It Works
1. `build_installer.py` reads the current `mdview.py` file
2. Extracts or creates an installer template from existing `mdview_installer.py`
3. Embeds the mdview.py content into the template's `create_mdview_script()` function
4. Outputs a new `mdview_installer.py` with the latest code

### Template Generation
If `installer_template.py` doesn't exist, the build script will:
1. Extract it from the existing `mdview_installer.py`
2. Replace the embedded mdview.py content with a placeholder
3. Save as `installer_template.py` for future builds

This ensures the installer always contains the latest version of mdview.py and prevents version drift.

### Backup Reference
A backup of the original installer is maintained at `mdview_installer.py.backup` for reference and recovery purposes.

### Package Manager Support
The installer includes intelligent package manager detection:
- Checks for both pip and pipx availability
- Reports which package managers are available
- Handles modern Linux distribution restrictions (PEP 668)
- Provides clear guidance when only pipx is available
- Suggests pipx for cleaner installations when appropriate

This ensures compatibility with modern Linux distributions that restrict system pip usage.

### Installation Detection
The installer now automatically detects existing mdview installations:
- Checks PATH for mdview command
- Scans common installation directories (system and user)
- Detects pipx-managed installations
- Shows installation details (path, version, writability)
- Prompts user for reinstall/update/different location

New command line options:
- `--force` / `-f`: Skip installation detection and force reinstall
- Detection is automatically skipped in `--auto` mode

This prevents accidental duplicate installations and provides better user experience.

### Simplified Installation Flow
The installer now asks users upfront where they want to install MDView:
- Shows clear options with directory status (exists/will be created, writable/needs privileges)
- Prioritizes existing directories over non-existent ones
- Checks target location against existing installations
- Provides targeted conflict resolution for the chosen location

This streamlined approach reduces complexity and provides a better user experience.