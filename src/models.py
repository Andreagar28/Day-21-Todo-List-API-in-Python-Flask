from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    have_task = db.relationship('Todo', lazy=True)

    #Función para el Print 
    def __repr__(self):
        return f'User {self.email}, {self.id}'

    #Función to dict 
    def to_dict(self):
        return {
            'id': self.id, 
            'email': self.email
        }

    #Función para mostrar todos los usurios
    def get_all():
        users = User.query.all()
        users_dictionary = list(map(lambda x: x.to_dict(), users))
        return users_dictionary
    #Función para mostar los emails de los usuarios
    def get_by_email(email):
        user = User.query.filter_by(email=email)
        user_dictionary = list(map(lambda x: x.to_dict(), user))
        return user_dictionary


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(250), unique=False, nullable=False)
    done = db.Column(db.Boolean(False), unique=False, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    
# se realiza el "__repr__" para que nos sirvan los "print()"
    def __repr__(self):
        return f'Todo {self.id}, {self.user_id}, {self.tag}, {self.done}'

# se hace una funcion "to_dict()" para que muestre en la api de manera: clave valor (tipo diccionario)
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tag': self.tag,
            'done': self.done
        }

#ahora tienes que crear tu funcion "get_all()" para que puedas mostrar todos en la tabla de Todo

    def get_all():
        todos = Todo.query.all()
        todos_dictionary = list(map(lambda x: x.to_dict(), todos))
        return todos_dictionary

    def get_by_user_id(user_id):
        todo = Todo.query.filter_by(user_id=user_id)
        todo_dictionary = list(map(lambda x: x.to_dict(), todo))
        return todo_dictionary
    
    # def get_by_tag(tag):
    #     tag_todo = Todo.query.filter_by(tag=tag)
    #     tag_todo_dictionary = list(map(lambda x: x.to_dict(), tag_todo))
    #     return tag_todo_dictionary

    # def get_by_done(done):
    #     done_todo = Todo.query.filter_by(done=done)
    #     done_todo_dictionary = list(map(lambda x: x.to_dict(), done_todo))
    #     return done_todo_dictionary

