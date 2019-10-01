from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Username already exists. Please choose a different one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Email address already exists. Please choose a different one.'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please choose a different username.'))


class AdForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(min=3, max=50)])
    choices = [
        ('all', 'All'), ('motors', 'Motors'), ('electronics', 'Electronics'), ('kids', 'Kids'),
        ('wedding', 'Wedding'), ('properties', 'Properties'), ('fashion', 'Fashion'),
        ('sportandhobby', 'Sport & Hobby'), ('free', 'Free'), ('job', 'Job'),
        ('agriculture', 'Agriculture'), ('musicandeducation', 'Music & Education'), ('swap', 'Swap'),
        ('houseandgarden', 'House & Garden'), ('animals', 'Animals'), ('services', 'Services'),
        ('findspecialist', 'Find specialist')]
    # todo update category names
    category = SelectField(_l('Category'), choices=choices, validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired(), Length(min=1, max=1500)])
    submit = SubmitField(_l('Submit'))


class AdSearchForm(FlaskForm):
    choices = [
        'All', 'Motors', 'Electronics', 'Kids', 'Wedding', 'Properties', 'Fashion', 'Sport & Hobby', 'Free', 'Job',
        'Agriculture', 'Music & Education', 'Swap', 'House & Garden', 'Animals', 'Services', 'Find specialist']
    select = SelectField('Search in category:', choices=choices)
    search = StringField('')
    # todo finish later
