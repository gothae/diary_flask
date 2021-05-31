from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userid = StringField('userid', validators=[DataRequired()])
    userpw = PasswordField('userpw', validators=[DataRequired(), EqualTo('userpwck')])
    userpwck = PasswordField('userpwck', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        def __call__(self,form,field):
            userid = form['userid'].data
            userpw = field.data
            new_user = User.query.filter_by(userid=userid).first()
            if new_user.password != userpw:
                # raise ValidationError(message % d)
                raise ValueError('비밀번호가 틀렸습니다')
    userid = StringField('userid', validators=[DataRequired()])
    userpw = PasswordField('password', validators=[DataRequired(), UserPassword()])

class DiaryForm(FlaskForm):
    diary_title = StringField('diary_title',validators=[DataRequired()])
    diary_date = StringField('diary_date',validators=[DataRequired()])
    diary_content = StringField('diary_content',validators=[DataRequired()])