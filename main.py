from flask import Flask, jsonify, render_template, redirect, request, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='sqlite:///database'

db = SQLAlchemy(app)

#define the poems table
class Poems(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_posted = db.Column(db.DateTime)
  title = db.Column(db.String(200))
  author = db.Column(db.String(200))
  content = db.Column(db.String(200))
  
#with app.app_context:
@app.route('/')
def index():
  poems = Poems.query.all()
  return render_template('index.html', poems=poems)
  
#add poem
@app.route("/addpoem", methods=['POST', 'GET'])
def addpoem():
  if request.method == 'POST':
    poem_title = request.form['title']
    poem_content = request.form['content']
    poem_author = request.form['author']
    poem= Poems(date_posted=datetime.now(), title=poem_title, content=poem_content, author=poem_author)
    db.create_all()
    db.session.add(poem)
    db.session.commit()
    return redirect(url_for('index'))
  else:
    print('error')
  return render_template('addpoem.html')
  
@app.route('/poem/<int:poem_id>')
def poem(poem_id):
  poem = Poems.query.filter_by(id=poem_id).first()
  return render_template('poem.html', poem=poem)
  
  
@app.route('/delete/<int:poem_id>')
def delete(poem_id):
  poem_del = Poems.query.filter_by(id=poem_id).first()
  db.session.delete(poem_del)
  db.session.commit()
  return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
