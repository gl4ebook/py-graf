SRC = pygraf

.PHONY : version
version :
	@python -c 'from pygraf.version import VERSION; print(f"Py-graf v{VERSION}")'
#
# Testing helpers.
#

.PHONY : flake8
flake8 :
	flake8 pygraf tests scripts

.PHONY : format
format :
	black --check pygraf tests scripts

.PHONY : typecheck
typecheck :
	mypy pygraf tests scripts --cache-dir=/dev/null

.PHONY : test
test :
	pytest --color=yes -v -rf --durations=40 \
			--cov-config=.coveragerc \
			--cov=$(SRC) \
			--cov-report=xml
#
# Setup helpers
#

.PHONY : install
install :
	# Due to a weird thing with pip, we may need egg-info before running `pip install -e`.
	# See https://github.com/pypa/pip/issues/4537.
	# python setup.py install_egg_info
	# Install torch ecosystem first.
	pip install --upgrade pip
	pip install pip-tools
	pip-compile requirements.in -o final_requirements.txt --allow-unsafe --rebuild --verbose
	pip install -e . -r final_requirements.txt

.PHONY : clean
clean :
	rm -rf .pytest_cache/
	rm -rf pygraf.egg-info/
	rm -rf dist/
	rm -rf build/
	find . | grep -E '(\.mypy_cache|__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf