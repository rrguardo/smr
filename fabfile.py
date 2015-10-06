# -*- coding: utf-8 -*-
"""
fabfile module
--------------

Fabric deployment template for your generic Flask app.
"""

from fabric.api import *

# the user to use for the remote commands
env.user = 'appuser'

# the servers where the commands are executed
env.hosts = ['127.0.0.1'] #['192.168.56.1','192.168.56.101']

# virtual enviroment pyhton path
VIRT_ENV = ' /home/appuser/flaskdeploy/venv/bin/python'

# Path to uwsgi config file that use emperor
UWSGI_CONF = '/etc/uwsgi/vassals/nginx_flask.ini'

def pack():
    """ Create a new source distribution as tarball."""
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    """ Deploy app in all the servers"""
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/flaskapp.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/flaskapp')
    with cd('/tmp/flaskapp'):
        run('tar xzf /tmp/flaskapp.tar.gz')
        # now setup the package with our virtual environment’s
        # python interpreter
        with cd('/tmp/flaskapp/%s' % dist):
            run('%s setup.py install' % VIRT_ENV)
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/flaskapp /tmp/flaskapp.tar.gz')
    # and finally touch the .wsgi file so that emperor triggers
    # a reload of the application
    run('touch %s' % UWSGI_CONF)
