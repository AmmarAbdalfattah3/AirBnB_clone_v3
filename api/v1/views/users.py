#!/usr/bin/python3
"""A modulel for all user restful endpoints"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves All states"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a single user"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific user"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Creates a review user."""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "email" not in body:
        abort(400, "Missing email")
    if "password" not in body:
        abort(400, "Missing password")
    user = User(**body)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user_id(user_id):
    """Updates a specific user."""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    ignored_values = ['id', 'created_at', 'updated_at', 'email']
    for key, value in body.items():
        if key in ignored_values:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
