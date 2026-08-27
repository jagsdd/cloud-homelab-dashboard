#!/bin/sh

python -c "from app.db import init_db; init_db()"

exec gunicorn --bind 0.0.0.0:5000 app.app:app
