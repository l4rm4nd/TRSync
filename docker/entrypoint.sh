#!/bin/bash

echo "[~] Makemigrations and migrate"
python manage.py makemigrations polls
python manage.py migrate
echo "[~] Change ownership of db.sqlite3 to www-data"
chown www-data: /opt/mysite/database/db.sqlite3
echo "[!!] Running the application via UWSGI. Enjoy ;-)"
uwsgi --ini /opt/mysite/docker/docker_uwsgi.ini
