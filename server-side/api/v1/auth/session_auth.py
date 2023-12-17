from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar


class SessionAuth(Auth):
    """
    - Session Auth Implementation Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        A method that creates a Session ID for a user_id
        """
        if user_id and isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A method that returns a User ID based on a Session ID
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        - Overloads Auth and retrieves User instance for a request
        """
        from models.db import DBStorage
        db = DBStorage()
        try:
            session_cookie = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_cookie)
            with db:
                user = db.find_user_by_id(user_id)
                return user
        except Exception:
            return None

    def destroy_session(self, request=None):
        """
        - Deletes the user session / logout
        """
        if request is None:
            return False
        sess_cookie = self.session_cookie(request)
        if sess_cookie is None:
            return False
        user_id = self.user_id_for_session_id(sess_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[sess_cookie]
        return True
