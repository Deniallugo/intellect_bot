#!/usr/bin/env bash

python3 manage.py makemigrations --noinput --merge
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

if [ "$DEBUG" != '1' ]
then
    gunicorn bot_mother.wsgi:application \
        -b 0.0.0.0:8000 \
        -w $(nproc) \
        -t 2 \
        -k gevent \
        --timeout 120 \
        --log-level=debug
else
    python3 manage.py runserver 0.0.0.0:8000
fi

