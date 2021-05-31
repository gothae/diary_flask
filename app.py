from flask import Flask, render_template, redirect, request
from flask.helpers import flash, url_for
from models import db,User,Diary
import os
from flask import session
from forms import RegisterForm, LoginForm, DiaryForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from base64 import b64encode

app = Flask(__name__)

@app.route('/main')
def main():
    userid = session.get('userid',None)
    diarytable = Diary.query.filter_by(userid = userid).order_by(Diary.diary_date.desc()).all()
    return render_template('main.html', userid=userid, diarytable=diarytable)

@app.route('/main/<int:id>')
def diary(id):
    diary = Diary.query.filter_by(id=id).first()
    if diary.diary_image:
        image = b64encode(diary.diary_image).decode('utf-8')
        return render_template('diary.html',diary=diary, image=image)
    else:
        return render_template('diary.html',diary = diary)

@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/main')
    return render_template('login.html', form=form)

@app.route('/signout',methods=['GET','POST'])
def signout():
    session.pop('userid',None)
    return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        userid = request.form.get('userid')
        userpw = request.form.get('userpw')
        userpwck = request.form.get('userpwck')

        if not(username and userid and userpw and userpwck):
            flash("모두 입력해주세요")
        elif userpw != userpwck:
            return "비밀번호가 일치하지 않습니다"
        else:
            new_user = User()
            new_user.username = username
            new_user.userid = userid
            new_user.password = userpw

            db.session.add(new_user)
            db.session.commit()
            flash("회원가입 완료")
    return render_template('signup.html', form=form)

@app.route('/uploadDiary',methods=['GET','POST'])
def uploadDiary():
    form = DiaryForm()
    if form.validate_on_submit():
        diary_title = request.form.get('diary_title')
        diary_date = request.form.get('diary_date')
        diary_content = request.form.get('diary_content')

        new_diary = Diary()

        new_diary.userid = session['userid']
        new_diary.diary_title = diary_title
        new_diary.diary_date = diary_date
        new_diary.diary_content = diary_content
        if request.files['image']:
            image = request.files['image'].read()
            new_diary.diary_image = image

        db.session.add(new_diary)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('uploadDiary.html',form=form)

@app.route('/deleteDiary/<int:id>')
def deleteDiary(id):
    diary = Diary.query.filter_by(id=id).first()
    db.session.query(Diary).filter(Diary.id == diary.id).delete()
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/updateDiary/<int:id>',methods=['GET','POST'])
def updateDiary(id):
    diary = Diary.query.filter_by(id=id).first()
    form = DiaryForm()
    if form.validate_on_submit():
        new_title = request.form.get('diary_title')
        new_date = request.form.get('diary_date')
        new_content = request.form.get('diary_content')
        if request.files['image']:
            new_image = request.files['image'].read()
            diary.diary_image = new_image

        diary.diary_title = new_title
        diary.diary_date = new_date
        diary.diary_content = new_content

        db.session.commit()
        return redirect(url_for('main'))
    
    if diary.diary_image:
        image = b64encode(diary.diary_image).decode('utf-8')
        return render_template('updateDiary.html',diary=diary, image=image, form=form)
    else:
        return render_template('updateDiary.html',diary =  diary, form=form)

if __name__ == '__main__':

    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '526553af16de8020fd3b0fbd'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   #db 생성

    app.run(debug=True)