# tradeQuick API
Here is a brief description of the endpoints that were listed for version 1.0 of the application, tradeQuick.

## Authentication Endpoints
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /users | Create a new user |
| POST | /users/login | Login the user |
| POST | /users/{user_id} | Reset user password |
| POST | /users/logout | Logout the user |

## Other Users' Endpoints
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| GET | /users | Get all registered users |
| GET | /users/{user_id} | Get a single user |
| PUT | /users/{user_id} | Update the user with the `user_id` |
| DELETE | /users/{user_id} | Delete the user and all data associated with the user |

## Enpoints for Managing Items for Sale
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /items | Create a new item for sale |
| GET | /items | Get all items for sale (open to the public with no need for authentication); displayed on the landing page |
| GET | /items/{user_id} | Get all items belonging to the user with the `user_id` |
| GET | /items/{item_id} | Get a single item |
| PUT | /items/{item_id} | Update a particular item |
| DELETE | /items/{item_id} | Delete a particular item |

## Like, Dislike, and Unlike (undo)
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /likes/{status} | `status` here is an integer (either 0 or 1); 0 for dislike, 1 for like. Sending the request with a particular status two consecutive times will undo the like or dislike. Sending a status of 1 after sending 0 will change like to dislike and vice versa |
| GET | likes/{item_id} | Returns a count of all the likes and dislikes on the item with the `item_id` |

## Endpoints for Comments
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /comments | Add a new comment to an item for sale |
| PATCH | /comments/{comment_id} | Update the comment with the id |
| GET | /comments/{item_id} | Get all the comments on a particular item or post and return the count |
| DELETE | /comments/{comment_id} | Delete the particular comment with `comment_id` |

## Private Messages' Endpoints
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /messages | Create a new message |
| PATCH | /messages/{message_id} | Update a sent message |
| DELETE | /messages/{messages_id} | Delete a particular message |
| DELETE | /messages/{user_id} | Delete an entire chat with a particular user |

## Rating the Application
| Request type | Endpoint | Description |
| ----- | ----- | ---- |
| POST | /ratings | Rate the app |
| GET | ratings | get all ratings |

## Third Party Integrations
- Google authentication
- Facebook authentication
- UUID v4 for all IDs
- Brevo for emails, for notifications and OTPs
- Cloudinary for storing photos

The above were the initial endpoints listed out while aiming for MVP in 3 weeks; improvements or modifications are allowed, where necessary.

For help, kindly contact [Topman Paul-Dike](https://github.com/tpauldike)

###### &copy; 2023 tradeQuick. All rights reserved.