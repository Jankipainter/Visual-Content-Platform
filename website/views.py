import os.path

from flask import Blueprint,render_template,url_for,request,redirect,flash,session,send_from_directory

import app
from .model  import UserModel,Pin
from app import connection,Session,app

views=Blueprint('views',__name__,template_folder="D:/VisualContentPlatform/website/template")
static_bp=Blueprint('static',__name__,static_url_path='/static',static_folder="D:/VisualContentPlatform/website/static")
# uploads=Blueprint('uploads',__name__)

@views.route('/')
def Index():
    return render_template('index.html')

@views.route('/register',methods=['POST','GET'])
def Register():
    if request.method == 'POST':

        User_Name=request.form.get('User_Name')
        Email=request.form.get('Email')
        Password=request.form.get('Password')
        user=UserModel(connection)

        user.add_user(User_Name,Email, Password)
        flash('Register Successfullyy..','success')

        if user.get_user(Email):
            flash('Email Already Exists','error')
            return redirect(url_for('register.html'))
        else:
            return redirect(url_for('views.Index'))
    return render_template('register-2.html')

@views.route('/login',methods=['POST','GET'])
def Login():
    if request.method=='POST':
        Email=request.form['Email']
        Password=request.form['Password']
        user=UserModel(connection)
        u1=user.validate_pass(Email,Password)
        print(u1)
        if u1:
            session['loggedin']=True
            session['uid'] = u1[0]
            print(session['uid'])
            session['uname']=u1[1]
            session['email']=u1[2]
            session['reg']=u1[4]
            session['img']=u1[5]
            session['bio'] = u1[6]
            flash('Login successfully..','success')
            return redirect(url_for('views.Dashboard'))
        else:
            flash('Login failed','error')
    return render_template('login.html')

@views.route('/dash')
def Dashboard():
    return render_template('User/index.html',uname=session['uname'],img=session['img'],bio=session['bio'])

@views.route('/editUser',methods=['POST','GET'])
def EditProfile():
    if request.method=='POST':
        Email=session.get('email')
        User_Name = session.get('uname')
        Profile_Img = request.files['Profile_Img']
        Bio = request.form['Bio']
        if Profile_Img.filename !='':
            Profile_Img.save(os.path.join('D:/VisualContentPlatform/website/uploads/Profile',Profile_Img.filename))
            filePath=os.path.join('D:/VisualContentPlatform/website/uploads/Profile',Profile_Img.filename)
            session['filepath']=filePath
            print(filePath,Email,User_Name,Bio)
            user=UserModel(connection)
            success = user.edit_user(Email, User_Name, filePath, Bio)  # Assuming db.edit_user() method from your database module

            if success:
                flash('User data updated successfully', 'success')
            else:
                flash('User not found or update failed', 'error')

            return redirect(url_for('views.Dashboard'),filePath=filePath)
    return render_template('User/index.html',uname=session['uname'],filepath=session['filepath'])

@views.route('/addPin',methods=['GET','POST'])
def AddPin():
    if request.method=='POST':
        IMG_URL=request.files['IMG_URL']
        Title=request.form['Title']
        if IMG_URL.filename !='':
            IMG_URL.save(os.path.join('D:/VisualContentPlatform/website/uploads',IMG_URL.filename))
            filePath=os.path.join('D:/VisualContentPlatform/website/uploads',IMG_URL.filename)
            pin=Pin(connection)
            uid=session.get('uid')
            print(uid)
            pin.addPin(uid,Title,filePath)
            return redirect(url_for('views.Dashboard'))
    return  render_template('User/AddPin.html')

@views.route('/uploads/<filename>')
def recentPin(filename):
    pin = Pin(connection)
    filename=pin.RecentPins()
    return send_from_directory('uploads',filename)

@views.route('/logout')
def logout():
    session.clear()
    flash('log out successfullyyy','success')
    return redirect(url_for('views.Index'))