This is a document that is describing or explaining every API endpoint(TradeQuick) and it's usage.

## Users

# GET http://0.0.0.0:5000/api/v1/users

# Description

* This endpoint does not require authentication. 
* This endpoint retrieves all registered users.

# POST http://0.0.0.0:5000/api/v1/users

# Description

* This endpoint does not require authentication.
* Creates a new user with the data below


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

* This values are mock data that are used for this example purpose only. 


# POST http://0.0.0.0:5000/api/v1/users/login

# Description

* This endpoint creates a new login session for a user with their email and password
* With this session created users are authenticated automatically.


# GET http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication.
* This endpoint retrieves a registered user based on their user_id.

# GET http://0.0.0.0:5000/api/v1/users/me

# Description

* This endpoint requires authentication.
* This endpoint gets the current authenticated user.

# POST http://0.0.0.0:5000/api/v1/users/logout

# Description

* This endpoint logs out a user and deletes the authenticated session


# POST http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication.
* This endpoint reset a user password  based on their user_id.
* The field below are required to reset their password

|      key     |     value     |
|:------------:|:-------------:|
|  email       |johnd@gmail.com|
| password     |   1234        |
| new_password |   pass1234    |
   

# DELETE http://0.0.0.0:5000/api/v1/users/<user_id>

# Description

* This endpoint requires authentication.
* This endpoint deletes the current user entire account and it's relations.

