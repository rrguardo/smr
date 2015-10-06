"""
Flaskapp Setup
--------------

Setup template for your generic Flask app.

"""

from setuptools import setup

setup(
    name='Flask Application',
    version='0.1',
    long_description=__doc__,
    packages=['flaskapp', 'flaskapp.admin'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask>=0.10', 'SQLAlchemy>=0.7.8']
)
