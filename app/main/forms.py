from flask_wtf import FlaskForm
from flask import request
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from flask_babel import _, lazy_gettext as _l
from app.models import User


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
    title = StringField(_l('Title'), validators=[
        DataRequired(), Length(min=3, max=50),
        Regexp(regex='^[A-Z\d]', message='Title must begin with a capital letter or a number.')])
    choices = [
        ('-', '-'), ('Motors', 'Motors'), ('Electronics', 'Electronics'), ('Kids', 'Kids'),
        ('Wedding', 'Wedding'), ('Properties', 'Properties'), ('Fashion', 'Fashion'),
        ('Sport & Hobby', 'Sport & Hobby'), ('Free', 'Free'), ('Job', 'Job'),
        ('Agriculture', 'Agriculture'), ('Music & Education', 'Music & Education'), ('Swap', 'Swap'),
        ('House & Garden', 'House & Garden'), ('Animals', 'Animals'), ('Services', 'Services'),
        ('Find Specialist', 'Find Specialist')]

    category = SelectField(_l('Category'), choices=choices, validators=[
        DataRequired(), Regexp(regex='^(?!-)', message='Please choose the category.')])
    description = StringField(_l('Description'), validators=[DataRequired(), Length(min=1, max=1500)])
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
