"""
This file contains the basic authentication for the API
"""

import base64
from flask import abort, jsonify, request, abort
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        split_header = authorization_header.split(' ')
        if split_header[0] != 'Basic':
            return None
        if len(split_header) < 2:
            return None
        return split_header[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        decode_base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        split_header = decoded_base64_authorization_header.split(':')
        return split_header[0], split_header[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        user_object_from_credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None

        from models.db import DBStorage
        DB = DBStorage()
        with DB:
            user = DB.find_user_by_email(user_email)
            if user is None:
                return None
            if user.password == user_pwd:
                user_data = {
                    "user_id": user.user_id, "fullname": user.fullname,
                    "email": user.email, "verified": user.verified, "gender": user.gender,
                    "phone1": user.phone1, "about": user.about, "address": user.address,
                    "city": user.city, "town": user.town, "state": user.state,
                    "created_at": user.created_at, "updated_at": user.updated_at
                }
                return jsonify(user_data), 200

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Load the user from the request
        """
        auth_header = self.authorization_header(request)
        extract_base64 = self.extract_base64_authorization_header(auth_header)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        user_credentials = self.extract_user_credentials(decode_base64)
        user_object = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        return user_object
