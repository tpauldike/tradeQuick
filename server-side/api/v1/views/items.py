from api.v1.views import app_views
from flask import abort, request, jsonify
from os import getenv




@app_views.route('/items', methods=['POST'], strict_slashes=False)
def new_item():
    """Create a new item"""
    from models.db import DBStorage
    db = DBStorage()
    item_data = {}
    
    user_id = request.form.get('user_id')
    item_name = request.form.get('item_name')
    description = request.form.get('description')
    price = request.form.get('price')
    photo1 = request.form.get('photo1')
    photo2 = request.form.get('photo2')
    photo3 = request.form.get('photo3')
    if not user_id:
        abort(400, "Missing user_id")
    if not item_name:
        abort(400, "Missing item name")
    if not description:
        abort(400, "Missing description")
    if not price:
        abort(400, "Missing price")
    if not photo1:
        abort(400, "Missing photo1")

    item_data['user_id'] = user_id
    item_data['item_name'] = item_name
    item_data['description'] = description
    item_data['price'] = price
    item_data['photo1'] = photo1
    item_data['photo2'] = photo2
    item_data['photo3'] = photo3

    try:
        with db:
            item = db.create_item(item_data)
            print(f"Item successfully created for {item_data['user_id']}")
            db.save()
            return jsonify(item.to_dict()), 201
    except Exception as e:
        print(e)


@app_views.route('/items', methods=['GET'], strict_slashes=False)
def retreive_items():
    """Get all items"""
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            items = db.get_items()
            item_data = [item.to_dict() for item in items]
            return jsonify(item_data), 200
    except Exception as e:
        print(e)


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
            items_data = [item.to_dict() for item in items]
            return jsonify(items_data), 200
    except Exception as e:
        abort(400)


@app_views.route('/item/<string:item_id>', methods=['GET'], strict_slashes=False)
def get_item_by_item_id(item_id):
    """
    - Get item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            items = db.find_items_by_item_id(item_id)
            if items is None:
                abort(404)
            item_data = items.to_dict()
            return jsonify(item_data), 200
    except Exception as e:
        print(e)
        abort(400)


@app_views.route('/items/<string:item_id>', methods=['PUT'], strict_slashes=False)
def update_item_by_item_id(item_id):
    """
    - Update item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    item_data = {}

    item_name = request.form.get('item_name')
    description = request.form.get('description')
    price = request.form.get('price')
    photo1 = request.form.get('photo1')
    photo2 = request.form.get('photo2')
    photo3 = request.form.get('photo3')
    
    if item_name is None:
        abort(400, "Missing item name")
    if description is None:
        abort(400, "Missing description")
    if price is None:
        abort(400, "Missing price")
    if photo1 is None:
        abort(400, "Missing photo1")

    item_data['item_name'] = item_name
    item_data['description'] = description
    item_data['price'] = price
    item_data['photo1'] = photo1
    item_data['photo2'] = photo2
    item_data['photo3'] = photo3


    try:
        with db:
            item = db.find_items_by_item_id(item_id)
            if item is None:
                abort(404)
            item.item_name = item_data['item_name']
            item.description = item_data['description']
            item_data.price = item_data['price']
            item_data.photo1 = item_data['photo1']
            item_data.photo2 = item_data['photo2']
            item_data.photo3 = item_data['photo3']
            print(f"Item successfully updated for {item_data['user_id']}")
            db.save()
            return jsonify({}), 200
    except Exception as e:
        print(e)
        return jsonify({}), 400


@app_views.route('/items/<string:item_id>', methods=['DELETE'], strict_slashes=False)
def delete_item_by_item_id(item_id):
    """
    - Delete item by item_id
    """
    from models.db import DBStorage
    db = DBStorage()
    try:
        with db:
            item = db.find_items_by_item_id(item_id)
            if item is None:
                abort(404)
            db.delete(item)
            db.save()
            return jsonify({}), 200
    except Exception as e:
        abort(400)
