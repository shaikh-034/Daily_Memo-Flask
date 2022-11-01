from urllib import request
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from app import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.create_all()

class Memo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    descr = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        descr = request.form['descr']
        memo = Memo(title=title, descr=descr)
        db.session.add(memo)
        db.session.commit()
    allmemo = Memo.query.all()
    return render_template('index.html', allmemo=allmemo)

@app.route("/show")
def products():
    allmemo = Memo.query.all()
    print(allmemo)
    return "this is products page"

@app.route("/update/<int:sno>/", methods=['GET', 'POST'])
def update(sno):
    print("update.....")
    if request.method == "POST":
        title = request.form['title']
        descr = request.form['descr']
        memo = Memo.query.filter_by(sno=sno).first()
        memo.title = title
        memo.descr = descr
        db.session.add(memo)
        db.session.commit()
        return redirect("/")
    
    memo = Memo.query.filter_by(sno=sno).first()
    return render_template('update.html', memo=memo)

@app.route("/delete/<int:sno>")
def delete(sno):
    memo = Memo.query.filter_by(sno=sno).first()
    db.session.delete(memo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)