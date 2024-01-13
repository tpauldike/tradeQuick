# tradeQuick
*An app that let people within a locality buy/sell used items (ALX portfolio project)*

**Web URL:** [https://tradequick.vercel.app](https://tradequick.vercel.app)

![the_landing_page](https://github.com/tpauldike/rough_work/blob/main/designs/tradeQuick-landing-page.jpg)

## About the project
The web app is a market place for selling used items that someone else might be interested in, the seller uploads certain information such as the photos of it,
description and price and the buyer can either comment on the post or send private message.
**Disclaimer:**
1. Every user's security is in his hands. All users are to deal with people within their locality or close range and meet in public places before paying for
the goods.
3. The risk of purchasing spoilt or bad items is entirely the users. He/she must test the item very well (if possible) before paying for it.
4. It is safer to buy from store owners but any user can sell or buy on the app, so everyone has got to be very careful while dealing with anyone, as we are
not responsible for the outcome of the deal.

### Features
1. Logo and attractive user interface
2. Contents are available to the public (Read only)
3. No transaction except authenticated
4. User sign up and authentication
5. User account management (viewing, updating and deleting own account)
6. Items management (viewing, uploading, editing and deleting own items, and marking the sold ones as sold)
7. Search for items (public)
8. Social interaction
  - Comment on items for sale
  - like/dislike items for sale
  - Chat privately with the seller
7. Compulsory mobile number verification
8. SMS and email notifications, based on the user's preference.
  
### Extras
- Support/help
- Portfolio (about the team)
- About (about the app)
- Contact us

### Scope
Version 1.0 of the app is designed to be used within Nigeria only

## Team
**Front End**
- [Topman Paul-Dike](https://github.com/tpauldike)

**Back End**
- [David Gregs](https://github.com/davidgregs87)
- [Otueh Chibueze](https://github.com/OChibu)

## Technologies

### Programming Languages Used
**Front End**
- `HTML`
- `CSS`
- `JavaScript`

**API**
- `Python` (`Flask`)

**Database**
- `MySQL`

### Third Party Services
1. Cloudinary (for photo uploads)
2. Google authentication
3. Facebook authentication
4. Brevo (mailing/SMS services)

## Usage/Installation
To install and run the app locally or in a development environment, follow the instructions below:
### Front End
```bash
# Clone the git repository
:$ git clone https://github.com/tpauldike/tradeQuick.git

# Move into the directory
:$ cd tradeQuick

# Open it with your code editor (VScode for instance)
:$ code .

# Make sure you have the live server extension installed, then render index.html on your browser
# You may as well change the environment variables in the scripts to that of the local server, you're using.
```

> To have the app server and the database-serrver running locally as well , follow the instructions for server installation below:

### Back End

*This is an installation guide on how to setup the backend in order for you to be able to use tradequick API for backend operations. Throughout this manual we assume that mysql server is installed and running on your local machine. Also check the requirements.txt file to install the requirements required for the backend.*

```bash
# Clone the git repository if you haven't
:$ git clone https://github.com/tpauldike/tradeQuick.git
```

### Creating tables and relations

Firstly, we will use the script tradequick.sql to create all database, tables and relations in mysql. replace username with the correct mysql user

```bash
# Create database, tables and relations
:$ cat tradequick.sql | mysql -u <user_name> -p
```

### Environment Variables

#### Connecting to the Database

The API utilizes the following environment variables to connect to the database, we can assume that you have mysql server running on your machine:

* DB_HOST: The hostname or IP address of the database server.

Example: localhost
* DB_PORT: The port number on which the database server is listening.

Example: 3306
* DB_NAME: The name of the database to connect to.

Example: mydatabase
* DB_USER: The username for authenticating with the database server.

Example: myuser
* DB_PASSWORD: The password for authenticating with the database server.

Example: secretpassword

#### Connecting to the Flask

The API utilizes the following environment variables to connect to the flask, we can assume have flask installed:

* API_HOST: The hostname or IP address of the flask server.

Example: 0.0.0.0
* API_PORT: The port number on which the flask server is listening.

Example: 5000
* API_SECRET_KEY: flask secret key to handle sessions and other operations.

Example: 4354d34rf34f34112e1

#### Authentication variables

* AUTH_TYPE: The type of authentication the API uses.

* SESSION_NAME: The cookie name to be stored.

* SESSION_DURATION: The time the cookie should be cached before expiry. Note that the time is in minutes.


#### Cloudinary variables

All images are being stored in the cloud via cloudinary. Below are cloudinary credential for our API

* CLOUD_NAME: The name of the cloud our images are being stored.

* API_KEY: Cloudinary API key for API interaction and operations.

* API_SECRET: Cloudinary API secret key for API interaction and operations.


#### Using a Configuration File

Create a configuration file (e.g., .env) in the root directory of your project and populate it with the following content:

```
dbName=<db_name>
dbUser=<db_user>
dbHost=<db_host>
dbPasswd=<db_passwd>
dbPort=3306

API_HOST=0.0.0.0
API_PORT=5000
API_SECRET_KEY=07e18dc59990596ecb154e02de050dc8f117d8863ec759918d26627862007738

AUTH_TYPE=session_db_auth
SESSION_NAME=_my_session_id
SESSION_DURATION=43200

CLOUD_NAME=dtnj3pohk
API_KEY=397179555983987
API_SECRET=YL1k15fZkHdUh47Kf8puyvm0FRs
```

#### Using Command Line

Set the environment variables using command line:

```bash
:$ export dbName=<db_name>
:$ export dbUser=<db_user>
:$ export dbHost=<db_host>
:$ export dbPasswd=<db_passwd>
:$ export dbPort=3306

:$ export API_HOST=0.0.0.0
:$ export API_PORT=5000
:$ export API_SECRET_KEY=07e18dc59990596ecb154e02de050dc8f117d8863ec759918d26627862007738

:$ export AUTH_TYPE=session_db_auth
:$ export SESSION_NAME=_my_session_id
:$ export SESSION_DURATION=43200

:$ export CLOUD_NAME=dtnj3pohk
:$ export API_KEY=397179555983987
:$ export API_SECRET=YL1k15fZkHdUh47Kf8puyvm0FRs
```

*After setting these environment variables*

```bash
# Move into the directory
:$ cd tradeQuick/server-side

# Start Flask
:$ python3 -m api.v1.app 

# Please ensure that the environment variables are set, mysql server is running and all requirements are installed before starting flask 
```

If you followed everything correctly you should see this
```
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.20.88.152:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 110-366-493
```








## Authors
The file [AUTHOR.md](./AUTHOR.md) contains the names of the authors and their email addresses.

Feel free to contribute to the project, outside contributors from February 2024 and not before then, please. You may refer to [CONTRIBUTION.md](./CONTRIBUTION.md)
to know how to make an acceptable contribution to this project

###### &copy; 2023 tradeQuick. All rights reserved.
