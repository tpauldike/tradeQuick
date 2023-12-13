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
        - Creates a session ID for a user ID
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        - Returns a user_id based on a session_id
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

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
