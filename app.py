from flask import Flask,request,render_template,url_for,redirect,make_response,jsonify,session
from flask_sqlalchemy import SQLAlchemy
import json
import hashlib


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '#@$#erSammy'

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '707576750062313',
    'consumer_secret': '5fe0a3522470ae1c9535430c8b27491f'
}


class Notes(db.Model):
      __tablename__ = 'college_post'
      id = db.Column(db.Integer,primary_key=True)
      title = db.Column(db.String(50))
      note = db.Column(db.String(1100))
      uname = db.Column(db.String(30))
      color = db.Column(db.String(10))
      



class User(db.Model):
      __tablename__ = 'user'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(30))
      password = db.Column(db.String(50))
      useremail = db.Column(db.String(30))





@app.route("/",methods=["GET","POST"])
def index():
      if request.method=="POST":
            title = request.form['title']
            note = request.form['note']
            color = request.form['color']
            if title == "Title" and note == "Add Your Note Here.......":
                  error = "You must add title & note differ from Default"
                  return render_template('index.html',data=Notes.query.filter_by(uname=session["user"]),uname=session["user"],count=Notes.query.filter_by(uname=session["user"]).count(),error=error)
            else:
                  title = str(json.dumps(title))
                  note =str(json.dumps(note))
                  uname = session["user"]
                  data = Notes(title=title,note=note,uname=uname,color=color)
                  db.session.add(data)
                  db.session.commit()
                  return color
            
            
      else:
            if "user" in session and "email" in session:
                  return render_template('index.html',data=Notes.query.filter_by(uname=session["user"]),uname=session["user"],uemail=session["email"],count=Notes.query.filter_by(uname=session["user"]).count())
            else:
                  return render_template('login.html')



@app.route('/delete/id=<int:nid>')
def delete(nid):
      nid = str(nid)
      delete = Notes.query.filter_by(id=nid).first()
      db.session.delete(delete)
      db.session.commit()
      return redirect(url_for('index'))


@app.route('/login', methods=["GET","POST"])
def login():
      if request.method == "POST":
            uname = request.form.get('uname')
            password = request.form.get('password')
            if len(uname) == 0 and len(password) == 0:
                  return render_template('login.html',error="All Fields Required")
            else:
                  password = hashlib.md5(f'{password}'.encode()).hexdigest()
                  count = User.query.filter_by(username=uname,password=password).count()
                  if count > 0 :
                        data=User.query.filter_by(username=uname).first()
                        session["user"] = data.username
                        session["email"] = data.useremail
                        return redirect(url_for('index'))
                  else:
                        
                        return render_template('login.html',error="Invalid Username & Password")
      else:
            return render_template('login.html')


@app.route('/logout', methods=["GET"])
def logout():
      session.pop("user", None)
      return redirect(url_for('login'))
                  


@app.route('/new',methods=["GET","POST"])
def create_account():
      if request.method == "POST":
            uname = request.form.get('uname')
            password = request.form.get('password')
            uemail = request.form.get('uemail')
            count = User.query.filter_by(username=uname).count()
            if len(uname) < 6 and len(password) <6 and len(uemail) <15:
                  error = "You must choose a username and password of 6 letter long"
                  return render_template('create_account.html',error=error)
            elif count > 0 :
                  error = f"User with {uname} Already Exist"
                  return render_template('create_account.html', error=error)
            
            else:
                  data = User(username=uname,password = hashlib.md5(f'{password}'.encode()).hexdigest(),useremail=uemail)
                  db.session.add(data)
                  db.session.commit()
                  return render_template('login.html')
      else:
            return render_template('create_account.html')

            
      
      



if __name__ =="__main__":
      app.run()

