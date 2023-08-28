#!/bin/bash
echo "Check for errors with flake8..."
flake8 . --select=E9,F63,F7,F82 --show-source --statistics
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Check syntax with flake8..."
flake8 . --exit-zero --max-complexity=10 --max-line-length=127 --statistics
