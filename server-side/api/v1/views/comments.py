from flask import abort, request, jsonify
from dotenv import load_dotenv
from os import getenv
from api.v1.views import app_views

load_dotenv()


@app_views.route('/comments', methods=['POST'], strict_slashes=False)
def comments():
    """Create a new comment"""
    from models.db import DBStorage
    db = DBStorage()
    comment_data = request.json
    if not comment_data:
        abort(400, "Not a JSON")
    if 'commenter' not in comment_data.keys():
        abort(400, "Missing commenter")
    if 'item_id' not in comment_data.keys():
        abort(400, "Missing item_id")
    if 'comment' not in comment_data.keys():
        abort(400, "Missing comment")

    try:
        with db:
            new_comment = db.create_comment(comment_data)
            db.save()
            if not new_comment:
                abort(400, "Error creating comment")
            return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        abort(400)


@app_views.route('/comments/<string:comment_id>', methods=['PATCH'], strict_slashes=False)
def update_comment(comment_id):
    """Update a comment"""
    from models.db import DBStorage
    db = DBStorage()
    comment_data = request.json
    if not comment_data:
        abort(400, "Not a JSON")
    if 'comment' not in comment_data.keys():
        abort(400, "Missing comment")

    try:
        with db:
            comment = db.get_comments_by_comment_id(comment_id)
            if not comment:
                abort(404, "Comment not found")
            comment.comment = comment_data['comment']
            db.save()
            return jsonify(comment.to_dict()), 200
    except Exception as e:
        abort(400)


@app_views.route('/comments/<string:item_id>', methods=['GET'], strict_slashes=False)
def get_comments(item_id):
    """Get comments for an item"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            comments = db.get_comments_by_item_id(item_id)
            if not comments:
                abort(404, "No comments found")
            all_comments = [comment.to_dict() for comment in comments]
            count_comments = len(all_comments)
            response = {
                'count': count_comments,
                'comments': all_comments
            }
            return jsonify(response), 200
    except Exception as e:
        abort(400)


@app_views.route('/comments/<string:comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(comment_id):
    """Delete a comment"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            comment = db.get_comments_by_comment_id(comment_id)
            if not comment:
                abort(404, "Comment not found")
            db.delete(comment)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(400)
