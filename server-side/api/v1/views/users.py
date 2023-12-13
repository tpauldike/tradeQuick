"""
Modules for users endpoints
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ GET /api/v1/users
    Return:
      - All users
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            users = db.find_all_users()
            users_data = [{"user_id": user.user_id, "fullname": user.fullname,
                           "email": user.email, "verified": user.verified, "gender": user.gender,
                           "phone1": user.phone1, "about": user.about, "address": user.address,
                           "city": user.city, "town": user.town, "state": user.state,
                           "created_at": user.created_at, "updated_at": user.updated_at} for user in users]
            return jsonify(users_data), 200
    except Exception as e:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """
    - Get user based on user_id 
    """
    from models.db import DBStorage
    db = DBStorage()
    current_user = request.current_user
    try:
        if user_id is None:
            abort(404)
        with db:
            user = db.find_user_by_id(user_id)
            user_data = {
                "user_id": user.user_id, "fullname": user.fullname,
                "email": user.email, "verified": user.verified, "gender": user.gender,
                "phone1": user.phone1, "about": user.about, "address": user.address,
                "city": user.city, "town": user.town, "state": user.state,
                "created_at": user.created_at, "updated_at": user.updated_at
            }
            return jsonify(user_data), 200
    except Exception as e:
        abort(404)


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_current_user():
    current_user = request.current_user
    if current_user is None:
        abort(404)

    return current_user
