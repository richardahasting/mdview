#!/usr/bin/env python3
"""
Build the mdview_installer.py file by combining the installer template with the mdview.py source.

This script creates a self-contained installer that includes the entire mdview.py script embedded
within it, allowing users to install MDView with a single Python file.
"""

import sys
from pathlib import Path

def read_file(filepath):
    """Read a file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_mdview_function(installer_content):
    """Extract the create_mdview_script function content from the installer."""
    # Find the start of the function
    start_marker = "def create_mdview_script():"
    start_idx = installer_content.find(start_marker)
    if start_idx == -1:
        raise ValueError("Could not find create_mdview_script function")
    
    # Find where the triple quotes start
    triple_quote_start = installer_content.find("'''", start_idx)
    if triple_quote_start == -1:
        raise ValueError("Could not find start of mdview script")
    
    # Find where the triple quotes end
    triple_quote_end = installer_content.find("'''", triple_quote_start + 3)
    if triple_quote_end == -1:
        raise ValueError("Could not find end of mdview script")
    
    # Return the line with the def and the return statement
    func_start = installer_content.rfind('\n', 0, start_idx) + 1
    func_end = installer_content.find('\n', triple_quote_end + 3)
    if func_end == -1:
        func_end = len(installer_content)
    
    return installer_content[func_start:func_end]

def build_installer():
    """Build the mdview_installer.py file."""
    # Paths
    project_root = Path(__file__).parent
    mdview_path = project_root / "mdview.py"
    installer_template_path = project_root / "installer_template.py"
    output_path = project_root / "mdview_installer.py"
    
    # Check if mdview.py exists
    if not mdview_path.exists():
        print(f"Error: {mdview_path} not found")
        sys.exit(1)
    
    # Read the mdview.py content
    mdview_content = read_file(mdview_path)
    
    # If installer template exists, use it; otherwise create from existing installer
    if installer_template_path.exists():
        print(f"Using installer template from {installer_template_path}")
        installer_content = read_file(installer_template_path)
    else:
        print("No installer template found, extracting from existing installer")
        if not output_path.exists():
            print(f"Error: Neither {installer_template_path} nor {output_path} exist")
            print("Cannot build installer without a template")
            sys.exit(1)
        
        # Read existing installer and extract everything except the embedded mdview.py
        existing_installer = read_file(output_path)
        
        # Find and replace the create_mdview_script function
        old_function = extract_mdview_function(existing_installer)
        
        # Create the template by replacing the function content
        installer_content = existing_installer.replace(
            old_function,
            "def create_mdview_script():\n    \"\"\"Return the complete mdview.py source code.\"\"\"\n    return '''MDVIEW_CONTENT_PLACEHOLDER'''"
        )
        
        # Save the template for future use
        with open(installer_template_path, 'w', encoding='utf-8') as f:
            f.write(installer_content)
        print(f"Created installer template at {installer_template_path}")
    
    # Use repr() to properly escape all Python string content
    mdview_function = f'''def create_mdview_script():
    """Return the complete mdview.py source code."""
    return {repr(mdview_content)}'''
    
    # Replace the placeholder or existing function
    if "MDVIEW_CONTENT_PLACEHOLDER" in installer_content:
        final_content = installer_content.replace(
            "def create_mdview_script():\n    \"\"\"Return the complete mdview.py source code.\"\"\"\n    return '''MDVIEW_CONTENT_PLACEHOLDER'''",
            mdview_function
        )
    else:
        # If no placeholder, try to replace existing function
        old_function = extract_mdview_function(installer_content)
        final_content = installer_content.replace(old_function, mdview_function)
    
    # Write the final installer
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    # Make it executable on Unix-like systems
    if sys.platform != "win32":
        import os
        os.chmod(output_path, 0o755)
    
    print(f"Successfully built {output_path}")
    print(f"Size: {len(final_content):,} bytes")
    
    # Verify the embedded content matches
    if mdview_content in final_content:
        print("✓ Verified: mdview.py is correctly embedded")
    else:
        print("⚠ Warning: Could not verify mdview.py embedding")

if __name__ == "__main__":
    build_installer()