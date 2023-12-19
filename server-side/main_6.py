""" Main 6
"""
import base64
from api.v1.auth.basic_auth import BasicAuth

user_email = "benbooto@example.com"
user_clear_pwd = "!@@#hdd"

print(f"New User: {user_email}")

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(
    basic_clear.encode('utf-8')).decode("utf-8")))
