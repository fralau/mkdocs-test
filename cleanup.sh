#!/bin/bash
# This is necessary to start from a clean version for test

# Find and delete all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Find and delete all directories starting with __
find . -type d -name "__*" -exec rm -rf {} +

# Find and delete all .egg-info directories
find . -type d -name "*.egg-info" -exec rm -rf {} +

# Find and delete all .egg files
find . -type f -name "*.egg" -exec rm -f {} +

echo "Cleanup complete!"

