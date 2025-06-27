#!/bin/bash

echo "--- Building site for GitHub Pages production ---"
python3 src/main.py --directory "/static-site-generator/"

echo "--- Build complete. Check the 'docs' directory. ---"