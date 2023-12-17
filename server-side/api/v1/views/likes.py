from flask import Blueprint, request, jsonify
from models import db, Like

likes_bp = Blueprint('likes', __name__, url_prefix='/api/v1/likes')


@likes_bp.route('/', methods=['POST'])
def create_like():
    data = request.json

    # Assuming you have a database model for likes
    new_like = Like(
        user_id=data.get('user_id'),
        post_id=data.get('post_id')
        # Add more fields as needed
    )

    db.session.add(new_like)
    db.session.commit()

    return jsonify({'message': 'Like created successfully'}), 201


@likes_bp.route('/<like_id>', methods=['DELETE'])
def delete_like(like_id):
    like = Like.query.get(like_id)

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Like deleted successfully'}), 200
    else:
        return jsonify({'error': 'Like not found'}), 404


@likes_bp.route('/post/<post_id>', methods=['GET'])
def get_likes_for_post(post_id):
    likes = Like.query.filter_by(post_id=post_id).all()

    if likes:
        return jsonify({'likes': [like.serialize() for like in likes]}), 200
    else:
        return jsonify({'message': 'No likes found for the post'}), 404
