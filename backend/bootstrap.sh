#!/bin/bash
export FLASK_APP=./backend/src/main.py
source $(pipenv --venv)/Scripts/activate
flask run -h 0.0.0.0