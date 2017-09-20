from flask import Flask,render_template,flash,redirect,request,url_for,session,logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField
from flask_wtf.file import FileField,FileRequired
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt
# from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from functools import wraps
from werkzeug.utils import secure_filename

#<<<<----------------------------my uploads------------------------------>>>>>
from flask_wtf import FlaskForm
import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from werkzeug.wsgi import SharedDataMiddleware
from flask import send_from_directory
UPLOAD_FOLDER = 'F:\\employeeportal1\\images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -----------------------------Login/logout--------------------------------

# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/')

class ParttimeForm(FlaskForm):

  name=StringField('Name',[validators.Length(min=1,max=50)])
  fatherormothername=StringField('FatherorMother name',[validators.Length(min=1,max=50)])
  dateofbirth = DateField('Date of Birth', format='%Y-%m-%d')
  address = StringField('Address',[validators.Length(min=1,max=300)])
  phone = StringField('Phoneno',[validators.Length(min=10,max =13 )])
  email=StringField('Email Id',[validators.Length(min=2,max=50)])
  alternateno = StringField('Alternate no',[validators.Length(min=10,max =13 )])
  sscmemo = FileField('SSC memo')
  intermemo = FileField('Inter memo')
  degreememo = FileField('Degree memo')
  aadharcard = FileField('Aadhar card')
  pancard = FileField('Pan card')
  dateofjoining = DateField('Date of Joining', format='%Y-%m-%d')
  post = SelectField(u'Post', choices=[('None','None'),('Trainer','Trainer'),('Mentor','Mentor')])
  course = SelectField(u'Course', choices=[('None','None'),('UI','UI'),('Python','Python'),('Marketing','Marketing')])
  payrole = StringField('Payrole',[validators.Length(min=1,max =15 )])
  attendance = DateField('Attendance', format='%Y-%m-%d')
  remark = StringField('Remark', [validators.Length(min =2 , max = 50)])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',filename=filename))
    return render_template('upload.html')

#
@app.route('/parttime', methods = ['GET', 'POST'])

def parttime():

    form = ParttimeForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        fatherormothername = form.fatherormothername.data
        dateofbirth = form.dateofbirth.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        alternateno = form.alternateno.name
        dateofjoining = form.dateofjoining.data
        post = form.post.name
        course = form.course.data
        payrole = form.payrole.data
        attendance = form.attendance.data
        remark = form.remark.data

    # if form.validate_on_submit():
    #     sscmemo = form.sscmemo.data
    #     intermemo = form.intermemo.data
    #     degreememo = form.degreememo.data
    #     aadharcard = form.aadharcard.data
    #     pancard = form.pancard.data
        # filename = secure_filename(sscmemo.filename)
        # print(filename)
        # sscmemo.save(os.path.join(app.instance_path, 'photos', filename))

        # return '<h1>'+ name + fatherormothername + str(dateofbirth) + address + phone + email + alternateno + str(dateofjoining) + post + course + payrole + str(attendance) + remark + '</h1>'
        # return "<h1>"'sucess'"</h1>"
    return render_template('parttime.html',form = form)

class FulltimeForm(Form):
  name=StringField('Name',[validators.Length(min=1,max=50)])
  fatherormothername=StringField('FatherorMother name',[validators.Length(min=1,max=50)])
  dateofbirth = DateField('Date of Birth', format='%Y-%m-%d')
  address = StringField('Address',[validators.Length(min=1,max=300)])
  phone = StringField('Phoneno',[validators.Length(min=10,max =13 )])
  email=StringField('Email Id',[validators.Length(min=2,max=50)])
  alternateno = StringField('Alternate no',[validators.Length(min=10,max =13 )])
  sscmemo = StringField('SSC Memo',[validators.Length(min=10,max =13 )])
  intermemo = StringField('Inter Memo',[validators.Length(min=10,max =13 )])
  degreememo = StringField('Degree Memo ',[validators.Length(min=10,max =13 )])
  aadharcard = StringField('Aadhar Card',[validators.Length(min=10,max =20 )])
  pancard = StringField('Pan Card',[validators.Length(min=10,max =20 )])
  dateofjoining = DateField('Date of Joining', format='%Y-%m-%d')
  post = SelectField(u'Post', choices=[('None','None'),('Manager','Manager'),('Leader','Leader'),('Executive','Executive')])
  payrole = StringField('Payrole',[validators.Length(min=3,max =50 )])
  attendance = DateField('Attendance', format='%Y-%m-%d')
  remark = StringField('Remark', [validators.Length(min =2 , max = 50)]) 

  
@app.route('/fulltime', methods = ['GET', 'POST'])

def fulltime():
   form = FulltimeForm(request.form)
   if request.method == 'POST' and form.validate(): 
       name = form.name.data
       fatherormothername = form.fatherormothername.data
       dateofbirth = form.dateofbirth.data
       address = form.address.data
       phone = form.phone.data
       email = form.email.data
       alternateno = form.alternateno.name
       sscmemo = form.sscmemo.data 
       intermemo = form.intermemo.data 
       degreememo = form.degreememo.data
       aadharcard = form.aadharcard.data
       pancard = form.pancard.data
       dateofjoining = form.dateofjoining.data
       post = form.post.name
       payrole = form.payrole.data
       attendance = form.attendance.data
       remark = form.remark.data
       return '<h1>'+ name + fatherormothername + str(dateofbirth) + address + phone + email + alternateno + sscmemo + intermemo + degreememo + aadharcard + pancard + str(dateofjoining) + post + payrole + str(attendance) + remark + '</h1>'
   return render_template('fulltime.html',form = form)         

class InternshipForm(Form):
  name=StringField('Name',[validators.Length(min=1,max=50)])
  fatherormothername=StringField('FatherorMother name',[validators.Length(min=1,max=50)])
  dateofbirth = DateField('Date of Birth', format='%Y-%m-%d')
  address = StringField('Address',[validators.Length(min=1,max=300)])
  phone = StringField('Phoneno',[validators.Length(min=10,max =13 )])
  email=StringField('Email Id',[validators.Length(min=2,max=50)])
  alternateno = StringField('Alternate no',[validators.Length(min=10,max =13 )])
  sscmemo = StringField('SSC Memo',[validators.Length(min=10,max =13 )])
  intermemo = StringField('Inter Memo',[validators.Length(min=10,max =13 )])
  degreememo = StringField('Degree Memo',[validators.Length(min=10,max =13 )])
  aadharcard = StringField('Aadhar Card',[validators.Length(min=10,max =20)])
  pancard = StringField('Pan Card',[validators.Length(min=10,max =20 )])
  dateofjoining = DateField('Date of Joining', format='%Y-%m-%d')
  department = SelectField(u'Department', choices=[('None','None'),('UI','UI'),('Python','Python'),('Marketing','Marketing')])
  stipend = StringField('Stipend',[validators.Length(min=3,max =50 )])
  attendance = DateField('Date of Joining', format='%Y-%m-%d')
  remark = StringField('Remark', [validators.Length(min =2 , max = 50)]) 

  
@app.route('/internship', methods = ['GET', 'POST'])

def internship():
   form = InternshipForm(request.form)
   if request.method == 'POST' and form.validate(): 
       name = form.name.data
       fatherormothername = form.fatherormothername.data
       dateofbirth = form.dateofbirth.data
       address = form.address.data
       phone = form.phone.data
       email = form.email.data
       alternateno = form.alternateno.name
       sscmemo = form.sscmemo.data 
       intermemo = form.intermemo.data 
       degreememo = form.degreememo.data
       aadharcard = form.aadharcard.data
       pancard = form.pancard.data
       dateofjoining = form.dateofjoining.data
       department = form.department.data
       stipend = form.stipend.data
       attendance = form.attendance.data
       remark = form.remark.data
       return '<h1>'+ name + fatherormothername + str(dateofbirth) + address + phone + email + alternateno + sscmemo + intermemo + degreememo + aadharcard + pancard + str(dateofjoining) + department + stipend + str(attendance) + remark + '</h1>'
   return render_template('internship.html',form = form)         

#------------------------------------pase-2------------------------------------------------


if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=4000, debug=True)