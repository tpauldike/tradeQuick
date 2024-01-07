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
    rating_data = {}

    new_user_id = request.form.get('user_id')
    user_comment = request.form.get('comment')
    user_rating = request.form.get('rating')
    if new_user_id is None:
        abort(400, "Missing user_id")
    if user_comment is None:
        abort(400, "Missing comment")
    if user_rating is None:
        abort(400, "Missing rating")

    rating_data['user_id'] = new_user_id
    rating_data['comment'] = user_comment
    rating_data['rating'] = user_rating
    
    try:
        with db:
            auth_user = request.current_user
            if auth_user is not None:
                if auth_user.user_id != rating_data['user_id']:
                    return jsonify({"error": "Unauthorized"}), 401
            rating = db.create_rating(rating_data)
            print(f"Rating successfully created for {rating_data['user_id']}")
            db.save()
            return jsonify(rating.to_dict()), 201
    except Exception as e:
        print(e)
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
