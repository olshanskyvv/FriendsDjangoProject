# Friends service

## Technologies

According to the task, this service was developed on Django REST Framework.\
I have chosen SQLite to simplify database connection.

## Description

This is service for friends that support this list of functions
- registration of new users
- sending of friend request from one user to another
- accepting and declining friend request
- viewing incoming and outgoing requests of user
- viewing friends list of user
- checking of friendship status of two users
- deleting friends from user friends list
- making two users friends if they have request from each other

## API

This service use API interface. 
In includes this URLs and http methods (for more details look *openapi.yml*):

- **/api/users** - Users list interface
  - *GET* - view a list of registered users
  - *POST* - register a new user
- **/api/users/{username}/friends** - User's friend list interface
  - *GET* - view user's friends list
  - *POST* - send new friend request from user
  - *DELETE* - delete friend from user's friends list
- **/api/users/{username}/incoming** - User's incoming list interface
  - *GET* - view user's incoming friend requests
  - *POST* - answer to friend request
- **/api/users/{username}/outgoing** - User's outgoing list interface
  - *GET* - view user's outgoing friend requests
- **/api/requests** - Friend requests list interface
  - *GET* - view a list of unanswered requests
- **/api/friends** - Friend status checking interface
  - *GET* - get status of friendship of two users

## Installation

You can install and run service in two ways:
- docker
- python shell

In both cases you need to download source code and enter the resulting directory.
You need to run this two commands:
```shell
git clone https://github.com/olshanskyvv/FriendsDjangoProject.git
cd FriendsDjangoProject
```

### Python shell (Unix)

For this installation method you need to have installed Python and Pip.

Run this commands:
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

*After that service is ready to work!*

To start app - run:
```shell
python3 manage.py runserver 0.0.0.0:8000
```
Service will be able on http://localhost:8000

To stop app - press `ctrl + c`

### Docker

For this installation method you need only installed and started Docker.

For creating and starting Docker container just run:
```shell
docker-compose up
```
Service will be able on http://localhost:8000

To stop app - press `ctrl + c` or use **Docker Desktop**

## Using samples

We have running application on http://localhost:8000. Let's try to use it.

### Users

Let's try to view registered users. Send GET request to `/api/users` and 
receive response `[]`, because we have no registered users.

Register user with username "user". Send POST request to `/api/users` with body
```json
{
    "username": "user"
}
```
and receive registered user with code `200 OK`.
```json
{
    "id": 1,
    "username": "user"
}
```
In the same way we add 'user1' and 'user2'.

### Friends and requests

Let's try to view user's friends. Send GET request to `/api/users/user/friends`
and receive response with code `404 Not Found`.
```json
{
    "error": "friends not found"
}
```

Let's make user and user1 become friends. Create friend response from user to user1.
Send POST request to `/api/users/user/friends` with body
```json
{
    "username": "user1"
}
```
and receive created request with code `201 Created`
```json
{
    "sender": {
        "id": 1,
        "username": "user"
    },
    "recipient": {
        "id": 2,
        "username": "user1"
    }
}
```

Let's view this outgoing request from user. 
Send GET request to `/api/users/user/outgoing`
and receive our request with code `200 OK`
```json
[
    {
        "recipient": {
            "id": 2,
            "username": "user1"
        }
    }
]
```

Let's view incoming request to user1 and accept it.
Send GET request to `/api/users/user1/incoming` 
and receive request from user with code `200 OK`
```json
[
    {
        "sender": {
            "id": 1,
            "username": "user"
        }
    }
]
```

Send POST request to `/api/users/user1/incoming` with body
```json
{
    "username": "user",
    "answer": true
}
```
to accept request and add user to friends. Receive response with code `200 OK`
```json
{
    "response": "friend user added"
}
```

To view user1's friends send GET request to `/api/users/user1/friends`
and receive response with code `200 OK`
```json
[
    {
        "id": 1,
        "username": "user"
    }
]
```

Let's send request from user2 to user1 and view requests list.
Send POST request to `api/users/user2/friends` with body
```json
{
    "username": "user1"
}
```
and receive created request with code `201 Created`
```json
{
    "sender": {
        "id": 3,
        "username": "user2"
    },
    "recipient": {
        "id": 2,
        "username": "user1"
    }
}
```

After that view list of unanswered requests.
Send GET request to `/api/requests` and receive requests with code `200 OK`
```json
[
    {
        "sender": {
            "id": 3,
            "username": "user2"
        },
        "recipient": {
            "id": 2,
            "username": "user1"
        }
    }
]
```

Check friendship status of different pairs of users 
by sending GET request to `/api/friends` with body
```json
{
    "username1": "first_user",
    "username2": "second_user"
}
```

#### user and user1
Code `200 OK`
```json
{
    "response": "you are friends"
}
```

#### user1 and user2
Code `200 OK`
```json
{
    "response": "user1 have incoming request from user2"
}
```

#### user2 and user1
Code `200 OK`
```json
{
    "response": "user2 have outgoing request to user1"
}
```

#### user and user2
Code `200 OK`
```json
{
    "response": "you are not friends and there are no friend requests"
}
```