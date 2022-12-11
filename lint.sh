#! /bin/bash

set -e

. activate.sh
flake8 myapp_xxx tests
pylint myapp_xxx tests
mypy myapp_xxx tests