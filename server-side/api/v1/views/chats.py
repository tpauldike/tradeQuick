from flask import Blueprint, request, jsonify
from models import db, ChatMessage

chats_bp = Blueprint('chats', __name__, url_prefix='/api/v1/chats')


@chats_bp.route('/', methods=['POST'])
def send_message():
    data = request.json

    # Assuming you have a database model for chat messages
    new_message = ChatMessage(
        sender_id=data.get('sender_id'),
        receiver_id=data.get('receiver_id'),
        message=data.get('message')
        # Add more fields as needed
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 201


@chats_bp.route('/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = ChatMessage.query.get(message_id)

    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    else:
        return jsonify({'error': 'Message not found'}), 404


@chats_bp.route('/user/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    # Retrieve all messages where the user is either the sender or receiver
    messages = ChatMessage.query.filter(
        (ChatMessage.sender_id == user_id) | (ChatMessage.receiver_id == user_id)
    ).all()

    if messages:
        return jsonify({'messages': [message.serialize() for message in messages]}), 200
    else:
        return jsonify({'message': 'No messages found for the user'}), 404
