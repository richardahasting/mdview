# Developer Log

## Session: Build Process for mdview_installer.py Regeneration

### Date: 2025-07-24

### User Request
"I need you to reverse engineer the mdview_installer.py file so that it is recreatable, should we need to rebuild in the future. A build of a distribution should build this file."

### Analysis
Analyzed the structure of mdview_installer.py and found:
- It's a self-contained installer script (1419 lines)
- Contains the entire mdview.py script embedded within the `create_mdview_script()` function
- The embedded script starts at line 376 and runs through line 1053
- Includes installation logic, dependency management, and PATH configuration

### Implementation

1. **Created build_installer.py**
   - Reads the current mdview.py file
   - Extracts or creates an installer template
   - Embeds mdview.py content into the template
   - Generates a fresh mdview_installer.py

2. **Updated build.sh**
   - Added installer generation step before packaging
   - Ensures installer is always built with latest mdview.py code

3. **Updated CLAUDE.md**
   - Added "Building the Installer" section
   - Documented both automatic and manual build processes
   - Explained template generation mechanism

### Key Design Decisions

1. **Template Extraction**: If installer_template.py doesn't exist, the build script extracts it from the existing installer by replacing the embedded mdview.py with a placeholder

2. **Automatic Integration**: Integrated into build.sh so every distribution build automatically regenerates the installer

3. **Verification**: Build script verifies that mdview.py content is correctly embedded

### Testing
- Successfully ran build.sh - created installer_template.py on first run
- Verified installer regeneration works correctly
- File sizes: template ~28KB, complete installer ~48KB
- Confirmed repeatable builds produce consistent results

### Files Modified
- Created: build_installer.py
- Created: installer_template.py (generated)
- Modified: build.sh
- Modified: CLAUDE.md
- Modified: mdview_installer.py (regenerated)

### Next Steps
- Consider adding version checking to ensure installer version matches mdview.py version
- Could add integrity checks (checksums) to verify correct embedding
- Template could be committed to version control for consistency

### Session Complete
All requested functionality implemented and tested successfully.

## Session: Enhanced pipx Support for Linux Compatibility

### Date: 2025-07-24

### User Request
"If pip is not there, can we check for a pipx?"

### Analysis
- The installer already had pipx detection code (`is_pipx_available()` function)
- However, it wasn't being used effectively in the dependency installation flow
- Modern Linux distributions (Debian 12+, Ubuntu 23.04+) restrict pip usage due to PEP 668
- pipx is becoming more common as the recommended tool for Python applications

### Implementation

1. **Added pip detection function**
   - Created `is_pip_available()` to check if pip is installed
   - Mirrors the existing pipx detection approach

2. **Enhanced install_dependencies function**
   - Now checks for both pip and pipx availability
   - Reports which package managers are available
   - Provides clear error messages when neither is available
   - Explains that pipx cannot install libraries (only applications)
   - Handles the case where only pipx is available

3. **Added pipx suggestion**
   - After successful installation, suggests using pipx for cleaner installs
   - Provides the exact command: `pipx install mdview`

4. **Updated documentation**
   - Enhanced INSTALLER_README.md to mention package manager detection
   - Updated CLAUDE.md with package manager support details

### Key Design Decisions

1. **Clear Communication**: When only pipx is available, clearly explain why it can't install libraries
2. **Graceful Degradation**: Installer provides helpful guidance rather than just failing
3. **Future-Proofing**: Supports modern Linux distributions with PEP 668 restrictions

### Testing
- Verified pip and pipx detection works correctly
- Rebuilt installer with enhanced support (49,990 bytes)
- Confirmed the installer provides appropriate messages based on available tools

### Files Modified
- Modified: installer_template.py (added pip detection and enhanced logic)
- Modified: mdview_installer.py (regenerated with enhancements)
- Modified: INSTALLER_README.md (updated documentation)
- Modified: CLAUDE.md (added package manager support section)

### Impact
- Better Linux compatibility, especially for modern distributions
- Clearer error messages and guidance for users
- Future-proof against Python packaging ecosystem changes

### Session Complete
Enhanced installer now properly handles pip/pipx detection and provides appropriate guidance.

## Session: Add Existing Installation Detection

### Date: 2025-07-24

### User Request
"What other thing we need to do, check to see if we are already installed somewhere. No need to install if it's already there. Ask the user if they want to reinstall if it does exist."

### Analysis
- Users might run the installer multiple times without realizing mdview is already installed
- This could lead to duplicate installations or confusion about which version is being used
- Need to check common installation locations and PATH
- Should handle different installation methods (direct install, pipx, etc.)

### Implementation

1. **Created comprehensive detection functions**
   - `find_existing_mdview()`: Main detection function
   - `get_mdview_version()`: Attempts to extract version from existing installations
   - `find_pipx_mdview()`: Specifically detects pipx-managed installations
   - `check_existing_and_prompt()`: Main flow integration function

2. **Detection coverage**
   - Checks if mdview is available in PATH (using `shutil.which()`)
   - Scans common installation directories:
     - Unix/Linux: `/usr/local/bin`, `/usr/bin`, `/opt/local/bin`, `~/.local/bin`, `~/bin`, `~/.bin`
     - Windows: `~/AppData/Local/Programs/mdview`, `~/bin`, `C:/Program Files/mdview`
   - Detects pipx installations via `pipx list --short`
   - Avoids duplicate entries from same installation

3. **User interaction enhancements**
   - Shows detailed information about each found installation:
     - Full path to executable
     - Version (if detectable)
     - Whether it's in PATH
     - Whether the installation is writable for updates
   - Provides clear options:
     1. Reinstall/Update (overwrites existing)
     2. Install to different location
     3. Cancel installation

4. **Command line options**
   - Added `--force` / `-f` flag to skip detection and force reinstall
   - Detection automatically skipped in `--auto` mode for non-interactive usage

5. **Version detection**
   - Attempts to run `mdview -h` and parse output for version info
   - Falls back to reading file content for version patterns
   - Gracefully handles cases where version cannot be determined

### Testing
- Successfully detects existing installations on system
- Found 2 installations during testing: `~/.local/bin/mdview` and `~/bin/mdview`
- Version detection works (shows "unknown" when no version info available)
- Help output shows new `--force` option

### Files Modified
- Modified: installer_template.py (added detection functions and flow integration)
- Modified: mdview_installer.py (regenerated with 57,408 bytes - significant size increase)
- Modified: CLAUDE.md (documented installation detection features)
- Modified: INSTALLER_README.md (added smart detection section)

### Key Features Added
- **Comprehensive detection**: PATH, common directories, pipx installations
- **Detailed reporting**: Shows path, version, PATH status, writability
- **User choice**: Reinstall, different location, or cancel
- **Non-interactive support**: `--force` flag and `--auto` mode skip detection
- **Duplicate prevention**: Avoids showing same installation multiple times

### Impact
- Prevents accidental duplicate installations
- Provides better user experience with clear information about existing installations
- Supports various installation methods (manual, pipx, system packages)
- Maintains backward compatibility with existing command-line options

### Session Complete
Installer now intelligently detects existing installations and guides users appropriately.

## Session: Add Installation Location Prompt

### Date: 2025-07-24

### User Request
"Good. One more thing, while we are at it, we should probably ask the user where they want the product to be installed."

Follow-up: "Make sure to present a default directory that already exists."

### Analysis
- The existing installation flow was complex with multiple decision points
- Users had to navigate through detection, then location selection
- Better UX would be to ask for location upfront, then handle conflicts
- Need to prioritize existing directories to avoid creation issues

### Implementation

1. **Simplified get_install_location function**
   - Removed complex nested logic for finding "best" directories
   - Now presents clear options with status information
   - Shows whether directories exist or will be created
   - Indicates write permissions for each option
   - Prioritizes existing system directories over non-existent ones

2. **Restructured main installation flow**
   - Moved location selection to occur immediately after Python version check
   - Location is determined before dependency installation or conflict checking
   - More logical sequence: Location → Check conflicts → Install dependencies → Install

3. **Enhanced location conflict detection**
   - Created `should_install_to_location()` function
   - Checks specifically for conflicts at the target location
   - Shows details about existing installation at target (if any)
   - Lists other installations elsewhere for user awareness
   - Simple yes/no prompt for overwriting at target location

4. **Improved option presentation**
   - Shows exact paths for each option
   - Indicates "(exists)" or "(will be created)" status
   - Shows "✓ writable" or "⚠ may need elevated privileges"
   - Finds first existing system directory rather than defaulting to non-existent ones

5. **Cross-platform directory handling**
   - Windows: User AppData, System Program Files
   - Unix/Linux/macOS: ~/.local/bin, existing system bin, current directory
   - Scans ["/usr/local/bin", "/opt/local/bin", "/usr/bin"] and uses first existing one

### Key Changes Made

**Before:**
- Complex auto-detection tried to find "best" directory
- Multiple prompts and decision points
- Location selected after dependency installation
- Confusing flow with nested choices

**After:**
- Simple, clear options presented upfront
- Location selected immediately after version check
- Targeted conflict resolution for chosen location only
- Streamlined, logical flow

### Testing
- Fixed variable name error (`pipx_available` → `is_pipx_available()`)
- Successfully tested with custom path: `/tmp/test_mdview`
- Installer correctly detected existing installations elsewhere
- Showed clear status of target location
- Size increased slightly to 58,585 bytes

### Files Modified
- Modified: installer_template.py (completely rewrote get_install_location, added should_install_to_location, restructured main flow)
- Modified: mdview_installer.py (regenerated with new flow)
- Modified: CLAUDE.md (documented simplified installation flow)
- Modified: INSTALLER_README.md (added streamlined process section)

### User Experience Improvements
- **Clearer Decision Making**: Users know exactly where they're installing upfront
- **Better Information**: Each option shows existence and permission status
- **Logical Flow**: Location → Conflicts → Dependencies → Install
- **Targeted Conflict Resolution**: Only addresses conflicts at chosen location
- **Reduced Complexity**: Eliminated nested decision trees

### Impact
- Much more intuitive installation process
- Prevents user confusion about where mdview will be installed
- Clearer conflict resolution focused on target location
- Better handling of existing vs. non-existent directories
- Maintains all existing functionality while improving UX

### Session Complete
Installer now asks users upfront where they want to install mdview, with clear options and streamlined conflict resolution.