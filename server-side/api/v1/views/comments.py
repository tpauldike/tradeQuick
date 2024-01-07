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
    comment_data = {}

    commenter = request.form.get('commenter')
    item_id = request.form.get('item_id')
    comment = request.form.get('comment')
    if not commenter:
        abort(400, "Missing commenter")
    if not item_id:
        abort(400, "Missing item_id")
    if not comment:
        abort(400, "Missing comment")
    
    comment_data['commenter'] = commenter
    comment_data['item_id'] = item_id
    comment_data['comment'] = comment

    try:
        with db:
            auth_user = request.current_user
            if auth_user is not None:
                if auth_user.user_id != comment_data['commenter']:
                    abort(401, "Unauthorized")
            new_comment = db.create_comment(comment_data)
            if not new_comment:
                abort(400, "Error creating comment")
            db.save()
            return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        abort(401)


@app_views.route('/comments/<string:comment_id>', methods=['PATCH'], strict_slashes=False)
def update_comment(comment_id):
    """Update a comment"""
    from models.db import DBStorage
    db = DBStorage()
    comment_data = {}

    comment = request.form.get('comment')
    if not comment:
        abort(400, "Missing comment")
    
    comment_data['comment'] = comment

    try:
        with db:
            auth_user = request.current_user
            comment = db.get_comments_by_comment_id(comment_id)
            if not comment:
                abort(404, "Comment not found")
            if auth_user is not None:
                if auth_user.user_id != comment.commenter:
                    abort(401, "Unauthorized")
            comment.comment = comment_data['comment']
            db.save()
            return jsonify(comment.to_dict()), 200
    except Exception as e:
        print(e)
        abort(401)


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
            auth_user = request.current_user
            comment = db.get_comments_by_comment_id(comment_id)
            if not comment:
                abort(404, "Comment not found")
            if auth_user is not None:
                if auth_user.user_id != comment.commenter:
                    abort(401, "Unauthorized")
            db.delete(comment)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        print(e)
        abort(401)
