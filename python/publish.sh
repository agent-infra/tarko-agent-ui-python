#!/bin/bash

# Script to publish the agent-sandbox package

set -e

echo "Building package..."
python -m build

echo "Package built successfully!"
echo "To publish to PyPI, run:"
echo "  python -m twine upload dist/*"
echo ""
echo "To publish to test PyPI, run:"
echo "  python -m twine upload --repository testpypi dist/*"
