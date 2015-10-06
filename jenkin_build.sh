#!/bin/sh
echo 'Activating virtual enviroment'
. /home/appuser/flaskdeploy/venv/bin/activate

echo 'Deploy sources to nginx test server'
fab pack
fab deploy -p 1234567
echo 'try emperor reload'
touch /etc/uwsgi/vassals/nginx_flask.ini
sleep 7

cd ./flaskapp/
python ../lettuce-webdriver-setup-master/lettuce_cli.py --with-xunit
echo 'Script Build Done!'
