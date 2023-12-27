This is a document that is describing or explaining every API endpoint(TradeQuick) and it's usage.

## Users

# GET http://0.0.0.0:5000/api/v1/users

# Description

* This endpoint does not require authentication. 
* This endpoint retrieves all registered users.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users"
```

# POST http://0.0.0.0:5000/api/v1/users

# Description

* This endpoint does not require authentication.
* Creates a new user with the data below
* This will also automtically create a default avatar for you as your profile pics
which you can update later to the photo you would like to use.

|      key         |     value     |
|:----------------:|:-------------:|
|     fullname     |   John Doe    |
|     email        |johnd@gmail.com|
|     password     |   1234        |
|     gender       |  male         |
|     about        |   wefsdwewed  |
|     phone1       |   232-442-646 |
|     phone2       |   731-843-742 |
|     address      |  23D3 cray ave|
|     town         |  old town     |
|     city         |  new city     |
|     state        |      CA       |

Example usage could be like this;
```
curl --location 'http://0.0.0.0:5000/api/v1/users' \
--form 'fullname="Glory Maurice"' \
--form 'email="glo.maurice@gmail.com"' \
--form 'gender="Female"' \
--form 'password="1234"' \
--form 'about="I love Jesus"' \
--form 'phone1="232-323-2322"' \
--form 'address="23d32 bradway ave"' \
--form 'photo="new_pic.png"' \
--form 'town="maryland"' \
--form 'city="boston"' \
--form 'state="NY"'
``` 
* This values are mock data that are used for this example purpose only.

# POST http://0.0.0.0:5000/api/v1/users/login

# Description

* This endpoint creates a new login session for a user with their email and password
* With this session created users are authenticated automatically.

Example usage could be like this;
```
curl -XPOST 'http://0.0.0.0:5000/api/v1/users/login' \
--form 'email="enola.fish@gmail.com"' \
--form 'password="1234"'
```


# GET http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint retrieves a registered user based on their user_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users/<user_id>"
```

# GET http://0.0.0.0:5000/api/v1/users/me

# Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint gets the current authenticated user.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users/me"
```

# POST http://0.0.0.0:5000/api/v1/users/logout

# Description

* This endpoint logs out a user and deletes the authenticated session

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/users/logout"
```


# POST http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint reset a user password  based on their user_id.
* The field below are required to reset their password

|      key     |     value     |
|:------------:|:-------------:|
|  email       |johnd@gmail.com|
| password     |   1234        |
| new_password |   pass1234    |

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/users/<user_id>" --cookie "_my_session_id=e86b182f-7889-4f50-941f-726f38caf24b" --form 'email="enola.fish@gmail.com"' \
--form 'password="1234"' \
--form 'new_password="1234"'
```
   

# DELETE http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint deletes the current user entire account and it's relations.

Example usage could be like this;
```
curl -XDELETE "http://0.0.0.0:5000/api/v1/users/<user_id>" --cookie "_my_session_id=e86b182f-7889-4f50-941f-726f38caf24b"
```

# PUT http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint updates the information of the user.
* This endpoint updates any information the user might want to change

Example usage could be like this;
```
curl -XPUT "http://0.0.0.0:5000/api/v1/users/19ebfab1-db5d-499c-95a5-fb74cbfd5d44" -H "Content-type: multipart/form-data" -F "fullname=Kayla Fisher" -F "phone1=341-545-2342" -F "about=God is working it out" -F"address=34D newton ave" -F "town=New Haven" -F "city=Los Angeles" -F "state=CA" -F "photo=@../server-side/api/v1/views/landscape.jpg" --cookie "_my_session_id=e86b182f-7889-4f50-941f-726f38caf24b"
```
