"""
Modules for users endpoints
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, abort
from dotenv import load_dotenv
from os import getenv
from bcrypt import hashpw, gensalt, checkpw


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
        with db:
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            db.save()
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
            hashed_password = hashpw(
                user_data['password'].encode('utf-8'), gensalt())
            user_data['password'] = hashed_password
            user = db.create_user(user_data)
            print(f"User created successfully for {user.fullname}")
            db.save()
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
            if not checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                return jsonify({"error": "wrong password"}), 401
            from api.v1.auth.session_db_auth import SessionDBAuth
            session_auth = SessionDBAuth()
            session_id = session_auth.create_session(user.user_id)
            response = jsonify(user.to_dict())
            cookie_name = getenv('SESSION_NAME')
            response.set_cookie(cookie_name, session_id)
            db.save()
            return response, 200
    except Exception as e:
        abort(404)


@app_views.route('/users/logout', methods=['POST'], strict_slashes=False)
def logout_user():
    """
    - Logout a user
    """
    try:
        from api.v1.auth.session_db_auth import SessionDBAuth
        session_auth = SessionDBAuth()
        session_auth.destroy_session(request)
        return jsonify({}), 200
    except Exception as e:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['POST'], strict_slashes=False)
def put_user(user_id):
    """
    - Update a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        new_password = request.form.get('new_password')

        if user_email is None:
            return jsonify({"error": "email missing"}), 400
        if user_password is None:
            return jsonify({"error": "password missing"}), 400
        if new_password is None:
            return jsonify({"error": "new_password missing"}), 400
        with db:
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            if not checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                return jsonify({"error": "wrong password"}), 401
            hashed_password = hashpw(new_password.encode('utf-8'), gensalt())
            user.password = hashed_password
            db.save()
            return jsonify(user.to_dict()), 201
    except Exception as e:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    - Delete a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            db.delete_user(user)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_user_id(user_id):
    """
    - Update a user
    """
    from models.db import DBStorage
    db = DBStorage()
    user_data = request.json
    if user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'about' not in user_data:
        return jsonify({"error": "about missing"}), 400
    if 'address' not in user_data:
        return jsonify({"error": "address missing"}), 400
    if 'city' not in user_data:
        return jsonify({"error": "city missing"}), 400
    if 'town' not in user_data:
        return jsonify({"error": "town missing"}), 400
    if 'state' not in user_data:
        return jsonify({"error": "state missing"}), 400
    if 'gender' not in user_data:
        return jsonify({"error": "missing gender"})
    if 'fullname' not in user_data:
        return jsonify({"error": "missing fullname"})
    if 'phone1' not in user_data:
        return jsonify({"error": "missing phone1"})
    if 'email' not in user_data:
        return jsonify({"error": "missing email"})
    if 'verified' not in user_data:
        return jsonify({"error": "missing verified"})
    try:
        with db:
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            user.about = user_data['about']
            user.address = user_data['address']
            user.city = user_data['city']
            user.town = user_data['town']
            user.state = user_data['state']
            user.verified = user_data['verified']
            user.gender = user_data['gender']
            user.fullname = user_data['fullname']
            user.phone1 = user_data['phone1']
            user.email = user_data['email']
            db.save()
            return jsonify(user.to_dict()), 200
    except Exception as e:
        abort(404)
