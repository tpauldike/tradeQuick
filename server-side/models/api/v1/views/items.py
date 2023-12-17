from flask import abort, request, jsonify
from dotenv import load_dotenv
from os import getenv
from api.v1.views import app_views

load_dotenv()


@app_views.route('/items', methods=['POST'], strict_slashes=False)
def create_item():
    """Create a new item"""
    from models.db import DBStorage
    db = DBStorage()
    item_data = request.json
    if not item_data:
        abort(400, "Not a JSON")
    if 'user_id' not in item_data.keys():
        abort(400, "Missing user_id")
    if 'item_name' not in item_data.keys():
        abort(400, "Missing item name")
    if 'description' not in item_data.keys():
        abort(400, "Missing description")
    if 'sold' not in item_data.keys():
        abort(400, "Missing sold")
    if 'price' not in item_data.keys():
        abort(400, "Missing price")
    if 'photo1' not in item_data.keys():
        abort(400, "Missing photo1")
    try:
        with db:
            item = db.create_item(item_data)
            print(f"Item successfully created for {item_data['user_id']}")
            db.save()
            db.close()
            return jsonify(item.to_dict()), 201
    except Exception as e:
        abort(400)


@app_views.route('/items', methods=['GET'], strict_slashes=False)
def get_items():
    """Get all items"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            items = db.get_items()
            users_data = [{"user_id": item.user_id, "item_id": item.item_id,
                           "item_name": item.item_name, "price": item.price, "description": item.description,
                           "phone1": item.phone1, "sold": item.sold,
                           "created_at": item.created_at, "updated_at": item.updated_at} for item in items]
            return jsonify(users_data), 200
    except Exception as e:
        abort(400)


@app_views.route('/items/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_items_by_user_id(user_id):
    """
    - Get all items by user_id
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            items = db.get_items_by_user_id(user_id)
            items_data = [{"user_id": item.user_id, "item_id": item.item_id,
                           "item_name": item.item_name, "price": item.price, "description": item.description,
                           "phone1": item.phone1, "sold": item.sold,
                           "created_at": item.created_at, "updated_at": item.updated_at} for item in items]
            return jsonify(items_data), 200
    except Exception as e:
        abort(400)


@app_views.route('/items/<string:item_id', methods=['GET'], strict_slashes=False)
def get_item_by_item_id(item_id):
    """
    - Get item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            item = db.get_item_by_item_id(item_id)
            return jsonify(item.to_dict()), 200
    except Exception as e:
        abort(400)


@app_views.route('/items/<string:item_id>', methods=['PUT'], strict_slashes=False)
def update_item_by_item_id(item_id):
    """
    - Update item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    item_data = request.json
    if not item_data:
        abort(400, "Not a JSON")
    if 'user_id' not in item_data.keys():
        abort(400, "Missing user_id")
    if 'item_name' not in item_data.keys():
        abort(400, "Missing item name")
    if 'description' not in item_data.keys():
        abort(400, "Missing description")
    if 'sold' not in item_data.keys():
        abort(400, "Missing sold")
    if 'price' not in item_data.keys():
        abort(400, "Missing price")
    if 'photo1' not in item_data.keys():
        abort(400, "Missing photo1")
    try:
        with db:
            item = db.update_item_by_item_id(item_id, item_data)
            print(f"Item successfully updated for {item_data['user_id']}")
            db.save()
            return jsonify(item.to_dict()), 200
    except Exception as e:
        abort(400)


@app_views.route('/items/<string:item_id>', methods=['DELETE'], strict_slashes=False)
def delete_item_by_item_id(item_id):
    """
    - Delete item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            db.delete_item_by_item_id(item_id)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(400)
