#! /bin/bash

set -e

. activate.sh
black src tests
flake8 src tests
pylint src
pylint tests  # seperate, else crashes
mypy src tests
