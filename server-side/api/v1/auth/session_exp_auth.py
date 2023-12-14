"""
A module for session expiration
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    A session expiration class
    """

    def __init__(self) -> None:
        try:
            session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id is None or not session_id:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        - User ID for session ID
        """
        try:
            if session_id is None:
                return None
            sess_info = self.user_id_by_session_id.get(session_id)
            if not sess_info:
                return None

            if self.session_duration <= 0:
                user_id = sess_info.get("user_id")
                return user_id

            created_at = sess_info.get("created_at")
            if not created_at:
                return None

            expiration_time = created_at + \
                timedelta(seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None

            user_id = sess_info.get("user_id")
            return user_id
        except Exception as e:
            print(e)
            return None
