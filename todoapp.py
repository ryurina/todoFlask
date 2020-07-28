from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoflask.db'
db = SQLAlchemy(app)

class Todo(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		content = db.Column(db.String(50), nullable=False)
		date_created = db.Column(db.DateTime, default=datetime.utcnow)

		def __repr__(self):
				return '<Todo %r>' % self.id

@app.route("/", methods=["GET", "POST"])
def todo():
	todos = Todo.query.order_by(Todo.date_created).all()
	if request.method == "POST":
		todoTask = request.form["taskadd"]
		newTask = Todo(content=todoTask)
		try:
			db.session.add(newTask)
			db.session.commit()
			return redirect("/")
		except:
			return "Cannot add your todo"
	return render_template("index.html", todos=todos)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/deleteTask/<int:id>")
def deleteTask(id):
	taskToDelete = Todo.query.get_or_404(id)
	try:
		db.session.delete(taskToDelete)
		db.session.commit()
		return redirect("/")
	except:
		return "Cannot delete this task"
	
@app.route("/editTask/<int:id>", methods=["GET", "POST"])
def editTask(id):
	taskToEdit = Todo.query.get_or_404(id)
	if request.method == "POST":
		taskToEdit.content = request.form["taskadd"]
		try:
			db.session.commit()
			return redirect("/")
		except:
			return "Cannont edit this task"
	else:
		return render_template("editTask.html", taskToEdit=taskToEdit)

if __name__ == '__main__':
	app.run(debug=True)