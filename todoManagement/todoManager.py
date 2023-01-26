from datetime import datetime

from flask import jsonify


class Todos:
    def todo(reqData:object,reqmethod,Todo:object,currentUser:object,db:object,Status:object):
        match (reqmethod):
            case 'GET':
                response = {"message":"","data":[]}
                if reqData not in Status._member_names_ :
                    allTodos=Todo.query.filter_by(UserId = currentUser.Id).all()
                    for todo in allTodos:
                        response['data'].append({"id":todo.Id,"name":todo.Name,"description":todo.Description,"username":currentUser.Email,"status":todo.Status.value})
                    response['message'] = "No status found. this is all your Todos"
                    return jsonify(response)
                allTodos = Todo.query.filter_by(Status = reqData,UserId = currentUser.Id).all()
                for todo in allTodos:
                    response['data'].append({"id":todo.Id,"name":todo.Name,"description":todo.Description,"username":currentUser.Email,"status":todo.Status.value})
                return jsonify(response)
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