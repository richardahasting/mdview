#!/bin/bash
# Build script for MDView package

echo "Building MDView package..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the installer first (before packaging)
echo "Building self-contained installer..."
python3 build_installer.py

# Build source distribution
echo "Building source distribution..."
python3 setup.py sdist

# Build wheel distribution
echo "Building wheel distribution..."
python3 setup.py bdist_wheel

echo "Build complete!"
echo "Distribution files created in dist/"
echo ""
echo "To install locally for testing:"
echo "  pip install dist/mdview-*.whl"
echo ""
echo "To upload to PyPI:"
echo "  pip install twine"
echo "  twine upload dist/*"