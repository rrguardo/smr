# -*- coding: utf-8 -*-


from flask import Blueprint


monitor_bp = Blueprint('monitor', __name__, template_folder='templates',
            static_folder='static')

#Loding url<->views
import flaskapp.services_monitor.urls
