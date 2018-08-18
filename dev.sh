#!/bin/sh
DJANGO_SETTINGS_MODULE=tmknorg.settings.dev
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=test

if [ "$1" == "run" ]; then
    exec ./manage.py runserver 0:8000
fi
exec ./manage.py $@
