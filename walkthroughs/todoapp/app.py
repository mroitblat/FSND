from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://maxroitblat@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship('Todo', backref='list', lazy=True, cascade='all, delete-orphan')

@app.route('/lists', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
        body['id'] = list.id
        body['name'] = list.name
        body['completed'] = list.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

# note: more conventionally, we would write a
# POST endpoint to /todos for the create endpoint:
# @app.route('/todos', method=['POST'])
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list = int(request.get_json()['list'])
        todo = Todo(description=description, list_id=list)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
        body['list'] = todo.list_id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_todo(list_id):
    try:
        list = TodoList.query.get(list_id)
        list.completed = True
        for todo in list.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('get_list_todos', list_id=list_id))

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        db.session.delete(list)
        db.session.commit()
        ret = jsonify({'success': True})
    except:
        db.session.rollback()
        ret = jsonify({'success': False})
        error = True
    finally:
        db.session.close()
    return ret

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        ret = jsonify({'success': True})
    except:
        db.session.rollback()
        ret = jsonify({'success': False})
    finally:
        db.session.close()
    return ret


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
    lists=TodoList.query.order_by('id').all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
    app.run()
