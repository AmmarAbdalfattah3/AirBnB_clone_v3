#!/usr/bin/python3
""" The index of the views api"""


from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """An endpoint that returns the app status"""
    return make_response(jsonify({"status": 'OK'}), 200)


@app_views.route('/stats', methods=['GET'])
def stats():
    """An endpoint that count the number
       of each class instances
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    res = {}
    for key, value in classes.items():
        res[key] = storage.count(value)
    return make_response(jsonify(res), 200)
