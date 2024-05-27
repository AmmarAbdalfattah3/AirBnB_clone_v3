#!/usr/bin/python3
"""A module for all states restful endpoints"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves All states"""
    states = storage.all()
    return make_response(jsonify([state.to_dict() for
                         state in states.values()]), 200)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a single state"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return make_response(jsonify({state.to_dict}), 200)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific state"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    state.delete()
    state.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """Creates a review state."""
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    state = State(**body)
    storage.new(state)
    storage.save
    return make_response(jsonify(state.to_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a specific state."""
    state = storage.get('State', state_id)
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    ignored_values = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_values:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
