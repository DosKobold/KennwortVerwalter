#!/bin/sh

#This script runs unittest and coverage
#You can run a unittest without coverage with this command:
# >> python3 -m unittest -v tests/test_cryptor.py

export PYTHONPATH='source/'

echo "Choosen folder for source code: $PYTHONPATH"

/bin/python3-coverage run -m unittest -v tests/test_cryptor.py
#FIXME Doesn't work proberly: We have to run all tests in one run to receive correct test results
/bin/python3-coverage run -m unittest -v tests/test_dataHandler.py


/bin/python3-coverage report

/bin/python3-coverage html
