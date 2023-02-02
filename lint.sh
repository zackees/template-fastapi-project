#! /bin/bash

set -e

. activate.sh
black src tests
flake8 src tests
pylint src tests
mypy src tests
