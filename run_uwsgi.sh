uwsgi -s /tmp/uwsgi.sock -H ./venv/ --chmod-socket=666 --processes 4 --threads 2 --stats 127.0.0.1:9191 -w flaskapp:app
