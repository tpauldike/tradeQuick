from flask import abort, request, jsonify
from dotenv import load_dotenv
from os import getenv
from api.v1.views import app_views

load_dotenv()


@app_views.route('/ratings', methods=['POST'], strict_slashes=False)
def create_rating():
    """Create a new rating"""
    from models.db import DBStorage
    db = DBStorage()
    rating_data = request.json
    if not rating_data:
        abort(400, "Not a JSON")
    if 'user_id' not in rating_data.keys():
        abort(400, "Missing user_id")
    if 'comment' not in rating_data.keys():
        abort(400, "Missing comment")
    if 'rating' not in rating_data.keys():
        abort(400, "Missing rating")
    try:
        with db:
            rating = db.create_rating(rating_data)
            print(f"Rating successfully created for {rating_data['user_id']}")
            db.save()
            return jsonify(rating.to_dict()), 201
    except Exception as e:
        abort(400)


@app_views.route('/ratings', methods=['GET'], strict_slashes=False)
def get_all_ratings():
    """Get all ratings"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            ratings = db.get_all_ratings()
            ratings_data = [rating.to_dict() for rating in ratings]
            return jsonify(ratings_data), 200
    except Exception as e:
        abort(400)
