#! /bin/bash

set -e

. activate.sh
flake8 fastapi_template_project tests
pylint fastapi_template_project tests
mypy fastapi_template_project tests