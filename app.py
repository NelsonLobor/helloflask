from flask import Flask, render_template, url_for, request, redirect


#toolkit and object relational mapper for python
from flask_sqlalchemy import SQLAlchemy

#import datetime
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///root.db'

#initiliaze the db with our app settings
db = SQLAlchemy(app)

#Create the database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def _tsl_(self):
        return '<Entry %r>' &self.id

@app.route('/', methods = ['POST','GET'])
def index ():
    if request.method == 'POST':
        entry_content = request.form['content']
        new_entry = Task(content = entry_content)

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/')
        except:
            return "Error Creating Task"
    else:
        entries = Task.query.order_by(Task.date_added).all()
        return render_template('index.html', entries=entries)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_remove = Task.query.get_or_404(id)

    try: 
        db.session.delete(task_to_remove)
        db.session.commit()
        return redirect('/')
    except:
        return "Error deleting the task"


if __name__ == "__main__":
    app.run(debug=True) 
