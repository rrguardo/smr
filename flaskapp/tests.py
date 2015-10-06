# -*- coding: utf-8 -*-
"""
    flaskapp.tests
    ~~~~~~~~~~~~~~

    Tests base for Flask application.
"""


import flaskapp
import unittest


class FlaskappTestCase(unittest.TestCase):
    """ Main package test here"""
    def setUp(self):
        """Before each test, set up a blank database"""
        #self.db_fd, flaskapp.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flaskapp.app.test_client()
        #flaskapp.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        #os.close(self.db_fd)
        #os.unlink(flaskr.app.config['DATABASE'])
        pass

    # testing functions

    def test_homepage(self):
        """Home page testing."""
        rvp = self.app.get('/')
        assert b'Home Page' in rvp.data


if __name__ == '__main__':
    unittest.main()
