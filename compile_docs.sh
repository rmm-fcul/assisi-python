#!/bin/bash
# Compile docs for the assisipy module

echo "Compiling latex docs..."
sphinx-build -b latex doc/src/ doc/latex/

echo "Compiling html docs..."
sphinx-build -b html doc/src doc/html
