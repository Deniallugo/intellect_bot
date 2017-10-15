FROM python:3.6-onbuild

ENV DJANGO_SETTINGS_MODULE=bot_mother.settings
ENV CELERY_CONFIG=bot.modules.celery

ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos '' intellect_bot
RUN chown -R intellect_bot:intellect_bot ./
RUN chmod +x ./run_celery.bash
