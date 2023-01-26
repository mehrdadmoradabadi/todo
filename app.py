try:
    import enum
    from datetime import datetime
    from functools import wraps

    import jwt
    from flasgger import Swagger
    from flask import Flask, jsonify, request
    from flask_sqlalchemy import SQLAlchemy
    from todoManagement.todoManager import Todos
    from userManagement.userManagement import Users

    from config import configs, secretKey
except: raise Exception('Please install required packages from requirement.txt')
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{configs['postgresUsername']}:{configs['postgresPWD']}@{configs ['postgresHostname']}:{configs ['postgresPort']}/{configs ['postgresDatabase']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db.init_app(app)
app.config['SECRET_KEY'] = secretKey
swagger = Swagger(app)

def tokenRequired(func):
    @wraps(func)
    def decorated (*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token :
            return jsonify({'Alert!':'Token is missing!'})
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms='HS256')
            currentUser = Todouser.query.filter_by(Email=data['email']).first()
            if data['expiration']<= str(datetime.now()):
                return jsonify({'Alert!':'token expired! login again'})
        except:
            return jsonify({'Alert!':'Invalid token!'})
        return func(currentUser,*args,**kwargs)
    return(decorated)

class Status(enum.Enum):
    NotStarted = 'NotStarted'
    OnGoing = 'OnGoing'
    Completed = 'Completed'

class Todouser(db.Model):
    __tablename__='Todouser'
    Id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    Email =db.Column(db.String(200), nullable = False)
    Password =db.Column(db.String(200), nullable = False)
    CreatedTimestamp =db.Column(db.String(100), nullable = False)
    UpdatedTimestamp =db.Column(db.String(100), nullable = False)
    def __init__(self,Email,Password,CreatedTimestamp,UpdatedTimestamp) -> None:
        self.Email=Email
        self.Password=Password
        self.CreatedTimestamp=CreatedTimestamp
        self.UpdatedTimestamp=UpdatedTimestamp

class Todo(db.Model):
    __tablename__='Todo'
    Id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    Name =db.Column(db.String(100), nullable = False)
    Description =db.Column(db.String(400), nullable = True)
    UserId =db.Column(db.Integer, db.ForeignKey(Todouser.Id),nullable = False)
    CreatedTimestamp =db.Column(db.String(100), nullable = False)
    UpdatedTimestamp =db.Column(db.String(100), nullable = False)
    Status =db.Column(db.Enum(Status), nullable = False)
    def __init__(self,Name,Description,UserId,CreatedTimestamp:datetime,UpdatedTimestamp:datetime,Status:enum):
        self.Name=Name
        self.Description=Description
        self.CreatedTimestamp=CreatedTimestamp
        self.UpdatedTimestamp=UpdatedTimestamp
        self.Status=Status
        self.UserId=UserId
@app.route('/api/v1/todos/',methods=['GET'])
@tokenRequired
def todosget(currentUser)->object:
    """
    Get all your TODOs. accepts a json object in the body and a x-access-token then returns a Message.
    ---
    parameters:
      - in: header
        name: x-access-token
        type: string
        required: true
        description:  For authentication
      - in: query
        name: status
        type: string
        example: "OnGoing"
            
    responses:
      200:
        description: This will return Todos based on your status. if there is no status you will get all todos as object!
    """
    if request.args and 'status' in request.args:
        status =request.args['status']
    else:status =" "
    return Todos.todo(status,request.method,Todo,currentUser,db,Status)
@app.route('/api/v1/todos',methods=['POST'])
@tokenRequired
def todospost(currentUser):
    """
    Create a new Todo accepts a json object in the body and a x-access-token then returns a Message
    ---
    parameters:
      - in: header
        name: x-access-token
        type: string
        required: true
        description:  For authentication
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: "name of your todo"
            description:
              type: string
              example: "some description"
            status:
              type: string
              example: "OnGoing"
    responses:
      200:
        description: This will return a success message !
    """
    reqData =  request.get_json()
    return Todos.todo(reqData,request.method,Todo,currentUser,db,Status)
@app.route('/api/v1/todos',methods=['PUT'])
@tokenRequired
def todosput(currentUser):
    """
    Change or update your Todo. accepts a json object in the body and a x-access-token then returns a Message
    ---
    parameters:
      - in: header
        name: x-access-token
        type: string
        required: true
        description:  For authentication
      - in: body
        name: body
        schema:
          type: object
          properties:
            id:
              type: string
              example: "2"
            name:
              type: string
              example: "name of your todo"
            description:
              type: string
              example: "some description"
            status:
              type: string
              example: "OnGoing"
    responses:
      200:
        description: This will return a success message !
    """
    reqData =  request.get_json()
    return Todos.todo(reqData,request.method,Todo,currentUser,db,Status)
@app.route('/api/v1/todos',methods=['DELETE'])
@tokenRequired
def todosdel(currentUser):
    """
    Delete a Todo. accepts a json object in the body and a x-access-token then returns a Message
    ---
    parameters:
      - in: header
        name: x-access-token
        type: string
        required: true
        description:  For authentication
      - in: body
        name: body
        schema:
          type: object
          properties:
            id:
              type: string
              example: "2"
    responses:
      200:
        description: This will return a notice message !
    """
    reqData =  request.get_json()
    return Todos.todo(reqData,request.method,Todo,currentUser,db,Status)
@app.route('/api/v1/signup',methods=['POST'])
def signup():
    """
    Signup in to TODOapp accepts a json object in the body and returns a Message
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            email:
              type: string
              example: "email@domain.com"
            password:
              type: string
              example: "somepassword"
    responses:
      200:
        description: This will return a login message. in case of duplicate email you will get an alert!
    """
    reqData =  request.get_json()
    return Users.signup(db ,reqData,Todouser)
@app.route('/api/v1/signin',methods=['POST'])
def signin():
    """
    Signing in to TODOapp accepts a json object in the body and returns a TOKEN
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            email:
              type: string
              example: "email@domain.com"
            password:
              type: string
              example: "somepassword"
    responses:
      200:
        description: This will return a "x-access-token" you will need this token
    """
    reqData =  request.get_json()
    return Users.signin(reqData,Todouser,app)
@app.route('/api/v1/changePassword',methods=['PUT'])
@tokenRequired
def changePassword(currentUser):
    """
    Change your password in to TODOapp accepts a json object in the body and a x-access-token then returns a Message
    ---
    parameters:
      - in: header
        name: x-access-token
        type: string
        required: true
        description:  For authentication
      - in: body
        name: body
        schema:
          type: object
          properties:
            oldpassword:
              type: string
              example: "oldpassword"
            newpassword:
              type: string
              example: "newpassword"
            confirmpassword:
              type: string
              example: "confirmpassword"
    responses:
      200:
        description: This will return a notice message !
    """
    reqData =  request.get_json()
    return Users.changePassword(reqData,currentUser,db)
if __name__=='__main__':
    with app.app_context():
        db.create_all()
<<<<<<< HEAD
    app.run('0.0.0.0',debug=False,port=5000)
=======
    app.run('0.0.0.0',debug=False)
>>>>>>> 079454e98624b203539df87303e0e8cc5ccd055c
