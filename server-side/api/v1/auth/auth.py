"""
Auth class
"""

from typing import List, TypeVar


class Auth:
    """
      Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header
        """
        if request is None:
            return None
        value = request.headers.get('Authorization')
        if value is None or value == '':
            return None
        else:
            return value

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user
        """
        return None

    def session_cookie(self, request=None):
        """
        - Returns a cookie value from a requests
        """
        if request is None:
            return None
        cookie_value = request.cookies.get('_my_session_id')
        return cookie_value
