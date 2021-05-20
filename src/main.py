"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
from sqlalchemy import exc
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




#-------AQUIÍ EMPIEZAN LOS GET

#-------Get de todos los usuarios
@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.get_all() 

    if all_users:
        return jsonify(all_users), 200
    return jsonify({'message': 'No users yet'}), 200

#-------Get de todos los emails de los usuarios
@app.route('/user/<email>', methods=['GET'])
def get_users_by_email(email):
    user = User.get_by_email(email) 
    
    if user:
        return jsonify(user), 200
    return jsonify({'error':'User not found'}), 404


#aqui viene la lista de las funciones creadas en la tabla Todo

#-------Get de todos los mi tabla Todo
@app.route('/todo', methods=['GET'])
def get_todo():
    all_todos = Todo.get_all() 

    if all_todos:
        return jsonify(all_todos), 200
    return jsonify({'message': 'No tasks yet'}), 200

#-------Get de todos los user_id de mi tabla Todo
@app.route('/todo/<user_id>', methods=['GET'])
def get_todo_by_user_id(user_id):
    todo = Todo.get_by_user_id(user_id) 

    if todo:
      return jsonify(todo), 200
    return jsonify({'error': 'Task not found'}), 404




#----AQUIÍ EMPIEZAN LOS POST para crear usuarios y tareas

#----POST de user

@app.route('/user', methods=['POST'])
def create_user():
    email = request.json.get("email", None)
    #password = request.json.get("password", None)
    if not email:
        return jsonify({'error': 'Missing parametre'}), 403

    user= User(email=email)
    try:
        user = user.create()
        return jsonify(user), 201
    except exc.IntegrityError:
        return jsonify({'error': 'User already exists'}), 404



#----POST de todo

@app.route('/todo', methods=['POST'])
def create_todo():
    tag = request.json.get("tag", None)
    done = request.json.get("done", None)
    user_id = request.json.get("user_id", None)

    if not tag or not done or not user_id:
        return jsonify({'error': 'Missing parameter'}), 403
    task = Todo(tag=tag, done=done, user_id=user_id)
    try:
        task = task.create_todo()
        return jsonify(task), 201
    except exc.IntegrityError:
        return jsonify({'error':'Task already exists'}), 404
        


#-----DELETE de user filtrando el email
@app.route('/user/<email>', methods=['DELETE'])
def delete_user(email):
    user = User.get_by_email(email) #línea 33 del models
    if user:
        user_delete = user.delete() #el user es el de la línea 118 del main //el delete() es de la línea 43 del models 
        return jsonify(user_delete), 204
    else:
        return 'That username does not exists', 404

#-----DELETE de todo filtrando el user_id
@app.route('/todo/<user_id>', methods=['DELETE'])
def delete_task(user_id):
    task = Todo.get_by_user_id(user_id) 
    if task:
        task_delete = task.delete() 
        return jsonify(task_delete), 204
    else:
        return 'That username does not exists', 404





#--------------------------------
# this only runs if '$ python src/main.py' is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)