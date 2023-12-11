from prototype import User
from db import DBStorage

try:
    db = DBStorage()

    mock_data = {
        'fullname': 'Adam Ben',
        'verified': False,
        'email': 'bennyAdam@example.com',
        'password': 'sd@#@sds',
        'gender': 'Male',
        'phone1': '3453453456',
        'phone2': '8674532345',
        'about': "A Lover of God.",
        'address': '2E4 Qyade way',
        'town': 'Brooklyn',
        'city': 'Texas',
        'state': 'CA',

    }

    new_data = User(**mock_data)
    with db:
        db.new(new_data)
        db.save()

except Exception as e:
    print(f"An error occurred: {e}")

# The session will be closed automatically when exiting the 'with' block
