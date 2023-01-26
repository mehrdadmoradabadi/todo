
# TODO app

A simple TODO Application writen with flask.
This app has swagger documention accessable through :`/apidocs` .
You can  use the `test.py` to check the api functionality.


## How to run

To run TODO App in development mode; Just use steps below:

1. Install `Python 3.10.0rc1`, `pip` in your system.
2. Clone the project `https://github.com/`.
3. Make development environment ready using commands below;

  ```bash
  git clone https://github.com/ && cd todo
  pip install -r requirements.txt
  ```
4. Install postgre and create a database for TODO app.
5. Update config.py file.
6. Run `TODO` using `python app.py`


## Sample Inputs
1. sign up using your email and password.(No token require)
    URL = `http://127.0.0.1:5000/api/v1/signup`
    Method = `POST`
    {
        "email":"email@domain.com",
        "password":"somepassword"
    }

2. sign in to the app and recieve a `x-access-token` token.(No token require)
    URL = `http://127.0.0.1:5000/api/v1/signin`
    Method = `POST`
    {
        "email":"email@domain.com",
        "password":"somepassword
    }

3. You can change you password through this API. (token require)
    URL = `http://127.0.0.1:5000/api/v1/changePassword`
    Method = `PUT`
    {
        "oldpassword":"your current password",
        "newpassword":"new strong password",
        "confirmpassword","new strong password"
    }

4. You can view all your Current todo with this API. (token require)
    URL = `http://127.0.0.1:5000/api/v1/todos/?status=OnGoing`
    Method = `GET`
    "status":"filter by status" `Optionaly you can set status one of these ('NotStarted','OnGoing','Completed') if status send empty you will get all your TODOS`

5. To create new TODO you can use this API. (token require)
    URL = `http://127.0.0.1:5000/api/v1/todos`
    Method = `POST`
    {
        "name":"Eat",
        "description":"Eat Breakfast at 9 o'clock",
        "status":"NotStarted"
    }

6. If you need to update a TODO use this API. (token require)
    URL = `http://127.0.0.1:5000/api/v1/todos`
    Method = `PUT`
    {
        "id": 1,`The Id of todo you wish to update get it fom number 4` 
        "name":"Eat",
        "description":"Eat Breakfast at 9 o'clock",
        "status":"Completed"
    }

7. If you need to Delete a TODO use this API. (token require)
    URL = `http://127.0.0.1:5000/api/v1/todos`
    Method = `DELETE`
    {
        "id":"1"`The Id of todo you wish to Delete get it fom number 4`
    }

## Run tests

To run tests in TODO app simply use `test.py`.
