from flask import Blueprint, request, jsonify
from models import db, Comment

comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1/comments')


@comments_bp.route('/', methods=['POST'])
def create_comment():
    data = request.json

    # Assuming you have a database model for comments
    new_comment = Comment(
        user_id=data.get('user_id'),
        post_id=data.get('post_id'),
        content=data.get('content')
        # Add more fields as needed
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment created successfully'}), 201


@comments_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    else:
        return jsonify({'error': 'Comment not found'}), 404


@comments_bp.route('/post/<post_id>', methods=['GET'])
def get_comments_for_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()

    if comments:
        return jsonify({'comments': [comment.serialize() for comment in comments]}), 200
    else:
        return jsonify({'message': 'No comments found for the post'}), 404
