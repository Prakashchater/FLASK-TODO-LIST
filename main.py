from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuioplkjhgfdsa'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

# CONFIGURE TABLE


class TodoTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean)


db.create_all()


@app.route('/')
def get_all_task():
    incomplete = TodoTable.query.filter_by(complete=False).all()
    complete = TodoTable.query.filter_by(complete=True).all()
    return render_template("index.html", incomplete=incomplete, complete=complete)


@app.route('/add', methods=["POST"])
def add_task():
    if request.method == "POST":
        new_task = TodoTable(
            task=request.form["task"],
            complete=False
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('get_all_task'))
    # return render_template("add.html")


@app.route('/edit', methods=["GET", "POST"])
def edit_task():
    if request.method == "POST":
        task_id = request.form["id"]
        task_to_update = TodoTable.query.get(task_id)
        task_to_update.task = request.form["task"]
        db.session.commit()
        return redirect(url_for('get_all_task'))
    task_id = request.args.get('id')
    task_selected = TodoTable.query.get(task_id)
    return render_template("edit.html", task=task_selected)


@app.route('/complete/<id>')
def complete(id):
    todo = TodoTable.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('get_all_task'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = TodoTable.query.get(task_id)
    db.session.delete(tasks)
    db.session.commit()
    return redirect(url_for('get_all_task'))


if __name__ == "__main__":
    app.run(debug=True)
