#! /bin/bash

set -e

. activate.sh
flake8 src tests
pylint src tests
mypy src tests