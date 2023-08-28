#!/bin/bash
echo "Check for errors with pylint..."
pylint --errors-only --score=n **/*.py
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Check syntax with pylint..."
pylint --disable=C,R --score=n **/*.py
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Check conventions with pylint..."
pylint --exit-zero --disable=C0103,C0114,C0115,C0116 --max-line-length=120 --score=n *.py
