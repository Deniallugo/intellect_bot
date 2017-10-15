#!/usr/bin/env bash

su -m intellect_bot -c "celery -A ${CELERY_CONFIG} worker  -Q default -n default@%h --loglevel=INFO"
