"""
Modules for users endpoints
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, abort
from dotenv import load_dotenv
from os import getenv


load_dotenv()


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

    # Check if user_id is None
    try:
        if user_id is None:
            abort(404)
        if user_id == 'me':
            if request.current_user is None:
                abort(404)
            user = request.current_user
            user_data = {"user_id": user.user_id, "fullname": user.fullname,
                         "about": user.about, "address": user.address,
                         "email": user.email, "verified": user.verified, "gender": user.gender,
                         "city": user.city, "town": user.town, "state": user.state,
                         "created_at": user.created_at, "updated_at": user.updated_at}
            return jsonify(user_data), 200
        user = db.find_user_by_id(user_id)
        if user is None:
            abort(404)
        db.close()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {e}")
        # Return an error response
        return jsonify({"error": "Internal Server Error"}), 500


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    - Post a new user
    """
    from models.db import DBStorage
    db = DBStorage()
    user_data = request.json

    try:
        with db:
            user = db.create_user(user_data)
            print(f"User created successfully for {user.fullname}")
            return jsonify(user.to_dict()), 201
    except Exception as e:
        abort(404)


@app_views.route('/users/login', methods=['POST'], strict_slashes=False)
def login_user():
    """
    - Login a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        if user_email is None:
            return jsonify({"error": "email missing"}), 400
        if user_password is None:
            return jsonify({"error": "password missing"}), 400
        with db:
            user = db.find_user_by_email(user_email)
            if user is None:
                return jsonify({"error": "No user found for that email"}), 404
            if user_password != user.password:
                return jsonify({"error": "wrong password"}), 401
            from api.v1.auth.session_auth import SessionAuth
            session_auth = SessionAuth()
            session_id = session_auth.create_session(user.user_id)
            response = jsonify(user.to_dict())
            cookie_name = getenv('SESSION_NAME')
            response.set_cookie(cookie_name, session_id)
            return response, 200
    except Exception as e:
        abort(404)


@app_views.route('/users/logout', methods=['POST'], strict_slashes=False)
def logout_user():
    """
    - Logout a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            from api.v1.auth.session_auth import SessionAuth
            session_auth = SessionAuth()
            session_auth.destroy_session(request)
            return jsonify({}), 200
    except Exception as e:
        abort(404)
