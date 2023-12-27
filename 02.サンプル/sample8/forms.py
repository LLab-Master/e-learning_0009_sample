from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,IntegerField
from wtforms.validators import DataRequired,Length,NumberRange


class UserForm(FlaskForm):
    name = StringField('氏名',validators=[DataRequired(),Length(max=10,message='10文字以下で')])
    password = PasswordField('パスワード',validators=[DataRequired()])
    age = IntegerField('年齢',validators=[DataRequired(message='年齢は必須です')
        ,NumberRange(min=20,max=60,message='年齢が不正')])
    address = StringField('住所')
    submit = SubmitField('送信')

