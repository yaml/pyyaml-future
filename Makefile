SHELL := bash
ROOT != pwd

export PYTHONPATH := $(ROOT)/lib:$(ROOT)/../pyyaml/lib3:$(PATH)

default:

test:
	python3 test.py

clean:
	find . -name '*.pyc' -o -name __pycache__ | \
	    xargs rm -fr
