from flask import render_template, request, session
from flask_login import current_user

from app.blueprints.home import blue_home

@blue_home.route('/')
def home():
    custome_cookie = request.cookies.get('UserID','Undefined')
    print(custome_cookie)
    if current_user.is_authenticated:
        username = current_user.username
        print(username)
    return render_template('home.html')

@blue_home.route('/portal',methods = ['GET'])
def portal():
    return render_template('portal.html')
