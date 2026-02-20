# Work in Progress

## Status: No Active Tasks

All planned features have been implemented. The project is stable.

## Completed Tasks (in order)

- Created build process for `mdview_installer.py` regeneration
- Enhanced installer for pipx support and package manager detection
- Added comprehensive existing installation detection
- Added upfront installation location prompt
- Fixed temp file cleanup: replaced daemon threads with detached subprocess (30s delay, survives parent exit)
- Switched default display mode to system browser; added `-g/--gui` flag for PyWebView

## Potential Future Work

- Automated test suite (currently manual testing only)
- Resolve license inconsistency (setup.py says MIT, LICENSE file is Apache 2.0)
- Version number in the script itself (for `mdview -h` version reporting)
