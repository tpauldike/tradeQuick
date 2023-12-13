""" Main 4
"""
from flask import Flask, request
from api.v1.auth.session_auth import SessionAuth
from models.db import DBStorage
from models.tables import User

sa = SessionAuth()
db = DBStorage()
try:
    with db:
        user = db.find_user_by_email('susyHalle@example.com')
        """ Create a session ID """
        session_id = sa.create_session(user.user_id)
        print("User with ID: {} has a Session ID: {}".format(
            user.user_id, session_id))
except Exception as e:
    print(e)


""" Create a Flask app """
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """ Root path
    """
    request_user = sa.current_user(request)
    if request_user is None:
        return "No user found\n"
    return "User found: {}\n".format(request_user.user_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
