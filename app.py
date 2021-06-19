from flask import Flask, render_template, request, url_for, redirect, abort
import database as db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_, func



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_session = scoped_session(sessionmaker(bind=db.engine))
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        category = request.form.get('category')
        if name and value and category:
            todo = db.Todo(
                name = name,
                value = value,
                category = category.lower()
            )
            db_session.add(todo)
            db_session.commit()
        return redirect(url_for('index'))
    category = request.args.get('category')
    if category:
        todos = db_session.query(db.Todo).filter_by(category=category).all()
    else:
        todos = db_session.query(db.Todo).all()
        category = "All"
    categories = list(set([entry[0] for entry in db_session.query(db.Todo.category).all()]))
    return render_template('home.html', todos=todos, categories=categories, current_category=category)



@app.route('/remove/<int:todo_id>')
def remove(todo_id):
    db_session = scoped_session(sessionmaker(bind=db.engine))
    todo = db_session.query(db.Todo).filter_by(id=todo_id).first()
    if not todo:
        abort(404)
    else:
        db_session.delete(todo)
        db_session.commit()
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)