setup:
	python3 -m venv ~/.devml

install:
	pip install -r requirements.txt

test:
	python -m pytest -vv --cov=devml --cov=dml tests/*.py
	#PYTHONPATH=. && py.test --nbval-lax notebooks/*.ipynb

deploy-pypi:
	pandoc --from=markdown --to=rst README.md -o README.rst
	python setup.py check --restructuredtext --strict --metadata
	rm -rf dist
	python setup.py sdist
	twine upload dist/*
	rm -f README.rst

profile:
	python -m cProfile -s cumtime ./dml gstats activity --path /Users/noahgift/src/cpython --sort active_days

lint:
	pylint --disable=R,C,W1203 devml dml

all: install lint test
