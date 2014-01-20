#!/bin/bash
# Compile docs for the assisipy module

echo "Compiling latex docs..."
sphinx-build -b latex doc/src/ doc/latex/
