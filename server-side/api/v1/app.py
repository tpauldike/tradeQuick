"""
App Initialiser
"""

from flask import Flask, jsonify, abort, request, flash, redirect, url_for, render_template
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.views import auth
from dotenv import load_dotenv
from os import getenv
import os
from models.db import DBStorage


db = DBStorage()


load_dotenv()


app = Flask(
    __name__, template_folder='/mnt/c/Users/udohd/Project/tradeQuick/client-side/templates', static_folder='/mnt/c/Users/udohd/Project/tradeQuick/client-side/static', static_url_path='/static')
app.register_blueprint(app_views)
app.register_blueprint(auth)
app.config['SECRET_KEY'] = getenv("API_SECRET_KEY")
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
if AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
if AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
if AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.teardown_appcontext
def close_db(error):
    """
    close database session
    """
    with db:
        db.close()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_func():
    """ Before request handler
    """

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/users/login/',
                      '/api/v1/users/',
                      '/api/v1/items/',
                      '/api/v1/signup/',
                      '/api/v1/login/',
                      '/auth/signup/',
                      '/auth/login/',
                      '/static/images/logo.png/',
                      '/static/images/logo1.png/',
                      '/static/scripts/register.js/',
                      '/static/scripts/login.js/',
                      '/favicon.ico/',
                      '/logo.png',
                      '/auth/user/login/',
                      '/static/images/banner.jpg/',
                      ]
    if auth is None:
        pass
    else:
        setattr(request, 'current_user', auth.current_user(request))
        if auth.require_auth(request.path, excluded_paths):
            pass
            if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
                flash('Session expired. Please login again', 'danger')
                return redirect(url_for('auth.login_page'))
            if auth.current_user(request) is None:
                flash('Session expired. Please login again', 'danger')
                return redirect(url_for('auth.login_page'))


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
