help:
	@echo ""
	@echo "Options:"
	@echo ""
	@echo "- make help          Show this help"
	@echo ""
	@echo "CODE FORMATTING"
	@echo "- make format        Run all formatters"
	@echo "- make pyupgrade     Run pyupgrade        (upgrades outdated Python code)"
	@echo "- make absolufy      Run absolufy-imports (removes relative import headers)"
	@echo "- make isort         Run isort            (sorts and wraps import headers)"
	@echo "- make black         Run black            (formats code consistently)"
	@echo ""
	@echo "CODE CHECKS"
	@echo "- make checks        Run all code quality checks"
	@echo "- make flake8        Run flake8           (checks code quality)"
	@echo "- make mypy          Run mypy             (checks typing)"
	@echo ""
	@echo "TESTING"
	@echo "- make test          Run unit tests"
	@echo "- make itest          Run integration tests"
	@echo "- make alltests          Run all tests (unit + integration)"
	@echo ""

test:
	@coverage run -m pytest tests/unit/
	@coverage xml
	@coverage report --show-missing --skip-covered

itest:
	@coverage run -m pytest tests/integration
	@coverage xml
	@coverage report --show-missing --skip-covered

alltests:
	@coverage run -m pytest tests/unit tests/integration
	@coverage xml
	@coverage report --show-missing --skip-covered

format: pyupgrade absolufy isort black

pyupgrade:
	find src/   -type f -name '*.py' -exec pyupgrade --py311-plus {} +
	find tests/ -type f -name '*.py' -exec pyupgrade --py311-plus {} +

absolufy:
	@find src/   -type f -name '*.py' -exec absolufy-imports --application-directories src/ {} +
	@find tests/ -type f -name '*.py' -exec absolufy-imports --application-directories tests/ {} +

isort:
	@isort --profile black src/ tests/

black:
	@black src/ tests/

checks: flake8 mypy

flake8:
	flake8 src/ tests/

mypy:
	mypy src/ tests/

run:
	@cd src/entrypoints && flask run --debug
