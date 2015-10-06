# -*- coding: utf-8 -*-
"""
    flaskapp.lazyhelpers
    ~~~~~~~~~~~~~~~~~~~~
    
    Optimization helper for lazy load of views modules.
"""

from werkzeug import import_string, cached_property


class LazyView(object):
    """ Load views lazy to optimize module loads."""
    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name
    
    @cached_property
    def view(self):
        return import_string(self.import_name)
    
    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)

def url(app, url_rule, import_name, **options):
    """ Lazy add a url rule to the main app"""
    view = LazyView('flaskapp.' + import_name)
    app.add_url_rule(url_rule, view_func=view, **options)


class MultiUrls(object):
    """ Add multiple urls rules to the same endpoint \n
    Usage example::
        
        admin_bp_lz = MultiUrls('admin.views.show', admin_blueprint)
        admin_bp_lz.add_url_rule('/<page>')
        admin_bp_lz.add_url_rule('/', defaults={'page': 'index'} )
        # This code adds to url rules specific options
    """
    
    def __init__(self, import_name, app_object):
        """ Setup view \n
        import_name: view fucntion \n
        app_object: a blueprint or main app object
        """
        self.view_func = LazyView('flaskapp.' + import_name)
        self.app_object = app_object
        
    def add_url_rule(self, url_rule, **options):
        """ Add the rule using the same view."""
        self.app_object.add_url_rule(url_rule,
                                     view_func=self.view_func, **options)

