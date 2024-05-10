#!/bin/bash
export FLASK_APP=./backend/src/main.py
source $(pipenv --venv)/Scripts/activate
flask run -h 0.0.0.0
read -n1 -r -p "Press any key to continue..." key