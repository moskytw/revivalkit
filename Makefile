.PHONY: test test-all clean

test:
	py.test --cov=revivalkit

test-all:
	tox

clean:
	find . \( \
		-name '*.pyc' -o \
		-name '__pycache__' -o \
		-name '*.coffin' \
	\)  -print -delete

lint:
	flake8 revivalkit
