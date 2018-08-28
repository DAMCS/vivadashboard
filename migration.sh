#!/bin/sh
# Requirements
# Python==3.7 under a virtualenv would be preferable
#

python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
