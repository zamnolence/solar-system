from flask_wtf          import FlaskForm
from wtforms            import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models         import User

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username): # validate duplicated username
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists; Please use a different username.')

    def validate_email(self, email):       # validate duplicated email
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is registered with another user; Please use a different email address.')


# Edit profile form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs): # accept original username
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):                  # validate duplicated username
        if username.data != self.original_username:         # check whether username is changed
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:                            # if username is found in db (duplicated)
                raise ValidationError('Username already exists; Please use a different username.')


# Reset password request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


# Password reset form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
