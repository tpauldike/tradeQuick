from flask import abort, request, jsonify
from dotenv import load_dotenv
from os import getenv
from api.v1.views import app_views

load_dotenv()


@app_views.route('/likes/<int:status>', methods=['POST'], strict_slashes=False)
def likes(status):
    """Create a new like"""
    from models.db import DBStorage
    db = DBStorage()
    like_data = request.json
    like_data['liked'] = status
    if not like_data:
        abort(400, "Not a JSON")
    if 'user_id' not in like_data.keys():
        abort(400, "Missing user_id")
    if 'item_id' not in like_data.keys():
        abort(400, "Missing item_id")

    try:
        with db:
            like_user = db.get_like_by_item_id(like_data['item_id'])
            if not like_user:
                new_like = db.create_like(like_data)
                db.save()
                if not new_like:
                    abort(400, "Error creating like")
                return jsonify(new_like.to_dict()), 201
            else:
                if like_user.liked == status:
                    like_user.liked = 1 - status
                else:
                    like_user.liked = status
                db.save()
                return jsonify(like_user.to_dict()), 200
    except Exception as e:
        abort(400)


@app_views.route('likes/<string:item_id>', methods=['GET'], strict_slashes=False)
def get_likes(item_id):
    """Get likes by item_id"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            likes = db.get_like_by_item_id_all(item_id)
            if not likes:
                return jsonify([])
            return jsonify([like.to_dict() for like in likes]), 200
    except Exception as e:
        abort(400)
