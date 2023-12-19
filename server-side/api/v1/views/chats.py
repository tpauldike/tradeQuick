from flask import abort, request, jsonify
from dotenv import load_dotenv
from os import getenv
from api.v1.views import app_views

load_dotenv()


@app_views.route('/messages', methods=['POST'], strict_slashes=False)
def create_message():
    """
    - Create a new message
    """
    message_data = request.json
    if not message_data:
        abort(400, "Not a JSON")
    if 'sender_id' not in message_data.keys():
        abort(400, "sender_id missing")
    if 'receiver_id' not in message_data.keys():
        abort(400, "receiver_id missing")
    if 'message' not in message_data.keys():
        abort(400, "message missing")
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            new_message = db.create_message(message_data)
            db.save()
            if not new_message:
                abort(400, "Error creating message")
            return jsonify(new_message.to_dict()), 201
    except Exception as e:
        abort(400)


@app_views.route('/messages/<string:message_id>', methods=['PATCH'], strict_slashes=False)
def update_message(message_id):
    from models.db import DBStorage
    db = DBStorage()
    message_data = request.json
    if not message_data:
        abort(400, "Not a JSON")
    if 'message' not in message_data.keys():
        abort(400, "Missing message")
    try:
        with db:
            new_message = db.get_messages_by_message_id(message_id)
            if not new_message:
                abort(404, "message not found")
            new_message.message = message_data['message']
            db.save()
            return jsonify(new_message.to_dict()), 200
    except Exception as e:
        abort(400)


@app_views.route('/messages/<string:message_id>', methods=['DELETE'], strict_slashes=False)
def delete_message(message_id):
    """
    - Delete a message
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            message = db.get_messages_by_message_id(message_id)
            if not message:
                abort(404, "message not found")
            db.delete(message)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(400)


@app_views.route('/messages/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_all_user_chat(user_id):
    """
    - Delete all messages from a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            messages = db.get_messages_by_user_id(user_id)
            if not messages:
                abort(404, "messages not found")
            for message in messages:
                db.delete(message)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(400)
