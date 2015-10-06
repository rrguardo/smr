.. _fabricdeploy:

.. currentmodule:: fabfile

Fabric Deploy
=============

A basic UWSGI fabric deploy script module **fabfile.py** can be located 
outside flaskapp package 

Update Configuration
--------------------

Update **fabfile** module with correct deployment options (user, hosts, ...)::

    # the user to use for the remote commands
    env.user = 'appuser'
    
    # the servers where the commands are executed
    env.hosts = ['192.168.56.1','192.168.56.101']
    
    # virtual enviroment pyhton path
    VIRT_ENV = ' /home/appuser/flaskdeploy/venv/bin/python'
    
    # Path to uwsgi config file that use emperor
    UWSGI_CONF = '/etc/uwsgi/vassals/nginx_flask.ini'

After update config, deploy the current version of the code on the remote 
server using this command: 

| ``$ fab pack deploy``

UWSGI NGINX UTILS
^^^^^^^^^^^^^^^^^

Inside directory ``deployconf/`` useful configuration files can be found for
fabric deploy using **UWSGI** and **NGINX**.

.. automodule:: fabfile
   :members:
