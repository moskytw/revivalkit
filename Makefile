.PHONY: test test-all

test:
	py.test --cov-config .coveragerc --cov=revivalkit

test-all:
	tox
