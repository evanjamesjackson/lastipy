#!/bin/bash

echo Creating virtual environment...
python3 -m venv venv
source venv/bin/activate
pip install .

echo

echo Running tests...
python -m pytest test/

echo

echo Incrementing version number...
python -m pip install --upgrade bump2version
bump2version patch

echo

echo Deploying to pypi...
python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade twine
python setup.py sdist bdist_wheel
python -m twine upload dist/* -u $pypi_username -p $pypi_password

deactivate