# -*- coding: utf-8 -*-
"""
    runserver
    ~~~~~~~~~

    Script to run the Flask application.
    Usage::
        
        bash~$ python runserver.py [options]

    Options::
        
        utest   Run the application unittests
        test    Run the application in testing mode
        dev     Run the application in development mode
        prod    Run the application in production mode
        initdb  Init database from models
        junit   Run the application unittests and outputs JUnit compatible XML 

    Example::
        
        python runserver.py
        python runserver.py test
        python runserver.py dev
        python runserver.py prod
        python runserver.py initdb
        python runserver.py junit
"""

from sys import argv
from flaskapp import app
import unittest

def run_tests_junit():
    """ Python unittest TestResult that outputs JUnit compatible XML."""
    import junitxml
    import sys
    result = junitxml.JUnitXmlResult(sys.stdout)
    result.startTestRun()
    suite = unittest.defaultTestLoader.discover("flaskapp",
                                                top_level_dir="flaskapp")
    suite.run(result)
    result.stopTestRun()

def run_tests():
    """ Run application unittests"""
    print "Running application unittests"
    suite = unittest.defaultTestLoader.discover("flaskapp",
                                                top_level_dir="flaskapp")
    unittest.TextTestRunner(verbosity=2).run(suite)

def run_test_mode():
    """ Run server in test mode"""
    print "Running app in test mode"
    app.config.from_object('flaskapp.settings.TestingConfig')
    app.run()

def run_development():
    """ Run server in development mode"""
    print "Running app in Development mode [Warning debug=True]"
    app.config.from_object('flaskapp.settings.DevelopmentConfig')
    app.run(use_debugger=app.debug)

def run_production():
    """ Run the application in production mode"""
    print "Running app in Production mode"
    app.config.from_object('flaskapp.settings.ProductionConfig')
    from flaskapp.flasklog import set_loggers
    set_loggers()
    app.run()

def init_database():
    """ Init database using models, remove the previous database"""
    import shelltools
    import os
    try:
        os.remove('./flaskapp/flask.db')
    except:
        pass
    shelltools.init_database()

if len(argv) != 2 or argv[1] not in ['dev', 'test', 'utest', 'prod', 'initdb',
                                                     'junit']:
    print __doc__
    exit
elif argv[1] == "utest":
    # unittests
    run_tests()
elif argv[1] == "test":
    # test mode
    run_test_mode()
elif argv[1] == "prod":
    # prod
    run_production()
elif argv[1] == "dev":
    # dev
    run_development()
elif argv[1] == "initdb":
    init_database()
elif argv[1] == "junit":
    run_tests_junit()
