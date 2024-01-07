from models.db import DBStorage
from collections import Counter

db = DBStorage()

item_id = 'be25de1b-4c76-4798-b26b-cd59069bbeed'

try:
    with db:
        likes = db.get_like_by_item_id_all(item_id)
        if not likes:
            print('[]')
        all_likes = [like.to_dict() for like in likes]
        c = Counter()
        for count in all_likes:
            c[count['liked']] += 1
        response = {
            'liked': c[True],
            'dislike': c[False]
        }
        print(response)
except Exception as e:
    print(e)