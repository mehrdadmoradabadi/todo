import hashlib
from datetime import datetime, timedelta

import jwt
from flask import jsonify


class Users:


    def signup(db:object,reqData:object,Todouser:object):
        '''
        To create a new user you need to pass all of the argumants.

        reqData => user request as JSON format.
        '''
        try:
            email = reqData['email']
            user = Todouser.query.filter_by(Email = reqData['email']).first()
            if user :
                return(jsonify({"message":"Email exist. Try to login!"})) # to filter the duplicate email addresses
            plainPassword = reqData['password']
            hashPassword = hashlib.md5(plainPassword.encode()).hexdigest()
            db.session.add(Todouser(email,hashPassword,str(datetime.now()),str(datetime.now())))
            db.session.commit()
            return(jsonify({"message":"successful. Now you can login"}))
        except: return(jsonify({"message":"Something went wrong Please check your input! you need email and password to signup"}))


    def signin(reqData:object,Todouser:object,app:object)->object:
        '''
        To signing in you need to pass all of the argumants.

        reqData => user request as JSON format.
        '''
        try:
            hashPassword = hashlib.md5(reqData['password'].encode()).hexdigest()
            user = Todouser.query.filter_by(Email = reqData['email']).first()
            if user and hashPassword == user.Password:
                payload = {'expiration' : str(datetime.now() + timedelta(minutes=30)),
                            'email': reqData['email'],
                            }
                return jsonify({"x-access-token": jwt.encode(payload, 
                    app.config['SECRET_KEY'],
                    algorithm='HS256'
                    )})
            else:
                return jsonify({"message":'Unable to verify'})
        except: return(jsonify({"message":"Something went wrong Please check your input! you need email and password to signin"}))

    
    def changePassword (reqData:object,currentUser,db:object):
        '''
        To change the password you need to pass all of the argumants.

        reqData => user request as JSON format.
        '''
        try:
            hashPassword = hashlib.md5(reqData['oldpassword'].encode()).hexdigest()
            if hashPassword == currentUser.Password and reqData['newpassword'] == reqData['confirmpassword']:
                currentUser.Password = hashlib.md5(reqData['newpassword'].encode()).hexdigest()
                db.session.commit()
                return jsonify({"message":"password successfully changed"})
            else:
                return jsonify({"message":"try again. wrong input"})
        except: return(jsonify({"message":"Something went wrong Please check your input! you need 'oldpassword','newpassword','confirmpassword' to change your password!"}))


