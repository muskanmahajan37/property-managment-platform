set -e
set -x

mypy src
black src --check
isort  --check-only src
flake8