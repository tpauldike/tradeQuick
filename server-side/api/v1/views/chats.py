from flask import abort, request, jsonify
from os import getenv
from api.v1.views import app_views



@app_views.route('/messages', methods=['POST'], strict_slashes=False)
def create_message():
    """
    - Create a new message
    """
    message_data = {}
    sender_id = request.form.get('sender_id')
    receiver_id = request.form.get('receiver_id')
    message = request.form.get('message')
    if not sender_id:
        abort(400, "Missing sender_id")
    if not receiver_id:
        abort(400, "Missing receiver_id")
    if not message:
        abort(400, "Missing message")
    message_data['sender_id'] = sender_id
    message_data['receiver_id'] = receiver_id
    message_data['message'] = message

    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            auth_user = request.current_user
            receiver = db.find_user_by_id(message['receiver_id'])
            if auth_user is not None:
                if auth_user.user_id != message_data['sender_id']:
                    abort(401, "Unauthorized")
            if receiver is None:
                abort(404, "No user found for that ID")
            new_message = db.create_message(message_data)
            if not new_message:
                abort(404, "Error creating message")
            db.save()
            return jsonify(new_message.to_dict()), 201
    except Exception as e:
        abort(400)


@app_views.route('/messages/<string:message_id>', methods=['PATCH'], strict_slashes=False)
def update_message(message_id):
    from models.db import DBStorage
    db = DBStorage()
    message_data = {}
    message = request.form.get('message')
    if not message:
        abort(400, "Missing message")
    message_data['message'] = message
    try:
        with db:
            auth_user = request.current_user
            new_message = db.get_messages_by_message_id(message_id)
            if not new_message:
                abort(404, "message not found")
            if auth_user is not None:
                if auth_user.user_id != new_message.sender_id:
                    abort(401, "Unauthorized")
            new_message.message = message_data['message']
            db.save()
            return jsonify(new_message.to_dict()), 200
    except Exception as e:
        print(e)
        abort(401)


@app_views.route('/message/<string:message_id>', methods=['DELETE'], strict_slashes=False)
def delete_message(message_id):
    """
    - Delete a message
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            auth_user = request.current_user
            message = db.get_messages_by_message_id(message_id)
            if not message:
                abort(404, "message not found")
            if auth_user is not None:
                if auth_user.user_id != message.sender_id:
                    abort(401, "Unauthorized")
            db.delete(message)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(401)


@app_views.route('/messages/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_all_user_chat(user_id):
    """
    - Delete all messages from a user
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            auth_user = request.current_user

            # Retrieve messages
            messages = db.get_messages_by_user_id(user_id)

            # Check if there are no messages
            if not messages:
                abort(404, "Messages not found")

            # Check sender authorization and delete messages
            for message in messages:
                if auth_user is not None and auth_user.user_id != message.sender_id:
                    abort(401, "Unauthorized")
                db.delete(message)

            # Save changes after all messages have been deleted
                db.save()
            return jsonify({}), 200
    except Exception as e:
        print(e)
        return jsonify({}), 200
