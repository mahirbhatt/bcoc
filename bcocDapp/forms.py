from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, IntegerField


class SignUpForm(FlaskForm):
    emp_id = IntegerField('emp_id')
    password = PasswordField('psw')
    evidence_id = IntegerField('evidence_id')
    submit = SubmitField('login')