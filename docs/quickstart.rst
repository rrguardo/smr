.. _quickstart:

Quickstart
==========

.. currentmodule:: flaskapp

Flaskapp represent a set of defaults configurations, basic setups and 
coding patterns preferred for my in usual development scenarios.

Configuration Pattern
---------------------

Flaskapp use the module `flaskapp.settings`_ to store configurations. 
By default the development configuration is loaded in main package::

    # create application
    app = Flask(__name__)
    app.config.from_object('flaskapp.settings.DevelopmentConfig')

Replace this settings in production stage to::

    # create application
    app = Flask(__name__)
    app.config.from_object('flaskapp.settings.ProductionConfig')

.. automodule:: flaskapp.settings
   :members:


Lazy views and URL Pattern
--------------------------

This pattern allows start quick the application, loading views only if 
required. 

In every package and sub-package create a **views.py** and 
**urls.py** files where **views.py** will contains the views functions and 
**urls.py** will map url patterns to an specific view.

Urls file example **urls.py**: ::

    ....
    from flaskapp.lazyhelpers import url
    from flaskapp import app

    #Set all lazy-optimized views here >>>
    url(app, '/', 'views.index')
    url(app, '/_add_numbers', 'views.add_numbers')

View file example **views.py**: ::

    ....
    def index():
        return "Index Page"
    
    def add_numbers():
        a = request.args.get('a', 0, type=int)
        b = request.args.get('b', 0, type=int)
        return jsonify(result=a + b)

Now main application module should import only url modules **urls.py** because 
views are loading lazy. Inside main package module file **__init__.py** at 
the end add url modules import ::

    #file "flaskapp/__init__.py"
    ....
    # Views import here >>
    import flaskapp.urls #lazy-optimized views load
    import flaskapp.admin.urls #lazy-optimized views load


Blueprints
^^^^^^^^^^

For blueprints, load **urls.py** in the sub-package after create the blueprint
object. ::

    #file /flaskapp/admin/__init__.py
    from flask import Blueprint
    
    admin_bp = Blueprint('admin', __name__, template_folder='templates',
                static_folder='static')
    
    # Views import here >>
    #lazy-optimized views load
    import flaskapp.admin.urls


One view with multiple routes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If view function has more than one url route, use the flaskapp.lazyhelpers 
utilities to load views lazy.

.. autoclass:: flaskapp.lazyhelpers.MultiUrls
   :members:


Models and Database Pattern
---------------------------

Each package should contains the required database structure using a 
SQLAlchemy models in a separated module file **models.py** ::

    #file flaskapp/models.py
    from flaskapp import db
        
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
    
        def __init__(self, username, email):
            self.username = username
            self.email = email
    
        def __repr__(self):
            return '<User %r>' % self.username
    ...

All models modules should be imported in the main package 
**flaskapp/__init__.py** after de **db** object creation. ::

    ....
    # Database
    db = SQLAlchemy(app)
    import flaskapp.models
    import flaskapp.admin.models
    ....

To access the SQLAlchemy database object import from the main package the 
**db** object. ::

    from flaskapp import db
    ...

Running Server
--------------

Module `runserver`_ can be used to test Flaskapp with different settings.

.. automodule:: runserver



