#!/bin/bash

echo '******************** Linting (1/2) *************************************'
./lint_flake8.sh
if [ $? -ne 0 ]; then
    echo 'Failed'
    exit 1
fi

echo '******************** Linting (2/2) *************************************'
./lint_pylint.sh
if [ $? -ne 0 ]; then
    echo 'Failed'
    exit 1
fi

echo '******************** Static type checking ******************************'
./mypy.sh
if [ $? -ne 0 ]; then
    echo 'Failed'
    exit 1
fi

echo '******************** Unit testing **************************************'
./pytest.sh
if [ $? -ne 0 ]; then
    echo 'Failed'
    exit 1
fi

