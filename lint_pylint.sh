#!/bin/bash
echo "Check for errors with pylint..."
pylint --errors-only --score=n **/*.py

echo "Check syntax with pylint..."
pylint --disable=C,R --score=n **/*.py

echo "Check conventions with pylint..."
pylint --disable=C0103,C0114,C0115,C0116 --max-line-length=120 --score=n *.py

echo "Done."
