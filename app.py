from flask import Flask,render_template,flash,redirect,request,url_for,session,logging,abort
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt
from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
import os
from functools import wraps
app=Flask(__name__)
# app.config['SECRET_KEY']='Thisissupposedtobesecret!'
gmail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shivam.vku@gmail.com'
app.config['MAIL_PASSWORD'] = '7569880950vineet'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
gmail = Mail(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskappemp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)#https://realpython.com/blog/python/the-minimum-viable-test-suite/

@app.route('/')
def home():
  return render_template('home.html')

# @app.route('/login12')
# def login12():
#   return render_template('login12.html')
#----------------------------leave------------------
class Leave(Form):
  From_email = StringField('From_Email', [validators.Length(min =2 , max = 20)])
  To_email = StringField('To_Email', [validators.Length(min =2 , max = 20)]) 
  From_date=DateField('From_date', format='%Y-%m-%d')
  To_date=DateField('To_date', format='%Y-%m-%d')
  Reason = StringField('Reason', [validators.Length(min =2 , max = 20)]) 

@app.route('/leavefrom', methods = ['GET', 'POST'])

def councling():
   form = Leave(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello')
       From_email = form.From_email.data 
       To_email = form.To_email.data 
       From_date = form.From_date.data
       To_date = form.To_date.data
       Reason = form.Reason.data
       msg = Message('Hello', sender = "'"+From_email+"'", recipients = [(To_email)])
       msg.body = "Hi  welcome to Digital lync Academy "
       gmail.send(msg)
       return render_template('home.html',form = form)
   return render_template('leave.html',form = form)


#----------------------------------------------------------
@app.route('/home')
def index():
  cur=mysql.connection.cursor()
  cur.execute('''SELECT * FROM examle''')
  rv=cur.fetchall()
  # return str(rv)

  return render_template('index.html',rv=rv)
@app.route('/home1')
def home1():
  return render_template('home1.py')
class RegisterForm(Form):
  name=StringField('Name',[validators.Length(min=1,max=50)])
  father_mother_name=StringField('father_mother_name',[validators.Length(min=4,max=50)])
  date_of_brith = DateField('date_of_brith', format='%Y-%m-%d')
  address=StringField('address',[validators.Length(min=1,max=50)])
  aadhar_number=StringField('aadhar_number',[validators.Length(min=1,max=50)])
  mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
  email=StringField('email',[validators.Length(min=2,max=50)])
  alternate_no=StringField('alternate_no',[validators.Length(min=6,max=50)])
  type1=SelectField(u'type',choices=[('None','None'),('FULLTIME','FULLTIME'),('PARTTIME','PARTTIME'),('INTENDS','INTENDS')])

@app.route('/register', methods = ['GET', 'POST'])
def register():
   form = RegisterForm(request.form)
   if request.method == 'POST' and form.validate():
       name = form.name.data
       father_mother_name = form.father_mother_name.data
       date_of_brith = form.date_of_brith.data
       address = form.address.data
       aadhar_number = form.aadhar_number.data
       mobile = form.mobile.data
       email = form.email.data
       alternate_no = form.alternate_no.data
       type1 = form.type1.data    
       # create cursor
       print(aadhar_number)
       cur = mysql.connection.cursor()

       cur.execute("INSERT INTO employees(Name,Father_Mother_Name,Date_Brith,Address,Aadhar_number,Phone_number,Email_id,Alternate_no,Type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,father_mother_name,date_of_brith,address,aadhar_number,mobile,email,alternate_no,type1))

       #commit to DB

       mysql.connection.commit()

       #close connection
       cur.close()

       flash('You are now registered and can log in','success')

       return redirect(url_for('home'))

   return render_template('register.html',form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('about'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#-----------------------------------------login----------------
@app.route('/EMPlogin',methods = ['GET','POST'])
def EMPloginn():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('home'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout1')
def EMPlogout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('EMPlogin'))


@app.route('/updateprofile')
def updateprofile():
  id=request.args.get('id')
  print('updateproile::',id)
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE id=%s",[id])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  return render_template('update.html',person=person)

@app.route('/updateprofile12')
def updateprofile12():
  name=request.args.get('st_name')
  email=request.args.get('st_email')
  
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE st_name=%s",[name])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  a=person['id']
  print(person['email'])


  cur=mysql.connection.cursor()
  cur.execute("UPDATE `registers` SET `name`=%s,`email`=%s WHERE id=%s",[name,email,a])
  print(name)
  print(email)
  print(a)
  mysql.connection.commit()

  return redirect(url_for('about'))

@app.route('/deleteprofile')
def deleteprofile():
  id=request.args.get('id')
  print("delect",id)
  cur=mysql.connection.cursor()
  cur.execute("DELETE FROM `users`  WHERE id=%s",[id])
  mysql.connection.commit()
 
  return redirect(url_for('about'))


if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=5000, debug=True)

from flask import Flask,render_template,flash,redirect,request,url_for,session,logging,abort
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt
from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
import os
from functools import wraps
app=Flask(__name__)
# app.config['SECRET_KEY']='Thisissupposedtobesecret!'
gmail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shivam.vku@gmail.com'
app.config['MAIL_PASSWORD'] = '7569880950vineet'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
gmail = Mail(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskappemp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)#https://realpython.com/blog/python/the-minimum-viable-test-suite/

@app.route('/')
def home():
  return render_template('home.html')

# @app.route('/login12')
# def login12():
#   return render_template('login12.html')
#----------------------------leave------------------
class Leave(Form):
  From_email = StringField('From_Email', [validators.Length(min =2 , max = 20)])
  To_email = StringField('To_Email', [validators.Length(min =2 , max = 20)]) 
  From_date=DateField('From_date', format='%Y-%m-%d')
  To_date=DateField('To_date', format='%Y-%m-%d')
  Reason = StringField('Reason', [validators.Length(min =2 , max = 20)]) 

@app.route('/leavefrom', methods = ['GET', 'POST'])

def councling():
   form = Leave(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello')
       From_email = form.From_email.data 
       To_email = form.To_email.data 
       From_date = form.From_date.data
       To_date = form.To_date.data
       Reason = form.Reason.data
       msg = Message('Hello', sender = "'"+From_email+"'", recipients = [(To_email)])
       msg.body = "Hi  welcome to Digital lync Academy "
       gmail.send(msg)
       return render_template('home.html',form = form)
   return render_template('leave.html',form = form)


#----------------------------------------------------------
@app.route('/home')
def index():
  cur=mysql.connection.cursor()
  cur.execute('''SELECT * FROM examle''')
  rv=cur.fetchall()
  # return str(rv)

  return render_template('index.html',rv=rv)
@app.route('/home1')
def home1():
  return render_template('home1.py')
class RegisterForm(Form):
  name=StringField('Name',[validators.Length(min=1,max=50)])
  father_mother_name=StringField('father_mother_name',[validators.Length(min=4,max=50)])
  date_of_brith = DateField('date_of_brith', format='%Y-%m-%d')
  address=StringField('address',[validators.Length(min=1,max=50)])
  aadhar_number=StringField('aadhar_number',[validators.Length(min=1,max=50)])
  mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
  email=StringField('email',[validators.Length(min=2,max=50)])
  alternate_no=StringField('alternate_no',[validators.Length(min=6,max=50)])
  type1=SelectField(u'type',choices=[('None','None'),('FULLTIME','FULLTIME'),('PARTTIME','PARTTIME'),('INTENDS','INTENDS')])

@app.route('/register', methods = ['GET', 'POST'])
def register():
   form = RegisterForm(request.form)
   if request.method == 'POST' and form.validate():
       name = form.name.data
       father_mother_name = form.father_mother_name.data
       date_of_brith = form.date_of_brith.data
       address = form.address.data
       aadhar_number = form.aadhar_number.data
       mobile = form.mobile.data
       email = form.email.data
       alternate_no = form.alternate_no.data
       type1 = form.type1.data    
       # create cursor
       print(aadhar_number)
       cur = mysql.connection.cursor()

       cur.execute("INSERT INTO employees(Name,Father_Mother_Name,Date_Brith,Address,Aadhar_number,Phone_number,Email_id,Alternate_no,Type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,father_mother_name,date_of_brith,address,aadhar_number,mobile,email,alternate_no,type1))

       #commit to DB

       mysql.connection.commit()

       #close connection
       cur.close()

       flash('You are now registered and can log in','success')

       return redirect(url_for('home'))

   return render_template('register.html',form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('about'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#-----------------------------------------login----------------
@app.route('/EMPlogin',methods = ['GET','POST'])
def EMPloginn():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('home'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout1')
def EMPlogout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('EMPlogin'))


@app.route('/updateprofile')
def updateprofile():
  id=request.args.get('id')
  print('updateproile::',id)
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE id=%s",[id])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  return render_template('update.html',person=person)

@app.route('/updateprofile12')
def updateprofile12():
  name=request.args.get('st_name')
  email=request.args.get('st_email')
  
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE st_name=%s",[name])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  a=person['id']
  print(person['email'])


  cur=mysql.connection.cursor()
  cur.execute("UPDATE `registers` SET `name`=%s,`email`=%s WHERE id=%s",[name,email,a])
  print(name)
  print(email)
  print(a)
  mysql.connection.commit()

  return redirect(url_for('about'))

@app.route('/deleteprofile')
def deleteprofile():
  id=request.args.get('id')
  print("delect",id)
  cur=mysql.connection.cursor()
  cur.execute("DELETE FROM `users`  WHERE id=%s",[id])
  mysql.connection.commit()
 
  return redirect(url_for('about'))


if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=5000, debug=True)

