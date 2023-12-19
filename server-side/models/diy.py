from db import DBStorage

db = DBStorage()

user_id = '4a4cc176-43b5-466c-9b64-4e0e011e8487'

with db as session:
    user = session.find_user_by_id(user_id)
    if user is None:
        print(f'No user found with email {user_id}')
    else:
        print(f'Found user: {user.fullname}')
