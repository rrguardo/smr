.. _babel:

.. currentmodule:: flaskapp

Babel
=====

Flaskapp have preconfigured Flask-Babel extension and also implement a helper
module `flaskapp.babelhelper`_ to allow set pages language and timezone based
on users database info or browser header.

.. _babel.cfg:

The default babel configuration file **babel.cfg** use this configuration::

    [python: **.py]
    [jinja2: **/templates/**.html]
    [python: **/admin/**.py]
    [jinja2: **/admin/templates/**.html]
    extensions=jinja2.ext.autoescape,jinja2.ext.with_

Update this configuration to add new sub-package modules and templates.

Setting Babel Helper
--------------------

By default babel helper module will try get language and timezone info from 
active user. If not exist active user then helper will try get language code 
from browser header and use default timezone.

If is required a different pages language behavior, update helper function 
`flaskapp.babelhelper.get_locale`_, the current implementation is::

    @babel.localeselector
    def get_locale():
        """ Get the g.user.locale language code, 
            otherwise try get language code using browser header.
        """
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits. We support de/fr/en in this
        # example. The best match wins.
        return request.accept_languages.best_match(['en','es'])

To change pages timezone behavior, update helper function 
`flaskapp.babelhelper.get_timezone`_, the current implementation is::

    @babel.timezoneselector
    def get_timezone():
        """ Get the user.timezone else otherwise use default timezone."""
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone
        return None

.. automodule:: flaskapp.babelhelper
   :members:

Babel Utils Scripts
-------------------

A set of 4 scripts helps with custom project translation.

* ``babel_create_template.sh`` executed from outside **flaskapp** package will 
  create the base translation template using babel config `babel.cfg`_

* ``babel_create_trans_es.sh es`` executed from outside **flaskapp** package 
  will create the base translation template for the language code **es** 
  using template ``flaskapp/messages.pot``. The second parameter is the 
  language code.

* ``babel_compile_trans.sh`` executed from outside **flaskapp** package will 
  compile all the translations inside ``flaskapp/translations``

* ``babel_update_trans.sh`` Update the translations.
