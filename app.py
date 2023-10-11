# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
bcrypt = Bcrypt(app)

# DB 기본 코드

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


@app.route("/")
def home():
    title = '전국팔도 구석구석'
    return render_template('home.html', data=title)

@app.route("/byuser/")
def byuser():
    return render_template('by-user.html')


@app.route('/login', methods=['GET'])
def getLogin():
    return render_template('login.html')


users = [{
    "username": 'bob1234',
    "password": "$2b$12$ZRqQ2WM/UWcFlHyTSmWb5upnpB3YzDJw97/.lgkce1e6pqcodVym6"
},
    {
    "username": 'jun1234',
    "password": "$2b$12$ZRqQ2WM/UWcFlHyTSmWb5upnpB3YzDJw97/.lgkce1e6pqcodVym6"
}]


@app.route('/login', methods=['POST'])
def postLogin():
    username = request.form.get('username')
    # user가 있는지 확인
    user = [user for user in users if user["username"] == username]

    # user 없는 경우
    error_message = '아이디 또는 비밀번호가 일치하지 않습니다'
    if not user:
        print('username not found')
        return render_template('login.html', error_message=error_message)

    # user가 있는 경우
    password = request.form.get('password')

    password_match = bcrypt.check_password_hash(user[0]["password"], password)

    # # password 틀린 경우
    if not password_match:
        print('wrong password')
        return render_template('login.html', error_message=error_message)

    return redirect(url_for('home'))


@app.route('/signup',  methods=['GET'])
def getSignup():
    return render_template('signup.html')


@app.route('/signup',  methods=['POST'])
def postSignup():
    username = request.form.get('username')

    # user가 있는지 확인
    user = [user for user in users if user["username"] == username]

    # user 있는 경우
    if user:
        print('username already exists')
        return render_template('signup.html', error_message='이미 존재하는 아이디입니다.')

    # user 없는 경우
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    # password 다른 경우
    if password1 != password2:
        print("passwords do not match")
        return render_template('signup.html', error_message='비밀번호가 일치하지 않습니다.')

    # password 같은 경우
    hashed = bcrypt.generate_password_hash(password1).decode('utf-8')
    new_user = {
        "username": username,
        "password": hashed
    }

    user.append(new_user)
    print(user)
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
