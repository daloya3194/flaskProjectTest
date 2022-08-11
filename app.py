from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

my_tasks = ['Learn Flask', 'Make App']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_task = request.form['content']
        t = Task(content=new_task)
        db.session.add(t)
        db.session.commit()
        return redirect('/')
    else:
        my_tasks = Task.query.all()
        return render_template('index.html', tasks=my_tasks)


@app.route('/delete/<int:id>')
def delete(id):
    t = Task.query.get(id)
    db.session.delete(t)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    t = Task.query.get(id)
    if request.method == 'POST':
        t.content = request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', task=t)


if __name__ == '__main__':
    app.run()


# models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))


db.create_all()
