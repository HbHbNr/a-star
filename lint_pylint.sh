#!/bin/bash
echo "Check for errors with pylint..."
pylint --errors-only **/*.py
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Check syntax with pylint..."
pylint --disable=C,R **/*.py
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Check conventions with pylint..."
pylint --exit-zero **/*.py
