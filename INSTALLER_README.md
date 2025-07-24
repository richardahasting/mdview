# MDView - Self-Contained Installer

## 🚀 One-File Installation

This single file (`mdview_installer.py`) contains everything you need to install and run MDView!

### Quick Start

```bash
# Download and run the installer
python3 mdview_installer.py
```

That's it! The installer will:
- ✅ Check your Python version (3.6+ required)
- ✅ Check for existing MDView installations
- ✅ Detect available package managers (pip/pipx)
- ✅ Install required dependencies (markdown, pywebview)
- ✅ Install MDView to your chosen location
- ✅ Create a test file to verify installation
- ✅ Provide usage instructions

## 📦 What You Get

**MDView** is a powerful yet simple Markdown viewer that:

- 🖥️ **Native GUI** - Beautiful native windows using PyWebView
- 🌐 **Browser Mode** - Fallback to your default web browser
- 📄 **Single Files** - View individual markdown documents
- 📚 **Multiple Files** - Tabbed interface for multiple documents
- 🎨 **Beautiful Styling** - GitHub-like rendering with syntax highlighting
- ⚡ **Fast & Lightweight** - Minimal dependencies, maximum performance

## 🎯 Usage Examples

After installation:

```bash
# View a single file
mdview README.md

# View multiple files with tabs
mdview docs/*.md

# Force browser mode
mdview -b presentation.md

# View built-in help
mdview -r

# Keep HTML files instead of auto-deleting
mdview -k -b report.md
```

## 🛠️ Installation Options

The installer offers several installation locations:

1. **User directory** (recommended) - `~/.local/bin`
2. **System directory** - `/usr/local/bin` (requires sudo)
3. **Current directory** - Install right here
4. **Custom location** - Specify your own path

### 🔍 Smart Installation Detection

The installer automatically detects existing MDView installations and will:
- Show you all found installations with their versions
- Check if they're accessible via PATH
- Indicate if they're writable for updates
- Ask if you want to reinstall, update, or install to a different location

**Command line options:**
- `--force` or `-f`: Skip detection and force reinstall
- `--auto` or `-a`: Skip all prompts (also skips detection)

### 🎯 Streamlined Installation Process

The installer now follows a simple, logical flow:

1. **Choose Installation Location** - Asked upfront with clear options and status
2. **Check Target Location** - Verifies if mdview already exists at chosen location
3. **Install Dependencies** - Only after location is confirmed
4. **Install MDView** - To the pre-selected location

This prevents confusion and provides a much cleaner installation experience!

## 📋 Requirements

- Python 3.6 or higher
- pip or pipx (Python package installer)
- Internet connection (for downloading dependencies)

### 🔧 Troubleshooting Package Installation

If you encounter pip installation issues:

```bash
# On macOS with Homebrew
brew install pipx

# On other systems
python3 -m pip install --user pipx
```

The installer will automatically detect and use pipx if pip fails.

## 🔧 Dependencies

- **markdown** (required) - For converting Markdown to HTML
- **pywebview** (optional) - For native GUI windows
  - If not installed, MDView will use browser mode

## 🎨 Features

### GUI Mode (with pywebview)
- Native application window
- Tabbed interface for multiple files
- Full HTML rendering with CSS styling
- Syntax highlighting for code blocks

### Browser Mode (fallback)
- Opens in your default web browser
- Index page for multiple files
- Temporary or permanent HTML file generation
- Same beautiful styling as GUI mode

## 🚚 Sharing MDView

Want to share MDView with others? Just send them the `mdview_installer.py` file! It's completely self-contained and includes:

- The complete MDView application
- Installation logic
- Dependency management
- Cross-platform support (Windows, macOS, Linux)
- Built-in documentation

## 💡 Pro Tips

1. **Add to PATH** - The installer will guide you on adding MDView to your PATH
2. **Test First** - The installer creates a test file to verify everything works
3. **Multiple Locations** - You can install to multiple locations for different users
4. **No Internet After Install** - Once installed, MDView works completely offline

## 🎉 What Makes This Special

This installer is designed for easy sharing and distribution:

- **Single File** - No need to clone repositories or manage multiple files
- **No Build Process** - Just download and run
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **User-Friendly** - Interactive prompts guide you through installation
- **Self-Contained** - Everything needed is embedded in the installer

## 📞 Support

MDView is designed to be simple and reliable. If you encounter issues:

1. Make sure you have Python 3.6+
2. Check that pip is working: `python3 -m pip --version`
3. Try installing to a different location
4. Use `mdview -r` to view the full documentation

---

**Created with ❤️ for the Markdown community**

Enjoy your new Markdown viewing experience!