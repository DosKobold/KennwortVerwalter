#!/bin/sh

SRCDIR="source/"


# Static code analysis with pylint
echo "==> running pylint...\n"
pylint "$SRCDIR"/*.py


# Type checking with MyPy
echo "==> running mypy...\n"
mypy "$SRCDIR"/*.py
