.PHONY: install-tools compile-requirements

install-tools:
	pip install pip-tools

compile-requirements:
	pip-compile requirements.in --output-file=requirements.txt

install-requirements:
	pip install -r requirements.txt