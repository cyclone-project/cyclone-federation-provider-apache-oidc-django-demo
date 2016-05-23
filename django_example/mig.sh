#!/usr/bin/env bash
rm -f polls/migrations/0001_initial* oidc_customization/migrations/0001_initial* db.sqlite3 && ./manage.py makemigrations && ./manage.py migrate && chmod 777 db.sqlite3
#./manage.py createsuperuser
