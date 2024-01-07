**This web app is a market place for selling used items that someone else might be interested in, the seller uploads certain information such as the photos of it, description and price and the buyer can either comment on the post or send private message. This is a document that is describing or explaining every API endpoint(TradeQuick) and it's usage.**

### Users

#### GET http://0.0.0.0:5000/api/v1/users

##### Description

* This endpoint does not require authentication. 
* This endpoint retrieves all registered users.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users"
```

#### POST http://0.0.0.0:5000/api/v1/users

##### Description

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
curl -XPOST 'http://0.0.0.0:5000/api/v1/users' \
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

#### POST http://0.0.0.0:5000/api/v1/users/login

##### Description

* This endpoint creates a new login session for a user with their email and password
* With this session created users are authenticated automatically.

Example usage could be like this;
```
curl -XPOST 'http://0.0.0.0:5000/api/v1/users/login' \
--form 'email="enola.fish@gmail.com"' \
--form 'password="1234"'
```


#### GET http://0.0.0.0:5000/api/v1/users/<user_id>

##### Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint retrieves a registered user based on their user_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users/<user_id>"
```

#### GET http://0.0.0.0:5000/api/v1/users/me

##### Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint gets the current authenticated user.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/users/me"
```

#### POST http://0.0.0.0:5000/api/v1/users/logout

##### Description

* This endpoint logs out a user and deletes the authenticated session

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/users/logout"
```


#### POST http://0.0.0.0:5000/api/v1/users/<user_id>

##### Description

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
curl -XPOST "http://0.0.0.0:5000/api/v1/users/<user_id>"
--form 'email="johnd@gmail.com"' \
--form 'password="1234"' \
--form 'new_password="new_pass1234"'
```
   

#### DELETE http://0.0.0.0:5000/api/v1/users/<user_id>

##### Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint deletes the current user entire account and it's relations.

Example usage could be like this;
```
curl -XDELETE "http://0.0.0.0:5000/api/v1/users/<user_id>"
```

#### PUT http://0.0.0.0:5000/api/v1/users/<user_id>

##### Description

* This endpoint requires authentication which will be the current user to carry out this operation.
* This endpoint updates the information of the user.
* This endpoint updates any information the user might want to change

Example usage could be like this;
```
curl -XPUT "http://0.0.0.0:5000/api/v1/users/19ebfab1-db5d-499c-95a5-fb74cbfd5d44" -H "Content-type: multipart/form-data" \ 
-F "fullname=Kayla Fisher" \
-F "phone1=341-545-2342" \
-F "about=God is working it out" \
-F"address=34D newton ave" \
-F "town=New Haven" \
-F "city=Los Angeles" \
-F "state=CA" \
-F "photo=@../server-side/api/v1/views/landscape.jpg"
```


### Items

#### GET http://0.0.0.0:5000/api/v1/items

##### Description

* This endpoint does not requires authentication. 
* This endpoint retrieves all item posted by all registered users.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/items"
```

#### POST http://0.0.0.0:5000/api/v1/items

##### Description

* This endpoint requires authentication. 
* This endpoint post an item for sale by a registered user.

|      key         |     value     |
|:----------------:|:-------------:|
|     item_name    |     Watch     |
|    description   |Quality and durable watch|
|     price        |   1000000     |
|     photo1       | 3v-a42-6e4.jpg|
|     photo2       | 32-df-23ds.jpg|
|     photo3       | 3df-2ecwsd.jpg|

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/items"
-H "Content-type: multipart/form-data" \
-F "item_name=Watch" \
-F "description=Quality and durable watch" \
-F "price=100000" \
-F "photo1=@../path/to/gadget1.jpg" \
-F "photo2=@../path/to/gadget2.jpg" 
```

#### GET http://0.0.0.0:5000/api/v1/items/<user_id>

##### Description

* This endpoint does not require authentication. 
* This endpoint retrieves all items posted by a user based on their user_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/items/<user_id>"
```

#### GET http://0.0.0.0:5000/api/v1/item/<item_id>

##### Description

* This endpoint does not require authentication. 
* This endpoint retrieves an item posted by a user based on it's item_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/item/<item_id>"
```

#### PUT http://0.0.0.0:5000/api/v1/items/<item_id>

##### Description

* This endpoint requires authentication. 
* This endpoint updates an item based on it's item_id.

Example usage could be like this;
```
curl -XPUT "http://0.0.0.0:5000/api/v1/items/<item_id>"
-H "Content-type: multipart/form-data" \
-F "item_name=TV" \
-F "description=LG 42 inch HDMI Tv" \
-F "price=150000" \
-F "photo1=@../path/to/TV1.jpg" \
-F "photo2=@../path/to/TV2.jpg" 
```

#### DELETE http://0.0.0.0:5000/api/v1/items/<item_id>

##### Description

* This endpoint requires authentication. 
* This endpoint deletes an item posted by a user based on it's item_id.

Example usage could be like this;
```
curl -XDELETE "http://0.0.0.0:5000/api/v1/item/<item_id>"
```

### Ratings

#### POST http://0.0.0.0:5000/api/v1/ratings

##### Description

* This endpoint requires authentication. 
* This endpoint post a new rating.

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/ratings" \
-H "Content-type: multipart/form-data" \
-F "user_id=19ebfab1-db5d-499c-95a5-fb74cbfd5d44" \
-F "comment=I love this watch" \
-F "rating=4"
```

#### GET http://0.0.0.0:5000/api/v1/ratings

##### Description

* This endpoint does not require authentication. 
* This endpoint retrieves all ratings posted by all registered users.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/ratings"
```

### Likes

#### POST http://0.0.0.0:5000/api/v1/likes/0

##### Description

* This endpoint requires authentication
* Passing the parameter 0 or 1 set dislike or like an item respectively
* Sending a post request twice with the same parameter undo the dislike or like and sets it to like or dislike respectively.

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/likes/0" -d "user_id=<user_id>&item_id=<item_id>" --cookie="<cookie_value>"
```

#### GET http://0.0.0.0:5000/api/v1/likes/<item_id>

##### Description

* This endpoint requires authentication. 
* This endpoint retrieves all likes and dislikes based on an item_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/likes/<item_id>" --cookie="<cookie_value>"


### Comments

#### POST http://0.0.0.0:5000/api/v1/comments

##### Description

* This endpoint requires authentication. 
* This endpoint post a new comment.

Example usage could be like this;
```
curl -XPOST "http://0.0.0.0:5000/api/v1/comments" \
-H "Content-type: multipart/form-data" \
-F "commenter=19ebfab1-db5d-499c-95a5-fb74cbfd5d44" \
-F "comment=I love this TV" \
-F "item_id=a2585ea3-dd0b-451a-83a6-a1ee52c02580"
```

#### PATCH http://0.0.0.0:5000/api/v1/comments/<comment_id>

##### Description

* This endpoint requires authentication. 
* This endpoint updates a comment based on their comment_id.

Example usage could be like this;
```
curl -XPATCH "http://0.0.0.0:5000/api/v1/comments/<comment_id>"  -d "comment=Do you have the latest one?" --cookie=<cookie_value>
```

#### http://0.0.0.0:5000/api/v1/comments/<item_id>

##### Description

* This endpoint requires authentication. 
* This endpoint retreives a comment based on the item_id.

Example usage could be like this;
```
curl "http://0.0.0.0:5000/api/v1/comments/<item_id> --cookie=<cookie_value>
```

#### DELETE http://0.0.0.0:5000/api/v1/comments/comment_id

##### Description

* This endpoint requires authentication. 
* This endpoint deletes a comment based on the comment_id.

Example usage could be like this;
```
curl -XDELETE "http://0.0.0.0:5000/api/v1/comments/<comment_id> --cookie=<cookie_value>
```

### Chats

