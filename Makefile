clean:
	rm -rf build dist *.egg-info
	python setup.py clean --all

build:
	python setup.py sdist bdist_wheel

upload:
	python -m twine upload dist/*

rebuild_and_reupload: clean build upload

lint:
	ruff format && ruff check --fix