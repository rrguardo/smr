pybabel extract -F flaskapp/babel.cfg -k lazy_gettext -o flaskapp/messages.pot ./flaskapp
pybabel update -i flaskapp/messages.pot -d flaskapp/translations
