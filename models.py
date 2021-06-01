from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'usertable'
    id = db.Column(db.Integer, primary_key = True)   #userid 아님
    username = db.Column(db.String(100))
    userid = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Diary(db.Model):
    __tablename__ = 'diarytable'
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.String(100), db.ForeignKey('usertable.userid'), nullable = False)
    diary_title = db.Column(db.String(100))
    diary_date = db.Column(db.String(8))
    diary_content = db.Column(db.String(1000))
    diary_image = db.Column(db.BLOB,nullable = True)