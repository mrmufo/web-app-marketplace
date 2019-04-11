from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    ads = [
        {
            'author': {'username': 'John'},
            'content': 'Yamaha FZ6 for sale!'
        },
        {
            'author': {'username': 'Susan'},
            'content': 'I sell nothing'
        }
    ]
    return render_template('index.html', title='Home Page', ads=ads)


@app.route('/new_ad')
@login_required
def new_ad_form():
    return render_template('new_ad.html')


@app.route('/new_ad', methods=['POST'])
def post_new_ad():
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # Redirect only to relative URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
