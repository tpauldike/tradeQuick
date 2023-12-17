"""
Modules for index endpoints
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, abort


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status() -> str:
    """ GET /api/v1/status
    Return:
      - Status OK
    """
    return jsonify({"status": "OK"}), 200


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
      - Unauthorized
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v1/forbidden
    Return:
      - Forbidden
    """
    abort(403)
