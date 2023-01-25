try:
    import enum
    import hashlib
    from datetime import datetime, timedelta
    from functools import wraps

    import jwt
    from flask import Flask, jsonify, make_response, request, session
    from flask_sqlalchemy import SQLAlchemy

    from config import configs, secretKey
except: raise Exception('Please install required packages from requirement.txt')
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{configs['postgresUsername']}:{configs['postgresPWD']}@{configs ['postgresHostname']}:{configs ['postgresPort']}/{configs ['postgresDatabase']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db.init_app(app)
app.config['SECRET_KEY'] = secretKey

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

@app.route('/api/v1/todos',methods=['GET','POST','PUT','DELETE'])
@tokenRequired
def todos(currentUser):
    reqData =  request.get_json()
    match (request.method):
        case 'GET':
            response = []
            if 'status' not in reqData or not reqData['status'] or reqData['status'] not in Status._member_names_ :
                allTodos=Todo.query.filter_by(UserId = currentUser.Id).all()
                for todo in allTodos:
                    response.append({"Id":todo.Id,"Name":todo.Name,"Description":todo.Description,"Username":currentUser.Email,"Status":todo.Status.value})
                return jsonify({"message":f"No status found. this is all your Todos :{str(response)}"})
            allTodos = Todo.query.filter_by(Status = reqData['status'],UserId = currentUser.Id).all()
            for todo in allTodos:
                response.append({"Id":todo.Id,"Name":todo.Name,"Description":todo.Description,"Username":currentUser.Email,"Status":todo.Status.value})
            return jsonify({"message":str(response)})
        case 'POST':
            try:
                newTodo =Todo(reqData['name'],reqData['description'],currentUser.Id,str(datetime.now()),str(datetime.now()),reqData['status'])
                db.session.add(newTodo)
                db.session.commit()
                return(jsonify({"message":"successful. new TODO added"}))
            except: return(jsonify({"message":"Something went wrong Please check your input! you need name, description and status to create a TODO!"}))
        case 'PUT':
            try:
                if 'status' not in reqData or not reqData['status'] or reqData['status'] not in Status._member_names_:
                    return jsonify({'message':f'Status condition has 3 condition please use one: {Status._member_names_}'})
                updateTodo = Todo.query.filter_by(Id = reqData['id'],UserId = currentUser.Id).first()
                updateTodo.Name = reqData['name']
                updateTodo.Description = reqData['description']
                updateTodo.Status = reqData['status']
                updateTodo.UpdatedTimestamp = datetime.now()
                db.session.commit()
                return jsonify({'message':'Todo updated successfully!'})
            except: return(jsonify({"message":"Something went wrong Please check your input! you need name, description,id and status to update a TODO!"}))

        case 'DELETE':
            try:
                deleteTodo = Todo.query.filter_by(Id = reqData['id'],UserId = currentUser.Id).first()
                if not deleteTodo:
                    return jsonify({'message':'Wrong todo Id. Please try again!'})
                db.session.delete(Todo.query.filter_by(Id = reqData['id']).first())
                db.session.commit()
                return jsonify({'message':'Todo deleted successfully!'})
            except: return(jsonify({"message":"Something went wrong Please check your input! you need send todo id to delete a TODO!"}))
@app.route('/api/v1/signup',methods=['POST'])
def signup():
    reqData =  request.get_json()
    try:
        email = reqData['email']
        plainPassword = reqData['password']
        hashPassword = hashlib.md5(plainPassword.encode()).hexdigest()
        print(session.values())
        db.session.add(Todouser(email,hashPassword,str(datetime.now()),str(datetime.now())))
        db.session.commit()
        return(jsonify({"message":"successful. Now you can login"}))
    except: return(jsonify({"message":"Something went wrong Please check your input! you need Email and Password to signup"}))
@app.route('/api/v1/signin',methods=['POST'])
def signin():
    reqData =  request.get_json()
    try:
        plainPassword = reqData['password']
        hashPassword = hashlib.md5(plainPassword.encode()).hexdigest()
        user = Todouser.query.filter_by(Email = reqData['email']).first()
        if user and hashPassword == user.Password:
            session['logged_in']=True
            payload = {'expiration' : str(datetime.now() + timedelta(minutes=30)),
                        'email': reqData['email'],
                        }
            return jsonify({"x-access-token": jwt.encode(payload, 
                app.config['SECRET_KEY'],
                algorithm='HS256'
                )})
        else:
            return make_response('Unable to verify' ,403)
    except: return(jsonify({"message":"Something went wrong Please check your input! you need email and password to signin"}))
@app.route('/api/v1/changePassword',methods=['PUT'])
@tokenRequired
def changePassword(currentUser):
    try:
        reqData =  request.get_json()
        hashPassword = hashlib.md5(reqData['oldpassword'].encode()).hexdigest()
        if hashPassword == currentUser.Password and reqData['newpassword'] == reqData['confirmpassword']:
            currentUser.Password = hashlib.md5(reqData['newPassword'].encode()).hexdigest()
            db.session.commit()
        else:
            return jsonify({"message":"try again. wrong input"})
        return jsonify({"message":"password successfully changed"})
    except: return(jsonify({"message":"Something went wrong Please check your input! you need 'oldpassword','newpassword','confirmpassword' to change your password!"}))
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0',debug=True)