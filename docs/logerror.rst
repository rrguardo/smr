.. _logerror:

.. currentmodule:: flaskapp

Loggers And Custom Errors
=========================

Flaskapp preconfigure: basic loggers, custom error pages and exceptions. 
The pattern is simple, a separated module for loggers, custom error pages and 
exceptions is created. Main application then import all this modules.

Loggers Configuration
---------------------

All the application loggers are located in a separated module 
`flaskapp.flasklog`_. Add all the application logger handlers inside function 
`flaskapp.flasklog.set_loggers`_. Main application will call this function 
automatically to add logger handlers. Example::

    #file flaskapp/flasklog.py
    ...
    def set_loggers():
        ...
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
        ...

.. automodule:: flaskapp.flasklog
   :members:

Then logger is accesible through **app.logger**. Usage example::

    from flaskapp import app
    app.logger.debug('debug message')
    app.logger.info('info message')
    app.logger.warn('warn message')
    app.logger.error('error message')
    app.logger.critical('critical message')

*If server run in debug mode, handlers will be skiped and all 
messages will be displayed to stderr*


Custom Error Pages
------------------

To register all the custom error pages a separated module `flaskapp.epages`_ 
was created. Add all page error handlers inside this module. Example::

    #file flaskapp/epages.py
    ...
    @app.errorhandler(404)
    def page_not_found(e):
        """ Resources not found"""
        return render_template('epages/404.html'), 404
    ...

.. automodule:: flaskapp.epages
   :members:


Custom Exceptions
-----------------

To register all the custom exceptions a separated module 
`flaskapp.app_exceptions`_ was created. Add all the custom exceptions inside 
this module. Example::

    #file flaskapp/app_exceptions.py
    ...
    class InvalidUsage(Exception):
        """ Custom exception example."""
        status_code = 400
        
        def __init__(self, message, status_code=None, payload=None):
            Exception.__init__(self)
            self.message = message
            if status_code is not None:
                self.status_code = status_code
                self.payload = payload
        
        def to_dict(self):
            """ ret the dictionary"""
            rvd = dict(self.payload or ())
            rvd['message'] = self.message
            return rvd
    
    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        """ Error handle example."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    ...

.. automodule:: flaskapp.app_exceptions
   :members:
