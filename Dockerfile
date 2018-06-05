FROM python:3.6.5-stretch

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE={{ project_name }}.settings.production \
    PYTHONPATH=/app \
    WEB_CONCURRENCY=3 \
    PORT=8000 \
    GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -"

EXPOSE 8000

RUN pip install "gunicorn>=19.8,<19.9"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd tmknorg
RUN chown -R tmknorg .
USER tmknorg

RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

CMD gunicorn {{ project_name }}.wsgi:application
