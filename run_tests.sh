#!/bin/bash

set -e

export LD_LIBRARY_PATH=$PWD/tests

python3 -m unittest discover -v tests
