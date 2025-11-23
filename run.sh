#!/usr/bin/env bash

set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make part1
make part2
make part3
make part4