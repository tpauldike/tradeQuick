"""
Modules for users endpoints
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, abort
import os
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw


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
            auth_user = request.current_user
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            if auth_user is not None:
                if auth_user.user_id != user.user_id:
                    return jsonify({"error": "Unauthorized"}), 401
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
    user_data = {}

    user_fullname = request.form.get('fullname')
    user_verified = request.form.get('verified')
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_gender = request.form.get('gender')
    user_phone1 = request.form.get('phone1')
    user_phone2 = request.form.get('phone2')
    user_about = request.form.get('about')
    user_address = request.form.get('address')
    user_town = request.form.get('town')
    user_city = request.form.get('city')
    user_state = request.form.get('state')
    
    if user_fullname is None:
        return jsonify({"error": "fullname missing"}), 400
    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if user_password is None:
        return jsonify({"error": "password missing"}), 400
    if user_gender is None:
        return jsonify({"error": "gender missing"}), 400
    if user_phone1 is None:
        return jsonify({"error": "phone1 missing"}), 400
    if user_about is None:
        return jsonify({"error": "about missing"}), 400
    if user_address is None:
        return jsonify({"error": "address missing"}), 400
    if user_town is None:
        return jsonify({"error": "town missing"}), 400
    if user_city is None:
        return jsonify({"error": "city missing"}), 400
    if user_state is None:
        return jsonify({"error": "state missing"}), 400
    user_data['fullname'] = user_fullname
    user_data['email'] = user_email
    user_data['verified'] = user_verified
    user_data['password'] = user_password
    user_data['gender'] = user_gender
    user_data['phone1'] = user_phone1
    user_data['phone2'] = user_phone2
    user_data['about'] = user_about
    user_data['address'] = user_address
    user_data['town'] = user_town
    user_data['city'] = user_city
    user_data['state'] = user_state
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
                return jsonify({"error": "Invalid login details"}), 401
            if not checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                return jsonify({"error": "Invalid login details"}), 401
            from api.v1.auth.session_db_auth import SessionDBAuth
            session_auth = SessionDBAuth()
            session_id = session_auth.create_session(user.user_id)
            response = jsonify(user.to_dict())
            cookie_name = os.getenv('SESSION_NAME')
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
            auth_user = request.current_user
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            if not checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                return jsonify({"error": "wrong password"}), 401
            if auth_user is not None:
                if auth_user.user_id != user.user_id:
                    return jsonify({"error": "Unauthorized"}), 401
            hashed_password = hashpw(new_password.encode('utf-8'), gensalt())
            user.password = hashed_password
            db.save()
            return jsonify(user.to_dict()), 201
    except Exception as e:
        abort(401)


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    - Delete a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            auth_user = request.current_user
            user = db.find_user_by_id(user_id)
            sess = db.find_session_by_id_by_user_id(user_id)
            
            if user is None:
                return jsonify({"error": "User not found"}), 404
            if sess is None:
                return jsonify({"error": "No session found for that user"}), 404
            if auth_user is not None:
                if auth_user.user_id != user.user_id:
                    return jsonify({"error": "Unauthorized"}), 401

            db.delete_session(sess)
            db.delete_user(user)
            db.save()
            return jsonify({}), 204  # 204 No Content for successful deletion
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


def save_picture(form_picture):
    """
    - Save the picture
    """
    pics_id = str(uuid4())
    _, f_ext = os.path.splitext(form_picture.filename)
    
    allowed_extensions = {'.png', '.jpg', '.jpeg'}
    
    if f_ext.lower() in allowed_extensions:
        picture_fn = pics_id + f_ext
        picture_path = os.path.join(os.path.dirname(__file__), '..', 'client-side', 'assets', 'profile_pics', picture_fn)
        
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        
        form_picture.save(picture_path)
        return picture_fn
    else:
        return None

@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_user_id(user_id):
    """
    - Update a user
    """
    from models.db import DBStorage
    db = DBStorage()
    user_data = {}

    user_fullname = request.form.get('fullname')
    user_phone1 = request.form.get('phone1')
    user_phone2 = request.form.get('phone2')
    user_about = request.form.get('about')
    user_address = request.form.get('address')
    user_town = request.form.get('town')
    user_city = request.form.get('city')
    user_state = request.form.get('state')
    user_photo = request.files.get('photo')
    
    pics_fn = save_picture(user_photo)
    
    user_data['fullname'] = user_fullname
    user_data['phone1'] = user_phone1
    user_data['phone2'] = user_phone2
    user_data['about'] = user_about
    user_data['address'] = user_address
    user_data['town'] = user_town
    user_data['city'] = user_city
    user_data['state'] = user_state
    user_data['photo'] = pics_fn
    try:
        with db:
            auth_user = request.current_user
            user = db.find_user_by_id(user_id)
            if user is None:
                abort(404)
            if auth_user is not None:
                if auth_user.user_id != user.user_id:
                    return jsonify({"error": "Unauthorized"}), 400
            user.about = user_data['about']
            user.address = user_data['address']
            user.city = user_data['city']
            user.town = user_data['town']
            user.state = user_data['state']
            user.fullname = user_data['fullname']
            user.phone1 = user_data['phone1']
            user.phone2 = user_data['phone2']
            user.photo = user_data['photo']
            db.save()
            return jsonify(user.to_dict()), 200
    except Exception as e:
        print(e)
        abort(404)
