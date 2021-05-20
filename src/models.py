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
    @classmethod
    def get_all(cls):
        users = cls.query.all()
        
        return [user.to_dict() for user in users] #Por cada elemento que hay en "users" conviertemelo en diccionionario (def to_dict()) 
        #Aquí user = elemento del for "element"

    #Función para mostar los emails de los usuarios
    @classmethod
    def get_by_email(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
    
        return user.to_dict() if user else None #Si hay un "user" traémelo con diccionario filtrando el email sino devuélveme None
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.to_dict() #este es el new_user del main en la línea 83

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_dict()


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
    @classmethod
    def get_all(cls):
        todos = cls.query.all()
       
        return [task.to_dict() for task in todos]
        
    @classmethod
    def get_by_user_id(cls, user_id):
        todo = cls.query.filter_by(user_id=user_id).one_or_none()
        
        return todo.todict() if todo else None
    
    # def get_by_tag(tag):
    #     tag_todo = Todo.query.filter_by(tag=tag)
    #     tag_todo_dictionary = list(map(lambda x: x.to_dict(), tag_todo))
    #     return tag_todo_dictionary

    # def get_by_done(done):
    #     done_todo = Todo.query.filter_by(done=done)
    #     done_todo_dictionary = list(map(lambda x: x.to_dict(), done_todo))
    #     return done_todo_dictionary

    def create_todo(self):
        db.session.add(self)
        db.session.commit()
        return self.to_dict() #este es el new_todo del main en la línea 94
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_dict()

       
