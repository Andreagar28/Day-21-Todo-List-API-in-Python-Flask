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

#-------Get de todos los usuarios
@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.get_all() 

    return jsonify(all_users), 200

#-------Get de todos los emails de los usuarios
@app.route('/user/<email>', methods=['GET'])
def get_users_by_email(email):
    user = User.get_by_email(email) 
    print(jsonify(user))

    return jsonify(user), 200


#aqui viene la lista de las funciones creadas en la tabla Todo

#-------Get de todos los mi tabla Todo
@app.route('/todo', methods=['GET'])
def get_todo():
    all_todos = Todo.get_all() 

    return jsonify(all_todos), 200

#-------Get de todos los user_id de mi tabla Todo
@app.route('/todo/<user_id>', methods=['GET'])
def get_todo_by_user_id(user_id):
    todo = Todo.get_by_user_id(user_id) 

    return jsonify(todo), 200





# this only runs if '$ python src/main.py' is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)