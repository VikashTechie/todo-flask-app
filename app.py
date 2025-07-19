from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Cloud#1234567890@localhost/Flask_project'
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.Sno} - {self.title}"

# ✅ FIXED HERE
with app.app_context():
    db.create_all()

@app.route("/", methods=['Get', 'Post'])
def hello_world():
    if request.method == "POST":
        todo = Todo(title=request.form['title'], desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    return render_template("index.html", todos=Todo.query.all(), count=Todo.query.count())

@app.route("/show")
def products():
    # ✅ FIXED HERE: Use the query to fetch all todos
    count= Todo.query.count()
    all_todos = Todo.query.all()
    return redirect("/")

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(Sno=sno).first()
    # ✅ FIXED HERE: Use sno as an integer in the URL
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    else:
        return "Todo item not found", 404
    
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(Sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    print(todo.Sno)
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
