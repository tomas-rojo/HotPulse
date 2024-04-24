test:
	@coverage run -m pytest tests/unit/
	@coverage xml
	@coverage report --show-missing --skip-covered

absolufy:
	@find src/   -type f -name '*.py' -exec absolufy-imports --application-directories src/ {} +
	@find tests/ -type f -name '*.py' -exec absolufy-imports --application-directories tests/ {} +

isort:
	@isort --profile black src/ tests/

checks: flake8 mypy

black:
	@black src/ tests/

flake8:
	flake8 src/ tests/

mypy:
	mypy src/ tests/
