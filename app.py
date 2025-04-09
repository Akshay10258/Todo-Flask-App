from flask import Flask,render_template,request,jsonify,redirect,send_from_directory
# Import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///project.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "project.db")
# db instance 
db = SQLAlchemy(app)

# Create a class to create the class model/table
class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
@app.route('/service-worker.js')
def sw():
    return send_from_directory('.', 'service-worker.js', mimetype='application/javascript')\
    
@app.route("/",methods=['POST','GET'])
def todofn():
    if request.method=='POST':
        print("this is the req",request)
        data =request.get_json()

        title=data.get("title")
        desc=data.get("desc")
        print("datra",data,title,desc)
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

        return jsonify({"message": "Todo added", "title": title, "desc": desc}), 200

    alltodo = Todo.query.all()

    return render_template('index.html',allTodo = alltodo)

def refresh_data():
    alltodo = Todo.query.all()
    return render_template('index.html',allTodo = alltodo)

@app.route("/update",methods=['POST','GET'])
def update():
    if request.method == 'POST':
        # print("this is the req",request)
        data =request.get_json()

        new_title=data.get("title")
        new_desc=data.get("desc")
        sno=data.get("sno")

        print("datra",data,new_title,new_desc,sno)

        todo = Todo.query.get_or_404(int(sno))
        

        if new_title:  # Update only if a new title is provided
            todo.title = new_title
        if new_desc:
            todo.desc = new_desc

        db.session.commit()
        refresh_data()
        return jsonify({"message": "Todo updated", "title": new_title, "desc": new_desc}), 200

    alltodo = Todo.query.all()

    return render_template('index.html',allTodo = alltodo)

@app.route("/delete/<int:sno>",methods=['POST','GET'])
def delete(sno):
    todo = Todo.query.get_or_404(int(sno))
        
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/hello")
def hello_page():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)