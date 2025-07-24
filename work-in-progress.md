# Work in Progress

## Current Task: Add Installation Location Prompt

### Objective
Simplify the installation flow by asking the user upfront where they want to install mdview, rather than using complex location detection.

### Plan
1. Modify get_install_location function to be simpler and more direct
2. Move installation location selection earlier in the process
3. Update existing installation check to consider the target location
4. Simplify the overall installation flow
5. Test the streamlined installation process

### Previous Tasks Completed
- Created build process for mdview_installer.py regeneration
- Enhanced installer for pipx support and package manager detection
- Added comprehensive existing installation detection

### Status
- Starting implementation of upfront location selection