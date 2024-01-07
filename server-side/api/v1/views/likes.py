from flask import abort, request, jsonify
from os import getenv
from collections import Counter
from api.v1.views import app_views


@app_views.route('/likes/<int:status>', methods=['POST'], strict_slashes=False)
def likes(status):
    """Create a new like"""
    from models.db import DBStorage
    db = DBStorage()
    like_data = {}

    get_user_id = request.form.get('user_id')
    get_item_id = request.form.get('item_id')
    if not get_user_id:
        abort(400, "Missing user_id")
    if not get_item_id:
        abort(400, "Missing item_id")

    like_data['user_id'] = get_user_id
    like_data['item_id'] = get_item_id
    like_data['liked'] = status
    
    try:
        with db:
            like_user = db.get_user_like(like_data['item_id'], like_data['user_id'])
            auth_user = request.current_user
            if not auth_user:
                abort(401)
            if auth_user.user_id != like_data['user_id']:
                abort(401)
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
        print(e)
        abort(401)


@app_views.route('likes/<string:item_id>', methods=['GET'], strict_slashes=False)
def get_likes(item_id):
    """Get likes by item_id"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            count = 0
            likes = db.get_like_by_item_id_all(item_id)
            if not likes:
                return jsonify([])
            all_likes = [like.to_dict() for like in likes]
            c = Counter()
            for count in all_likes:
                c[count['liked']] += 1
            response = {
                'liked': c[True],
                'dislike': c[False]
            }
            return jsonify(response), 200
    except Exception as e:
        print(e)
        abort(400)