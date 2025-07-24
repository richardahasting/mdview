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
    return '''MDVIEW_CONTENT_PLACEHOLDER'''

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
