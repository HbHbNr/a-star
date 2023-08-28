#!/bin/bash
echo "Check for errors with flake8..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

echo "Check syntax with flake8..."
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

echo "Done."
