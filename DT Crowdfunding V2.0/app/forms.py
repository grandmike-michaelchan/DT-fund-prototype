from flask_wtf import Form
from wtforms import StringField, PasswordField, validators

#WTF is used for data validation
#Need pip install flask-WTF before using it
#Use WTF: xxxField('Username', [validators.required('xxxx')])

#WTForm types:
#StringField-> only string is ok
#IntegerField-> only integers 
#DecimalField
#PasswordField
#BooleanField
#RadioField
#SelectField
#TextAreaField
#SubmitField

#Validators info:
#DataRequired: Check if empty 
#Email: Check valid email
#IPAddress: Check valid IP Address
#Length: password/ text liength is within expectation
#NumberRange: Set Number Range
#URL: Validate URL
#EqualTo: Check if the content is the same 


class LoginForm(Form):
    '''User Login Form validation'''

    userid = StringField('UserID：', [validators.DataRequired('Username field is required')])
    password = PasswordField('Password：', [validators.DataRequired('Password is required')])


class CustomerRegForm(Form):
    '''User Register Form validation'''

    userid = StringField('UserID：', [validators.DataRequired('UserID input is mandatory')])
    name = StringField('User Full Name：', [validators.DataRequired('Username input is mandatory')])
    password = PasswordField('User Password：', [validators.DataRequired('Password input is mandatory')])
    password2 = PasswordField('Re-Enter Password：', [validators.EqualTo('password', message='Input password is not consistent')])

    # Date validation format YYYY-MM-DD YY-MM-DD
    reg_date = r'^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
    birthday = StringField('Date of birth：', [validators.Regexp(reg_date, message='Invalid date input')])
    address = StringField('email address：')
    phone = StringField('Phone number：')
