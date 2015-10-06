# -*- coding: utf-8 -*-
"""
    flaskapp.api.views
    ~~~~~~~~~~~~~~~~~~~~

    API RESTFUL views here.
"""

import json
from flask import Flask, g, jsonify, render_template, request, abort
from flaskapp.user.models import User
from flaskapp import db, cache


def get_users():
    """ Listing existing users
    
    route("/users", methods=['GET'])    
    """
    selection = []
    try:
        selection = [{'id':usr.id, 'username':usr.username, 'email':usr.email} 
                                for usr in User.query.all()]
    except:
        selection = {'error':True}
    return json.dumps(selection)

def new_user():
    """ Creating a user
    
    route("/users", methods=['POST'])
    """
    success = True
    try:
        usr = User(request.json['username'], request.json['email'])
        db.session.add(usr)
        db.session.commit()
    except:
        success = False
    return jsonify(success=success)

def get_user(user_id):
    """ Retrieving a single user
    
    route("/users/<string:user_id>", methods=['GET'])    
    """
    result = {}
    try:
        usr = User.query.filter_by(id=user_id).first()
        result = {'username':usr.username, 'email':usr.email, 'id':usr.id}
    except:
        result = {'success':False}
    return jsonify(result)

def update_user(user_id):
    """ Editing/Updating a task
    
    route("/users/<string:user_id>", methods=['PUT'])
    """
    success = True
    try:
        usr = db.session.query(User).get(user_id)
        usr.username = request.json['username']
        usr.email = request.json['email']    
        db.session.commit()
    except:
        success = False
    return jsonify(success=success)

def patch_user(user_id):
    """ Update operation to happen as the result of a `PATCH` request 
    (carrying only the updated fields)
    
    route("/users/<string:user_id>", methods=['PATCH'])
    """
    success = True
    try:
        usr = db.session.query(User).get(user_id)
        for item in request.json:
            if item == 'username':
                usr.username = request.json['username']
            elif item == 'email':
                usr.username = request.json['email']
        db.session.commit()
    except:
        success = False
    return jsonify(success=success)

def delete_user(user_id):
    """ Deleting a item
    
    route("/users/<string:user_id>", methods=['DELETE'])
    """
    success = True
    try:
        usr = db.session.query(User).get(user_id)
        db.session.delete(usr)
        db.session.commit()
    except:
        success = False
    return jsonify(success=success)

