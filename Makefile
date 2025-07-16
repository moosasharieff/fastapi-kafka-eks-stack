.PHONY: install-tools compile-requirements

install-tools:
	pip install pip-tools

compile-requirements:
	pip install pip-tools
	pip-compile requirements.in --output-file=requirements.txt

install-requirements:
	pip install -r requirements.txt


format-files:
	black .
	ruff format .