from flask import Flask, render_template, request, url_for, redirect, abort, send_file
import database as db


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    category = request.args.get('category')
    if category:
        todos = db.session.query(db.Todo).filter_by(category=category).all()
    else:
        todos = db.session.query(db.Todo).all()
        category = "all"
    categories = list(
        set([entry[0] for entry in db.session.query(db.Todo.category).all()]))
    db.session.remove()
    return render_template('home.html', todos=todos, categories=categories, current_category=category)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        category = request.form.get('category')
        if name and category:
            todo = db.Todo(
                name=name,
                value=value,
                category=category.lower()
            )
            db.session.add(todo)
            db.session.commit()
        db.session.remove()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/download')
def download():
    category = request.args.get('category')
    if not category or category.lower() == "all":
        todos = db.session.query(db.Todo).all()
    else:
        todos = db.session.query(db.Todo).filter_by(category=category).all()
    with open('list.txt', 'w') as f:
        for todo in todos:
            f.write(f'{todo.name} ({todo.category})\n{todo.value}\n\n')
    db.session.remove()
    return send_file('list.txt', as_attachment=True, download_name="todos.txt")


@app.route('/remove/<int:todo_id>', methods=['GET', 'POST'])
def remove(todo_id):
    todo = db.session.query(db.Todo).filter_by(id=todo_id).first()
    if request.method == "POST":
        if not todo:
            db.session.remove()
            abort(404)
        else:
            db.session.delete(todo)
            db.session.commit()
            db.session.remove()
            return redirect(url_for('index'))
    else:
        db.session.remove()
        return render_template('remove.html', todo=todo)


@app.route('/rename', methods=['GET', 'POST'])
def rename():
    todos = db.session.query(db.Todo).all()
    current_categories = list(set([todo.category for todo in todos]))
    if request.method == "POST":
        old_category = request.form.get('old')
        new_category = request.form.get('new')
        if not old_category or not new_category:
            db.session.remove()
            abort(400)
        else:
            new_category = new_category.lower()
            to_update = db.session.query(db.Todo).filter_by(
                category=old_category).all()
            for todo in to_update:
                todo.category = new_category
            db.session.remove()
            db.session.commit()
            return redirect(url_for('index'))
    else:
        db.session.remove()
        return render_template('rename.html', current_categories=current_categories)


if __name__ == "__main__":
    app.run()
