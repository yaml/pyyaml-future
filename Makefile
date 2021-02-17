SHELL := bash

VERSION := 0.0.1

default:

dist:
	python3 setup.py sdist

publish: dist
	twine upload dist/*

test:
	poetry run pytest

clean:
	rm -rf dist .pytest_cache
	find . -name '*pycache*' | xargs rm -fr
