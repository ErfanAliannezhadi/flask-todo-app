from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Column, DateTime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class TodoModel(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'Todo({self.id}, {self.content[:10]}, {self.date})'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    todos = TodoModel.query.all()
    return render_template('home.html', todos=todos)


@app.route('/todo/<int:id>')
def todo_detail(id):
    todo = TodoModel.query.get(id)
    return render_template('detail.html', todo=todo)


@app.route('/todo/delete/<int:id>')
def todo_delete(id):
    todo = TodoModel.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
