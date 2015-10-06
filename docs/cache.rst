.. _cache:

.. currentmodule:: flaskapp

Cache
=====

Flaskapp have the Flask-Cache extension enable and also implement a helper 
functiom :py:func:`flaskapp.babelhelper.key_prefix_babelcache` to support 
cache of multilingual views that uses Flask-Babel extension.

Example Configuration
---------------------

Default cache configuration use **simple** *cache type*. To change cache 
settings modify main package cache config section located in file 
**flaskapp/__init__.py**::

    ...
    #setup cache
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})
    ...

.. seealso::

    Flask-Cache extension documentation.

Using Cache And Babel
---------------------

To allow cache views per client language, use the helper function 
:py:func:`flaskapp.babelhelper.key_prefix_babelcache`.

.. autofunction:: flaskapp.babelhelper.key_prefix_babelcache
   :noindex: