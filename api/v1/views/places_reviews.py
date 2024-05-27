#!/usr/bin/python3
"""A module for all restful reviews endpoints"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves All reviews"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    req_reviews = []
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.place_id == place_id:
            req_reviews.append(review.to_json())
    return make_response(jsonify(req_reviews), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a single review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """Creates a review object."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'user_id' not in body:
        abort(400, "Missing user_id")
    user = storage.get("User", body['user_id'])
    if user is None:
        abort(404)
    if 'text' not in body:
        abort(400, "Missing text")
    review = Review(**body)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a specific review."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key, value in body.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict), 200)
