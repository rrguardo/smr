# -*- coding: utf-8 -*-
"""
    flaskapp.admin.tests
    ~~~~~~~~~~~~~~~~~~~~
    
    Tests for admin sub-package here.
"""


import flaskapp
import unittest


class FlaskAdminTestCase(unittest.TestCase):
    """ Tests for admin package here"""
    def setUp(self):
        self.app = flaskapp.app.test_client()

    def tearDown(self):
        """Get rid of the database again after each test."""
        pass
    
    # testing functions
    
    def test_adminhomepage(self):
        """Admin home page testing."""
        rvt = self.app.get('/admin/')
        assert u'Admin' in rvt.data


if __name__ == '__main__':
    unittest.main()
