from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from typing import TypeVar

load_dotenv()

SESSION_DURATION = getenv('SESSION_DURATION')
SESSION_DURATION = int(SESSION_DURATION)


class SessionExpAuth(SessionAuth):
    """
    - Session Exp Auth Implementation Class
    """

    def __init__(self):
        """
        - Constructor
        """
        super().__init__()
        self.session_duration = SESSION_DURATION
        if self.session_duration is None or not isinstance(self.session_duration, int):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        - Creates a session ID for a user ID
        """
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
        - Returns a user_id based on a session_id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            user_id = session_dict.get('user_id')
            return user_id
        if 'created_at' not in session_dict.keys():
            return None
        if session_dict['created_at'] + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_dict.get('user_id')
