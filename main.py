from flask import Flask, jsonify, render_template, redirect, request
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='sqlite:///database'

db = SQLAlchemy(app)

#define the poems table
class Poems(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_posted = db.Column(db.DateTime)
  content = db.Column(db.String(200))
  
#with app.app_context:
@app.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    poem_content = request.form['content']
    
    poem= Poems(date_posted=datetime.now(), content=poem_content)
    db.create_all()
    db.session.add(poem)
    db.session.commit()
    #print('added successfully')
  poems = Poems.query.all()
  return render_template('index.html', poems=poems)

if __name__ == '__main__':
    app.run(debug=True)
