.PHONY: test test-all clean

test:
	py.test --cov-config .coveragerc --cov=revivalkit

test-all:
	tox

clean:
	find . \( \
		-name '*.pyc' -o \
		-name '__pycache__' -o \
		-name '*.coffin' \
	\)  -print -delete

lint:
	flake8 revivalkit --ignore=F401,E203,E221,E226,E261,E302
