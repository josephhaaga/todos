t:
	python3 -m pytest

build:
	python3 setup.py sdist bdist_wheel
	twine check dist/*

freeze:
	pip freeze > requirements.txt
