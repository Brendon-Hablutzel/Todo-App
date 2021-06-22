from flask import Flask, render_template, request, url_for, redirect, abort, send_file
import database as db
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_, func



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_session = scoped_session(sessionmaker(bind=db.engine))
    category = request.args.get('category')
    if category:
        todos = db_session.query(db.Todo).filter_by(category=category).all()
    else:
        todos = db_session.query(db.Todo).all()
        category = "all"
    categories = list(set([entry[0] for entry in db_session.query(db.Todo.category).all()]))
    return render_template('home.html', todos=todos, categories=categories, current_category=category)



@app.route('/create', methods=['GET', 'POST'])
def create():
    db_session = scoped_session(sessionmaker(bind=db.engine))
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        category = request.form.get('category')
        if name and category:
            todo = db.Todo(
                name = name,
                value = value,
                category = category.lower()
            )
            db_session.add(todo)
            db_session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/download')
def download():
    db_session = scoped_session(sessionmaker(bind=db.engine))
    category = request.args.get('category')
    if not category or category == "all" or category == "All":
        todos = db_session.query(db.Todo).all()
        filename = "all_list.txt"
    else:
        todos = db_session.query(db.Todo).filter_by(category=category).all()
        filename = f"{category}_list.txt"
    with open('list.txt', 'w') as f:
        for todo in todos:
            f.write(f'{todo.name} ({todo.category})\n{todo.value}\n\n')
    return send_file(filename_or_fp='list.txt', as_attachment=True, attachment_filename=filename)



@app.route('/remove/<int:todo_id>', methods=['GET', 'POST'])
def remove(todo_id):
    db_session = scoped_session(sessionmaker(bind=db.engine))
    todo = db_session.query(db.Todo).filter_by(id=todo_id).first()
    if request.method == "POST":
        if not todo:
            abort(404)
        else:
            db_session.delete(todo)
            db_session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('remove.html', todo=todo)


@app.route('/rename', methods=['GET', 'POST'])
def rename():
    db_session = db_session = scoped_session(sessionmaker(bind=db.engine))
    todos = db_session.query(db.Todo).all()
    current_categories = list(set([todo.category for todo in todos]))
    if request.method == "POST":
        old_category = request.form.get('old')
        new_category = request.form.get('new')
        if not old_category or not new_category:
            abort(400)
        else:
            new_category = new_category.lower()
            to_update = db_session.query(db.Todo).filter_by(category=old_category).all()
            for todo in to_update:
                todo.category = new_category
            db_session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('rename.html', current_categories=current_categories)


if __name__ == "__main__":
    app.run()
