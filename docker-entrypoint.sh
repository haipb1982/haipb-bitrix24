#!/usr/bin/env bash

# export PYTHONPATH=.

# sudo python3 api.py 6666

export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 5000
