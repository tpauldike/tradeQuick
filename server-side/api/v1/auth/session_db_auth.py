from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class SessionDBAuth(SessionExpAuth):
    """
    - SessionDBAuth class
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
        try:
            from models.db import DBStorage
            db = DBStorage()
            session_data = {
                "user_id": user_id,
                "session_id": session_id
            }
            with db:
                session = db.create_session(session_data)
                if session is None:
                    return None
                db.save()
                db.close()
                return session.session_id
        except Exception as e:
            print(e)
            return None

    def user_id_for_session_id(self, session_id=None):
        """
        - User ID for session ID
        """
        try:
            if session_id is None:
                return None

            from models.db import DBStorage
            db = DBStorage()
            with db:
                session = db.find_session_by_id(session_id)
                if session is None:
                    return None

                if self.session_duration > 0:
                    created_at = session.created_at
                    if not created_at:
                        return None

                    expiration_time = created_at + \
                        timedelta(hours=self.session_duration)

                    if expiration_time < datetime.now():
                        try:
                            db.delete_session(session)
                        except Exception as e:
                            print(f"Error during session deletion: {e}")
                            return None
                        return None  # Session expired, return None
                    db.save()
                db.close()

                return session.user_id

        except Exception as e:
            print(f"Error during user_id_for_session_id: {e}")
            return None

    def destroy_session(self, request=None):
        """
        - Destroy session
        """
        try:
            session_id = self.session_cookie(request)
            if session_id is None:
                return False
            from models.db import DBStorage
            db = DBStorage()
            with db:
                session = db.find_session_by_id(session_id)
                if session is None:
                    return False
                db.delete_session(session)
                db.save()
                db.close()
                return True
        except Exception as e:
            print(e)
            return False
