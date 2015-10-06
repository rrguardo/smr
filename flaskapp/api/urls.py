# -*- coding: utf-8 -*-
"""
    flaskapp.admin.urls
    ~~~~~~~~~~~~~~~~~~~
    
    Add all url <-> view maps here for admin sub-package.
"""


from flaskapp.lazyhelpers import url
from flaskapp.api import api_bp


#Lazy-optimized blueprint views load here 
url(api_bp, '/users', 'api.views.get_users', methods=['GET'])

url(api_bp, '/users', 'api.views.new_user', methods=['POST'])

url(api_bp, '/users/<string:user_id>', 'api.views.get_user', methods=['GET'])

url(api_bp, '/users/<string:user_id>', 'api.views.update_user', 
                                                        methods=['PUT'])
                                                        
url(api_bp, '/users/<string:user_id>', 'api.views.patch_user', 
                                                        methods=['PATCH'])
                                                        
url(api_bp, '/users/<string:user_id>', 'api.views.delete_user', 
                                                        methods=['DELETE'])
